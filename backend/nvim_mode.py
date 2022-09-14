from abc import ABC
from enum import Enum


class VimMode(Enum):
    NORMAL = 'normal'
    INSERT = 'insert'
    VISUAL = 'visual'
    VISUAL_BLOCK = 'visual_block'
    VISUAL_LINE = 'visual_line'
    OTHER = 'other'


def get_vim_mode(m: str) -> VimMode:
    if m == 'n':
        return VimMode.NORMAL
    elif m == 'i':
        return VimMode.INSERT
    elif m == 'v':
        return VimMode.VISUAL
    elif m == 'V':
        return VimMode.VISUAL_LINE
    elif m == '^V':
        return VimMode.VISUAL_BLOCK
    else:
        return VimMode.OTHER

