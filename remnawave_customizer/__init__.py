__version__ = "0.6.0"

# Install the small Remnawave frontend compatibility layer before CLI modules
# import themes/proxy functions. It only changes generated CSS/proxy config;
# official Panel and Subscription Page files are never modified.
from .compat import install as _install_compat

_install_compat()
del _install_compat
