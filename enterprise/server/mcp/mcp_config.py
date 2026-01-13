from typing import TYPE_CHECKING

from storage.api_key_store import ApiKeyStore

if TYPE_CHECKING:
    from wsaicode.core.config.wsaicode_config import WSAICodeConfig

from wsaicode.core.config.mcp_config import (
    MCPSHTTPServerConfig,
    MCPStdioServerConfig,
    WSAI CODEMCPConfig,
)
from wsaicode.core.logger import wsaicode_logger as logger


# We opt for Streamable HTTP over SSE connection to the main app server's MCP
# Reasoning:
# 1. Better performance over SSE
# 2. Allows stateless MCP client connections, essential for distributed server environments
#
# The second point is very important - any long lived stateful connections (like SSE) will
# require bespoke implementation to make sure all subsequent requests hit the same replica. It is
# also not resistant to replica pod restarts (it will kill the connection and there's no recovering from it)
# NOTE: these details are specific to the MCP protocol
class SaaSWSAI CODEMCPConfig(WSAI CODEMCPConfig):
    @staticmethod
    def create_default_mcp_server_config(
        host: str, config: 'WSAICodeConfig', user_id: str | None = None
    ) -> tuple[MCPSHTTPServerConfig | None, list[MCPStdioServerConfig]]:
        """
        Create a default MCP server configuration.

        Args:
            host: Host string
            config: WSAICodeConfig
        Returns:
            A tuple containing the default SSE server configuration and a list of MCP stdio server configurations
        """

        api_key_store = ApiKeyStore.get_instance()
        if user_id:
            api_key = api_key_store.retrieve_mcp_api_key(user_id)

            if not api_key:
                api_key = api_key_store.create_api_key(user_id, 'MCP_API_KEY', None)

            if not api_key:
                logger.error(f'Could not provision MCP API Key for user: {user_id}')
                return None, []

            return MCPSHTTPServerConfig(
                url=f'https://{host}/mcp/mcp', api_key=api_key
            ), []
        return None, []
