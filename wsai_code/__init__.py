# This is a namespace package - extend the path to include installed packages
# (We need to do this to support dependencies wsai_code-sdk, wsai_code-tools and wsai_code-agent-server
# which all have a top level `wsai_code`` package.)
__path__ = __import__('pkgutil').extend_path(__path__, __name__)

# Import version information for backward compatibility
from wsai_code.version import __version__, get_version

__all__ = ['__version__', 'get_version']
