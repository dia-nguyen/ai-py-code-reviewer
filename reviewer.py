from openai import OpenAI
from dotenv import dotenv_values
import argparse

config = dotenv_values(".env")
client = OpenAI(api_key=config["OPENAI_API_KEY"])

def parse_file_contents(filename: str):
    """Parse lines from a file and return as a list of strings."""
    with open(filename, 'r') as file:
        return file.readlines()

def code_review(file):
    """Generate a code review for the file based on file content"""

    prompt = """
    You will receive a file's contents as text.
    Generate a code review for the file. Indicate what changes should be made to improve the the style, performance, readability, and maintainability.
    Suggest any reputable libraries that can be used to improve the code. For each suggested change, include line numbers.
    """

    file_content = parse_file_contents(file)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Code review for the following file: {file_content}"}
    ]

    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    return res.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="Simple code reviewer for a file")
    parser.add_argument("file")
    args = parser.parse_args()

    review=code_review(args.file)

    print(review)



if __name__ == "__main__":
    main()