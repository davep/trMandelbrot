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

    point = reactive( Point( 0, 0 ) )
    """Point: The point in the Mandelbrot set that this cell tracks."""

    def __init__( self, x: float, y: float ) -> None:
        """Initialise a point in the Mandelbrot Set.

        Args:
            x (float): The X position of the point in the set.
            y (float): The Y position of the point in the set.
        """
        super().__init__()
        self.add_class( "no-text" )
        self.point = Point( x, y )

    def watch_point( self, new_point: Point ) -> None:
        """React to the Point changing.

        Args:
            new_point (Point): The new value for the point.
        """
        # TODO: need a way of setting classes to a specific list.
        self.remove_class( "stable", "unstable", *[ f"escape-{n}" for n in range( 2, 16 ) ] )
        self.add_class(
            "stable" if self.point.is_stable else "unstable",
            f"escape-{min( int( self.point ), 15 )}"
        )
        self.update( str( int( new_point ) ) )

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
        ( "up", "move( 0, -0.1 )", "Up" ),
        ( "down", "move( 0, 0.1 )", "Down" ),
        ( "left", "move( -0.1, 0 )", "Left" ),
        ( "right", "move( 0.1, 0 )", "Right" ),
        ( "e", "toggle_escape", "Toggle #s" ),
        ( "q", "quit", "Quit" ),
        ( "r", "remove", "Perform the Query.remove test" )
    ]
    """The keyboard bindings for the app."""

    from_x = -2.0
    to_x   = 2.0
    from_y = -2.5
    to_y   = 1.5

    def refresh_title( self ) -> None:
        """Refresh the title to show the dimensions."""
        self.title = f"{self.TITLE} -- ({self.from_x:.2f}, {self.from_y:.2f} -> {self.to_x:.2f}, {self.to_y:.2f})"

    def on_mount( self ) -> None:
        """Do some stuff once the DOM is loaded."""
        self.refresh_title()

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

    def action_remove( self ) -> None:
        """Perform a worst-case remove.

        Note: This doesn't do anything useful at all, it just tests a
        worst-case don't-ever-do-this thing in Textual itself. Handy for
        performance testing.
        """
        self.query( MandelPoint ).remove()

    def action_move( self, x: int, y: int ) -> None:
        """Move the Mandelbrot Set within the view.

        Args:
            x (int): The amount to move in the X direction.
            y (int): The amount to move in the Y direction.
        """

        # Move the "canvas" bounds.
        self.from_x += x
        self.to_x   += x
        self.from_y += y
        self.to_y   += y

        # Shuffle the points.
        for cell in self.query( MandelPoint ):
            cell.point += ( x, y )

        # For some reason that I can't see right now, this isn't doing what
        # I'd expect.
        self.refresh_title()

### mandelplot.py ends here
