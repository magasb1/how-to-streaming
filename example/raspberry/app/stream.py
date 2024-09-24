from ffmpeg import FFmpeg
import os

def stream_video(video_source: str, rtmp_url: str):
    """
    Streams a video to the specified RTMP URL using ffmpeg.

    Args:
    video_source (str): The path or URL of the video source.
    rtmp_url (str): The RTMP URL to stream the video to.
    """
    ffmpeg = (
        FFmpeg()
        .option("re")
        .input(video_source)
        .output(
            rtmp_url,
            {"codec:v": "libx264"},
            f="flv",
            r=6,
            g=18,
            crf=23,
            preset="ultrafast",
            map="0",
        )
    )

    ffmpeg.execute()

# Example usage
if __name__ == "__main__":
    video_source = os.getenv("VIDEO_SOURCE")
    rtmp_url = os.getenv("RTMP_URL")
    stream_video(video_source, rtmp_url)
