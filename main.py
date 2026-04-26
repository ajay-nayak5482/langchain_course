import os
from dotenv import load_dotenv #load_dotenv is a function that loads environment variables from a .env file into the environment variables of the operating system. This allows you to keep sensitive information, such as API keys, out of your code and instead store them in a separate file.
#import promopt template and openaicha models well as the chain that we will use to summarize given text
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage

# Load environment variables from .env file
load_dotenv()



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
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

    # The | operator is used to chain together the prompt and the language model. This means that the output of the prompt will be passed as input to the language model, allowing us to generate a summary based on the formatted prompt.
    # its based on LCEL (LangChain Execution Language) which is a way to define a sequence of operations that can be executed by the language model. In this case, we are defining a chain that takes the formatted prompt as input and passes it to the language model to generate a summary.
    chain = prompt_template | llm 

    # Get the summary from the model
    summary = chain.invoke(input={"text": text})

    return summary

def main():
    print("Hello from langchain-course!")
    print(f"Your API key is: {os.getenv('OPENAI_API_KEY')}")
    text = "Your text to summarize goes here"
    summary = summarize_text(text)
    print(f"Summary: {summary.content}")

if __name__ == "__main__":
    main()
