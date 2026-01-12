import os
from uuid import UUID

from pydantic import BaseModel

from wsai_code.core.config.wsai_code_config import WSAI CODEConfig
from wsai_code.core.logger import wsai_code_logger as logger
from wsai_code.sdk import Agent
from wsai_code.server.session.conversation_init_data import ConversationInitData
from wsai_code.server.shared import file_store
from wsai_code.storage.locations import get_experiment_config_filename
from wsai_code.utils.import_utils import get_impl


class ExperimentConfig(BaseModel):
    config: dict[str, str] | None = None


def load_experiment_config(conversation_id: str) -> ExperimentConfig | None:
    try:
        file_path = get_experiment_config_filename(conversation_id)
        exp_config = file_store.read(file_path)
        return ExperimentConfig.model_validate_json(exp_config)

    except FileNotFoundError:
        pass
    except Exception as e:
        logger.warning(f'Failed to load experiment config: {e}')

    return None


class ExperimentManager:
    @staticmethod
    def run_agent_variant_tests__v1(
        user_id: str | None, conversation_id: UUID, agent: Agent
    ) -> Agent:
        return agent

    @staticmethod
    def run_conversation_variant_test(
        user_id: str | None,
        conversation_id: str,
        conversation_settings: ConversationInitData,
    ) -> ConversationInitData:
        return conversation_settings

    @staticmethod
    def run_config_variant_test(
        user_id: str | None, conversation_id: str, config: WSAI CODEConfig
    ) -> WSAI CODEConfig:
        exp_config = load_experiment_config(conversation_id)
        if exp_config and exp_config.config:
            agent_cfg = config.get_agent_config(config.default_agent)
            try:
                for attr, value in exp_config.config.items():
                    if hasattr(agent_cfg, attr):
                        logger.info(
                            f'Set attrib {attr} to {value} for {conversation_id}'
                        )
                        setattr(agent_cfg, attr, value)
            except Exception as e:
                logger.warning(f'Error processing exp config: {e}')

        return config


experiment_manager_cls = os.environ.get(
    'WSAI_CODE_EXPERIMENT_MANAGER_CLS',
    'wsai_code.experiments.experiment_manager.ExperimentManager',
)
ExperimentManagerImpl = get_impl(ExperimentManager, experiment_manager_cls)
