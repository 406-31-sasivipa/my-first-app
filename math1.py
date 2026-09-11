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
# ฟังก์ชันเริ่มเกมใหม่
# =========================
def reset_game():
    st.session_state.started = False
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.start_time = 0
    st.session_state.game_over = False
    st.session_state.show_popup = False
    st.session_state.correct = False


# =========================
# Session State
# =========================
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.start_time = 0
    st.session_state.game_over = False
    st.session_state.show_popup = False
    st.session_state.correct = False
    st.session_state.high_score = 0


# =========================
# หน้าเริ่มเกม
# =========================
if not st.session_state.started:

    st.info("🎯 ตอบโจทย์ให้ได้มากที่สุดภายในเวลาที่กำหนด")

    if st.button("▶️ เริ่มเกม", use_container_width=True):
        st.session_state.started = True
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.show_popup = False
        st.session_state.start_time = time.time()
        st.rerun()

    st.stop()


# =========================
# Sidebar แสดงคะแนน
# =========================
st.sidebar.title("🏆 คะแนน")

st.sidebar.metric(
    "คะแนนปัจจุบัน",
    f"{st.session_state.score} / {len(questions)}"
)

st.sidebar.metric(
    "High Score",
    st.session_state.high_score
)


# =========================
# เกมจบ
# =========================
if st.session_state.game_over:

    st.subheader("📊 สรุปผล")

    score = st.session_state.score

    st.metric(
        "คะแนนที่ได้",
        f"{score} / {len(questions)}"
    )

    # บันทึก High Score
    if score > st.session_state.high_score:
        st.session_state.high_score = score
        st.success("🏆 New High Score!")

    if score == 10:
        st.balloons()
        st.success("🎉 สุดยอดอัจฉริยะ!!!")

    elif 7 <= score < 10 :
        st.info("🔥 ตัวท็อปคณิตศาสตร์")

    elif 5 <= score < 7 :
        st.warning("👍 คณิตศาสตร์คนปกติ")

    else:
        st.error("🙂 เด็กหลังห้อง พยายามใหม่นะ")

    st.markdown("---")

    if st.button("🔄 เริ่มเล่นใหม่", use_container_width=True):
        reset_game()
        st.rerun()

    st.stop()


# =========================
# แสดงโจทย์
# =========================
q_index = st.session_state.q_index

question, answer, level = questions[q_index]

st.subheader(question)

st.write(f"ระดับ: {level}")

# แสดงคะแนนด้านบน
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "📊 คะแนน",
        f"{st.session_state.score} / {len(questions)}"
    )

with col2:
    st.metric(
        "📝 ข้อที่",
        f"{q_index + 1} / {len(questions)}"
    )


# =========================
# Timer
# =========================
if "start" in st.session_state and not st.session_state.get("is_ended", False):
    time_left = int(30 - (time.time() - st.session_state.start))

    if time_left > 0:
        st.error(f"⏳ เหลือเวลา: {time_left} วินาที")
    else:
        st.session_state.is_ended = True
        st.rerun()

st.divider()

# =========================
# หมดเวลา
# =========================
if remaining == 0:

    st.error("⏰ หมดเวลา!")

    st.session_state.game_over = True

    st.markdown("---")

    st.warning(
        f"📊 คุณทำได้ {st.session_state.score} / {len(questions)} คะแนน"
    )

    if st.button("🔄 เริ่มเล่นใหม่", use_container_width=True):
        reset_game()
        st.rerun()

    st.stop()


# =========================
# ช่องกรอกคำตอบ
# =========================
user_answer = st.text_input(
    "✏️ คำตอบ:",
    key=f"answer_{q_index}"
)


# =========================
# ปุ่มตอบ + ลบคำตอบ
# =========================
col1, col2 = st.columns(2)

with col1:
    answer_button = st.button(
        "✅ ตอบ",
        use_container_width=True
    )

with col2:
    clear_button = st.button(
        "🗑️ ลบคำตอบ",
        use_container_width=True
    )


# ปุ่มลบคำตอบ
if clear_button:
    st.session_state[f"answer_{q_index}"] = ""
    st.rerun()


# =========================
# ตรวจคำตอบ
# =========================
if answer_button:

    st.session_state.show_popup = True

    # รองรับจำนวนเต็ม
    try:
        user_number = int(user_answer)

        if user_number == answer:
            st.session_state.correct = True

            # เพิ่มคะแนน
            st.session_state.score += 1

        else:
            st.session_state.correct = False

    except ValueError:
        st.session_state.correct = False


# =========================
# แสดงผลคำตอบ
# =========================
if st.session_state.show_popup:

    st.markdown("---")

    if st.session_state.correct:

        st.success("✔️ ถูกต้อง!")

        st.write(
            f"🎉 เก่งมาก! ตอนนี้คุณได้ "
            f"**{st.session_state.score} / {len(questions)} คะแนน**"
        )

        # ถ้ายังมีข้อเหลือ
        if q_index + 1 < len(questions):

            if st.button(
                "➡️ ข้อถัดไป",
                use_container_width=True
            ):

                st.session_state.q_index += 1
                st.session_state.start_time = time.time()
                st.session_state.show_popup = False
                st.session_state.correct = False

                st.rerun()

        # ถ้าครบ 10 ข้อ
        else:

            st.session_state.game_over = True

            if st.button(
                "🏆 ดูคะแนนสุดท้าย",
                use_container_width=True
            ):
                st.rerun()

    else:

        st.error(f"❌ ผิด! คำตอบคือ {answer}")

        st.write(
            f"📊 คะแนนของคุณ: "
            f"**{st.session_state.score} / {len(questions)}**"
        )

        st.warning("เกมจบแล้ว 😢")

        if st.button(
            "🔄 เริ่มเล่นใหม่",
            use_container_width=True
        ):
            reset_game()
            st.rerun()
