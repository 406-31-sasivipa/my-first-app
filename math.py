import streamlit as st
import time

st.set_page_config(page_title="เกมคณิตศาสตร์", page_icon="🧠")

st.title("🧠 เกมคิดเลขเร็ว!")
st.write("ตอบให้ถูกภายใน 30 วินาที ⏱️")

# เสียง (ใช้ลิงก์ออนไลน์)
correct_sound = "https://www.soundjay.com/buttons/sounds/button-4.mp3"
wrong_sound = "https://www.soundjay.com/buttons/sounds/button-10.mp3"

# โจทย์
questions = [
    ("ข้อ 1: 14 + 8 = ?", 22),
    ("ข้อ 2: 35 - 17 = ?", 18),
    ("ข้อ 3: 6 × 6 + 5 = ?", 41),
    ("ข้อ 4: 36 ÷ 6 + 7 = ?", 13),
    ("ข้อ 5: 15 + 4 × 5 = ?", 35),
    ("ข้อ 6: (20 + 10) ÷ 5 + 3 = ?", 9),
    ("ข้อ 7: 50 - 4 × 6 + 8 = ?", 34),
    ("ข้อ 8: (18 ÷ 3 + 5) × 2 = ?", 22),
    ("ข้อ 9: 72 ÷ (6 × 2) + 9 = ?", 15),
    ("ข้อ 10: (24 + 12) ÷ 6 × 4 + 5 = ?", 29),
]

# session
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.high_score = 0

# รีเกม
if st.button("🔄 เริ่มใหม่"):
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.game_over = False

# แสดง High Score
st.sidebar.title("🏆 High Score")
st.sidebar.write(f"คะแนนสูงสุด: {st.session_state.high_score}")

# เกมจบ
if st.session_state.game_over:
    st.subheader("📊 สรุปผล")
    score = st.session_state.score
    st.write(f"คุณได้ {score} / 10 คะแนน")

    # อัปเดต High Score
    if score > st.session_state.high_score:
        st.session_state.high_score = score
        st.success("🏆 New High Score!")

    if score == 10:
        st.balloons()
        st.success("🎉 สุดยอดอัจฉริยะ!!!")
    elif score >= 7:
        st.info("🔥 เก่งมาก!")
    elif score >= 4:
        st.warning("🙂 พอใช้ ลองใหม่!")
    else:
        st.error("😅 ฝึกอีกนิดนะ!")

else:
    q_index = st.session_state.q_index
    question, answer = questions[q_index]

    st.subheader(question)

    # เวลา
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 30 - int(elapsed))
    st.write(f"⏱️ เวลาเหลือ: {remaining} วินาที")

    user_answer = st.text_input("✏️ คำตอบ:", key=q_index)

    # หมดเวลา
    if remaining == 0:
        st.audio(wrong_sound)
        st.error("⏰ หมดเวลา!")
        st.session_state.game_over = True

    # ตอบ
    if st.button("✅ ตอบ"):
        if user_answer.isdigit() and int(user_answer) == answer:
            st.audio(correct_sound)
            st.success("✔️ ถูกต้อง!")
            st.session_state.score += 1
            st.session_state.q_index += 1
            st.session_state.start_time = time.time()

            if st.session_state.q_index == len(questions):
                st.session_state.game_over = True
        else:
            st.audio(wrong_sound)
            st.error(f"❌ ผิด! คำตอบคือ {answer}")
            st.session_state.game_over = True
