"""Very simple Mandelbrot set plotter in the terminal.

Built as a quick and dirty test of Textual.
"""

##############################################################################
# Local imports.
from .mandelplot import MandelbrotPlot

##############################################################################
# Main entry point.
if __name__ == "__main__":
    MandelbrotPlot().run()

### __main__.py ends here
