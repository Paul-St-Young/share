set tabstop=2
set shiftwidth=2
set expandtab

" increase buffer size to copy lots of stuff
set viminfo='20,<1000,s1000
" automatically make search case sensitive
set smartcase

set autoindent
set fdm=indent

" don't save the annoying ~ files
set nobackup
set wildmenu
hi Folded ctermfg=DarkGray
hi Folded ctermbg=LightCyan

" Julia syntax highlighting through vundle
set nocompatible              " to be improved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
Plugin 'JuliaLang/julia-vim'
call vundle#end()            " required
filetype plugin indent on    " required

"Use TAB to complete when typing words, else inserts TABs as usual.
" !! just use ctrl+n instead
"Uses dictionary and source files to find matching words to complete.

"See help completion for source,
"Note: usual completion is on <C-n> but more trouble to press all the time.
"Never type the same word twice and maybe learn a new spellings!
"Use the Linux dictionary when spelling is in doubt.
"Window users can copy the file to their machine.
function! Tab_Or_Complete()
  if col('.')>1 && strpart( getline('.'), col('.')-2, 3 ) =~ '^\w'
    return "\<C-N>"
  else
    return "\<Tab>"
  endif
endfunction
":inoremap <Tab> <C-R>=Tab_Or_Complete()<CR>
