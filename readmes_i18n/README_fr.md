<div align="center">

<img src="static/LLMQ.webp" width="400" style="margin-bottom: 10px;">

# 🤖 LLMQ-Horizon Robot de Chat QQ

**Un robot QQ intelligent basé sur NoneBot2 et LangGraph, prenant en charge les conversations multi-modèles, l'appel d'outils et la gestion des sessions**

<br>

**Les outils sont tous écrits en utilisant Function-calling, sans utiliser de plugins, en référence à [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) , [LangChain Tools](https://python.langchain.com/docs/how_to/#tools)**

<br>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_small)
[![Docker Release](https://img.shields.io/docker/pulls/bitfennec/llmq-horizon?color=%230077c8&label=Docker%20Pulls&logo=docker&logoColor=white&style=flat)](https://hub.docker.com/r/bitfennec/llmq-horizon)
[![License](https://img.shields.io/github/license/Mgrsc/LLMQ-Horizon?color=%2300c853&label=Licence%20MIT&style=flat)](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE)

<br>

[English](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_en.md) | [Deutsch](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_de.md) | [Español](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_es.md) | [Français](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_fr.md) | [日本語](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_ja.md)

</div>

---

## ✨ Principales Caractéristiques

-   **🔌 Intégration d'outils riches :** Exécution de code, prévisions météo, divination, dessin, etc.
-   **🤖 Prise en charge de plusieurs grands modèles :** OpenAI, Google Gemini, Groq, etc.
-   **💬 Gestion de conversation complète :** Discussions de groupe/privées, conversations multi-tours, isolation de session
-   **🎯 Modes de déclenchement flexibles :** @, mots-clés, préfixes de commande
-   **🎨 Capacités multimédias :** Analyse d'image, traitement audio et vidéo
-   **⚡ Gestion automatique de session :** Nettoyage après expiration, contrôle de la concurrence
-   **🦖 Puissantes capacités d'extension :** Possibilité d'écrire des outils soi-même, possibilité d'utiliser des outils pour contrôler nonebot

---

## 🚀 Démarrage Rapide

### 1. Préparation de l'environnement de déploiement

-   Docker et Docker Compose
-   Environnement réseau stable
-   Systèmes recommandés : Ubuntu 22.04 et versions supérieures, Debian 11 et versions supérieures

> Remarque : Pour le modèle deepseek, n'activez pas plus de 5 outils et utilisez un prompt aussi court que possible, sinon ds appellera les outils de manière frénétique jusqu'à vous submerger, ou bien ne les appellera pas du tout.

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

# 3. Modifier la configuration (se référer aux commentaires dans les fichiers de configuration pour les modifications)
vim config.toml
vim config-tools.toml

# 4. Démarrer le service
docker compose up -d

# 5. Scanner le code QR pour se connecter
docker compose logs -f

# Redémarrer le service LLMQ
docker compose restart llmq

# Arrêter tous les services
docker compose down
```

## 🛠️ Configuration des Outils

<details>
<summary>💻 Exécution de Code (Code Runner - Judge0)</summary>

[Tutoriel de Déploiement Officiel de Judge0](https://github.com/judge0/judge0/blob/master/CHANGELOG.md)

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

    # Générer deux mots de passe et les définir
    openssl rand -hex 32

    # Utiliser les mots de passe générés pour mettre à jour les variables REDIS_PASSWORD et POSTGRES_PASSWORD dans le fichier judge0.conf.

    # Démarrer le service
    docker-compose up -d db redis
    sleep 10s
    docker-compose up -d
    sleep 5s
    ```

    Votre instance Judge0 CE v1.13.1 est maintenant démarrée et en cours d'exécution; consultez http://<votre_adresse_IP_serveur>:2358/docs pour la documentation.

3. **Configurer config-tools.toml :**

    ```toml
    [code_generation_running]
    judge0_url = "http://votre-serveur:2358"
    judge0_api_key = "votre-clé-api"
    ```

</details>

<details>
<summary>📝 Mémos (memos_manage - Memos)</summary>

[Tutoriel de Déploiement Officiel de Memos](https://www.usememos.com/docs/install/container-install)

1. **Préparer l'environnement :**
   - Ubuntu 22.04 et versions supérieures
   - Docker et Docker Compose

2. **Écrire le fichier docker-compose.yaml**

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

3. **Démarrer le service :**
```bash
docker compose up -d
```

Vous pouvez maintenant accéder à memos sur http://<votre_adresse_IP_serveur>:5230. Récupérez les Tokens dans les Paramètres de memos.

4. **Configurer config-tools.toml :**

```toml
[memos_manage]
url = "http://votre-serveur:5230"
memos_token = "votre-jeton-memos"  # Jeton récupéré depuis la page Paramètres
default_visibility = "PRIVATE"
page_size = 10
user_id = 6
```
</details>

<details>
<summary>📰 Récupération d'Actualités (get_news - SynapseNews)</summary>

[Adresse du Projet SynapseNews](https://github.com/Mgrsc/SynapseNews)

1. **Étapes de déploiement :**
```bash
git clone https://github.com/Mgrsc/SynapseNews.git
cd synapsenews
# Configurer config.toml
docker compose up -d
```
</details>

## 📝 Instructions des Commandes

| Commande                      | Description                                  |
| :---------------------------- | :------------------------------------------- |
| `/chat model <nom_du_modèle>` | Changer de modèle de conversation            |
| `/chat clear`                | Effacer toutes les conversations              |
| `/chat group <true/false>`    | Activer/désactiver l'isolation des groupes  |
| `/chat down`                 | Désactiver la fonctionnalité de conversation |
| `/chat up`                   | Activer la fonctionnalité de conversation    |
| `/chat chunk <true/false>`    | Activer/désactiver l'envoi par segments     |

## 🦊 Astuces pour la Rédaction de Prompts

<details>
<summary>1. Principes de Base</summary>

- Instructions claires : Utilisez un langage impératif pour exprimer clairement les besoins de l'utilisateur, en vous assurant que le LLM comprend précisément.
- Fournir des exemples/textes de référence : Fournissez des exemples et des informations détaillés pour créer un Prompt "Few-shot", aidant le LLM à mieux comprendre l'intention.
- Expression structurée : Utilisez des symboles de balisage (tels que des balises XML, des guillemets triples, Markdown) pour améliorer la lisibilité, en rendant l'expression du prompt claire.
- Contrôle de la sortie : Spécifiez le format de sortie, le style de langue et d'autres exigences, en vous assurant que le LLM génère une sortie qui répond aux attentes de l'utilisateur.
- Optimisation de la disposition : Organisez soigneusement la disposition du prompt pour faciliter la compréhension du LLM.
</details>

<details>
<summary>2. Autres Astuces</summary>

- Listez les outils disponibles, et expliquez et précisez les outils complexes.
  ```
  create_speech génère de la parole
    - 40 caractères maximum, sans emojis
    - Langues prises en charge : chinois, anglais, japonais, allemand, français, espagnol, coréen, arabe, russe, néerlandais, italien, polonais, portugais
    - Mappages de voix disponibles :
        Keli = keli
        Sigewen = xigewen
        Shenzi = shenzi
        Dingzhen = dingzhen
        Leijun = leijun
        Lanyangyang = lanyangyang
  ```
- Demandez à ce que l'adresse file:// renvoyée par l'outil soit envoyée
  ```
    Le dessin, la récupération de musique et le tts doivent envoyer le lien ou le chemin d'accès du fichier renvoyé à l'utilisateur.
  ```
- Exemple de mise en page du contenu retourné par l'outil
  ```
      # Exemple d'optimisation de la mise en page du contenu renvoyé par l'outil
    Exemple de formatage des données renvoyées par get_weather_data :
    *   A : Dites-moi le temps qu'il fait aujourd'hui à Changsha
        T : Appel de l'outil `get_weather_data` pour obtenir la météo
        Q :
        🌤️ Météo à {lieu}
        🌅 Lever et coucher du soleil : {xx:xx}-{xx:xx sans l'année}
        ⏱️   Heure : {heure}
        🌡️ Température : {température}°C
        💧 Humidité : {humidité}%
        🧣 Température ressentie : {température_ressentie}°C
        🍃 Direction et vitesse du vent : {direction_vent}-{vitesse_vent}
        📋 Situation générale : {analyse_générale}
        Bébé, mets plus de vêtements quand tu sors ! Fais attention de ne pas attraper froid !
  ```
</details>

## 🤝 Guide de Contribution

1. Fork ce dépôt
2. Créez votre branche de fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Validez vos modifications (`git commit -m 'Ajouter une AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 🤖 Questions Fréquentes
Tous les outils ont été testés. Si vous rencontrez des problèmes, veuillez vous référer aux vérifications ci-dessous.

<details>
<summary>1. Échec de connexion</summary>

-   Vérifiez si la configuration du numéro QQ est correcte.
-   Vérifiez le format du fichier de configuration napcat.
-   Consultez les journaux du conteneur napcat pour identifier les problèmes.

</details>

<details>
<summary>2. Échec de l'appel d'outils</summary>

-   Vérifiez que le modèle prend en charge les capacités d'appel de fonctions.
-   Vérifiez les configurations des clés API correspondantes.
-   Consultez les journaux du conteneur LLMQ pour identifier les erreurs.
-   Ajoutez [LangSmith](https://smith.langchain.com/) au conteneur docker pour le débogage.

    ```yaml
    environment:
      - LANGCHAIN_TRACING_V2=true
      - LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
      - LANGCHAIN_API_KEY="<your_api_key>"
      - LANGCHAIN_PROJECT="<your_project_name>"
    ```

</details>

<details>
<summary>3. Autres problèmes</summary>

-   Pour d'autres problèmes, veuillez rejoindre le groupe QQ pour discuter.
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
Ce projet est sous licence MIT - Consultez le fichier [LICENSE](LICENSE) pour plus de détails.
Copyright © 2024 Bitfennec.
---
</div>