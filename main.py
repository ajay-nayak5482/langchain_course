import os
from dotenv import load_dotenv #load_dotenv is a function that loads environment variables from a .env file into the environment variables of the operating system. This allows you to keep sensitive information, such as API keys, out of your code and instead store them in a separate file.
#import promopt template and openaicha models well as the chain that we will use to summarize given text
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_ollama.chat_models import ChatOllama

# Load environment variables from .env file
load_dotenv()

def generate_password(input_password: str) -> AIMessage:
    password_prompt_format = """You are an expert password generator.

        Your task is to generate exactly 3 strong, readable, and memorable passwords based on the user's input password.

        Input:
        - Input password: {input_password}

        Rules:
        - Use the input password as a base inspiration, so the generated passwords are related to it and not completely different.
        - Do not repeat the input password exactly.
        - Do not make only trivial changes such as adding "123" or a single symbol at the end.
        - Each generated password must preserve some recognizable part, pattern, sound, or structure from the input password while still improving security.
        - Generate exactly 3 passwords and nothing else.
        - Each password length must be between 8 and 12 characters only.
        - Each password should include a balanced mix of uppercase letters, lowercase letters, numbers, and optionally 1 special character.
        - Keep each password readable and memorable; avoid fully random gibberish unless necessary.
        - Avoid common weak patterns, repeated characters, keyboard walks, dates, names, and predictable suffixes.
        - If the input password is leaked, weak, or very short, transform it into a stronger version while still keeping some resemblance.
        - Ensure all 3 passwords are unique.

        Output format:
        - Return only 3 passwords, one per line.
        - Do not include explanations, labels, numbering, bullet points, or extra text."""


    # Create a prompt template for summarization
    prompt_template = PromptTemplate(input_variables=["input_password"], template=password_prompt_format)

    # Create an instance of the ChatOpenAI model
    # temperature is a parameter that controls the randomness of the model's output. A higher temperature will result in more random output, while a lower temperature will result in more deterministic output. In this case, we set it to 0.7 to allow for some creativity in the summary while still maintaining coherence.
    # temperature 0 to 0.3 means the model will generate more focused and deterministic responses, while a temperature of 0.7 allows for more creativity and variability in the output. This can be useful for tasks like summarization, where you want the model to generate a concise summary that captures the main points of the input text, but you also want it to be able to generate different summaries each time it is run.
    # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
    llm = ChatOllama(model="gemma4:e2b", temperature=0.2)
    # llm = ChatOllama(model="gemma3:270m", temperature=0)
    # llm = ChatOllama(model="gemma3:1b", temperature=0)

    # The | operator is used to chain together the prompt and the language model. This means that the output of the prompt will be passed as input to the language model, allowing us to generate a summary based on the formatted prompt.
    # its based on LCEL (LangChain Execution Language) which is a way to define a sequence of operations that can be executed by the language model. In this case, we are defining a chain that takes the formatted prompt as input and passes it to the language model to generate a summary.
    chain = prompt_template | llm 

    # Get the summary from the model
    response = chain.invoke(input={"input_password": input_password})

    return response

def generate_password1(input_password: str) -> AIMessage:

    char0 = input_password[0] if len(input_password) > 0 else "x"
    char1 = input_password[1] if len(input_password) > 1 else char0

    # Pre-compute a partial mutation in Python to anchor the model
    partial = input_password[:3].lower()

    password_prompt_format1 = """Input: cat
Output:
C@t5xRm2k
cA7t!nKp3
cAt3$wLz9

Input: moonlight
Output:
m00nL!ght4
M0onl1Gh@3
m0OnL!9htx

Input: robot
Output:
r0B0t!Kx3
R0b0T@j7n
r0b#T5wNk

Input: {input_password}
# passwords based on {input_password} starting with {partial}
Output:"""

    prompt_template = PromptTemplate(
        input_variables=["input_password", "partial"],
        template=password_prompt_format1
    )

    llm = ChatOllama(
        model="gemma3:1b",
        temperature=0.2,
        repeat_penalty=1.3,
        stop=["\n\n", "Input:", "#"]
    )

    chain = prompt_template | llm

    response = chain.invoke(input={
        "input_password": input_password,
        "partial": partial
    })

    return response

def summarize_text(text: str) -> AIMessage:
    summary_template = """
    given the information '{text}', provide the following: 
    1. A short summary
    2. two interesting findings from the text
    """    
    # Create a prompt template for summarization
    prompt_template = PromptTemplate(input_variables=["text"], template=summary_template)
    
    # Create an instance of the ChatOpenAI model
    # temperature is a parameter that controls the randomness of the model's output. A higher temperature will result in more random output, while a lower temperature will result in more deterministic output. In this case, we set it to 0.7 to allow for some creativity in the summary while still maintaining coherence.
    # temperature 0 to 0.3 means the model will generate more focused and deterministic responses, while a temperature of 0.7 allows for more creativity and variability in the output. This can be useful for tasks like summarization, where you want the model to generate a concise summary that captures the main points of the input text, but you also want it to be able to generate different summaries each time it is run.
    # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
    llm = ChatOllama(model="gemma4:e2b", temperature=0.2)

    # The | operator is used to chain together the prompt and the language model. This means that the output of the prompt will be passed as input to the language model, allowing us to generate a summary based on the formatted prompt.
    # its based on LCEL (LangChain Execution Language) which is a way to define a sequence of operations that can be executed by the language model. In this case, we are defining a chain that takes the formatted prompt as input and passes it to the language model to generate a summary.
    chain = prompt_template | llm 

    # Get the summary from the model
    summary = chain.invoke(input={"text": text})

    return summary

def main():
    print("Hello from langchain-course!")
    # print(f"Your API key is: {os.getenv('OPENAI_API_KEY')}")
    text = """Building LangChain for Mobile: How We Designed an On-Device AI Framework for iOS and Android

On-device AI is one of the most exciting shifts in mobile development. Apple Intelligence brings Foundation Models to iOS 26+. Google ships Gemini Nano via ML Kit on Android 14+. For the first time, powerful language models run natively on phones — no cloud, no latency, no privacy trade-offs.

But there’s a problem: these APIs are completely different.

On iOS, you write Swift with SystemLanguageModel and @Generable. On Android, you write Kotlin with GenerativeModel from ML Kit. If you want composable chains, memory management, or a pipeline DSL — the things that made LangChain transformative for cloud LLMs — you're on your own.
"""
    summary = summarize_text(text)
    print(f"Summary: {summary.content}")
    generated_password = generate_password1("Ajay")
    print(f"Generated Passwords: {generated_password.content}")

if __name__ == "__main__":
    main()
