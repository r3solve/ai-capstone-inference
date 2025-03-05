from youtube_transcript_api import YouTubeTranscriptApi
from pypdf import PdfReader
from uuid import uuid4
from typing import Any


def annotate_data_as_json(data:str):
    """
    This method takes the data list and returns a json object
    {
      "id":32sf,
      "chunk_text": page_content"
    }

    This is done for easy insertion into the vector database.
    """
    return {
        "id":str(uuid4()).split("-")[0],
        "chunk_text":data
    }


def extract_youtube_video_transcript(video_link:str)->str:
    try:
        vid_id = video_link.split("?v=")[-1]
        content = YouTubeTranscriptApi.get_transcript(video_id=vid_id)
        return "\n".join([data.get("text") for data in content if data.get("text") != "[Music]"])
    except Exception as e:
        raise Exception(f'{e}')



def extract_pdf_content(filepath:str)->list[Any]:
    try:
        reader = PdfReader(filepath)
        return "\n".join([page.extract_text() for page in reader.pages])
    except Exception as e:
        raise  Exception(e.__str__())

if __name__ == "__main__":
    # print(extract_youtube_video_transcript("https://www.youtube.com/watch?v=wQ9r_UVMBr4"))
    print(extract_pdf_content("resume.pdf"))
