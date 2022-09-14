from abc import ABC
from enum import Enum


class VimMode(Enum):
    NORMAL = 'normal'
    INSERT = 'insert'
    VISUAL = 'visual'
    VISUAL_BLOCK = 'visual_block'
    VISUAL_LINE = 'visual_line'

