<div align="center">

<img src="static/LLMQ.webp" width="400" style="margin-bottom: 10px;">

# 🤖 LLMQ-Horizon Robot de Chat QQ

**Robot QQ intelligent basé sur NoneBot2 et LangGraph, prenant en charge les conversations multi-modèles, l'appel d'outils et la gestion de sessions**

<br>

**Les outils sont tous écrits en utilisant Function-calling, sans utiliser de plugins, en référence à [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) , [LangChain Tools](https://python.langchain.com/docs/how_to/#tools)**

<br>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_small)
[![Docker Release](https://img.shields.io/docker/pulls/bitfennec/llmq-horizon?color=%230077c8&label=Docker%20Pulls&logo=docker&logoColor=white&style=flat)](https://hub.docker.com/r/bitfennec/llmq-horizon)
[![License](https://img.shields.io/github/license/Mgrsc/LLMQ-Horizon?color=%2300c853&label=MIT%20License&style=flat)](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE)

<br>

[English](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_en.md) | [Deutsch](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_de.md) | [Español](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_es.md) | [Français](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_fr.md) | [日本語](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_ja.md)

</div>

---

## ✨ Caractéristiques principales

-   **🔌 Intégration d'outils riches :** exécution de code, prévisions météorologiques, divination, dessin, etc.
-   **🤖 Prise en charge de plusieurs grands modèles :** OpenAI, Google Gemini, Groq, etc.
-   **💬 Gestion complète des conversations :** discussions de groupe/privées, conversations à plusieurs tours, isolation des sessions
-   **🎯 Méthodes de déclenchement flexibles :** @, mots-clés, préfixes de commandes
-   **🎨 Capacités multimédias :** analyse d'images, traitement audio et vidéo
-   **⚡ Gestion automatique des sessions :** nettoyage des délais d'attente, contrôle de la concurrence
-   **🦖 Forte capacité d'extension :** possibilité d'écrire ses propres outils, possibilité d'utiliser des outils pour contrôler nonebot

---

## 🚀 Démarrage rapide

### 1. Préparation de l'environnement de déploiement

-   Docker et Docker Compose
-   Environnement réseau stable
-   Systèmes recommandés : Ubuntu 22.04 et versions ultérieures, Debian 11 et versions ultérieures

### 2. Étapes d'installation

```bash
# 1. Cloner le projet
git clone https://github.com/Mgrsc/LLMQ-Horizon.git
cd LLMQ-Horizon

# 2. Préparer les fichiers de configuration
cp config-tools.toml.example config-tools.toml
cp config.toml.example config.toml
cd napcat/config/
mv onebot11_qq.json onebot11_<votre_QQ>.json  # Remplacer par votre numéro QQ réel

# 3. Modifier la configuration (se référer aux commentaires dans les fichiers de configuration pour effectuer les modifications)
vim config.toml
vim config-tools.toml

# 4. Démarrer les services
docker compose up -d

# 5. Scanner le code pour se connecter
docker compose logs -f

# Redémarrer le service LLMQ
docker compose restart llmq

# Arrêter tous les services
docker compose down
```

## 🛠️ Configuration des outils

<details>
<summary>💻 Exécution de code (Code Runner - Judge0)</summary>

[Tutoriel de déploiement officiel de Judge0](https://github.com/judge0/judge0/blob/master/CHANGELOG.md)

1. **Préparer un environnement Ubuntu 22.04 ou supérieur et Docker, configurer cgroup v1 :**

    ```bash
    sudo sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"/' /etc/default/grub
    sudo update-grub
    sudo reboot
    ```

2. **Déployer Judge0 :**

    ```bash
    wget https://github.com/judge0/judge0/releases/download/v1.13.1/judge0-v1.13.1.zip
    unzip judge0-v1.13.1.zip
    cd judge0-v1.13.1

    # Générer deux mots de passe et les définir
    openssl rand -hex 32

    # Utiliser les mots de passe générés pour mettre à jour les variables REDIS_PASSWORD et POSTGRES_PASSWORD dans le fichier judge0.conf.

    # Démarrer les services
    docker-compose up -d db redis
    sleep 10s
    docker-compose up -d
    sleep 5s
    ```

    Votre instance Judge0 CE v1.13.1 est maintenant démarrée et en cours d’exécution ; consultez la documentation à l’adresse http://<votre_adresse_IP_de_serveur>:2358/docs.

3. **Configurer config-tools.toml :**

    ```toml
    [code_generation_running]
    judge0_url = "http://votre-serveur:2358"
    judge0_api_key = "votre-clé-api"
    ```

</details>

<details>
<summary>😎 Mémos (memos_manage - Memos)</summary>

[Tutoriel de déploiement officiel de Memos](https://www.usememos.com/docs/install/container-install)

1. **Préparer un environnement Ubuntu 22.04 ou supérieur et Docker :**

2. **Écrire un fichier docker-compose.yaml**

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

3. **Démarrer Memos**

    ```shell
    docker compose up -d
    ```

    Vous pouvez maintenant accéder à Memos sur http://<votre_adresse_IP_de_serveur>:5230, et obtenir des Tokens dans les Paramètres de Memos

4. **Remplir le fichier de configuration**

    ```toml
    [memos]
    url = "http://votre-serveur:xxx"
    memos_token = "<entrer les tokens obtenus>"
    default_visibility = "PRIVATE"
    page_size = 10
    user_id = 6
    ```

</details>

## 📝 Explication des commandes

| Commande                      | Explication                             |
| :------------------------ | :------------------------------- |
| `/chat model <nom_du_modèle>`   | Changer de modèle de conversation                     |
| `/chat clear`             | Effacer toutes les sessions                     |
| `/chat group <true/false>` | Activer/désactiver l'isolation des discussions de groupe                     |
| `/chat down`              | Désactiver la fonction de conversation                     |
| `/chat up`                | Activer la fonction de conversation                    |
| `/chat chunk <true/false>` | Activer/désactiver l'envoi par segments                    |

## 🦊 Astuces pour la rédaction de prompts

<details>
<summary>1. Principes de base</summary>

-   Instructions claires : Utiliser un langage impératif pour énoncer clairement les besoins de l'utilisateur, en s'assurant que le LLM peut comprendre avec précision.
-   Fournir des exemples/textes de référence : Fournir des exemples et des informations détaillés, en constituant un Few-shot-Prompt pour aider le LLM à renforcer sa compréhension de l'intention.
-   Expression structurée : Utiliser des symboles de marquage (tels que des balises XML, des triples guillemets, Markdown) pour améliorer la lisibilité, afin que l'expression du prompt soit claire.
-   Contrôle de la sortie : Spécifier le format de sortie, le style de langage et d'autres exigences pour s'assurer que le LLM génère une sortie qui répond aux attentes de l'utilisateur.
-   Optimisation de la mise en page : Organiser soigneusement la mise en page du Prompt pour faciliter sa compréhension par le LLM.
</details>
<details>
<summary>2. Autres astuces</summary>

-   Lister les outils disponibles, avec une explication et des exigences pour les outils complexes
  ```
  create_speech générer de la parole
    - 40 caractères maximum, pas d'emojis
    - Langues prises en charge : chinois, anglais, japonais, allemand, français, espagnol, coréen, arabe, russe, néerlandais, italien, polonais, portugais
    - Mappage de tonalités disponible :
        可莉 = keli
        西格雯 = xigewen
        神子 = shenzi
        丁真 = dingzhen
        雷军 = leijun
        懒羊羊 = lanyangyang
  ```
- Exiger l'envoi de l'adresse file:// renvoyée par l'outil
  ```
  Le dessin, l'obtention de musique et le tts doivent envoyer le lien renvoyé ou l'adresse du chemin du fichier à l'utilisateur
  ```
- Exemple de mise en page du contenu renvoyé par l'outil
  ```
      # Exemple d'optimisation de la mise en page du contenu renvoyé par l'outil
    Exemple de formatage des données renvoyées par get_weather_data :
    *   A : Indiquez-moi la météo à Changsha aujourd'hui
        T : Appel de l'outil `get_weather_data` pour obtenir la météo
        Q :
        🌤️ Météo à {lieu}
        🌅 Lever et coucher du soleil : {xx:xx}-{xx:xx, sans l'année}
        ⏱️   Heure : {Heure}
        🌡️ Température : {Température} °C
        💧 Humidité : {Humidité} %
        🧣 Température ressentie : {Température ressentie} °C
        🍃 Direction et vitesse du vent : {Direction du vent}-{Vitesse du vent}
        📋 Situation globale : {Analyse globale}
        Bébé, couvre-toi bien en sortant~ Fais attention à ne pas attraper froid
  ```
</details>

## ❗ Questions fréquentes

Tous les outils ont été testés, veuillez vous référer aux informations ci-dessous en cas de problème.

<details>
<summary>1. Échec de la connexion</summary>

-   Vérifiez si la configuration du numéro QQ est correcte
-   Vérifiez le format du fichier de configuration de napcat
-   Consultez les journaux du conteneur napcat pour identifier le problème

</details>

<details>
<summary>2. Échec de l'appel d'outil</summary>

-   Vérifiez que le modèle prend en charge la fonctionnalité d'appel de fonction
-   Vérifiez la configuration des clés d'API associées
-   Consultez les journaux du conteneur LLMQ pour localiser l'erreur
-   Dans le conteneur Docker, ajoutez [LangSmith](https://smith.langchain.com/) pour effectuer le débogage

    ```yaml
    environment:
      - LANGCHAIN_TRACING_V2=true
      - LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
      - LANGCHAIN_API_KEY="<votre_clé_api>"
      - LANGCHAIN_PROJECT="<votre_nom_de_projet>"
    ```

</details>

<details>
<summary>3. Autres problèmes</summary>

-   Pour d'autres problèmes, veuillez rejoindre le groupe QQ pour en discuter
    ![qrcode](static/qrcode.jpg)

</details>

## 🔗 Projets associés

-   [NoneBot2](https://github.com/nonebot/nonebot2)
-   [LangGraph](https://github.com/langchain-ai/langgraph)
-   [LangChain](https://github.com/langchain-ai/langchain)
-   [Judge0](https://github.com/judge0/judge0)
-   [Memos](https://github.com/usememos/memos)
-   [NapCat](https://github.com/NapNeko/NapCatQQ)

## 📄 Licence

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=large&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_large&issueType=license)

Ce projet est sous licence [Licence MIT](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE).

Copyright © 2024 Bitfennec.

---