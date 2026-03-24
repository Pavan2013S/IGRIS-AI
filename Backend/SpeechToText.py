import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import dotenv_values
import mtranslate as mt
from time import sleep

env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-IN")

HtmlCode = f'''<!DOCTYPE html>
<html>
<body>

<button id="start">Start Recognition</button>
<button id="end">Stop Recognition</button>
<p id="output"></p>

<script>

let recognition;

if ('webkitSpeechRecognition' in window) {{
    recognition = new webkitSpeechRecognition();
}} else if ('SpeechRecognition' in window) {{
    recognition = new SpeechRecognition();
}} else {{
    alert("Speech Recognition not supported in this browser");
}}

recognition.lang = "{InputLanguage}";
recognition.continuous = true;

const output = document.getElementById("output");

recognition.onresult = function(event) {{
    const transcript = event.results[event.results.length - 1][0].transcript;
    output.textContent += transcript;
}}

document.getElementById("start").onclick = () => recognition.start();

document.getElementById("end").onclick = () => {{
    recognition.stop();
    output.innerHTML="";
}}

</script>

</body>
</html>
'''

os.makedirs("Data", exist_ok=True)

html_path = os.path.abspath("Data/Voice.html")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--use-fake-ui-for-media-stream")

driver = webdriver.Chrome(options=chrome_options)

TempDirPath = os.path.abspath("Frontend/Files")
os.makedirs(TempDirPath, exist_ok=True)

def SetAssistantStatus(Status):
    with open(f"{TempDirPath}/Status.data", "w", encoding="utf-8") as file:
        file.write(Status)

def QueryModifier(Query):

    new_query = Query.lower().strip()

    question_words = [
        "what","who","when","where","why","how",
        "can you","would you","is it possible"
    ]

    if any(q in new_query for q in question_words):
        new_query = new_query.rstrip(".?!,") + "?"
    else:
        new_query = new_query.rstrip(".?!,") + "."

    return new_query.capitalize()

def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def SpeechRecognization():

    driver.get("file:///" + html_path.replace("\\","/"))

    sleep(1)

    driver.find_element(By.ID, "start").click()

    while True:

        try:
            Text = driver.find_element(By.ID, "output").text

            if Text:

                driver.find_element(By.ID, "end").click()

                if InputLanguage.lower().startswith("en"):
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))

        except:
            pass

        sleep(0.2)

if __name__ == "__main__":

    while True:
        text = SpeechRecognization()
        print(text)
