<div align="center">

<img src="static/LLMQ.webp" width="400" style="margin-bottom: 10px;">

# 🤖 LLMQ-Horizon QQ チャットボット

**NoneBot2とLangGraphをベースにしたインテリジェントなQQボットで、多モデル対話、ツール呼び出し、セッション管理をサポート**

<br>

**ツールはすべて Function-calling で記述されており、プラグインは使用していません。[OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) 、[LangChain Tools](https://python.langchain.com/docs/how_to/#tools) を参照してください。**

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
-   **💬 完璧な対話管理：** グループチャット/プライベートチャット、複数回の対話、セッション分離
-   **🎯 柔軟なトリガー方式：** @、キーワード、コマンドプレフィックス
-   **🎨 マルチメディア機能：** 画像分析、音声・動画処理
-   **⚡ 自動セッション管理：** タイムアウトクリア、同時実行制御
-   **🦖 強力な拡張性：** 独自のツールを作成可能、ツールでnonebotを制御可能

---

## 🚀 クイックスタート

### 1. 展開環境の準備

-   DockerとDocker Compose
-   安定したネットワーク環境
-   推奨システム：Ubuntu 22.04 以上、Debian 11以上

### 2. インストール手順

```bash
# 1. プロジェクトをクローン
git clone https://github.com/Mgrsc/LLMQ-Horizon.git
cd LLMQ-Horizon

# 2. 設定ファイルの準備
cp config-tools.toml.example config-tools.toml
cp config.toml.example config.toml
cd napcat/config/
mv onebot11_qq.json onebot11_<あなたのQQ>.json  # 実際のQQ番号に置き換える

# 3. 設定の変更（設定ファイルのコメントを参照して変更）
vim config.toml
vim config-tools.toml

# 4. サービスの起動
docker compose up -d

# 5. QRコードログイン
docker compose logs -f

# LLMQサービスを再起動
docker compose restart llmq

# すべてのサービスを停止
docker compose down
```

## 🛠️ ツールの設定

<details>
<summary>💻 コード実行 (Code Runner - Judge0)</summary>

[Judge0 公式デプロイチュートリアル](https://github.com/judge0/judge0/blob/master/CHANGELOG.md)

1. **Ubuntu 22.04以上の環境とDockerを準備し、cgroup v1を設定します：**

    ```bash
    sudo sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"/' /etc/default/grub
    sudo update-grub
    sudo reboot
    ```

2. **Judge0をデプロイ：**

    ```bash
    wget https://github.com/judge0/judge0/releases/download/v1.13.1/judge0-v1.13.1.zip
    unzip judge0-v1.13.1.zip
    cd judge0-v1.13.1

    # 2つのパスワードを生成し、設定します。
    openssl rand -hex 32

    # 生成したパスワードを使用して、judge0.confファイルのREDIS_PASSWORDとPOSTGRES_PASSWORD変数を更新します。

    # サービスを起動します。
    docker-compose up -d db redis
    sleep 10s
    docker-compose up -d
    sleep 5s
    ```

    Judge0 CE v1.13.1インスタンスが起動しました。ドキュメントは http://<あなたのサーバーIPアドレス>:2358/docs で参照できます。

3.  **config-tools.toml を設定します：**

    ```toml
    [code_generation_running]
    judge0_url = "http://your-server:2358"
    judge0_api_key = "your-api-key"
    ```

</details>

<details>
<summary>😎 メモ (memos_manage - Memos)</summary>

[Memos 公式デプロイチュートリアル](https://www.usememos.com/docs/install/container-install)

1. **Ubuntu 22.04以上の環境とDockerを準備します：**

2. **docker-compose.yaml ファイルを作成します**

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

3. **memosを起動します**

    ```shell
    docker compose up -d
    ```

    これで http://<あなたのサーバーIPアドレス>:5230 で memos にアクセスできます。memos の設定でトークンを取得します。

4. **設定ファイルを記入します**

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

| コマンド                        | 説明                               |
| :------------------------------ | :--------------------------------- |
| `/chat model <モデル名>`      | 対話モデルを切り替える               |
| `/chat clear`                   | すべてのセッションをクリアする         |
| `/chat group <true/false>`     | グループチャットの分離を切り替える       |
| `/chat down`                    | 対話機能をオフにする                 |
| `/chat up`                      | 対話機能をオンにする                 |
| `/chat chunk <true/false>`     | 分割送信を切り替える                 |

## 🦊プロンプト作成のヒント

<details>
<summary>1.基本原則</summary>

- 明確な指示: 命令形を使い、ユーザーの要求を明確に伝えることで、LLMが正確に理解できるようにします。
- 参考例/テキストの提供: 詳細な例や情報を提供し、Few-shot-Promptを構成することで、LLMが意図をよりよく理解できるようにします。
- 構造化された表現: XMLタグ、三重引用符、Markdownなどのマークを使用して可読性を高め、プロンプトを明確に表現します。
- 出力制御: 出力形式や言語スタイルなどの要件を指定し、LLMがユーザーの期待に沿った出力を生成できるようにします。
- レイアウトの最適化: プロンプトのレイアウトを慎重に調整し、LLMが理解しやすくします。
</details>
<details>
<summary>2.その他のヒント</summary>

- 利用可能なツールをリストし、複雑なツールについては説明と要件を示します。
  ```
  create_speechで音声を生成
    - 最大40文字、絵文字不可
    - 対応言語：中国語、英語、日本語、ドイツ語、フランス語、スペイン語、韓国語、アラビア語、ロシア語、オランダ語、イタリア語、ポーランド語、ポルトガル語
    - 使用可能な音色：
        可莉 = keli
        西格雯 = xigewen
        神子 = shenzi
        丁真 = dingzhen
        雷军 = leijun
        懒羊羊 = lanyangyang
  ```
- ツールから返されるfile://アドレスを要求します。
  ```
    絵を描く、音楽を取得する、ttsの場合は、返されたリンクまたはファイルパスのアドレスをユーザーに送信する必要があります。
  ```
- ツールから返される内容のレイアウト例
  ```
      # ツールから返される内容のレイアウト最適化例
    get_weather_dataから返されたデータ形式の例：
    *   A: 今日の長沙の天気を教えて
        T: ツール`get_weather_data`を呼び出して天気を取得
        Q:
        🌤️ {場所}の天気
        🌅 日の出日の入り: {xx:xx}-{xx:xx年なし}
        ⏱️   時間: {時間}
        🌡️ 温度: {温度}℃
        💧 湿度: {湿度}%
        🧣 体感温度: {体感温度}℃
        🍃 風向風速: {風向}-{風速}
        📋 総合状況: {総合分析}
        赤ちゃんは外出する際は服をたくさん着せてね〜風邪に気を付けて
  ```
</details>

## ❗ よくある質問

すべてのツールはテスト済みです。問題がある場合は、以下を参照して確認してください。

<details>
<summary>1. ログイン失敗</summary>

-   QQ番号の設定が正しいか確認してください
-   napcatの設定ファイル形式を確認してください
-   napcatコンテナのログを見て問題を特定してください

</details>

<details>
<summary>2. ツール呼び出し失敗</summary>

-   モデルが関数呼び出し機能をサポートしているか確認してください
-   関連するAPIキー設定を確認してください
-   LLMQコンテナのログを見てエラーを特定してください
-   [LangSmith](https://smith.langchain.com/) をDockerコンテナに追加してデバッグします

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

-   その他の問題はQQグループでご相談ください
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

このプロジェクトは [MIT ライセンス](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE) の下でライセンスされています。

Copyright © 2024 Bitfennec.

---