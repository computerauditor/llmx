#!/usr/bin/env python3
import g4f
import sys
import time
import threading
from typing import List, Dict
import textwrap
import argparse
import itertools
import signal

# List of available models
AVAILABLE_MODELS = ["gpt-4", "gpt-4-turbo", "gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o",  
"claude-3-haiku", "claude-3-sonnet", "claude-3-5-sonnet", "claude-3-opus",  
"llama-3-70b", "llama-3-8b", "llama-2-13b", "llama-3.1-405b", "llama-3.1-70b", "llama-3.1-8b",  
"llamaguard-2-8b", "llamaguard-7b", "llama-3.2-90b",  
"mixtral-8x7b", "mixtral-8x22b", "mistral-7b",  
"qwen-1.5-7b", "qwen-1.5-14b", "qwen-1.5-72b", "qwen-1.5-110b", "qwen-2-72b",  
"gemma-2b", "gemma-2-9b", "gemma-2-27b",  
"gemini-flash", "gemini-pro", "deepseek",  
"mixtral-8x7b-dpo", "yi-34b", "wizardlm-2-8x22b", "solar-10.7b",  
"mythomax-l2-13b", "cosmosrp"]

# Define a refined set of Braille characters for smoother animation
braille_chars = ['⠸', '⠼', '⠧', '⠇', '⠙', '⠹', '⠼', '⠴']

def query_llm(prompt: str, model: str = "gpt-4o", conversation: List[Dict] = None) -> str:
    if not conversation:
        conversation = [
            {"role": "system", "content": "You are a helpful assistant. Respond to the user's input or question."}
        ]
    conversation.append({"role": "user", "content": prompt})

    with LoadingIndicator():
        try:
            response = g4f.ChatCompletion.create(model=model, messages=conversation)
            formatted_response = format_response(response)
            return formatted_response
        except Exception as e:
            print(f"\nError occurred: {e}")
            return ""

class LoadingIndicator:
    def __enter__(self):
        self.loading = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.loading = False
        if self.thread:
            self.thread.join()
        print("\r" + " " * 20 + "\r", end='', flush=True)

    def _animate(self):
        """ Braille animation for smoother visual effect """
        for frame in itertools.cycle(braille_chars):
            if not self.loading:
                break
            sys.stdout.write(f'\r{frame} Processing...')
            sys.stdout.flush()
            time.sleep(0.1)

def format_response(response: List[Dict[str, str]] | str) -> str:
    if isinstance(response, list):
        return "\n".join(msg['content'] for msg in response if 'content' in msg)
    return str(response)

def print_wrapped_text(text: str, width: int = 80) -> str:
    """ Return formatted wrapped text for consistent display """
    wrapped_text = "\n".join("\n".join(textwrap.wrap(line, width=width)) for line in text.split("\n"))
    border = "-" * width
    return f"\nResponse:\n{border}\n{wrapped_text}\n{border}"

def list_models():
    print("Available models:")
    for i, model in enumerate(AVAILABLE_MODELS, 1):
        print(f"{i}. {model}")

def get_model_choice() -> str:
    # Limit the display to the first 10 models
    limited_models = AVAILABLE_MODELS[:10]
    
    print("Available models (first 10):")
    for i, model in enumerate(limited_models, 1):
        print(f"{i}. {model}")
    print("\nUse --list-models to view all available models.")
    
    while True:
        try:
            choice = input("\nEnter the number of the model you want to use: ")
            choice = int(choice)
            if 1 <= choice <= len(limited_models):
                return limited_models[choice - 1]
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(limited_models)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except EOFError:
            print("\nNo input available. Using default model (gpt-3.5-turbo).")
            return "gpt-3.5-turbo"

def read_input() -> str:
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return ""

def choose_model_with_piped_input() -> str:
    """Handle model selection even when input is piped."""
    if sys.stdin.isatty():
        return get_model_choice()
    else:
        sys.stdin = open('/dev/tty')  # Redirect stdin to allow user input for model selection
        return get_model_choice()

def restore_interactive_input():
    """Restores stdin to allow interactive conversation mode after piping."""
    if not sys.stdin.isatty():
        sys.stdin = open('/dev/tty')

def signal_handler(sig, frame):
    print("\nCtrl+C pressed. Exiting gracefully...")
    sys.exit(0)

def save_output_to_file(text: str, file_path: str):
    """Append the formatted output to a specified file."""
    try:
        with open(file_path, 'a') as file:
            file.write(text + "\n")
        print(f"Output appended to {file_path}")
    except IOError as e:
        print(f"Error saving to file: {e}")


def main():
    # Register the signal handler for Ctrl+C (SIGINT)
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Query an LLM with various input methods.")
    parser.add_argument("prompt", nargs="?", help="The prompt to send to the LLM.")
    parser.add_argument("-f", "--file", help="File containing context for the prompt.")
    parser.add_argument("-m", "--model", nargs='?', const='choose', help="Model to use for the query. Use without a value to choose from a list.")
    parser.add_argument("--list-models", action="store_true", help="List all available models and exit.")
    parser.add_argument("-nc", "--no-continuous", action="store_true", help="Disable continuous conversation mode.")
    parser.add_argument("-o", "--output", help="File to save the LLM response output.")
    args = parser.parse_args()

    if args.list_models:
        list_models()
        sys.exit(0)

    # Handle input from stdin or file
    input_content = read_input()
    if not input_content and args.file:
        try:
            with open(args.file, 'r') as f:
                input_content = f.read().strip()
        except IOError as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

    # Determine the prompt
    if args.prompt:
        prompt = f"{input_content}\n\n{args.prompt}" if input_content else args.prompt
    elif input_content:
        prompt = input_content
    else:
        prompt = input("Enter your prompt: ")

    if not prompt:
        print("Error: No input provided. Please provide a prompt, pipe in content, or specify a file.")
        sys.exit(1)

    # Model selection logic
    model = "gpt-3.5-turbo"  # Default model
    if args.model == 'choose':
        model = choose_model_with_piped_input()  # Ask for model even if input is piped
    elif args.model in AVAILABLE_MODELS:
        model = args.model

    conversation = []  # Initialize conversation history

    # First query with the initial prompt
    response = query_llm(prompt, model=model, conversation=conversation)
    conversation.append({"role": "assistant", "content": response})

    # Format and print the output
    formatted_response = print_wrapped_text(response)

    # Print formatted response
    print(formatted_response)

    # Save to file if output flag is provided
    if args.output:
        save_output_to_file(formatted_response, args.output)

    # Restore interactive input for further conversation
    restore_interactive_input()

    # Continuous conversation mode
    if not args.no_continuous:
        print("\nEntering continuous conversation mode. Type 'exit' to end.")
        while True:
            try:
                next_prompt = input("You: ")
                if next_prompt.lower() == "exit":
                    print("Exiting chat...")
                    break
                response = query_llm(next_prompt, model=model, conversation=conversation)
                conversation.append({"role": "assistant", "content": response})

                # Format and print the response
                formatted_response = print_wrapped_text(response)
                print(formatted_response)

                # Save to file if output flag is provided
                if args.output:
                    save_output_to_file(formatted_response, args.output)
            except EOFError:
                print("\nExiting chat...")
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCtrl+C pressed. Exiting gracefully...")
        sys.exit(0)
