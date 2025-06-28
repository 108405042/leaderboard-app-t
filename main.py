import requests
import pandas as pd
import streamlit as st

# n8n webhook endpoint
url = "https://yulab.zeabur.app/webhook/0f675395-a33e-4a86-be50-ed66d838f1b4"

st.title("🏆 每週排行榜")

try:
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data)
    df = df[["Rank", "weeklyScore"]]

    # 確保欄位為數值型別
    df["Rank"] = pd.to_numeric(df["Rank"], errors="coerce")
    df["weeklyScore"] = pd.to_numeric(df["weeklyScore"], errors="coerce")

    df = df.dropna(subset=["Rank", "weeklyScore"])
    df = df.sort_values(by="Rank").reset_index(drop=True)

    for _, row in df.iterrows():
        rank = int(row['Rank'])
        score = int(round(row['weeklyScore']))
        if rank == 1:
            emoji = "🥇"
            color = "gold"
        elif rank == 2:
            emoji = "🥈"
            color = "silver"
        elif rank == 3:
            emoji = "🥉"
            color = "#cd7f32"
        else:
            emoji = "🎖️"
            color = "#1f77b4"

        st.markdown(f"""
        <div style='background-color: #f9f9f9; border-radius: 10px; padding: 12px 20px; margin: 10px 0; box-shadow: 1px 1px 3px rgba(0,0,0,0.1);'>
            <span style='font-size: 18px; color: black;'>{emoji} <strong>第 {rank} 名</strong></span>
            <span style='float: right; font-size: 18px; color: {color}; font-weight: bold;'>{score} 分</span>
        </div>
        """, unsafe_allow_html=True)

        if rank == 25:
            st.markdown("""
            <div style='font-size: 16px; color: #444; margin-top: 20px; margin-bottom: 10px; text-align: center;'>----- 🎁 前25名可獲得額外獎勵 -----</div>
            """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"資料讀取失敗：{e}")
