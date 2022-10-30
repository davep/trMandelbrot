"""Terminal-based Mandelbrot generator.

Written with Textual.
"""

######################################################################
# Main library information.
__author__     = "Dave Pearson"
__copyright__  = "Copyright 2022, Dave Pearson"
__credits__    = [ "Dave Pearson" ]
__maintainer__ = "Dave Pearson"
__email__      = "davep@davep.org"
__version__    = "0.0.1"
__licence__    = "GPLv3+"

##############################################################################
# Make the app class available via easy import.
from .mandelplot import MandelbrotPlot

##############################################################################
# Export the main app class.
__all__ = [ "MandelbrotPlot" ]

### __init__.py ends here
