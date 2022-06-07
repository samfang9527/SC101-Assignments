"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao

Please execute this file to start the game.
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
import time

FRAME_RATE = 1000 / 120  # 120 frames per second.


def main():
    graphics = BreakoutGraphics()
    # main loop
    while True:

        # start and restart page
        if graphics.get_page() == 0 or graphics.get_page() == 2:
            graphics.start_page()
            while True:
                pause(FRAME_RATE)
                if graphics.get_page() != 0 or graphics.get_page != 2:
                    break

        # game page
        elif graphics.get_page() == 1:
            graphics.game_reset()
            graphics.draw_bricks()
            ball = graphics.get_ball()
            window = graphics.get_window()
            while graphics.get_lives() > 0:
                pause(FRAME_RATE)
                ball.move(graphics.get_ball_velocity()[0], graphics.get_ball_velocity()[1])
                if 0 > ball.x or ball.x + ball.width > window.width:
                    if ball.x < 0:
                        ball.x = 0
                    elif ball.x + ball.width > window.width:
                        ball.x = window.width - ball.width
                    graphics.set_ball_velocity(x=-1)
                if 0 > ball.y:
                    ball.y = 0
                    graphics.set_ball_velocity(y=-1)
                graphics.detect_collision()
                graphics.wind()
                if ball.y > window.height:
                    graphics.set_lives()
                    graphics.game_reset()
                    graphics.draw_bricks()
                if graphics.check_over():
                    break
            graphics.set_page(2)


if __name__ == '__main__':
    main()
