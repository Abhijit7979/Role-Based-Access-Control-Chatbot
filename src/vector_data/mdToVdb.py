from langchain.text_splitter import MarkdownHeaderTextSplitter
import json
import pandas as pd

# Define the markdown header splitter
splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "H1"), ("##", "H2")])

# Read the markdown file
with open("/Users/abhijit/Desktop/DS-RPC-01/data/engineering/engineering_master_doc.md", "r", encoding="utf-8") as file:
    md_content = file.read()

# Split the markdown content
chunks = splitter.split_text(md_content)

# Convert chunks into JSON-serializable format
json_chunks = [
    {
        "chunk_index": i,
        "content": chunk.content,
        "metadata": chunk.metadata  # headers like H1, H2
    }
    for i, chunk in enumerate(chunks)
]

# Print as pretty JSON
print(json.dumps(json_chunks, indent=2, ensure_ascii=False))

# Optional: Save to a .json file
with open("engineering_chunks.json", "w", encoding="utf-8") as f:
    json.dump(json_chunks, f, indent=2, ensure_ascii=False)
