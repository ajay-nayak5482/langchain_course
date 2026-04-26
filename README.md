# Environment Setup Instructions

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




