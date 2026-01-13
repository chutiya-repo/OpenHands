# IMPORTANT: LEGACY V0 CODE
# This file is part of the legacy (V0) implementation of WSAI CODE and will be removed soon as we complete the migration to V1.
# WSAI CODE V1 uses the Software Agent SDK for the agentic core and runs a new application server. Please refer to:
#   - V1 agentic core (SDK): https://github.com/wsaicode/software-agent-sdk
#   - V1 application server (in this repo): wsaicode/app_server/
# Unless you are working on deprecation, please avoid extending this legacy file and consult the V1 codepaths above.
# Tag: Legacy-V0
# This module belongs to the old V0 web server. The V1 application server lives under wsaicode/app_server/.
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from wsaicode.core.logger import wsaicode_logger as logger
from wsaicode.events.async_event_store_wrapper import AsyncEventStoreWrapper
from wsaicode.events.event_filter import EventFilter
from wsaicode.events.serialization import event_to_trajectory
from wsaicode.server.dependencies import get_dependencies
from wsaicode.server.session.conversation import ServerConversation
from wsaicode.server.utils import get_conversation

app = APIRouter(
    prefix='/api/conversations/{conversation_id}', dependencies=get_dependencies()
)


@app.get('/trajectory')
async def get_trajectory(
    conversation: ServerConversation = Depends(get_conversation),
) -> JSONResponse:
    """Get trajectory.

    This function retrieves the current trajectory and returns it.

    Args:
        request (Request): The incoming request object.

    Returns:
        JSONResponse: A JSON response containing the trajectory as a list of
        events.
    """
    try:
        async_store = AsyncEventStoreWrapper(
            conversation.event_stream, filter=EventFilter(exclude_hidden=True)
        )
        trajectory = []
        async for event in async_store:
            trajectory.append(event_to_trajectory(event))
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={'trajectory': trajectory}
        )
    except Exception as e:
        logger.error(f'Error getting trajectory: {e}', exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'trajectory': None,
                'error': f'Error getting trajectory: {e}',
            },
        )
