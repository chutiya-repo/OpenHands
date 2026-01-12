# IMPORTANT: LEGACY V0 CODE
# This file is part of the legacy (V0) implementation of WSAI CODE and will be removed soon as we complete the migration to V1.
# WSAI CODE V1 uses the Software Agent SDK for the agentic core and runs a new application server. Please refer to:
#   - V1 agentic core (SDK): https://github.com/WSAI CODE/software-agent-sdk
#   - V1 application server (in this repo): wsai_code/app_server/
# Unless you are working on deprecation, please avoid extending this legacy file and consult the V1 codepaths above.
# Tag: Legacy-V0
# This module belongs to the old V0 web server. The V1 application server lives under wsai_code/app_server/.
import os

from wsai_code.core.logger import wsai_code_logger as logger
from wsai_code.server.types import AppMode, ServerConfigInterface
from wsai_code.utils.import_utils import get_impl


class ServerConfig(ServerConfigInterface):
    config_cls = os.environ.get('WSAI_CODE_CONFIG_CLS', None)
    app_mode = AppMode.WSAI_CODE
    posthog_client_key = 'phc_3ESMmY9SgqEAGBB6sMGK5ayYHkeUuknH2vP6FmWH9RA'
    github_client_id = os.environ.get('GITHUB_APP_CLIENT_ID', '')
    enable_billing = os.environ.get('ENABLE_BILLING', 'false') == 'true'
    hide_llm_settings = os.environ.get('HIDE_LLM_SETTINGS', 'false') == 'true'
    # This config is used to hide the microagent management page from the users for now. We will remove this once we release the new microagent management page.
    settings_store_class: str = (
        'wsai_code.storage.settings.file_settings_store.FileSettingsStore'
    )
    secret_store_class: str = (
        'wsai_code.storage.secrets.file_secrets_store.FileSecretsStore'
    )
    conversation_store_class: str = (
        'wsai_code.storage.conversation.file_conversation_store.FileConversationStore'
    )
    conversation_manager_class: str = os.environ.get(
        'CONVERSATION_MANAGER_CLASS',
        'wsai_code.server.conversation_manager.standalone_conversation_manager.StandaloneConversationManager',
    )
    monitoring_listener_class: str = 'wsai_code.server.monitoring.MonitoringListener'
    user_auth_class: str = (
        'wsai_code.server.user_auth.default_user_auth.DefaultUserAuth'
    )
    enable_v1: bool = os.getenv('ENABLE_V1') != '0'

    def verify_config(self):
        if self.config_cls:
            raise ValueError('Unexpected config path provided')

    def get_config(self):
        config = {
            'APP_MODE': self.app_mode,
            'GITHUB_CLIENT_ID': self.github_client_id,
            'POSTHOG_CLIENT_KEY': self.posthog_client_key,
            'FEATURE_FLAGS': {
                'ENABLE_BILLING': self.enable_billing,
                'HIDE_LLM_SETTINGS': self.hide_llm_settings,
            },
        }

        return config


def load_server_config() -> ServerConfig:
    config_cls = os.environ.get('WSAI_CODE_CONFIG_CLS', None)
    logger.info(f'Using config class {config_cls}')

    server_config_cls = get_impl(ServerConfig, config_cls)
    server_config: ServerConfig = server_config_cls()
    server_config.verify_config()

    return server_config
