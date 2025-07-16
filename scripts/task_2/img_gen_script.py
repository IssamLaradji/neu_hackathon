# suppress warnings
import warnings

warnings.filterwarnings("ignore")

# import libraries
import requests, os
import argparse
from PIL import Image


import gradio as gr
from together import Together
import textwrap

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")


## FUNCTION 1: This Allows Us to Prompt the AI MODEL
# -------------------------------------------------
def prompt_llm(prompt, with_linebreak=False):
    # This function allows us to prompt an LLM via the Together API

    # model
    model = "meta-llama/Meta-Llama-3-8B-Instruct-Lite"

    # Make the API call
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    output = response.choices[0].message.content

    if with_linebreak:
        # Wrap the output
        wrapped_output = textwrap.fill(output, width=50)

        return wrapped_output
    else:
        return output


## FUNCTION 2: This Allows Us to Generate Images
# -------------------------------------------------
def gen_image(prompt, width=256, height=256):
    # This function allows us to generate images from a prompt
    response = client.images.generate(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell-Free",  # Using a supported model
        steps=2,
        n=1,
    )
    image_url = response.data[0].url
    image_filename = "image.png"

    # Download the image using requests instead of wget
    response = requests.get(image_url)
    with open(image_filename, "wb") as f:
        f.write(response.content)
    img = Image.open(image_filename)
    img = img.resize((height, width))

    return img


if __name__ == "__main__":
    # Get Client for your LLMs
    client = Together(api_key=TOGETHER_API_KEY)

    text_prompt = "write a 3 line post about resident evil for instagram"
    image_prompt = f"give me an image that represents this '{text_prompt}'"

    # Generate Text
    response = prompt_llm(text_prompt, with_linebreak=True)

    print("\nResponse:\n")
    print(response)
    print("-" * 100)

    # Generate Image
    print(f"\nCreating Image for your prompt: {image_prompt}... ")
    os.makedirs("results", exist_ok=True)

    img = gen_image(prompt=image_prompt, width=256, height=256)
    path = "results/image.png"
    img.save(path)

    # Show the output
    print(
        f"""\n\n
Based on the image in {path} - here is the text:\n\n
{response}\n\n"""
    )
