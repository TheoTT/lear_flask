# Linux下搭建基于python的VIM

参考：

https://www.jianshu.com/p/297802d16fb4?from=timeline&isappinstalled=0



​	之前自动补全用的是jedi，手感一般，还是YCM流匹（自动补全，goto，什么都有）。



### 第一步，先安装Vundle（注意，一定要先下载Vundle，因为后面的所有的插件都需要用Vundle来管理）

```
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
```

编辑配置文件vimrc添加如下内容:

```
"去除VI一致性,必须
set nocompatible
"必须             
filetype off                  
 
"设置Vundle的运行路径
set rtp+=~/.vim/bundle/Vundle.vim
"设置插件的安装路径,vundle插件起始标志
call vundle#begin('~/.vim/bundle')
 
"让vundle管理插件版本
Plugin 'VundleVim/Vundle.vim'
"你的所有插件需要在下面这行之前
call vundle#end()
"加载vim自带和插件相应的语法和文件类型相关脚本
filetype plugin indent on

```

进入vim，的命令模式，执行PluginInstall

```
#Plugin的常用命令参考：
PluginList

PluginInstall

#PluginClean --(delete Plugin:删除插件只需要在vimrc配置文件中注释掉插件，在vim中用PluginClean进行清理)


```



当前完整的配置文件如下：

```
"去除VI一致性,必须
set nocompatible
"必须             
filetype off

"设置Vundle的运行路径
set rtp+=~/.vim/bundle/Vundle.vim
"设置插件的安装路径,vundle插件起始标志
call vundle#begin('~/.vim/bundle')

"让vundle管理插件版本
Plugin 'VundleVim/Vundle.vim'

"添加nerdtree插件
Plugin 'scrooloose/nerdtree'
"使用tab键切换窗口与目录树
Plugin 'jistr/vim-nerdtree-tabs'
"添加jedi-vim代码补全插件
"Plugin 'davidhalter/jedi-vim'
Plugin 'Valloric/YouCompleteMe'

"python语法检测
Plugin 'scrooloose/syntastic'

"添加PEP8代码风格检查
Plugin 'nvie/vim-flake8'
"配色方案
Plugin 'jnurmine/Zenburn'
Plugin 'altercation/vim-colors-solarized'
"代码折叠插件
Plugin 'tmhedberg/SimpylFold'
"自动缩进
Plugin 'vim-scripts/indentpython.vim'
"在vim的normal模式下搜索文件
Plugin 'kien/ctrlp.vim'
"Powerline状态栏
Plugin 'Lokaltog/powerline', {'rtp': 'powerline/bindings/vim/'}

"你的所有插件需要在下面这行之前
call vundle#end()


"设置分割窗口
set splitbelow
set splitright
"设置窗口移动快捷键
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>
"设置按F2启动NerdTree
map <F2> :NERDTreeToggle<CR>

"youcompleteme  默认tab  s-tab 和自动补全冲突
""let g:ycm_key_list_select_completion=['<c-n>']
let g:ycm_key_list_select_completion = ['<Down>']
"let g:ycm_key_list_previous_completion=['<c-p>']
"let g:ycm_key_list_previous_completion = ['<Up>']
"关闭加载.ycm_extra_conf.py提示
let g:ycm_confirm_extra_conf=0
" 开启 YCM 基于标签引擎
"let g:ycm_collect_identifiers_from_tags_files=1 
" 从第2个键入字符就开始罗列匹配项
let g:ycm_min_num_of_chars_for_completion=2
" 禁止缓存匹配项,每次都重新生成匹配项
"let g:ycm_cache_omnifunc=0  
" 语法关键字补全
let g:ycm_seed_identifiers_with_syntax=1
"force recomile with syntastic
"nnoremap <F5> :YcmForceCompileAndDiagnostics<CR>    
"nnoremap <leader>lo :lopen<CR> "open locationlist
"nnoremap <leader>lc :lclose<CR>    "close locationlist
"inoremap <leader><leader> <C-x><C-o>
"在注释输入中也能补全
let g:ycm_complete_in_comments = 1 
"注释和字符串中的文字也会被收入补全
let g:ycm_collect_identifiers_from_comments_and_strings = 0

"goto,YCM提供的跳跃功能采用了vim的jumplist，往前跳和往后跳的快捷键为Ctrl+O以及Ctrl+I。
nnoremap <leader>gl :YcmCompleter GoToDeclaration<CR>
nnoremap <leader>gf :YcmCompleter GoToDefinition<CR>
nnoremap <leader>gg :YcmCompleter GoToDefinitionElseDeclaration<CR>


"隐藏目录树种的.pyc文件
let NERDTreeIgnore=['\.pyc$', '\~$'] "ignore files in NERDTree

"设置主题颜色，以及设置快捷键F5
if has('gui_running')
  set background=dark
  colorscheme solarized
else
  colorscheme zenburn
endif
call togglebg#map("<F5>")

"syntastic
"设置error和warning的标志
let g:syntastic_enable_signs = 1
let g:syntastic_error_symbol='✗'
let g:syntastic_warning_symbol='►'
"总是打开Location List（相当于QuickFix）窗口，如果你发现syntastic因为与其他插件冲突而经常崩溃，将下面选项置0
let g:syntastic_always_populate_loc_list = 1
"自动打开Locaton List，默认值为2，表示发现错误时不自动打开，当修正以后没有再发现错误时自动关闭，置1表示自动打开自动关闭，0表示关闭自动打开>和自动关闭，3表示自动打开，但不自动关闭
let g:syntastic_auto_loc_list = 1

"开启代码折叠
set foldmethod=indent
set foldlevel=99
"设置快捷键为空格
nnoremap <space> za
"显示折叠代码的文档字符串
let g:SimpylFold_docstring_preview=1

"python代码缩进PEP8风格
au BufNewFile,BufRead *.py,*.pyw set tabstop=4
au BufNewFile,BufRead *.py,*.pyw set softtabstop=4
au BufNewFile,BufRead *.py,*.pyw set shiftwidth=4
au BufNewFile,BufRead *.py,*.pyw set textwidth=79
au BufNewFile,BufRead *.py,*.pyw set expandtab
au BufNewFile,BufRead *.py,*.pyw set autoindent
au BufNewFile,BufRead *.py,*.pyw set fileformat=unix

"对其他文件类型设置au命令
au BufNewFile,BufRead *.js, *.html, *.css set tabstop=2
au BufNewFile,BufRead *.js, *.html, *.css set softtabstop=2
au BufNewFile,BufRead *.js, *.html, *.css set shiftwidth=2
"高亮显示行伟不必要的空白字符
highlight Whitespace ctermbg=red guibg=red
au BufRead,BufNewFile *.py,*.pyw,*.c,*.h match Whitespace /\s\+$\ \+/
"设置行号显示
set nu

"设置utf-8编码
set encoding=utf-8

let python_highlight_all=1
syntax on

"加载vim自带和插件相应的语法和文件类型相关脚本
filetype plugin indent on

                                                              
```



## 总结

可能需要安装的依赖包：

pylama、jedi

sudo pip3 install pylama

sudo pip3 install jedi



可能会出现^M的报错

替换^M字符
在[Linux](http://lib.csdn.net/base/linux)下使用vi来查看一些在Windows下创建的文本文件，有时会发现在行尾有一些“^M”。有几种方法可以处理。

1.使用dos2unix命令。一般的分发版本中都带有这个小工具（如果没有可以根据下面的连接去下载），使用起来很方便(推荐使用):
$ dos2unix myfile.txt
上面的命令会去掉行尾的^M。

2.使用vi的替换功能。启动vi，进入命令模式，输入以下命令:
:%s/^M$//g # 去掉行尾的^M。

:%s/^M//g # 去掉所有的^M。

:%s/^M/[ctrl-v]+[enter]/g # 将^M替换成回车。

:%s/^M/\r/g # 将^M替换成回车。

3.使用sed命令。和vi的用法相似：
$ sed -e ‘s/^M/\n/g’ myfile.txt

注意：这里的“^M”要使用“CTRL-V CTRL-M”生成，而不是直接键入“^M”。（么按出来，可能是与操作系统的复制快捷键冲突，我是在windows操作系统下ssh到服务器的）