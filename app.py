import streamlit as st
import google.generativeai as genai
import requests
import random

# --- 設定頁面配置 ---
st.set_page_config(page_title="玫瑰手札", page_icon="🌹", layout="centered")

# --- 自定義 CSS (打造美女與野獸風格) ---
st.markdown("""
<style>
    /* 全局背景色 - 羊皮紙感 */
    .stApp {
        background-color: #FDF5E6;
        background-image: linear-gradient(to bottom, #FDF5E6, #F0E6D2);
    }
    
    /* 標題字體 */
    h1 {
        font-family: 'Times New Roman', Times, serif;
        color: #8B0000; /* 深紅色 */
        text-shadow: 2px 2px 4px #D4AF37; /* 金色陰影 */
        text-align: center;
        font-weight: bold;
    }

    h2, h3, p, div, label, span {
        font-family: 'Times New Roman', serif;
        color: #4A4A4A;
    }
    
    /* 輸入框樣式 */
    .stTextInput>div>div>input {
        background-color: #FFF8DC;
        border: 2px solid #D4AF37; /* 金邊 */
        color: #4B0082;
        border-radius: 5px;
    }
    
    /* 按鈕樣式 - 模仿封蠟章 */
    div.stButton > button {
        background-color: #8B0000;
        color: white !important;
        border-radius: 20px;
        border: 2px solid #D4AF37;
        font-size: 18px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
        width: 100%;
        margin-top: 20px;
    }
    div.stButton > button:hover {
        background-color: #A52A2A;
        border-color: #FFD700;
        color: #FFD700 !important;
    }

    /* 漫畫圖片樣式 */
    .comic-img {
        border: 4px double #D4AF37;
        border-radius: 10px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.2);
        margin-bottom: 10px;
    }
    
    /* 總結框樣式 */
    .summary-box {
        background-color: rgba(255, 255, 255, 0.7);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #D4AF37;
        text-align: center;
        font-style: italic;
        margin-top: 20px;
        color: #5c4033;
    }
</style>
""", unsafe_allow_html=True)

# --- 側邊欄：設定你的樣子 ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/rose.png", width=50)
    st.header("🏰 魔鏡設定")
    st.markdown("請輸入剛才拿到的鑰匙：")
    
    # 這裡讓用戶輸入 API Key
    api_key = st.text_input("Gemini API Key", type="password")
    
    st.markdown("---")
    st.subheader("主角特徵")
    st.markdown("告訴魔鏡你長什麼樣子，漫畫主角就會是你！")
    
    hair_color = st.text_input("髮色/髮型", "Green wavy hair (綠色波浪捲髮)")
    glasses = st.text_input("眼鏡/配件", "Round glasses (圓框眼鏡)")
    outfit = st.text_input("服裝風格", "Yellow vintage dress (黃色復古洋裝)")
    vibe = st.selectbox("整體氛圍", ["Warm (溫暖)", "Magical (魔法)", "Cozy (舒適)", "Royal (皇家)"])

# --- 主畫面 ---
st.title("🌹 玫瑰手札")
st.markdown("<p style='text-align: center;'>親愛的，書寫是打破日常魔咒的魔法。</p>", unsafe_allow_html=True)

# 建立表單
with st.form("journal_form"):
    col1, col2 = st.columns(2)
    with col1:
        q1 = st.text_input("✨ 感恩日記 1", placeholder="今晨的陽光...")
        q2 = st.text_input("✨ 感恩日記 2", placeholder="好喝的咖啡...")
    with col2:
        q3 = st.text_input("🌟 顯化目標 1", placeholder="順利完成專案...")
        q4 = st.text_input("🌟 顯化目標 2", placeholder="健康的身體...")
    
    # 提交按鈕
    submitted = st.form_submit_button("📜 封存並生成魔法篇章")

# --- 核心邏輯 ---
if submitted:
    if not api_key:
        st.error("⚠️ 請先在左側側邊欄輸入你的 Gemini API Key 喔！(點擊左上角箭頭展開)")
    elif not q1 and not q2 and not q3 and not q4:
        st.warning("請至少寫下一句感恩的話語...")
    else:
        # 1. 設定 Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        # 2. 生成總結 (Text)
        with st.spinner("☕ 茶壺太太正在為故事倒茶... (正在編織文字)"):
            try:
                diary_content = f"1.{q1}, 2.{q2}, 3.{q3}, 4.{q4}"
                prompt_text = f"""
                你是一位溫柔的童話神仙教母。用戶寫下了今天的感恩日記：{diary_content}。
                任務：
                1. 請用「美女與野獸」的優雅語氣，寫一段約 80 字的繁體中文溫暖總結，鼓勵用戶。
                2. 根據這四件事，設計四個「四格漫畫的分鏡描述(英文)」。
                
                漫畫風格關鍵詞：Vintage Disney fairytale style, Beauty and the Beast 1991 aesthetic, watercolor and ink.
                主角特徵：{hair_color}, {glasses}, {outfit}.
                
                重要：請將現代事物轉化為童話元素（例如：電腦->魔法書, 咖啡->魔法藥水, 手機->魔鏡）。
                
                請嚴格依照以下格式回傳（不要有多餘的引言）：
                總結：[你的總結內容]
                Panel 1: [第一格的詳細英文描述]
                Panel 2: [第二格的詳細英文描述]
                Panel 3: [第三格的詳細英文描述]
                Panel 4: [第四格的詳細英文描述]
                """
                
                response = model.generate_content(prompt_text)
                result_text = response.text
                
                # 解析回傳結果
                summary = "魔法正在匯聚..."
                panels = []
                
                # 簡單的解析邏輯
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
                
                # 確保有四個面板，不夠就補預設
                while len(panels) < 4:
                    panels.append(f"A happy girl writing diary in a castle, {hair_color}, {outfit}, vintage style")

            except Exception as e:
                st.error(f"魔法訊號中斷：{str(e)}")
                summary = "雖然魔法暫時失效，但你的心意宇宙已經收到了。"
                panels = ["A beautiful rose"] * 4

        # 3. 顯示總結
        st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        # 4. 生成並顯示圖片
        st.subheader("🖼️ 今日的魔法記憶")
        
        # 使用 Pollinations.ai 生成圖片 (免費、無限量)
        cols = st.columns(2)
        for i in range(4):
            with cols[i % 2]:
                with st.spinner(f"正在繪製第 {i+1} 格..."):
                    # 組合 Prompt
                    seed = random.randint(1, 99999)
                    image_prompt = f"Vintage storybook illustration, Beauty and the Beast style, watercolor, warm lighting, {vibe} atmosphere. {panels[i]}. Character details: {hair_color}, {glasses}, {outfit}."
                    
                    # 處理網址
                    encoded_prompt = requests.utils.quote(image_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=800&seed={seed}&nologo=true&model=flux"
                    
                    # 顯示
                    st.image(image_url, use_container_width=True)
                    st.caption(f"Chapter {i+1}")

st.markdown("---")
st.caption("Made with 🌹 for SC")
