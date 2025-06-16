# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================

# ----------------------------------------------
#  BPL -> BleuRaven Python Library
#  https://github.com/xavier150/BPL
#  BleuRaven.fr
#  XavierLoux.com
# ----------------------------------------------

import time


class ProgressionBarClass():
    def _get_name(self) -> str:
        return self.__name

    def _set_name(self, value: str) -> None:
        self.__name = value

    name = property(_get_name, _set_name)

    def _get_length(self) -> float:
        return self.__length

    def _set_length(self, value: float) -> None:
         self.__length = value

    length = property(_get_length, _set_length)

    previous_step = 0.0

    def _get_total_step(self) -> float:
        return self.__total_step

    def _set_total_step(self, value: float) -> None:
        self.__total_step = value

    total_step = property(_get_total_step, _set_total_step)

    # Visual
    show_block = True
    show_steps = True
    show_percentage = True

    def __init__(self):
        self.__name = "My progression bar"
        self.__length = 20  # modify this to change the length
        self.__previous_step = 0.0
        self.__total_step = 1.0  # from 0 to 1
        self.__counter_start = time.perf_counter()

    def update_progress(self, progress: float) -> None:
        job_title = self.__name
        length = self.__length
        total_step = self.__total_step
        self.__previous_step = progress  # Update the previous step.

        is_done = progress >= total_step

        # Write message
        msg = "\r{0}:".format(job_title)

        if self.show_block:
            block = int(round(length * progress / total_step))
            msg += " [{0}]".format("#" * block + "-" * int(length - block))

        if self.show_steps:
            msg += " {0}/{1}".format(progress, total_step)

        if is_done:
            msg += " DONE IN {0}s\r\n".format(round(time.perf_counter() - self.__counter_start, 3))
        elif self.show_percentage:
            msg += " {0}%".format(round((progress * 100) / total_step, 2))

        # Print the progress message on the same line
        print(msg, end='', flush=True)

def print_formatted_text(
    text: str, 
    width: int = 60, 
    fill_char: str = "=", 
    left_border: str = "# ", 
    left_padding: str = " ", 
    right_padding: str = " ", 
    right_border: str = " #"
) -> None:
    """
    Prints formatted text with customizable padding and border characters.

    Args:
        text (str): The text to display.
        width (int, optional): The total width of the line. Defaults to 60.
        fill_char (str, optional): The character used to fill the padding. Defaults to '='.
        left_border (str, optional): The left border characters. Defaults to '# '.
        left_padding (str, optional): The padding character(s) on the left of the text. Defaults to ' '.
        right_padding (str, optional): The padding character(s) on the right of the text. Defaults to ' '.
        right_border (str, optional): The right border characters. Defaults to ' #'.
    """

    padding = (width - len(text) - len(left_border) - len(right_border)) // 2
    if padding < 0:
        raise ValueError("The width is too small to fit the text and borders.")
    
    print(f"{left_border}{fill_char * padding}{left_padding}{text}{right_padding}{fill_char * padding}{right_border}")

def print_separator(width: int = 60, fill_char: str = "-"):
    """
    Prints a separator line with customizable characters.

    Args:
        width (int, optional): The width of the separator. Defaults to 60.
        fill_char (str, optional): The character used to create the separator. Defaults to '-'.
    """
    print_formatted_text(
        text="", 
        width=width, 
        fill_char=fill_char, 
        left_border="# ", 
        left_padding=fill_char, 
        right_padding=fill_char, 
        right_border=" #"
    )

def print_big_title(
    text: str, 
    width: int = 60, 
    border_char: str = "#"
) -> None:
    """
    Prints a big title enclosed by a border.

    Args:
        text (str): The title text.
        width (int, optional): The width of the title line. Defaults to 60.
        border_char (str, optional): The character used for the border. Defaults to '#'.
    """
    print(border_char * width)
    print_formatted_text(
        text=text, 
        width=width, 
        fill_char=border_char, 
        left_border=border_char, 
        right_border=border_char
    )
    print(border_char * width)

def print_simple_title(
    text: str, 
    width: int = 60, 
    fill_char: str = "=", 
    border_char: str = "#"
) -> None:
    """
    Prints a simple title with side borders.

    Args:
        text (str): The title text.
        width (int, optional): The width of the title line. Defaults to 60.
        fill_char (str, optional): The character used to fill the line. Defaults to '='.
        border_char (str, optional): The character used for the side borders. Defaults to '#'.
    """
    print_formatted_text(
        text=text, 
        width=width, 
        fill_char=fill_char, 
        left_border=border_char + " ", 
        right_border=" " + border_char
    )