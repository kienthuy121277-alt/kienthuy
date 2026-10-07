import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện ứng dụng
st.set_page_config(page_title="AI Tạo Đề Kiểm Tra CV 7991", page_icon="📝", layout="wide")

st.title("📝 Ứng dụng AI Tạo Ma Trận, Bản Đặc Tả & Đề Kiểm Tra")
st.caption("Chuẩn hóa theo Công văn 7991/BGDĐT-GDTrH của Bộ Giáo dục và Đào tạo")

# Thanh cấu hình bên trái (Sidebar)
with st.sidebar:
    st.header("⚙️ Cấu hình Hệ thống")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")
    
    st.header("📋 Thông tin Đề kiểm tra")
    mon_hoc = st.selectbox("Môn học:", [
        "Toán học", "Ngữ văn", "Tiếng Anh", "Vật lí", "Hóa học", 
        "Sinh học", "Lịch sử", "Địa lí", "GDKT&PL", "Tin học", "KHTN"
    ])
    khoi_lop = st.selectbox("Khối lớp:", [
        "Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"
    ])
    loai_de = st.selectbox("Loại đề:", ["Kiểm tra Giữa kỳ", "Kiểm tra Cuối kỳ"])
    thoi_gian = st.number_input("Thời gian làm bài (phút):", value=60, step=15)
    chu_de = st.text_area("Nội dung / Chủ đề kiểm tra:", value="Ví dụ: Chương 1 - Biến đổi khí hậu")

# Lệnh yêu cầu gửi đến AI (Prompt chuẩn 7991)
PROMPT_CV7991 = f"""
Bạn là chuyên gia kiểm tra đánh giá của Bộ Giáo dục và Đào tạo. Hãy xây dựng bộ hồ sơ kiểm tra đánh giá cho môn {mon_hoc} - {khoi_lop} ({loai_de}, thời gian {thoi_gian} phút) dựa trên phạm vi kiến thức: {chu_de}.

YÊU CẦU BẮT BUỘC TUÂN THỦ CÔNG VĂN 7991/BGDĐT-GDTrH:

I. MA TRẬN ĐỀ KIỂM TRẠ (Bảng Markdown):
Cấu trúc cột gồm: STT, Chủ đề/Chương, Nội dung/Đơn vị kiến thức.
Mức độ đánh giá chia theo các dạng bài:
1. Trắc nghiệm Nhiều lựa chọn (Nhận biết, Thông hiểu, Vận dụng).
2. Trắc nghiệm Đúng - Sai (mỗi câu gồm 4 ý a, b, c, d) (Nhận biết, Thông hiểu, Vận dụng).
3. Trắc nghiệm Trả lời ngắn (Nhận biết, Thông hiểu, Vận dụng).
4. Tự luận (Nhận biết, Thông hiểu, Vận dụng).
Tổng số câu, Tổng số điểm, Tỉ lệ % (Đảm bảo tổng tỉ lệ điểm là 100%).

II. BẢN ĐẶC TẢ ĐỀ KIỂM TRA (Bảng Markdown):
Thể hiện rõ: STT, Chủ đề/Chương, Nội dung/Đơn vị kiến thức, Yêu cầu cần đạt và Số câu hỏi tương ứng ở từng mức độ cho 4 dạng câu hỏi trên.

III. ĐỀ KIỂM TRẠ VÀ HƯỚNG DẪN CHẤM:
Tạo đề thi minh họa dựa đúng Ma trận và Đặc tả, gồm các phần:
- PHẦN I: Trắc nghiệm Nhiều lựa chọn (chọn 1 phương án đúng A, B, C, D).
- PHẦN II: Trắc nghiệm Đúng - Sai (Mỗi câu gồm lệnh hỏi và 4 ý a, b, c, d; chọn Đúng hoặc Sai cho mỗi ý).
- PHẦN III: Trắc nghiệm Trả lời ngắn.
- PHẦN IV: Tự luận.
- ĐÁP ÁN VÀ HƯỚNG DẪN CHẤM CHI TIẾT (Có thang điểm cụ thể cho từng ý).
"""

# Nút xử lý
if st.button("🚀 Khởi tạo Ma trận, Bản đặc tả & Đề kiểm tra"):
    if not api_key:
        st.error("Vui lòng nhập API Key để sử dụng!")
    elif not chu_de:
        st.warning("Vui lòng nhập nội dung/chủ đề kiểm tra!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            with st.spinner("AI đang tạo hồ sơ kiểm tra chuẩn Công văn 7991..."):
                response = model.generate_content(PROMPT_CV7991)
                
                st.success("Tạo thành công!")
                st.markdown("---")
                st.markdown(response.text)
                
                # Nút tải file kết quả
                st.download_button(
                    label="📥 Tải Đề thi & Ma trận về (.md)",
                    data=response.text,
                    file_name=f"De_kiem_tra_{mon_hoc}_{khoi_lop}_CV7991.md",
                    mime="text/markdown"
                )
        except Exception as e:
            st.error(f"Có lỗi xảy ra: {e}")