# 土木技術管理規程集（道路Ⅰ編）

## 準備

`static`ディレクトリ配下に[「土木技術管理規程集」＞「道路１編」](../道路１編/)ディレクトリを作成する。

※ 後述するが、ベクトルDB「FAISS」の無料利用枠に制限があるため、検索対象としたい図書の単位ごとにベクトルDBを作成する必要がある。（つまりこの単位でディレクトリを分ける）

※ 本来は「道路Ⅰ編」だが、ベクトルDBの命名規則に違反するため「道路１編」としている。

```
static/
  　├─ 土木技術管理規程集
  　　　  ├─ 道路Ⅰ編
```

ディレクトリ内にPDFを格納する。この際、表紙や目次などは削除しておく。

また、道路１編のページ番号は「1-1」、「2-1」というように、章ごとに番号が付与されている。ページ番号を正確に反映するために、PDFファイルを分割した。

- 第１章_道路一般.pdf
- 第２章_土工.pdf
- 第３章_擁壁.pdf
- 第４章_排水.pdf
- 第５章_ボックスカルバート.pdf
- 第６章_舗装.pdf
- 第７章_参考資料.pdf


## PDFを読み込んでベクトルDBに保存する

[save_faiss.py](save_faiss.py)を実行することで、ローカルにベクトルDBが作成される。

以下、順を追って説明する。

### 設定

OpenAIのAPIキーをsecretsから読み込む。

```py
# openAIのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
```

作業ディレクトリ（PDFを格納したディレクトリ）とベクトルDBを出力するディレクトリを設定する。

ベクトルDBを保存するディレクトリ名は日本語を使えない。


```py
# 作業ディレクトリの設定
WORK_DIR = "static/土木技術管理規程集/道路１編"

# vectorstoreを保存するディレクトリの設定
# 日本語のディレクトリ名はエラーになる
VECTORSTORE_DIR = "vectorstore/faiss/kiteisyuu/douro1"
```

ここが精度のキモになる部分だと思うが、とりあえずチャンクサイズを1000、オーバーラップを100とした。

今後、回答精度を見ながらチューニングが必要。


```python
# チャンクサイズとオーバーラップの設定
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
```
参考サイト
- https://ict-worker.com/ai/langchain-chunk.html



### PDFファイル一覧の取得

分割したPDFファイルを一括で処理するために、ファイルパスのリストを作成する。

```py
pdf_files = glob.glob(f"{WORK_DIR}/*.pdf")
```

```py
pprint.pprint(pdf_files)

['static/土木技術管理規程集/道路１編\\第１章_道路一般.pdf',
 'static/土木技術管理規程集/道路１編\\第２章_土工.pdf',
 'static/土木技術管理規程集/道路１編\\第３章_擁壁.pdf',
 'static/土木技術管理規程集/道路１編\\第４章_排水.pdf',
 'static/土木技術管理規程集/道路１編\\第５章_ボックスカルバート.pdf',
 'static/土木技術管理規程集/道路１編\\第６章_舗装.pdf',
 'static/土木技術管理規程集/道路１編\\第７章_参考資料.pdf']
```

あとは、各ファイルに繰り返し処理する。

```py
for i, file in enumerate(pdf_files):
```

### PDFの読み込み

LangChainの[Document Loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf)を利用する。

色々種類はあるが、今回は[PyMuPDFLoader](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf#using-pymupdf)を採用した。

PyPDFとUnstructuredはエラーが出た。原因は突き止めていない。
PyPDFでExtracting imageを利用すればもっと精度は上がるかもしれない。

```py
def pdf_loader(pdf_file: str):
    """PDFをOCR処理してLangChainのDocumentクラスに変換する関数"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    loader = PyMuPDFLoader(pdf_file)
    docs = loader.load_and_split(text_splitter)

    return docs
```

結果はDocument型のリストが返される。

```py
docs = pdf_loader(file)
print(docs[0])
```

<details>
  <summary>出力結果のサンプル</summary>

```
page_content='1-1 \n第１章 道路一般 \n \n第１節 設計一般（標準） \n この土木技術管理規程集は兵庫県管内の道路設計に適用する。ただし、各
設計は法令、通達、示方\n書類が全てに優先するので、示方書類の改訂、新しい通達等により内容が規程集と異なった場合は規\n程集の内容を読み変 えること。また、内容の解釈に関する疑問点は、その都度、主管課に問い合わせ\nること。  \n \n表１－１－１ 示方書等の名称 \n示 方 書・指 針 \n発 刊 年 月 \n発  刊  者 \n道路構造令の解説と運用 \n平成２７年 ６月 \n日本道路協会 \n設計便覧 第3編 道路編 \n平成２４年 ４月 \n近畿地方整備局 \n積雪寒冷特別地域における道路交通確保に関す\nる特別措置法（略称：雪寒法） \n昭和３１年 ４月 \n \n平面交差の計画と設計―基礎編― \n平成３０年 １２月 \n交通工学研究会 \n改訂平面交差の計画と設計―応用編― \n平成１９年 １１月 \n〃 \n防護柵の設置基準・同解説 \n平成２８年 １２月 \n日本道路協会 \n車両用防護柵標準仕様・同解説 \n平成１６年 ３月 \n〃 \nクロソイドポケットブック \n昭和４９年 ８月 \n〃 \nラウンドアバウトマニュアル \n平成２８年 ４月  \n交通工学研究会 \n道路土工構造物技術基準・同解説 \n平成２９年 ４月 \n日本道路協会 \n（注記）地域高規格道路等の自動車専用道路については、上記の他「設計要領第一集～第四集」\n(日本道路公団)及び「高規格幹線道路幾何構造基準（案）」 （平成元年 9 月 28 日建設省\n道路局企画課）による。 \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n近畿地方整備局 \n設計便覧（案 ） \n第３編 道路編 \n第１章 道路一般 \np1-1' metadata={'source': 'static/土木技術管理規程集/道路１編\\第１章_道路一般.pdf', 'file_path': 'static/土木技術管理規程集/道路１編\\第１章_道路一般.pdf', 'page': 0, 'total_pages': 73, 'format': 'PDF 1.6', 'title': '土木技術管理 規程集', 'author': 'PC-9800ﾕｰｻﾞ', 'subject': '', 'keywords': '', 'creator': 'Microsoft® Word 2013', 'producer': 'Adobe Acrobat 10.0 Paper Capture Plug-in', 'creationDate': "D:20230422100439+09'00'", 'modDate': "D:20240121135000+09'00'", 'trapped': ''}
  ```
</details>

### metadataの加工

このままベクトルDBに保存しても良いが、せっかくなのでmetadataを加工しておく。

```python
def format_docs(org_docs, page_prefix: int):
    """MetaDataを加工する関数"""
    docs = copy.deepcopy(org_docs)
    for doc in docs:
        # source
        source = doc.metadata["source"].split("/")
        new_source = source[1] + "_" + source[2].split("\\")[0]
        doc.metadata.update({"source": new_source})

        # page
        new_page = f'{str(page_prefix)}-{str(doc.metadata["page"]+1)}'
        doc.metadata.update({"page": new_page})

    return docs
```

sourceはファイルパスが入力されているので、余計な情報を削除して整形した。

```
old:'static/土木技術管理規程集/道路１編\\第１章_道路一般.pdf'

new:土木技術管理規程集_道路１編
```

pageについても、PDFファイルのページ数を単純に「0」からカウントしているので、規程集の様式に従って「1-1」から開始する。

この辺りは、文書ごとにカスタマイズが必要。
```
old:0

new:1-1
```

### ベクトルDBに格納

LangChainで利用できるベクトルDBは多いが、今回は[FAISS](https://python.langchain.com/docs/integrations/vectorstores/faiss)を利用する。

※最初、Pineconeを利用しようとした。しかし保存はできたが読込時にSSLエラーが発生した。proxy設定しても解決しなかったので、一旦ペンディングにしておく。

FAISSの良いところは、ベクトルDBをローカルに保存できるところ。

ただしローカルDBの更新（データ追加）はできないため、複数のPDFを一つのDBに格納するためには、全PDFを一つのDocumentリストに格納してから保存する必要がある。


```python
def save_local_faiss(docs):
    """vectorstore(FAISS)に保存する関数"""
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(VECTORSTORE_DIR)
    print(f'{len(docs)}個のドキュメントを{VECTORSTORE_DIR}に保存しました。')
    return 

```

[指定したディレクトリ](/vectorstore/faiss/kiteisyuu/douro1/)にFAISSのインデックスファイルが作成される。

```
vectorstore/
  ├─ faiss
  　  ├─ kiteisyuu
 　　　　　├─  douro1
 　　　　　　　　├─  index.faiss
            　　└─  index.pkl
```

## ベクトルDBを踏まえたchat-bot

[llm_faiss.py](llm_faiss.py)でテストする。

保存したベクトルDBを読み込んで、質問に回答するchatモデルを作成する。

### 設定

対象となるベクトルDBを指定する。

```py
# ベクトルDBの指定
VECTORSTORE_DIR = "vectorstore/faiss/kiteisyuu/douro1"

```

### ベクトル検索結果の付与

[LangChainのRetrievers](https://python.langchain.com/docs/modules/data_connection/retrievers/)を利用して、FAISSの検索結果をコンテキストとして渡す。


```python
def run_llm(query, chat_history = []):
    """ベクトルDBの検索結果を踏まえて回答する関数"""

    # set embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY )
    
    # load vectorstore
    vectorstore = FAISS.load_local(VECTORSTORE_DIR,embeddings)
    
    # set chat-model
    chat = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY ,
        verbose=True,
        temperature=0,
        model_name="gpt-3.5-turbo-0613"
    )

    # set chain
    chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=vectorstore.as_retriever(), 
        return_source_documents=True)
    
    return chain({"question": query, "chat_history": chat_history})

```

せっかくなので、回答の根拠となる出典も含めるよう、加工しておく。

```python
def format_answer(response):
    """回答に出典を付与する関数"""
    sources = []
    for r in response["source_documents"]:
        source = r.metadata["source"]
        page = r.metadata["page"]
        sources.append(source + 'P:'+ page)
    
    return  f"{response['answer']} \n\n 出典「{sources}」"
```

### 出力テスト

サンプルコードは[llm_faiss.py]に置いておく。

```
質問： アスファルト舗装の最小厚さは？

回答： アスファルト舗装の最小厚さは、舗装計画交通量によって異なります。以下の表を参考にしてください。

- 舗装計画交通量が3,000以上の場合：表層と基層を合わせて20cm（15cm）
- 舗装計画交通量が1,000以上3,000未満の場合：表層と基層を合わせて15cm（10cm）
- 舗装計画交通量が250以上1,000未満の場合：表層と基層を合わせて10cm（5cm）
- 舗装計画交通量が100以上250未満の場合：表層のみを5cm
- 舗装計画交通量が40以上100未満の場合：表層のみを5cm
- 舗装計画交通量が40未満の場合：表層のみを4cm（3cm）

ただし、大型車の交通量を考慮しない場合や特殊な条件がある場合は、上記の厚さよりも薄くすることも可能です。

 出典「['土木技術管理規程集_道路１編P:6-27', '土木技術管理規程集_道路１編P:6-26', '土木技術管理規程集_道路１編P:6-24', '土木技術管理規 程集_道路１編P:6-20']」
 ```
