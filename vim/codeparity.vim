" CodeParity colorscheme: Gruvbox accents on charcoal / soft grey.
hi clear
if exists('syntax_on') | syntax reset | endif
let g:colors_name = 'codeparity'

if &background ==# 'light'
  let s:bg0='#e2e4e6' | let s:bg1='#ebecee' | let s:bg2='#d8dadc' | let s:bg3='#c2c6ca'
  let s:fg='#282c34' | let s:dim='#665c54' | let s:red='#9d0006' | let s:green='#79740e'
  let s:yellow='#b57614' | let s:blue='#076678' | let s:purple='#8f3f71' | let s:aqua='#427b58' | let s:orange='#af3a03'
else
  let s:bg0='#181818' | let s:bg1='#1e1e1e' | let s:bg2='#2a2a2a' | let s:bg3='#3a3a3a'
  let s:fg='#ebdbb2' | let s:dim='#a89984' | let s:red='#fb4934' | let s:green='#b8bb26'
  let s:yellow='#fabd2f' | let s:blue='#83a598' | let s:purple='#d3869b' | let s:aqua='#8ec07c' | let s:orange='#fe8019'
endif
let s:groups = {
\ 'Normal': [s:fg,s:bg0], 'NormalFloat': [s:fg,s:bg1], 'CursorLine': ['NONE',s:bg1],
\ 'LineNr': [s:dim,s:bg0], 'CursorLineNr': [s:yellow,s:bg1], 'Comment': [s:dim,'NONE'],
\ 'Constant': [s:purple,'NONE'], 'String': [s:green,'NONE'], 'Character': [s:green,'NONE'],
\ 'Number': [s:purple,'NONE'], 'Boolean': [s:purple,'NONE'], 'Identifier': [s:blue,'NONE'],
\ 'Function': [s:green,'NONE'], 'Statement': [s:red,'NONE'], 'Keyword': [s:red,'NONE'],
\ 'Type': [s:yellow,'NONE'], 'Special': [s:orange,'NONE'], 'PreProc': [s:aqua,'NONE'],
\ 'Operator': [s:fg,'NONE'], 'Visual': [s:fg,s:bg3], 'Search': [s:bg0,s:yellow],
\ 'Error': [s:red,'NONE'], 'Todo': [s:orange,s:bg1], 'StatusLine': [s:fg,s:bg2],
\ 'StatusLineNC': [s:dim,s:bg1], 'Pmenu': [s:fg,s:bg1], 'PmenuSel': [s:bg0,s:blue],
\ 'VertSplit': [s:bg3,s:bg0], 'Directory': [s:blue,'NONE'] }
for [s:name, s:colors] in items(s:groups)
  execute 'hi ' . s:name . ' guifg=' . s:colors[0] . ' guibg=' . s:colors[1] . ' ctermfg=NONE ctermbg=NONE'
endfor
hi Comment gui=italic
hi Statement gui=bold
hi Function gui=bold
