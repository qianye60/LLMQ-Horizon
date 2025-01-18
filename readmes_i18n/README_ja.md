<div align="center">

<img src="static/LLMQ.webp" width="400" style="margin-bottom: 10px;">

# 🤖 LLMQ-Horizon QQ チャットボット

**NoneBot2とLangGraphをベースにしたインテリジェントなQQボットで、マルチモデル対話、ツール呼び出し、会話管理をサポート**

<br>

**ツールはすべてFunction-callingで記述されており、プラグインは使用していません。[OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) , [LangChain Tools](https://python.langchain.com/docs/how_to/#tools) を参照してください。**

<br>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_small)
[![Docker Release](https://img.shields.io/docker/pulls/bitfennec/llmq-horizon?color=%230077c8&label=Docker%20Pulls&logo=docker&logoColor=white&style=flat)](https://hub.docker.com/r/bitfennec/llmq-horizon)
[![License](https://img.shields.io/github/license/Mgrsc/LLMQ-Horizon?color=%2300c853&label=MIT%20License&style=flat)](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE)

<br>

[English](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_en.md) | [Deutsch](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_de.md) | [Español](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_es.md) | [Français](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_fr.md) | [日本語](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_ja.md)

</div>

---

## ✨ 主な機能

-   **🔌 豊富なツール統合：** コード実行、天気予報、占い、絵画など
-   **🤖 複数の大規模モデルをサポート：** OpenAI、Google Gemini、Groqなど
-   **💬 充実した会話管理：** グループチャット/プライベートチャット、複数回対話、会話隔離
-   **🎯 柔軟なトリガー方法：** @、キーワード、コマンドプレフィックス
-   **🎨 マルチメディア機能：** 画像分析、音声・動画処理
-   **⚡ 自動会話管理：** タイムアウトクリア、同時実行制御
-   **🦖 強力な拡張性：** 独自のツール作成、ツールによるNoneBot制御

---

## 🚀 クイックスタート

### 1. 環境構築の準備

-   DockerとDocker Compose
-   安定したネットワーク環境
-   推奨システム：Ubuntu 22.04以上、Debian 11以上

> 注意：deepseekモデルでツールを有効にする場合は、5つを超えないようにしてください。また、プロンプトはできるだけ少なくしてください。そうしないと、dsがツールを大量に呼び出して使い果たしてしまうか、ツールをまったく使用しなくなる可能性があります。

### 2. インストール手順

```bash
# 1. プロジェクトのクローン
git clone https://github.com/Mgrsc/LLMQ-Horizon.git
cd LLMQ-Horizon

# 2. 設定ファイルの準備
cp config-tools.toml.example config-tools.toml
cp config.toml.example config.toml
cd napcat/config/
mv onebot11_qq.json onebot11_<あなたのQQ>.json  # 実際のQQ番号に置き換える

# 3. 設定の変更（設定ファイルのコメントを参考にして変更してください）
vim config.toml
vim config-tools.toml

# 4. サービスの起動
docker compose up -d

# 5. QRコードログイン
docker compose logs -f

# LLMQサービスの再起動
docker compose restart llmq

# すべてのサービスの停止
docker compose down
```

## 🛠️ ツールの設定

<details>
<summary>💻 コード実行 (Code Runner - Judge0)</summary>

[Judge0 公式デプロイチュートリアル](https://github.com/judge0/judge0/blob/master/CHANGELOG.md)

1.  **Ubuntu 22.04以上の環境とDockerを準備し、cgroup v1を設定：**

    ```bash
    sudo sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"/' /etc/default/grub
    sudo update-grub
    sudo reboot
    ```

2.  **Judge0をデプロイ：**

    ```bash
    wget https://github.com/judge0/judge0/releases/download/v1.13.1/judge0-v1.13.1.zip
    unzip judge0-v1.13.1.zip
    cd judge0-v1.13.1

    # 2つのパスワードを生成し、設定
    openssl rand -hex 32

    # 生成したパスワードを使用して、judge0.confファイルのREDIS_PASSWORDとPOSTGRES_PASSWORD変数を更新します。

    # サービスの起動
    docker-compose up -d db redis
    sleep 10s
    docker-compose up -d
    sleep 5s
    ```

    これで、Judge0 CE v1.13.1インスタンスが起動し、実行されます。http://<あなたのサーバーIPアドレス>:2358/docsにアクセスしてドキュメントを参照してください。

3.  **config-tools.tomlの設定：**

    ```toml
    [code_generation_running]
    judge0_url = "http://your-server:2358"
    judge0_api_key = "your-api-key"
    ```

</details>

<details>
<summary>📝 メモ (memos_manage - Memos)</summary>

[Memos 公式デプロイチュートリアル](https://www.usememos.com/docs/install/container-install)

1.  **環境の準備：**
    - Ubuntu 22.04以上
    - DockerとDocker Compose

2.  **docker-compose.yamlファイルの作成**

    ```yaml
    services:
      memos:
        image: neosmemo/memos:stable
        container_name: memos
        ports:
          - 5230:5230
        volumes:
          - ./memos:/var/opt/memos
        restart: always
    ```

3.  **サービスの起動：**

```bash
docker compose up -d
```

    これで http://<あなたのサーバーIPアドレス>:5230 でmemosにアクセスできるようになり、memosの設定でトークンを取得できます。

4.  **config-tools.tomlの設定：**

```toml
[memos_manage]
url = "http://your-server:5230"
memos_token = "your-memos-token"  # 設定ページから取得したトークン
default_visibility = "PRIVATE"
page_size = 10
user_id = 6
```
</details>

<details>
<summary>📰 ニュース取得 (get_news - SynapseNews)</summary>

[SynapseNews プロジェクトアドレス](https://github.com/Mgrsc/SynapseNews)

1.  **デプロイ手順：**

```bash
git clone https://github.com/Mgrsc/SynapseNews.git
cd synapsenews
# config.tomlの設定
docker compose up -d
```
</details>

## 📝 コマンドの説明

| コマンド                   | 説明                               |
| :------------------------- | :--------------------------------- |
| `/chat model <モデル名>`    | 会話モデルの切り替え               |
| `/chat clear`              | すべての会話をクリア               |
| `/chat group <true/false>`  | グループチャット隔離のオン/オフ     |
| `/chat down`               | 会話機能の停止                     |
| `/chat up`                 | 会話機能の開始                     |
| `/chat chunk <true/false>` | 分割送信のオン/オフ               |

## 🦊 プロンプト作成のヒント

<details>
<summary>1. 基本原則</summary>

-   明確な指示：命令形の言葉を使用して、ユーザーのニーズを明確に述べ、LLMが正確に理解できるようにします。
-   参考例/テキストの提供：詳細な例と情報を提供し、Few-shot-Promptを構成し、LLMが意図の理解を強化するのを助けます。
-   構造化された表現：マーク記号（XMLタグ、トリプルクォート、Markdownなど）を使用して可読性を高め、プロンプトの表現を明確にします。
-   出力制御：出力形式、言語スタイルなどの要件を指定して、LLMがユーザーの期待に合った出力を生成できるようにします。
-   レイアウトの最適化：LLMが理解しやすいように、プロンプトのレイアウトを慎重に調整します。
</details>

<details>
<summary>2. その他のヒント</summary>

-   利用可能なツールをリストし、複雑なツールについては説明と要件を提供します
    ```
    create_speechで音声を生成する
      - 最大40文字、絵文字は不可
      - サポート言語：中国語、英語、日本語、ドイツ語、フランス語、スペイン語、韓国語、アラビア語、ロシア語、オランダ語、イタリア語、ポーランド語、ポルトガル語
      - 使用可能な音色のマッピング:
          クレー = keli
          シグウィン = xigewen
          神子 = shenzi
          ディン・ジェン = dingzhen
          レイ・ジュン = leijun
          レイジーシープ = lanyangyang
    ```
-   ツールから返されたfile://アドレスを送信するように要求します
    ```
      絵を描く、音楽を取得する、ttsは、返されたリンクまたはファイルパスアドレスをユーザーに送信する必要があります
    ```
-   ツールから返されたコンテンツのレイアウト例
    ```
        # ツールの返されたコンテンツレイアウトの最適化例
      get_weather_dataで返されたデータのフォーマット例：
      *   A: 今日の長沙の天気を教えて
          T: ツール`get_weather_data`を呼び出して天気を取得します
          Q:
          🌤️ {場所}の天気
          🌅 日の出と日の入り: {xx:xx}-{xx:xx年を除く}
          ⏱️   時間: {時間}
          🌡️ 温度: {温度}℃
          💧 湿度: {湿度}%
          🧣 体感温度: {体感温度}℃
          🍃 風向風速: {風向}-{風速}
          📋 総合状況: {総合分析}
          赤ちゃんは外出時に服を多く着てくださいね〜風邪に気をつけて
    ```
</details>

## 🤝 貢献ガイド

1.  このリポジトリをフォークする
2.  機能ブランチを作成する (`git checkout -b feature/AmazingFeature`)
3.  変更をコミットする (`git commit -m 'Add some AmazingFeature'`)
4.  ブランチをプッシュする (`git push origin feature/AmazingFeature`)
5.  プルリクエストを開く

## 🤖 よくある質問

すべてのツールはテスト済みです。問題がある場合は、以下を参照して確認してください。

<details>
<summary>1. ログイン失敗</summary>

-   QQ番号の設定が正しいか確認してください
-   napcat設定ファイルの形式を確認してください
-   napcatコンテナログを確認して問題を解決してください

</details>

<details>
<summary>2. ツールの呼び出し失敗</summary>

-   モデルが関数呼び出し機能をサポートしていることを確認してください
-   関連するAPIキー設定を確認してください
-   LLMQコンテナログを確認してエラーを特定してください
-   dockerコンテナに[LangSmith](https://smith.langchain.com/)を追加してデバッグしてください

    ```yaml
    environment:
      - LANGCHAIN_TRACING_V2=true
      - LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
      - LANGCHAIN_API_KEY="<your_api_key>"
      - LANGCHAIN_PROJECT="<your_project_name>"
    ```

</details>

<details>
<summary>3. その他の問題</summary>

-   その他の問題については、QQグループで話し合ってください
    ![qrcode](static/qrcode.jpg)

</details>

## 🔗 関連プロジェクト

-   [NoneBot2](https://github.com/nonebot/nonebot2)
-   [LangGraph](https://github.com/langchain-ai/langgraph)
-   [LangChain](https://github.com/langchain-ai/langchain)
-   [Judge0](https://github.com/judge0/judge0)
-   [Memos](https://github.com/usememos/memos)
-   [NapCat](https://github.com/NapNeko/NapCatQQ)

## 📄 ライセンス

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=large&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_large&issueType=license)
このプロジェクトは、MITライセンスの下で配布されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
Copyright © 2024 Bitfennec.
---