import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

@tool
def calculator (a: float , b: float) -> str:
    """Useful for performing basic arithmetic calculations."""
    print("tool has been called.")
    return f"the sum of {a} and {b} is {a + b}"

def say_hello (name: str) -> str:
    """Useful for greeting"""
    print("tool has been called.")
    return f"Hello, {name}!, I hope you are doing well."

def main():
    # --- START: NECESSARY CHANGES ---

    # Ensure your .env file has your OPENROUTER_API_KEY
    if "OPENROUTER_API_KEY" not in os.environ:
        raise ValueError("OPENROUTER_API_KEY not found in .env file")

    model = ChatOpenAI(
        model="gpt 3.5-turbo",  # Or any other model from openrouter.ai/models
        temperature=0,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    # --- END: NECESSARY CHANGES ---


    # This part of your code is conceptually flawed but not a syntax error.
    # An agent with no tools can't do anything but chat.
    # Consider adding tools like the calculator example from the previous answer.
    tools = [calculator, say_hello ]
    agent_executor = create_react_agent(model, tools)

    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "quit":
            break
        print("\nAssistant: ", end="", flush=True)

        # There was a small typo in your stream call, it should be "messages" not "message"
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="", flush=True)
        print()

if __name__ == "__main__":
    main()