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

    stock = st.radio(
        label='対象図書を選択してください',
        options=('スノーピーク', '楽天', 'トヨタ'),
        index=0,
        # horizontal=True,
        )

    st.subheader('Link')
    "[Source Code](https://github.com/dicechick373/chatbot-doboku)"
    "[OpenAI API](https://platform.openai.com)"

# header
st.header("LangChain🦜🔗 doboku-model")

st.caption("サイドメニューから質問対象の図書を選んでください")

