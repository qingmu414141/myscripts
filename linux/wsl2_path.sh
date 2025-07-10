#!/bin/bash

# 检查是否提供了参数
if [ $# -eq 0 ]; then
    echo "Usage: $0 <windows_path>"
    exit 1
fi

# 获取第一个参数
windows_path="$1"

# 转换路径格式：
# 1. 将反斜杠替换为正斜杠
# 2. 将盘符(C:, D:等)转换为/mnt/小写盘符
# 3. 处理路径中的空格
converted=$(echo "$windows_path" | sed -e 's#\\#/#g' -e 's#^\([A-Za-z]\):#/mnt/\L\1#')

# 打印转换结果
echo "$converted"
