import ffmpeg

def get_mp3_metadata(file_location: str):
    metadata = {}

    metadata['duration'] = ffmpeg.probe(file_location)['format']['duration']
