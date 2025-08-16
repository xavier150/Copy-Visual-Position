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

# This use ANSI color codes. 
# You can found it all here -> https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124
# This file use the code of rene-d -> https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007



# SGR color constants
# rene-d 2018

class Colors:
    """ ANSI color codes """

    # Color
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"

    #Style
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"


def black(string: str) -> str:
    """ Returns the string wrapped in black ANSI color codes. """
    return Colors.BLACK + string + Colors.END

def red(string: str) -> str:
    """ Returns the string wrapped in red ANSI color codes. """
    return Colors.RED + string + Colors.END

def green(string: str) -> str:
    """ Returns the string wrapped in green ANSI color codes. """
    return Colors.GREEN + string + Colors.END

def brown(string: str) -> str:
    """ Returns the string wrapped in brown ANSI color codes. """
    return Colors.BROWN + string + Colors.END

def blue(string: str) -> str:
    """ Returns the string wrapped in blue ANSI color codes. """    
    return Colors.BLUE + string + Colors.END

def purple(string: str) -> str:
    """ Returns the string wrapped in purple ANSI color codes. """
    return Colors.PURPLE + string + Colors.END

def cyan(string: str) -> str:
    """ Returns the string wrapped in cyan ANSI color codes. """
    return Colors.CYAN + string + Colors.END

def light_gray(string: str) -> str:
    """ Returns the string wrapped in light gray ANSI color codes. """
    return Colors.LIGHT_GRAY + string + Colors.END

def dark_gray(string: str) -> str:
    """ Returns the string wrapped in dark gray ANSI color codes. """
    return Colors.DARK_GRAY + string + Colors.END

def light_red(string: str) -> str:
    """ Returns the string wrapped in light red ANSI color codes. """
    return Colors.LIGHT_RED + string + Colors.END

def light_green(string: str) -> str:
    """ Returns the string wrapped in light green ANSI color codes. """
    return Colors.LIGHT_GREEN + string + Colors.END

def yellow(string: str) -> str:
    """ Returns the string wrapped in yellow ANSI color codes. """
    return Colors.YELLOW + string + Colors.END

def light_blue(string: str) -> str:
    """ Returns the string wrapped in light blue ANSI color codes. """
    return Colors.LIGHT_BLUE + string + Colors.END

def light_purple(string: str) -> str:
    """ Returns the string wrapped in light purple ANSI color codes. """
    return Colors.LIGHT_PURPLE + string + Colors.END

def light_cyan(string: str) -> str:
    """ Returns the string wrapped in light cyan ANSI color codes. """
    return Colors.LIGHT_CYAN + string + Colors.END

def light_white(string: str) -> str:
    """ Returns the string wrapped in light white ANSI color codes. """
    return Colors.LIGHT_WHITE + string + Colors.END

def bold(string: str) -> str:
    """ Returns the string wrapped in bold ANSI color codes. """
    return Colors.BOLD + string + Colors.END

def faint(string: str) -> str:
    """ Returns the string wrapped in faint ANSI color codes. """
    return Colors.FAINT + string + Colors.END

def italic(string: str) -> str:
    """ Returns the string wrapped in italic ANSI color codes. """
    return Colors.ITALIC + string + Colors.END

def underline(string: str) -> str:
    """ Returns the string wrapped in underline ANSI color codes. """
    return Colors.UNDERLINE + string + Colors.END

def blink(string: str) -> str:
    """ Returns the string wrapped in blink ANSI color codes. """
    return Colors.BLINK + string + Colors.END

def negative(string: str) -> str:
    """ Returns the string wrapped in negative ANSI color codes. """
    return Colors.NEGATIVE + string + Colors.END

def crossed(string: str) -> str:
    """ Returns the string wrapped in crossed ANSI color codes. """
    return Colors.CROSSED + string + Colors.END