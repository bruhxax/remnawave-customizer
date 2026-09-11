__version__ = "0.5.0"

# Install the small Remnawave frontend compatibility layer before CLI modules
# import themes/proxy functions. It only changes our generated CSS/proxy config;
# official Panel files are never modified.
from .compat import install as _install_compat

_install_compat()
del _install_compat
