import streamlit as st
import pandas as pd
import datetime
import time

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
    ["🏠 Trang Chủ", "📝 Tạo Hợp Đồng (Logic Tree)", "🤖 Trợ Lý AI (Chatbot)", "📁 Quản Lý Hồ Sơ (CRM)"]
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
    1. **Tạo Hợp Đồng:** Thuật toán rẽ nhánh If/Else chuẩn xác 100%, không lo AI ảo giác.
    2. **Trợ Lý AI:** Phễu tư vấn luật cơ bản mô phỏng ChatGPT.
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

# --- MODULE 3: TRỢ LÝ AI (Chatbot) ---
elif menu == "🤖 Trợ Lý AI (Chatbot)":
    st.title("🤖 Trợ Lý Pháp Lý AI")
    st.caption("Giao diện Demo mô phỏng tích hợp LLM (Đã cài sẵn kịch bản trả lời nhanh).")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Xin chào! Tôi có thể giúp gì cho bạn về thủ tục (Thành lập công ty, NDA, Thuế...)?"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Nhập câu hỏi tại đây..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            prompt_lower = prompt.lower()
            if "thành lập" in prompt_lower:
                reply = "Thành lập công ty cần:\n1. Điều lệ công ty.\n2. Giấy đề nghị đăng ký doanh nghiệp.\n3. Danh sách thành viên.\n👉 **Chuyển sang mục 'Tạo Hợp Đồng' bên trái để tự động soạn Điều lệ nhé!**"
            elif "nda" in prompt_lower or "bảo mật" in prompt_lower:
                reply = "Thỏa thuận bảo mật (NDA) cần quy định rõ phạm vi, thời hạn và mức phạt. 👉 Hệ thống LawEase có sẵn biểu mẫu NDA, bạn hãy dùng thử ở Menu bên trái!"
            else:
                reply = "Tính năng giải đáp chuyên sâu đang được nhóm hoàn thiện bằng API của Google. Mời bạn trải nghiệm tính năng 'Tạo Hợp Đồng' nhé!"

            # Giả lập AI gõ chữ
            for chunk in reply.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

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
