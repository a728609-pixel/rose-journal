import streamlit as st
import google.generativeai as genai
import requests
import random

# --- 設定頁面配置 ---
st.set_page_config(page_title="玫瑰手札", page_icon="🌹", layout="centered")

# --- 高級皇家風格 CSS (深藍與流動金) ---
st.markdown("""
<style>
    /* 引入高級字體 */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;1,400&display=swap');

    /* 1. 全局背景：深邃皇家藍 (象徵野獸的西裝與夜空) */
    .stApp {
        background-color: #0F172A;
        background-image: radial-gradient(circle at 50% 0%, #1E293B 0%, #0F172A 100%);
        color: #E2E8F0;
    }

    /* 2. 主內容區塊：半透明深色玻璃質感 */
    .block-container {
        background-color: rgba(15, 23, 42, 0.6);
        border: 1px solid #D4AF37; /* 金色邊框 */
        border-radius: 15px;
        padding: 2rem !important;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.15);
        margin-top: 1rem;
    }

    /* 3. 標題樣式 */
    h1 {
        font-family: 'Cinzel', serif !important;
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }

    /* 4. 輸入框樣式 - 深色高級感 */
    .stTextInput label {
        color: #F1C40F !important; /* 金黃色文字 */
        font-family: 'Cinzel', serif;
        font-size: 1rem;
    }
    .stTextInput input {
        background-color: rgba(30, 41, 59, 0.9) !important;
        color: #F8FAFC !important;
        border: 1px solid #475569;
        border-left: 4px solid #D4AF37; /* 左側金條 */
    }
    
    /* 5. 按鈕樣式 - 貝兒禮服漸層金 */
    div.stButton > button {
        background: linear-gradient(135deg, #B8860B 0%, #FFD700 100%);
        color: #000000 !important;
        font-family: 'Cinzel', serif !important;
        font-weight: bold;
        border: none;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
        width: 100%;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
    }
    
    /* 總結框 */
    .summary-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 20px;
        border-radius: 10px;
        color: #E2E8F0;
        font-family: 'Playfair Display', serif;
        text-align: center;
        font-style: italic;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# --- 側邊欄 ---
with st.sidebar:
    st.header("🏰 皇家更衣室")
    api_key = st.text_input("Gemini API Key", type="password")
    
    st.divider()
    st.subheader("主角設定")
    hair_color = st.text_input("髮色", "Green wavy hair (綠色波浪捲髮)")
    glasses = st.text_input("配件", "Round glasses (圓框眼鏡)")
    outfit = st.text_input("服裝", "Royal yellow ballgown (皇家黃色禮服)")
    vibe = st.selectbox("場景", ["Royal Castle (皇家城堡)", "Magic Library (魔法圖書館)", "Enchanted Forest (魔法森林)"])

# --- 主標題 ---
st.title("THE ROSE JOURNAL")
st.markdown("<div style='text-align:center; color:#94A3B8; font-family:Playfair Display; margin-bottom:20px;'>— Be our guest, put your magic to the test —</div>", unsafe_allow_html=True)

# --- 輸入表單 ---
with st.form("journal_form"):
    col1, col2 = st.columns(2)
    with col1:
        q1 = st.text_input("🌹 感恩之一", placeholder="今晨的陽光...")
        q2 = st.text_input("☕ 感恩之二", placeholder="好喝的咖啡...")
    with col2:
        q3 = st.text_input("✨ 顯化願望", placeholder="順利完成專案...")
        q4 = st.text_input("👑 自我期許", placeholder="健康的身體...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("⚜️ 封存記憶 ‧ 開啟篇章")

# --- 核心邏輯 (已修復 404 錯誤) ---
if submitted:
    if not api_key:
        st.error("⚠️ 請在左側輸入您的鑰匙，城堡大門才能開啟。")
    elif not q1 and not q2 and not q3 and not q4:
        st.warning("請寫下您的魔法咒語（輸入內容）...")
    else:
        # 1. 設定 Gemini (使用最新的 flash 模型，解決 404 問題)
        genai.configure(api_key=api_key)
        # *** 這裡修正了模型名稱 ***
        model = genai.GenerativeModel('gemini-1.5-flash')

        # 2. 生成總結
        with st.spinner("🕯️ 盧米亞正在點亮燭光..."):
            try:
                diary_content = f"1.{q1}, 2.{q2}, 3.{q3}, 4.{q4}"
                prompt_text = f"""
                你是一位優雅的皇家圖書館長。用戶寫下了感恩日記：{diary_content}。
                任務：
                1. 用極度優雅、古典文學氣息的繁體中文寫一段約 80 字總結，稱呼用戶為「親愛的 SC」。
                2. 設計四個「四格漫畫分鏡描述(英文)」。
                
                風格：Vintage Disney Beauty and the Beast 1991 style, cinematic lighting, deep blue and gold.
                主角：{hair_color}, {glasses}, {outfit}.
                轉化：將現代事物轉化為古典宮廷元素 (例如: 電腦->魔法書)。
                
                格式：
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
                    panels.append(f"A lady in castle, {hair_color}, {outfit}")

            except Exception as e:
                st.error(f"魔法訊號干擾：{str(e)}")
                summary = "請檢查 API Key 是否正確，或稍後再試。"
                panels = ["Rose"] * 4

        # 3. 顯示結果
        st.markdown(f"<div class='summary-card'>❝ {summary} ❞</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 4. 生成圖片 (Flux 模型)
        cols = st.columns(2)
        for i in range(4):
            with cols[i % 2]:
                with st.spinner(f"繪製第 {i+1} 幕..."):
                    seed = random.randint(1, 99999)
                    image_prompt = f"Masterpiece, cinematic shot, vintage disney animation style, Beauty and the Beast aesthetic, {vibe}, royal atmosphere, deep blue and gold colors. {panels[i]}. Character: {hair_color}, {glasses}, {outfit}."
                    
                    encoded_prompt = requests.utils.quote(image_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=800&seed={seed}&nologo=true&model=flux"
                    
                    st.image(image_url, use_container_width=True)
                    st.markdown(f"<div style='text-align:center; color:#94A3B8; font-family:Playfair Display; font-size:0.8rem;'>Chapter {i+1}</div>", unsafe_allow_html=True)

st.markdown("<br><div style='text-align:center; color:#475569; font-size:0.8rem;'>Designed for SC</div>", unsafe_allow_html=True)
