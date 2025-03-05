from youtube_transcript_api import YouTubeTranscriptApi
from typing import Any
def extract_youtube_video_transcript(video_link:str)->str:
    try:
        vid_id = video_link.split("?v=")[-1]
        content = YouTubeTranscriptApi.get_transcript(video_id=vid_id)
        return "\n".join([data.get("text") for data in content if data.get("text") != "[Music]"])
    except Exception as e:
        raise Exception(f'{e}')



def extract_pdf_content(filepath:str)->list[Any]:
    try:
        elements = ''
        return elements
    except Exception as e:
        raise  Exception(e.__str__())

if __name__ == "__main__":
    print(extract_youtube_video_transcript("https://www.youtube.com/watch?v=wQ9r_UVMBr4"))
