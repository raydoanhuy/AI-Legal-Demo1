import os
import re
from docx import Document

# Đường dẫn thư mục chứa file .docx (tương đối với repository)
input_folder = "legal_docs"
output_file = "training_data.txt"

# Hàm để đọc nội dung từ file .docx
def read_docx(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                full_text.append(text)
        return "\n".join(full_text)
    except Exception as e:
        print(f"Lỗi khi đọc {file_path}: {e}")
        return ""

# Hàm làm sạch dữ liệu: Xóa thông tin nhạy cảm
def clean_text(text):
    text = re.sub(r'\b\d{9}\b|\b\d{12}\b', '[Số CMND]', text)
    text = re.sub(r'\b(Ông|Bà)?\s*[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b', '[Tên Khách Hàng]', text)
    text = re.sub(r'\b0\d{9}\b', '[Số Điện Thoại]', text)
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[Email]', text)
    text = re.sub(r'\b\d{10,13}\b', '[Mã Số Thuế]', text)
    return text

# Danh sách để lưu nội dung tất cả file
all_content = []

# Kiểm tra thư mục tồn tại
if not os.path.exists(input_folder):
    print(f"Thư mục {input_folder} không tồn tại!")
    exit(1)

# Duyệt qua tất cả file trong thư mục
for filename in os.listdir(input_folder):
    if filename.endswith(".docx"):
        file_path = os.path.join(input_folder, filename)
        print(f"Đang xử lý: {filename}")
        content = read_docx(file_path)
        if content:
            cleaned_content = clean_text(content)
            all_content.append(cleaned_content)

# Kiểm tra nếu không có nội dung
if not all_content:
    print("Không tìm thấy file .docx nào để xử lý!")
    exit(1)

# Gộp tất cả nội dung vào một file lớn với ký tự phân cách "==="
with open(output_file, "w", encoding="utf-8") as f:
    for i, content in enumerate(all_content):
        f.write(content)
        if i < len(all_content) - 1:
            f.write("\n===\n")

print(f"Đã gộp tất cả nội dung vào {output_file}")
