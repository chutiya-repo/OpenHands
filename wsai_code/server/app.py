# IMPORTANT: LEGACY V0 CODE
# This file is part of the legacy (V0) implementation of WSAI CODE and will be removed soon as we complete the migration to V1.
# WSAI CODE V1 uses the Software Agent SDK for the agentic core and runs a new application server. Please refer to:
#   - V1 agentic core (SDK): https://github.com/WSAI CODE/software-agent-sdk
#   - V1 application server (in this repo): wsai_code/app_server/
# Unless you are working on deprecation, please avoid extending this legacy file and consult the V1 codepaths above.
# Tag: Legacy-V0
# This module belongs to the old V0 web server. The V1 application server lives under wsai_code/app_server/.
import contextlib
import warnings
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi.routing import Mount

with warnings.catch_warnings():
    warnings.simplefilter('ignore')

from fastapi import (
    FastAPI,
    Request,
)
from fastapi.responses import JSONResponse

import wsai_code.agenthub  # noqa F401 (we import this to get the agents registered)
from wsai_code.app_server import v1_router
from wsai_code.app_server.config import get_app_lifespan_service
from wsai_code.integrations.service_types import AuthenticationError
from wsai_code.server.routes.conversation import app as conversation_api_router
from wsai_code.server.routes.feedback import app as feedback_api_router
from wsai_code.server.routes.files import app as files_api_router
from wsai_code.server.routes.git import app as git_api_router
from wsai_code.server.routes.health import add_health_endpoints
from wsai_code.server.routes.manage_conversations import (
    app as manage_conversation_api_router,
)
from wsai_code.server.routes.mcp import mcp_server
from wsai_code.server.routes.public import app as public_api_router
from wsai_code.server.routes.secrets import app as secrets_router
from wsai_code.server.routes.security import app as security_api_router
from wsai_code.server.routes.settings import app as settings_router
from wsai_code.server.routes.trajectory import app as trajectory_router
from wsai_code.server.shared import conversation_manager, server_config
from wsai_code.server.types import AppMode
from wsai_code.version import get_version

mcp_app = mcp_server.http_app(path='/mcp', stateless_http=True)


def combine_lifespans(*lifespans):
    # Create a combined lifespan to manage multiple session managers
    @contextlib.asynccontextmanager
    async def combined_lifespan(app):
        async with contextlib.AsyncExitStack() as stack:
            for lifespan in lifespans:
                await stack.enter_async_context(lifespan(app))
            yield

    return combined_lifespan


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with conversation_manager:
        yield


lifespans = [_lifespan, mcp_app.lifespan]
app_lifespan_ = get_app_lifespan_service()
if app_lifespan_:
    lifespans.append(app_lifespan_.lifespan)


app = FastAPI(
    title='WSAI CODE',
    description='WSAI CODE: Code Less, Make More',
    version=get_version(),
    lifespan=combine_lifespans(*lifespans),
    routes=[Mount(path='/mcp', app=mcp_app)],
)


@app.exception_handler(AuthenticationError)
async def authentication_error_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=401,
        content=str(exc),
    )


app.include_router(public_api_router)
app.include_router(files_api_router)
app.include_router(security_api_router)
app.include_router(feedback_api_router)
app.include_router(conversation_api_router)
app.include_router(manage_conversation_api_router)
app.include_router(settings_router)
app.include_router(secrets_router)
if server_config.app_mode == AppMode.WSAI_CODE:
    app.include_router(git_api_router)
if server_config.enable_v1:
    app.include_router(v1_router.router)
app.include_router(trajectory_router)
add_health_endpoints(app)
