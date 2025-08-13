# CuimsBot

A modern, conversational AI assistant for Chandigarh University campus queries, built with Streamlit, Gemini, and FAISS.

## Features
- Chatbot interface for asking questions about Chandigarh University
- Uses Google Gemini for intelligent, context-aware answers
- Fast semantic search with FAISS and Google Generative AI Embeddings
- Stylish, responsive UI with custom CSS
- Multi-turn conversation support

## Setup

### 1. Clone the repository
```
git clone <your-repo-url>
cd CuimsBot
```

### 2. Install dependencies
```
pip install -r requirements.txt
```
Or manually:
```
pip install streamlit google-generativeai langchain-google-genai langchain-community faiss-cpu
```

### 3. Add your Google API Key
Create a file at `.streamlit/secrets.toml` with:
```
GOOGLE_API_KEY = "your_actual_api_key_here"
```

### 4. Add your FAISS vector database
Place your `Vectors` folder (containing the FAISS index and data) in the project root.

### 5. Run the app
```
streamlit run app.py
```

## Usage
- Ask questions about Chandigarh University campus, facilities, academics, etc.
- The bot will search the knowledge base and respond with relevant, accurate answers.

## Customization
- Edit `app.py` to change the UI, prompts, or add more features.
- Update the FAISS database for new knowledge.

## License

This project is licensed under the [MIT License](LICENSE).
