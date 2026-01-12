from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import and_, desc
from sqlalchemy.orm import sessionmaker
from storage.database import session_maker
from storage.wsai_code_pr import WSAICodePR

from wsai_code.core.logger import wsai_code_logger as logger
from wsai_code.integrations.service_types import ProviderType


@dataclass
class WSAICodePRStore:
    session_maker: sessionmaker

    def insert_pr(self, pr: WSAICodePR) -> None:
        """
        Insert a new PR or delete and recreate if repo_id and pr_number already exist.
        """
        with self.session_maker() as session:
            # Check if PR already exists
            existing_pr = (
                session.query(WSAICodePR)
                .filter(
                    WSAICodePR.repo_id == pr.repo_id,
                    WSAICodePR.pr_number == pr.pr_number,
                    WSAICodePR.provider == pr.provider,
                )
                .first()
            )

            if existing_pr:
                # Delete existing PR
                session.delete(existing_pr)
                session.flush()

            session.add(pr)
            session.commit()

    def increment_process_attempts(self, repo_id: str, pr_number: int) -> bool:
        """
        Increment the process attempts counter for a PR.

        Args:
            repo_id: Repository identifier
            pr_number: Pull request number

        Returns:
            True if PR was found and updated, False otherwise
        """
        with self.session_maker() as session:
            pr = (
                session.query(WSAICodePR)
                .filter(
                    WSAICodePR.repo_id == repo_id, WSAICodePR.pr_number == pr_number
                )
                .first()
            )

            if pr:
                pr.process_attempts += 1
                session.merge(pr)
                session.commit()
                return True
            return False

    def update_pr_wsai_code_stats(
        self,
        repo_id: str,
        pr_number: int,
        original_updated_at: datetime,
        wsai_code_helped_author: bool,
        num_wsai_code_commits: int,
        num_wsai_code_review_comments: int,
        num_wsai_code_general_comments: int,
    ) -> bool:
        """
        Update WSAI CODE statistics for a PR with row-level locking and timestamp validation.

        Args:
            repo_id: Repository identifier
            pr_number: Pull request number
            original_updated_at: Original updated_at timestamp to check for concurrent modifications
            wsai_code_helped_author: Whether WSAI CODE helped the author (1+ commits)
            num_wsai_code_commits: Number of commits by WSAI CODE
            num_wsai_code_review_comments: Number of review comments by WSAI CODE
            num_wsai_code_general_comments: Number of PR comments (not review comments) by WSAI CODE

        Returns:
            True if PR was found and updated, False if not found or timestamp changed
        """
        with self.session_maker() as session:
            # Use row-level locking to prevent concurrent modifications
            pr: WSAICodePR | None = (
                session.query(WSAICodePR)
                .filter(
                    WSAICodePR.repo_id == repo_id, WSAICodePR.pr_number == pr_number
                )
                .with_for_update()
                .first()
            )

            if not pr:
                # Current PR snapshot is stale
                logger.warning('Did not find PR {pr_number} for repo {repo_id}')
                return False

            # Check if the updated_at timestamp has changed (indicating concurrent modification)
            if pr.updated_at != original_updated_at:
                # Abort transaction - the PR was modified by another process
                session.rollback()
                return False

            # Update the WSAI CODE statistics
            pr.wsai_code_helped_author = wsai_code_helped_author
            pr.num_wsai_code_commits = num_wsai_code_commits
            pr.num_wsai_code_review_comments = num_wsai_code_review_comments
            pr.num_wsai_code_general_comments = num_wsai_code_general_comments
            pr.processed = True

            session.merge(pr)
            session.commit()
            return True

    def get_unprocessed_prs(
        self, limit: int = 50, max_retries: int = 3
    ) -> list[WSAICodePR]:
        """
        Get unprocessed PR entries from the WSAICodePR table.

        Args:
            limit: Maximum number of PRs to retrieve (default: 50)

        Returns:
            List of WSAICodePR objects that need processing
        """
        with self.session_maker() as session:
            unprocessed_prs = (
                session.query(WSAICodePR)
                .filter(
                    and_(
                        ~WSAICodePR.processed,
                        WSAICodePR.process_attempts < max_retries,
                        WSAICodePR.provider == ProviderType.GITHUB.value,
                    )
                )
                .order_by(desc(WSAICodePR.updated_at))
                .limit(limit)
                .all()
            )

            return unprocessed_prs

    @classmethod
    def get_instance(cls):
        """Get an instance of the WSAICodePRStore."""
        return WSAICodePRStore(session_maker)
