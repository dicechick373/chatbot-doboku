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
    elif stock == '土木技術管理規程集【道路Ⅰ編】':
        return "vectorstore/faiss/kiteisyuu/douro1"
    elif stock == '土木技術管理規程集【道路Ⅱ編】':
        return "vectorstore/faiss/kiteisyuu/douro2"
    elif stock == '土木技術管理規程集【河川編】':
        return "vectorstore/faiss/kiteisyuu/kasen"
    elif stock == '土木技術管理規程集【砂防編_砂防】':
        return "vectorstore/faiss/kiteisyuu/sabou"
    elif stock == '土木技術管理規程集【砂防編_急傾斜】':
        return "vectorstore/faiss/kiteisyuu/kyuukeisya"
    elif stock == '土木技術管理規程集【砂防編_地すべり】 ':
        return "vectorstore/faiss/kiteisyuu/jisuberi"
    elif stock == '近畿地整設計便覧【土木工事共通編】':
        return "vectorstore/faiss/chiseibinran/kyoutsuu"
    elif stock == '近畿地整設計便覧【道路編】 ':
        return "vectorstore/faiss/chiseibinran/douro"
    elif stock == '近畿地整設計便覧【河川編】 ':
        return "vectorstore/faiss/chiseibinran/kasen"
    
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

