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
        border-bottom: 1px solid #1e2
