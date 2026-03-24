from groq import Groq
from dotenv import dotenv_values
from rich import print

env_vars = dotenv_values(".env")

GroqAPIKey = env_vars.get("GROQ_API_KEY")

client = Groq(api_key=GroqAPIKey)

funcs = [
    "exit",
    "open",
    "close",
    "play",
    "generate image",
    "system",
    "content",
    "google search",
    "youtube search",
    "reminder",
    "realtime",
    "general"
]

messages = []

preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation.
Do not answer any query, just decide what kind of query is given to you.
"""

ChatHistory = [
    ("user", "how are you?"),
    ("assistant", "general how are you?"),
    ("user", "do you like pizza?"),
    ("assistant", "general do you like pizza?"),
    ("user", "thanks, i really liked it"),
    ("assistant", "general thanks, i really liked it"),
    ("user", "chat with me"),
    ("assistant", "general chat with me"),
    ("user", "who is he?"),
    ("assistant", "general who is he?"),
    ("user", "tell me more about him"),
    ("assistant", "general tell me more about him"),
    ("user", "what's his net worth?"),
    ("assistant", "general what's his net worth?"),
    ("user", "who is indian prime minister"),
    ("assistant", "realtime who is indian prime minister"),
    ("user", "what is today's news"),
    ("assistant", "realtime what is today's news"),
    ("user", "tell me facebook's latest update"),
    ("assistant", "realtime tell me facebook's latest update"),
    ("user", "open chrome"),
    ("assistant", "open chrome"),
    ("user", "open chrome and firefox"),
    ("assistant", "open chrome, open firefox"),
    ("user", "close notepad"),
    ("assistant", "close notepad"),
    ("user", "open telegram and close whatsapp"),
    ("assistant", "open telegram, close whatsapp"),
    ("user", "open chrome and tell me about mahatma gandhi"),
    ("assistant", "open chrome, general tell me about mahatma gandhi"),
    ("user", "open youtube and play let her go"),
    ("assistant", "open youtube, play let her go"),
    ("user", "play afsanay by ys"),
    ("assistant", "play afsanay by ys"),
    ("user", "play let her go and play perfect"),
    ("assistant", "play let her go, play perfect"),
    ("user", "set a reminder at 9pm for dinner"),
    ("assistant", "reminder 9pm dinner"),
    ("user", "remind me on 20th jan at 11pm for my meeting"),
    ("assistant", "reminder 20th jan 11pm meeting"),
    ("user", "mute the system"),
    ("assistant", "system mute"),
    ("user", "volume up and unmute"),
    ("assistant", "system volume up, system unmute"),
    ("user", "write a leave application"),
    ("assistant", "content leave application"),
    ("user", "write python code for calculator"),
    ("assistant", "content python calculator code"),
    ("user", "search python tutorials on google"),
    ("assistant", "google search python tutorials"),
    ("user", "search django crash course on youtube"),
    ("assistant", "youtube search django crash course"),
    ("user", "what's the time now"),
    ("assistant", "general what's the time now"),
    ("user", "what is today's date"),
    ("assistant", "general what is today's date"),
    ("user", "bye jarvis"),
    ("assistant", "exit"),
    ("user", "goodbye"),
    ("assistant", "exit"),
]

def FirstLayerDMM(prompt: str):

    messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": preamble},
            *[
                {"role": r, "content": m}
                for r, m in ChatHistory
            ],
            *messages
        ],
        temperature=0.2,
        max_tokens=200
    )

    response = completion.choices[0].message.content

    if not response:
        return []

    response = response.replace("\n", "")
    response = response.split(",")

    response = [i.strip().lower() for i in response]

    final = []

    for task in response:
        for func in funcs:
            if task.startswith(func):
                final.append(task)
                break

    return final

if __name__ == "__main__":
    while True:
        user_input = input(">>> ")

        if not user_input:
            continue

        result = FirstLayerDMM(user_input)

        print(result)
