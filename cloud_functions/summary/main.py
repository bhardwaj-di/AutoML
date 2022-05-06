from os import path
import firestore as fs
import os
import math
from transformers import pipeline
from google.cloud import storage

def predict(text):
        summarizer = pipeline("summarization",model="/tmp/model")
        summary = summarizer(text, max_length=130, min_length=50, do_sample=False)
        return summary

def extract_text(event, context):
    """Triggered by a change to a Firestore document.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    resource_string = context.resource
    # print out the resource string that triggered the function
    print(f"Function triggered by change to: {resource_string}.")

    # file_exist = str(path.isdir('/tmp/model'))
    # if not file_exist:
    # print("models are downloading")
    # get_model('sshleifer/distilbart-xsum-1-1')
    # get_tokenizer('sshleifer/distilbart-xsum-1-1')
    # print("models are downloaded")
    # else:
    #     print("model is already downloaded")

    BUCKET_NAME        = "gcp_pegasus"
    GCS_MODEL_FILE     = "model"
    dl_dir = '/tmp/'
    os.mkdir(dl_dir + "model")

    storage_client   = storage.Client()
    bucket   = storage_client.get_bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=GCS_MODEL_FILE)
    for blob in blobs:
      filename = blob.name
      blob.download_to_filename(dl_dir + filename)
    print("files inside /tmp/model is",os.listdir("/tmp/model"))

    document_name = resource_string.split("/")[-1]
    print("document_name is",document_name)
    transcribed_dict = fs.getData(document_name)

    print("transcribed_dict  is",transcribed_dict)
    summarized_dict = {}

    max_words = 512
    for k,v in transcribed_dict.items():
        words = v.split()
        chunks = math.ceil(len(words) / max_words)
        truncated_summary = ""
        start = 0
        end = max_words
        for i in range(chunks):
            truncated_text = v[start:end]
            if not len(truncated_text.split()) > 30:
                break
            truncated_summary += (predict(truncated_text)[0].get("summary_text"))
            start = end
            end += max_words

        summarized_dict[str(k)] = truncated_summary
    print("summarized dict is",summarized_dict)
    fs.addData(document_name,summarized_dict)
    print("added to fs")

