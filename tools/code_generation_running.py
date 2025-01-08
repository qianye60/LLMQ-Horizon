# judge0
# 测试通过语言: Assembly,Bash,C,C++,Clojure,C#,COBOL,Common Lisp,D,Elixir,Fortran,Go,Groovy,Haskell,Java,JavaScript,Kotlin,Lua,OCaml,Octave,Pascal,Perl,PHP,Plain Text,Python,Python2,R,Ruby,Rust,Scala,SQL,Swift,TypeScript,Visual Basic.Net
from langchain_core.tools import tool
from datetime import datetime, timezone, timedelta
from .config import config
import requests
import codecs
import base64
import json
import time
import re
import os
code_generation_running = config.get("code_generation_running", {})

judge0_api_key = code_generation_running.get("judge0_api_key")
cpu_time_limit = code_generation_running.get("cpu_time_limit", 5)
wall_time_limit = code_generation_running.get("wall_time_limit", 8)
judge0_url = code_generation_running.get("judge0_url")
openai_api_key = code_generation_running.get("openai_api_key")
openai_base_url = code_generation_running.get("openai_base_url")
model = code_generation_running.get("model", "gemini-exp-1206")
CACHE_FILE = "languages_cache.json"
UPDATE_INTERVAL = 2 * 24 * 60 * 60
# submit_fields = "stdout,stderr,compile_output,exit_code,exit_signal,created_at,finished_at,time,wall_time,memory,source_code"
submit_fields = "stdout,stderr,compile_output,message,exit_code,exit_signal,status,created_at,finished_at,time,wall_time,memory,compile_output,language,status"

_language_cache = None

MAX_OUTPUT_LENGTH = 300

def _fetch_languages_from_api_():
    """
    从 API 获取数据并更新缓存文件
    """
    print("Fetching languages from API...")
    url = f"{judge0_url}/languages"
    headers = {
        'X-Auth-Token': judge0_api_key,
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        languages = response.json()
        formatted_languages = {}
        for lang in languages:
            lang_id = lang["id"]
            lang_name = lang["name"]
            parts = lang_name.split("(", 1)
            name = parts[0].strip()
            if len(parts) > 1:
                version = parts[1].replace(")", "").strip()
            else:
                version = ""
            if name not in formatted_languages:
                formatted_languages[name] = []
            formatted_languages[name].append({"id": lang_id, "version": version})
        # 更新缓存文件
        with open(CACHE_FILE, "w") as f:
            json.dump({"timestamp": time.time(), "data": formatted_languages}, f)
        return formatted_languages
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        # 如果API请求失败且有缓存文件，则返回缓存数据
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                cached_data = json.load(f)
                print("Using cached data due to API error.")
                return cached_data["data"]
        return None

def _get_formatted_languages_dict_():
    """
    从 Judge0 API 获取语言列表并格式化为以语言名为键的字典。
    使用文件缓存结果，并根据指定的时间间隔更新缓存。
    """
    # 检查缓存文件是否存在以及是否过期
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            try:
                cached_data = json.load(f)
                timestamp = cached_data.get("timestamp", 0)
                if time.time() - timestamp < UPDATE_INTERVAL:
                    print("Using cached languages data.")
                    return cached_data["data"]
                else:
                    print("Cached data is outdated.")
                    return _fetch_languages_from_api_()
            except json.JSONDecodeError:
                print("Error decoding cached data.")
                return _fetch_languages_from_api_()
    else:
        print("Cache file not found.")
        return _fetch_languages_from_api_()

def _normalize_lang_name_(query_name):
    """
    规范化语言名称
    """
    name_mapping = {
        "c#": "csharp",
        "objective-c": "objective-c",
        "objectivec": "objective-c",
        "plain text": "plain text",
        "visual basic.net": "visual basic.net",
        "visual basic net": "visual basic.net",
        "vb.net": "visual basic.net",
        "objc": "objective-c",
    }
    return name_mapping.get(query_name, query_name)
    
def _match_lang_name_(query_name, lang_name_lower):
    """
    判断语言名称是否匹配
    """
    if query_name == lang_name_lower:
        return True
    if query_name == "c++" and "c++" in lang_name_lower:
        return True
    if query_name == "c" and lang_name_lower.startswith("c "):
        return True
    if query_name == "csharp" and "c#" in lang_name_lower:
        return True
    if query_name == "objective-c" and ("objective-c" in lang_name_lower  or "Objective-C" in lang_name_lower):
         return True
    if query_name == "plain text" and "plain text" in lang_name_lower:
        return True
    if query_name == "visual basic.net" and "visual basic.net" in lang_name_lower:
        return True
    return False
    
def _match_lang_version_(query_name, query_version, lang_version):
    """
    判断版本是否匹配
    """
    if not query_version:
        return True
    if query_version == lang_version:
        return True
    if lang_version.startswith(query_version):
        return True
    if query_name == "c++" and query_version == "14" and "gcc 8" in lang_version.lower():
        return True
    if query_name == "c" and query_version == "7" and "gcc 7" in lang_version.lower():
        return True
    return False

def _find_best_lang_match_(query):
    """
    根据查询字符串在语言字典中找到最佳匹配的语言ID
    """
    global _language_cache
    if _language_cache is None:
         _language_cache = _get_formatted_languages_dict_()
    if not _language_cache:
        return None

    query = query.lower()
    matches = []

    # 1. 分离语言名称和版本
    match = re.match(r"([a-z#\.\s]+)(\+*)(\d*\.?\d*)?", query)
    if not match:
        return None

    query_name, plus_signs, query_version = match.groups()
    query_name = query_name.strip()
    query_version = query_version.strip()

    # 2. 特殊处理 C/C++ 和规范化语言名称
    if query_name == "c" and plus_signs:
        query_name = "c++"
    query_name = _normalize_lang_name_(query_name)

    for lang_name, versions in _language_cache.items():
        lang_name_lower = lang_name.lower()

        # 3. 名称匹配 
        if _match_lang_name_(query_name, lang_name_lower):
            for version_info in versions:
                lang_version = version_info["version"]

                # 4. 版本匹配
                if _match_lang_version_(query_name, query_version, lang_version):
                    matches.append((version_info, lang_version))

    if not matches:
        return None

    # 5. 排序和选择最佳匹配 (版本号排序优化)
    if len(matches) > 1:
        def sort_by_version(match_tuple):
            version_str = match_tuple[1]
            try:
                version_parts = re.findall(r'\d+', version_str)
                version_float = float(version_parts[0]) * 1000
                for i, part in enumerate(version_parts[1:]):
                    version_float += int(part) / (100 ** (i + 1))
                return version_float
            except ValueError:
                return 0

        best_match = max(matches, key=sort_by_version)[0]
    else:
        best_match = matches[0][0]
        
    if best_match:
        print(f"Query: '{query}', Best Match: {best_match}")
    else:
        print(f"Query: '{query}', No Match Found.")
    
    return best_match["id"]

def submit_code(source_code, language_id=100, stdin=None):
    """
    提交代码并获取执行结果。
    """
    url = f"{judge0_url}/submissions?base64_encoded=true&wait=true&fields={submit_fields}"

    payload = {
       "language_id": language_id,
       "source_code": source_code,
       "cpu_time_limit": cpu_time_limit,
       "cpu_extra_time": 1,
       "wall_time_limit": wall_time_limit
    }
    
    if stdin:
        payload["stdin"] = stdin
        
    payload = json.dumps(payload)

    headers = {
       'X-Auth-Token': judge0_api_key,
       'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    try:
      response.raise_for_status()
      return response.json()
    except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")
      return None


def format_submission_result(result):
    """
    解码 stdout, stderr 和 compile_output 并格式化其他字段。
    """
    if not result:
        return None
    formatted_result = result.copy()

    # 解码 stdout, stderr, compile_output
    for key in ["stdout", "stderr", "compile_output", "source_code", "message"]:
        if key in result and result[key]:
            try:
                cleaned_base64_string = result[key].replace('\r\n', '').replace('\n', '').replace('\r','')
                decoded_text = base64.b64decode(cleaned_base64_string).decode("utf-8")
                # 对stdout进行长度限制
                if key == "stdout" and len(decoded_text) > MAX_OUTPUT_LENGTH:
                    formatted_result[key] = decoded_text[:MAX_OUTPUT_LENGTH] + "..."
                else:
                    formatted_result[key] = decoded_text
            except UnicodeDecodeError as e:
                formatted_result[key] = f"Decode error: Invalid UTF-8 sequence at position {e.start}-{e.end}. Raw bytes: {result[key][e.start:e.end]}"
            except Exception as e:
                formatted_result[key] = f"Decode error: {e}"
        else:
            formatted_result[key] = ""

    # 格式化时间为中国时间
    china_tz = timezone(timedelta(hours=8))
    for key in ["created_at", "finished_at"]:
        if key in result and result[key]:
            try:
                datetime_obj = datetime.fromisoformat(result[key].replace("Z", "+00:00"))
                china_time = datetime_obj.astimezone(china_tz)
                formatted_result[key] = china_time.strftime("%H:%M:%S")
            except ValueError as e:
                formatted_result[key] = f"Parse error: {e}"
    
    # 格式化内存单位
    if "memory" in result and result["memory"]:
        formatted_result["memory"] = f"{result['memory'] / 1024:.2f} KB"

    # 移除 status 的id，description。
    if "status" in formatted_result:
        formatted_result.pop("status")

    # 清理结果，移除空值
    cleaned_result = {}
    for key, value in formatted_result.items():
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        if value == 0:
            cleaned_result[key] = value
            continue
        if value:
            cleaned_result[key] = value

    if 'language' in cleaned_result and isinstance(cleaned_result['language'], dict):
        cleaned_result['language'] = cleaned_result['language'].get('name', '')

    return cleaned_result


def base64_code(source_code, stdin=None):
    """
    对源代码进行 Base64 编码
    """

    encoded_source_code = base64.b64encode(source_code.encode("utf-8")).decode("utf-8")
    result = {"source_code": encoded_source_code}
    if stdin:
        encoded_stdin = base64.b64encode(stdin.encode("utf-8")).decode("utf-8")
        result["stdin"] = encoded_stdin

    return result


VALID_LANGUAGES = [
    "python3", "python2", "Assembly", "Bash", "C", "C++", "Clojure", "C#", "COBOL", 
    "Common Lisp", "D", "Elixir", "Fortran", "Go", "Groovy", "Haskell", "Java",
    "JavaScript", "Kotlin", "Lua", "OCaml", "Octave", "Pascal", "Perl", "PHP", 
    "Plain Text", "Python", "Python2", "R", "Ruby", "Rust", "Scala", "SQL", "Swift",
    "TypeScript", "Visual Basic.Net"
]
def llm_code_generator(query: str) -> dict:
    """使用 LLM 生成代码并格式化输出"""
    url = f"{openai_base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json",
    }
    print(f"Generating code for: {query}")

    data = {
        "model": "gemini-exp-1206",
        "temperature": 0,
        "messages": [
            {
                "role": "system",
                "content": f"""# Role Definition
                You are a professional code processor responsible for transforming user requirements into precise, executable code, ensuring it can be successfully submitted and run on the Judge0 platform. You must strictly adhere to Judge0's environment and rules, generating concise, efficient, and error-free programs.

                # Core Principles

                ## 1. Input Handling
                - Standard input (stdin) is passed as is, without any modifications or preprocessing.
                - No newline characters are automatically added.
                - The program should gracefully handle potentially empty inputs, avoiding crashes.

                ## 2. Code Generation
                - Strictly follow user requirements, accurately implementing the functionality described by the user.
                - Code should be concise, efficient, without comments, and compact.
                - Avoid unnecessary processing, handling only essential operations.
                - If the user directly provides code, only perform necessary formatting; do not modify code logic or content.
                - Generate code that is as compatible as possible with various evaluation environments, such as using common input/output methods.

                ## 3. Environment Constraints
                - Third-party libraries are prohibited. For example, using urllib instead of requests in Python
                - Avoid over-reliance on specific environments:
                    - Use standardized APIs whenever possible.
                    - Avoid relying on the Node.js environment; use standard JavaScript or TypeScript APIs, unless environment support is ensured.
                    - In Java, do not use `System.console()` to read input; use `Scanner`.
                - Consider resource (time, memory) limitations when generating code. Avoid infinite loops, recursion overflows, etc.

                # Considerations
                - **Error Handling:**
                    - Programs should not crash due to errors.
                    - Use mechanisms like `try...catch` to catch potential exceptions.
                    - When errors occur, output error messages to standard output or standard error output, but avoid directly throwing exceptions.
                - **Performance:**
                    - Code should be as efficient as possible.
                    - Avoid algorithms with high time complexity.
                    - Avoid issues like memory leaks.
                    - When testing code, pay attention to `wall_time`; even if `time` is small, a large `wall_time` can still lead to timeouts.
                - **Specific APIs:** Not all standard library APIs are available in all Judge0 environments. For example, `System.console()` in Java usually returns `null` in the Judge0 environment. Avoid using these environment-specific APIs; use common methods instead.
                - **Newline Characters:** Some languages, like C/C++, automatically add newline characters with `println`. However, some languages like Rust do not automatically add newline characters with `print`; ensure you add them according to the problem requirements.
                - **Special handling**: js should use standard js functions and use process.stdin to read standard input. In TypeScript, avoid using `require`. Read input through `process.stdin`, use type declarations to resolve type issues, and output using the standard `console.log`.It is necessary to add the declare declaration at the beginning of the code to resolve TypeScript type checking issues.
                - The default time zone is UTC.  The China time zone needs to be converted (UTC+8) `timedelta(hours=8)`

                Strictly  return a json object, should be like this {{'code':'python code', 'language':'python3', 'stdin':'standard input'}}.  
                The 'language' field must be one of the following: {', '.join(VALID_LANGUAGES)}. 
                only output the code in json format.Do not output any explanations. """
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "language": {"type": "string", "enum": VALID_LANGUAGES},
                    "stdin": {"type": "string", "description": "optional standard input"}
                },
                "required": ["code", "language"],
                "additionalProperties": False,
            }
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        print(response_json)

        if "choices" in response_json and len(response_json["choices"]) > 0:
            message = response_json["choices"][0].get("message")
            if message and "content" in message:
                content = message["content"]
                try:
                    # 尝试解析 JSON
                    return json.loads(content)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON content: {e}. Content: {content}")
                    return None
            else:
                print("Invalid response: 'message' or 'content' key missing.")
                return None
        else:
            print("Invalid response: 'choices' key missing or empty.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


@tool(parse_docstring=True)
def code_generation_running(query: str) -> str:
    """Write code as required and run it, or run user code

    Args:
        query: Natural language description of the code requirement, e.g. "write a C program to sum numbers from 1 to 100"
    """
    try:
        generated = llm_code_generator(query)
        if not generated:
            return "代码生成失败，无法获取代码生成结果。"
        
        source_code = generated.get('code')
        language = generated.get('language')
        stdin = generated.get('stdin')
        
        if not source_code or not language:
            return "代码生成结果不完整，缺少必要的代码或语言信息。"
        
        language_id = _find_best_lang_match_(language)
        if language_id is None:
            return f"未找到匹配的编程语言：{language}"

        base64_result = base64_code(source_code, stdin)
        base64_source_code = base64_result["source_code"]
        base64_stdin = base64_result.get("stdin")
        
        result = submit_code(base64_source_code, language_id, base64_stdin)
        if not result:
            return "代码提交失败，无法获取执行结果。"
            
        formatted_result = format_submission_result(result)
        if not formatted_result:
            return "代码执行结果格式化失败。"
        
        return {
            "source_code": source_code,
            "language": language,
            "execution_result": formatted_result
        }
        
    except Exception as e:
        return f"代码执行过程中发生错误: {str(e)}"

tools = [code_generation_running]

# print(code_generation_running("""编写一个循环打印十次标准输入的go程序，
# 标准输入为你好世界"""))
# print(code_generation_running("编写一个循环打印十次标准输入的python3程序，标准输入为你好世界"))
# print(code_generation_running("编写一个循环打印十次标准输入的python2程序，标准输入为你好世界"))
# print(code_generation_running("编写一个程序，标准输入为你好世界，然后使用汇编语言(Assembly)循环打印十次该输入"))
# print(code_generation_running("编写一个Bash脚本，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个C程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个C++程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Clojure程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个C#程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个COBOL程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Common Lisp程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个D程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Elixir程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个F#程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Fortran程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Groovy程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Haskell程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Java程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个JavaScript程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Kotlin程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Lua程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个OCaml程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Octave程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Pascal程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Perl程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个PHP程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个输出 'Hello, World!' 的Plain Text文件")) # Plain Text 没有标准输入的概念
# print(code_generation_running("编写一个Python程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Python2程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个R程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Ruby程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Rust程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Scala程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个查询所有名为 'users' 的表中所有记录的SQL语句")) # SQL 没有标准输入的概念
# print(code_generation_running("编写一个Swift程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个TypeScript程序，标准输入为你好世界，然后循环打印十次该输入"))
# print(code_generation_running("编写一个Visual Basic.Net程序，标准输入为你好世界，然后循环打印十次该输入"))
