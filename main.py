import os
import argparse
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from config import MAX_ITERS
from call_function import available_functions, call_function




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
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #Call the client.chat.completions.create() Method to get a response
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    #Print User Prompt
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    
    for _ in range(MAX_ITERS):
        try:
            outcome = generate_content(client, messages, args.verbose)
            if outcome:
                print(f"Final response: \n {outcome}")
                return
        except Exception as e:
            print(f"Errror in generate_content: {e}")

    print(f"Maximum iterations ({MAX_ITERS}) reached")
    sys.exit(1)

    
    




def generate_content(client: OpenAI, messages: list, verbose: bool):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
    )
    if not response.usage:
        raise RuntimeError("Response Usage Property is None")
    

    
    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    #Print response to the prompt
    print("Response:")
    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        return message.content

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        result_message = call_function(tool_call,verbose)
        
        if not result_message.get("content"):
            raise Exception("Error: Content is empty")
    
        if verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)
    return None



if __name__ == "__main__":
    main()

