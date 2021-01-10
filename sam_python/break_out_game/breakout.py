"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 1000 / 120  # 120 frames per second.
NUM_LIVES = 3


def main():
    global NUM_LIVES
    graphics = BreakoutGraphics()
    # Add animation loop here!
    dx = 0
    dy = 0
    # check if the player still alive
    while NUM_LIVES > 0:
        # check if there are any bricks still in the window
        if graphics.get_brick_ct() > 0:
            if dx == 0 and dy == 0:
                dx = graphics.get_dx
                dy = graphics.get_dy
                pause(FRAME_RATE)
            else:
                graphics.ball.move(dx, dy)
                ball_sensor = graphics.ball_sensor(graphics.ball.x, graphics.ball.y)
                graphics.ball_action(ball_sensor)
                if ball_sensor is not None:
                    dy = graphics.get_dy
                if graphics.ball.x + graphics.ball.width > graphics.window.width or graphics.ball.x < 0:
                    dx = -dx
                if graphics.ball.y < 0:
                    dy = -dy
                if graphics.ball.y > graphics.window.height:
                    NUM_LIVES -= 1
                    dx = 0
                    dy = 0
                    graphics.reset_game()
                pause(FRAME_RATE)
        else:
            graphics.remove_ball()
            graphics.lose()
            break
    graphics.remove_ball()
    graphics.lose()


if __name__ == '__main__':
    main()
