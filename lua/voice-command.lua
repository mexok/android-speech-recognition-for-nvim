--[[
--
--  Plugin for voice-command. The main idea is to store word commands as a table
--  on a per-mode basis. It will then traverse the words to find commands. If
--  commands are ambigious, it will temporary hold the unmatched commands in a
--  buffer until finalized.
--
--  It will try to match from the beginning, not skipping any words at the
--  start. As of now, numbers are always passed directly and immediate.
--
--]]


local vcmd = {}
vcmd.cmds = {}
vcmd.preprocessor = {}
vcmd.buffer = {}

function vcmd.setup()
end

function vcmd.set(mode, words, cmd)
    --[[
    --    n ... normal mode
    --    v ... visual and select mode (including block and line mode)
    --    x ... visual mode (including block and line mode)
    --    s ... select mode (including block and line mode)
    --    i ... insert mode
    --    c ... command mode
    --    o ... operator pending mode
    --    a ... all modes
    --]]
    if (type(mode) == 'table') then
        for _, value in pairs(mode) do
            vcmd.set(value, words, cmd)
        end
        return
    end
    if (type(words) == 'table') then
        for _, w in pairs(words) do
            vcmd.set(mode, w, cmd)
        end
        return
    end
    _set_voice_cmd(mode, words, cmd)
end

function _set_voice_cmd(mode, words, cmd)
    if (mode == 'a') then
        _set_voice_cmd('n', words, cmd)
        _set_voice_cmd('v', words, cmd)
        _set_voice_cmd('i', words, cmd)
        _set_voice_cmd('c', words, cmd)
        _set_voice_cmd('o', words, cmd)
        return
    elseif (mode == 'v') then
        _set_voice_cmd('x', words, cmd)
        _set_voice_cmd('s', words, cmd)
        return
    end
    possible_raw_modes = {n=true, x=true, s=true, i=true, c=true, o=true}
    assert(possible_raw_modes[mode] ~= nil, string.format("Invalid mode '%s'", mode))
    local v = vim.g.vcmd
    if (type(v.cmds[mode]) ~= 'table') then
        v.cmds[mode] = {}
    end
    words = _get_splitted_words(words)
    curr = v.cmds[mode]
    for _, word in pairs(words) do
        if (type(curr[word]) ~= 'table') then
            curr[word] = {}
        end
        curr = curr[word]
    end
    curr['_cmd'] = cmd
    vim.g.vcmd = v
end

function _get_splitted_words(words)
    splitted_words = words
    if (type(splitted_words) ~= 'table') then
        splitted_words = {}
        for word in string.gmatch(words, "[^%s]+") do
            table.insert(splitted_words, word)
        end
    end
    return splitted_words
end

function vcmd.define_replacement(word, replacement)
    local v = vim.g.vcmd
    v.preprocessor[word] = replacement
    vim.g.vcmd = v
end

function vcmd.exec(words)
    local v = vim.g.vcmd
    words = _get_splitted_words(words)
    for i = 1, #words do
        if (v.preprocessor[words[i]] ~= nil) then
            words[i] = v.preprocessor[words[i]]
        end
    end
    table.move(words, 1, #words, #v.buffer + 1, v.buffer)
    vim.g.vcmd = v
    _process_buffer()
end

function _process_buffer()
    local v = vim.g.vcmd
    local m = _get_current_mode()
    if (type(v.cmds[m]) ~= 'table') then
        -- no mode mapping available, falling back to single word processing
        for _, word in pairs(v.buffer) do
            _finalize_unmatched_single_word(word)
        end
        v.buffer = {}
        vim.g.vcmd = v
        return
    end

    t = v.cmds[m]
    to_remove = 0
    while (#v.buffer > to_remove) do
        to_remove = to_remove + 1
        next_word = v.buffer[to_remove]
        if (t[next_word] == nil) then
            _finalize_unchecked_command(t['_cmd'])
            for i=1, to_remove-1, 1 do
                table.remove(v.buffer, 1)
            end
            to_remove = 1
            t = v.cmds[m]
            if (t[next_word] == nil) then
                _finalize_unmatched_single_word(next_word)
                table.remove(v.buffer, 1)
                to_remove = 0
            else
                t = t[next_word]
            end
        else
            t = t[next_word]
        end
    end
    _finalize_unchecked_command(t['_cmd'])
    v.buffer = {}
    vim.g.vcmd = v
end

function _get_current_mode()
    local m = vim.api.nvim_command_output("echo mode()")
    if (m == 'n') then
        return 'n'
    elseif (m == 'v' or m == 'V' or m == '^V') then
        return 'x'
    elseif (m == 's' or m == 'S' or m == '^S') then
        return 's'
    elseif (m == 'i') then
        return 'i'
    elseif (m == 'c') then
        return 'c'
    elseif (m == 'o') then
        return 'o'
    else
        return ''
    end
end

function _finalize_unmatched_single_word(word)
    if not word:match("%D") then
        _feed_input(word)
    end
end

function _finalize_unchecked_command(cmd)
    if (type(cmd) == 'string') then
        _feed_input(cmd)
    end
end

function _feed_input(cmd)
    vim.api.nvim_feedkeys(vim.api.nvim_replace_termcodes(cmd, true, false, true), 'm', false)
end


vim.g.vcmd = vcmd

return vcmd

