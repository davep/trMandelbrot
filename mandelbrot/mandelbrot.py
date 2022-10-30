"""The code responsible for calculating the Mandelbrot Set."""

##############################################################################
# Python imports.
from typing import NamedTuple

##############################################################################
class Point( NamedTuple ):
    """Track/calculate a single point in a Mandelbrot Set."""

    x: float
    """float: The X position of the point to track."""

    y: float
    """float: The Y position of the point to track."""

    resolution: int = 5000
    """int: The resolution of the Mandelbrot set.

    Or, more to the point, the number of steps performed in the calculation,
    to decide if the point is stable or not. The higher this is the deeper
    you go, but the longer it takes to calculate.
    """

    @property
    def is_stable( self ) -> bool:
        """Is the point stable?"""
        c1 = complex( self.x, self.y )
        c2 = 0
        for _ in range( self.resolution ):
            if abs( c2 ) > 2:
                return False
            c2 = c1 + ( c2 * c2 )
        return True

### mandelbrot.py ends here
