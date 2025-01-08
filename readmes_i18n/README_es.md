<div align="center">

<img src="static/LLMQ.webp" width="400" style="margin-bottom: 10px;">

# 🤖 LLMQ-Horizon Bot de chat QQ

**Bot inteligente de QQ basado en NoneBot2 y LangGraph, que admite conversaciones con múltiples modelos, llamadas a herramientas y gestión de sesiones**

<br>

**Las herramientas están escritas utilizando Function-calling, sin usar plugins, siguiendo [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) , [LangChain Tools](https://python.langchain.com/docs/how_to/#tools)**

<br>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_small)
[![Docker Release](https://img.shields.io/docker/pulls/bitfennec/llmq-horizon?color=%230077c8&label=Docker%20Pulls&logo=docker&logoColor=white&style=flat)](https://hub.docker.com/r/bitfennec/llmq-horizon)
[![License](https://img.shields.io/github/license/Mgrsc/LLMQ-Horizon?color=%2300c853&label=MIT%20License&style=flat)](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE)

<br>

[English](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_en.md) | [Deutsch](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_de.md) | [Español](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_es.md) | [Français](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_fr.md) | [日本語](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_ja.md)

</div>

---

## ✨ Características Principales

-   **🔌 Rica Integración de Herramientas:** Ejecución de código, consulta del clima, adivinación, dibujo, etc.
-   **🤖 Soporte para Múltiples Modelos Grandes:** OpenAI, Google Gemini, Groq, etc.
-   **💬 Gestión Completa de Conversaciones:** Chats grupales/privados, conversaciones de múltiples turnos, aislamiento de sesiones.
-   **🎯 Métodos de Activación Flexibles:** @, palabras clave, prefijos de comandos.
-   **🎨 Capacidades Multimedia:** Análisis de imágenes, procesamiento de audio y video.
-   **⚡ Gestión Automática de Sesiones:** Limpieza por tiempo de espera, control de concurrencia.
-   **🦖 Potente Capacidad de Expansión:** Posibilidad de escribir herramientas propias, posibilidad de usar herramientas para controlar nonebot.

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

# 2. Preparar el archivo de configuración
cp config-tools.toml.example config-tools.toml
cp config.toml.example config.toml
cd napcat/config/
mv onebot11_qq.json onebot11_<tu_QQ>.json  # Reemplazar con el número de QQ real

# 3. Modificar la configuración (consultar los comentarios en los archivos de configuración)
vim config.toml
vim config-tools.toml

# 4. Iniciar el servicio
docker compose up -d

# 5. Iniciar sesión escaneando el código QR
docker compose logs -f

# Reiniciar el servicio LLMQ
docker compose restart llmq

# Detener todos los servicios
docker compose down
```

## 🛠️ Configuración de Herramientas

<details>
<summary>💻 Ejecución de Código (Code Runner - Judge0)</summary>

[Tutorial de implementación oficial de Judge0](https://github.com/judge0/judge0/blob/master/CHANGELOG.md)

1. **Preparar un entorno Ubuntu 22.04 o superior y Docker, configurar cgroup v1:**

    ```bash
    sudo sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"/' /etc/default/grub
    sudo update-grub
    sudo reboot
    ```

2. **Implementar Judge0:**

    ```bash
    wget https://github.com/judge0/judge0/releases/download/v1.13.1/judge0-v1.13.1.zip
    unzip judge0-v1.13.1.zip
    cd judge0-v1.13.1

    # Generar dos contraseñas y establecer contraseñas
    openssl rand -hex 32

    # Usar las contraseñas generadas para actualizar las variables REDIS_PASSWORD y POSTGRES_PASSWORD en el archivo judge0.conf.

    # Iniciar el servicio
    docker-compose up -d db redis
    sleep 10s
    docker-compose up -d
    sleep 5s
    ```

    Su instancia Judge0 CE v1.13.1 ahora está iniciada y en funcionamiento; visite http://<su_dirección_IP_del_servidor>:2358/docs para obtener la documentación.

3. **Configurar config-tools.toml:**

    ```toml
    [code_generation_running]
    judge0_url = "http://tu-servidor:2358"
    judge0_api_key = "tu-api-key"
    ```

</details>

<details>
<summary>😎 Notas (memos_manage - Memos)</summary>

[Tutorial de implementación oficial de Memos](https://www.usememos.com/docs/install/container-install)

1. **Preparar un entorno Ubuntu 22.04 o superior y Docker:**

2. **Escribir el archivo docker-compose.yaml**

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

3. **Iniciar memos**

    ```shell
    docker compose up -d
    ```

    Ahora puede acceder a memos en http://<su_dirección_IP_del_servidor>:5230, y obtener Tokens en Settings de memos.

4. **Completar el archivo de configuración**

    ```toml
    [memos]
    url = "http://tu-servidor:xxx"
    memos_token = "<ingresar_los_tokens_obtenidos>"
    default_visibility = "PRIVATE"
    page_size = 10
    user_id = 6
    ```

</details>

## 📝 Descripción de Comandos

| Comando                      | Descripción                                  |
| :--------------------------- | :------------------------------------------- |
| `/chat model <nombre_modelo>` | Cambiar el modelo de conversación             |
| `/chat clear`               | Limpiar todas las conversaciones              |
| `/chat group <true/false>`   | Activar/desactivar el aislamiento de chats grupales |
| `/chat down`                | Desactivar la función de conversación        |
| `/chat up`                  | Activar la función de conversación          |
| `/chat chunk <true/false>`  | Activar/desactivar el envío segmentado         |

## 🦊 Técnicas para la Redacción de Prompts

<details>
<summary>1. Principios Básicos</summary>

- Instrucciones Claras: Utilizar lenguaje imperativo para indicar claramente las necesidades del usuario, asegurando que el LLM comprenda con precisión.
- Proporcionar Ejemplos/Textos de Referencia: Proporcionar ejemplos e información detallada, constituyendo un Prompt Few-shot, que ayude al LLM a fortalecer la comprensión de la intención.
- Expresión Estructurada: Utilizar símbolos de marcado (como etiquetas XML, triple comillas, Markdown) para mejorar la legibilidad y hacer que la expresión del prompt sea clara.
- Control de Salida: Especificar los requisitos de formato de salida, estilo de lenguaje, etc., para asegurar que el LLM genere una salida que cumpla con las expectativas del usuario.
- Optimización del Diseño: Organizar cuidadosamente el diseño de la disposición del Prompt, para que el LLM lo comprenda fácilmente.
</details>
<details>
<summary>2. Otras Técnicas</summary>

- Listar las herramientas disponibles, con explicaciones y requisitos para las herramientas complejas
  ```
  create_speech generar voz
    - Máximo 40 palabras, no se pueden añadir emojis
    - Idiomas soportados: chino, inglés, japonés, alemán, francés, español, coreano, árabe, ruso, holandés, italiano, polaco, portugués
    - Mapeo de voces disponibles:
        Keli = keli
        Sigewen = xigewen
        Shenzi = shenzi
        Dingzhen = dingzhen
        Leijun = leijun
        Lanyangyang = lanyangyang
  ```
- Requerir el envío de la dirección file:// retornada por la herramienta
  ```
    El dibujo, la obtención de música y el tts deben enviar al usuario el enlace o la dirección de la ruta del archivo retornada
  ```
- Ejemplos de maquetación del contenido devuelto por la herramienta
  ```
    # Ejemplo de optimización de la maquetación del contenido devuelto por la herramienta
    Ejemplo de formato de datos devueltos por get_weather_data:
    * A: Dime el clima de Changsha hoy
        T: Llama a la herramienta `get_weather_data` para obtener el clima
        Q:
        🌤️ Clima de {ubicación}
        🌅 Amanecer y atardecer: {xx:xx}-{xx:xx sin año}
        ⏱️ Hora: {hora}
        🌡️ Temperatura: {temperatura}℃
        💧 Humedad: {humedad}%
        🧣 Sensación térmica: {sensación térmica}℃
        🍃 Dirección y velocidad del viento: {dirección del viento}-{velocidad del viento}
        📋 Condición general: {análisis integral}
        Cariño, deberías ponerte más ropa cuando salgas~ Ten cuidado de no resfriarte
  ```
</details>

## ❗ Preguntas Frecuentes

Todas las herramientas se han probado. Si hay algún problema, consulte las siguientes comprobaciones.

<details>
<summary>1. Error al iniciar sesión</summary>

-   Comprobar si la configuración del número de QQ es correcta
-   Confirmar el formato del archivo de configuración de napcat
-   Ver los logs del contenedor de napcat para solucionar problemas

</details>

<details>
<summary>2. Error al llamar a las herramientas</summary>

-   Confirmar que el modelo admite la función de llamada a funciones
-   Comprobar la configuración de las claves API relacionadas
-   Ver los logs del contenedor LLMQ para ubicar los errores
-   Añadir [LangSmith](https://smith.langchain.com/) en el contenedor docker para depurar

    ```yaml
    environment:
      - LANGCHAIN_TRACING_V2=true
      - LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
      - LANGCHAIN_API_KEY="<tu_api_key>"
      - LANGCHAIN_PROJECT="<nombre_de_tu_proyecto>"
    ```

</details>

<details>
<summary>3. Otros problemas</summary>

-   Para otros problemas, únete al grupo QQ para discutir
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

Este proyecto está licenciado bajo la [Licencia MIT](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE).

Copyright © 2024 Bitfennec.

---