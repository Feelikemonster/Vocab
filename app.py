import random
import streamlit as st

st.set_page_config(page_title="Vocab Dictionary", page_icon="📚", layout="centered")

st.title("📚 Vocab Dictionary")
with st.expander("📱 Telefona uygulama gibi ekle"):
    st.markdown("""
**Android (Chrome):** ⋮ → **Ana ekrana ekle**

**iPhone (Safari):** Paylaş (⬆️) → **Ana Ekrana Ekle**
""")
st.write("Doğru seçeneği işaretle. Next ile yeni soruya geç.")

WORDS = [
    {"word": "borrow", "tr": "ödünç almak"},
    {"word": "lend", "tr": "ödünç vermek"},
    {"word": "increase", "tr": "artmak / artırmak"},
    {"word": "improve", "tr": "geliştirmek"},
    {"word": "achieve", "tr": "başarmak"},
    {"word": "refuse", "tr": "reddetmek"},
]

def new_question():
    q = random.choice(WORDS)
    correct = q["tr"]
    wrong = random.sample([w["tr"] for w in WORDS if w["tr"] != correct], k=3)
    choices = wrong + [correct]
    random.shuffle(choices)
    st.session_state.q = q
    st.session_state.choices = choices
    st.session_state.answered = False
    st.session_state.selected = None

if "score" not in st.session_state:
    st.session_state.score = 0
if "q" not in st.session_state or "choices" not in st.session_state:
    new_question()
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected" not in st.session_state:
    st.session_state.selected = None

q = st.session_state.q
st.subheader(f"Word: **{q['word']}**")

st.session_state.selected = st.radio(
    "Meaning:",
    st.session_state.choices,
    index=None,
    key="radio_choice"
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✅ Submit", use_container_width=True):
        if st.session_state.selected is None:
            st.warning("Bir seçenek seç 🙂")
        else:
            st.session_state.answered = True
            if st.session_state.selected == q["tr"]:
                st.session_state.score += 1
                st.success("Doğru! 🎉")
            else:
                st.error(f"Yanlış. Doğru cevap: **{q['tr']}**")

with col2:
    if st.button("➡️ Next", use_container_width=True):
        new_question()
        st.rerun()

with col3:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.score = 0
        new_question()
        st.rerun()

st.divider()
st.metric("Score", st.session_state.score)

