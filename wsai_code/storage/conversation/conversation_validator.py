import os
from datetime import datetime, timezone

from wsai_code.core.config.utils import load_wsai_code_config
from wsai_code.core.logger import wsai_code_logger as logger
from wsai_code.server.config.server_config import ServerConfig
from wsai_code.storage.conversation.conversation_store import ConversationStore
from wsai_code.storage.data_models.conversation_metadata import ConversationMetadata
from wsai_code.utils.conversation_summary import get_default_conversation_title
from wsai_code.utils.import_utils import get_impl


class ConversationValidator:
    """Abstract base class for validating conversation access.

    This is an extension point in WSAI CODE that allows applications to customize how
    conversation access is validated. Applications can substitute their own implementation by:
    1. Creating a class that inherits from ConversationValidator
    2. Implementing the validate method
    3. Setting WSAI_CODE_CONVERSATION_VALIDATOR_CLS environment variable to the fully qualified name of the class

    The class is instantiated via get_impl() in create_conversation_validator().

    The default implementation performs no validation and returns None, None.
    """

    async def validate(
        self,
        conversation_id: str,
        cookies_str: str,
        authorization_header: str | None = None,
    ) -> str | None:
        user_id = None
        metadata = await self._ensure_metadata_exists(conversation_id, user_id)
        return metadata.user_id

    async def _ensure_metadata_exists(
        self,
        conversation_id: str,
        user_id: str | None,
    ) -> ConversationMetadata:
        config = load_wsai_code_config()
        server_config = ServerConfig()

        conversation_store_class: type[ConversationStore] = get_impl(
            ConversationStore,
            server_config.conversation_store_class,
        )
        conversation_store = await conversation_store_class.get_instance(
            config, user_id
        )

        try:
            metadata = await conversation_store.get_metadata(conversation_id)
        except FileNotFoundError:
            logger.info(
                f'Creating new conversation metadata for {conversation_id}',
                extra={'session_id': conversation_id},
            )
            await conversation_store.save_metadata(
                ConversationMetadata(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    title=get_default_conversation_title(conversation_id),
                    last_updated_at=datetime.now(timezone.utc),
                    selected_repository=None,
                )
            )
            metadata = await conversation_store.get_metadata(conversation_id)
        return metadata


def create_conversation_validator() -> ConversationValidator:
    conversation_validator_cls = os.environ.get(
        'WSAI_CODE_CONVERSATION_VALIDATOR_CLS',
        'wsai_code.storage.conversation.conversation_validator.ConversationValidator',
    )
    ConversationValidatorImpl = get_impl(
        ConversationValidator, conversation_validator_cls
    )
    return ConversationValidatorImpl()
