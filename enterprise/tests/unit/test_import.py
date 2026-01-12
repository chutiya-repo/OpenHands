from server.auth.sheets_client import GoogleSheetsClient

from wsai_code.core.logger import wsai_code_logger


def test_import():
    assert wsai_code_logger is not None
    assert GoogleSheetsClient is not None
