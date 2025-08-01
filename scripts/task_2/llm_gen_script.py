# suppress warnings
import warnings
import os

warnings.filterwarnings("ignore")

# import libraries
import argparse
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


if __name__ == "__main__":
    # Get Client for your LLMs
    client = Together(api_key=TOGETHER_API_KEY)

    # Example usage
    prompt = "write a 3 line post about pizza"
    response = prompt_llm(prompt)

    print("\nResponse:\n")
    print(response)
    print("-" * 100)
