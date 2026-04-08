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

# Ẩn menu mặc định của Streamlit cho chuyên nghiệp
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ==========================================
# 2. HỆ THỐNG ĐIỀU HƯỚNG (SIDEBAR MENU)
# ==========================================
st.sidebar.title("⚖️ LawEase Menu")
menu = st.sidebar.radio(
    "Chọn tính năng:",
    ["🏠 Trang Chủ", "📝 Tạo Hợp Đồng (Logic Tree)", "🤖 Trợ Lý AI Đọc PDF", "📁 Quản Lý Hồ Sơ (CRM)"]
)

st.sidebar.divider()
st.sidebar.info("Bản Demo MVP phục vụ thuyết trình cuộc thi Khởi nghiệp & KHKT.")

# ==========================================
# 3. CÁC MODULE CHỨC NĂNG CHÍNH
# ==========================================

# --- MODULE 1: TRANG CHỦ ---
if menu == "🏠 Trang Chủ":
    st.title("⚖️ LawEase - Pháp lý tinh gọn cho Startup")
    st.markdown("### Giải pháp Tự động hóa Văn bản Pháp lý & Trợ lý Ảo thế hệ mới")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Văn bản đã tự động hóa", value="50+ Mẫu", delta="Cập nhật liên tục")
    with col2:
        st.metric(label="Thời gian tạo hợp đồng", value="2 Phút", delta="-98% thời gian", delta_color="inverse")
    with col3:
        st.metric(label="Độ chuẩn xác pháp lý", value="100%", delta="Bảo chứng bởi ULAW")

    st.divider()
    st.info("👈 Vui lòng sử dụng thanh Menu bên trái để trải nghiệm các phân hệ của bản Demo MVP.")
    st.markdown("""
    **Bản Demo này trình diễn 3 công nghệ lõi:**
    1. **Tạo Hợp Đồng:** Thuật toán rẽ nhánh If/Else chuẩn xác 100%, kháng ảo giác AI.
    2. **Trợ Lý AI (RAG):** Trí tuệ nhân tạo đọc hiểu và phân tích văn bản PDF cục bộ.
    3. **Quản Lý Hồ Sơ:** Hệ thống cảnh báo thời hạn tự động giúp giữ chân khách hàng.
    """)

# --- MODULE 2: TẠO HỢP ĐỒNG (Lõi Logic Tree) ---
elif menu == "📝 Tạo Hợp Đồng (Logic Tree)":
    st.title("📝 Trình Tạo Hợp Đồng Tự Động")
    st.write("Hệ thống rẽ nhánh điều khoản đảm bảo tính chính xác tuyệt đối mà không phụ thuộc vào AI tạo sinh.")

    with st.container(border=True):
        loai_hd = st.selectbox("1. Chọn loại văn bản cần tạo:", ["Hợp đồng Thử việc", "Thỏa thuận bảo mật (NDA)"])
        
        st.write("2. Thông tin các bên:")
        col1, col2 = st.columns(2)
        with col1:
            ten_cong_ty = st.text_input("Tên Doanh nghiệp (Bên A):", "Công ty Cổ phần công nghệ LawEase")
            nguoi_dai_dien = st.text_input("Người đại diện pháp luật:", "Ông Nguyễn Văn Founder")
        with col2:
            ten_nhan_vien = st.text_input("Tên Người/Đối tác (Bên B):", "Trần Thị C")
            cccd = st.text_input("Số CCCD/CMND:", "079123456789")

        st.write("3. Thỏa thuận cốt lõi:")
        if loai_hd == "Hợp đồng Thử việc":
            luong = st.number_input("Mức lương thỏa thuận (VNĐ):", min_value=0, step=500000, value=8000000)
            co_dong_bhxh = st.checkbox("Doanh nghiệp hỗ trợ đóng BHXH trong thời gian thử việc?")
        else:
            muc_phat = st.number_input("Mức phạt vi phạm (VNĐ):", min_value=10000000, step=10000000, value=50000000)
            thoi_han = st.slider("Thời hạn bảo mật (Năm) kể từ ngày nghỉ việc:", 1, 5, 2)

    if st.button("🚀 Khởi chạy Thuật toán & Tạo Văn bản", type="primary"):
        st.success("Hệ thống đã xử lý xong cây logic. Dưới đây là văn bản của bạn:")
        
        ngay_hien_tai = datetime.date.today().strftime("%d/%m/%Y")
        
        # Cây logic
        if loai_hd == "Hợp đồng Thử việc":
            dieu_khoan_bhxh = "Bên A đồng ý đóng đầy đủ các khoản Bảo hiểm xã hội, Bảo hiểm y tế cho Bên B ngay trong thời gian thử việc theo quy định." if co_dong_bhxh else "Do đang trong thời gian thử việc, Bên B sẽ tự túc các khoản bảo hiểm bắt buộc theo thỏa thuận."
            hop_dong_mau = f"""CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
-----------------------------

HỢP ĐỒNG THỬ VIỆC
(Số: 01/2026/HĐTV)

Hôm nay, ngày {ngay_hien_tai}, chúng tôi gồm:
BÊN A: {ten_cong_ty.upper()} (Đại diện: {nguoi_dai_dien})
BÊN B: {ten_nhan_vien.upper()} (Số CCCD: {cccd})

Hai bên thỏa thuận ký kết hợp đồng thử việc với các điều khoản sau:
Điều 1: Mức lương thỏa thuận trong thời gian thử việc là {luong:,.0f} VNĐ/tháng.
Điều 2: Chế độ phúc lợi và bảo hiểm: {dieu_khoan_bhxh}
Điều 3: Hợp đồng có hiệu lực kể từ ngày ký."""
        else:
            hop_dong_mau = f"""CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
-----------------------------

THỎA THUẬN BẢO MẬT THÔNG TIN (NDA)

Hôm nay, ngày {ngay_hien_tai}, giữa:
BÊN TIẾT LỘ: {ten_cong_ty.upper()} (Đại diện: {nguoi_dai_dien})
BÊN NHẬN: {ten_nhan_vien.upper()} (CCCD: {cccd})

Điều 1: Bên nhận cam kết không sao chép, chia sẻ bí mật kinh doanh của Bên tiết lộ cho bên thứ ba.
Điều 2: Thời hạn bảo mật kéo dài {thoi_han} năm kể từ ngày chấm dứt hợp tác.
Điều 3: Chế tài vi phạm: Bồi thường ngay {muc_phat:,.0f} VNĐ nếu vi phạm thỏa thuận."""

        st.text_area("Bản xem trước Hợp đồng:", hop_dong_mau, height=350)
        st.download_button("⬇️ Tải file Hợp đồng (.txt)", data=hop_dong_mau, file_name=f"LawEase_{loai_hd.replace(' ', '_')}.txt")

# --- MODULE 3: TRỢ LÝ AI (Đọc hiểu PDF) ---
elif menu == "🤖 Trợ Lý AI Đọc PDF":
    st.title("🤖 Trợ Lý Phân Tích Hợp Đồng (AI Q&A)")
    st.write("Tải hợp đồng của bạn lên, AI sẽ phân tích và trích xuất thông tin chuẩn xác.")

    # 1. KIỂM TRA BẢO MẬT API KEY
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')
    except KeyError:
        st.error("🚨 Lỗi Bảo Mật: Chưa tìm thấy API Key. Vui lòng vào Streamlit Cloud -> Settings -> Secrets và cấu hình GEMINI_API_KEY.")
        st.stop() # Dừng chạy code bên dưới nếu không có key

    # 2. CÁC HÀM XỬ LÝ LÕI
    def extract_text_from_pdf(file):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        return text

    def get_ai_response(document_text, user_question):
        system_prompt = f"""
        Bạn là một trợ lý pháp lý ảo của nền tảng LawEase, chuyên gia phân tích hợp đồng.
        Dưới đây là nội dung hợp đồng:
        <hop_dong>
        {document_text}
        </hop_dong>
        
        Quy tắc TỐI THƯỢNG:
        1. Chỉ trả lời dựa vào nội dung hợp đồng.
        2. Nếu không có thông tin, PHẢI trả lời: "Xin lỗi, thông tin này không có trong tài liệu."
        3. KHÔNG tự bịa đặt điều khoản.
        
        Câu hỏi: {user_question}
        """
        response = model.generate_content(system_prompt)
        return response.text

    # 3. GIAO DIỆN CHATBOT
    uploaded_file = st.file_uploader("📂 Tải file Hợp đồng lên đây (Định dạng PDF)", type=['pdf'])

    if "contract_text" not in st.session_state:
        st.session_state.contract_text = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if uploaded_file is not None:
        if st.session_state.contract_text == "": # Tránh việc load lại file nhiều lần
            with st.spinner("Đang quét và số hóa tài liệu..."):
                st.session_state.contract_text = extract_text_from_pdf(uploaded_file)
            st.success("Tài liệu đã được mã hóa thành công! Bạn có thể bắt đầu đặt câu hỏi.")
        
        st.divider()
        st.subheader("💬 Khung Chat Phân Tích")
        
        # In lại lịch sử chat
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        # Khung nhập liệu
        if prompt := st.chat_input("Ví dụ: Ngày ký hợp đồng là ngày nào? Ai là đại diện công ty?"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                with st.spinner("AI đang truy xuất dữ liệu..."):
                    try:
                        answer = get_ai_response(st.session_state.contract_text, prompt)
                        st.markdown(answer)
                        st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        st.error(f"Lỗi kết nối API máy chủ Google: {e}")

# --- MODULE 4: QUẢN LÝ HỒ SƠ ---
elif menu == "📁 Quản Lý Hồ Sơ (CRM)":
    st.title("📁 Quản Lý Hồ Sơ Khách Hàng (CRM)")
    st.write("Nơi lưu trữ và cảnh báo rủi ro pháp lý tự động.")

    st.error("🚨 **CẢNH BÁO TỰ ĐỘNG:** Hợp đồng thuê văn phòng trụ sở sẽ hết hạn vào 30/04/2026.")
    st.warning("⚠️ **LƯU Ý:** Thỏa thuận NDA với nhân sự 'Trần Thị C' chuẩn bị hết hạn tuần tới.")

    st.subheader("📚 Kho Lưu Trữ Tài Liệu")
    data = {
        "Mã VB": ["HD-001", "HD-002", "DL-001", "NDA-005"],
        "Tên văn bản": ["Hợp đồng Thử việc", "Hợp đồng thuê VP", "Điều lệ CTY", "NDA - Trần Thị C"],
        "Ngày tạo": ["15/01/2026", "01/05/2025", "10/01/2026", "20/04/2025"],
        "Trạng thái": ["Đang hiệu lực", "🔴 Sắp hết hạn", "Đang hiệu lực", "🟡 Sắp hết hạn"]
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("Tải hồ sơ (.ZIP)", type="primary")
    with col2:
        st.button("Đồng bộ Google Drive")
