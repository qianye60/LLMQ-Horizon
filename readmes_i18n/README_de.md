<div align="center">

<img src="static/LLMQ.webp" width="400" style="margin-bottom: 10px;">

# 🤖 LLMQ-Horizon QQ Chatbot

**Intelligenter QQ-Bot basierend auf NoneBot2 und LangGraph, unterstützt Multimodell-Dialoge, Tool-Aufrufe und Sitzungsmanagement**

<br>

**Tools sind alle mit Function-Calling geschrieben, verwenden keine Plugins, siehe [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) , [LangChain Tools](https://python.langchain.com/docs/how_to/#tools)**

<br>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_small)
[![Docker Release](https://img.shields.io/docker/pulls/bitfennec/llmq-horizon?color=%230077c8&label=Docker%20Pulls&logo=docker&logoColor=white&style=flat)](https://hub.docker.com/r/bitfennec/llmq-horizon)
[![License](https://img.shields.io/github/license/Mgrsc/LLMQ-Horizon?color=%2300c853&label=MIT%20License&style=flat)](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE)

<br>

[English](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_en.md) | [Deutsch](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_de.md) | [Español](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_es.md) | [Français](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_fr.md) | [日本語](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_ja.md)

</div>

---

## ✨ Hauptmerkmale

-   **🔌 Umfangreiche Tool-Integration:** Codeausführung, Wetterabfrage, Wahrsagerei, Zeichnen usw.
-   **🤖 Unterstützung für verschiedene große Modelle:** OpenAI, Google Gemini, Groq usw.
-   **💬 Umfangreiches Dialogmanagement:** Gruppenchat/Privatchat, mehrfache Dialoge, Sitzungsisolation
-   **🎯 Flexible Auslösemethoden:** @, Schlüsselwörter, Befehlspräfix
-   **🎨 Multimedia-Fähigkeiten:** Bildanalyse, Audio- und Videoverarbeitung
-   **⚡ Automatische Sitzungsverwaltung:** Zeitüberschreitungsbereinigung, Parallelitätskontrolle
-   **🦖 Starke Erweiterbarkeit:** Eigene Tools können geschrieben werden, Tools können nonebot steuern

---

## 🚀 Schnellstart

### 1. Umgebungsvorbereitung für die Bereitstellung

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
mv onebot11_qq.json onebot11_<deineQQ>.json  # Durch tatsächliche QQ-Nummer ersetzen

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

[Judge0 Offizielle Bereitstellungsanleitung](https://github.com/judge0/judge0/blob/master/CHANGELOG.md)

1. **Ubuntu 22.04 oder höhere Umgebung und Docker vorbereiten, cgroup v1 konfigurieren:**

    ```bash
    sudo sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"/' /etc/default/grub
    sudo update-grub
    sudo reboot
    ```

2. **Judge0 bereitstellen:**

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

    Ihre Judge0 CE v1.13.1-Instanz ist jetzt gestartet und läuft; besuchen Sie http://<Ihre Server-IP-Adresse>:2358/docs, um die Dokumentation zu erhalten.

3. **config-tools.toml konfigurieren:**

    ```toml
    [code_generation_running]
    judge0_url = "http://your-server:2358"
    judge0_api_key = "your-api-key"
    ```

</details>

<details>
<summary>😎 Notizen (memos_manage - Memos)</summary>

[Memos Offizielle Bereitstellungsanleitung](https://www.usememos.com/docs/install/container-install)

1. **Ubuntu 22.04 oder höhere Umgebung und Docker vorbereiten:**

2. **docker-compose.yaml-Datei erstellen**

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

    Sie können nun unter http://<Ihre Server-IP-Adresse>:5230 auf Memos zugreifen und die Token in den Einstellungen von Memos abrufen.

4. **Konfigurationsdatei ausfüllen**

    ```toml
    [memos]
    url = "http://your-server:xxx"
    memos_token = "<füge die abgerufenen Token ein>"
    default_visibility = "PRIVATE"
    page_size = 10
    user_id = 6
    ```

</details>

## 📝 Befehlsbeschreibung

| Befehl                      | Beschreibung                                |
| :------------------------ | :------------------------------------------ |
| `/chat model <Modellname>`   | Dialogmodell wechseln                         |
| `/chat clear`             | Alle Sitzungen löschen                       |
| `/chat group <true/false>` | Gruppenchat-Isolation ein-/ausschalten      |
| `/chat down`              | Dialogfunktion deaktivieren                  |
| `/chat up`                | Dialogfunktion aktivieren                    |
| `/chat chunk <true/false>` | Aktivieren/Deaktivieren von Nachrichten in Teilstücken |


## 🦊 Tipps zur Prompt-Erstellung

<details>
<summary>1. Grundprinzipien</summary>

-   Klare Anweisungen: Verwenden Sie eine imperative Sprache, um die Bedürfnisse der Benutzer klar zu formulieren und sicherzustellen, dass LLM sie präzise versteht.
-   Referenzbeispiele/Text bereitstellen: Geben Sie detaillierte Beispiele und Informationen, um einen Few-Shot-Prompt zu erstellen, der LLM hilft, das Verständnis der Absicht zu verbessern.
-   Strukturierter Ausdruck: Verwenden Sie Markierungssymbole (wie XML-Tags, dreifache Anführungszeichen, Markdown), um die Lesbarkeit zu verbessern und Prompts klarer auszudrücken.
-   Ausgabesteuerung: Legen Sie Ausgabeformate, Sprachstile und andere Anforderungen fest, um sicherzustellen, dass LLM eine Ausgabe generiert, die den Erwartungen der Benutzer entspricht.
-   Layoutoptimierung: Ordnen Sie das Layout des Prompts sorgfältig an, um das Verständnis von LLM zu erleichtern.
</details>
<details>
<summary>2. Andere Tipps</summary>

-   Listen Sie die verfügbaren Tools auf und geben Sie Erklärungen und Anforderungen für komplexe Tools an.
  ```
  create_speech generiert Sprache
    - maximal 40 Wörter, keine Emojis erlaubt
    - Unterstützte Sprachen: Chinesisch, Englisch, Japanisch, Deutsch, Französisch, Spanisch, Koreanisch, Arabisch, Russisch, Niederländisch, Italienisch, Polnisch, Portugiesisch
    - Verfügbare Stimmzuordnungen:
        Klee = keli
        Sigewen = xigewen
        Yae Miko = shenzi
        Ding Zhen = dingzhen
        Lei Jun = leijun
        Lazy Goat = lanyangyang
  ```
-   Fordern Sie die Zusendung der von Tool zurückgegebenen file://-Adresse an.
  ```
    Das Zeichnen, der Abruf von Musik und TTS müssen die zurückgegebenen Links oder Dateipfade an den Benutzer senden.
  ```
-   Beispiel für die Formatierung des von Tool zurückgegebenen Inhalts
  ```
      # Beispiel für die Formatierungsoptimierung von Tool-Rückgabeinhalten
    Beispiel für das Format der von get_weather_data zurückgegebenen Daten:
    *   A: Sag mir, wie das Wetter heute in Changsha ist
        T: Ruft das Tool `get_weather_data` ab, um das Wetter abzurufen
        Q:
        🌤️ {Ort} Wetter
        🌅 Sonnenaufgang und Sonnenuntergang: {xx:xx}-{xx:xx ohne Jahr}
        ⏱️   Zeit: {Zeit}
        🌡️ Temperatur: {Temperatur}℃
        💧 Luftfeuchtigkeit: {Luftfeuchtigkeit}%
        🧣 Gefühlte Temperatur: {Gefühlte Temperatur}℃
        🍃 Windrichtung und Windgeschwindigkeit: {Windrichtung}-{Windgeschwindigkeit}
        📋 Gesamtstatus: {Gesamtanalyse}
        Baby, zieh dich warm an, wenn du ausgehst~ sei vorsichtig vor einer Erkältung
  ```
</details>

## ❗ Häufige Fragen

Alle Tools wurden getestet. Wenn es Probleme gibt, beziehen Sie sich bitte auf die folgenden Überprüfungen.

<details>
<summary>1. Anmeldefehler</summary>

-   Überprüfen Sie, ob die QQ-Nummernkonfiguration korrekt ist.
-   Bestätigen Sie das Format der napcat-Konfigurationsdatei.
-   Überprüfen Sie die napcat-Containerprotokolle, um das Problem zu beheben.

</details>

<details>
<summary>2. Tool-Aufruf fehlgeschlagen</summary>

-   Bestätigen Sie, dass das Modell die Funktion zum Aufrufen von Funktionen unterstützt.
-   Überprüfen Sie die zugehörigen API-Schlüsselkonfigurationen.
-   Überprüfen Sie die LLMQ-Containerprotokolle, um den Fehler zu lokalisieren.
-   Fügen Sie [LangSmith](https://smith.langchain.com/) im Docker-Container hinzu, um zu debuggen.

    ```yaml
    environment:
      - LANGCHAIN_TRACING_V2=true
      - LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
      - LANGCHAIN_API_KEY="<dein_api_schlüssel>"
      - LANGCHAIN_PROJECT="<dein_projektname>"
    ```

</details>

<details>
<summary>3. Andere Probleme</summary>

-   Bei anderen Problemen treten Sie bitte der QQ-Gruppe zur Diskussion bei.
    ![qrcode](static/qrcode.jpg)

</details>

## 🔗 Zugehörige Projekte

-   [NoneBot2](https://github.com/nonebot/nonebot2)
-   [LangGraph](https://github.com/langchain-ai/langgraph)
-   [LangChain](https://github.com/langchain-ai/langchain)
-   [Judge0](https://github.com/judge0/judge0)
-   [Memos](https://github.com/usememos/memos)
-   [NapCat](https://github.com/NapNeko/NapCatQQ)

## 📄 Lizenz

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=large&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_large&issueType=license)

Dieses Projekt ist unter der [MIT-Lizenz](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE) lizenziert.

Copyright © 2024 Bitfennec.

---