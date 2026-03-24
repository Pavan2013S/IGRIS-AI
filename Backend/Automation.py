from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import playonyt, search
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

env_vars = dotenv_values(".env")

GROQ_API_KEY = env_vars.get("GROQ_API_KEY") or ""

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric","Z0LcW","gsrt vk_bk FzWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc","05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt","sXLaOe",
            "LWkfKe","VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"

client = Groq(api_key=GROQ_API_KEY)

professional_response = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you wish.",
    "I'm here to assist you with anything else you may need, so please don't hesitate to ask.",
]

messages = []

SystemChatBot = [
    {"role": "system", "content": f"Hello, I am {env_vars.get('Username','Boss')}, You're a content writer. You have to write content like letters, emails, applications, codes, etc. about any topic given to you. You have to write content in a professional way and make sure to use proper grammar, full stops, commas, question marks, etc. Just write the content and do not provide any notes in the output."}
]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):

    def OpenNotepad(File):
        default_text_editor = "notepad.exe"
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        messages.append({"role": "system", "content": f"{prompt}"})

        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=SystemChatBot + messages,
                max_tokens=3000,
                temperature=0.7,
                stream=True,
                stop=None
            )

            Answer = ""

            for chunk in completion:
                if chunk.choices[0].delta and chunk.choices[0].delta.content:
                    Answer += chunk.choices[0].delta.content

            Answer = Answer.replace("</s>", "")
            messages.append({"role": "assistant", "content": Answer})
            return Answer

        except Exception as e:
            print(f"[red]Groq Error:[/red] {e}")
            return "Error generating content."

    Topic = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    os.makedirs("Data", exist_ok=True)

    filepath = rf"Data\{Topic.lower().replace(' ','')}.txt"

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    OpenNotepad(filepath)

    return True

def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYouTube(Query):
    playonyt(Query)
    return True

def OpenApp(app, sess=requests.Session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:

        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {'User-Agent': useragent}
            response = sess.get(url, headers=headers)

            if response.status_code == 200:
                return response.text

            return None

        html = search_google(app)

        if html:
            links = extract_links(html)
            if links:
                webopen(links[0])

        return True

def CloseApp(app):
    if "chrome" in app:
        return True
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

def System(command):

    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute")

    def volumeup():
        keyboard.press_and_release("volume up")

    def volumedown():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volumeup()
    elif command == "volume down":
        volumedown()

    return True

async def TranslateAndExecute(commands):
    funcs = []

    for command in commands:

        if command.startswith("open "):
            if "open it" in command:
                pass
            elif "open file" in command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general "):
            pass

        elif command.startswith("realtime "):
            pass

        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)

        else:
            print(f"No Function Found for {command}")

    results = await asyncio.gather(*funcs, return_exceptions=True)

    for result in results:
        yield result

async def Automation(commands):
    async for result in TranslateAndExecute(commands):
        pass

    return True
