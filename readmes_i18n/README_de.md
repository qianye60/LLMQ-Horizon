<div align="center">

<img src="static/LLMQ.webp" width="400" style="margin-bottom: 10px;">

# 🤖 LLMQ-Horizon QQ Chatbot

**Intelligenter QQ-Bot basierend auf NoneBot2 und LangGraph, unterstützt Mehrfachmodell-Dialoge, Tool-Aufrufe und Sitzungsverwaltung**

<br>

**Die Tools sind alle mit Function-calling geschrieben, ohne Plugins, siehe [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) , [LangChain Tools](https://python.langchain.com/docs/how_to/#tools)**

<br>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_small)
[![Docker Release](https://img.shields.io/docker/pulls/bitfennec/llmq-horizon?color=%230077c8&label=Docker%20Pulls&logo=docker&logoColor=white&style=flat)](https://hub.docker.com/r/bitfennec/llmq-horizon)
[![License](https://img.shields.io/github/license/Mgrsc/LLMQ-Horizon?color=%2300c853&label=MIT%20License&style=flat)](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE)

<br>

[English](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_en.md) | [Deutsch](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_de.md) | [Español](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_es.md) | [Français](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_fr.md) | [日本語](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_ja.md)

</div>

---

## ✨ Hauptmerkmale

-   **🔌 Umfangreiche Tool-Integration:** Codeausführung, Wetterabfrage, Wahrsagerei, Malen usw.
-   **🤖 Unterstützung mehrerer großer Modelle:** OpenAI, Google Gemini, Groq usw.
-   **💬 Ausgereiftes Dialogmanagement:** Gruppenchat/Privatchat, Mehrfachdialoge, Sitzungsisolierung
-   **🎯 Flexible Auslösemethoden:** @, Schlüsselwörter, Befehlspräfix
-   **🎨 Multimedia-Fähigkeiten:** Bildanalyse, Audio- und Videoverarbeitung
-   **⚡ Automatische Sitzungsverwaltung:** Timeout-Bereinigung, Parallelitätskontrolle
-   **🦖 Starke Erweiterbarkeit:** Eigene Tools können geschrieben werden, Tools können verwendet werden, um nonebot zu steuern

---

## 🚀 Schnellstart

### 1. Vorbereitung der Einsatzumgebung

-   Docker und Docker Compose
-   Stabile Netzwerkumgebung
-   Empfohlenes System: Ubuntu 22.04 und höher, Debian 11 und höher

> Hinweis: Wenn Sie das Deepseek-Modell mit Tools verwenden, sollten Sie nicht mehr als 5 Tools aktivieren und die Eingabeaufforderungen so kurz wie möglich halten, da DS sonst Tools unaufhörlich aufruft und Sie damit überflutet, oder gar keine Tools aufruft und nur so tut als ob.

### 2. Installationsschritte

```bash
# 1. Projekt klonen
git clone https://github.com/Mgrsc/LLMQ-Horizon.git
cd LLMQ-Horizon

# 2. Konfigurationsdateien vorbereiten
cp config-tools.toml.example config-tools.toml
cp config.toml.example config.toml
cd napcat/config/
mv onebot11_qq.json onebot11_<Ihre QQ>.json  # Durch tatsächliche QQ-Nummer ersetzen

# 3. Konfiguration ändern (siehe Kommentare in den Konfigurationsdateien)
vim config.toml
vim config-tools.toml

# 4. Dienst starten
docker compose up -d

# 5. QR-Code scannen zum Anmelden
docker compose logs -f

# LLMQ-Dienst neu starten
docker compose restart llmq

# Alle Dienste beenden
docker compose down
```

## 🛠️ Tool-Konfiguration

<details>
<summary>💻 Codeausführung (Code Runner - Judge0)</summary>

[Offizielle Judge0-Bereitstellungsanleitung](https://github.com/judge0/judge0/blob/master/CHANGELOG.md)

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

    Ihre Judge0 CE v1.13.1 Instanz ist jetzt gestartet und läuft; Zugriff auf die Dokumentation erhalten Sie unter http://<Ihre Server-IP-Adresse>:2358/docs.

3. **config-tools.toml konfigurieren:**

    ```toml
    [code_generation_running]
    judge0_url = "http://your-server:2358"
    judge0_api_key = "your-api-key"
    ```

</details>

<details>
<summary>📝 Memo (memos_manage - Memos)</summary>

[Offizielle Memos-Bereitstellungsanleitung](https://www.usememos.com/docs/install/container-install)

1. **Umgebung vorbereiten:**
   - Ubuntu 22.04 und höher
   - Docker und Docker Compose

2. **docker-compose.yaml-Datei schreiben**

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

3. **Dienst starten:**
```bash
docker compose up -d
```

Jetzt können Sie unter http://<Ihre Server-IP-Adresse>:5230 auf Memos zugreifen und in den Einstellungen von Memos Tokens erhalten.

4. **config-tools.toml konfigurieren:**

```toml
[memos_manage]
url = "http://your-server:5230"
memos_token = "your-memos-token"  # Token von der Einstellungsseite
default_visibility = "PRIVATE"
page_size = 10
user_id = 6
```
</details>

<details>
<summary>📰 Nachrichtenerfassung (get_news - SynapseNews)</summary>

[SynapseNews Projektadresse](https://github.com/Mgrsc/SynapseNews)

1. **Bereitstellungsschritte:**
```bash
git clone https://github.com/Mgrsc/SynapseNews.git
cd synapsenews
# Konfigurieren von config.toml
docker compose up -d
```
</details>

## 📝 Befehlsbeschreibung

| Befehl                      | Beschreibung                             |
| :------------------------ | :--------------------------------------- |
| `/chat model <Modellname>`   | Dialogmodell wechseln                    |
| `/chat clear`             | Alle Sitzungen löschen                    |
| `/chat group <true/false>` | Gruppenchat-Isolierung ein-/ausschalten |
| `/chat down`              | Dialogfunktion deaktivieren               |
| `/chat up`                | Dialogfunktion aktivieren                |
| `/chat chunk <true/false>` | Segmentweises Senden ein-/ausschalten     |

## 🦊 Tipps zum Schreiben von Prompts

<details>
<summary>1. Grundprinzipien</summary>

- Klare Anweisungen: Verwenden Sie eine imperative Sprache, um die Bedürfnisse des Benutzers klar zu formulieren und sicherzustellen, dass das LLM sie genau versteht.
- Geben Sie Referenzbeispiele/-texte an: Stellen Sie detaillierte Beispiele und Informationen bereit, um einen Few-Shot-Prompt zu erstellen, der dem LLM hilft, das Konzept besser zu verstehen.
- Strukturierte Ausdrücke: Verwenden Sie Markierungssymbole (z. B. XML-Tags, dreifache Anführungszeichen, Markdown), um die Lesbarkeit zu verbessern und die Prompts klar auszudrücken.
- Ausgabesteuerung: Legen Sie Ausgabeformate, Sprachstile und andere Anforderungen fest, um sicherzustellen, dass das LLM eine Ausgabe generiert, die den Erwartungen des Benutzers entspricht.
- Layout-Optimierung: Ordnen Sie das Layout des Prompts sorgfältig an, um das Verständnis des LLM zu erleichtern.
</details>

<details>
<summary>2. Weitere Tipps</summary>

- Listen Sie verfügbare Tools auf und erläutern und fordern Sie komplexe Tools an
  ```
  create_speech generiert Sprache
    - Maximal 40 Zeichen, keine Emojis erlaubt
    - Unterstützte Sprachen: Chinesisch, Englisch, Japanisch, Deutsch, Französisch, Spanisch, Koreanisch, Arabisch, Russisch, Niederländisch, Italienisch, Polnisch, Portugiesisch
    - Verfügbare Stimmenzuordnungen:
        Klee = keli
        Sigewinne = xigewen
        Yae Miko = shenzi
        Ding Zhen = dingzhen
        Lei Jun = leijun
        Lazy Sheep = lanyangyang
  ```
- Fordern Sie an, die von Tools zurückgegebenen file://-Adressen zu senden
  ```
    Das Zeichnen, Abrufen von Musik und TTS müssen den zurückgegebenen Link oder den Dateipfad an den Benutzer senden
  ```
- Beispiel für das Layout der von Tools zurückgegebenen Inhalte
  ```
      # Beispiel für die Layoutoptimierung der von Tools zurückgegebenen Inhalte
    Beispiel für die Formatierung der von get_weather_data zurückgegebenen Daten:
    *   A: Sag mir, wie das Wetter heute in Changsha ist
        T: Rufe das Tool `get_weather_data` auf, um das Wetter abzurufen
        Q:
        🌤️ Wetter in {Ort}
        🌅 Sonnenaufgang und Sonnenuntergang: {xx:xx}-{xx:xx ohne Jahr}
        ⏱️   Uhrzeit: {Zeit}
        🌡️ Temperatur: {Temperatur}℃
        💧 Luftfeuchtigkeit: {Luftfeuchtigkeit}%
        🧣 Gefühlte Temperatur: {Gefühlte Temperatur}℃
        🍃 Windrichtung und -geschwindigkeit: {Windrichtung}-{Windgeschwindigkeit}
        📋 Gesamtsituation: {Gesamtanalyse}
        Baby, zieh dich warm an, wenn du rausgehst~ Pass auf, dass du dich nicht erkältest
  ```
</details>

## 🤝 Leitfaden für Beiträge

1. Forken Sie dieses Repository
2. Erstellen Sie Ihren Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Übernehmen Sie Ihre Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Pushen Sie zum Branch (`git push origin feature/AmazingFeature`)
5. Öffnen Sie eine Pull-Anfrage

## 🤖 Häufig gestellte Fragen
Alle Tools wurden getestet, überprüfen Sie bitte Folgendes, wenn Sie Probleme haben.

<details>
<summary>1. Anmeldung fehlgeschlagen</summary>

-   Überprüfen Sie, ob die QQ-Nummer korrekt konfiguriert ist
-   Bestätigen Sie das Format der napcat-Konfigurationsdatei
-   Überprüfen Sie die napcat-Containerprotokolle, um das Problem zu beheben

</details>

<details>
<summary>2. Toolaufruf fehlgeschlagen</summary>

-   Bestätigen Sie, dass das Modell die Fähigkeit zum Funktionsaufruf unterstützt
-   Überprüfen Sie die Konfiguration der zugehörigen API-Schlüssel
-   Überprüfen Sie die LLMQ-Containerprotokolle, um Fehler zu lokalisieren
-   Fügen Sie [LangSmith](https://smith.langchain.com/) im Docker-Container zum Debuggen hinzu

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
Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) Datei für Details.
Copyright © 2024 Bitfennec.
---
</div>