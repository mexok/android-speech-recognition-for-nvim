local vcmd = {}
vcmd.cmds = {}
vcmd.number_handling = 'normal'  -- numbers will always be redirected

function vcmd.setup()
end

function vcmd.set(mode, word, cmd)
    if (type(mode) == 'table')
    then
        for key, value in pairs(mode) do
            _set_voice_cmd(value, word, cmd)
        end
    else
        _set_voice_cmd(mode, word, cmd)
    end
end

function _set_voice_cmd(mode, word, cmd)
    --[[
    --    n ... normal mode
    --    v ... visual mode (including block visual mode and line visual mode)
    --    i ... insert mode
    --    a ... all modes (including command mode)
    --]]
    possible_modes = {n=true, v=true, i=true, a=true}
    assert(possible_modes[mode] ~= nil, string.format("Invalid mode '%s'", mode))
    local v = vim.g.vcmd
    if (type(v.cmds[word]) ~= 'table')
    then
        v.cmds[word] = {}
    end
    v.cmds[word][mode] = cmd
    vim.g.vcmd = v
end

function vcmd.json()
    return
end

vim.g.vcmd = vcmd

return vcmd

