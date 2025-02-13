import fitz
import os

def extract_images_from_pdf(pdf_path, output_folder):
    # 打开 PDF 文件
    pdf_document = fitz.open(pdf_path)
    
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍历每一页
    imgs = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image_list = page.get_images(full=True)
        # 遍历每一页中的每一张图片
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = os.path.join(output_folder, f"page_{page_num + 1}_{img_index + 1}.{image_ext}")
            
            # 保存图片
            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)
                imgs.append(image_filename)
    
    print(f"提取完成，图片保存在 {output_folder} 文件夹中")
    return imgs

if __name__ == "__main__":
    pdf_path = "./example.pdf"
    output_folder = "./images"
    imgs = extract_images_from_pdf(pdf_path, output_folder)
    print("提取的图片：", imgs)