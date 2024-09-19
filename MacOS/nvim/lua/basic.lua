-- utf8
vim.g.encoding = "UTF-8"
vim.o.fileencoding = 'utf-8'

-- jkhl 移动时光标周围保留 8 行
vim.o.scrolloff = 8
vim.o.sidescrolloff = 8

-- 使用相对行号
vim.wo.number = true
vim.wo.relativenumber = true

-- 高度所在行
vim.wo.cursorline = true

-- 显示左侧图标指示列
vim.wo.signcolumn = "yes"

-- 右侧参考线,超过表示代码太长了,考虑换行
vim.wo.colorcolumn= "80"

-- 缩进 2 个空格等于一个 Tab
vim.o.tabstop = 2
vim.bo.tabstop = 2
vim.o.softtabstop = 2
vim.o.shiftround = true

-- >> << 时移动长度
vim.o.shiftwidth = 2
vim.bo.shiftwidth = 2

-- 新行对齐当前行
vim.o.autoindent = true
vim.bo.autoindent = true
vim.o.smartindent = true

-- 边输入边搜索
vim.o.incsearch = true

-- 命令行高为 2,提供足够的显示空间
vim.o.cmdheight = 2

-- 当文件被外部程序修改时,自动加载
vim.o.autoread = true
vim.bo.autoread = true

-- 禁止拆行
vim.wo.wrap = false

-- 光标在行首尾时<Left><Right>可以跳到下一行
vim.o.whichwrap = '<,>,[,]'

-- 允许隐藏被修改过的 buffer
vim.o.hidden = true

-- 鼠标支持
vim.o.mouse = "a"

-- smaller updatetime
vim.o.updatetime = 300

-- 设置 timeoutlen 为等待键盘连击时间 500 毫秒,可根据需要设置
vim.o.timeoutlen = 500

-- split window 从下边和右边出现
vim.o.splitbelow = true
vim.o.splitright = true

-- 自动补全不自动选中
vim.g.completeout = "menu,menuone,noselect,noinsert"

-- 样式
vim.o.background = "dark"
vim.termguicolors = true
vim.termguicolors = true

-- 不可见字符的显示,这里只把空格显示为一个点
vim.o.list = true
vim.o.listchars = "space:."

-- 补全增强
vim.o.wildmenu = true

-- 补全最多显示 10 行
vim.o.pumheight = 10

-- 永远显示 tabline
vim.o.showtabline = 2

-- 使用增强状态栏插件后不再需要 vim 的模式提示
vim.o.showmode = false

