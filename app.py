import streamlit as st
import google.generativeai as genai
import datetime
import random

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="玫瑰手札", page_icon="🌹", layout="centered")

# --- 2. 皇家風格 CSS (保留你喜歡的高級感) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;1,400&display=swap');

    /* 全局背景：深邃皇家藍 */
    .stApp {
        background-color: #0F172A;
        background-image: radial-gradient(circle at 50% 0%, #1E293B 0%, #0F172A 100%);
        color: #E2E8F0;
    }

    /* 輸入區塊：半透明玻璃感 */
    .block-container {
        background-color: rgba(15, 23, 42, 0.7);
        border: 1px solid #D4AF37;
        border-radius: 15px;
        padding: 2rem !important;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.1);
    }

    /* 標題 */
    h1 {
        font-family: 'Cinzel', serif !important;
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    /* 日期 */
    .date-display {
        text-align: center;
        font-family: 'Cinzel', serif;
        color: #94A3B8;
        font-size: 1rem;
        margin-bottom: 30px;
        border-bottom: 1px solid #334155;
        padding-bottom: 10px;
    }

    /* 輸入框美化 */
    .stTextInput label { color: #F1C40F !important; font-family: 'Cinzel', serif; }
    .stTextInput input {
        background-color: rgba(30, 41, 59, 0.9) !important;
        color: #F8FAFC !important;
        border: 1px solid #475569;
        border-left: 4px solid #D4AF37;
    }

    /* 按鈕 */
    div.stButton > button {
        background: linear-gradient(135deg, #B8860B 0%, #FFD700 100%);
        color: #000000 !important;
        font-family: 'Cinzel', serif !important;
        font-weight: bold;
        border: none;
        padding: 0.8rem;
        border-radius: 50px;
        width: 100%;
        margin-top: 20px;
        font-size: 1.2rem;
    }

    /* 結果卡片 (最重要的部分) */
    .journal-card {
        background-color: #1E293B;
        border: 2px solid #D4AF37;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
        position: relative;
    }
    .card-title {
        font-family: 'Cinzel', serif;
        color: #D4AF37;
        font-size: 1.5rem;
        margin-bottom: 20px;
    }
    .card-text {
        font-family: 'Playfair Display', serif;
        color: #E2E8F0;
        font-size: 1.1rem;
        line-height: 1.8;
        text-align: left;
        margin-bottom: 10px;
        border-bottom: 1px dashed #334155;
        padding-bottom: 10px;
    }
    .ai-summary {
        margin-top: 20px;
        font-style: italic;
        color: #94A3B8;
        font-size: 0.9rem;
        background: rgba(0,0,0,0.2);
        padding: 15px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 側邊欄 (簡化版) ---
with st.sidebar:
    st.header("🔑 鑰匙存放處")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("💡 只要輸入一次，瀏覽器通常會記住。若沒有 Key，程式會切換成「純紀錄模式」，依然可以使用！")

# --- 4. 主介面 ---
today = datetime.date.today().strftime("%Y 年 %m 月 %d 日")
st.title("THE ROSE JOURNAL")
st.markdown(f"<div class='date-display'>{today} ‧ Daily Gratitude</div>", unsafe_allow_html=True)

# 輸入表單
with st.form("journal_form"):
    st.markdown("### 🌹 今日的感恩 (Gratitude)")
    q1 = st.text_input("1. 我感恩...", placeholder="微小的幸福...")
    q2 = st.text_input("2. 我感恩...", placeholder="他人的善意...")
    
    st.markdown("### ✨ 明日的顯化 (Manifestation)")
    q3 = st.text_input("3. 我顯化...", placeholder="理想的狀態...")
    q4 = st.text_input("4. 我顯化...", placeholder="達成的目標...")
    
    submitted = st.form_submit_button("⚜️ 封存今日記憶")

# --- 5. 核心邏輯 (穩定優先) ---
if submitted:
    if not q1 and not q2 and not q3 and not q4:
        st.warning("親愛的，請至少寫下一件事，讓魔法生效。")
    else:
        # A. 準備資料
        content = f"1.{q1} 2.{q2} 3.{q3} 4.{q4}"
        summary_text = "（今日星象寧靜，用心感受當下即是美好。）" # 預設文字
        
        # B. 嘗試使用 AI (但如果失敗，絕不報錯)
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash') # 使用最新模型
                prompt = f"你是一位優雅的皇家圖書館長。請根據用戶的日記：'{content}'，寫一段約 50 字的溫暖短評，語氣優雅、鼓勵人心。不要用 Markdown，直接給文字。"
                response = model.generate_content(prompt)
                if response.text:
                    summary_text = response.text
            except:
                summary_text = "（魔法訊號雖有波動，但宇宙已接收到您的心意。願您的明日如玫瑰般綻放。）"
        
        # C. 顯示結果 (漂亮的卡片)
        st.success("記憶已封存！")
        
        st.markdown(f"""
        <div class="journal-card">
            <div class="card-title">⚜️ {today} ⚜️</div>
            <div class="card-text">🌹 {q1 if q1 else '...'}</div>
            <div class="card-text">🌹 {q2 if q2 else '...'}</div>
            <div class="card-text">✨ {q3 if q3 else '...'}</div>
            <div class="card-text">✨ {q4 if q4 else '...'}</div>
            <div class="ai-summary">
                ❝ {summary_text} ❞
            </div>
            <br>
            <div style="font-size:3rem;">🌹</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("💡 您可以截圖這張卡片，作為今日的紀念。")
