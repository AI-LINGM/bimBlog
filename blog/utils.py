import random
import re


def select_random_quote(paragraph):
    sentences = re.split(r'(?<=[.!?]) +', paragraph)
    random_quote = random.choice(sentences)
    return random_quote


def format_body(input_string, random_quote):
    sections = input_string.split('\n\n')
    formatted_string = ''
    quote_inserted = False

    for section in sections:
        paragraphs = section.split('\n')
        for i, paragraph in enumerate(paragraphs):
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            if i == 0:
                formatted_string += f'<h5>{paragraph}</h5>\n'
            else:
                formatted_string += f'<p>{paragraph}</p>\n'
            if i == len(paragraphs) // 2 and not quote_inserted:
                formatted_string += f'<blockquote class="blockquote wow fadeInUp">\n<p>{random_quote}</p>\n</blockquote>\n'
                quote_inserted = True
        formatted_string += '\n'

    return formatted_string
