<div align="center">

<img src="static/LLMQ.webp" width="400" style="margin-bottom: 10px;">

# 🤖 LLMQ-Horizon Bot de Chat QQ

**Un bot inteligente de QQ basado en NoneBot2 y LangGraph, que admite conversaciones con múltiples modelos, llamadas a herramientas y gestión de sesiones**

<br>

**Las herramientas están escritas usando Function-calling, sin usar plugins, con referencia a [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) y [LangChain Tools](https://python.langchain.com/docs/how_to/#tools)**

<br>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2FMgrsc%2FLLMQ-Horizon?ref=badge_small)
[![Docker Release](https://img.shields.io/docker/pulls/bitfennec/llmq-horizon?color=%230077c8&label=Docker%20Pulls&logo=docker&logoColor=white&style=flat)](https://hub.docker.com/r/bitfennec/llmq-horizon)
[![License](https://img.shields.io/github/license/Mgrsc/LLMQ-Horizon?color=%2300c853&label=MIT%20License&style=flat)](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/LICENSE)

<br>

[Inglés](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_en.md) | [Alemán](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_de.md) | [Español](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_es.md) | [Francés](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_fr.md) | [Japonés](https://github.com/Mgrsc/LLMQ-Horizon/blob/main/readmes_i18n/README_ja.md)

</div>

---

## ✨ Características Principales

-   **🔌 Amplia integración de herramientas:** Ejecución de código, consulta del clima, adivinación, dibujo, etc.
-   **🤖 Soporte para múltiples modelos grandes:** OpenAI, Google Gemini, Groq, etc.
-   **💬 Gestión completa de conversaciones:** Chats grupales/privados, conversaciones de varios turnos, aislamiento de sesiones
-   **🎯 Métodos de activación flexibles:** @, palabras clave, prefijos de comandos
-   **🎨 Capacidades multimedia:** Análisis de imágenes, procesamiento de audio y video
-   **⚡ Gestión automática de sesiones:** Limpieza por tiempo de espera, control de concurrencia
-   **🦖 Potente capacidad de expansión:** Posibilidad de escribir herramientas propias y de usar herramientas para controlar nonebot

---

## 🚀 Inicio Rápido

### 1. Preparación del entorno de implementación

-   Docker y Docker Compose
-   Entorno de red estable
-   Sistema recomendado: Ubuntu 22.04 y superior, Debian 11 y superior

> Nota: Al activar herramientas con el modelo deepseek, no use más de 5, y las indicaciones deben ser lo más breves posible. De lo contrario, deepseek llamará a las herramientas sin parar y las saturará, o simplemente no las usará.

### 2. Pasos de instalación

```bash
# 1. Clona el proyecto
git clone https://github.com/Mgrsc/LLMQ-Horizon.git
cd LLMQ-Horizon

# 2. Prepara los archivos de configuración
cp config-tools.toml.example config-tools.toml
cp config.toml.example config.toml
cd napcat/config/
mv onebot11_qq.json onebot11_<tu_QQ>.json  # Reemplaza con tu número de QQ real

# 3. Modifica la configuración (consulta los comentarios en los archivos de configuración)
vim config.toml
vim config-tools.toml

# 4. Inicia el servicio
docker compose up -d

# 5. Escanea el código QR para iniciar sesión
docker compose logs -f

# Reinicia el servicio LLMQ
docker compose restart llmq

# Detén todos los servicios
docker compose down
```

## 🛠️ Configuración de Herramientas

<details>
<summary>💻 Ejecución de Código (Code Runner - Judge0)</summary>

[Tutorial oficial de despliegue de Judge0](https://github.com/judge0/judge0/blob/master/CHANGELOG.md)

1. **Prepara un entorno Ubuntu 22.04 o superior y Docker, configura cgroup v1:**

    ```bash
    sudo sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"/' /etc/default/grub
    sudo update-grub
    sudo reboot
    ```

2. **Despliega Judge0:**

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

    Tu instancia Judge0 CE v1.13.1 ahora está iniciada y funcionando; accede a http://<la dirección IP de tu servidor>:2358/docs para obtener la documentación.

3. **Configura config-tools.toml:**

    ```toml
    [code_generation_running]
    judge0_url = "http://tu-servidor:2358"
    judge0_api_key = "tu-api-key"
    ```

</details>

<details>
<summary>📝 Notas (memos_manage - Memos)</summary>

[Tutorial oficial de despliegue de Memos](https://www.usememos.com/docs/install/container-install)

1. **Prepara el entorno:**
   - Ubuntu 22.04 y superior
   - Docker y Docker Compose

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

3. **Inicia el servicio:**
```bash
docker compose up -d
```

Ahora puedes acceder a memos en http://<la dirección IP de tu servidor>:5230, y obtener los Tokens en la configuración de memos.

4. **Configura config-tools.toml:**

```toml
[memos_manage]
url = "http://tu-servidor:5230"
memos_token = "tu-memos-token"  # Token obtenido desde la página de configuración
default_visibility = "PRIVATE"
page_size = 10
user_id = 6
```
</details>

<details>
<summary>📰 Obtención de noticias (get_news - SynapseNews)</summary>

[Dirección del proyecto SynapseNews](https://github.com/Mgrsc/SynapseNews)

1. **Pasos de despliegue:**
```bash
git clone https://github.com/Mgrsc/SynapseNews.git
cd synapsenews
# Configura config.toml
docker compose up -d
```
</details>

## 📝 Descripción de Comandos

| Comando                      | Descripción                             |
| :------------------------ | :-------------------------------------- |
| `/chat model <nombre_modelo>`   | Cambiar el modelo de conversación       |
| `/chat clear`             | Limpiar todas las sesiones               |
| `/chat group <true/false>` | Activar/desactivar el aislamiento de grupos |
| `/chat down`              | Desactivar la función de conversación  |
| `/chat up`                | Activar la función de conversación     |
| `/chat chunk <true/false>` | Activar/desactivar el envío por fragmentos |

## 🦊 Consejos para la Elaboración de Indicaciones

<details>
<summary>1. Principios Básicos</summary>

-   Instrucciones claras: Utilizar lenguaje imperativo para establecer las necesidades del usuario, asegurando que el LLM pueda entender con precisión.
-   Proporcionar ejemplos/texto de referencia: Ofrecer ejemplos e información detallada, configurando un Prompt de pocos disparos para ayudar al LLM a mejorar la comprensión de la intención.
-   Expresión estructurada: Usar símbolos de marcado (como etiquetas XML, comillas triples, Markdown) para mejorar la legibilidad, haciendo que las indicaciones sean claras.
-   Control de salida: Especificar los requisitos de formato de salida, estilo de lenguaje, etc., para garantizar que el LLM genere una salida que cumpla con las expectativas del usuario.
-   Optimización del diseño: Organizar cuidadosamente el diseño del Prompt para facilitar la comprensión del LLM.
</details>

<details>
<summary>2. Otros Consejos</summary>

-   Enumerar las herramientas disponibles, explicando y requiriendo las herramientas complejas.
  ```
  create_speech generar voz
    - Máximo 40 caracteres, sin emojis
    - Idiomas admitidos: chino, inglés, japonés, alemán, francés, español, coreano, árabe, ruso, holandés, italiano, polaco, portugués
    - Asignaciones de voces disponibles:
        可莉 = keli
        西格雯 = xigewen
        神子 = shenzi
        丁真 = dingzhen
        雷军 = leijun
        懒羊羊 = lanyangyang
  ```
-   Solicitar el envío de la dirección file:// devuelta por la herramienta.
  ```
    El dibujo, la obtención de música y la función TTS deben enviar la dirección del enlace o la ruta del archivo al usuario
  ```
-   Ejemplo de formato de la salida de la herramienta.
  ```
      # Ejemplo de optimización del formato de salida de la herramienta
    Ejemplo de formato de datos devueltos por get_weather_data:
    *   A: Dime el clima de Changsha hoy
        T: Llamar a la herramienta `get_weather_data` para obtener el clima
        Q:
        🌤️ Clima en {lugar}
        🌅 Salida y puesta del sol: {xx:xx}-{xx:xx sin año}
        ⏱️   Hora: {hora}
        🌡️ Temperatura: {temperatura}℃
        💧 Humedad: {humedad}%
        🧣 Sensación térmica: {sensación térmica}℃
        🍃 Dirección y velocidad del viento: {dirección del viento}-{velocidad del viento}
        📋 Estado general: {análisis general}
        ¡Cariño, abrígate al salir para no resfriarte!
  ```
</details>

## 🤝 Guía de Contribución

1. Haz un fork de este repositorio
2. Crea tu rama de función (`git checkout -b feature/AmazingFeature`)
3. Envía tus cambios (`git commit -m 'Añade una característica increíble'`)
4. Sube a la rama (`git push origin feature/AmazingFeature`)
5. Abre una solicitud de extracción (Pull Request)

## 🤖 Preguntas Frecuentes
Todas las herramientas han sido probadas. Si hay algún problema, consulta la siguiente verificación.

<details>
<summary>1. Fallo al iniciar sesión</summary>

-   Comprueba si la configuración del número de QQ es correcta.
-   Confirma el formato del archivo de configuración de napcat.
-   Consulta los registros del contenedor napcat para solucionar el problema.

</details>

<details>
<summary>2. Fallo al llamar a la herramienta</summary>

-   Confirma que el modelo admite la capacidad de llamada a funciones.
-   Comprueba la configuración de las claves de la API relacionadas.
-   Consulta los registros del contenedor LLMQ para localizar el error.
-   Añade [LangSmith](https://smith.langchain.com/) al contenedor docker para depurar.

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

-   Para otros problemas, únete al grupo de QQ para discutir.
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
Este proyecto tiene licencia MIT - consulta el archivo [LICENSE](LICENSE) para obtener detalles.
Copyright © 2024 Bitfennec.
---