local packer = require("packer")
packer.startup({
	function(use)
	-- Packer 可以管理自己本身
	use 'wbthomason/packer.nvim'
	-- 你的插件列表...
--------------------- colorschemes --------------------
	-- tokyonight
	use("folke/tokyonight.nvim")
	-- OceanicNext
	use("mhartington/oceanic-next")
	-- gruvbox
	use({ "ellisonleao/gruvbox.nvim", requires = { "rktjmp/lush.nvim" } })
	-- zephyr 暂时不推荐，详见上边解释
	-- use("glepnir/zephyr-nvim")
	-- nord
	use("shaunsingh/nord.nvim")
-- onedark
	use("ful1e5/onedark.nvim")
	-- nightfox
	use("EdenEast/nightfox.nvim")
-------------------------------------------------------
	-- nvim-tree(侧边栏)
	use({ 'kyazdani42/nvim-tree.lua', requires = 'kyazdani42/nvim-web-devicons' })
	-- bufferline(顶部标签页)
	use({'akinsho/bufferline.nvim', tag = "*", requires = 'nvim-tree/nvim-web-devicons'})
-- lualine(底部信息信息显示栏)
	use { 'nvim-lualine/lualine.nvim',  requires = { 'nvim-tree/nvim-web-devicons', opt = true }}
	end,
	config = {
		display = {
			open_fn = function()
				return require("packer.util").float({ border = "single"}) 
			end,
		},
	},
})

-- 每次保存 plugins.lua 自动安装插件
pcall(
	vim.cmd,
	[[
		augroup packer_user_config
		autocmd!
		autocmd BufWritePost plugins.lua source <afile> | PackerSync
		augroup end
	]]
)
