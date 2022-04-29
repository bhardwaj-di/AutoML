from google.cloud import storage
from google.cloud import speech
import firestore as fs

client = storage.Client()


def transcribe_gcs(gcs_uri,model):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""

    client = speech.SpeechClient()

    diarization_config = speech.SpeakerDiarizationConfig(
    enable_speaker_diarization=True,
    min_speaker_count=2,
    max_speaker_count=10,
    )

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        # sample_rate_hertz=44100,
        language_code="en-US",
        audio_channel_count=1,
        diarization_config=diarization_config,
        # enable_separate_recognition_per_channel=True,
        model = model,
        use_enhanced = True

    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")

    response = operation.result(timeout=90)
    result = response.results[-1]
    words_info = result.alternatives[0].words

    # Printing out the output:
    speaker_text = {}
    for word_info in words_info:
        if (str(word_info.speaker_tag) in speaker_text):
            speaker_text[str(word_info.speaker_tag)].append(word_info.word)
        else:
            new_key_values_dict = {str(word_info.speaker_tag): list(word_info.word)}
            speaker_text.update(new_key_values_dict)
        # print(
        #     u"sentence: '{}', speaker_tag: {}".format(word_info.word, word_info.speaker_tag)
        # )
    return speaker_text


def generateText(speaker_text):
    for key,value in zip(speaker_text.keys(),speaker_text.values()):
        speaker_text[key] = " ".join(value)
    return speaker_text

def start_transcription(data, context):
    dl_bucket = client.get_bucket(data['bucket'])
    dl_blob = dl_bucket.get_blob(data['name'])
    # dl_blob.download_to_filename(f'/tmp/{data["name"]}')
    print("file path is. ",f'gs://preprocessed_audio/{data["name"]}')
    speaker_text = transcribe_gcs(f'gs://preprocessed_audio/{data["name"]}','video')
    print("speaker test completed")
    data = generateText(speaker_text)
    print("data has been generated")
    fs.addData('Check',data)
    print("Firestore updated with data")
