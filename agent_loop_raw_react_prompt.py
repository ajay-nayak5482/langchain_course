import inspect
from dotenv import load_dotenv
import re

from langsmith import traceable
import ollama

load_dotenv()

MAX_ITERATIONS = 5
MODEL_NAME = "qwen3:1.7b"

@traceable(run_type="tool")
def get_product_price(product_name: str) -> float:
    """Look up the price of a product in the catalog."""
    print(f"    >> Executing get_product_price(product='{product_name}')")
    prices = {
        "laptop": 999.0,
        "smartphone": 499.0,
        "headphones": 199.0,
        "keyboard": 89.50
    }
    return prices.get(product_name.lower(), 0.0)

@traceable(run_type="tool")
def apply_discount(price: float, discount_tier: str) -> float:
    """Apply a discount tier to a price and return the final price.
    Available tiers: bronze, silver, gold."""
    print(f"    >> Executing apply_discount(price={price}, discount_tier='{discount_tier}')")
    price = float(price)
    discount_percentages = {
        "gold": 0.23,
        "silver": 0.12,
        "bronze": 0.05
    }
    discount = discount_percentages.get(discount_tier, 0.0)
    return round(price - (price * discount), 2)

tools = {
        "get_product_price": get_product_price,
        "apply_discount": apply_discount
    }

def get_tool_descriptions(tools_dict):
    descriptions = []
    for name, func in tools_dict.items():
        origional_function = getattr(func, "__wrapped__", func)
        signature = inspect.signature(origional_function)
        docstring = inspect.getdoc(origional_function) or ""
        descriptions.append(f"{name}{signature} - {docstring}")

    retVal = "\n".join(descriptions)
    print(f"Tool descriptions for LLM:\n{retVal}")
    return retVal

tool_names = ", ".join(tools.keys())
print(f"Tool names for LLM: {tool_names}")

tool_descriptions = get_tool_descriptions(tools)

react_prompt = f"""
STRICT RULES — you must follow these exactly:
1. NEVER guess or assume any product price. You MUST call get_product_price first to get the real price.
2. Only call apply_discount AFTER you have received a price from get_product_price. Pass the exact price returned by get_product_price — do NOT pass a made-up number.
3. NEVER calculate discounts yourself using math. Always use the apply_discount tool.
4. If the user does not specify a discount tier, ask them which tier to use — do NOT assume one.

Answer the following questions as best you can. You have access to the following tools:

{tool_descriptions}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action, as comma separated values
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {{question}}
Thought:"""

@traceable(name="Ollama Chat", run_type="llm")
def ollama_chat_traced(model, messages, options):
    return ollama.chat(model=model, messages=messages, options=options)

@traceable(name="Agent Loop")
def run_agent(question: str):
    print(f"Question: {question}")
    print("_" * 60)
    prompt = react_prompt.format(question=question)
    scratchpad = ""
    
    
    

    for iteration in range(MAX_ITERATIONS+1):
        print(f"Iteration {iteration + 1}:")
        full_prompt = prompt + scratchpad
        response = ollama_chat_traced(
            model = MODEL_NAME,
            messages=[{"role": "user", "content": full_prompt}],
            options={"stop": ['\nObservation'], "temperature": 0},
        )

        output = response.message.content
        print(f"Model output:\n{output}")

        final_answer_match = re.search(r"Final Answer:\s*(.+)", output, re.IGNORECASE)
        if final_answer_match:
            final_answer = final_answer_match.group(1).strip()
            print(f"Final answer found: {final_answer}")
            return final_answer
        action_match = re.search(r"Action:\s*(.+)", output, re.IGNORECASE)
        action_input_match = re.search(r"Action Input:\s*(.+)", output, re.IGNORECASE)
        print(f"Extracted action: {action_match.group(1).strip() if action_match else 'None'}")
        print(f"Extracted action input: {action_input_match.group(1).strip() if action_input_match else 'None'}")

        if not action_match or not action_input_match:
            print("No action or action input found, treating output as final answer.")
            return output.strip()
        
        tool_name = action_match.group(1).strip()
        tool_args_raw = action_input_match.group(1).strip()
        tool_args = [arg.strip() for arg in tool_args_raw.split(",")]
        args = [x.split("=", 1)[-1].strip().strip("'\'") for x in tool_args]

        print(f"Model called tool: {tool_name} with args: {tool_args} and parsed args: {args}")
        tool_to_call = tools.get(tool_name)
        if not tool_to_call:
            observation = f"Tool {tool_name} not found. available tools: {list(str)(tools.keys())}"
            print(observation)
        else:
            observation = str(tool_to_call(*args))
            print(f"[Tool Result]: {observation}")

        scratchpad += f"{output}\nObservation:\n{observation}\nThought:"

    print("Max iterations reached without a final answer.")
    return None

if __name__ == "__main__":
    run_agent("What is the price of a laptop after applying a gold discount?")