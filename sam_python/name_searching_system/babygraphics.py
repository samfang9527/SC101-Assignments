"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

YOUR DESCRIPTION HERE
"""

import tkinter
import babynames
import babygraphicsgui as gui
from campy.gui.events.timer import pause

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000
DELAY = 20


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    year_space = (width-GRAPH_MARGIN_SIZE)//len(YEARS)
    x_coordinate = GRAPH_MARGIN_SIZE+int(year_index)*year_space
    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Write your code below this line
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE)
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE,
                       CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)
    for year in range(len(YEARS)):
        x = get_x_coordinate(CANVAS_WIDTH, year)
        canvas.create_line(x, 0, x, CANVAS_HEIGHT)
        canvas.create_text(x+TEXT_DX, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, text=YEARS[year], font='roboto 12',
                           anchor=tkinter.NW)
    #################################


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # Write your code below this line
    rank_space = (CANVAS_HEIGHT-GRAPH_MARGIN_SIZE*2) / MAX_RANK
    color_ct = 0
    for name in lookup_names:  # First for loop is to read the value of key name in name_data
        name_dict = name_data[name]
        point_lst = []  # record the point to draw line
        """
        Second for loop, read the constant YEARS and see if it's in the 
        """
        for i in range(len(YEARS)):
            x_point = get_x_coordinate(CANVAS_WIDTH, i)
            if str(YEARS[i]) in name_dict:
                y_point_in_rank = GRAPH_MARGIN_SIZE+name_dict[str(YEARS[i])]*rank_space
                canvas.create_text(x_point + TEXT_DX, y_point_in_rank, text=name + '  ' + str(name_dict[str(YEARS[i])]),
                                   font='roboto 12', anchor=tkinter.SW, fill=COLORS[color_ct])
                canvas.create_text(x_point + TEXT_DX, y_point_in_rank, text='♥︎', fill=COLORS[color_ct])
                point_lst.append([x_point, y_point_in_rank])
            else:
                y_point_out_of_rank = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
                canvas.create_text(x_point + TEXT_DX, y_point_out_of_rank, text=name + ' * ',
                                   font='roboto 12', anchor=tkinter.SW, fill=COLORS[color_ct])
                canvas.create_text(x_point + TEXT_DX, y_point_out_of_rank, text='♥︎', fill=COLORS[color_ct])
                point_lst.append([x_point, y_point_out_of_rank])
        for point in range(len(point_lst)):
            if point+1 in range(len(point_lst)):
                canvas.create_line(point_lst[point][0], point_lst[point][1], point_lst[point+1][0],
                                   point_lst[point+1][1], fill=COLORS[color_ct], width=LINE_WIDTH)
                pause(DELAY)
            else:
                break
        color_ct = (color_ct + 1) % len(COLORS)
    #################################


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
