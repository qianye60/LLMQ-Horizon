<div align="center">

<img src="static/LLMQ.webp" width="400" style="margin-bottom: 10px;">

# 🤖 LLMQ-Horizon QQ チャットボット

**NoneBot2とLangGraphをベースにしたインテリジェントなQQボットで、複数モデルの会話、ツール呼び出し、およびセッション管理をサポートします**

<br>

**ツールはすべてFunction-callingで記述されており、プラグインは使用していません。[OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) 、 [LangChain Tools](https://python.langchain.com/docs/how_to/#tools) を参考にしています。**

<br>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_small)
[![Docker Release](https://img.shields.io/docker/pulls/bitfennec/llmq-horizon?color=%230077c8&label=Docker%20Pulls&logo=docker&logoColor=white&style=flat)](https://hub.docker.com/r/bitfennec/llmq-horizon)
[![License](https://img.shields.io/github/license/Mgrsc/LLMQ-Horizon?color=%2300c853&label=MIT%20License&style=flat)](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE)

</div>

---

## ✨ 主な特徴

-   **🔌 豊富なツール統合：** コード実行、天気予報、占い、絵画など
-   **🤖 複数大規模モデルのサポート：** OpenAI、Google Gemini、Groqなど
-   **💬 充実した会話管理：** グループチャット/プライベートチャット、複数回会話、セッション分離
-   **🎯 柔軟なトリガー方式：** @、キーワード、コマンドプレフィックス
-   **🎨 マルチメディア機能：** 画像分析、音声ビデオ処理
-   **⚡ 自動セッション管理：** タイムアウトクリーンアップ、同時実行制御
-   **🦖 強力な拡張機能：** 独自のツールの記述、ツールによるnonebotの制御

---

## 🚀 クイックスタート

### 1. デプロイ環境の準備

-   DockerとDocker Compose
-   安定したネットワーク環境
-   推奨システム：Ubuntu 22.04以上、Debian 11以上

### 2. インストール手順

```bash
# 1. プロジェクトをクローン
git clone https://github.com/Mgrsc/LLMQ-Horizon.git
cd LLMQ-Horizon

# 2. 設定ファイルの準備
cp config-tools.toml.example config-tools.toml
cp config.toml.example config.toml
cd napcat/config/
mv onebot11_qq.json onebot11_<あなたのQQ>.json  # 実際のQQ番号に置き換えます

# 3. 設定の変更（設定ファイルのコメントを参照して変更してください）
vim config.toml
vim config-tools.toml

# 4. サービスの起動
docker compose up -d

# 5. QRコードログイン
docker compose logs -f

# LLMQサービスの再起動
docker compose restart llmq

# すべてのサービスを停止
docker compose down
```

## 🛠️ ツールの設定

<details>
<summary>💻 コード実行 (Code Runner - Judge0)</summary>

[Judge0 公式デプロイチュートリアル](https://github.com/judge0/judge0/blob/master/CHANGELOG.md)

1. **Ubuntu 22.04以上の環境とDockerを準備し、cgroup v1を構成します。**

    ```bash
    sudo sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"/' /etc/default/grub
    sudo update-grub
    sudo reboot
    ```

2. **Judge0をデプロイします。**

    ```bash
    wget https://github.com/judge0/judge0/releases/download/v1.13.1/judge0-v1.13.1.zip
    unzip judge0-v1.13.1.zip
    cd judge0-v1.13.1

    # 2つのパスワードを生成して設定します
    openssl rand -hex 32

    # 生成されたパスワードを使用して、judge0.confファイル内のREDIS_PASSWORDとPOSTGRES_PASSWORD変数を更新します。

    # サービスを起動します
    docker-compose up -d db redis
    sleep 10s
    docker-compose up -d
    sleep 5s
    ```

    Judge0 CE v1.13.1インスタンスが起動し、実行されています。http://<あなたのサーバーIPアドレス>:2358/docsにアクセスしてドキュメントを参照してください。

3. **config-tools.tomlを設定します。**

    ```toml
    [code_runner]
    judge0_url = "http://your-server:2358"
    judge0_api_key = "your-api-key"
    ```

</details>

<details>
<summary>😎 メモ (memos_manage - Memos)</summary>

[Memos 公式デプロイチュートリアル](https://www.usememos.com/docs/install/container-install)

1. **Ubuntu 22.04以上の環境とDockerを準備します。**

2. **docker-compose.yamlファイルを作成します。**

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

3. **Memosを起動します。**

    ```shell
    docker compose up -d
    ```

    この時点で、http://<あなたのサーバーIPアドレス>:5230からMemosにアクセスできます。Memosの設定でトークンを取得します。

4. **設定ファイルを記入します。**

    ```toml
    [memos]
    url = "http://your-server:xxx"
    memos_token = "<取得したトークンを入力>"
    default_visibility = "PRIVATE"
    page_size = 10
    user_id = 6
    ```

</details>

## 📝 コマンド説明

| コマンド                      | 説明                             |
| :------------------------ | :------------------------------- |
| `/chat model <モデル名>`   | 会話モデルの切り替え                 |
| `/chat clear`             | すべての会話をクリア                 |
| `/chat group <true/false>` | グループチャットの隔離のオン/オフ         |
| `/chat down`              | 会話機能をオフにします               |
| `/chat up`                | 会話機能をオンにします               |
| `/chat chunk <true/false>` | 分割送信のオン/オフ                   |

## ❗ よくある質問

<details>
<summary>1. ログインに失敗する</summary>

-   QQ番号の設定が正しいか確認してください
-   napcatの設定ファイル形式を確認してください
-   napcatコンテナのログを見て問題を特定してください

</details>

<details>
<summary>2. ツールの呼び出しに失敗する</summary>

-   モデルが関数呼び出し機能をサポートしているか確認してください
-   関連するAPIキーの設定を確認してください
-   LLMQコンテナのログを見てエラーを特定してください
-   [LangSmith](https://smith.langchain.com/)をDockerコンテナに追加してデバッグしてください。

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

-   その他の問題については、QQグループに参加して議論してください
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

このプロジェクトは[MITライセンス](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE)を採用しています。

Copyright © 2024 Bitfennec.

---