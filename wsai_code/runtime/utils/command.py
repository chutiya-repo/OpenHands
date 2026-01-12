import os

from wsai_code.core.config import WSAI CODEConfig
from wsai_code.core.logger import wsai_code_logger as logger
from wsai_code.runtime.plugins import PluginRequirement

DEFAULT_PYTHON_PREFIX = [
    '/wsai_code/micromamba/bin/micromamba',
    'run',
    '-n',
    'wsai_code',
    'poetry',
    'run',
]
DEFAULT_MAIN_MODULE = 'wsai_code.runtime.action_execution_server'

RUNTIME_USERNAME = os.getenv('RUNTIME_USERNAME')
RUNTIME_UID = os.getenv('RUNTIME_UID')


def get_action_execution_server_startup_command(
    server_port: int,
    plugins: list[PluginRequirement],
    app_config: WSAI CODEConfig,
    python_prefix: list[str] = DEFAULT_PYTHON_PREFIX,
    override_user_id: int | None = None,
    override_username: str | None = None,
    main_module: str = DEFAULT_MAIN_MODULE,
    python_executable: str = 'python',
) -> list[str]:
    sandbox_config = app_config.sandbox
    logger.debug(f'app_config {vars(app_config)}')
    logger.debug(f'sandbox_config {vars(sandbox_config)}')
    logger.debug(f'RUNTIME_USERNAME {RUNTIME_USERNAME}, RUNTIME_UID {RUNTIME_UID}')
    logger.debug(
        f'override_username {override_username}, override_user_id {override_user_id}'
    )

    # Plugin args
    plugin_args = []
    if plugins is not None and len(plugins) > 0:
        plugin_args = ['--plugins'] + [plugin.name for plugin in plugins]

    # Browsergym stuffs
    browsergym_args = []
    if sandbox_config.browsergym_eval_env is not None:
        browsergym_args = [
            '--browsergym-eval-env'
        ] + sandbox_config.browsergym_eval_env.split(' ')

    username = (
        override_username
        or RUNTIME_USERNAME
        or ('wsai_code' if app_config.run_as_wsai_code else 'root')
    )
    user_id = (
        override_user_id or RUNTIME_UID or (1000 if app_config.run_as_wsai_code else 0)
    )
    logger.debug(f'username {username}, user_id {user_id}')

    base_cmd = [
        *python_prefix,
        python_executable,
        '-u',
        '-m',
        main_module,
        str(server_port),
        '--working-dir',
        app_config.workspace_mount_path_in_sandbox,
        *plugin_args,
        '--username',
        username,
        '--user-id',
        str(user_id),
        *browsergym_args,
    ]

    if not app_config.enable_browser:
        base_cmd.append('--no-enable-browser')
    logger.debug(f'get_action_execution_server_startup_command: {base_cmd}')

    return base_cmd
