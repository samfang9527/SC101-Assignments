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
        self.__window = GWindow((BRICK_WIDTH+BRICK_SPACING)*BRICK_COLS+BRICK_SPACING,
                                BRICK_OFFSET + 3 * (BRICK_ROWS * (BRICK_HEIGHT + BRICK_SPACING) - BRICK_SPACING),
                                title=title)

        self.__page = 0     # control which page to show

        # start page
        self.__start_label = GLabel('')
        self.__start_label.font = 'Chalkduster-40'
        self.__start_label.color = 'black'
        self.__highscore = 0

        # game page
        self.__ball = GOval(ball_radius, ball_radius)
        self.__ball.filled = True

        self.__paddle = GRect(paddle_width, paddle_height)
        self.__paddle.filled = True

        self.__score_board = GLabel('Score: 0')
        self.__score_board.font = 'Chalkduster-20'
        self.__score_board.color = 'black'

        self.__num_lives = 3
        self.__live_board = GLabel(f'Lives: {self.__num_lives}')
        self.__live_board.font = 'Chalkduster-20'
        self.__live_board.color = 'black'

        self.__wind_vane = GLabel(f'Wind direction: ◎ ')
        self.__wind_vane.font = 'Chalkduster-15'
        self.__wind_vane.color = 'black'

        self.__wind_sign = GLabel(f'Next wind: 10s')
        self.__wind_sign.font = 'Chalkduster-15'
        self.__wind_sign.color = 'black'

        self.__last_wind_time = 0
        self.__next_wind_time = 0
        self.__wind_time_pass = 0
        self.__next_wind = self.random_wind()
        self.__wind_change = False

        self.__vx = 0
        self.__vy = 0
        self.__remove_ct = 0
        self.__ing = False

        self.__protect_object = [self.__paddle, self.__score_board, self.__live_board, self.__wind_vane, self.__wind_sign]
        self.__invisible_object = [self.__score_board, self.__live_board, self.__wind_vane, self.__wind_sign]

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
                self.__window.add(brick, BRICK_SPACING + (BRICK_WIDTH + BRICK_SPACING) * col,
                                  BRICK_OFFSET + (BRICK_HEIGHT + BRICK_SPACING) * row)

    def game_reset(self):
        """
        You can use this method to reset the game.
        """
        self.__window.clear()
        self.__window.add(self.__paddle, (self.__window.width - self.__paddle.width)//2,
                          self.__window.height - PADDLE_OFFSET - self.__paddle.height)
        self.__window.add(self.__ball, self.__paddle.x + self.__paddle.width//2 - self.__ball.width//2,
                          self.__paddle.y - self.__ball.height)
        self.__score_board.text = f'Score: 0'
        self.__window.add(self.__live_board, LABEL_SPACING, self.__window.height)
        self.__window.add(self.__score_board, self.__live_board.x + self.__live_board.width + LABEL_SPACING,
                          self.__window.height)
        self.__window.add(self.__wind_vane, self.__window.width//2, self.__window.height)
        self.__window.add(self.__wind_sign, self.__wind_vane.x + self.__wind_vane.width + LABEL_SPACING,
                          self.__window.height)
        self.__vx = 0
        self.__vy = 0
        self.__remove_ct = 0
        self.__ing = False
        self.__wind_change = True
        self.__wind_time_pass = 0

    def detect_collision(self):
        """
        Use four corners of the ball to check if collide with any other object.
        """
        if 0 > self.__vy:
            top_left = self.__window.get_object_at(self.__ball.x, self.__ball.y)
            top_right = self.__window.get_object_at(self.__ball.x + self.__ball.width, self.__ball.y)
            if top_left is not None and top_right is not None:
                if top_left is top_right:
                    if top_left not in self.__protect_object:
                        self.__window.remove(top_left)
                        self.__remove_ct += 1
                else:
                    if top_left not in self.__protect_object:
                        self.__window.remove(top_left)
                        self.__remove_ct += 1
                    if top_right not in self.__protect_object:
                        self.__window.remove(top_right)
                        self.__remove_ct += 1
                if top_left not in self.__invisible_object and top_right not in self.__invisible_object:
                    self.set_ball_velocity(y=-1)
            elif top_left is None and top_right is not None:
                if self.__vx > 0:
                    if top_right not in self.__protect_object:
                        self.__window.remove(top_right)
                        self.__remove_ct += 1
                    if abs(self.__ball.x + self.__ball.width - top_right.x) >= abs(self.__ball.y - top_right.y + top_right.height):
                        if top_right not in self.__invisible_object:
                            self.set_ball_velocity(y=-1)
                    else:
                        if top_right not in self.__invisible_object:
                            self.set_ball_velocity(x=-1)
                else:
                    if top_right not in self.__protect_object:
                        self.__window.remove(top_right)
                        self.__remove_ct += 1
                    if top_right not in self.__invisible_object:
                        self.set_ball_velocity(y=-1)
            elif top_left is not None and top_right is None:
                if self.__vx > 0:
                    if top_left not in self.__protect_object:
                        self.__window.remove(top_left)
                        self.__remove_ct += 1
                    if top_left not in self.__invisible_object:
                        self.set_ball_velocity(y=-1)
                else:
                    if top_left not in self.__protect_object:
                        self.__window.remove(top_left)
                        self.__remove_ct += 1
                    if abs(self.__ball.x - top_left.x + top_left.width) >= abs(self.__ball.y - top_left.y + top_left.height):
                        if top_left not in self.__invisible_object:
                            self.set_ball_velocity(y=-1)
                    else:
                        if top_left not in self.__invisible_object:
                            self.set_ball_velocity(x=-1)
        else:
            bottom_left = self.__window.get_object_at(self.__ball.x, self.__ball.y + self.__ball.height)
            bottom_right = self.__window.get_object_at(self.__ball.x + self.__ball.width, self.__ball.y + self.__ball.height)
            if bottom_left is not None and bottom_right is not None:
                if bottom_left is bottom_right:
                    if bottom_left not in self.__protect_object:
                        self.__window.remove(bottom_left)
                        self.__remove_ct += 1
                else:
                    if bottom_left not in self.__protect_object:
                        self.__window.remove(bottom_left)
                        self.__remove_ct += 1
                    if bottom_right not in self.__protect_object:
                        self.__window.remove(bottom_right)
                        self.__remove_ct += 1
                if bottom_left not in self.__invisible_object and bottom_right not in self.__invisible_object:
                    self.set_ball_velocity(y=-1)
            elif bottom_left is not None and bottom_right is None:
                if self.__vx < 0:
                    if bottom_left not in self.__protect_object:
                        self.__window.remove(bottom_left)
                        self.__remove_ct += 1
                    if abs(bottom_left.x + bottom_left.width - self.__ball.x) >= abs(self.__ball.y + self.__ball.height - bottom_left.y):
                        if bottom_left not in self.__invisible_object:
                            self.set_ball_velocity(y=-1)
                    else:
                        if bottom_left not in self.__invisible_object:
                            self.set_ball_velocity(x=-1)
                else:
                    if bottom_left not in self.__protect_object:
                        self.__window.remove(bottom_left)
                        self.__remove_ct += 1
                    if bottom_left not in self.__invisible_object:
                        self.set_ball_velocity(y=-1)
            elif bottom_left is None and bottom_right is not None:
                if self.__vx < 0:
                    if bottom_right not in self.__protect_object:
                        self.__window.remove(bottom_right)
                        self.__remove_ct += 1
                    if bottom_right not in self.__invisible_object:
                        self.set_ball_velocity(y=-1)
                else:
                    if bottom_right not in self.__protect_object:
                        self.__window.remove(bottom_right)
                        self.__remove_ct += 1
                    if abs(self.__ball.x + self.__ball.width - bottom_right.x) >= abs(self.__ball.y + self.__ball.height - bottom_right.y):
                        if bottom_right not in self.__invisible_object:
                            self.set_ball_velocity(y=-1)
                    else:
                        if bottom_right not in self.__invisible_object:
                            self.set_ball_velocity(x=-1)
        self.update_score()

    def update_score(self):
        """
        Update the score on the window
        """
        score = self.__remove_ct * 10
        self.__score_board.text = f'Score: {score}'
        if score > self.__highscore:
            self.__highscore = score

    def wind(self):
        """
        This method create random wind to influent the movement of ball.
        """
        def random_wind():
            speed = random.randint(1, 10)
            dir_ = random.randrange(-1, 2, 2)
            return speed, dir_

        if self.__ing:
            self.__wind_time_pass += (time.time() - self.__last_wind_time)
            self.__wind_sign.text = f'Next wind: {10 - round(self.__wind_time_pass)}s'
            self.__last_wind_time = time.time()

            if self.__wind_change:
                self.__next_wind = random_wind()
                self.__wind_change = False

            wind_speed = self.__next_wind[0]
            wind_dir = self.__next_wind[1]

            if wind_dir > 0:
                self.__wind_vane.text = f'Next wind direction: →{wind_speed}'
                self.__wind_sign.x = self.__wind_vane.x + self.__wind_vane.width + LABEL_SPACING
            elif wind_dir < 0:
                self.__wind_vane.text = f'Next wind direction: ←{wind_speed}'
                self.__wind_sign.x = self.__wind_vane.x + self.__wind_vane.width + LABEL_SPACING
            if self.__wind_time_pass >= 10:
                self.__vx = wind_speed * wind_dir
                self.__wind_change = True
                self.__wind_time_pass = 0
        else:
            self.__wind_sign.text = f'Next wind: 10s'
            self.__last_wind_time = time.time()

    def start_page(self):
        """
        This method draw the start page and restart page.
        """
        if self.__page == 0:
            check = self.__window.get_object_at(self.__window.width//2, self.__window.height//2)
            if check is None:
                progress_rate_board = GLabel(f'Loading...0%')
                progress_rate_board.font = 'Chalkduster-15'
                self.__window.add(progress_rate_board, (self.__window.width-progress_rate_board.width)//2,
                                  (self.__window.height + PROGRESS_BAR_SIZE)//2 + progress_rate_board.height + LABEL_SPACING)
                pause_time = 300
                for i in range(10):
                    color = COLOR_LIST[i % len(COLOR_LIST)]
                    progress_bar = GRect(PROGRESS_BAR_SIZE*(i+1), PROGRESS_BAR_SIZE)
                    progress_bar.filled = True
                    progress_bar.fill_color = color
                    progress_bar.color = color
                    self.__window.add(progress_bar, self.__window.width // 2 - PROGRESS_BAR_SIZE * 5,
                                      self.__window.height // 2 - PROGRESS_BAR_SIZE // 2)
                    progress_rate_board.text = f'Loading...{10*(i+1)}'
                    pause(pause_time)
                    pause_time += 100

            self.__window.clear()
            self.draw_bricks()
            self.__start_label.text = f'Click to start'
            self.__window.add(self.__start_label, (self.__window.width - self.__start_label.width)//2,
                              (self.__window.height + self.__start_label.height)//2)
        elif self.__page == 2:
            self.__window.clear()
            # self.draw_bricks()
            self.__start_label.text = f'Click to restart'
            self.__window.add(self.__start_label, (self.__window.width - self.__start_label.width) // 2,
                              (self.__window.height + self.__start_label.height) // 2)
            highscore_board = GLabel(f'High score: {self.__highscore}')
            highscore_board.font = 'Chalkduster-60'
            highscore_board.color = 'navy'
            self.__window.add(highscore_board, (self.__window.width - highscore_board.width)//2,
                              self.__start_label.y - self.__start_label.height - LABEL_SPACING*3)

    def check_over(self):
        """
        Check if the game is over.
        """
        if self.__remove_ct == BRICK_COLS * BRICK_ROWS or self.__num_lives == 0:
            return True

    def click_event(self, m):
        """
        Control the behavior of mouse click.
        """
        if 0 < m.x < self.__window.width and 0 < m.y < self.__window.height:
            # start page
            if self.__page == 0 or self.__page == 2:
                if self.__start_label.x <= m.x <= self.__start_label.x + self.__start_label.width and self.__start_label.y - self.__start_label.height <= m.y <= self.__start_label.y:
                    self.__page = 1
                    self.__ing = False
                    self.__num_lives = 3
                    self.__live_board.text = f'Lives: {self.__num_lives}'
            # game page
            elif self.__page == 1:
                if not self.__ing:
                    self.__vx = random.randint(1, MAX_X_SPEED) * random.randrange(-1, 2, 2)
                    self.__vy = -INITIAL_Y_SPEED
                    self.__ing = True

    def move_event(self, m):
        """
        Control the behavior of mouse move.
        """
        if self.__page == 0 or self.__page == 2:
            if self.__start_label.x <= m.x <= self.__start_label.x + self.__start_label.width and self.__start_label.y - self.__start_label.height <= m.y <= self.__start_label.y:
                self.__start_label.color = 'magenta'
            else:
                self.__start_label.color = 'black'
        elif self.__page == 1:
            if self.__paddle.width//2 < m.x < self.__window.width - self.__paddle.width//2:
                self.__paddle.x = m.x - self.__paddle.width//2
            elif m.x <= self.__paddle.width//2:
                self.__paddle.x = 0
            elif m.x >= self.__window.width - self.__paddle.width//2:
                self.__paddle.x = self.__window.width - self.__paddle.width
            if self.__vx == 0 and self.__vy == 0:
                self.__ball.x = self.__paddle.x + (self.__paddle.width - self.__ball.width)//2

    def get_page(self):
        return self.__page

    def set_page(self, page_num):
        self.__page = page_num

    def get_ball(self):
        return self.__ball

    def get_ball_velocity(self):
        return self.__vx, self.__vy

    def set_ball_velocity(self, x=1, y=1):
        self.__vx *= x
        self.__vy *= y

    def get_window(self):
        return self.__window

    def get_lives(self):
        return self.__num_lives

    def set_lives(self):
        self.__num_lives -= 1
        self.__live_board.text = f'Lives: {self.__num_lives}'

    def get_game_start(self):
        return self.__ing


if __name__ == 'breakoutgraphics':
    print(f'Thank you for playing my game!')