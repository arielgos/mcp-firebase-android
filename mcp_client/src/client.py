import requests
import uuid
from google import genai
from google.genai import types

# 1. Cliente Gemini (ajusta a tu lib real / API key)
client = genai.Client(api_key="AIzaSyB4DEzXz-cVNYuGz55tSfQY2wRo850_WZ8")

MCP_URL = "https://c31ec0d41130.ngrok-free.app/mcp"

def gen_id():
    return str(uuid.uuid4())

def call_mcp_sum(a: int, b: int) -> int:
    headers = {"Authorization": "Bearer gdg-santa-cruz"}
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
    resp = requests.post(MCP_URL, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()

def chat_with_gemini(user_prompt: str):
    system_prompt = """
                    Eres un orquestador que puede usar una herramienta remota 'add(a, b)'.
                    Si el usuario te pide sumar, responde con el JSON:
                    {"tool": "add", "a": X, "b": Y}
                    Si no, responde normalmente.
                    """
    config = types.GenerateContentConfig(
            system_instruction=system_prompt,
        )

    result = client.models.generate_content(
        model="gemini-2.5-pro",
        contents= user_prompt,
        config=config,
    )

    text = result.text.strip()
    clean = text.strip().strip("`").replace("json", "", 1).strip()

    if '"tool"' in clean and '"add"' in clean:
        import json
        print("Detected tool call:", clean)
        tool_call = json.loads(clean)
        if tool_call.get("tool") == "add":
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
        print("Gemini+MCP:", reply)
