import streamlit as st
import google.generativeai as genai
import requests
import random

# --- 設定頁面配置 ---
st.set_page_config(page_title="玫瑰手札", page_icon="🌹", layout="centered")

# --- 高級皇家風格 CSS (Beauty and the Beast Royal Theme) ---
st.markdown("""
<style>
    /* 引入高級字體：Cinzel (標題) 和 Playfair Display (內文) */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;1,400&display=swap');

    /* 1. 全局背景：深邃皇家藍 (象徵野獸的西裝與夜空) */
    .stApp {
        background-color: #0F172A;
        background-image: radial-gradient(circle at 50% 10%, #1E293B 10%, #0F172A 90%);
        color: #E2E8F0;
    }

    /* 2. 主內容區塊：像是一張漂浮的魔法羊皮紙 */
    .block-container {
        background-color: rgba(15, 23, 42, 0.8); /* 半透明深底 */
        border: 2px solid #D4AF37; /* 金色邊框 */
        border-radius: 15px;
        padding: 3rem !important;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2); /* 金色微光 */
        margin-top: 2rem;
    }

    /* 3. 標題樣式 (電影海報感) */
    h1 {
        font-family: 'Cinzel', serif !important;
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 700;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 0.5rem;
    }
    
    /* 副標題 */
    .subtitle {
        font-family: 'Playfair Display', serif;
        color: #94A3B8;
        text-align: center;
        font-style: italic;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }

    /* 4. 輸入框樣式 */
    .stTextInput label {
        color: #D4AF37 !important; /* 金色標籤 */
        font-family: 'Cinzel', serif;
        font-size: 1rem;
    }
    .stTextInput input {
        background-color: rgba(30, 41, 59, 0.8) !important;
        color: #F8FAFC !important;
        border: 1px solid #475569;
        border-left: 3px solid #D4AF37; /* 左側金邊 */
        border-radius: 4px;
    }
    .stTextInput input:focus {
        border-color: #D4AF37;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
    }

    /* 5. 按鈕樣式 (貝兒的黃色禮服漸層) */
    div.stButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #F5C542 100%);
        color: #0F172A !important; /* 深藍色文字 */
        font-family: 'Cinzel', serif !important;
        font-weight: bold;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 50px; /* 圓潤感 */
        font-size: 1.2rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.6);
        background: linear-gradient(135deg, #F5C542 0%, #FFF8DC 100%);
    }

    /* 6. 總結框 (半透明玻璃質感) */
    .summary-box {
        background: rgba(255, 255, 255, 0.05);
        border-top: 1px solid #D4AF37;
        border-bottom: 1px solid #D4AF37;
        padding: 2rem;
        text-align: center;
        font-family: 'Playfair Display', serif;
        color: #E2E8F0;
        font-size: 1.1rem;
        line-height: 1.8;
        margin: 2rem 0;
        position: relative;
    }
    
    /* 圖片邊框 */
    .comic-img-container {
        border: 1px solid #D4AF37;
        padding: 5px;
        background: #0F172A;
    }

</style>
""", unsafe_allow_html=True)

# --- 側邊欄：設定你的樣子 ---
with st.sidebar:
    st.header("🏰 皇家更衣室")
    st.markdown("請輸入您的專屬鑰匙：")
    
    api_key = st.text_input("Gemini API Key", type="password")
    
    st.markdown("---")
    st.subheader("主角特徵")
    
    hair_color = st.text_input("髮色/髮型", "Green wavy hair (綠色波浪捲髮)")
    glasses = st.text_input("眼鏡/配件", "Round glasses (圓框眼鏡)")
    outfit = st.text_input("服裝風格", "Royal yellow ballgown (皇家黃色禮服)")
    vibe = st.selectbox("場景氛圍", ["Royal Castle (皇家城堡)", "Enchanted Library (魔法圖書館)", "Rose Garden (玫瑰花園)", "Ballroom (舞廳)"])

# --- 主畫面 ---
st.markdown("<h1>THE ROSE JOURNAL</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>— Be our guest, put your magic to the test —<br>書寫，是打破日常魔咒的最強魔法。</div>", unsafe_allow_html=True)

# 建立表單
with st.form("journal_form"):
    col1, col2 = st.columns(2)
    with col1:
        q1 = st.text_input("🌹 第一道魔法 (感恩)", placeholder="今晨的陽光...")
        q2 = st.text_input("☕ 第二道魔法 (感恩)", placeholder="好喝的咖啡...")
    with col2:
        q3 = st.text_input("✨ 星星的指引 (顯化)", placeholder="順利完成專案...")
        q4 = st.text_input("👑 皇冠的榮耀 (顯化)", placeholder="健康的身體...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    # 提交按鈕
    submitted = st.form_submit_button("⚜️ 封存記憶 ‧ 開啟篇章")

# --- 核心邏輯 ---
if submitted:
    if not api_key:
        st.error("⚠️ 請先在左側輸入您的鑰匙，城堡大門才能開啟。")
    elif not q1 and not q2 and not q3 and not q4:
        st.warning("魔法書需要文字才能啟動...")
    else:
        # 1. 設定 Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        # 2. 生成總結 (Text)
        with st.spinner("🕯️ 盧米亞正在點亮燭光... 茶壺太太正在倒茶..."):
            try:
                diary_content = f"1.{q1}, 2.{q2}, 3.{q3}, 4.{q4}"
                prompt_text = f"""
                你是一位優雅、充滿智慧的皇家圖書館長（類似美女與野獸的旁白風格）。
                用戶寫下了今天的感恩日記：{diary_content}。
                
                任務：
                1. 請用極度優雅、帶點古典文學氣息的繁體中文寫一段約 80 字的總結。語氣要像是在朗讀童話故事的結尾，稱呼用戶為「親愛的 SC」。
                2. 設計四個「四格漫畫的分鏡描述(英文)」。
                
                漫畫風格關鍵詞：Masterpiece, highly detailed, vintage Disney style, Beauty and the Beast 1991 aesthetic, cinematic lighting, deep blue and gold color palette.
                主角特徵：{hair_color}, {glasses}, {outfit}.
                
                請將現代事物轉化為古典宮廷元素（例如：辦公室->書房, 手機->魔鏡, 汽車->馬車）。
                
                回傳格式：
                總結：[內容]
                Panel 1: [英文描述]
                Panel 2: [英文描述]
                Panel 3: [英文描述]
                Panel 4: [英文描述]
                """
                
                response = model.generate_content(prompt_text)
                result_text = response.text
                
                # 解析
                summary = "魔法正在匯聚..."
                panels = []
                
                lines = result_text.split('\n')
                current_panel = ""
                for line in lines:
                    if "總結：" in line:
                        summary = line.replace("總結：", "").strip()
                    elif "Panel" in line and ":" in line:
                        if current_panel:
                            panels.append(current_panel)
                        current_panel = line.split(":", 1)[1].strip()
                    else:
                        current_panel += " " + line.strip()
                if current_panel:
                    panels.append(current_panel)
                
                while len(panels) < 4:
                    panels.append(f"A elegant lady in a castle, {hair_color}, {outfit}, cinematic lighting")

            except Exception as e:
                st.error(f"魔法訊號受到干擾：{str(e)}")
                summary = "雖然燭光暫時閃爍，但您的心意宇宙已經收到了。"
                panels = ["Red rose"] * 4

        # 3. 顯示總結
        st.markdown(f"<div class='summary-box'>❝ {summary} ❞</div>", unsafe_allow_html=True)
        
        # 4. 生成並顯示圖片
        st.markdown("<h3 style='text-align:center; color:#D4AF37; font-family:Cinzel;'>✧ 今日的永恆篇章 ✧</h3>", unsafe_allow_html=True)
        
        cols = st.columns(2)
        for i in range(4):
            with cols[i % 2]:
                with st.spinner(f"正在繪製第 {i+1} 幕..."):
                    seed = random.randint(1, 99999)
                    # 增強畫質與風格的 Prompt
                    image_prompt = f"Cinematic shot, vintage disney animation style, Beauty and the Beast aesthetic, {vibe}, royal atmosphere, deep blue and gold colors. {panels[i]}. Character: {hair_color}, {glasses}, {outfit}. Intricate details, masterpiece."
                    
                    encoded_prompt = requests.utils.quote(image_prompt)
                    # 使用 Flux 模型獲得更好的畫質
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=800&seed={seed}&nologo=true&model=flux"
                    
                    st.markdown(f"""
                    <div class="comic-img-container">
                        <img src="{image_url}" width="100%" style="border-radius:5px;">
                    </div>
                    <p style="text-align:center; color:#94A3B8; font-family:'Playfair Display'; margin-top:5px;">Chapter {i+1}</p>
                    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border-color:#1E293B;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#475569; font-size:0.8rem;'>Designed for SC ‧ The Rose Journal</div>", unsafe_allow_html=True)
