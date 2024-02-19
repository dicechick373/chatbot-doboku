from backend.llm_faiss import run_llm
import streamlit as st
from streamlit_chat import message

# proxy設定 
# デプロイ時はコメントアウト
# os.environ["http_proxy"] = st.secrets["PROXY"]
# os.environ["https_proxy"] = st.secrets["PROXY"]

def vectorstore_dir(stock):
    if stock == '土木工事共通仕様書':
        return "vectorstore/faiss/kyoutsuu_shiyousyo"
    elif stock == '土木請負工事必携':
        return "vectorstore/faiss/hikkei"
    elif stock == '規程集【道路Ⅰ編】':
        return "vectorstore/faiss/kiteisyuu/douro1"
    elif stock == '規程集【道路Ⅱ編】':
        return "vectorstore/faiss/kiteisyuu/douro2"
    elif stock == '規程集【河川編】':
        return "vectorstore/faiss/kiteisyuu/kasen"
    elif stock == '規程集【砂防編_砂防】':
        return "vectorstore/faiss/kiteisyuu/sabou"
    elif stock == '規程集【砂防編_急傾斜】':
        return "vectorstore/faiss/kiteisyuu/kyuukeisya"
    elif stock == '規程集【砂防編_地すべり】 ':
        return "vectorstore/faiss/kiteisyuu/jisuberi"
    elif stock == '地整便覧【土木工事共通編】':
        return "vectorstore/faiss/chiseibinran/kyoutsuu"
    elif stock == '地整便覧【道路編】 ':
        return "vectorstore/faiss/chiseibinran/douro"
    elif stock == '地整便覧【河川編】 ':
        return "vectorstore/faiss/chiseibinran/kasen"
    
# sidebar
with st.sidebar:
    openai_api_key = st.sidebar.text_input('OpenAI API Key')

    stock = st.radio(
        label='対象図書を選択してください',
        options=('土木工事共通仕様書', '土木請負工事必携', '規程集【道路Ⅰ編】'
                 '規程集【道路Ⅱ編】', '規程集【河川編】','規程集【砂防編_砂防】',
                 '規程集【砂防編_急傾斜】', '規程集【砂防編_地すべり】',
                 '地整便覧【土木工事共通編】', '地整便覧【道路編】', '地整便覧【河川編】'),
        index=0,
        # horizontal=True,
        )

    st.subheader('Link')
    "[Source Code](https://github.com/dicechick373/chatbot-doboku)"
    "[OpenAI API](https://platform.openai.com)"

# header
st.header("LangChain🦜🔗 doboku-model")

VECTORSTORE_DIR = vectorstore_dir(stock)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "質問を入力してください"}]

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not st.session_state["openai_api_key"]:
        st.info("OpenAI API key を入力してください")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = run_llm(
            openai_api_key=st.session_state["openai_api_key"],
            query=prompt,
            vectordir = VECTORSTORE_DIR
        )
    msg = response['answer']
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)