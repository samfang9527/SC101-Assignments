"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

This is the class of a simple breakout game, have fun!
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from campy.gui.events.timer import pause
import random
import time

# CONSTANT
BRICK_SPACING = 5       # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40        # Height of a brick (in pixels).
BRICK_HEIGHT = 15       # Height of a brick (in pixels).
BRICK_ROWS = 10         # Number of rows of bricks.
BRICK_COLS = 15         # Number of columns of bricks.
BRICK_OFFSET = 50       # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 20        # Radius of the ball (in pixels).
PADDLE_WIDTH = 100      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15      # Height of the paddle (in pixels).
PADDLE_OFFSET = 50      # Vertical offset of the paddle from the window bottom (in pixels).
LABEL_SPACING = 10      # The space bwtween each label.
PROGRESS_BAR_SIZE = 20  # The rect size of the progress bar.
INITIAL_Y_SPEED = 5     # Initial vertical speed for the ball.
MAX_X_SPEED = 5         # Maximum initial horizontal speed for the ball.
COLOR_LIST = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']     # color of bricks


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, title='Breakout'):
        # window
        self._window = GWindow((BRICK_WIDTH+BRICK_SPACING)*BRICK_COLS+BRICK_SPACING,
                               BRICK_OFFSET + 3 * (BRICK_ROWS * (BRICK_HEIGHT + BRICK_SPACING) - BRICK_SPACING),
                               title=title)

        self._page = 0     # control which page to show

        # start page
        self._start_label = GLabel('')
        self._start_label.font = 'Chalkduster-40'
        self._start_label.color = 'black'
        self._highscore = 0

        # game page
        self._ball = GOval(ball_radius, ball_radius)
        self._ball.filled = True

        self._paddle = GRect(paddle_width, paddle_height)
        self._paddle.filled = True

        self._score_board = GLabel('Score: 0')
        self._score_board.font = 'Chalkduster-20'
        self._score_board.color = 'black'

        self._num_lives = 3
        self._live_board = GLabel(f'Lives: {self._num_lives}')
        self._live_board.font = 'Chalkduster-20'
        self._live_board.color = 'black'

        self._wind_vane = GLabel(f'Wind direction: ◎ ')
        self._wind_vane.font = 'Chalkduster-15'
        self._wind_vane.color = 'black'

        self._wind_sign = GLabel(f'Next wind: 10s')
        self._wind_sign.font = 'Chalkduster-15'
        self._wind_sign.color = 'black'

        self._last_wind_time = 0
        self._next_wind_time = 0
        self._wind_time_pass = 0
        self._next_wind = 0
        self._wind_change = False

        self._vx = 0
        self._vy = 0
        self._remove_ct = 0
        self._ing = False

        self._protect_object = [self._paddle, self._score_board, self._live_board, self._wind_vane, self._wind_sign]
        self._invisible_object = [self._score_board, self._live_board, self._wind_vane, self._wind_sign]

        # mouse event
        onmouseclicked(self.click_event)
        onmousemoved(self.move_event)

    def draw_bricks(self):
        """
        Draw bricks on the window.
        """
        color_counter = -1
        for row in range(BRICK_ROWS):
            if row % 2 == 0:
                color_counter += 1
            for col in range(BRICK_COLS):
                brick = GRect(BRICK_WIDTH, BRICK_HEIGHT)
                brick.filled = True
                color = COLOR_LIST[color_counter % len(COLOR_LIST)]
                brick.fill_color = color
                brick.color = color
                self._window.add(brick, BRICK_SPACING + (BRICK_WIDTH + BRICK_SPACING) * col,
                                 BRICK_OFFSET + (BRICK_HEIGHT + BRICK_SPACING) * row)

    def game_reset(self):
        """
        You can use this method to reset the game.
        """
        self._window.clear()
        self._window.add(self._paddle, (self._window.width - self._paddle.width)//2,
                         self._window.height - PADDLE_OFFSET - self._paddle.height)
        self._window.add(self._ball, self._paddle.x + self._paddle.width//2 - self._ball.width//2,
                         self._paddle.y - self._ball.height)
        self._score_board.text = f'Score: 0'
        self._window.add(self._live_board, LABEL_SPACING, self._window.height)
        self._window.add(self._score_board, self._live_board.x + self._live_board.width + LABEL_SPACING,
                         self._window.height)
        self._window.add(self._wind_vane, self._window.width//2, self._window.height)
        self._window.add(self._wind_sign, self._wind_vane.x + self._wind_vane.width + LABEL_SPACING,
                         self._window.height)
        self._vx = 0
        self._vy = 0
        self._remove_ct = 0
        self._ing = False
        self._wind_change = True
        self._wind_time_pass = 0

    def detect_collision(self):
        """
        Use four corners of the ball to check if collide with any other object.
        """
        if 0 > self._vy:
            top_left = self._window.get_object_at(self._ball.x, self._ball.y)
            top_right = self._window.get_object_at(self._ball.x + self._ball.width, self._ball.y)
            if top_left is not None and top_right is not None:
                if top_left is top_right:
                    if top_left not in self._protect_object:
                        self._window.remove(top_left)
                        self._remove_ct += 1
                else:
                    if top_left not in self._protect_object:
                        self._window.remove(top_left)
                        self._remove_ct += 1
                    if top_right not in self._protect_object:
                        self._window.remove(top_right)
                        self._remove_ct += 1
                if top_left not in self._invisible_object and top_right not in self._invisible_object:
                    self.set_ball_velocity(y=-1)
            elif top_left is None and top_right is not None:
                if self._vx > 0:
                    if top_right not in self._protect_object:
                        self._window.remove(top_right)
                        self._remove_ct += 1
                    if abs(self._ball.x + self._ball.width - top_right.x) >= abs(self._ball.y - top_right.y + top_right.height):
                        if top_right not in self._invisible_object:
                            self.set_ball_velocity(y=-1)
                    else:
                        if top_right not in self._invisible_object:
                            self.set_ball_velocity(x=-1)
                else:
                    if top_right not in self._protect_object:
                        self._window.remove(top_right)
                        self._remove_ct += 1
                    if top_right not in self._invisible_object:
                        self.set_ball_velocity(y=-1)
            elif top_left is not None and top_right is None:
                if self._vx > 0:
                    if top_left not in self._protect_object:
                        self._window.remove(top_left)
                        self._remove_ct += 1
                    if top_left not in self._invisible_object:
                        self.set_ball_velocity(y=-1)
                else:
                    if top_left not in self._protect_object:
                        self._window.remove(top_left)
                        self._remove_ct += 1
                    if abs(self._ball.x - top_left.x + top_left.width) >= abs(self._ball.y - top_left.y + top_left.height):
                        if top_left not in self._invisible_object:
                            self.set_ball_velocity(y=-1)
                    else:
                        if top_left not in self._invisible_object:
                            self.set_ball_velocity(x=-1)
        else:
            bottom_left = self._window.get_object_at(self._ball.x, self._ball.y + self._ball.height)
            bottom_right = self._window.get_object_at(self._ball.x + self._ball.width, self._ball.y + self._ball.height)
            if bottom_left is not None and bottom_right is not None:
                if bottom_left is bottom_right:
                    if bottom_left not in self._protect_object:
                        self._window.remove(bottom_left)
                        self._remove_ct += 1
                else:
                    if bottom_left not in self._protect_object:
                        self._window.remove(bottom_left)
                        self._remove_ct += 1
                    if bottom_right not in self._protect_object:
                        self._window.remove(bottom_right)
                        self._remove_ct += 1
                if bottom_left not in self._invisible_object and bottom_right not in self._invisible_object:
                    self.set_ball_velocity(y=-1)
            elif bottom_left is not None and bottom_right is None:
                if self._vx < 0:
                    if bottom_left not in self._protect_object:
                        self._window.remove(bottom_left)
                        self._remove_ct += 1
                    if abs(bottom_left.x + bottom_left.width - self._ball.x) >= abs(self._ball.y + self._ball.height - bottom_left.y):
                        if bottom_left not in self._invisible_object:
                            self.set_ball_velocity(y=-1)
                    else:
                        if bottom_left not in self._invisible_object:
                            self.set_ball_velocity(x=-1)
                else:
                    if bottom_left not in self._protect_object:
                        self._window.remove(bottom_left)
                        self._remove_ct += 1
                    if bottom_left not in self._invisible_object:
                        self.set_ball_velocity(y=-1)
            elif bottom_left is None and bottom_right is not None:
                if self._vx < 0:
                    if bottom_right not in self._protect_object:
                        self._window.remove(bottom_right)
                        self._remove_ct += 1
                    if bottom_right not in self._invisible_object:
                        self.set_ball_velocity(y=-1)
                else:
                    if bottom_right not in self._protect_object:
                        self._window.remove(bottom_right)
                        self._remove_ct += 1
                    if abs(self._ball.x + self._ball.width - bottom_right.x) >= abs(self._ball.y + self._ball.height - bottom_right.y):
                        if bottom_right not in self._invisible_object:
                            self.set_ball_velocity(y=-1)
                    else:
                        if bottom_right not in self._invisible_object:
                            self.set_ball_velocity(x=-1)
        self.update_score()

    def update_score(self):
        """
        Update the score on the window
        """
        score = self._remove_ct * 10
        self._score_board.text = f'Score: {score}'
        if score > self._highscore:
            self._highscore = score

    def wind(self):
        """
        This method create random wind speed and direction to influent the movement of ball.
        """
        def random_wind():
            speed = random.randint(1, 10)
            dir_ = random.randrange(-1, 2, 2)
            return speed, dir_

        if self._ing:
            self._wind_time_pass += (time.time() - self._last_wind_time)
            self._wind_sign.text = f'Next wind: {10 - round(self._wind_time_pass)}s'
            self._last_wind_time = time.time()

            if self._wind_change:
                self._next_wind = random_wind()
                self._wind_change = False

            wind_speed = self._next_wind[0]
            wind_dir = self._next_wind[1]

            if wind_dir > 0:
                self._wind_vane.text = f'Next wind direction: →{wind_speed}'
                self._wind_sign.x = self._wind_vane.x + self._wind_vane.width + LABEL_SPACING
            elif wind_dir < 0:
                self._wind_vane.text = f'Next wind direction: ←{wind_speed}'
                self._wind_sign.x = self._wind_vane.x + self._wind_vane.width + LABEL_SPACING
            if self._wind_time_pass >= 10:
                self._vx = wind_speed * wind_dir
                self._wind_change = True
                self._wind_time_pass = 0
        else:
            self._wind_sign.text = f'Next wind: 10s'
            self._last_wind_time = time.time()

    def start_page(self):
        """
        This method draw the start page and restart page.
        """
        if self._page == 0:
            check = self._window.get_object_at(self._window.width//2, self._window.height//2)
            if check is None:
                progress_rate_board = GLabel(f'Loading...0%')
                progress_rate_board.font = 'Chalkduster-15'
                self._window.add(progress_rate_board, (self._window.width-progress_rate_board.width)//2,
                                 (self._window.height + PROGRESS_BAR_SIZE)//2 + progress_rate_board.height + LABEL_SPACING)
                pause_time = 300
                for i in range(10):
                    color = COLOR_LIST[i % len(COLOR_LIST)]
                    progress_bar = GRect(PROGRESS_BAR_SIZE*(i+1), PROGRESS_BAR_SIZE)
                    progress_bar.filled = True
                    progress_bar.fill_color = color
                    progress_bar.color = color
                    self._window.add(progress_bar, self._window.width // 2 - PROGRESS_BAR_SIZE * 5,
                                     self._window.height // 2 - PROGRESS_BAR_SIZE // 2)
                    progress_rate_board.text = f'Loading...{10*(i+1)}'
                    pause(pause_time)
                    pause_time += 100

            self._window.clear()
            self.draw_bricks()
            self._start_label.text = f'Click to start'
            self._window.add(self._start_label, (self._window.width - self._start_label.width)//2,
                             (self._window.height + self._start_label.height)//2)
        elif self._page == 2:
            self._window.clear()
            # self.draw_bricks()
            self._start_label.text = f'Click to restart'
            self._window.add(self._start_label, (self._window.width - self._start_label.width) // 2,
                             (self._window.height + self._start_label.height) // 2)
            highscore_board = GLabel(f'High score: {self._highscore}')
            highscore_board.font = 'Chalkduster-60'
            highscore_board.color = 'navy'
            self._window.add(highscore_board, (self._window.width - highscore_board.width)//2,
                             self._start_label.y - self._start_label.height - LABEL_SPACING*3)

    def check_over(self):
        """
        Check if the game is over.
        """
        if self._remove_ct == BRICK_COLS * BRICK_ROWS or self._num_lives == 0:
            return True

    def click_event(self, m):
        """
        Control the behavior of mouse click.
        """
        if 0 < m.x < self._window.width and 0 < m.y < self._window.height:
            # start page
            if self._page == 0 or self._page == 2:
                if self._start_label.x <= m.x <= self._start_label.x + self._start_label.width and self._start_label.y - self._start_label.height <= m.y <= self._start_label.y:
                    self._page = 1
                    self._ing = False
                    self._num_lives = 3
                    self._live_board.text = f'Lives: {self._num_lives}'
            # game page
            elif self._page == 1:
                if not self._ing:
                    self._vx = random.randint(1, MAX_X_SPEED) * random.randrange(-1, 2, 2)
                    self._vy = -INITIAL_Y_SPEED
                    self._ing = True

    def move_event(self, m):
        """
        Control the behavior of mouse move.
        """
        if self._page == 0 or self._page == 2:
            if self._start_label.x <= m.x <= self._start_label.x + self._start_label.width and self._start_label.y - self._start_label.height <= m.y <= self._start_label.y:
                self._start_label.color = 'magenta'
            else:
                self._start_label.color = 'black'
        elif self._page == 1:
            if self._paddle.width//2 < m.x < self._window.width - self._paddle.width//2:
                self._paddle.x = m.x - self._paddle.width//2
            elif m.x <= self._paddle.width//2:
                self._paddle.x = 0
            elif m.x >= self._window.width - self._paddle.width//2:
                self._paddle.x = self._window.width - self._paddle.width
            if self._vx == 0 and self._vy == 0:
                self._ball.x = self._paddle.x + (self._paddle.width - self._ball.width)//2

    def get_page(self):
        return self._page

    def set_page(self, page_num):
        self._page = page_num

    def get_ball(self):
        return self._ball

    def get_ball_velocity(self):
        return self._vx, self._vy

    def set_ball_velocity(self, x=1, y=1):
        self._vx *= x
        self._vy *= y

    def get_window(self):
        return self._window

    def get_lives(self):
        return self._num_lives

    def set_lives(self):
        self._num_lives -= 1
        self._live_board.text = f'Lives: {self._num_lives}'

    def get_game_start(self):
        return self._ing


if __name__ == 'breakoutgraphics':
    print(f'Welcome to my breakout game, hope you enjoy it!')
