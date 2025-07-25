import streamlit as st
import time
from rag_system import get_rag_chain

# Page configuration
st.set_page_config(
    page_title="Stardew Valley Assistant",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Stardew Valley theme with better text visibility
st.markdown("""
<style>
    .main {
        background-color: #f8f5e4;
    }
    
    /* Fix input text visibility */
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #5cb85c;
        color: #2c3e50 !important;
        background-color: white !important;
    }
    
    /* Chat input styling */
    .stChatInput > div > div > input {
        color: #2c3e50 !important;
        background-color: white !important;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: #fff;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #2c3e50;
    }
    
    /* User message styling */
    .stChatMessage[data-testid="user-message"] {
        background-color: #e8f4f8 !important;
        border-left: 4px solid #4a90e2;
        color: #2c3e50 !important;
    }
    
    /* Assistant message styling */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #f0f8e8 !important;
        border-left: 4px solid #5cb85c;
        color: #2c3e50 !important;
    }
    
    /* Header styling */
    .chat-header {
        background: linear-gradient(90deg, #4a90e2, #5cb85c);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #5cb85c;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #4a90e2;
        transition: all 0.3s;
    }
    
    /* Better contrast for all text */
    .stMarkdown, .stText, p, div {
        color: #2c3e50 !important;
    }
    
    /* Ensure chat messages are visible */
    [data-testid="stChatMessage"] {
        color: #2c3e50 !important;
    }
    
    [data-testid="stChatMessage"] p {
        color: #2c3e50 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_chain" not in st.session_state:
    with st.spinner("🌱 Loading Stardew Valley knowledge base..."):
        try:
            st.session_state.rag_chain = get_rag_chain()
            st.success("✅ Ready to help with your farming questions!")
        except Exception as e:
            st.error(f"❌ Error loading the chatbot: {str(e)}")
            st.stop()

# Header
st.markdown("""
<div class="chat-header">
    <h1>🌟 Stardew Valley Assistant 🌟</h1>
    <p>Your friendly farming companion! Ask me about crops, animals, fishing, mining, and more!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with helpful information
with st.sidebar:
    st.markdown("### 💡 Try asking about:")
    st.markdown("""
    - **Crops**: "What's the best spring crop?"
    - **Animals**: "How do I get a cow?"
    - **Fishing**: "Where can I catch salmon?"
    - **Mining**: "What's on floor 80?"
    - **Villagers**: "What does Abigail like?"
    - **Seasons**: "What should I do in winter?"
    """)
    
    st.markdown("### 🎮 Quick Tips:")
    st.markdown("""
    - Be specific in your questions
    - Ask about game mechanics
    - I know about all items and locations!
    """)
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Chat interface
chat_container = st.container()

# Display chat messages with better styling
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(f'<div style="color: #2c3e50;">{message["content"]}</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask me anything about Stardew Valley..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(f'<div style="color: #2c3e50;">{prompt}</div>', unsafe_allow_html=True)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                # Get response from RAG chain
                result = st.session_state.rag_chain.invoke(prompt)
                
                # Extract just the answer text from the result dict
                if isinstance(result, dict):
                    response = result.get('result', str(result))
                else:
                    response = str(result)
                
                # Stream the response for better UX
                message_placeholder = st.empty()
                full_response = ""
                
                # Simulate streaming
                words = response.split()
                for i, word in enumerate(words):
                    full_response += word + " "
                    time.sleep(0.02)
                    message_placeholder.markdown(f'<div style="color: #2c3e50;">{full_response}▌</div>', unsafe_allow_html=True)
                
                message_placeholder.markdown(f'<div style="color: #2c3e50;">{full_response}</div>', unsafe_allow_html=True)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                error_message = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "🌾 Powered by the Stardew Valley Wiki knowledge base 🌾<br>"
    "Built with Streamlit"
    "</div>", 
    unsafe_allow_html=True
)