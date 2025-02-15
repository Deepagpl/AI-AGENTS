import streamlit as st
import asyncio
import sys
import os

# Add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.agent import AIAgent

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = AIAgent()
if 'messages' not in st.session_state:
    st.session_state.messages = []

def main():
    st.title("AI Agent Chatbot 🤖")
    st.subheader("Powered by Google Gemini with DuckDuckGo Search")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "search_results" in message and message["search_results"]:
                st.info(message["search_results"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            with st.spinner('Thinking...'):
                response = asyncio.run(st.session_state.agent.process_message(prompt))
                full_response = response['response']
                search_results = response.get('search_results', None)
            
            message_placeholder.markdown(full_response)
            if search_results:
                st.info(search_results)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response, "search_results": search_results})

    # Sidebar for options
    with st.sidebar:
        st.title("Options")
        if st.button("New Chat"):
            st.session_state.messages = []
            st.session_state.agent.clear_memory()
            st.rerun()

if __name__ == "__main__":
    main()
