import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI




def main() -> None:
    #.env Varibalen Laden
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("No valid Environment Variable found")

    #Create new OpenAI client and change base url to OpenRouter instead of OpenAI-default
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        )
    
    #User Input
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Type in your prompt")
    args = parser.parse_args()

    #Call the client.chat.completions.create() Method to get a response
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role":"user",
                "content":args.user_prompt,
            }
        ],
    )
    
    print(f"User prompt: {args.user_prompt}")

    #Print used tokens
    print(f"Prompt tokens: {response.usage.prompt_tokens}")

    if response.usage is None:
        raise RuntimeError("Response Usage Property is None")
    else:
        print(f"Response tokens: {response.usage.completion_tokens}")
    
    #Print response to the prompt
    print("Response:")
    print(response.choices[0].message.content)




if __name__ == "__main__":
    main()

