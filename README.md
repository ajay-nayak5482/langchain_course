## Prerequisites

Before setting up the environment, ensure you have the following installed:

- **Python 3.11**  
    It is recommended to use Python 3.11 for compatibility. You can download it from the [official Python website](https://www.python.org/downloads/).

## Environment Setup Instructions

This project uses **uv** as the package manager. Follow the steps below to set up your development environment:

1. **Install uv**  
        ```bash
        pip install uv
        ```

2. **Initialize uv in your project**  
        ```bash
        uv init
        ```

3. **Add required packages**  
        Use the following command to add packages:  
        ```bash
        uv add PACKAGE_NAME
        ```
        For example:  
        ```bash
        uv add langchain
        ```

4. **Install additional dependencies**  
        Add other necessary packages such as:
        - `langchain-openai`
        - `python-dotenv`
        - `black`
        - `isort`

5. **Configure environment variables**  
        Create a `.env` file in your project directory and add the required key-value pairs. For example:
        ```
        OPENAI_API_KEY=YOUR_OPENAI_API_KEY
        ```
        Add any other environment variables as needed.

6. **Load environment variables in your code**  
        Import and use `dotenv` to load environment variables:
        ```python
        from dotenv import load_dotenv
        load_dotenv()
        ```
        After calling `load_dotenv()`, you can access your environment variables in your code.Environment Setup Instructions

This project uses **uv** as the package manager. Follow the steps below to set up your development environment:

1. **Install uv**  
    ```bash
    pip install uv
    ```

2. **Initialize uv in your project**  
    ```bash
    uv init
    ```

3. **Add required packages**  
    Use the following command to add packages:  
    ```bash
    uv add PACKAGE_NAME
    ```
    For example:  
    ```bash
    uv add langchain
    ```

4. **Install additional dependencies**  
    Add other necessary packages such as:
    - `langchain-openai`
    - `python-dotenv`
    - `black`
    - `isort`

5. **Configure environment variables**  
    Create a `.env` file in your project directory and add the required key-value pairs. For example:
    ```
    OPENAI_API_KEY=YOUR_OPENAI_API_KEY
    ```
    Add any other environment variables as needed.

6. **Load environment variables in your code**  
    Import and use `dotenv` to load environment variables:
    ```python
    from dotenv import load_dotenv
    load_dotenv()
    ```
    After calling `load_dotenv()`, you can access your environment variables in your code.

    ## Usage Example

    The project provides a `summarize_text` method in `main.py` to quickly summarize input text using LangChain and OpenAI. 

    **Example usage:**
    ```python
    from main import summarize_text

    text = "Your long text goes here."
    summary = summarize_text(text)
    print(summary)
    ```

    Replace `"Your long text goes here."` with the content you want to summarize. The function will return a concise summary of the input text.

    Make sure your environment variables (such as `OPENAI_API_KEY`) are set up as described above before running the code.


### Explanation of `summarize_text` Method

The `summarize_text` function in `main.py` typically follows these steps (based on standard LangChain usage):

1. **Load the Language Model (LLM):**  
    The method initializes an LLM (like OpenAI’s GPT) using your API key.  
    *Significance:* This step sets up the connection to the model that will generate the summary.

2. **Configure the Prompt:**  
    The function prepares a prompt template that instructs the LLM to summarize the input text.  
    *Significance:* Crafting a clear prompt ensures the model understands the task (summarization) and produces relevant output.

3. **Set the Temperature Parameter:**  
    The temperature parameter controls the randomness of the model’s output.  
    - Low values (e.g., 0.0–0.3): Output is more deterministic and focused.  
    - High values (e.g., 0.7–1.0): Output is more creative and varied.  
    *Significance:* For summarization, a lower temperature is often preferred for concise and accurate summaries.

4. **Run the Chain (using LCEL):**  
    The method uses LangChain’s Expression Language (LCEL) to compose and execute the summarization chain.  
    *Significance:* LCEL allows you to declaratively build and run chains of operations (like prompt formatting, LLM calls, and output parsing) in a readable and modular way.

5. **Return the Summary:**  
    The function extracts and returns the summary from the LLM’s response.
    
---
    
## Ollama Setup and Running Local LLMs

1. **Download and Install Ollama**  
    Visit [Ollama's official website](https://ollama.com/) to download and install the application for your operating system.

2. **Browse and Select Models**  
    Go to the [Ollama models page](https://ollama.com/search) to search for available models (e.g., `gemma4:e2b`, `gemma3:270m`, `gemma3:1b`, etc.).

3. **Download a Model**  
    Use the following command to download your chosen model (replace `MODEL_NAME` with the actual model name, e.g., `gemma3:270m`):
    ```bash
    ollama pull MODEL_NAME
    ```

4. **Run a Model Locally**  
    Start a local instance of a model with:
    ```bash
    ollama run MODEL_NAME
    ```
    Example:
    ```bash
    ollama run gemma3:270m
    ```

5. **List Installed Models**  
    To see all models installed locally, run:
    ```bash
    ollama list
    ```

---

## LangSmith Setup

1. **Sign Up and Log In**  
    Go to [LangSmith](https://smith.langchain.com/) and log in using your preferred method (e.g., Google account).

2. **Create a New Project**  
    On the Home page, create a new project for tracing. Fill in the required project details.

3. **Configure LangSmith for Tracing**  
    After creating the project, follow the on-screen instructions to set up LangSmith tracing.

4. **Generate API Key and Set Environment Variables**  
    Click "Generate API Key" and copy the environment variables provided.

    - **Note:** By default, the API endpoint is set for the USA region. If you are outside the USA, update your environment variable as follows:
        ```
        LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com
        ```
        This helps avoid authentication errors.

5. **Start Tracing**  
    Once the environment variables are set, tracing will begin automatically—no further code changes are required.



