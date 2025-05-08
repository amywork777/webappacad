import os, openai, anthropic, traceback

PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

def ask_llm(prompt: str) -> str:
    try:
        print(f"Using LLM provider: {PROVIDER}")
        if PROVIDER == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not set in environment variables")
            
            print("Initializing Anthropic client...")
            client = anthropic.Anthropic(api_key=api_key)
            
            print("Sending request to Anthropic...")
            resp = client.messages.create(
                model="claude-3-sonnet-20240229",
                temperature=0,
                max_tokens=4096,
                messages=[{"role":"user","content":prompt}]
            )
            return resp.content[0].text
        
        # default: OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment variables")
        
        print("Initializing OpenAI client...")
        client = openai.OpenAI(api_key=api_key)
        
        print("Sending request to OpenAI...")
        resp = client.chat.completions.create(
            model="o3",
            messages=[{"role":"user","content":prompt}]
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"Error in ask_llm: {str(e)}")
        traceback.print_exc()
        raise ValueError(f"LLM API error: {str(e)}")