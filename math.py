import streamlit as st
import time

st.set_page_config(page_title="เกมคณิตศาสตร์", page_icon="🧠")

st.title("🧠 เกมคิดเลขเร็ว")

# เสียง
correct_sound = "https://www.soundjay.com/buttons/sounds/button-4.mp3"
wrong_sound = "https://www.soundjay.com/buttons/sounds/button-10.mp3"

# โจทย์ + ระดับความยาก
questions = [
    ("ข้อ 1: 14 + 8 = ?", 22, "🟢 ง่าย"),
    ("ข้อ 2: 35 - 17 = ?", 18, "🟢 ง่าย"),
    ("ข้อ 3: 6 × 6 + 5 = ?", 41, "🟡 ปานกลาง"),
    ("ข้อ 4: 36 ÷ 6 + 7 = ?", 13, "🟡 ปานกลาง"),
    ("ข้อ 5: 15 + 4 × 5 = ?", 35, "🟡 ปานกลาง"),
    ("ข้อ 6: (20 + 10) ÷ 5 + 3 = ?", 9, "🟠 ยาก"),
    ("ข้อ 7: 50 - 4 × 6 + 8 = ?", 34, "🟠 ยาก"),
    ("ข้อ 8: (18 ÷ 3 + 5) × 2 = ?", 22, "🔴 ยากมาก"),
    ("ข้อ 9: 72 ÷ (6 × 2) + 9 = ?", 15, "🔴 ยากมาก"),
    ("ข้อ 10: (24 + 12) ÷ 6 × 4 + 5 = ?", 29, "🔥 โหดสุด"),
]

# session
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.start_time = 0
    st.session_state.game_over = False
    st.session_state.answered = False
    st.session_state.correct = False
    st.session_state.high_score = 0

# ปุ่มเริ่มเกม
if not st.session_state.started:
    if st.button("▶️ เริ่มเกม"):
        st.session_state.started = True
        st.session_state.start_time = time.time()
    st.stop()

# sidebar คะแนนสูงสุด
st.sidebar.title("🏆 High Score")
st.sidebar.write(st.session_state.high_score)

# เกมจบ
if st.session_state.game_over:
    st.subheader("📊 สรุปผล")
    score = st.session_state.score
    st.write(f"คุณได้ {score} / 10 คะแนน")

    if score > st.session_state.high_score:
        st.session_state.high_score = score
        st.success("🏆 New High Score!")

    if score == 10:
        st.balloons()
        st.success("🎉 สุดยอดอัจฉริยะ!!!")
    elif score >= 7:
        st.info("🔥 เก่งมาก!")
    elif score >= 4:
        st.warning("🙂 พอใช้")
    else:
        st.error("😅 ลองใหม่!")

    if st.button("🔄 เล่นอีกครั้ง"):
        st.session_state.started = False
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.answered = False
    st.stop()

# แสดงข้อ
q_index = st.session_state.q_index
question, answer, level = questions[q_index]

st.subheader(question)
st.write(f"ระดับ: {level}")

# เวลา
elapsed = time.time() - st.session_state.start_time
remaining = max(0, 30 - int(elapsed))
st.write(f"⏱️ เวลาเหลือ: {remaining} วินาที")

user_answer = st.text_input("✏️ คำตอบ:", key=q_index)

# หมดเวลา
if remaining == 0 and not st.session_state.answered:
    st.audio(wrong_sound)
    st.error("⏰ หมดเวลา!")
    st.session_state.game_over = True
    st.stop()

# ปุ่มตอบ
if not st.session_state.answered:
    if st.button("✅ ตอบ"):
        st.session_state.answered = True
        if user_answer.isdigit() and int(user_answer) == answer:
            st.audio(correct_sound)
            st.success("✔️ ถูกต้อง!")
            st.session_state.score += 1
            st.session_state.correct = True
        else:
            st.audio(wrong_sound)
            st.error(f"❌ ผิด! คำตอบคือ {answer}")
            st.session_state.game_over = True
            st.stop()

# ปุ่มไปข้อถัดไป
if st.session_state.answered and st.session_state.correct:
    if st.button("➡️ ข้อถัดไป"):
        st.session_state.q_index += 1
        st.session_state.start_time = time.time()
        st.session_state.answered = False
        st.session_state.correct = False

        if st.session_state.q_index == len(questions):
            st.session_state.game_over = True
