from ddgs import DDGS
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import os

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GROQ_API_KEY")

client = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

os.makedirs("Data", exist_ok=True)

try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
    messages = []

def GoogleSearch(query):

    Answer = f"The search results for {query} are:\n[start]\n"

    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
            found = False

            for r in results:
                found = True
                title = r.get("title", "No title")
                body = r.get("body", "No description")
                link = r.get("href", "No link")

                Answer += f"Title: {title}\n"
                Answer += f"Description: {body}\n"
                Answer += f"Link: {link}\n\n"

            if not found:
                Answer += "No search results found.\n"

    except Exception as e:
        Answer += f"Search failed: {str(e)}\n"

    Answer += "[end]"
    return Answer

def AnswerModifier(Answer):

    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "system", "content": "Hii"},
    {"role": "system", "content": "Hello, how can i help you?"}
]

def Information():

    current_date_time = datetime.datetime.now()

    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"

    return data

def RealtimeSearchEngine(prompt):

    global SystemChatBot, messages

    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)

    messages.append({"role": "user", "content": prompt})

    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        top_p=1,
        stream=True
    )

    Answer = ""

    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.replace("</s>", "")

    messages.append({"role": "assistant", "content": Answer})

    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    return AnswerModifier(Answer)

if __name__ == "__main__":

    while True:
        user_input = input("Enter Your Question: ")

        if not user_input:
            continue

        print(RealtimeSearchEngine(user_input))
