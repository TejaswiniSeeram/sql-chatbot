import streamlit as st
from pathlib import Path
from faq import ingest_faq_data, faq_chain
from chatbot import sql_chain
from router import router

# Ingest FAQ data once at startup
if "faq_ingested" not in st.session_state:
    FAQ_PATH = Path(__file__).parent / "data" / "faqs.csv"
    ingest_faq_data(FAQ_PATH)
    st.session_state.faq_ingested = True

# Page config
st.set_page_config(
    page_title="Music Store Assistant", 
    page_icon="🎵",                       
    layout="centered"
)

st.title("🎵 Music Store Assistant") 
st.caption("Ask about store policies or explore the music database.")  

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render all previous messages on every rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("sql"):
            st.code(message["sql"], language="sql")
        st.write(message["content"])

# Chat input — always pinned to bottom
if prompt := st.chat_input("Ask me anything..."):

    # Show user message immediately
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "sql": None})

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            route = router(prompt).name

            if route == "faq":
                answer = faq_chain(prompt)
                sql_query = None
            elif route == "sql":
                answer, sql_query = sql_chain(prompt)
            else:
                answer = "I can answer questions about our store policies or help you explore the music database. Try asking something like 'What is your return policy?' or 'Which artist has the most albums?'"
                sql_query = None

        if sql_query:
            st.code(sql_query, language="sql")
        st.write(answer)

    # Save assistant message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sql": sql_query
    })