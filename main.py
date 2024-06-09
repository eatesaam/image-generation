import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
import uvicorn
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


@app.get("/image")
def image_generation(url : str):
    url = url.replace(" ","+")
    print("Image url: ", url)
    image_desc_prompt = "What’s in this image?"
    image_url = url
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": image_desc_prompt},
                {
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                },
                },
            ],
            }
        ],
        max_tokens=300,
    )
    image_desc = response.choices[0].message.content
    dalle_prompt = f"""
        As an artist and satirical copywriter with a flair for the flamboyant, Transform the image with description: {image_desc} into
        the version of the image that not only embody the spirit of cheesy 80s hair metal but also draw inspiration from vintage car culture
        (think Pontiac Trans Am, Firebird). This unique blend of aesthetics ensures each creation oozes the raw, unapologetic essence of the era,
        complete with an 80s hair metal, outlaw, grunge, and classic car filter. Maintain the description of the image to the most allowable extent while
        infusing each image with the essence of this distinctive style. Apply the same “Your Mama Would Hate Me” watermark to the image.
    """
    # Call the API
    dalle_response = client.images.generate(
        model="dall-e-3",
        prompt=dalle_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    generated_image_url = dalle_response.data[0].url
    image_desc_prompt = """
        Provide the comedic bios of the image with a roasting tone, using a given nickname that will incorporate the name
        provided, a humorous go-to pickup line (ensuring variety beyond the classic “Are you a parking ticket? Because you’ve got FINE written all
        over you,” to include a mix of other lines), and a chosen vice for each greaser persona. These creations are inspired by trading-card culture,
        aimed at delivering both a visual and textual laugh. Every bio features #yourmamawouldhateme at the end. The content of the bio
        should read like a comedy roast, bordering on the  edge of offensiveness but still maintaining a level of respect and fun.
        Handle it with a blend of creativity, humor, and a touch of nostalgia, ensuring compliance with guidelines for respectful and fun depictions.
    """
    final_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": image_desc_prompt},
                {
                "type": "image_url",
                "image_url": {
                    "url": generated_image_url,
                },
                },
            ],
            }
        ],
        max_tokens=300,
    )
    image_desc = final_response.choices[0].message.content
    print(image_desc)
 
    return { "image_url" : generated_image_url, "image_description" : image_desc}


if __name__ == "__main__":
    uvicorn.run(app=app, host='127.0.0.1', port=8000)