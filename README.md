![ss1](https://github.com/user-attachments/assets/236453c5-343e-4f80-a75c-2713e7f83493)![ss1](https://github.com/user-attachments/assets/2ff14eee-3fd4-4edd-9f8e-a33f528b819d)# LLMX

This Python script allows you to interact with a Language Model (LLM) through the command line. It supports providing context through files or piped input, making it versatile for various use cases.

![Screenshot from 2024-10-16 22-07-55](https://github.com/user-attachments/assets/6316a54a-eeb6-4a11-a228-4c1b773ff972)

## Features

- Query an LLM with a prompt
- Provide additional context through a file or piped input
- Loading indicator for better user experience
- Formatted and wrapped text output for improved readability
- Error handling for robustness

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/computerauditor/llmx
   cd llmx
   ```

2. Install the required dependencies:
   ```
   pip install -r requirement.txt
   ```

3. Make the script executable:
   ```
   chmod +x llmx.py
   ```

## Usage

The script can be used in several ways:

### 1. Interactive mode

If you run the script without a prompt, it will ask you to enter one:

```
python llmx.py
Enter your prompt: What is the meaning of life?
```

### 2. Basic prompt

```
python llmx.py "What is the capital of France?" # Use -nc if you don't want to ask follow up questions & -o to save the contents to a file
```

![ss2](https://github.com/user-attachments/assets/a52c46f8-d551-4e33-a80e-c39a4e3ddc0a)

### 3. Prompt with file context

```
python llmx.py -f code.txt "Please explain the function on line 33." -o output_file.txt
```

### 4. Prompt with piped input as context

```
cat code.txt | python llmx.py "Please see at line 33 where it says exec.func[1], what's the error?"
```

![ss1](https://github.com/user-attachments/assets/bffcfe67-dd39-41a7-ae70-ae6288510fa1)

### 5. Prompt with both file and piped input (file takes precedence)

```
cat additional_info.txt | python llmx.py -f code.txt "Explain the code considering the additional information."
```

## Command-line Arguments

- `prompt`: The question or instruction for the LLM (optional as a command-line argument)
- `-f, --file`: Path to a file containing context for the prompt
- `-o, --output`: Path to a save the contexts of the response
- `-nc, --no-continuous`: Disable continuous conversation mode
- `--list-models`: List all the available models
- `-m", "--model`: Model to use for the query. Use without a value to choose from a list 

## Notes

- If both file input and piped input are provided, the file input takes precedence.
- The script uses the g4f library to interact with the LLM. Make sure you have the necessary API credentials set up if required by the library.

## Contributing

- A big thanks to g4f team for providing the LLM clients!!!
- Contributions are welcome! Please feel free to submit a Pull Request.
