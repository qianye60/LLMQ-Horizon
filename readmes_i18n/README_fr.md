<div align="center">

<img src="static/LLMQ.webp" width="400" style="margin-bottom: 10px;">

# 🤖 LLMQ-Horizon Robot de Chat QQ

**Un robot QQ intelligent basé sur NoneBot2 et LangGraph, prenant en charge les conversations multimodèles, l'appel d'outils et la gestion de sessions**

<br>

**Les outils sont tous écrits en utilisant Function-calling, sans utiliser de plugins, voir [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) , [LangChain Tools](https://python.langchain.com/docs/how_to/#tools)**

<br>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_small)
[![Docker Release](https://img.shields.io/docker/pulls/bitfennec/llmq-horizon?color=%230077c8&label=Docker%20Pulls&logo=docker&logoColor=white&style=flat)](https://hub.docker.com/r/bitfennec/llmq-horizon)
[![License](https://img.shields.io/github/license/Mgrsc/LLMQ-Horizon?color=%2300c853&label=Licence%20MIT&style=flat)](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE)

</div>

---

## ✨ Principales Caractéristiques

-   **🔌 Intégration d'outils riches :** Exécution de code, prévisions météorologiques, divination, dessin, etc.
-   **🤖 Prise en charge de divers grands modèles :** OpenAI, Google Gemini, Groq, etc.
-   **💬 Gestion complète des dialogues :** Chat de groupe/privé, conversations à plusieurs tours, isolation des sessions
-   **🎯 Modes de déclenchement flexibles :** @, mots-clés, préfixes de commande
-   **🎨 Capacités multimédias :** Analyse d'images, traitement audio et vidéo
-   **⚡ Gestion automatique des sessions :** Nettoyage des délais d'attente, contrôle de la concurrence
-   **🦖 Forte capacité d'extension :** Possibilité d'écrire des outils soi-même, possibilité d'utiliser des outils pour contrôler nonebot

---

## 🚀 Démarrage Rapide

### 1. Préparation de l'environnement de déploiement

-   Docker et Docker Compose
-   Environnement réseau stable
-   Systèmes recommandés : Ubuntu 22.04 et versions ultérieures, Debian 11 et versions ultérieures

### 2. Étapes d'installation

```bash
# 1. Cloner le projet
git clone https://github.com/Mgrsc/LLMQ-Horizon.git
cd LLMQ-Horizon

# 2. Préparer les fichiers de configuration
cp config-tools.toml.example config-tools.toml
cp config.toml.example config.toml
cd napcat/config/
mv onebot11_qq.json onebot11_<votreQQ>.json  # Remplacer par votre numéro QQ réel

# 3. Modifier la configuration (se référer aux commentaires dans les fichiers de configuration pour la modification)
vim config.toml
vim config-tools.toml

# 4. Démarrer le service
docker compose up -d

# 5. Scanner pour se connecter
docker compose logs -f

# Redémarrer le service LLMQ
docker compose restart llmq

# Arrêter tous les services
docker compose down
```

## 🛠️ Configuration des Outils

<details>
<summary>💻 Exécution de Code (Code Runner - Judge0)</summary>

[Tutoriel de déploiement officiel de Judge0](https://github.com/judge0/judge0/blob/master/CHANGELOG.md)

1. **Préparer un environnement Ubuntu 22.04 ou supérieur et Docker, configurer cgroup v1 :**

    ```bash
    sudo sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"/' /etc/default/grub
    sudo update-grub
    sudo reboot
    ```

2. **Déployer Judge0 :**

    ```bash
    wget https://github.com/judge0/judge0/releases/download/v1.13.1/judge0-v1.13.1.zip
    unzip judge0-v1.13.1.zip
    cd judge0-v1.13.1

    # Générer deux mots de passe et définir les mots de passe
    openssl rand -hex 32

    # Utiliser les mots de passe générés pour mettre à jour les variables REDIS_PASSWORD et POSTGRES_PASSWORD dans le fichier judge0.conf.

    # Démarrer le service
    docker-compose up -d db redis
    sleep 10s
    docker-compose up -d
    sleep 5s
    ```

    Votre instance Judge0 CE v1.13.1 est maintenant démarrée et en fonctionnement ; consultez http://<Votre adresse IP de serveur>:2358/docs pour obtenir la documentation.

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

1. **Préparer un environnement Ubuntu 22.04 ou supérieur et Docker :**

2. **Rédiger le fichier docker-compose.yaml**

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

3. **Démarrer memos**

    ```shell
    docker compose up -d
    ```

    Vous pouvez maintenant accéder à memos sur http://<Votre adresse IP de serveur>:5230, et obtenir des jetons dans les Paramètres de memos.

4. **Remplir le fichier de configuration**

    ```toml
    [memos]
    url = "http://votre-serveur:xxx"
    memos_token = "<Entrez les jetons obtenus>"
    default_visibility = "PRIVATE"
    page_size = 10
    user_id = 6
    ```

</details>

## 📝 Description des Commandes

| Commande                       | Description                               |
| :----------------------------- | :---------------------------------------- |
| `/chat model <nom du modèle>` | Changer le modèle de conversation          |
| `/chat clear`                  | Effacer toutes les conversations         |
| `/chat group <true/false>`     | Activer/désactiver l'isolation des groupes |
| `/chat down`                   | Désactiver la fonctionnalité de conversation |
| `/chat up`                     | Activer la fonctionnalité de conversation  |
| `/chat chunk <true/false>`      | Activer/désactiver l'envoi par segments    |

## ❗ Problèmes courants

<details>
<summary>1. Échec de la connexion</summary>

-   Vérifier si la configuration du numéro QQ est correcte
-   Confirmer le format du fichier de configuration napcat
-   Consulter les journaux du conteneur napcat pour identifier les problèmes

</details>

<details>
<summary>2. Échec de l'appel d'outils</summary>

-   Confirmer que le modèle prend en charge la capacité d'appel de fonctions
-   Vérifier la configuration des clés API associées
-   Consulter les journaux du conteneur LLMQ pour localiser l'erreur
-   Dans le conteneur Docker, ajouter [LangSmith](https://smith.langchain.com/) pour le débogage

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

## 🔗 Projets Associés

-   [NoneBot2](https://github.com/nonebot/nonebot2)
-   [LangGraph](https://github.com/langchain-ai/langgraph)
-   [LangChain](https://github.com/langchain-ai/langchain)
-   [Judge0](https://github.com/judge0/judge0)
-   [Memos](https://github.com/usememos/memos)
-   [NapCat](https://github.com/NapNeko/NapCatQQ)

## 📄 Licence

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=large&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_large&issueType=license)

Ce projet est sous [licence MIT](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE).

Copyright © 2024 Bitfennec.

---