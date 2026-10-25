import os
from dotenv import load_dotenv
from openai import OpenAI



def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("No valid Environment Variable found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        )
    prompt = "why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role":"user",
                "content":prompt,
            }
        ],
    )
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")

    if response.usage is None:
        raise RuntimeError("Response Usage Property is None")
    else:
        print(f"Response tokens: {response.usage.completion_tokens}")
    
    
    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
