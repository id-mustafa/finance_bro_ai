import streamlit as st
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OpenAI API Key not found. Please set it in your .env file or Streamlit secrets.")
    st.stop()

# -- 1. Load your existing Chroma store
@st.cache_resource
def load_vectorstore():
    return Chroma(
        persist_directory="chroma_store",
        embedding_function=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY),
    )

# -- 2. Create retriever
@st.cache_resource
def get_retriever():
    vectorstore = load_vectorstore()
    return vectorstore.as_retriever(
        search_type="similarity", 
        search_kwargs={"k": 2}
    )

# -- 3. Build a RetrievalQA chain
@st.cache_resource
def build_retrieval_qa():
    retriever = get_retriever()
    llm = ChatOpenAI(
        model="gpt-4o",  
        openai_api_key=OPENAI_API_KEY,
        temperature=0.7,
    )
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )
    return chain

# Some of the code below has been copied from streamlit documentation
# https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps

# -- Streamlit Chat Interface
st.title("Finance Bro AI")

# This list holds the entire conversation for UI display only.
# There's no memory chain under the hood—just a single retrieval call per user question.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the conversation so far
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Prompt the user
user_input = st.chat_input("Enter your question here...")

if user_input:
    # 1) Show the user’s message in the UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2) Send the query to the retrieval chain
    with st.chat_message("assistant"):
        with st.spinner("Retrieving and generating response..."):
            chain = build_retrieval_qa()
            result = chain(user_input)
            answer = result["result"]
            sources = result["source_documents"]

    # 3) Display the assistant's response
    st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # 4) Display sources
    if sources:
        with st.expander("Sources"):
            seen = set()
            for i, doc in enumerate(sources, start=1):
                url = doc.metadata.get("source", "Unknown")
                if url not in seen:
                    seen.add(url)
                    st.write(f"{i}. {url}")
                else:
                    continue
