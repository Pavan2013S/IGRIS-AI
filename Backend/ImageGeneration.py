import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

def open_image(prompt):

    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")

    files = [f"{prompt}{i}.jpg" for i in range(1,5)]

    for jpg_file in files:

        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except Exception:
            print(f"Error opening image: {image_path}")

API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

api_key = get_key(".env", "HuggingFaceAPIKey") or ""

headers = {
    "Authorization": f"Bearer {api_key}"
}

async def query(payload):

    try:

        response = await asyncio.to_thread(
            requests.post,
            API_URL,
            headers=headers,
            json=payload
        )

        content_type = response.headers.get("content-type","")

        if content_type.startswith("image"):
            return response.content
        else:
            print("API returned error:", response.text)
            return None

    except Exception as e:
        print("Request failed:", e)
        return None

async def generate_image(prompt):

    tasks = []

    for _ in range(4):

        payload = {
            "inputs": f"{prompt}, ultra detailed, 4k, cinematic lighting, high quality, seed={randint(0,1000000)}"
        }

        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):

        if image_bytes:

            file_path = fr"Data\{prompt.replace(' ','_')}{i+1}.jpg"

            try:
                with open(file_path,"wb") as f:
                    f.write(image_bytes)

                print("Saved:", file_path)

            except Exception as e:
                print("Error saving image:", e)

        else:
            print(f"Skipping image {i+1}")

def GenerateImages(prompt):

    os.makedirs("Data",exist_ok=True)

    asyncio.run(generate_image(prompt))

    open_image(prompt)

while True:

    try:

        with open(r"Frontend\Files\ImageGeneration.data","r") as f:
            Data = f.read().strip()

        if "," in Data:

            Prompt, Status = Data.split(",",1)

            if Status.strip() == "True":

                print("Generating images...")

                GenerateImages(prompt=Prompt)

                with open(r"Frontend\Files\ImageGeneration.data","w") as f:
                    f.write("False,False")

                break

        sleep(1)

    except Exception:
        sleep(1)
