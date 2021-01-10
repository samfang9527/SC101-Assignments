"""
File: 
Name:
----------------------
TODO:
"""

from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
from campy.graphics.gimage import GImage

SIZE = 50
w = GWindow(600, 600)
DELAY = 200
CIRCLE_REDUCE = 50


def main():
    """
    TODO:
    """
    circle_size = w.width
    count = 0
    # the while loop below is for the circle in the background
    while circle_size >= 0:
        if count % 2 == 0:
            circle = GOval(circle_size, circle_size)
            circle.filled = True
            circle.fill_color = 'white'
            circle.color = 'white'
            w.add(circle, (w.width-circle.width)/2, (w.height-circle.height)/2)
            circle_size -= CIRCLE_REDUCE
            count += 1
        elif count % 2 == 1:
            circle = GOval(circle_size, circle_size)
            circle.filled = True
            w.add(circle, (w.width - circle.width) / 2, (w.height - circle.height) / 2)
            circle_size -= CIRCLE_REDUCE
            count += 1
            pause(500)
    # below is for the img in the center, adjustable
    img = GImage('winnie')
    start_point = 0-img.height
    w.add(img, x=(w.width - img.width) / 2, y=start_point)
    speed = 1
    # this while loop is the movement of the img
    while True:
        img.move(0, speed)
        speed += 1
        if img.y+img.height >= w.height:
            speed = -speed
        elif img.y+img.height < w.height and speed == -25:
            break
        pause(20)
    # below is for the body
    body_move = img.y+img.height
    body = GRect(img.width / 2, img.width / 2)
    while body.y+body.height < w.height-body.height*2:
        body = GRect(img.width / 2, img.width / 2)
        body.filled = True
        body.fill_color = 'red'
        body.color = 'red'
        w.add(body, img.x+body.width/2, body_move)
        body_move += 1
        pause(1)
    # below is for the hands and legs
    hand_move_y = img.y + img.height
    hand_move_x = 0
    leg_move_y = body_move+body.height
    leg_move_x = 0
    leg = GRect(img.width/3, img.width/3)
    while leg_move_y + leg.height < w.height:
        l_leg = GRect(img.width / 3, img.width / 3)
        l_leg.filled = True
        l_leg.fill_color = 'yellow'
        l_leg.color = 'yellow'
        r_leg = GRect(img.width/3, img.width/3)
        r_leg.filled = True
        r_leg.fill_color = 'yellow'
        r_leg.color = 'yellow'
        l_hand = GRect(img.width / 3, img.width / 3)
        l_hand.filled = True
        l_hand.fill_color = 'yellow'
        l_hand.color = 'yellow'
        r_hand = GRect(img.width / 3, img.width / 3)
        r_hand.filled = True
        r_hand.fill_color = 'yellow'
        r_hand.color = 'yellow'
        w.add(l_hand, img.x - l_hand.width + body.width/2 + hand_move_x, hand_move_y)
        w.add(r_hand, img.x + img.width - body.width/2 - hand_move_x, hand_move_y)
        w.add(l_leg, body.x - leg_move_x, leg_move_y)
        w.add(r_leg, body.x + body.width - r_leg.width + leg_move_x, leg_move_y)
        leg_move_x += 1
        leg_move_y += 1
        hand_move_x -= 1
        hand_move_y -= 1
        pause(1)
    # StanCode title
    banner = GRect(200, 100)
    banner.filled = True
    banner.fill_color = 'magenta'
    w.add(banner, 0, 0)
    title = GLabel('StanCode')
    title.font = 'roboto-30-bold'
    w.add(title, (banner.width-title.width)/2, (banner.height+banner.height)/2)




if __name__ == '__main__':
    main()
