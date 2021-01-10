"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 15        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 50      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7.0  # Initial vertical speed for the ball.
MAX_X_SPEED = 5      # Maximum initial horizontal speed for the ball.
score = 0
brick_ct = 0
trick_ct = 0


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):

        # Create a graphical window, with some extra space.
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create score board.
        self.score_board = GLabel('Score: '+str(score))
        self.score_board.font = 'helvetica-20-bold'
        self.window.add(self.score_board, 0, self.window.height)
        # Create a paddle.
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.window.add(self.paddle, (self.window.width-self.paddle.width)/2,
                        self.window.height-paddle_offset-paddle_height)
        # Center a filled ball in the graphical window.
        self.ball = GOval(ball_radius*2, ball_radius*2)
        self.ball.filled = True
        self.start_point_x = (self.window.width-self.ball.width)/2
        self.start_point_y = (self.window.height-self.ball.height)/2
        self.window.add(self.ball, self.start_point_x, self.start_point_y)
        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0
        if random.random() > 0.5:
            self.__dx = -self.__dx
        # Initialize our mouse listeners.
        onmouseclicked(self.game_start)
        onmousemoved(self.paddle_move)
        # Draw bricks.
        bricks_x = 0
        bricks_y = 0
        rows_ct = 0
        color_ct = 0
        while True:
            global brick_ct
            self.bricks = GRect(brick_width, brick_height)
            self.bricks.filled = True
            self.bricks.fill_color = self.bricks_color(color_ct)
            self.bricks.color = self.bricks_color(color_ct)
            if bricks_x < self.window.width and \
                    bricks_y < brick_rows*(self.bricks.height+brick_spacing):
                self.window.add(self.bricks, x=bricks_x, y=bricks_y)
                bricks_x += self.bricks.width + brick_spacing
                brick_ct += 1
            elif bricks_x > self.window.width and \
                    bricks_y + self.bricks.height+brick_spacing < brick_rows*(self.bricks.height+brick_spacing):
                bricks_y += self.bricks.height + brick_spacing
                bricks_x = 0
                rows_ct += 1
                color_ct += 1
            elif bricks_y+self.bricks.height+brick_spacing >= brick_rows * (self.bricks.height + brick_spacing):
                break
        self.brick_rows = BRICK_ROWS

    # define brick's color
    def bricks_color(self, row_count):
        color_list = ['red', 'green', 'yellow', 'magenta', 'navy']
        if row_count < 2:
            return color_list[0]
        if row_count < 4:
            return color_list[1]
        if row_count < 6:
            return color_list[2]
        if row_count < 8:
            return color_list[3]
        if row_count < 10:
            return color_list[4]
        elif row_count >= 10:
            return color_list[random.randint(0, 4)]

    # let the paddle follow mouse
    def paddle_move(self, mouse):
        self.paddle.x = mouse.x - self.paddle.width/2
        if self.paddle.x + self.paddle.width > self.window.width:
            self.paddle.x = self.window.width-self.paddle.width
        elif self.paddle.x < 0:
            self.paddle.x = 0

    # give the ball starting velocity
    def game_start(self, mouse):
        if self.ball.x == (self.window.width-self.ball.width)/2 and \
                self.ball.y == (self.window.height-self.ball.height)/2:
            if 0 < mouse.x < self.window.width and 0 < mouse.y < self.window.height:
                self.__dx = random.randint(1, MAX_X_SPEED)
                self.__dy = INITIAL_Y_SPEED
                if random.random() > 0.5:
                    self.__dx = -self.__dx

    @property
    def get_dx(self):
        return self.__dx

    @property
    def get_dy(self):
        return self.__dy

    # to check if the ball is collide any objects
    def ball_sensor(self, ball_x, ball_y):
        p1 = self.window.get_object_at(ball_x, ball_y)
        p2 = self.window.get_object_at(ball_x+self.ball.width, ball_y)
        p3 = self.window.get_object_at(ball_x, ball_y + self.ball.width)
        p4 = self.window.get_object_at(ball_x + self.ball.width, ball_y + self.ball.width)
        if p1 is not None:
            return p1
        elif p2 is not None:
            return p2
        elif p3 is not None:
            return p3
        elif p4 is not None:
            return p4
        else:
            return None

    # define if the ball move into something, what actions will it take
    def ball_action(self, sensor):
        global score
        if sensor is not self.paddle and sensor is not None:
            if sensor is not self.score_board:
                self.window.remove(sensor)
                score += 1
                self.score_board.text = 'Score: '+str(score)
                self.window.add(self.score_board, 0, self.window.height)
                self.__dy = -self.__dy
                self.__dx = -self.__dx
        elif sensor is not None and sensor is self.paddle:
            if self.ball.y+self.ball.height <= sensor.y+sensor.height and\
                    sensor.x <= self.ball.x+self.ball.width/2 <= sensor.x+sensor.width:
                self.window.add(self.ball, self.ball.x, sensor.y-self.ball.height)
                if self.paddle.x+self.paddle.width*2/3 < self.ball.x+self.ball.width/2 <\
                        self.paddle.x+self.paddle.width/3:
                    self.__dy = -self.__dy
                else:
                    self.__dy = -self.__dy
            else:
                self.__dx = -self.__dx

    # reset the ball in the center
    def reset_game(self):
        self.window.add(self.ball, self.start_point_x, self.start_point_y)
        self.__dx = 0
        self.__dy = 0

    @staticmethod
    def get_brick_ct():
        return brick_ct

    # print lose if the player lost the game
    def lose(self):
        lose_label = GLabel('You lose!')
        lose_label.font = 'helvetica-50-bold'
        self.window.add(lose_label, (self.window.width-lose_label.width)/2, (self.window.height+lose_label.height)/2)

    # remove the ball
    def remove_ball(self):
        self.window.remove(self.ball)
