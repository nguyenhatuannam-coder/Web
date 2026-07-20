import streamlit as st
import google.generativeai as genai
import sqlite3
import asyncio
import aiohttp

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()

genai.configure(api_key="AIzaSyB2IFXHn2XuiliAxL_BWbRuRTrxs0oRNDY")
model = genai.GenerativeModel("gemini-2.5-flash")

def register(username, password):
    try:
        c.execute(
            "INSERT INTO users(username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True
    except:
        return False

def login(username, password):
    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    return c.fetchone() is not None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 Đăng nhập hệ thống")

    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])

    with tab1:
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")

        if st.button("Đăng nhập"):
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Sai tài khoản hoặc mật khẩu!")

    with tab2:
        new_user = st.text_input("Tên tài khoản mới")
        new_pass = st.text_input(
            "Mật khẩu mới",
            type="password"
        )

        if st.button("Đăng ký"):
            if register(new_user, new_pass):
                st.success("✅ Đăng ký thành công!")
            else:
                st.error("❌ Tên tài khoản đã tồn tại!")

else:

    st.title("🌍 Tra Cứu Thủ Đô Các Quốc Gia")

    st.write(
        f"Xin chào **{st.session_state.username}** 👋"
    )

    if st.button("Đăng xuất"):
        st.session_state.logged_in = False
        st.rerun()

    country = st.text_input("Nhập tên quốc gia:")

    if st.button("Tìm kiếm"):

        if country.strip() == "":
            st.warning("⚠️ Vui lòng nhập tên quốc gia!")

        else:

            try:

                response = model.generate_content(
                    f"""
                    Thủ đô của quốc gia {country} là gì?

                    Chỉ trả lời tên thủ đô.
                    """
                )

                st.subheader("Kết quả:")
                st.success(response.text)

            except Exception as e:

                error_msg = str(e)

                if "429" in error_msg or "quota" in error_msg.lower():
                    st.error(
                        "⚠️ Đã hết lượt sử dụng Gemini API hoặc gửi quá nhiều yêu cầu. "
                        "Vui lòng đợi khoảng 1 phút rồi thử lại."
                    )

                elif "API_KEY_INVALID" in error_msg:
                    st.error(
                        "🔑 API Key không hợp lệ. Hãy tạo API Key mới."
                    )

                else:
                    st.error(
                        f"❌ Có lỗi xảy ra:\n\n{error_msg}"
                    )
URL = "https://example.com/api"

async def bot(session, bot_id):
    for i in range(5):
        try:
            async with session.get(URL) as resp:
                print(f"Bot {bot_id} -> {resp.status}")
        except Exception as e:
            print(f"Bot {bot_id} error:", e)

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []

        for i in range(100):  
            tasks.append(bot(session, i))

        await asyncio.gather(*tasks)

asyncio.run(main())