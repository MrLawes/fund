import os

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def create_pdf_with_images(output_pdf_path, images_folder):
    """
    创建PDF并将图片按一行两个，共8行的方式排版

    Args:
        output_pdf_path (str): 输出PDF文件路径
        images_folder (str): 图片文件夹路径
    """
    # 设置PDF页面大小（A4）
    page_width, page_height = A4
    c = canvas.Canvas(output_pdf_path, pagesize=A4)

    # 获取图片列表
    image_files = [f for f in os.listdir(images_folder)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # 图片布局参数
    images_per_row = 2
    max_rows = 8
    images_per_page = images_per_row * max_rows

    # 计算图片尺寸和间距
    margin_x = 50
    margin_y = 50
    spacing_x = 20
    spacing_y = 20

    # 计算每个图片的可用空间
    available_width = page_width - 2 * margin_x
    available_height = page_height - 2 * margin_y
    image_width = (available_width - (images_per_row - 1) * spacing_x) / images_per_row
    image_height = (available_height - (max_rows - 1) * spacing_y) / max_rows

    # 分页处理图片
    for page_start in range(0, len(image_files), images_per_page):
        # 如果不是第一页，需要新建一页
        if page_start > 0:
            c.showPage()

        # 获取当前页的图片
        page_images = image_files[page_start:page_start + images_per_page]

        # 在当前页放置图片
        for idx, image_file in enumerate(page_images):
            row = idx // images_per_row
            col = idx % images_per_row

            # 计算图片位置（注意PDF坐标系从左下角开始）
            x = margin_x + col * (image_width + spacing_x)
            y = page_height - margin_y - (row + 1) * image_height - row * spacing_y

            # 图片完整路径
            image_path = os.path.join(images_folder, image_file)

            try:
                # 打开图片并调整尺寸
                with Image.open(image_path) as img:
                    # 保持图片比例
                    img_width, img_height = img.size
                    ratio = min(image_width / img_width, image_height / img_height)
                    scaled_width = img_width * ratio
                    scaled_height = img_height * ratio

                    # 调整位置使图片居中
                    x_offset = (image_width - scaled_width) / 2
                    y_offset = (image_height - scaled_height) / 2

                # 绘制图片
                c.drawImage(image_path,
                            x + x_offset,
                            y + y_offset,
                            width=scaled_width,
                            height=scaled_height)
            except Exception as e:
                print(f"无法处理图片 {image_file}: {e}")

    # 保存PDF
    c.save()
    print(f"PDF已创建: {output_pdf_path}")


# 使用示例
if __name__ == "__main__":
    # 设置输出PDF路径和图片文件夹路径
    output_pdf = "images_layout.pdf"
    # 创建PDF
    create_pdf_with_images(output_pdf, "./images")
