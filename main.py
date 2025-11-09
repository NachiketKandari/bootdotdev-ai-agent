from logging import exception
import os
from google import genai
from dotenv import load_dotenv
import argparse 
from google.genai import types
from functions.function_schemas import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from call_function import call_function
from config import SYSTEM_PROMPT
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Argument Parser for the AI Agent")
    parser.add_argument("prompt", type=str, help="Enter the Prompt")
    parser.add_argument("-v", "--verbose", dest="verbose",action='store_true', help="Enable Verbose" )

    args = parser.parse_args()
    if args.prompt.isspace() or len(args.prompt) == 0:
        raise SystemExit(1)

    messages = [
    types.Content(role="user", parts=[types.Part(text=args.prompt)]),
    ]

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
    )

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=messages,
        config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=SYSTEM_PROMPT
    )
    )
    if args.verbose:
        print(f"User prompt: {args.prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count} \nResponse tokens: {response.usage_metadata.candidates_token_count}")
    function_calls = response.function_calls
    if not function_calls:
        return response.text
    
    function_responses = []
    for function_call_part in function_calls:
        function_call_result = call_function(function_call_part, args.verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

if __name__ == "__main__":
    main()
