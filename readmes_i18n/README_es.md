<div align="center">

<img src="static/LLMQ.webp" width="400" style="margin-bottom: 10px;">

# 🤖 LLMQ-Horizon Bot de Chat QQ

**Un bot inteligente de QQ basado en NoneBot2 y LangGraph, que admite conversaciones con múltiples modelos, invocación de herramientas y gestión de sesiones**

<br>

**Las herramientas están escritas utilizando Function-calling, sin usar complementos, consulta [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) y [LangChain Tools](https://python.langchain.com/docs/how_to/#tools)**

<br>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_small)
[![Docker Release](https://img.shields.io/docker/pulls/bitfennec/llmq-horizon?color=%230077c8&label=Docker%20Pulls&logo=docker&logoColor=white&style=flat)](https://hub.docker.com/r/bitfennec/llmq-horizon)
[![License](https://img.shields.io/github/license/Mgrsc/LLMQ-Horizon?color=%2300c853&label=MIT%20License&style=flat)](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE)

</div>

---

## ✨ Características Principales

-   **🔌 Integración de Herramientas Ricas:** Ejecución de código, consulta del clima, adivinación, pintura, etc.
-   **🤖 Soporte para Múltiples Modelos Grandes:** OpenAI, Google Gemini, Groq, etc.
-   **💬 Gestión Completa de Conversaciones:** Chat grupal/privado, conversaciones de múltiples turnos, aislamiento de sesiones.
-   **🎯 Formas Flexibles de Activación:** @, palabras clave, prefijos de comandos.
-   **🎨 Capacidades Multimedia:** Análisis de imágenes, procesamiento de audio y video.
-   **⚡ Gestión Automática de Sesiones:** Limpieza por tiempo de espera, control de concurrencia.
-   **🦖 Potente Capacidad de Extensión:** Posibilidad de escribir herramientas propias, posibilidad de usar herramientas para controlar Nonebot.

---

## 🚀 Inicio Rápido

### 1. Preparación del Entorno de Implementación

-   Docker y Docker Compose
-   Entorno de red estable
-   Sistemas recomendados: Ubuntu 22.04 y superior, Debian 11 y superior

### 2. Pasos de Instalación

```bash
# 1. Clonar el proyecto
git clone https://github.com/Mgrsc/LLMQ-Horizon.git
cd LLMQ-Horizon

# 2. Preparar los archivos de configuración
cp config-tools.toml.example config-tools.toml
cp config.toml.example config.toml
cd napcat/config/
mv onebot11_qq.json onebot11_<tu_QQ>.json  # Reemplaza con tu número de QQ real

# 3. Modificar la configuración (consulta los comentarios en los archivos de configuración para realizar las modificaciones)
vim config.toml
vim config-tools.toml

# 4. Iniciar el servicio
docker compose up -d

# 5. Escanear el código para iniciar sesión
docker compose logs -f

# Reiniciar el servicio LLMQ
docker compose restart llmq

# Detener todos los servicios
docker compose down
```

## 🛠️ Configuración de Herramientas

<details>
<summary>💻 Ejecución de Código (Code Runner - Judge0)</summary>

[Tutorial oficial de implementación de Judge0](https://github.com/judge0/judge0/blob/master/CHANGELOG.md)

1. **Prepara un entorno Ubuntu 22.04 o superior y Docker, configura cgroup v1:**

    ```bash
    sudo sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"/' /etc/default/grub
    sudo update-grub
    sudo reboot
    ```

2. **Implementa Judge0:**

    ```bash
    wget https://github.com/judge0/judge0/releases/download/v1.13.1/judge0-v1.13.1.zip
    unzip judge0-v1.13.1.zip
    cd judge0-v1.13.1

    # Genera dos contraseñas y configúralas
    openssl rand -hex 32

    # Usa las contraseñas generadas para actualizar las variables REDIS_PASSWORD y POSTGRES_PASSWORD en el archivo judge0.conf.

    # Inicia el servicio
    docker-compose up -d db redis
    sleep 10s
    docker-compose up -d
    sleep 5s
    ```

    Tu instancia de Judge0 CE v1.13.1 ahora está activa y en funcionamiento; accede a http://<tu_dirección_IP_del_servidor>:2358/docs para obtener la documentación.

3. **Configura config-tools.toml:**

    ```toml
    [code_runner]
    judge0_url = "http://tu-servidor:2358"
    judge0_api_key = "tu-api-key"
    ```

</details>

<details>
<summary>😎 Notas (memos_manage - Memos)</summary>

[Tutorial oficial de implementación de Memos](https://www.usememos.com/docs/install/container-install)

1. **Prepara un entorno Ubuntu 22.04 o superior y Docker:**

2. **Escribe el archivo docker-compose.yaml**

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

3. **Inicia Memos**

    ```shell
    docker compose up -d
    ```

    Ahora puedes acceder a Memos en http://<tu_dirección_IP_del_servidor>:5230, y obtener los Tokens en la configuración de Memos.

4. **Rellena el archivo de configuración**

    ```toml
    [memos]
    url = "http://tu-servidor:xxx"
    memos_token = "<introduce_los_tokens_obtenidos>"
    default_visibility = "PRIVATE"
    page_size = 10
    user_id = 6
    ```

</details>

## 📝 Descripción de Comandos

| Comando                      | Descripción                             |
| :------------------------ | :-------------------------------------- |
| `/chat model <nombre_modelo>`   | Cambia el modelo de conversación        |
| `/chat clear`             | Limpia todas las conversaciones          |
| `/chat group <true/false>` | Activa/desactiva el aislamiento de grupos |
| `/chat down`              | Desactiva la función de conversación     |
| `/chat up`                | Activa la función de conversación       |
| `/chat chunk <true/false>` | Activa/desactiva el envío en fragmentos  |

## ❗ Preguntas Frecuentes

<details>
<summary>1. Fallo al iniciar sesión</summary>

-   Verifica que la configuración del número de QQ sea correcta.
-   Confirma el formato del archivo de configuración de napcat.
-   Consulta los registros del contenedor napcat para solucionar el problema.

</details>

<details>
<summary>2. Fallo al invocar herramientas</summary>

-   Confirma que el modelo admita la capacidad de invocación de funciones.
-   Verifica la configuración de las claves API relacionadas.
-   Consulta los registros del contenedor LLMQ para localizar el error.
-   En el contenedor docker, añade [LangSmith](https://smith.langchain.com/) para depurar.

    ```yaml
    environment:
      - LANGCHAIN_TRACING_V2=true
      - LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
      - LANGCHAIN_API_KEY="<tu_clave_api>"
      - LANGCHAIN_PROJECT="<tu_nombre_de_proyecto>"
    ```

</details>

<details>
<summary>3. Otros problemas</summary>

-   Para otros problemas, por favor únete al grupo de QQ para discutir
    ![qrcode](static/qrcode.jpg)

</details>

## 🔗 Proyectos Relacionados

-   [NoneBot2](https://github.com/nonebot/nonebot2)
-   [LangGraph](https://github.com/langchain-ai/langgraph)
-   [LangChain](https://github.com/langchain-ai/langchain)
-   [Judge0](https://github.com/judge0/judge0)
-   [Memos](https://github.com/usememos/memos)
-   [NapCat](https://github.com/NapNeko/NapCatQQ)

## 📄 Licencia

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=large&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_large&issueType=license)

Este proyecto se distribuye bajo la [Licencia MIT](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE).

Copyright © 2024 Bitfennec.

---