import re
import textwrap
import uuid
from meera.types import  Vector
from pydantic import BaseModel
import json
class Chunk(BaseModel):
    id:str
    chunk_text:str

def chunk_transcript(transcript: str, max_chunk_size: int = 300, overlap: int = 50):
    """
    Splits a transcript into meaningful chunks.

    - max_chunk_size: Maximum characters per chunk
    - overlap: Number of overlapping characters between chunks for context retention
    """
    # Split transcript into sentences using regex for punctuation-based splitting
    sentences = re.split(r'(?<=[.!?]) +', transcript)

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)

        # If adding a new sentence exceeds max_chunk_size, save the current chunk
        if current_length + sentence_length > max_chunk_size:
            chunk_text = " ".join(current_chunk).strip()
            chunks.append(chunk_text)

            # Start a new chunk with overlap from the previous one
            current_chunk = [chunk_text[-overlap:]] if overlap else []
            current_length = len(current_chunk[0]) if overlap else 0

        # Add sentence to the current chunk
        current_chunk.append(sentence)
        current_length += sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk).strip())

    return chunks

def chunk_long_text(text, chunk_size=100, overlap=50):
    words = re.findall(r'\S+', text)
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        if len(chunk) < chunk_size:
            break  # Stop if the last chunk is smaller than expected
        chunks.append(' '.join(chunk))
    return [ json.loads(Chunk(id=str(uuid.uuid4()).split('-')[0], chunk_text=chunk).model_dump_json()) for chunk in  chunks]



if __name__ == "__main__":
    print(chunk_transcript(""))