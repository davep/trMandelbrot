# trMandelbrot

## Background

![Evil](img/evil.jpg)

This started out as, and for now remains as, a not-very-efficient Mandelbrot
Set plotter for the Terminal. It is written in Python, using
[Textual](https://textual.textualize.io/); written in part as a
demonstration but mostly as a really harsh test of the library.

![Evil](img/set1.jpg)

## More details

There is a lot about this code that doesn't exactly make it a well-written
Textual application; or rather much of it *is* doing Textual properly, but
in some key areas it very much takes a "if you were to do this, don't do it
like this" approach. As suggested above, this is on purpose. The code has
proven to be, and continues to be, a rather good stress-test of the library.

![Evil](img/set2.jpg)

Eventually, when the sorts of performance issues this code tests are taken
care of, I'll likely do a rewrite to make it far more efficient. Until then
though, if you're tempted to submit improvements, please don't be offended
if I don't accept them -- improvements aren't quite what this code needs
right now. ;-)

[//]: # (README.md ends here)
