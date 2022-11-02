"""Simple Mandelbrot Set plotter for the terminal, done in Textual."""

##############################################################################
# Python imports.
from decimal  import Decimal
from typing   import Iterator
from operator import mul, truediv

##############################################################################
# Textual imports.
from textual.app      import App, ComposeResult
from textual.binding  import Binding
from textual.widgets  import Static, Header, Footer
from textual.reactive import reactive

##############################################################################
# Local imports.
from .mandelbrot import Point

##############################################################################
class MandelPoint( Static ):
    """Widget that handles drawing a specific point in the set."""

    point = reactive( Point( Decimal( 0 ), Decimal( 0 ) ) )
    """Point: The point in the Mandelbrot set that this cell tracks."""

    @staticmethod
    def at( x: int, y: int ) -> str:
        """Get the ID of a Mandelbrot point at a given position.

        Args:
            x (int): The X location of the cell.
            y (int): The Y location of the cell.

        Returns:
            str: The ID for the cell.
        """
        return f"point-{x}-{y}"

    def __init__( self, point_id: str, x: Decimal, y: Decimal ) -> None:
        """Initialise a point in the Mandelbrot Set.

        Args:
            x (Decimal): The X position of the point in the set.
            y (Decimal): The Y position of the point in the set.
        """
        super().__init__( id=point_id )
        self.add_class( "no-text" )
        self.point = Point( x, y )

    def watch_point( self, new_point: Point ) -> None:
        """React to the Point changing.

        Args:
            new_point (Point): The new value for the point.
        """
        # Point has moved so let's remove any class that isn't the one that
        # controls if the calculation result of the point is shown...
        self.remove_class( *filter( lambda c: c!= "no-text", self.classes ) )
        # ...and then calculate the classes again.
        self.add_class(
            "stable" if self.point.is_stable else "unstable",
            f"escape-{min( int( self.point ), 15 )}"
        )
        # Finally update the content with the new result.
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
        Binding( "up", "move( -0.1, 0 )", "Up", key_display="↑" ),
        Binding( "down", "move( 0.1, 0 )", "Down", key_display="↓" ),
        Binding( "left", "move( 0, -0.1 )", "Left", key_display="←" ),
        Binding( "right", "move( 0, 0.1 )", "Right", key_display="→" ),
        Binding( "right_square_bracket", "zoom( -1.2 )", "In", key_display="]" ),
        Binding( "left_square_bracket", "zoom( 1.2 )", "Out", key_display="[" ),
        Binding( "right_curly_bracket", "zoom( -2.0 )", "In+", key_display="}" ),
        Binding( "left_curly_bracket", "zoom( 2.0 )", "Out+", key_display="{" ),
        ( "e", "toggle_escape", "Toggle #s" ),
        ( "q", "quit", "Quit" ),
        ( "r", "remove", "Remove Test" )
    ]
    """The keyboard bindings for the app."""

    from_x = reactive( Decimal( -2.0 ) )
    to_x   = reactive( Decimal( 2.0 ) )
    from_y = reactive( Decimal( -2.5 ) )
    to_y   = reactive( Decimal( 1.5 ) )

    def refresh_title( self ) -> None:
        """Refresh the title to show the dimensions."""
        self.title = f"{self.TITLE} -- ({self.from_x:.2f}, {self.from_y:.2f} -> {self.to_x:.2f}, {self.to_y:.2f})"

    def on_mount( self ) -> None:
        """Do some stuff once the DOM is loaded."""
        self.refresh_title()

    def watch_from_x( self, _ ):
        self.refresh_title()

    def watch_from_y( self, _ ):
        self.refresh_title()

    @classmethod
    def frange( cls, r_from: Decimal, r_to: Decimal ) -> Iterator[ Decimal ]:
        """Generate a float range for the plot.

        Args:
            r_from (Decimal): The value to generate from.
            r_to (Decimal): The value to generate to.

        Yields:
            Decimal: Values between the range to fit the plot.
        """
        steps = 0
        step  = Decimal( r_to - r_from ) / Decimal( cls.SIZE )
        n     = Decimal( r_from )
        while n < r_to and steps < cls.SIZE:
            yield n
            n += Decimal( step )
            steps += 1

    def compose( self ) -> ComposeResult:
        """Compose the main screen..

        Returns:
            ComposeResult: The result of composing the screen.
        """
        yield Header()
        for col, x in enumerate( self.frange( self.from_x, self.to_x ) ):
            for row, y in enumerate( self.frange( self.from_y, self.to_y ) ):
                yield MandelPoint( MandelPoint.at( col, row ), y, x )
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

    def action_move( self, x: Decimal, y: Decimal ) -> None:
        """Move the Mandelbrot Set within the view.

        Args:
            x (Decimal): The amount to move in the X direction.
            y (Decimal): The amount to move in the Y direction.
        """

        # Move the "canvas" bounds.
        self.from_x += Decimal( x )
        self.to_x   += Decimal( x )
        self.from_y += Decimal( y )
        self.to_y   += Decimal( y )

        # Shuffle the points.
        for cell in self.query( MandelPoint ):
            cell.point += ( Decimal( y ), Decimal( x ) )

        # For some reason that I can't see right now, this isn't doing what
        # I'd expect.
        self.refresh_title()

    def action_zoom( self, zoom: Decimal ):
        """Zoom in our out.

        Args:
            zoom (Decimal): The amount to zoom by.
        """

        # Figure the operator from the sign.
        by = truediv if zoom < 0 else mul

        # We don't need the sign anymore.
        zoom = Decimal( abs( zoom ) )

        # Apply the zoom.
        self.from_x = Decimal( by( self.from_x, zoom ) )
        self.to_x   = Decimal( by( self.to_x,   zoom ) )
        self.from_y = Decimal( by( self.from_y, zoom ) )
        self.to_y   = Decimal( by( self.to_y,   zoom ) )

        # Recalculate the points.
        for col, x in enumerate( self.frange( self.from_x, self.to_x ) ):
            for row, y in enumerate( self.frange( self.from_y, self.to_y ) ):
                self.query_one(
                    f"#{MandelPoint.at( col, row )}", MandelPoint
                ).point = Point( y, x )

        # TODO: For now, ring the bell when we're done.
        self.bell()

### mandelplot.py ends here
