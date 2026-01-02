from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from tools.Flight_Search_Tool import search_flights
from tools.Hotel_recommendation_tool import recommend_hotel
from tools.Place_discovery_tool import discover_places
from tools.Weather_look_up_tool import weather_lookup_tool
from tools.Budget_estimation_tool import estimate_budget
import os

model = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    google_api_key=os.environ['GOOGLE_API_KEY'],
    temperature=0.1,
    max_tokens=1000,
    timeout=30
)

tools = [
    search_flights,
    recommend_hotel,
    discover_places,
    weather_lookup_tool,
    estimate_budget
]

agent = create_agent(model, tools=tools)
chat_history = []

prompt_template = ChatPromptTemplate.from_messages([
    ('system', "Answer the user's questions based on the context.", ),
    MessagesPlaceholder(variable_name="chat_history"),
    ('human', '{messages}'),
])

chain = prompt_template | agent


def run_agent(query):
    result = chain.invoke({
                           'messages': query,
                           'chat_history': chat_history
                           })
    chat_history.append(HumanMessage(content=query))

    final_answer = result['messages'][-1].content
    chat_history.append(AIMessage(content=final_answer))

    return final_answer

