# IMPORTANT: LEGACY V0 CODE
# This file is part of the legacy (V0) implementation of WSAI CODE and will be removed soon as we complete the migration to V1.
# WSAI CODE V1 uses the Software Agent SDK for the agentic core and runs a new application server. Please refer to:
#   - V1 agentic core (SDK): https://github.com/WSAI CODE/software-agent-sdk
#   - V1 application server (in this repo): wsai_code/app_server/
# Unless you are working on deprecation, please avoid extending this legacy file and consult the V1 codepaths above.
# Tag: Legacy-V0
from typing import TYPE_CHECKING

import wsai_code.agenthub.loc_agent.function_calling as locagent_function_calling
from wsai_code.agenthub.codeact_agent import CodeActAgent
from wsai_code.core.config import AgentConfig
from wsai_code.core.logger import wsai_code_logger as logger
from wsai_code.llm.llm_registry import LLMRegistry

if TYPE_CHECKING:
    from wsai_code.events.action import Action
    from wsai_code.llm.llm import ModelResponse


class LocAgent(CodeActAgent):
    VERSION = '1.0'

    def __init__(
        self,
        config: AgentConfig,
        llm_registry: LLMRegistry,
    ) -> None:
        """Initializes a new instance of the LocAgent class.

        Parameters:
        - llm (LLM): The llm to be used by this agent
        - config (AgentConfig): The configuration for the agent
        """

        super().__init__(config, llm_registry)

        self.tools = locagent_function_calling.get_tools()
        logger.debug(
            f'TOOLS loaded for LocAgent: {", ".join([tool.get("function").get("name") for tool in self.tools])}'
        )

    def response_to_actions(self, response: 'ModelResponse') -> list['Action']:
        return locagent_function_calling.response_to_actions(
            response,
            mcp_tool_names=list(self.mcp_tools.keys()),
        )
