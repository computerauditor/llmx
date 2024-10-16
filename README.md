# LLM Query Script

This Python script allows you to interact with a Language Model (LLM) through the command line. It supports providing context through files or piped input, making it versatile for various use cases.

## Features

- Query an LLM with a prompt
- Provide additional context through a file or piped input
- Loading indicator for better user experience
- Formatted and wrapped text output for improved readability
- Error handling for robustness

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/llm-query-script.git
   cd llm-query-script
   ```

2. Install the required dependencies:
   ```
   pip install g4f
   ```

3. Make the script executable:
   ```
   chmod +x llm_query.py
   ```

## Usage

The script can be used in several ways:

### 1. Basic prompt

```
python llm_query.py "What is the capital of France?"
```

### 2. Prompt with file context

```
python llm_query.py -f code.txt "Please explain the function on line 33."
```

### 3. Prompt with piped input as context

```
cat code.txt | python llm_query.py "Please see at line 33 where it says exec.func[1], what's the error?"
```

### 4. Prompt with both file and piped input (file takes precedence)

```
cat additional_info.txt | python llm_query.py -f code.txt "Explain the code considering the additional information."
```

### 5. Interactive mode

If you run the script without a prompt, it will ask you to enter one:

```
python llm_query.py
Enter your prompt: What is the meaning of life?
```

## Command-line Arguments

- `prompt`: The question or instruction for the LLM (optional as a command-line argument)
- `-f, --file`: Path to a file containing context for the prompt

## Notes

- If both file input and piped input are provided, the file input takes precedence.
- The script uses the g4f library to interact with the LLM. Make sure you have the necessary API credentials set up if required by the library.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
