#!/bin/bash
# source: VIM and Python - a Match Made in Heaven, Real Python, https://realpython.com/blog/python/vim-and-python-a-match-made-in-heaven/

# !!!! backup your .vimrc first !!!!

sudo dnf update -y
sudo dnf install vim git -y

git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim

cp ~/.vimrc ~/.vimrc.bkp
echo "
\" use spaces instead of tabs
set tabstop=2
set shiftwidth=2
set expandtab

\" increase buffer size to copy lots of stuff
set viminfo='20,<1000,s1000

\"split navigations
set splitbelow
set splitright
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

\" Enable folding
set foldmethod=indent
set foldlevel=99

\" Enable folding with the spacebar
nnoremap <space> za

\" Vundle related stuff
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

" > ~/.vimrc
vim +PluginInstall +qall

sudo dnf update -y

sudo dnf install python-pip tkinter.x86_64 -y
# tkinter is needed by matplotlib.pyplot

sudo -H pip install --upgrade pip
sudo -H pip install jupyter numpy scipy pandas matplotlib
