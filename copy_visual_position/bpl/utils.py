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

class CounterTimer():
    """
    A simple timer.
    """

    def __init__(self):
        """
        Initialize the CounterTimer.
        """
        self.start = time.perf_counter()

    def reset_time(self):
        """
        Reset the timer.
        """
        self.start = time.perf_counter()

    def get_time(self):
        """
        Get the elapsed time since the timer started.

        Returns:
            float: Elapsed time in seconds.
        """
        return time.perf_counter() - self.start
        
    def get_str_time(self):
        """
        Get the elapsed str time since the timer started.

        Returns:
            str: Elapsed time formatted as a string.
        """
        return get_formatted_time(self.get_time())
        
def format_property_name(name):
    """
    Formats a property name from snake_case to Title Case and replaces underscores with spaces.
    
    Parameters:
    name (str): The property name in snake_case.
    
    Returns:
    str: The formatted property name in Title Case with spaces.
    """
    # Split the name at underscores, capitalize each part, and join them with spaces
    formatted_name = ' '.join(word.capitalize() for word in name.split('_'))
    return formatted_name

def get_formatted_time(time_in_seconds):
    """
    Formats the elapsed time into a readable string, including milliseconds.

    Args:
        time_in_seconds (float): Time in seconds to format.

    Returns:
        str: Formatted elapsed time as a string.
    """
    milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
    
    if time_in_seconds < 1:
        return f"{milliseconds} ms"
    elif time_in_seconds < 60:
        return f"{int(time_in_seconds)} seconds and {milliseconds} ms"
    elif time_in_seconds < 3600:
        minutes, seconds = divmod(time_in_seconds, 60)
        return f"{int(minutes)} minutes, {int(seconds)} seconds and {milliseconds} ms"
    else:
        hours, remainder = divmod(time_in_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds and {milliseconds} ms"