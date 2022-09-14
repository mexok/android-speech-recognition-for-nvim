
from typing import List

from pynvim import Nvim
from linguistic import ADDITIONAL_KEY_VISUAL_BLOCK_MODE, ADDITIONAL_KEY_VISUAL_LINE_MODE, KEY_ABOVE, KEY_APPEND, KEY_BACK, KEY_BELOW, KEY_ESCAPE, KEY_FRONT, KEY_VISUAL_MODE, MapCharModifier, is_key_copy, is_key_delete, is_key_insert, is_key_remove, map_char, get_map_char_modifier, map_hjkl
from nvim_mode import VimMode


class Context:
    def __init__(self, nvim: Nvim):
       self.vim_mode = VimMode.NORMAL
       self.nvim = nvim

    def process_words(self, words: List[str]):
        if self.vim_mode is VimMode.NORMAL:
            self._process_vim_mode_normal(words)
        elif self.vim_mode is VimMode.INSERT:
            self._process_vim_mode_insert(words)
        elif self.vim_mode in [VimMode.VISUAL, VimMode.VISUAL_LINE, VimMode.VISUAL_BLOCK]:
            self._process_vim_mode_visual(words)
        else:
            raise NotImplementedError()

    def _process_vim_mode_normal(self, words: List[str]):
        if len(words) == 0:
            return

        if words[0] == KEY_VISUAL_MODE:
            if len(words) == 2:
                if words[1] == ADDITIONAL_KEY_VISUAL_LINE_MODE:
                    self.nvim.input(b'V')
                    self.vim_mode = VimMode.VISUAL_LINE
                    return
                elif words[1] == ADDITIONAL_KEY_VISUAL_BLOCK_MODE:
                    self.nvim.input(b'<C-v>')
                    self.vim_mode = VimMode.VISUAL_BLOCK
                    return
            self.nvim.input(b'v')
            self.vim_mode = VimMode.VISUAL
            return

        if is_key_insert(words[0]):
            self.nvim.input('i')
            self.vim_mode = VimMode.INSERT
            return
        elif len(words) == 2 and is_key_insert(words[1]):
            if words[0] == KEY_ABOVE:
                self.nvim.input('O')
                self.vim_mode = VimMode.INSERT
            elif words[0] == KEY_BELOW:
                self.nvim.input('o')
                self.vim_mode = VimMode.INSERT
            elif words[0] == KEY_APPEND:
                self.nvim.input('a')
                self.vim_mode = VimMode.INSERT
            elif words[0] == KEY_FRONT:
                self.nvim.input('I')
                self.vim_mode = VimMode.INSERT
            elif words[0] == KEY_BACK:
                self.nvim.input('A')
                self.vim_mode = VimMode.INSERT
            return

        if len(words) == 1:
            hjkl = map_hjkl(words[0])
            if hjkl:
                self.nvim.input(hjkl)
        elif len(words) == 2:
            hjkl = map_hjkl(words[1])
            if words[0].isdigit() and hjkl:
                self.nvim.input(f"{words[0]}{hjkl}")

    def _process_vim_mode_insert(self, words: List[str]):
        map_char_modifier = MapCharModifier.NONE
        for word in words:
            c = map_char(word=word, map_char_modifier=map_char_modifier)
            if c:
                self.nvim.input(c)
            elif word == KEY_ESCAPE:
                self.nvim.input('<ESC>')
                self.vim_mode = VimMode.NORMAL
                return
            elif is_key_delete(word=word):
                self.nvim.input('<Left><Del>')
            elif is_key_remove(word=word):
                self.nvim.input('<Del>')
            else:
                map_char_modifier = get_map_char_modifier(word=word)

    def _process_vim_mode_visual(self, words: List[str]):
        if is_key_copy(words[0]):
            self.nvim.input('y')
            self.vim_mode = VimMode.NORMAL
        elif is_key_delete(words[0]):
            self.nvim.input('d')
            self.vim_mode = VimMode.NORMAL

