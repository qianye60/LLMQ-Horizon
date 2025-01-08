<div align="center">

<img src="static/LLMQ.webp" width="400" style="margin-bottom: 10px;">

# 🤖 LLMQ-Horizon QQ Chatbot

**An intelligent QQ chatbot based on NoneBot2 and LangGraph, supporting multi-model conversations, tool invocation, and session management.**

<br>

**Tools are written using Function-calling, without using plugins, refer to [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) , [LangChain Tools](https://python.langchain.com/docs/how_to/#tools)**

<br>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_small)
[![Docker Release](https://img.shields.io/docker/pulls/bitfennec/llmq-horizon?color=%230077c8&label=Docker%20Pulls&logo=docker&logoColor=white&style=flat)](https://hub.docker.com/r/bitfennec/llmq-horizon)
[![License](https://img.shields.io/github/license/Mgrsc/LLMQ-Horizon?color=%2300c853&label=MIT%20License&style=flat)](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE)

<br>

[English](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_en.md) | [Deutsch](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_de.md) | [Español](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_es.md) | [Français](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_fr.md) | [日本語](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_ja.md)

</div>

---

## ✨ Key Features

-   **🔌 Rich Tool Integrations:** Code execution, weather queries, divination, drawing, etc.
-   **🤖 Supports Multiple Large Models:** OpenAI, Google Gemini, Groq, etc.
-   **💬 Comprehensive Conversation Management:** Group chat/private chat, multi-turn conversations, session isolation
-   **🎯 Flexible Triggering Methods:** @ mentions, keywords, command prefixes
-   **🎨 Multimedia Capabilities:** Image analysis, audio and video processing
-   **⚡ Automatic Session Management:** Timeout cleaning, concurrency control
-   **🦖 Powerful Extensibility:** You can write your own tools, and use tools to control nonebot

---

## 🚀 Quick Start

### 1. Deployment Environment Preparation

-   Docker and Docker Compose
-   Stable network environment
-   Recommended Systems: Ubuntu 22.04 and above, Debian 11 and above

### 2. Installation Steps

```bash
# 1. Clone the project
git clone https://github.com/Mgrsc/LLMQ-Horizon.git
cd LLMQ-Horizon

# 2. Prepare configuration files
cp config-tools.toml.example config-tools.toml
cp config.toml.example config.toml
cd napcat/config/
mv onebot11_qq.json onebot11_<your_QQ>.json  # Replace with your actual QQ number

# 3. Modify configurations (refer to the comments in the configuration files for modification)
vim config.toml
vim config-tools.toml

# 4. Start the service
docker compose up -d

# 5. Scan the QR code to log in
docker compose logs -f

# Restart the LLMQ service
docker compose restart llmq

# Stop all services
docker compose down
```

## 🛠️ Tool Configuration

<details>
<summary>💻 Code Execution (Code Runner - Judge0)</summary>

[Judge0 Official Deployment Tutorial](https://github.com/judge0/judge0/blob/master/CHANGELOG.md)

1.  **Prepare an environment with Ubuntu 22.04 or higher and Docker, and configure cgroup v1:**

    ```bash
    sudo sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"/' /etc/default/grub
    sudo update-grub
    sudo reboot
    ```

2.  **Deploy Judge0:**

    ```bash
    wget https://github.com/judge0/judge0/releases/download/v1.13.1/judge0-v1.13.1.zip
    unzip judge0-v1.13.1.zip
    cd judge0-v1.13.1

    # Generate two passwords and set the passwords
    openssl rand -hex 32

    # Use the generated passwords to update the REDIS_PASSWORD and POSTGRES_PASSWORD variables in the judge0.conf file.

    # Start the service
    docker-compose up -d db redis
    sleep 10s
    docker-compose up -d
    sleep 5s
    ```

    Your Judge0 CE v1.13.1 instance is now up and running; visit http://<your server IP address>:2358/docs for documentation.

3.  **Configure config-tools.toml:**

    ```toml
    [code_generation_running]
    judge0_url = "http://your-server:2358"
    judge0_api_key = "your-api-key"
    ```

</details>

<details>
<summary>😎 Memos (memos_manage - Memos)</summary>

[Memos Official Deployment Tutorial](https://www.usememos.com/docs/install/container-install)

1.  **Prepare an environment with Ubuntu 22.04 or higher and Docker:**

2.  **Create a docker-compose.yaml file**

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

3.  **Start memos**

    ```shell
    docker compose up -d
    ```

    You can now access memos at http://<your server IP address>:5230. Get the Tokens in the Settings of Memos.

4.  **Fill in the configuration file**

    ```toml
    [memos]
    url = "http://your-server:xxx"
    memos_token = "<fill in the obtained tokens>"
    default_visibility = "PRIVATE"
    page_size = 10
    user_id = 6
    ```

</details>

## 📝 Command Description

| Command                      | Description                                  |
| :--------------------------- | :------------------------------------------- |
| `/chat model <model name>`   | Switch the conversation model                |
| `/chat clear`               | Clear all conversations                       |
| `/chat group <true/false>`   | Turn on/off group chat isolation             |
| `/chat down`                | Turn off the chat function                   |
| `/chat up`                  | Turn on the chat function                    |
| `/chat chunk <true/false>`   | Turn on/off segmented message sending        |

## 🦊 Prompt Writing Tips

<details>
<summary>1. Basic Principles</summary>

-   Clear Instructions: Use imperative language to clearly state the user's needs, ensuring the LLM can understand accurately.
-   Provide Reference Examples/Text: Provide detailed examples and information to form a Few-shot-Prompt, helping the LLM strengthen its understanding of the intent.
-   Structured Expression: Use markup symbols (such as XML tags, triple quotes, Markdown) to enhance readability and make the prompt clear.
-   Output Control: Specify requirements for output format, language style, etc., to ensure the LLM generates output that meets user expectations.
-   Layout Optimization: Carefully arrange the layout of the Prompt for easy understanding by the LLM.
</details>
<details>
<summary>2. Other Tips</summary>

-   List available tools, and explain and request for complex tools
    ```
    create_speech generates speech
        - Maximum 40 characters, no emojis allowed
        - Supported languages: Chinese, English, Japanese, German, French, Spanish, Korean, Arabic, Russian, Dutch, Italian, Polish, Portuguese
        - Available voice mappings:
            Keli = keli
            Sigewinne = xigewen
            Yae Miko = shenzi
            Ding Zhen = dingzhen
            Lei Jun = leijun
            Lazy Sheep = lanyangyang
    ```
-   Require the tool to send back the file:// address
    ```
      Drawing, getting music, and tts must send the returned link or file path address to the user
    ```
-   Example of formatting tool return content
    ```
        # Example of optimizing the formatting of tool return content
      Example of formatting data returned by get_weather_data:
      * A: Tell me the weather in Changsha today
          T: Call tool `get_weather_data` to get the weather
          Q:
          🌤️ {Location} Weather
          🌅 Sunrise and Sunset: {xx:xx}-{xx:xx without year}
          ⏱️ Time: {Time}
          🌡️ Temperature: {Temperature}℃
          💧 Humidity: {Humidity}%
          🧣 Feels Like: {Feels Like}℃
          🍃 Wind Direction and Speed: {Wind Direction}-{Wind Speed}
          📋 Overall Situation: {Overall Analysis}
          Baby, remember to wear more clothes when going out~ Be careful not to catch a cold
    ```
</details>

## ❗ Common Issues

All tools have been tested. If you encounter problems, please refer to the following checks.

<details>
<summary>1. Login Failure</summary>

-   Check if the QQ number configuration is correct.
-   Confirm the napcat configuration file format.
-   View napcat container logs to troubleshoot the issue.

</details>

<details>
<summary>2. Tool Invocation Failure</summary>

-   Confirm that the model supports function calling capabilities.
-   Check the relevant API key configurations.
-   View LLMQ container logs to locate the error.
-   Add [LangSmith](https://smith.langchain.com/) to the docker container for debugging.

    ```yaml
    environment:
      - LANGCHAIN_TRACING_V2=true
      - LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
      - LANGCHAIN_API_KEY="<your_api_key>"
      - LANGCHAIN_PROJECT="<your_project_name>"
    ```

</details>

<details>
<summary>3. Other Issues</summary>

-   For other issues, please join the QQ group for discussion.
    ![qrcode](static/qrcode.jpg)

</details>

## 🔗 Related Projects

-   [NoneBot2](https://github.com/nonebot/nonebot2)
-   [LangGraph](https://github.com/langchain-ai/langgraph)
-   [LangChain](https://github.com/langchain-ai/langchain)
-   [Judge0](https://github.com/judge0/judge0)
-   [Memos](https://github.com/usememos/memos)
-  [NapCat](https://github.com/NapNeko/NapCatQQ)

## 📄 License

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=large&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_large&issueType=license)

This project is licensed under the [MIT License](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE).

Copyright © 2024 Bitfennec.

---