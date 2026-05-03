import streamlit as st
import time
from assistant.engine import process_query
from assistant.validator import validate_query

st.set_page_config(page_title="Election Experience", layout="wide")

# ---------------------------
# 🧠 SESSION STATE
# ---------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "mode" not in st.session_state:
    st.session_state.mode = "Assistant"

if "query" not in st.session_state:
    st.session_state.query = ""

# ---------------------------
# 🎨 HEADER
# ---------------------------
st.markdown("""
# 🗳️ Election Experience System  
### Learn, Explore, and Experience Elections
""")

st.divider()

# ---------------------------
# 👋 USER GUIDANCE
# ---------------------------
st.info("""
👋 Welcome!

You can:
- 🧭 Learn election process (Guide)
- 🎮 Experience decisions (Simulation)
- 🎯 Complete tasks (Mission)
- 💬 Ask anything about elections

👉 Start with a quick action or try a sample question below.
""")

# ---------------------------
# 🚀 QUICK ACTIONS
# ---------------------------
st.subheader("🚀 Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🧭 Guide"):
        st.session_state.mode = "Guide"

with col2:
    if st.button("🎮 Simulation"):
        st.session_state.mode = "Simulation"

with col3:
    if st.button("🎯 Mission"):
        st.session_state.mode = "Mission"

with col4:
    if st.button("💬 Assistant"):
        st.session_state.mode = "Assistant"

st.divider()

# ---------------------------
# 🧭 GUIDE MODE
# ---------------------------
if st.session_state.mode == "Guide":
    st.header("🧭 Election Guide")

    steps = [
        "Register before deadline",
        "Understand candidates",
        "Cast your vote",
        "Votes are counted",
        "Results are declared"
    ]

    for i, step in enumerate(steps, 1):
        st.info(f"Step {i}: {step}")

# ---------------------------
# 🎮 SIMULATION MODE
# ---------------------------
elif st.session_state.mode == "Simulation":
    st.header("🎮 Simulation Mode")

    register = st.radio("Register early?", ["Yes", "No"])
    research = st.radio("Research candidates?", ["Yes", "No"])
    vote = st.radio("Vote on election day?", ["Yes", "No"])

    if st.button("Run Simulation"):
        score = sum([
            register == "Yes",
            research == "Yes",
            vote == "Yes"
        ])

        with st.spinner("Analyzing..."):
            time.sleep(1)

        if score == 3:
            st.success("🏆 Perfect participation!")
        elif score == 2:
            st.warning("👍 Good, but can improve.")
        else:
            st.error("⚠️ Low engagement.")

# ---------------------------
# 🎯 MISSION MODE
# ---------------------------
elif st.session_state.mode == "Mission":
    st.header("🎯 Mission Mode")

    st.markdown("Complete the election journey by making the right choices.")

    t1 = st.selectbox(
        "Step 1: Registration",
        ["Choose...", "Register before deadline", "Ignore registration"]
    )

    t2 = st.selectbox(
        "Step 2: Candidate Awareness",
        ["Choose...", "Research candidates", "Skip research"]
    )

    t3 = st.selectbox(
        "Step 3: Voting",
        ["Choose...", "Vote on election day", "Do not vote"]
    )

    if st.button("Evaluate Mission"):
        score = 0

        if t1 == "Register before deadline":
            score += 1
        if t2 == "Research candidates":
            score += 1
        if t3 == "Vote on election day":
            score += 1

        with st.spinner("Evaluating..."):
            time.sleep(1)

        st.metric("Score", f"{score}/3")

        if score == 3:
            st.success("🏆 Perfect! You followed all best practices.")
        elif score == 2:
            st.warning("👍 Good job! You're close.")
        else:
            st.error("⚠️ You need to engage more in the process.")

# ---------------------------
# 💬 ASSISTANT MODE
# ---------------------------
else:
    st.header("💬 Ask Assistant")

    # Input with auto-fill
    query = st.text_input(
        "Ask about elections:",
        value=st.session_state.query
    )

    # ---------------------------
    # 💡 STARTER QUESTIONS
    # ---------------------------
    st.markdown("### 💡 Try asking:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("How do I register?"):
            st.session_state.query = "How do I register?"
            st.rerun()

    with col2:
        if st.button("How does voting work?"):
            st.session_state.query = "How does voting work?"
            st.rerun()

    with col3:
        if st.button("How are votes counted?"):
            st.session_state.query = "How are votes counted?"
            st.rerun()

    # ---------------------------
    # 🤖 RESPONSE
    # ---------------------------
    if query:
        if not validate_query(query):
            st.warning("Invalid input")
        else:
            with st.spinner("Thinking..."):
                time.sleep(0.5)
                response = process_query(query)

            st.markdown(f"**🤖 Assistant:** {response}")

            st.session_state.history.append((query, response))
            st.session_state.query = ""

    # ---------------------------
    # 🧠 HISTORY
    # ---------------------------
    if st.session_state.history:
        st.divider()
        st.subheader("🧠 Recent Conversations")

        for q, r in reversed(st.session_state.history[-5:]):
            with st.expander(q):
                st.write(r)