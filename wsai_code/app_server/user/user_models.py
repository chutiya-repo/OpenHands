from wsai_code.integrations.provider import PROVIDER_TOKEN_TYPE
from wsai_code.storage.data_models.settings import Settings


class UserInfo(Settings):
    """Model for user settings including the current user id."""

    id: str | None = None


class ProviderTokenPage:
    items: list[PROVIDER_TOKEN_TYPE]
    next_page_id: str | None = None
