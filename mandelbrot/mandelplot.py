"""Simple Mandelbrot Set plotter for the terminal, done in Textual."""

##############################################################################
# Python imports.
from decimal import Decimal
from typing  import Iterator

##############################################################################
# Textual imports.
from textual.app      import App, ComposeResult
from textual.widgets  import Static, Header, Footer
from textual.reactive import reactive

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
        """Decide the colour of the location in the plot."""
        self.add_class(
            "no-text",
            "stable" if self.point.is_stable else "unstable",
            f"escape-{min( int( self.point ), 15 )}"
        )

    def render( self ) -> str:
        """Show the escape value for the given point."""
        return str( int( self.point ) )

##############################################################################
class MandelbrotPlot( App[ None ] ):
    """An app to plot a Mandelbrot Set in the terminal."""

    TITLE = "trMandelbrot -- A Terminal Mandelbrot Set Plotter"
    """str: The title of the application."""

    CSS_PATH = "mandelplot.css"
    """str: The name of the CSS file."""

    SIZE = 40
    """int: The width/height of the plot."""

    BINDINGS = [
        ( "q", "quit", "Quit" ),
        ( "e", "toggle_escape", "Toggle #s" )
    ]
    """The keyboard bindings for the app."""

    from_x = reactive( -2.0 )
    to_x   = reactive( 2.0 )
    from_y = reactive( -2.5 )
    to_y   = reactive( 1.5 )

    def on_mount( self ) -> None:
        """Initialise some things once the DOM has been loaded."""
        self.title = f"{self.TITLE} -- ({self.from_x:.2f}, {self.from_y:.2f} -> {self.to_x:.2f}, {self.to_y:.2f})"

    @classmethod
    def frange( cls, r_from: float, r_to: float ) -> Iterator[ float ]:
        """Generate a float range for the plot.

        Args:
            r_from (float): The value to generate from.
            r_to (float): The value to generate to.

        Yields:
            float: Values between the range to fit the plot.
        """
        step = Decimal( r_to - r_from ) / Decimal( cls.SIZE )
        n    = Decimal( r_from )
        while n < r_to:
            yield float( n )
            n += Decimal( step )

    def compose( self ) -> ComposeResult:
        """Compose the main screen..

        Returns:
            ComposeResult: The result of composing the screen.
        """
        yield Header()
        for x in self.frange( self.from_x, self.to_x ):
            for y in self.frange( self.from_y, self.to_y ):
                yield MandelPoint( y, x )
        yield Footer()

    def action_toggle_escape( self ) -> None:
        """Toggle the display of the escape values for each cell."""
        self.query( MandelPoint ).toggle_class( "no-text" )

### mandelplot.py ends here
