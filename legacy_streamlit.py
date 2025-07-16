import streamlit as st
import os
import re
from backend.llm_groq import build_rag_chain
from langchain_core.messages import HumanMessage

# Folder berisi file markdown materi
LESSONS_FOLDER = "lessons"

ordered_lesson = [
    'python_variables',
    'python_list',
    'if_else',
    'while',
    'for_loops',
    'functions',
]

materi_list = []

for filename in ordered_lesson:
    filepath = os.path.join(LESSONS_FOLDER, f"{filename}.md")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

        materi_list.append({
            "file": filename,
            "konten": content
        })

# ==========================
# 2. Session State Setup
# ==========================
if "materi_index" not in st.session_state:
    st.session_state.materi_index = 0

if "chat" not in st.session_state:
    st.session_state.chat = []

# ==========================
# 3. Fungsi Ganti Topik
# ==========================
def next_topic():
    st.session_state.chat = []  # Hapus chat
    st.session_state.materi_index += 1
    if st.session_state.materi_index >= len(materi_list):
        st.session_state.materi_index = 0  # Loop ke awal
    
    # Tambahan penting
    st.session_state["user_input"] = ""  # Reset input

# ==========================
# 4. Layout Dua Kolom
# ==========================
col1, col2 = st.columns([1, 1])
# ==== 📘 Kolom Kiri: Materi ====
with col1:
    st.header("📘 Materi Python")

    with st.container():
        # Tambahkan gaya CSS agar kontainer bisa scroll
        st.markdown(
            """
            <style>
            .scrollable-box {
                width: 100%;             /* buat lebar mengikuti kolom */
                max-height: 600px;           /* opsional: perbesar tinggi juga */
                overflow-y: auto;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 1.5em;
                background-color: #f9f9f9;
                font-size: 16px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        current = materi_list[st.session_state.materi_index]

        st.markdown(f'<div class="scrollable-box">\n\n{current["konten"]}</div>', unsafe_allow_html=True)

    st.button("➡️ Next Topic", on_click=next_topic)


# ==== 🤖 Kolom Kanan: Chatbot ====
with col2:
    st.header("🤖 Tanya AI")

    user_input = st.text_input("Tanyakan sesuatu:", key="user_input")

    if user_input:
        current = materi_list[st.session_state.materi_index]
        filename = current["file"]

        # Bangun ulang RAG Chain sesuai materi
        rag_chain = build_rag_chain(filename)   

        config = {"configurable": {"session_id": f"chat-{filename}"}}

        response = rag_chain.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config
        )

        bot_response = response.content
        st.session_state.chat.append((user_input, bot_response))

    for user, bot in st.session_state.chat:
        st.markdown(f"**👤:** {user}")
        st.markdown(f"**🤖:** {bot}")
        st.markdown("---")
