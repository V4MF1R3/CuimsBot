import streamlit as st
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

st.set_page_config(
    page_title="CuimsBot",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

def load_css():
    st.markdown("""
    <style>
    /* --- General Styles --- */
    body {
        color: #e0e0e0;
    }
    .stApp {
        background: linear-gradient(135deg, #1f1c2c 0%, #3a3258 100%);
        background-attachment: fixed;
    }

    /* --- Main Title & Header --- */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
    }
    .header-icon {
        font-size: 3rem;
        margin-right: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }
    .subtitle {
        font-size: 1.1rem;
        color: #a0a0b0;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* --- Chat Message Styling --- */
    .stChatMessage {
        background: none;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        border-radius: 15px;
        margin-bottom: 1rem;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
    }
    .stChatMessage[data-testid="chat-message-container-user"] {
        # --- CACHED FAISS DB LOADING ---
        @st.cache_resource(show_spinner=False)
        def load_faiss_db(api_key):
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=api_key
            )
            return FAISS.load_local(
                "Vectors",
                embeddings=embeddings,
                allow_dangerous_deserialization=True
            )

        background: #2a273c;
    }
    .stChatMessage[data-testid="chat-message-container-assistant"] {
        background: #3a3258;
    }
    
    /* --- Avatars in Chat Messages --- */
    [data-testid="stChatMessageContent"]::before {
        font-family: "sans-serif";
        font-size: 1.5rem;
        position: absolute;
        top: 10px;
        left: -40px;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        box-shadow: 0 0 5px rgba(255,255,255,0.2);
    }
    [data-testid="chat-message-container-user"] [data-testid="stChatMessageContent"]::before {
        content: "👤";
        background: #6a5acd; /* SlateBlue */
    }
    [data-testid="chat-message-container-assistant"] [data-testid="stChatMessageContent"]::before {
        content: "🤖";
        background: #ff6347; /* Tomato */
    }
    [data-testid="stChatMessageContent"] {
        position: relative;
        padding-left: 20px;
    }
                        st.session_state.db = load_faiss_db(API_KEY)
        background-color: #ff6347;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.75rem 1rem;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #e5533d;
        border: none;
    }
    
    /* --- Welcome Screen --- */
    .welcome-container {
        text-align: center;
        padding: 2rem;
        background: rgba(42, 39, 60, 0.7);
        border-radius: 15px;
    }
    .example-prompt {
        background-color: #3a3258;
        border: 1px solid #4a4a6a;
        border-radius: 10px;
        padding: 0.75rem;
        margin: 0.5rem;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .example-prompt:hover {
        background-color: #4a4a6a;
    }

    </style>
    """, unsafe_allow_html=True)

load_css()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "db" not in st.session_state:
    st.session_state.db = None
if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = None

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except (KeyError, TypeError):
    st.error("🔑 Google API key not found. Please add it to your Streamlit secrets.")
    st.stop()
if st.session_state.gemini_model is None:
    st.session_state.gemini_model = genai.GenerativeModel('gemini-1.5-flash')

with st.sidebar:
    st.header("🛠️ Controls")
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    if st.session_state.db is None:
        with st.spinner("Loading knowledge base... Please wait."):
            try:
                embeddings = GoogleGenerativeAIEmbeddings(
                    model="models/embedding-001",
                    google_api_key=API_KEY
                )
                st.session_state.db = FAISS.load_local(
                    "Vectors", 
                    embeddings=embeddings, 
                    allow_dangerous_deserialization=True
                )
                st.success("✅ Knowledge base ready!")
            except Exception as e:
                st.error(f"❌ Error loading database: {e}", icon="🚨")
                st.info("Ensure the 'Vectors' folder is in the root directory.")
    else:
        st.success("✅ Knowledge base is active.")
    st.markdown("---")
    st.info("This bot provides information based on the CU campus knowledge base.")
    st.markdown('''<div style='text-align:center; padding: 1rem 0;'>Made with ❤️ by <a href="https://github.com/V4MF1R3">V4MF1R3</a></div>''', unsafe_allow_html=True)


st.markdown("""
<div class="header-container">
    <div class="header-icon">🎓</div>
    <div class="main-title">Chandigarh University AI Assistant</div>
</div>
<div class="subtitle">Your intelligent guide to the CU campus. Ask me anything!</div>
""", unsafe_allow_html=True)


SYSTEM_PROMPT = """You are an intelligent assistant trained to answer queries related to campus of Chandigarh University. 
Based on the context, provide relevant and accurate answers in a friendly and helpful tone. Format your answers clearly using markdown where appropriate (like lists or bolding).
If the answer cannot be found within the context, politely state that you don't have information on that specific topic and suggest asking another question about the campus.
Do not make up answers. Do not use disrespectful or foul language. Stick to the information provided in the context."""

def get_chatbot_response(user_input):
    if not st.session_state.db or not st.session_state.gemini_model:
        return "Please wait, the AI components are still initializing."
    if "gemini_chat" not in st.session_state:
        st.session_state.gemini_chat = st.session_state.gemini_model.start_chat()
    try:
        search_results = st.session_state.db.similarity_search(user_input, k=3)
        context = '\n'.join([page.page_content for page in search_results])
        if len(st.session_state.gemini_chat.history) == 0:
            user_message = f"{SYSTEM_PROMPT}\n\nContext: {context}\n\n{user_input}"
        else:
            user_message = f"Context: {context}\n\n{user_input}"
        response = st.session_state.gemini_chat.send_message(user_message)
        return response.text
    except Exception as e:
        st.error(f"Sorry, an error occurred: {e}")
        return "Sorry, I couldn't process your request right now. Please try again later."

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if not st.session_state.messages:
    with st.container():
        st.markdown("<div class='welcome-container'><h3>Welcome!</h3><p>What would you like to know about the CU campus? Try one of these:</p></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Tell me about Chandigarh University.", use_container_width=True):
                st.session_state.latest_prompt = "Tell me about Chandigarh University"
                st.rerun()
        with col2:
            if st.button("What is the fees of BE computer science?", use_container_width=True):
                st.session_state.latest_prompt = "What is the fees of BE computer science?"
                st.rerun()
prompt_to_process = st.chat_input("Ask about CU campus...") or st.session_state.get("latest_prompt")
if prompt_to_process:
    if "latest_prompt" in st.session_state:
        del st.session_state["latest_prompt"]
    st.session_state.messages.append({"role": "user", "content": prompt_to_process})
    with st.chat_message("user"):
        st.markdown(prompt_to_process)
    with st.chat_message("assistant"):
        with st.spinner("🧠 Thinking..."):
            response = get_chatbot_response(prompt_to_process)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    if not st.chat_input:
        st.rerun()