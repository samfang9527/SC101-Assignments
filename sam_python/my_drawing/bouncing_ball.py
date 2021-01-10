"""
File: 
Name:
-------------------------
TODO:
"""

from campy.graphics.gobjects import GOval
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
from campy.gui.events.mouse import onmouseclicked
from campy.graphics.gimage import GImage

VX = 3
DELAY = 10
GRAVITY = 1
SIZE = 20
REDUCE = 0.9
START_X = 30
START_Y = 40

window = GWindow(800, 500, title='bouncing_ball.py')
ball = GOval(SIZE, SIZE)
count = 0


def main():
    """
    This program simulates a bouncing ball at (START_X, START_Y)
    that has VX as x velocity and 0 as y velocity. Each bounce reduces
    y velocity to REDUCE of itself.
    """
    ball.filled = True
    window.add(ball, START_X, START_Y)
    onmouseclicked(isaac_newton)


def isaac_newton(event):
    global ball, count
    dy = GRAVITY
    if ball.x == START_X and ball.y == START_Y:
        # only react to mouse click when the ball is at the start point
        while count < 3:
            # control the playtime
            ball.move(VX, dy)
            # move of the ball in every loop
            dy += GRAVITY
            # plus one gravity to accelerate the drop speed
            if ball.y + SIZE >= window.height:
                dy = -dy * REDUCE
                # if the ball is going out of the window, change the speed to negative and times reduce rate
                if ball.x > window.width:
                    window.add(ball, START_X, START_Y)
                    count += 1
                    break
                    # stop the loop when the ball is out of the window
            pause(DELAY)


if __name__ == "__main__":
    main()
