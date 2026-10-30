" CodeParity colorscheme: muted Gruvbox accents on soft charcoal / warm light.
hi clear
if exists('syntax_on') | syntax reset | endif
let g:colors_name = 'codeparity'

if &background ==# 'light'
  let s:bg0='#efeee9' | let s:bg1='#f5f4ef' | let s:bg2='#e5e3dc' | let s:bg3='#d4d1c8'
  let s:fg='#343633' | let s:dim='#716d63' | let s:red='#a65d55' | let s:green='#69764a'
  let s:yellow='#98733c' | let s:blue='#426e78' | let s:purple='#805b76' | let s:aqua='#54745c' | let s:orange='#a35f36'
else
  let s:bg0='#202124' | let s:bg1='#282a2d' | let s:bg2='#34363a' | let s:bg3='#484a4e'
  let s:fg='#d6d3c8' | let s:dim='#a39d90' | let s:red='#e47769' | let s:green='#a9ad68'
  let s:yellow='#d6b66d' | let s:blue='#83a6a0' | let s:purple='#c08ca3' | let s:aqua='#91ad85' | let s:orange='#d8965f'
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
