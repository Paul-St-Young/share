#!/bin/bash
# source: VIM and Python - a Match Made in Heaven, Real Python, https://realpython.com/blog/python/vim-and-python-a-match-made-in-heaven/

# !!!! backup your .vimrc first !!!!

sudo apt-get remove vim-tiny -y
sudo apt-get update -y
sudo apt-get install vim -y

sudo apt-get install git -y
git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim

echo "
set nocompatible              \" required
filetype off                  \" required

\" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

\" alternatively, pass a path where Vundle should install plugins
\"call vundle#begin('~/some/path/here')

\" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'

\" Add all your plugins here (note older versions of Vundle used Bundle instead of Plugin)


\" All of your Plugins must be added before the following line
call vundle#end()            \" required
filetype plugin indent on    \" required

set splitbelow
set splitright
\"split navigations
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

\" Enable folding
set foldmethod=indent
set foldlevel=99

\" Enable folding with the spacebar
nnoremap <space> za

" > .vimrc
