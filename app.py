import streamlit as st
import pandas as pd
import datetime
import time
import PyPDF2
import google.generativeai as genai

# ==========================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN CHUNG
# ==========================================
st.set_page_config(page_title="LawEase MVP", page_icon="⚖️", layout="wide")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ==========================================
# 2. HỆ THỐNG ĐIỀU HƯỚNG
# ==========================================
st.sidebar.title("⚖️ LawEase Menu")
menu = st.sidebar.radio(
    "Chọn tính năng:",
    ["🏠 Trang Chủ", "📝 Tạo Hợp Đồng (Logic Tree)", "🤖 Trợ Lý AI Đọc PDF", "📁 Quản Lý Hồ Sơ (CRM)"]
)

st.sidebar.divider()
st.sidebar.info("Bản Demo MVP phục vụ thuyết trình cuộc thi Khởi nghiệp.")

# ==========================================
# 3. CÁC MODULE CHỨC NĂNG CHÍNH
# ==========================================

# --- MODULE 1: TRANG CHỦ ---
if menu == "🏠 Trang Chủ":
    st.title("⚖️ LawEase - Pháp lý tinh gọn cho Startup")
    st.markdown("### Giải pháp Tự động hóa Văn bản Pháp lý & Trợ lý Ảo thế hệ mới")
    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("Văn bản đã tự động hóa", "50+ Mẫu")
    col2.metric("Thời gian tạo hợp đồng", "2 Phút", "-98%")
    col3.metric("Độ chuẩn xác pháp lý", "100%")

    st.divider()
    st.info("👈 Vui lòng sử dụng thanh Menu bên trái để trải nghiệm bản Demo.")

# --- MODULE 2: TẠO HỢP ĐỒNG ---
elif menu == "📝 Tạo Hợp Đồng (Logic Tree)":
    st.title("📝 Trình Tạo Hợp Đồng Tự Động")
    st.write("Hệ thống rẽ nhánh điều khoản đảm bảo tính chính xác tuyệt đối mà không phụ thuộc vào AI tạo sinh.")

    with st.container(border=True):
        loai_hd = st.selectbox("1. Chọn loại văn bản cần tạo:", ["Hợp đồng Thử việc", "Thỏa thuận bảo mật (NDA)"])
        
        st.write("2. Thông tin các bên:")
        col1, col2 = st.columns(2)
        with col1:
            ten_cong_ty = st.text_input("Tên Doanh nghiệp (Bên A):", "Công ty Cổ phần Startup X")
            nguoi_dai_dien = st.text_input("Người đại diện:", "Ông Nguyễn Văn A")
        with col2:
            ten_nhan_vien = st.text_input("Tên Người/Đối tác (Bên B):", "Trần Thị C")
            cccd = st.text_input("Số CCCD/CMND:", "079123456789")

        st.write("3. Thỏa thuận cốt lõi:")
        if loai_hd == "Hợp đồng Thử việc":
            luong = st.number_input("Mức lương thỏa thuận (VNĐ):", min_value=0, step=500000, value=8000000)
            co_dong_bhxh = st.checkbox("Hỗ trợ đóng BHXH trong thời gian thử việc?")
        else:
            muc_phat = st.number_input("Mức phạt vi phạm (VNĐ):", min_value=10000000, step=10000000, value=50000000)
            thoi_han = st.slider("Thời hạn bảo mật (Năm):", 1, 5, 2)

    if st.button("🚀 Tạo Văn bản", type="primary"):
        ngay_hien_tai = datetime.date.today().strftime("%d/%m/%Y")
        if loai_hd == "Hợp đồng Thử việc":
            dieu_khoan_bhxh = "Bên A đóng đầy đủ BHXH cho Bên B." if co_dong_bhxh else "Bên B tự túc bảo hiểm."
            hop_dong_mau = f"""CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc\n\nHỢP ĐỒNG THỬ VIỆC\nNgày ký: {ngay_hien_tai}\n\nBÊN A: {ten_cong_ty.upper()} (Đại diện: {nguoi_dai_dien})\nBÊN B: {ten_nhan_vien.upper()} (CCCD: {cccd})\n\nĐiều 1: Lương thử việc {luong:,.0f} VNĐ/tháng.\nĐiều 2: {dieu_khoan_bhxh}"""
        else:
            hop_dong_mau = f"""CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc\n\nTHỎA THUẬN BẢO MẬT (NDA)\nNgày ký: {ngay_hien_tai}\n\nBÊN A: {ten_cong_ty.upper()}\nBÊN B: {ten_nhan_vien.upper()}\n\nĐiều 1: Thời hạn bảo mật {thoi_han} năm.\nĐiều 2: Vi phạm phạt {muc_phat:,.0f} VNĐ."""

        st.success("Đã tạo xong!")
        st.text_area("Bản xem trước:", hop_dong_mau, height=250)

# --- MODULE 3: TRỢ LÝ AI (TỰ ĐỘNG TÌM MODEL) ---
elif menu == "🤖 Trợ Lý AI Đọc PDF":
    st.title("🤖 Trợ Lý Phân Tích Hợp Đồng (AI Q&A)")
    st.write("Tải hợp đồng của bạn lên, AI sẽ phân tích và trích xuất thông tin chuẩn xác.")

    # 1. KẾT NỐI API & TỰ ĐỘNG CHỌN MODEL (Chiến thuật Bulletproof)
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
        
        # Thuật toán tự tìm model khả dụng thay vì hardcode
        working_model = None
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                working_model = m.name
                break # Lấy ngay model đầu tiên dùng được
                
        if working_model:
            model = genai.GenerativeModel(working_model)
            # st.caption(f"🔧 Debug: Đang chạy trên lõi {working_model}")
        else:
            st.error("Tài khoản API của bạn hiện không được cấp quyền dùng bất kỳ model nào.")
            st.stop()
            
    except KeyError:
        st.error("🚨 Chưa cấu hình GEMINI_API_KEY trong Secrets.")
        st.stop()
    except Exception as e:
        st.error(f"Lỗi khởi tạo API: {e}")
        st.stop()

    # 2. CÁC HÀM XỬ LÝ LÕI
    def extract_text_from_pdf(file):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        return text

    def get_ai_response(document_text, user_question):
        system_prompt = f"""
        Bạn là chuyên gia phân tích hợp đồng LawEase. Dưới đây là nội dung hợp đồng:
        <hop_dong>
        {document_text}
        </hop_dong>
        Quy tắc: Chỉ trả lời dựa vào nội dung. Nếu không có, đáp "Không có thông tin".
        Câu hỏi: {user_question}
        """
        response = model.generate_content(system_prompt)
        return response.text

    # 3. GIAO DIỆN CHATBOT
    uploaded_file = st.file_uploader("📂 Tải file PDF Hợp đồng", type=['pdf'])

    if "contract_text" not in st.session_state:
        st.session_state.contract_text = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if uploaded_file is not None:
        if st.session_state.contract_text == "":
            with st.spinner("Đang mã hóa tài liệu..."):
                st.session_state.contract_text = extract_text_from_pdf(uploaded_file)
            st.success("Tài liệu đã sẵn sàng!")
        
        st.divider()
        st.subheader("💬 Khung Chat Phân Tích")
        
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        if prompt := st.chat_input("Hỏi AI về hợp đồng này..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                with st.spinner("Đang phân tích..."):
                    try:
                        answer = get_ai_response(st.session_state.contract_text, prompt)
                        st.markdown(answer)
                        st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        st.error(f"Lỗi phản hồi từ Google: {e}")

# --- MODULE 4: QUẢN LÝ HỒ SƠ ---
elif menu == "📁 Quản Lý Hồ Sơ (CRM)":
    st.title("📁 Quản Lý Hồ Sơ Khách Hàng (CRM)")
    
    st.error("🚨 **CẢNH BÁO:** Hợp đồng thuê văn phòng trụ sở sẽ hết hạn vào 30/04/2026.")
    st.warning("⚠️ **LƯU Ý:** NDA với nhân sự 'Trần Thị C' chuẩn bị hết hạn.")

    data = {
        "Mã VB": ["HD-001", "HD-002", "DL-001"],
        "Tên văn bản": ["Hợp đồng Thử việc", "Hợp đồng thuê VP", "Điều lệ CTY"],
        "Ngày tạo": ["15/01/2026", "01/05/2025", "10/01/2026"],
        "Trạng thái": ["Đang hiệu lực", "🔴 Sắp hết hạn", "Đang hiệu lực"]
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
