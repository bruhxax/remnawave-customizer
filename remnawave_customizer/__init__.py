__version__ = "0.6.1"

# Install the small Remnawave frontend compatibility layer before CLI modules
# import themes/proxy functions. It only changes generated CSS/proxy config;
# official Panel and Subscription Page files are never modified.
from .compat import install as _install_compat

_install_compat()
del _install_compat

# Subscription Page has a few decorative gradients generated inline by its own
# frontend. Apply a late, reversible CSS compatibility layer for those too.
from .subpage_fixes import install as _install_subpage_fixes

_install_subpage_fixes()
del _install_subpage_fixes
