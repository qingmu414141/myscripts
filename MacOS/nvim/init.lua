-- 基础设置
require("basic")

-- 快捷键映射
require("keybindings")

-- Packer 插件管理
require("plugins")

-- 主体设置
require("colorscheme")

-- 插件配置
require("nvim-tree").setup({
  sort_by = "case_sensitive",
  view = {
    width = 30,
  },
  renderer = {
    group_empty = true,
  },
  filters = {
    dotfiles = true,
  },
})
require("plugin-config.bufferline")
require("plugin-config.lualine")
