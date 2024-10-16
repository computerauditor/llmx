#!/usr/bin/env python3
import g4f
import sys
import time
import threading
from typing import List, Dict
import textwrap
import argparse

def query_llm(prompt: str, context: str = "") -> None:
    model = "gpt-3.5-turbo"  # You can specify your model over here
    messages = [
        {"role": "system", "content": "You are a helpful assistant. If provided with additional context, use it to inform your response."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {prompt}" if context else prompt}
    ]
    
    with LoadingIndicator():
        try:
            response = g4f.ChatCompletion.create(model=model, messages=messages)
            formatted_response = format_response(response)
            print_wrapped_text(formatted_response)
        except Exception as e:
            print(f"\nError occurred: {e}")

class LoadingIndicator:
    def __init__(self):
        self.loading = False
        self.thread = None

    def __enter__(self):
        self.loading = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.loading = False
        if self.thread:
            self.thread.join()
        print("\r" + " " * 20 + "\r", end='', flush=True)  # Clear loading message

    def _animate(self):
        chars = "|/-\\"
        idx = 0
        while self.loading:
            print(f"\rProcessing {chars[idx % len(chars)]}", end='', flush=True)
            idx += 1
            time.sleep(0.1)

def format_response(response: List[Dict[str, str]] | str) -> str:
    if isinstance(response, list):
        return "\n".join(msg['content'] for msg in response if 'content' in msg)
    return str(response)

def print_wrapped_text(text: str, width: int = 80) -> None:
    print("\nResponse:")
    print("-" * width)
    for line in text.split('\n'):
        print("\n".join(textwrap.wrap(line, width=width)))
    print("-" * width)

def main():
    parser = argparse.ArgumentParser(description="Query an LLM with optional context from a file.")
    parser.add_argument("prompt", nargs="?", help="The prompt to send to the LLM.")
    parser.add_argument("-f", "--file", help="File containing context for the prompt.")
    args = parser.parse_args()

    context = ""
    if args.file:
        try:
            with open(args.file, 'r') as f:
                context = f.read().strip()
        except IOError as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

    if not sys.stdin.isatty():
        # If there's input from a pipe, use it as context
        context = sys.stdin.read().strip()

    prompt = args.prompt if args.prompt else input("Enter your prompt: ")

    if not prompt:
        print("Please provide a prompt.")
        sys.exit(1)
    
    query_llm(prompt, context)

if __name__ == "__main__":
    main()