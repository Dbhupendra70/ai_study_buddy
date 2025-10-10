 # app.py

import streamlit as st
from src.ai_engine import generate_text
from src.prompts import explain_topic, summarize_notes, generate_quiz
 
# Page config
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🧠",
    layout="centered"
)

# Header
st.title("AI Study Buddy")
st.markdown(
    "Struggling with a concept? Paste your notes? Need a quick quiz? "
    "I'm here to help — **explain, summarize, and test** your knowledge!"
)

# Tabs for core features
tab1, tab2, tab3 = st.tabs(["📘 Explain Topic ", "📝 Summarize Notes ", "❓ Generate Quiz "])

# === Tab 1: Explain Topic ===
with tab1:
    st.markdown("### 📖 What would you like to understand?")
    topic = st.text_input(
        "Enter a topic (e.g., 'Photosynthesis', 'Newton's Laws')",
        placeholder="Type a concept...",
        label_visibility="collapsed"
    )
    
    if st.button("Explain Simply", type="primary", key="explain_btn"):
        if topic.strip():
            with st.spinner("🧠 Thinking..."):
                prompt = explain_topic(topic)
                response = generate_text(prompt)
                # Save to session state so it persists
                st.session_state.explanation = response
                st.session_state.current_topic = topic
        else:
            st.warning("Please enter a topic.")

    # Always show the explanation if it exists
    if "explanation" in st.session_state and st.session_state.explanation:
        st.markdown("### 💡 Simple Explanation")
        st.write(st.session_state.explanation)

        # Follow-up question input (always visible after explanation)
        st.markdown("### ❓ Follow-Up Question")
        followup = st.text_input(
            "Ask a follow-up question about this topic:",
            placeholder="e.g., 'Can you give a real-life example?'",
            key="followup_input"
        )
        
        # Show follow-up answer only if user has typed something
        if followup.strip():
            with st.spinner("🤔 Thinking..."):
                followup_prompt = f"""
                You previously explained the topic: "{st.session_state.current_topic}".
                Now, the student asks: "{followup}"
                Answer this follow-up clearly and concisely, staying focused on the original topic.
                Keep your response under 120 words.
                """
                followup_response = generate_text(followup_prompt)
            st.markdown("### 💬 Answer")
            st.write(followup_response)

# === Tab 2: Summarize Notes ===
with tab2:
    st.markdown("### Paste your study notes below")
    notes = st.text_area(
        "Your notes",
        height=180,
        placeholder="e.g., 'Photosynthesis is the process by which green plants use sunlight to synthesize nutrients...'"
    )
    if st.button("Summarize Notes", type="primary", key="summarize_btn"):
        if notes.strip():
            with st.spinner("📝 Summarizing..."):
                prompt = summarize_notes(notes)
                response = generate_text(prompt)
                st.markdown("### 📌 Key Summary")
                st.write(response)
        else:
            st.warning("Please enter some notes.")

# === Tab 3: Generate Quiz ===
with tab3:
    st.markdown("### 📚 Paste content to quiz yourself on")
    content = st.text_area(
        "Study material",
        height=150,
        placeholder="e.g., 'Photosynthesis is the process by which green plants convert sunlight into chemical energy...'"
    )
    col1, col2 = st.columns([3, 1])
    with col1:
        num_q = st.slider("Number of questions", min_value=2, max_value=6, value=3)
    with col2:
        show_answers = st.checkbox("Show Answers", value=False)

    if st.button("🧠 Generate Quiz", type="primary"):
        if content.strip():
            with st.spinner("Generating your quiz..."):
                prompt = generate_quiz(content, num_q)
                response = generate_text(prompt)

            # Split into questions and answers
            if "Answers:" in response:
                q_part, a_part = response.split("Answers:", 1)
                questions = q_part.strip()
                answers = "Answers:\n" + a_part.strip()
            else:
                questions = response
                answers = ""

            # Display questions in a scrollable box
            st.markdown("### ❓ Your Quiz")
            st.markdown(
                f"""
                <div style="
                    background-color: #0e1117;
                    padding: 16px;
                    border-radius: 8px;
                    font-family: monospace;
                    white-space: pre-wrap;
                    max-height: 500px;
                    overflow-y: auto;
                    border: 1px solid #262730;
                ">{questions}</div>
                """,
                unsafe_allow_html=True
            )

            # Show answers conditionally
            if show_answers and answers:
                st.markdown("### ✅ Answers")
                st.markdown(
                    f"""
                    <div style="
                        background-color: #1b1e23;
                        padding: 12px;
                        border-radius: 6px;
                        font-family: monospace;
                        white-space: pre-wrap;
                    ">{answers}</div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.warning("⚠️ Please enter study content first.")