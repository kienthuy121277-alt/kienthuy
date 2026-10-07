import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện ứng dụng
st.set_page_config(page_title="AI Tạo Đề Kiểm Tra Toán 6 - GK1 (CV 7991)", page_icon="📐", layout="wide")

st.title("📐 Ứng Dụng AI Tạo Ma Trận, Bản Đặc Tả & Đề Kiểm Tra Giữa HK1 - Toán 6")
st.caption("Khung cấu trúc chuẩn hóa theo Công văn số 7991/BGDĐT-GDTrH của Bộ Giáo dục và Đào tạo")

# Thanh cấu hình bên trái (Sidebar)
with st.sidebar:
    st.header("⚙️ Cấu hình Hệ thống")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")
    
    st.header("📋 Thông tin Đề kiểm tra")
    mon_hoc = st.text_input("Môn học:", value="Toán học", disabled=True)
    khoi_lop = st.text_input("Khối lớp:", value="Lớp 6", disabled=True)
    loai_de = st.text_input("Loại đề:", value="Kiểm tra Giữa kỳ 1", disabled=True)
    thoi_gian = st.number_input("Thời gian làm bài (phút):", value=90, step=15)
    
    st.markdown("---")
    st.write("**Chủ đề kiến thức GK1 (Mặc định):**")
    chu_de = st.text_area(
        "Nội dung trọng tâm:", 
        value="1. Tập hợp các số tự nhiên (Các phép tính, lũy thừa, thứ tự thực hiện phép tính).\n2. Tính chia hết trong tập hợp số tự nhiên (Dấu hiệu chia hết 2, 3, 5, 9; Số nguyên tố, Hợp số, ƯC & BC).\n3. Các hình phẳng trong thực tiễn (Hình vuông, Tam giác đều, Lục giác đều, Hình chữ nhật, Hình thoi, Hình bình hành, Hình thang cân).",
        height=150
    )

# Prompt tối ưu hóa riêng cho Toán 6 - Giữa Kỳ 1 chuẩn 7991
PROMPT_TOAN6_GK1 = f"""
Bạn là chuyên gia huấn luyện và ra đề thi môn Toán cấp THCS của Bộ Giáo dục và Đào tạo.
Hãy xây dựng bộ hồ sơ kiểm tra đánh giá đầy đủ cho môn TOÁN 6 - GIỮA HỌC KỲ 1 (Thời gian: {thoi_gian} phút).

Phạm vi kiến thức kiểm tra:
{chu_de}

YÊU CẦU BẮT BUỘC TUÂN THỦ CÔNG VĂN 7991/BGDĐT-GDTrH:

I. MA TRẬN ĐỀ KIỂM TRẠ GIỮA HK1 (Dạng Bảng Markdown):
Cột bao gồm: STT | Chủ đề/Chương | Nội dung/Đơn vị kiến thức | Trắc nghiệm Nhiều lựa chọn (Nhận biết, Thông hiểu, Vận dụng) | Trắc nghiệm Đúng - Sai (Nhận biết, Thông hiểu, Vận dụng) | Trắc nghiệm Trả lời ngắn (Nhận biết, Thông hiểu, Vận dụng) | Tự luận (Nhận biết, Thông hiểu, Vận dụng) | Tổng điểm | Tỉ lệ %

Lưu ý phân bổ điểm số:
- Tỉ lệ điểm: Khoảng 40% Nhận biết, 30% Thông hiểu, 30% Vận dụng (tổng 10,0 điểm).

II. BẢN ĐẶC TẢ ĐỀ KIỂM TRẠ (Dạng Bảng Markdown):
Liệt kê chi tiết: STT | Chủ đề/Chương | Nội dung/Đơn vị kiến thức | Yêu cầu cần đạt | Số câu hỏi chi tiết ở 4 dạng bài (Nhiều lựa chọn, Đúng-Sai, Trả lời ngắn, Tự luận).

III. ĐỀ KIỂM TRẠ MINH HỌA GIỮA HK1 TOÁN 6:
Tạo đề bài chính xác 100% dựa theo Ma trận và Bản đặc tả trên, chia làm 4 PHẦN RÕ RÀNG:
- PHẦN I: Trắc nghiệm Nhiều lựa chọn (Mỗi câu có 4 phương án A, B, C, D; chỉ có 1 phương án đúng).
- PHẦN II: Trắc nghiệm Đúng - Sai (Mỗi câu hỏi gồm 1 ngữ cảnh/câu lệnh và 4 ý a), b), c), d); Yêu cầu học sinh xác định từng ý là Đúng hay Sai).
- PHẦN III: Trắc nghiệm Trả lời ngắn (Mỗi câu yêu cầu học sinh tính toán và điền đáp số ngắn gọn).
- PHẦN IV: Tự luận (Các bài toán trình bày chi tiết từng bước: tính toán, tìm x, toán thực tế hình học/chia hết).

IV. ĐÁP ÁN VÀ HƯỚNG DẪN CHẤM CHI TIẾT:
- Đáp án chi tiết cho Phần I, Phần II, Phần III.
- Lời giải chi tiết và thang điểm cụ thể đến từng 0,25 điểm cho Phần IV (Tự luận).
"""

# Nút xử lý
if st.button("🚀 Khởi tạo Ma trận, Bản đặc tả & Đề thi Toán 6 GK1"):
    if not api_key:
        st.error("Vui lòng nhập Gemini API Key ở thanh bên trái!")
    elif not chu_de:
        st.warning("Vui lòng không để trống nội dung kiểm tra!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            with st.spinner("AI đang tạo Ma trận, Đặc tả và Đề thi Giữa HK1 Toán 6 chuẩn 7991..."):
                response = model.generate_content(PROMPT_TOAN6_GK1)
                
                st.success("Khởi tạo thành công hồ sơ kiểm tra Toán 6 Giữa HK1!")
                st.markdown("---")
                st.markdown(response.text)
                
                # Nút tải file
                st.download_button(
                    label="📥 Tải Đề thi & Ma trận về (.md)",
                    data=response.text,
                    file_name="De_kiem_tra_GK1_Toan_6_CV7991.md",
                    mime="text/markdown"
                )
        except Exception as e:
            st.error(f"Có lỗi xảy ra trong quá trình xử lý: {e}")