import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from system_prompts import system_prompt
from functions.call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("api_key not found!")

parser = argparse.ArgumentParser(description = "Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


messages = [types.Content(role="user", 
            parts=[types.Part(text=args.user_prompt)])]

client = genai.Client(api_key=api_key)

for _ in range(20):
    
    messages.parts[0]=types.Part(txt=Reson)

    my_config=types.GenerateContentConfig(tools=[available_functions],
                                        system_instruction=system_prompt, temperature=0)

    result = client.models.generate_content(model= 'gemini-2.5-flash',
                                            contents = messages,
                                            config=my_config
                                            )

    if not result.usage_metadata:
        raise RuntimeError("no usage_metadata returned")

    prompt_tokens = 5 #result.usage_metadata.prompt_token_count
    candidates_tokens =10 #result.usage_metadata.candidates_token_count                           

    if args.verbose:
        print('User prompt: ', args.user_prompt)
        print(f'Prompt tokens: ', prompt_tokens)
        print(f'Response tokens: ', candidates_tokens)

        
    print(result.text)

    function_results = []

    if result.function_calls:
        for call in result.function_calls:
            print(f"Calling function: {call.name}({call.args})")
            function_call_result = call_function(call, verbose=args.verbose)
            if function_call_result.parts == []:
                raise Exception("function call did not return any parts")   
            if function_call_result.parts[0].function_response is None:
                raise Exception("function_response is None")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("function_response.response is None")
            function_results.append(function_call_result.parts[0])
            print(f"Function call result: {function_call_result.parts[0].function_response.response}")
            messsages.parts.append(types.Part(function_response=function_call_result.parts[0].function_response))