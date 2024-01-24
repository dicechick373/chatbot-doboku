from backend.llm_faiss import run_llm
import streamlit as st
from streamlit_chat import message

# proxy設定 
# デプロイ時はコメントアウト
# os.environ["http_proxy"] = st.secrets["PROXY"]
# os.environ["https_proxy"] = st.secrets["PROXY"]

# sidebar
with st.sidebar:
    openai_api_key = st.sidebar.text_input('OpenAI API Key')

    st.subheader('Link')
    "[Source Code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[OpenAI API](https://platform.openai.com)"

# header
st.header("LangChain🦜🔗 himeji-model")

st.caption("サイドメニューから質問対象の図書を選んでください")

