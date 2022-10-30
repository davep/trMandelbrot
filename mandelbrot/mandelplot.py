"""Simple Mandelbrot Set plotter for the terminal, done in Textual."""

##############################################################################
# Textual imports.
from textual.app     import App, ComposeResult
from textual.widgets import Static, Header, Footer

##############################################################################
# Local imports.
from .mandelbrot import Point

##############################################################################
class MandelPoint( Static ):
    """Widget that handles drawing a specific point in the set."""

    def __init__( self, x: float, y: float ) -> None:
        """Initialise a point in the Mandelbrot Set.

        Args:
            x (float): The X position of the point in the set.
            y (float): The Y position of the point in the set.
        """
        super().__init__()
        self.point = Point( x, y )

    def on_mount( self ) -> None:
        """Decide the colour of the location in the plot.

        Notes:
           For the moment this is simply a binary choice; either the point
           is in the set or not and the colour reflects that. In time this
           will be improved to add a bit more colour.
        """
        self.add_class(
            "stable" if self.point.is_stable else "unstable",
            f"escape-{min( int( self.point ), 15 )}"
        )

    def render( self ) -> str:
        """Show the escape value for the given point."""
        return "" # str( int( self.point ) )

##############################################################################
class MandelbrotPlot( App[ None ] ):
    """An app to plot a Mandelbrot Set in the terminal."""

    TITLE = "trMandelbrot -- A Terminal Mandelbrot Set Plotter"
    """str: The title of the application."""

    CSS_PATH = "mandelplot.css"
    """str: The name of the CSS file."""

    SIZE = 40
    """int: The width/height of the plot."""

    def compose( self ) -> ComposeResult:
        yield Header()
        for x in range( self.SIZE ):
            for y in range( self.SIZE ):
                yield MandelPoint(
                    ( ( 4.0 / self.SIZE ) * y ) - 3.0,
                    ( ( 4.0 / self.SIZE ) * x ) - 2.0
                )
        yield Footer()

### mandelplot.py ends here
