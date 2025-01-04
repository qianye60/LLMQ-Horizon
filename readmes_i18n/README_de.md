<div align="center">

<img src="static/LLMQ.webp" width="400" style="margin-bottom: 10px;">

# 🤖 LLMQ-Horizon QQ Chatbot

**Intelligenter QQ-Bot, basierend auf NoneBot2 und LangGraph, der Mehrfachmodell-Dialoge, Tool-Aufrufe und Sitzungsmanagement unterstützt**

<br>

**Alle Tools sind mit Function-calling geschrieben, keine Plugins werden verwendet, siehe [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) , [LangChain Tools](https://python.langchain.com/docs/how_to/#tools)**

<br>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_small)
[![Docker Release](https://img.shields.io/docker/pulls/bitfennec/llmq-horizon?color=%230077c8&label=Docker%20Pulls&logo=docker&logoColor=white&style=flat)](https://hub.docker.com/r/bitfennec/llmq-horizon)
[![License](https://img.shields.io/github/license/Mgrsc/LLMQ-Horizon?color=%2300c853&label=MIT%20License&style=flat)](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE)

</div>

---

## ✨ Hauptmerkmale

-   **🔌 Umfangreiche Tool-Integration:** Codeausführung, Wetterabfrage, Wahrsagerei, Malen usw.
-   **🤖 Unterstützung mehrerer großer Modelle:** OpenAI, Google Gemini, Groq usw.
-   **💬 Umfassendes Dialogmanagement:** Gruppenchat/Privatchat, Mehrfachdialoge, Sitzungsisolation
-   **🎯 Flexible Auslösemethoden:** @, Keywords, Befehlspräfixe
-   **🎨 Multimedia-Fähigkeiten:** Bildanalyse, Audio- und Videoverarbeitung
-   **⚡ Automatisches Sitzungsmanagement:** Zeitüberschreitungsbereinigung, Parallelitätskontrolle
-   **🦖 Starke Erweiterbarkeit:** Eigene Tools können geschrieben werden, Tools können verwendet werden, um Nonebot zu steuern

---

## 🚀 Schnellstart

### 1. Vorbereitung der Einsatzumgebung

-   Docker und Docker Compose
-   Stabile Netzwerkumgebung
-   Empfohlenes System: Ubuntu 22.04 und höher, Debian 11 und höher

### 2. Installationsschritte

```bash
# 1. Projekt klonen
git clone https://github.com/Mgrsc/LLMQ-Horizon.git
cd LLMQ-Horizon

# 2. Konfigurationsdateien vorbereiten
cp config-tools.toml.example config-tools.toml
cp config.toml.example config.toml
cd napcat/config/
mv onebot11_qq.json onebot11_<DeineQQ>.json  # Durch tatsächliche QQ-Nummer ersetzen

# 3. Konfiguration ändern (siehe Kommentare in den Konfigurationsdateien)
vim config.toml
vim config-tools.toml

# 4. Dienst starten
docker compose up -d

# 5. QR-Code scannen und anmelden
docker compose logs -f

# LLMQ-Dienst neu starten
docker compose restart llmq

# Alle Dienste stoppen
docker compose down
```

## 🛠️ Tool-Konfiguration

<details>
<summary>💻 Codeausführung (Code Runner - Judge0)</summary>

[Judge0 Offizielle Einsatzanleitung](https://github.com/judge0/judge0/blob/master/CHANGELOG.md)

1. **Ubuntu 22.04 oder höhere Umgebung und Docker vorbereiten, cgroup v1 konfigurieren:**

    ```bash
    sudo sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"/' /etc/default/grub
    sudo update-grub
    sudo reboot
    ```

2. **Judge0 einsetzen:**

    ```bash
    wget https://github.com/judge0/judge0/releases/download/v1.13.1/judge0-v1.13.1.zip
    unzip judge0-v1.13.1.zip
    cd judge0-v1.13.1

    # Zwei Passwörter generieren und Passwörter setzen
    openssl rand -hex 32

    # Verwenden Sie die generierten Passwörter, um die Variablen REDIS_PASSWORD und POSTGRES_PASSWORD in der Datei judge0.conf zu aktualisieren.

    # Dienst starten
    docker-compose up -d db redis
    sleep 10s
    docker-compose up -d
    sleep 5s
    ```

    Ihre Judge0 CE v1.13.1-Instanz ist jetzt gestartet und läuft; besuchen Sie http://<Ihre Server-IP-Adresse>:2358/docs für die Dokumentation.

3. **Konfigurieren Sie config-tools.toml:**

    ```toml
    [code_runner]
    judge0_url = "http://your-server:2358"
    judge0_api_key = "your-api-key"
    ```

</details>

<details>
<summary>😎 Memo (memos_manage - Memos)</summary>

[Memos Offizielle Einsatzanleitung](https://www.usememos.com/docs/install/container-install)

1. **Ubuntu 22.04 oder höhere Umgebung und Docker vorbereiten:**

2. **docker-compose.yaml Datei schreiben**

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

3. **Memos starten**

    ```shell
    docker compose up -d
    ```

    Jetzt können Sie Memos unter http://<Ihre Server-IP-Adresse>:5230 besuchen und Tokens in den Einstellungen von Memos abrufen.

4. **Konfigurationsdatei ausfüllen**

    ```toml
    [memos]
    url = "http://your-server:xxx"
    memos_token = "<Geben Sie die abgerufenen Token ein>"
    default_visibility = "PRIVATE"
    page_size = 10
    user_id = 6
    ```

</details>

## 📝 Befehlsbeschreibung

| Befehl                      | Beschreibung                                 |
| :-------------------------- | :------------------------------------------- |
| `/chat model <Modellname>`   | Dialogmodell wechseln                         |
| `/chat clear`               | Alle Sitzungen löschen                       |
| `/chat group <true/false>`  | Gruppenchat-Isolation ein-/ausschalten      |
| `/chat down`                | Dialogfunktion deaktivieren                  |
| `/chat up`                  | Dialogfunktion aktivieren                    |
| `/chat chunk <true/false>` | Abschnittsweises Senden ein-/ausschalten |

## ❗ Häufige Fragen

<details>
<summary>1. Anmeldung fehlgeschlagen</summary>

-   Überprüfen Sie, ob die QQ-Nummer korrekt konfiguriert ist
-   Bestätigen Sie das napcat-Konfigurationsdateiformat
-   Überprüfen Sie die napcat-Containerprotokolle zur Fehlerbehebung

</details>

<details>
<summary>2. Tool-Aufruf fehlgeschlagen</summary>

-   Bestätigen Sie, dass das Modell die Funktion zum Funktionsaufruf unterstützt
-   Überprüfen Sie die zugehörigen API-Schlüsselkonfigurationen
-   Überprüfen Sie die LLMQ-Containerprotokolle, um den Fehler zu lokalisieren
-   Fügen Sie [LangSmith](https://smith.langchain.com/) zum Debuggen in den Docker-Container ein

    ```yaml
    environment:
      - LANGCHAIN_TRACING_V2=true
      - LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
      - LANGCHAIN_API_KEY="<your_api_key>"
      - LANGCHAIN_PROJECT="<your_project_name>"
    ```

</details>

<details>
<summary>3. Andere Probleme</summary>

-   Bei anderen Problemen treten Sie bitte der QQ-Gruppe zur Diskussion bei
    ![qrcode](static/qrcode.jpg)

</details>

## 🔗 Verwandte Projekte

-   [NoneBot2](https://github.com/nonebot/nonebot2)
-   [LangGraph](https://github.com/langchain-ai/langgraph)
-   [LangChain](https://github.com/langchain-ai/langchain)
-   [Judge0](https://github.com/judge0/judge0)
-   [Memos](https://github.com/usememos/memos)
-   [NapCat](https://github.com/NapNeko/NapCatQQ)

## 📄 Lizenz

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=large&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_large&issueType=license)

Dieses Projekt verwendet die [MIT-Lizenz](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE).

Copyright © 2024 Bitfennec.

---