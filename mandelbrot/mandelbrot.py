"""The code responsible for calculating the Mandelbrot Set."""

##############################################################################
# Python imports.
from typing    import NamedTuple
from functools import cache

##############################################################################
class Point( NamedTuple ):
    """Track/calculate a single point in a Mandelbrot Set."""

    x: float
    """float: The X position of the point to track."""

    y: float
    """float: The Y position of the point to track."""

    max_iteration: int = 80
    """int: The resolution of the Mandelbrot set.

    Or, more to the point, the number of steps performed in the calculation,
    to decide if the point is stable or not. The higher this is the deeper
    you go, but the longer it takes to calculate.
    """

    @cache
    def __int__( self ) -> int:
        """Return the Mandelbrot calculation for the point.

        Returns:
            int: The number of loops to escape, or 0 if it didn't.

        Note:
            The point is considered to be stable, considered to have not
            escaped, if the ``max_iteration`` has been hit without the
            calculation going above 2.0.
        """
        c1 = complex( self.x, self.y )
        c2 = 0j
        for n in range( self.max_iteration ):
            if abs( c2 ) > 2:
                return n
            c2 = c1 + ( c2 * c2 )
        return 0

    @property
    def is_stable( self ) -> bool:
        """bool: Is the point stable?"""
        return int( self ) == 0

### mandelbrot.py ends here
