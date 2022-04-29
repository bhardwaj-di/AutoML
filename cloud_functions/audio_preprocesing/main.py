import ffmpeg
from google.cloud import storage

client = storage.Client()
AUDIO_BUCKET = 'preprocessed_audio'

def extract_wav_from_video(data, context):
    dl_bucket = client.get_bucket(data['bucket'])
    dl_blob = dl_bucket.get_blob(data['name'])
    dl_blob.download_to_filename(f'/tmp/temp_{data["name"]}')
    try:
        ffmpeg.input(f'/tmp/temp_{data["name"]}', ss=1).output('/tmp/temp.flac', format='flac', bits_per_raw_sample=16, ac=1, ar=16000).overwrite_output().run(capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
        print(e.stderr.decode())
        exit(0)
    ul_bucket = client.get_bucket(AUDIO_BUCKET)
    filename = data['name'].split('.')[0]
    newblob = ul_bucket.blob(f'{filename}.flac')
    newblob.upload_from_filename('/tmp/temp.flac')
