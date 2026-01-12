# IMPORTANT: LEGACY V0 CODE
# This file is part of the legacy (V0) implementation of WSAI CODE and will be removed soon as we complete the migration to V1.
# WSAI CODE V1 uses the Software Agent SDK for the agentic core and runs a new application server. Please refer to:
#   - V1 agentic core (SDK): https://github.com/WSAI CODE/software-agent-sdk
#   - V1 application server (in this repo): wsai_code/app_server/
# Unless you are working on deprecation, please avoid extending this legacy file and consult the V1 codepaths above.
# Tag: Legacy-V0
# This module belongs to the old V0 web server. The V1 application server lives under wsai_code/app_server/.
from fastapi import FastAPI

from wsai_code.runtime.utils.system_stats import get_system_info


def add_health_endpoints(app: FastAPI):
    @app.get('/alive')
    async def alive():
        return {'status': 'ok'}

    @app.get('/health')
    async def health() -> str:
        return 'OK'

    @app.get('/server_info')
    async def get_server_info():
        return get_system_info()
