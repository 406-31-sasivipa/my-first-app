import streamlit as st
import time

st.set_page_config(page_title="เกมคิดเลขเร็ว บวก ลบ คูณ หาร", page_icon="🧠")

st.title("🧠 เกมคิดเลขเร็ว!")

# โจทย์ + ระดับ
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
    st.session_state.show_popup = False
    st.session_state.correct = False
    st.session_state.high_score = 0

# ปุ่มเริ่ม
if not st.session_state.started:
    if st.button("▶️ เริ่มเกม"):
        st.session_state.started = True
        st.session_state.start_time = time.time()
    st.stop()

# sidebar
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
    else:
        st.warning("🙂 ลองใหม่!")

    if st.button("🔄 เล่นใหม่"):
        st.session_state.started = False
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.game_over = False
    st.stop()

# แสดงข้อ
q_index = st.session_state.q_index
question, answer, level = questions[q_index]

st.subheader(question)
st.write(f"ระดับ: {level}")

# ⏱️ นับถอยหลังแบบ real-time
time_placeholder = st.empty()

while True:
    elapsed = time.time() - st.session_state.start_time
    remaining = 30 - int(elapsed)

    if remaining <= 0:
        time_placeholder.error("⏰ หมดเวลา!")
        st.session_state.game_over = True
        st.stop()

    time_placeholder.markdown(f"## ⏱️ {remaining} วินาที")
    time.sleep(1)
    break  # สำคัญ (ไม่งั้นค้าง)

# รับคำตอบ
user_answer = st.text_input("✏️ คำตอบ:", key=q_index)

# ปุ่มตอบ
if st.button("✅ ตอบ"):
    st.session_state.show_popup = True

    if user_answer.isdigit() and int(user_answer) == answer:
        st.session_state.score += 1
        st.session_state.correct = True
    else:
        st.session_state.correct = False

# 🎉 POPUP
if st.session_state.show_popup:
    with st.dialog("🎉 ผลลัพธ์"):
        if st.session_state.correct:
            st.success("✔️ ถูกต้อง!")
            st.write("เก่งมาก ไปต่อเลย 🚀")

            if st.button("➡️ ข้อถัดไป"):
                st.session_state.q_index += 1
                st.session_state.start_time = time.time()
                st.session_state.show_popup = False

                if st.session_state.q_index == len(questions):
                    st.session_state.game_over = True
                st.rerun()

        else:
            st.error(f"❌ ผิด! คำตอบคือ {answer}")
            st.write("เกมจบแล้ว 😢")

            if st.button("🔄 เล่นใหม่"):
                st.session_state.started = False
                st.session_state.q_index = 0
                st.session_state.score = 0
                st.session_state.game_over = False
                st.session_state.show_popup = False
                st.rerun()
