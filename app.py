import streamlit as st
import pickle
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Sleep Predictor", page_icon="🌙", layout="centered")

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
    color: white;
    font-family: 'Poppins', sans-serif;
}

/* Center layout */
.block-container {
    max-width: 700px;
    margin: auto;
    padding-top: 2rem;
}

/* ⭐ LEFT STARS */
.stars-left {
    position: fixed;
    top: 0;
    left: 0;
    width: 25%;
    height: 100%;
    background-image: radial-gradient(white 2px, transparent 2px);
    background-size: 60px 60px;
    opacity: 0.7;
    animation: moveLeftStars 40s linear infinite;
}

/* ⭐ RIGHT STARS */
.stars-right {
    position: fixed;
    top: 0;
    right: 0;
    width: 25%;
    height: 100%;
    background-image: radial-gradient(white 2px, transparent 2px);
    background-size: 60px 60px;
    opacity: 0.7;
    animation: moveRightStars 50s linear infinite;
}

/* Animations */
@keyframes moveLeftStars {
    from { transform: translateY(0); }
    to { transform: translateY(100px); }
}

@keyframes moveRightStars {
    from { transform: translateY(0); }
    to { transform: translateY(-100px); }
}

/* 🌙 Moon */
.moon {
    position: fixed;
    top: 80px;
    right: 80px;
    font-size: 90px;
    opacity: 0.95;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(45deg, #6C63FF, #9D7CFF);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-size: 16px;
    border: none;
}

/* Card */
.card {
    background: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin-top: 20px;
    text-align: center;
}

/* Titles */
h1, h2, h3 {
    text-align: center;
}

</style>

<div class="stars-left"></div>
<div class="stars-right"></div>
<div class="moon">🌕</div>

""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))

# ---------------- TITLE ----------------
st.markdown("<h1>🌙 Sleep Quality Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Improve your sleep with smart predictions</p>", unsafe_allow_html=True)

# ---------------- INPUT ----------------
st.markdown("## 🛏️ Enter Your Daily Habits")

sleep = st.number_input("😴 Sleep Hours", min_value=0.0, step=0.5)
stress = st.slider("😓 Stress Level", 0, 10)
exercise = st.number_input("🏃 Exercise Minutes", min_value=0)

# ---------------- HISTORY ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- BUTTONS ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🔮 Predict Sleep Quality"):
        result = model.predict([[sleep, stress, exercise]])[0]

        st.markdown(f"""
        <div class="card">
            <h2>🌟 Sleep Quality: {result}</h2>
        </div>
        """, unsafe_allow_html=True)

        # Save history
        st.session_state.history.append({
            "Sleep": sleep,
            "Stress": stress,
            "Exercise": exercise,
            "Result": result
        })

        # Suggestions
        st.markdown("### 💡 Suggestions")

        if result == "Poor":
            st.error("❌ Poor sleep detected")

        if stress > 7:
            st.warning("⚠️ Reduce stress")

        if sleep < 6:
            st.warning("⚠️ Sleep more (7–8 hours)")

        if exercise < 10:
            st.warning("⚠️ Do more exercise")

        if result == "Good":
            st.success("✅ Great sleep quality!")

with col2:
    if st.button("🔄 Reset Inputs"):
        st.experimental_rerun()

# ---------------- NEW SIMPLE TREND ----------------
st.markdown("## 📈 Sleep Quality Trend")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)

    # Convert result to score
    mapping = {"Poor": 1, "Average": 2, "Good": 3}
    df["Score"] = df["Result"].map(mapping)

    st.line_chart(df["Score"])
    st.caption("1 = Poor | 2 = Average | 3 = Good")

else:
    st.info("No data yet. Click Predict multiple times.")

# ---------------- HISTORY TABLE ----------------
if st.button("📂 View Past Predictions"):
    if st.session_state.history:
        st.write(pd.DataFrame(st.session_state.history))
    else:
        st.write("No data available")