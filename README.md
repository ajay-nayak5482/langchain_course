# Project Python Scripts Overview

This project contains three Python scripts that demonstrate agent loops and function calling using LangChain, with the Qwen3:1.7B model running locally via Ollama. All scripts are designed to work with a local Ollama server and do not use OpenAI APIs. The environment is managed using `uv`, not `pip`.

## Setup Instructions

### Prerequisites

- **Python 3.10+** (recommended)
- **[uv](https://github.com/astral-sh/uv)** for environment and dependency management
- **[Ollama](https://ollama.com/)** installed and running locally with the `qwen3:1.7b` model pulled

### Installation Steps

1. **Clone the repository:**
    ```sh
    git clone <repo-url>
    cd langchain_course
    ```

2. **Create and activate a virtual environment using `uv`:**
    ```sh
    uv venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```sh
    uv pip install -r requirements.txt
    ```
    Or, if using a `pyproject.toml`:
    ```sh
    uv pip install .
    ```

4. **Ensure Ollama is running and the Qwen3:1.7B model is available:**
    ```sh
    ollama run qwen3:1.7b
    ```

### Example `pyproject.toml`

```toml
[project]
name = "langchain-course"
version = "0.1.0"
description = "Agent loop and function calling demos with LangChain and Qwen3:1.7B via Ollama"
requires-python = ">=3.10"

[project.dependencies]
langchain = "^0.1.0"
httpx = "^0.27.0"
ollama = "^0.1.0"
```

> **Note:** Adjust dependency versions as needed based on your actual `uv.lock` or `pyproject.toml`.

---
---

## 1. `agent_loop_function_calling.py`

**Purpose:**  
Implements an agent loop using LangChain's function calling features, interacting with the Qwen3:1.7B model through a local Ollama server.

**How it Works:**  
- Sets up a LangChain agent configured for the Ollama backend and Qwen3:1.7B.
- Processes user queries in a loop, invoking functions as needed.
- Manages agent state and responses across multiple turns.

---

## 2. `agent_loop_raw_function_calling.py`

**Purpose:**  
Shows a lower-level, manual approach to agent loops and function calling by directly interacting with the Ollama server and Qwen3:1.7B.

**How it Works:**  
- Sends HTTP requests directly to the Ollama server for function calls.
- Manages the agent loop, parses responses, and invokes functions as needed.
- Useful for understanding the mechanics of function calling with Ollama.

---

## 3. `agent_loop_raw_react_prompt.py`

**Purpose:**  
Implements an agent loop using the ReAct (Reasoning and Acting) prompting strategy, managing reasoning steps and tool use manually with Qwen3:1.7B via Ollama.

**How it Works:**  
- Constructs prompts following the ReAct pattern.
- Processes user input, generates reasoning steps, and selects actions/tools.
- Handles multi-step reasoning and tool invocation using the local Ollama server.

---
