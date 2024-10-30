import base64

def read_base64_from_file(file_path):
    with open(file_path, 'r') as file:
        base64_string = file.read()
    return base64_string

def base64_to_image(base64_string, output_file):
    # 解码 base64 字符串
    image_data = base64.b64decode(base64_string)
    
    # 将解码后的数据写入文件
    with open(output_file, 'wb') as f:
        f.write(image_data)

# 包含 base64 编码的文件路径
base64_file_path = "base64code.txt"

# 输出图片文件名
output_file = "output_image.jpg"

# 读取 base64 编码字符串
base64_string = read_base64_from_file(base64_file_path)

# 调用函数将 base64 编码解码并保存为图片
base64_to_image(base64_string, output_file)