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
from typing import List

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

    def get_time(self) -> float:
        """
        Get the elapsed time since the timer started.

        Returns:
            float: Elapsed time in seconds.
        """
        return time.perf_counter() - self.start

    def get_str_time(self) -> str:
        """
        Get the elapsed str time since the timer started.

        Returns:
            str: Elapsed time formatted as a string.
        """
        return get_formatted_time(self.get_time())

def format_property_name(name: str) -> str:
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

def get_formatted_time(
    time_in_seconds: float, 
    compact: bool = False,
) -> str:
    """
    Formats the elapsed time into a readable string, including milliseconds.

    Args:
        time_in_seconds (float): Time in seconds to format.
        compact (bool): If True, returns a compact format like '1h 2m 3s 456ms'.

    Returns:
        str: Formatted elapsed time as a string.
    """
    milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
    seconds_total = int(time_in_seconds)
    hours, remainder = divmod(seconds_total, 3600)
    minutes, seconds = divmod(remainder, 60)

    if compact:
        parts: List[str] = []
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if seconds:
            parts.append(f"{seconds}s")
        if milliseconds:
            parts.append(f"{milliseconds}ms")
        if not parts:  # time is 0
            parts.append("0ms")
        return ' '.join(parts)

    # Full verbose format
    if time_in_seconds < 1:
        return f"{milliseconds} ms"
    elif time_in_seconds < 60:
        return f"{seconds} seconds and {milliseconds} ms"
    elif time_in_seconds < 3600:
        return f"{minutes} minutes, {seconds} seconds and {milliseconds} ms"
    else:
        return f"{hours} hours, {minutes} minutes, {seconds} seconds and {milliseconds} ms"

def get_formatted_time_as_seconds(
    time_in_seconds: float, 
    compact: bool = False,
    min_decimals: int = 1,
) -> str:
    """
    Formats the elapsed time showing only full seconds.

    Args:
        time_in_seconds (float): Time in seconds to format.
        compact (bool): If True, returns a compact format like '12s'.

    Returns:
        str: Formatted time as a string.
    """
    format_str = f"{{:.{min_decimals}f}}"

    if compact:
        return format_str.format(time_in_seconds) + "s"
    else:
        value_str = format_str.format(time_in_seconds)
        if time_in_seconds == 1.0:
            return value_str + " second"
        else:
            return value_str + " seconds"