from dotenv import load_dotenv
load_dotenv()
from Travel_agent import run_agent
from langchain_core.messages import HumanMessage, AIMessage


def start_chat():
    print("--Travel Assistant is Online (type 'exit' to stop)--")
    chat = [AIMessage(content='Hi im your travel assistant'),
            HumanMessage(content='My name is amal francis')
    ]

    while True:

        user_input = input('You: ')
        if user_input.lower() in ['exit', 'quit', 'stop']:
            print('Assistant: Goodbye! Have a grate trip...')
            break
        try:

            response = run_agent(user_input )
            print(f"Assistant: {response}")

        except Exception as e:
            print(f"Assistant: Oops, I hit a sang. (Error: {e})")


if __name__== '__main__':
    start_chat()