import os
from typing import Tuple

# #############################################################################
# ################################## Others ###################################
# #############################################################################

def _get_console_size() -> Tuple:
    rows, columns = os.popen('stty size', 'r').read().split()
    return (int(rows), int(columns))

# #############################################################################
# ############################### Text styling ################################
# #############################################################################
class TextColorUnix:
    END    = '\033[0m'
    RED    = '\033[31m'
    GREEN  = '\033[32m'
    YELLOW = '\033[33m'
    BLUE   = '\033[34m'
    PURPLE = '\033[35m'
    CYAN   = '\033[36m'

class StyleUnix:
    END       = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'


def _format(cls: object, param_name: str, text: str) -> str:
    """ Helper function for color(), and style() """
    param = getattr(cls, param_name.upper(), '')
    end = '' if len(param) == 0 else getattr(cls, 'END', '')
    return param + text + end

def color(color: str, text: str) -> str:
    """ Set text color """
    return _format(TextColorUnix, color, text)

def style(style: str, text: str) -> str:
    """ Set text style """
    return _format(StyleUnix, style, text)

def center(text: str):
    width = _get_console_size()[1]
    padding = int((width - len(text)) / 2)
    text = ' ' * padding + text
    text += ' ' * (width - len(text))
    return text

def section_name(text: str):
    width = _get_console_size()[1]
    padding = int((width - len(text)) / 2 - 1)
    text = '=' * padding + ' ' + text + ' '
    text += '=' * (width - len(text))
    return style('bold', color('green', text))

def iteration_name(text: str):
    width = _get_console_size()[1]
    padding = int((width - len(text)) / 2 - 1)
    text = '=' * padding + ' ' + text + ' '
    text += '=' * (width - len(text))
    return style('bold', color('cyan', text))
    
    