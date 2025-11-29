import streamlit as st
import google.generativeai as genai
import datetime

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="玫瑰手札", page_icon="🌹", layout="centered")

# --- 2. 極致奢華皇家風格 CSS ---
st.markdown("""
<style>
    /* 引入頂級襯線字體：Cormorant Garamond (內文) & Cinzel (標題) */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&display=swap');

    /* 全局重置與背景：深邃午夜藍 */
    .stApp {
        background-color: #020617; /* 極深的藍黑 */
        background-image: linear-gradient(180deg, #0f172a 0%, #020617 100%);
        color: #E2E8F0;
    }

    /* 隱藏 Streamlit 預設的多餘元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 主容器：極簡磨砂玻璃感 */
    .block-container {
        max-width: 700px;
        padding-top: 3rem !important;
        padding-bottom: 5rem !important;
    }

    /* 標題樣式 - 低調奢華 */
    h1 {
        font-family: 'Cinzel', serif !important;
        color: #94a3b8; /* 霧面銀灰 */
        text-align: center;
        font-weight: 400;
        letter-spacing: 4px;
        font-size: 1.8rem !important;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }
    
    .date-sub {
        font-family: 'Cormorant Garamond', serif;
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        font-style: italic;
        margin-bottom: 3rem;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 20px;
        width: 60%;
        margin-left: auto;
        margin-right: auto;
    }

    /* 輸入框美化 - 極簡線條 */
    .stTextInput {
        margin-bottom: 1.5rem;
    }
    
    .stTextInput label {
        color: #C5A059 !important; /* 古銅金 */
        font-family: 'Cinzel', serif;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }
    
    .stTextInput input {
        background-color: transparent !important;
        color: #F1F5F9 !important;
        border: none;
        border-bottom: 1px solid #334155; /* 只有底線 */
        border-radius: 0;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.2rem;
        padding-left: 0;
    }
    
    .stTextInput input:focus {
        border-bottom: 1px solid #C5A059; /* 聚焦時變金線 */
        box-shadow: none;
    }

    /* 按鈕 - 像是一個印章 */
    div.stButton > button {
        background-color: #C5A059; /* 古銅金實色 */
        color: #0f172a !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 600;
        letter-spacing: 2px;
        border: none;
        padding: 0.8rem 3rem;
        border-radius: 2px; /* 方正一點更有書卷氣 */
        margin-top: 2rem;
        display: block;
        margin-left: auto;
        margin-right: auto;
        transition: all 0.4s ease;
    }
    div.stButton > button:hover {
        background-color: #e2c585;
        letter-spacing: 4px; /* hover 時字距拉開 */
    }

    /* 結果卡片 - 像是一頁書 */
    .journal-result {
        background-color: #0f172a;
        border: 1px solid #334155;
        padding: 40px;
        margin-top: 40px;
        text-align: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    
    .result-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.3rem;
        color: #cbd5e1;
        line-height: 2;
        margin-bottom: 10px;
        text-align: left;
        border-bottom: 1px solid #1e293b;
        padding: 10px 0;
    }

    .ai-feedback {
        margin-top: 30px;
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
        color: #C5A059;
        font-size: 1.1rem;
        line-height: 1.6;
    }

</style>
""", unsafe_allow_html=True)

# --- 3. 側邊欄 (極簡化) ---
with st.sidebar:
    st.markdown("<div style='text-align:center; color:#C5A059; font-family:Cinzel; margin-bottom:20px;'>SETTINGS</div>", unsafe_allow_html=True)
    api_key = st.text_input("API Key", type="password", placeholder="Enter your key here")

# --- 4. 主介面邏輯 ---
today_date = datetime.date.today().strftime("%B %d, %Y") # 英文日期比較高級

st.markdown("<h1>The Rose Journal</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='date-sub'>{today_date} &nbsp;•&nbsp; Daily Chronicles</div>", unsafe_allow_html=True)

# 表單
with st.form("daily_entry"):
    # 這裡改成四個通用的輸入，不再區分感恩或顯化
    c1 = st.text_input("CHAPTER I", placeholder="Write your first thought...")
    c2 = st.text_input("CHAPTER II", placeholder="Write your second thought...")
    c3 = st.text_input("CHAPTER III", placeholder="Write your third thought...")
    c4 = st.text_input("CHAPTER IV", placeholder="Write your fourth thought...")
    
    submit = st.form_submit_button("SEAL THE ENTRY") # 封存

# --- 5. 處理結果 ---
if submit:
    if not c1 and not c2 and not c3 and not c4:
        st.caption("Please write at least one chapter to seal the memory.")
    else:
        # A. 顯示結果 (這就是你要的漂亮日記頁面)
        st.markdown(f"""
        <div class='journal-result'>
            <div style='color:#C5A059; font-family:Cinzel; font-size:1.5rem; margin-bottom:30px;'>— {today_date} —</div>
            <div class='result-text'>I. {c1 if c1 else '...'}</div>
            <div class='result-text'>II. {c2 if c2 else '...'}</div>
            <div class='result-text'>III. {c3 if c3 else '...'}</div>
            <div class='result-text'>IV. {c4 if c4 else '...'}</div>
        """, unsafe_allow_html=True)

        # B. AI 總結 (靜默模式，有 Key 就跑，沒 Key 也不報錯)
        ai_message = ""
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                # 提示詞改成通用，不強調節日或感恩
                content = f"{c1}, {c2}, {c3}, {c4}"
                prompt = f"你是一位優雅的皇家圖書館長。用戶寫下了今天的四件事：'{content}'。請用極度優雅、充滿智慧的語氣（繁體中文），寫一段約 40 字的短評，為這一天畫下句點。"
                response = model.generate_content(prompt)
                ai_message = response.text
            except:
                pass # 失敗了就什麼都不做，保持安靜
        
        # 如果有 AI 回應就顯示，沒有就顯示一句預設的 elegant quote
        final_msg = ai_message if ai_message else "The magic is in the moment."
        
        st.markdown(f"""
            <div class='ai-feedback'>
                ❝ {final_msg} ❞
            </div>
        </div>
        """, unsafe_allow_html=True)
