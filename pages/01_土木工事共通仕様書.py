from backend.llm_faiss import run_llm
import streamlit as st
from streamlit_chat import message

# proxy設定 
# デプロイ時はコメントアウト
# os.environ["http_proxy"] = st.secrets["PROXY"]
# os.environ["https_proxy"] = st.secrets["PROXY"]

# header
st.header("LangChain🦜🔗 doboku-model")

# sidebar
with st.sidebar:
    openai_api_key = st.sidebar.text_input('OpenAI API Key')
    
    st.subheader('Link')
    "[Source Code](https://github.com/dicechick373/chatbot-doboku)"
    "[OpenAI API](https://platform.openai.com)"

# ベクトルDBの指定
VECTORSTORE_DIR = "vectorstore/faiss/kyoutsuu_shiyousyo"


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "質問を入力してください"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("OpenAI API key を入力してください")
        st.stop()
  
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = run_llm(
            openai_api_key=openai_api_key,
            query=prompt,
            vectordir = VECTORSTORE_DIR
        )
    msg = response['answer']
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

