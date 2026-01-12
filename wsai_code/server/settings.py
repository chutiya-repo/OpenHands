# IMPORTANT: LEGACY V0 CODE
# This file is part of the legacy (V0) implementation of WSAI CODE and will be removed soon as we complete the migration to V1.
# WSAI CODE V1 uses the Software Agent SDK for the agentic core and runs a new application server. Please refer to:
#   - V1 agentic core (SDK): https://github.com/WSAI CODE/software-agent-sdk
#   - V1 application server (in this repo): wsai_code/app_server/
# Unless you are working on deprecation, please avoid extending this legacy file and consult the V1 codepaths above.
# Tag: Legacy-V0
# This module belongs to the old V0 web server. The V1 application server lives under wsai_code/app_server/.
from __future__ import annotations

from pydantic import (
    BaseModel,
    ConfigDict,
    SecretStr,
)

from wsai_code.core.config.mcp_config import MCPConfig
from wsai_code.integrations.provider import CustomSecret, ProviderToken
from wsai_code.integrations.service_types import ProviderType
from wsai_code.storage.data_models.settings import Settings


class POSTProviderModel(BaseModel):
    """Settings for POST requests"""

    mcp_config: MCPConfig | None = None
    provider_tokens: dict[ProviderType, ProviderToken] = {}


class POSTCustomSecrets(BaseModel):
    """Adding new custom secret"""

    custom_secrets: dict[str, CustomSecret] = {}


class GETSettingsModel(Settings):
    """Settings with additional token data for the frontend"""

    provider_tokens_set: dict[ProviderType, str | None] | None = (
        None  # provider + base_domain key-value pair
    )
    llm_api_key_set: bool
    search_api_key_set: bool = False

    model_config = ConfigDict(use_enum_values=True)


class CustomSecretWithoutValueModel(BaseModel):
    """Custom secret model without value"""

    name: str
    description: str | None = None


class CustomSecretModel(CustomSecretWithoutValueModel):
    """Custom secret model with value"""

    value: SecretStr


class GETCustomSecrets(BaseModel):
    """Custom secrets names"""

    custom_secrets: list[CustomSecretWithoutValueModel] | None = None
