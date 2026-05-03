from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

load_dotenv()

MAX_ITERATIONS = 5
MODEL_NAME = "qwen3:1.7b"

@tool
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

@tool
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

def run_agent(question: str):
    tools = [get_product_price, apply_discount]
    tools_dict = {tool.name: tool for tool in tools}
    llm = init_chat_model(f"ollama:{MODEL_NAME}", temperature=0.3)
    llm_with_tools = llm.bind_tools(tools)

    print(f"Question: {question}")
    print("_" * 60)

    messages = [        
        SystemMessage(
            content=(
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
        ),        
        HumanMessage(content=question),
    ]

    for iteration in range(MAX_ITERATIONS+1):
        print(f"Iteration {iteration + 1}:")
        response = llm_with_tools.invoke(messages)
        tool_calls = response.tool_calls

        if not tool_calls:
            print(f"Model response: {response.content}")
            return response.content
        tool_call = tool_calls[0]
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})
        tool_call_id = tool_call.get("id")

        print(f"Model called tool: {tool_name} with args: {tool_args}")
        tool_to_call = tools_dict.get(tool_name)
        if not tool_to_call:
            print(f"Tool {tool_name} not found.")
            return None
        tool_response = tool_to_call.invoke(tool_args)
        print(f"Tool response: {tool_response}")

        messages.append(response)
        messages.append(
            ToolMessage(content=str(tool_response), tool_call_id=tool_call_id)
        )

    print("Max iterations reached without a final answer.")
    return None

if __name__ == "__main__":
    run_agent("What is the price of a laptop after applying a gold discount?")