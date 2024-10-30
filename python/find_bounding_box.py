import os
import cv2
import numpy as np
import PIL.Image as Image

def load_images_from_folder(folder_path):
    """
    批量读取指定文件夹中的所有图片
    Args:
        folder_path (str): 图片文件夹路径
    
    Return:
    list: 成功加载的图片对象列表
    """
    # 获取文件夹的所有图片文件名
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    images = []
    file_name_without_extension = []
    for file_name in image_files:
        file_path = os.path.join(folder_path, file_name)
        try:
            image = Image.open(file_path)
            images.append(image)
            name_without_extension, _ = os.path.splitext(file_name)
            file_name_without_extension.append(name_without_extension)
            print(f"Load {file_name} with size {image.size} and format {image.format}")
        except IOError:
            print(f"Failed to load {file_name}")
    return images, file_name_without_extension

def find_bounding_box(image):
    """
    计算图像中主要对象的水平最小外接矩形框，并返回矩形的两个对角顶点坐标。

    参数:
    image (PIL.Image.Image): 输入的灰度图像

    返回:
    tuple: 矩形框的左上角和右下角坐标 (box[0], box[2])
    """
    
    # 创建二值化掩模
    _, binary = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)

    # 找到轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 检查是否找到了轮廓
    if len(contours) > 0:
        # 找到最大的轮廓 (假设这是主要的对象)
        largest_contour = max(contours, key=cv2.contourArea)

        # 获取水平最小外接矩形框
        x, y, w, h = cv2.boundingRect(largest_contour)

        # 矩形的四个顶点
        box = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])

        # 返回左上角和右下角坐标
        return tuple(box[0]), tuple(box[2])
    else:
        print("No contours found!")
        return None, None

if __name__ == "__main__":
    folder_path = '/Users/huchenghang/Documents/subjects'
    save_fold = '/Users/huchenghang/Documents/external_matrix_box/'
    images, file_name_without_extension = load_images_from_folder(folder_path)
    
    for image, file_name in zip(images, file_name_without_extension):
        save_path = os.path.join(save_fold, f"{file_name}.png")
        # 将 RGBA 图像的通道分离
        r, g, b, a = image.split()

        # 将 alpha 通道转换为 NumPy 数组
        mask_out = np.array(a)
        top_left, bottom_right = find_bounding_box(mask_out)
        # 左上角和右下角的坐标
        start_x, start_y = top_left[0], top_left[1]
        end_x, end_y = bottom_right[0], bottom_right[1]
        # 裁剪图像
        cropped_image = image.crop((start_x, start_y, end_x, end_y))
        cropped_image.save(save_path, format="PNG")
        

