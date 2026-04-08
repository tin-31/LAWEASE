import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

# ==========================================
# CẤU HÌNH API (BẮT BUỘC)
# ==========================================
# Bạn cần vào trang Google AI Studio để lấy API Key miễn phí và điền vào đây
API_KEY = "AIzaSyAjh3mkKysCqriWu2kzml1Q-LnNjcMk3ok" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro') # Sử dụng model tối ưu cho tốc độ và văn bản dài

st.set_page_config(page_title="Trợ Lý AI Phân Tích Hợp Đồng", page_icon="🤖")
st.title("🤖 Trợ Lý Phân Tích Hợp Đồng (AI Document Q&A)")
st.write("Tải hợp đồng của bạn lên, AI sẽ phân tích và trích xuất thông tin chuẩn xác.")

# ==========================================
# HÀM XỬ LÝ LÕI
# ==========================================
def extract_text_from_pdf(file):
    """Hàm trích xuất text từ file PDF tải lên"""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

def get_ai_response(document_text, user_question):
    """Hàm giao tiếp với LLM tích hợp cơ chế Kháng ảo giác (Anti-Hallucination)"""
    # Prompt System ép buộc AI chỉ được trả lời dựa trên tài liệu
    system_prompt = f"""
    Bạn là một trợ lý pháp lý ảo của nền tảng LawEase, chuyên gia phân tích hợp đồng.
    Dưới đây là toàn bộ nội dung của một hợp đồng pháp lý:
    <hop_dong>
    {document_text}
    </hop_dong>
    
    Nhiệm vụ của bạn là trả lời câu hỏi của người dùng CHỈ DỰA VÀO nội dung hợp đồng trên.
    Quy tắc TỐI THƯỢNG:
    1. Nếu thông tin có trong hợp đồng, hãy trích xuất chính xác.
    2. Nếu thông tin KHÔNG CÓ trong hợp đồng, bạn PHẢI trả lời: "Xin lỗi, thông tin này không được đề cập trong hợp đồng bạn cung cấp."
    3. Tuyệt đối KHÔNG tự sáng tạo, suy diễn hay thêm thắt các điều khoản bên ngoài vào.
    
    Câu hỏi của người dùng: {user_question}
    """
    response = model.generate_content(system_prompt)
    return response.text

# ==========================================
# GIAO DIỆN NGƯỜI DÙNG (UI)
# ==========================================
# Khu vực tải file
uploaded_file = st.file_uploader("📂 Tải file Hợp đồng lên đây (Định dạng PDF)", type=['pdf'])

# Biến trạng thái lưu trữ nội dung hợp đồng và lịch sử chat
if "contract_text" not in st.session_state:
    st.session_state.contract_text = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Xử lý khi có file được tải lên
if uploaded_file is not None:
    with st.spinner("Đang quét và số hóa tài liệu..."):
        st.session_state.contract_text = extract_text_from_pdf(uploaded_file)
    st.success("Tài liệu đã được mã hóa thành công! Bạn có thể bắt đầu đặt câu hỏi.")
    
    # Khu vực hiển thị chat
    st.divider()
    st.subheader("💬 Khung Chat Phân Tích")
    
    # Hiển thị lịch sử
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Xử lý câu hỏi mới
    if prompt := st.chat_input("Ví dụ: Ngày ký hợp đồng là ngày nào? Ai là người đại diện công ty?"):
        # Lưu câu hỏi của user
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Gọi AI xử lý
        with st.chat_message("assistant"):
            with st.spinner("AI đang truy xuất dữ liệu..."):
                try:
                    answer = get_ai_response(st.session_state.contract_text, prompt)
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Lỗi kết nối API: {e}. Vui lòng kiểm tra lại API Key.")
