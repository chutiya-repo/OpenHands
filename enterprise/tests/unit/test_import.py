from server.auth.sheets_client import GoogleSheetsClient

from wsaicode.core.logger import wsaicode_logger


def test_import():
    assert wsaicode_logger is not None
    assert GoogleSheetsClient is not None
