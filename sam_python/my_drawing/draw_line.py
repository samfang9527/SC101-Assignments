"""
File: 
Name:
-------------------------
TODO:
"""

from campy.graphics.gobjects import GOval, GLine
from campy.graphics.gwindow import GWindow
from campy.gui.events.mouse import onmouseclicked

SIZE = 10
window = GWindow()
coordinate = GOval(SIZE, SIZE)
count = 1
# start with one, so we can make the first remainder a zero to draw a oval


def main():
    """
    This program creates lines on an instance of GWindow class.
    There is a circle indicating the user’s first click. A line appears
    at the condition where the circle disappears as the user clicks
    on the canvas for the second time.
    """
    onmouseclicked(draw_point)


def draw_point(mouse):
    global coordinate, count
    oval = GOval(SIZE, SIZE)
    oval.filled = True
    oval.fill_color = "white"
    count += 1
    if count % 2 != 1:
        window.add(oval, mouse.x - SIZE / 2, mouse.y - SIZE / 2)
        coordinate.x = oval.x+SIZE/2
        coordinate.y = oval.y+SIZE/2
        # record the first point's position
        # if the remainder is not one means this is the first point and draw a oval
    elif count % 2 == 1:
        remove_first_point = window.get_object_at(coordinate.x, coordinate.y)
        window.remove(remove_first_point)
        # remove the first point
        oval.x = mouse.x-SIZE/2
        oval.y = mouse.y-SIZE/2
        line = GLine(coordinate.x+SIZE/2, coordinate.y+SIZE/2, oval.x+SIZE/2, oval.y+SIZE/2)
        window.add(line)
        # if the remainder is one, remove the first point and draw a line


if __name__ == "__main__":
    main()
