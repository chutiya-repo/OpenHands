"""Tests for the setup script."""

from unittest.mock import patch

from conftest import (
    _load_runtime,
)

from wsaicode.core.setup import initialize_repository_for_runtime
from wsaicode.events.action import FileReadAction, FileWriteAction
from wsaicode.events.observation import FileReadObservation, FileWriteObservation
from wsaicode.integrations.service_types import ProviderType, Repository


def test_initialize_repository_for_runtime(temp_dir, runtime_cls, run_as_wsaicode):
    """Test that the initialize_repository_for_runtime function works."""
    runtime, config = _load_runtime(temp_dir, runtime_cls, run_as_wsaicode)
    mock_repo = Repository(
        id='1232',
        full_name='WSAI CODE/WSAI CODE',
        git_provider=ProviderType.GITHUB,
        is_public=True,
    )

    with patch(
        'wsaicode.runtime.base.ProviderHandler.verify_repo_provider',
        return_value=mock_repo,
    ):
        repository_dir = initialize_repository_for_runtime(
            runtime, selected_repository='WSAI CODE/WSAI CODE'
        )

    assert repository_dir is not None
    assert repository_dir == 'WSAI CODE'


def test_maybe_run_setup_script(temp_dir, runtime_cls, run_as_wsaicode):
    """Test that setup script is executed when it exists."""
    runtime, config = _load_runtime(temp_dir, runtime_cls, run_as_wsaicode)

    setup_script = '.wsaicode/setup.sh'
    write_obs = runtime.write(
        FileWriteAction(
            path=setup_script, content="#!/bin/bash\necho 'Hello World' >> README.md\n"
        )
    )
    assert isinstance(write_obs, FileWriteObservation)

    # Run setup script
    runtime.maybe_run_setup_script()

    # Verify script was executed by checking output
    read_obs = runtime.read(FileReadAction(path='README.md'))
    assert isinstance(read_obs, FileReadObservation)
    assert read_obs.content == 'Hello World\n'


def test_maybe_run_setup_script_with_long_timeout(
    temp_dir, runtime_cls, run_as_wsaicode
):
    """Test that setup script is executed when it exists."""
    runtime, config = _load_runtime(
        temp_dir,
        runtime_cls,
        run_as_wsaicode,
        runtime_startup_env_vars={'NO_CHANGE_TIMEOUT_SECONDS': '1'},
    )

    setup_script = '.wsaicode/setup.sh'
    write_obs = runtime.write(
        FileWriteAction(
            path=setup_script,
            content="#!/bin/bash\nsleep 3 && echo 'Hello World' >> README.md\n",
        )
    )
    assert isinstance(write_obs, FileWriteObservation)

    # Run setup script
    runtime.maybe_run_setup_script()

    # Verify script was executed by checking output
    read_obs = runtime.read(FileReadAction(path='README.md'))
    assert isinstance(read_obs, FileReadObservation)
    assert read_obs.content == 'Hello World\n'
