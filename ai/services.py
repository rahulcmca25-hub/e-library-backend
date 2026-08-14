from openai import OpenAI
from django.conf import settings


def generate_book_summary(book):

    client = OpenAI(
        api_key=settings.OPENAI_API_KEY
    )

    prompt = f"""
You are an expert librarian.

Generate a useful summary for this book.

Title: {book.title}

Description:
{book.description}

Author:
{book.author.name}

Category:
{book.category.name}

Return the response in this format:

Summary:
<summary>

Key Points:
- point 1
- point 2
- point 3

Target Audience:
<audience>
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text