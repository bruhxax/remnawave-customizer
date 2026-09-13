__version__ = "1.0.0"

# Install the small Remnawave frontend compatibility layer before CLI modules
# import themes/proxy functions. It only changes generated CSS/proxy config;
# official Panel and Subscription Page files are never modified.
from .compat import install as _install_compat

_install_compat()
del _install_compat

# Keep the core theme engine compact while shipping a much larger preset
# collection. Extending the shared tuple here makes the same presets available
# everywhere: Panel, local Subscription Page and tests.
from . import themes as _themes
from .extra_presets import EXTRA_PRESETS as _EXTRA_PRESETS

_themes.PRESETS = _themes.PRESETS + _EXTRA_PRESETS
del _EXTRA_PRESETS

# Subscription Page has a few decorative gradients generated inline by its own
# frontend. Apply a late, reversible CSS compatibility layer for those too.
from .subpage_fixes import install as _install_subpage_fixes

_install_subpage_fixes()
del _install_subpage_fixes
