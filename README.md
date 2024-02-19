# chat-botの使い方

まず大前提として、個人でOpenAI APIキーに登録していただく必要があります。

OpenAI APIキーを利用する際は[料金が発生](https://openai.com/pricing)します。

| モデル | 料金 |
|-------|-----|
|GPT-3.5 Turbo | $ 0.0005 / 1k tokens |
|GPT-4| $ 0.03 / 1k tokens |


このアプリは標準でGPT-3.5を利用しています。そこそこ使っても月数100円程度です。

GPT-4にカスタマイズすることも可能ですが、自己責任でお願いします。


## OpenAI APIキーの作成

[公式サイト](https://openai.com/blog/openai-api)にサインアップして、APIキーを取得する。

取得方法は検索すればいくらでも情報はあるが、いくつか例示する。

- https://laboratory.kazuuu.net/how-to-get-an-openai-api-key/
- https://book.st-hakky.com/data-science/open-ai-create-api-key/



[公式ドキュメント](https://platform.openai.com/docs/models/how-we-use-your-data)には次のように記載されており、意図的にオプトインしない限り、OpenAIモデルのトレーニングや改善に使用されない。

このため、兵庫県のガイドラインにも抵触しない。（デジタル改革課に確認済）

>Your data is your data.    
As of March 1, 2023, data sent to the OpenAI API will not be used to train or improve OpenAI models (unless you explicitly opt in). One advantage to opting in is that the models may get better at your use case over time.

## ローカル環境での起動

一番おススメの方法は、このアプリを各自のPCにダウンロードして、ローカル環境で起動させることです。

個人利用に限定することで、例えば「道路構造令」や「河川構造令」等の著作物についても、学習させることが可能です。

詳しくは[ローカル環境で起動させる方法](/run_local.md)を参照してください。


## WEBアプリとしてデプロイする

WEBアプリとしてデプロイすることも可能ですが、GitやGitHubの知識が必要となります。

1. GitHubのアカウントを作成する。
2. git cloneしたプロジェクト（このプロジェクト）をGitHubに連携する。
3. GitHubのリポジトリを[Streamlit](https://streamlit.io/)にデプロイする。

個人でデプロイするのが望ましいですが、例えば事務所の代表者（例えば技術専門員）がデプロイする方法もあります。事務所内でURLを共有しておけば、誰かがデプロイしたアプリを共有することができます。（利用者は自分のAPIキーを入力して使用する）

URLを一般に公開した場合、土木技術管理規程集などの内部資料の取り扱いに注意が必要となりますので、メールアドレス登録で利用者を限定するなどの対策が必要です。（streamlitで対応可能です）

参考までに[デプロイしたもの](https://chatbot-doboku.streamlit.app/)を載せておきます。