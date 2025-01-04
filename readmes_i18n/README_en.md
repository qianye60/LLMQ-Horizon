<div align="center">

<img src="static/LLMQ.webp" width="400" style="margin-bottom: 10px;">

# 🤖 LLMQ-Horizon QQ Chatbot

**An intelligent QQ chatbot based on NoneBot2 and LangGraph, supporting multi-model conversation, tool calling, and session management**

<br>

**Tools are all written using Function-calling, without using plugins, referring to [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) , [LangChain Tools](https://python.langchain.com/docs/how_to/#tools)**

<br>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_small)
[![Docker Release](https://img.shields.io/docker/pulls/bitfennec/llmq-horizon?color=%230077c8&label=Docker%20Pulls&logo=docker&logoColor=white&style=flat)](https://hub.docker.com/r/bitfennec/llmq-horizon)
[![License](https://img.shields.io/github/license/Mgrsc/LLMQ-Horizon?color=%2300c853&label=MIT%20License&style=flat)](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE)

</div>

---

## ✨ Key Features

-   **🔌 Rich Tool Integrations:** Code execution, weather query, divination, drawing, etc.
-   **🤖 Support for Multiple Large Models:** OpenAI, Google Gemini, Groq, etc.
-   **💬 Complete Conversation Management:** Group chat/private chat, multi-turn conversations, session isolation
-   **🎯 Flexible Trigger Methods:** @, keywords, command prefix
-   **🎨 Multimedia Capabilities:** Image analysis, audio and video processing
-   **⚡ Automatic Session Management:** Timeout cleanup, concurrency control
-   **🦖 Powerful Extensibility:** Ability to write custom tools, use tools to control NoneBot

---

## 🚀 Quick Start

### 1. Preparation of Deployment Environment

-   Docker and Docker Compose
-   Stable network environment
-   Recommended systems: Ubuntu 22.04 and above, Debian 11 and above

### 2. Installation Steps

```bash
# 1. Clone the project
git clone https://github.com/Mgrsc/LLMQ-Horizon.git
cd LLMQ-Horizon

# 2. Prepare configuration files
cp config-tools.toml.example config-tools.toml
cp config.toml.example config.toml
cd napcat/config/
mv onebot11_qq.json onebot11_<your_QQ_number>.json  # Replace with your actual QQ number

# 3. Modify the configuration (refer to the comments in the configuration file for modification)
vim config.toml
vim config-tools.toml

# 4. Start the service
docker compose up -d

# 5. Scan to log in
docker compose logs -f

# Restart LLMQ service
docker compose restart llmq

# Stop all services
docker compose down
```

## 🛠️ Tool Configuration

<details>
<summary>💻 Code Execution (Code Runner - Judge0)</summary>

[Judge0 Official Deployment Tutorial](https://github.com/judge0/judge0/blob/master/CHANGELOG.md)

1.  **Prepare an environment with Ubuntu 22.04 or above and Docker, configure cgroup v1:**

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

    # Generate two passwords and set passwords
    openssl rand -hex 32

    # Use the generated passwords to update the REDIS_PASSWORD and POSTGRES_PASSWORD variables in the judge0.conf file.

    # Start the service
    docker-compose up -d db redis
    sleep 10s
    docker-compose up -d
    sleep 5s
    ```

    Your Judge0 CE v1.13.1 instance is now up and running; access http://<your_server_IP_address>:2358/docs for documentation.

3.  **Configure config-tools.toml:**

    ```toml
    [code_runner]
    judge0_url = "http://your-server:2358"
    judge0_api_key = "your-api-key"
    ```

</details>

<details>
<summary>😎 Memos (memos_manage - Memos)</summary>

[Memos Official Deployment Tutorial](https://www.usememos.com/docs/install/container-install)

1.  **Prepare an environment with Ubuntu 22.04 or above and Docker:**

2.  **Write the docker-compose.yaml file**

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

3.  **Start Memos**

    ```shell
    docker compose up -d
    ```

    You can now access Memos at http://<your_server_IP_address>:5230. Get the Tokens in Settings within Memos.

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

| Command                      | Description                        |
| :--------------------------- | :--------------------------------- |
| `/chat model <model_name>`   | Switch conversation model         |
| `/chat clear`               | Clear all conversations            |
| `/chat group <true/false>`  | Toggle group chat isolation       |
| `/chat down`                | Disable chat feature             |
| `/chat up`                  | Enable chat feature                |
| `/chat chunk <true/false>`  | Toggle chunked message sending    |

## ❗ Common Issues

<details>
<summary>1. Login Failure</summary>

-   Check if the QQ number configuration is correct
-   Confirm the format of the napcat configuration file
-   View napcat container logs to troubleshoot

</details>

<details>
<summary>2. Tool Calling Failure</summary>

-   Confirm that the model supports function calling capabilities
-   Check relevant API key configurations
-   View LLMQ container logs to locate errors
-   Join [LangSmith](https://smith.langchain.com/) in the docker container for debugging

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

-   For other issues, please join the QQ group for discussion
    ![qrcode](static/qrcode.jpg)

</details>

## 🔗 Related Projects

-   [NoneBot2](https://github.com/nonebot/nonebot2)
-   [LangGraph](https://github.com/langchain-ai/langgraph)
-   [LangChain](https://github.com/langchain-ai/langchain)
-   [Judge0](https://github.com/judge0/judge0)
-   [Memos](https://github.com/usememos/memos)
-   [NapCat](https://github.com/NapNeko/NapCatQQ)

## 📄 License

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=large&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_large&issueType=license)

This project is licensed under the [MIT License](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE).

Copyright © 2024 Bitfennec.

---