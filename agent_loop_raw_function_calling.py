from dotenv import load_dotenv
import ollama
from langsmith import traceable

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
    discount_percentages = {
        "gold": 0.23,
        "silver": 0.12,
        "bronze": 0.05
    }
    discount = discount_percentages.get(discount_tier, 0.0)
    return round(price - (price * discount), 2)

# Difference 2: Without @tool, we must MANUALLY define the JSON schema for each function.
# This is exactly what LangChain's @tool decorator generates automatically
# from the function's type hints and docstring.
tools_for_llm = [
    {
        "type": "function",
        "function": {
            "name": "get_product_price",
            "description": "Look up the price of a product in the catalog.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "The product name, e.g. 'laptop', 'headphones', 'keyboard'",
                    },
                },
                "required": ["product_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "apply_discount",
            "description": "Apply a discount tier to a price and return the final price. Available tiers: bronze, silver, gold.",
            "parameters": {
                "type": "object",
                "properties": {
                    "price": {"type": "number", "description": "The original price"},
                    "discount_tier": {
                        "type": "string",
                        "description": "The discount tier: 'bronze', 'silver', or 'gold'",
                    },
                },
                "required": ["price", "discount_tier"],
            },
        },
    },
]


# NOTE: Ollama can also auto-generate these schemas if you pass the functions
# directly as tools (similar to LangChain's @tool decorator):
#   tools_for_llm = [get_product_price, apply_discount]
# However, this requires your docstrings to follow the Google docstring format
# so Ollama can parse parameter descriptions from the Args section. For example:
#   def get_product_price(product: str) -> float:
#       """Look up the price of a product in the catalog.
#
#       Args:
#           product: The product name, e.g. 'laptop', 'headphones', 'keyboard'.
#
#       Returns:
#           The price of the product, or 0 if not found.
#       """
# We keep the manual JSON version here so you can see what @tool hides from you.

# --- Helper: traced Ollama call ---
# Difference 3: Without LangChain, we must manually trace LLM calls for LangSmith.


@traceable(name="Ollama Chat", run_type="llm")
def ollama_chat_traced(messages):
    return ollama.chat(model=MODEL_NAME, tools=tools_for_llm, messages=messages)

@traceable(name="Agent Loop", run_type="agent")
def run_agent(question: str):
    print(f"Question: {question}")
    print("_" * 60)
    tools_dict = {
        "get_product_price": get_product_price,
        "apply_discount": apply_discount
    }
    messages = [
        {
            "role": "system",
             "content": (
                "You are a helpful shopping assistant. "
                "You have access to a product catalog through tools "
                "and ability to apply discounts using another tools.\n\n"
                "STRICT RULES — you must follow these exactly:\n"
                "1. NEVER guess or assume any product price. "
                "You MUST call get_product_price first to get the real price.\n"
                "2. Only call apply_discount AFTER you have received "
                "a price from get_product_price. Pass the exact price "
                "returned by get_product_price — do NOT pass a made-up number.\n"
                "3. NEVER calculate discounts yourself using math. "
                "Always use the apply_discount tool.\n"
                "4. If the user does not specify a discount tier, "
                "ask them which tier to use — do NOT assume one."
            )
        },
        {"role": "user", "content": question},
    ]

    for iteration in range(MAX_ITERATIONS+1):
        print(f"Iteration {iteration + 1}:")
        response = ollama_chat_traced(messages)
        ai_message = response.message
        tool_calls = ai_message.tool_calls or []

        if not tool_calls:
            print(f"Model response: {ai_message.content}")
            return ai_message.content
        tool_call = tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = tool_call.function.arguments        

        print(f"Model called tool: {tool_name} with args: {tool_args}")
        tool_to_call = tools_dict.get(tool_name)
        if not tool_to_call:
            print(f"Tool {tool_name} not found.")
            return None
        tool_response = tool_to_call(**tool_args)
        print(f"Tool response: {tool_response}")

        messages.append(ai_message)
        messages.append(
            {"role": "user", "content": str(tool_response)}
        )

    print("Max iterations reached without a final answer.")
    return None

if __name__ == "__main__":
    run_agent("What is the price of a laptop after applying a gold discount?")