import os, openai, anthropic

PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

def ask_llm(prompt: str) -> str:
    if PROVIDER == "anthropic":
        client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"))
        resp = client.messages.create(
            model="claude-3-sonnet-20240229",
            temperature=0,
            max_tokens=4096,
            messages=[{"role":"user","content":prompt}]
        )
        return resp.content[0].text
    # default: OpenAI
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="o3", temperature=0,
        messages=[{"role":"user","content":prompt}]
    )
    return resp.choices[0].message.content