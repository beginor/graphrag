import os
import glob

from markitdown import MarkItDown

docs_dir = "ragtest/gdee-rules/docs"
input_dir = "ragtest/gdee-rules/input"

def convert_to_markdown(docx_file: str, md_file: str):
    print(f"Converting {docx_file} to {md_file}")
    markdown_converter = MarkItDown()
    result = markdown_converter.convert(docx_file)
    with open(md_file, 'w', encoding='utf-8') as f:
        print(result.text_content)
        f.write(result.text_content)


for root, dirs, files in os.walk(docs_dir):
    for file in files:
        if file.endswith(".docx"):
            docx_file = os.path.join(root, file)
            md_file = os.path.join(input_dir, os.path.relpath(docx_file, docs_dir)).replace('.docx', '.md')
            os.makedirs(os.path.dirname(md_file), exist_ok=True)
            convert_to_markdown(docx_file, md_file)
