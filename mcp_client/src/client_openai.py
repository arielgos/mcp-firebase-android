from urllib import response
import requests
import uuid
import json
import openai
import re

MCP_URL = "http://host.docker.internal:8000/mcp"

def gen_id():
    return str(uuid.uuid4())

def call_mcp_sum(a: int, b: int) -> int:
    headers = {
            "Authorization": "Bearer gdg-santa-cruz",
            "Accept": "application/json, text/event-stream"
        }
    rid = gen_id()
    payload = {
        "id": rid,
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "add",
            "arguments":{"a": a, "b": b}
        }
    }
    response = requests.request("POST", MCP_URL, headers=headers, json=payload)
    text=response.text.replace("event: message"," ").replace("data: ","").strip()
    json_str = json.loads(text)
    return int(json_str["result"]["structuredContent"]["result"])

def chat_with_gemini(user_prompt: str):
    system_prompt = """
                    Eres un orquestador que puede usar una herramienta remota 'add(a, b)'.
                    Si el usuario te pide sumar, responde con el JSON:
                    {"tool": "add", "a": X, "b": Y}
                    Si no, responde normalmente.
                    """

    client = openai.OpenAI(
        base_url="http://host.docker.internal:8080/v1",
        api_key="lm-studio"
    )

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    text = completion.choices[0].message.content.strip()

    if 'tool.add' in text or ('"tool"' in text and '"add"' in text) : 
        clean = text.replace("<|channel|>", "").strip()
        clean = clean.replace("commentary ", "").strip()
        clean = clean.replace("<|message|>", "").strip()
        clean = clean.replace("<|constrain|>", "").strip()
        clean = clean.replace("to=", "").strip()
        clean = clean.replace("json", "").strip()
        clean = clean.replace("tool.", "").strip()
        clean = clean.replace("add", "").strip()
        clean = clean.replace("code", "").strip()
        tool_call = json.loads(clean)
        a = int(tool_call["a"])
        b = int(tool_call["b"])
        res = call_mcp_sum(a, b)
        return f"La suma de {a} + {b} = {res}"
    else:
        return text

if __name__ == "__main__":
    while True:
        msg = input("Tú: ")
        if not msg:
            break
        reply = chat_with_gemini(msg)
        print("MCP:", reply)
