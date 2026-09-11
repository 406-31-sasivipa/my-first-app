import streamlit as st
import time

st.set_page_config(
    page_title="เกมคิดเลขเร็ว บวก ลบ คูณ หาร",
    page_icon="🧠"
)

st.title("🧠 เกมคิดเลขเร็ว!")

# =========================
# โจทย์ + ระดับ
# =========================
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

# =========================
# reset game
# =========================
def reset_game():
    st.session_state.started = False
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.show_popup = False
    st.session_state.correct = False

# =========================
# init state
# =========================
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.show_popup = False
    st.session_state.correct = False
    st.session_state.high_score = 0

# =========================
# start screen
# =========================
if not st.session_state.started:

    st.info("🎯 ตอบโจทย์ให้ได้มากที่สุดภายใน 30 วินาทีต่อข้อ")

    if st.button("▶️ เริ่มเกม", use_container_width=True):
        st.session_state.started = True
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.session_state.game_over = False
        st.rerun()

    st.stop()

# =========================
# sidebar
# =========================
st.sidebar.title("🏆 คะแนน")

st.sidebar.metric("คะแนน", f"{st.session_state.score}/{len(questions)}")
st.sidebar.metric("High Score", st.session_state.high_score)

# =========================
# game over popup (ปลอดภัย)
# =========================
def show_result(score, total):

    st.balloons()
    st.subheader("📊 สรุปผล")

    st.metric("คะแนน", f"{score}/{total}")

    if score == total:
        st.success("🎉 อัจฉริยะสุด ๆ")
    elif score >= 7:
        st.info("🔥 เก่งมาก")
    elif score >= 5:
        st.warning("👍 ปานกลาง")
    else:
        st.error("🙂 ต้องฝึกอีก")

    if st.button("🔄 เล่นใหม่"):
        reset_game()
        st.rerun()

# =========================
# game over
# =========================
if st.session_state.game_over:

    show_result(st.session_state.score, len(questions))
    st.stop()

# =========================
# question
# =========================
q_index = st.session_state.q_index
question, answer, level = questions[q_index]

st.subheader(question)
st.write(f"ระดับ: {level}")

col1, col2 = st.columns(2)
with col1:
    st.metric("คะแนน", f"{st.session_state.score}/{len(questions)}")
with col2:
    st.metric("ข้อ", f"{q_index+1}/{len(questions)}")

# =========================
# timer (ไม่พัง UI)
# =========================
time_left = int(30 - (time.time() - st.session_state.start_time))

st.warning(f"⏳ เหลือเวลา: {max(time_left,0)} วินาที")

if time_left <= 0:
    st.session_state.game_over = True
    st.rerun()

# =========================
# answer input
# =========================
user_answer = st.text_input("✏️ คำตอบ:", key=f"ans_{q_index}")

col1, col2 = st.columns(2)

with col1:
    submit = st.button("✅ ตอบ", use_container_width=True)

with col2:
    clear = st.button("🗑️ ลบ", use_container_width=True)

if clear:
    st.session_state[f"ans_{q_index}"] = ""
    st.rerun()

# =========================
# check answer
# =========================
if submit:

    st.session_state.show_popup = True

    try:
        if int(user_answer) == answer:
            st.session_state.correct = True
            st.session_state.score += 1
        else:
            st.session_state.correct = False
    except:
        st.session_state.correct = False

# =========================
# result UI
# =========================
if st.session_state.show_popup:

    st.markdown("---")

    if st.session_state.correct:

        st.success("✔️ ถูกต้อง!")

        if q_index + 1 < len(questions):

            if st.button("➡️ ข้อถัดไป"):
                st.session_state.q_index += 1
                st.session_state.start_time = time.time()
                st.session_state.show_popup = False
                st.rerun()

        else:
            st.session_state.game_over = True
            st.rerun()

    else:

        st.error(f"❌ ผิด! คำตอบคือ {answer}")
        st.warning("เกมจบแล้ว 😢")

        st.session_state.game_over = True

        if st.button("🔄 เริ่มใหม่"):
            reset_game()
            st.rerun()
