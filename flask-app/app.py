import os

from flask import Flask, request
from google.cloud import storage
from google.cloud.video import transcoder_v1

app = Flask(__name__)

# Google Cloud Clients
storage_client = storage.Client()
transcoder_client = transcoder_v1.TranscoderServiceClient()

# GCP-Konfiguration
PROJECT_ID = "hsrm-cloud-1"
REGION = "us-central1"
BUCKET_NAME = "hsrm-cloud-bucket"

# Globaler Speicher für Job-Details
job_store = {}

@app.route("/", methods=["GET"])
def home():
    return "Welcome! Transcode a video via POST to /transcode-video\n"

@app.route("/transcode-video", methods=["POST"])
def upload_video():
    # File Namen als Parameter abrufen
    file_name = request.get_data(as_text=True).strip()
    if not file_name:
        return {"error": "No file_name provided"}, 400

    # Video in Cloud Storage identifizieren und In-/Output Variablen festlegen
    input_uri = f"gs://{BUCKET_NAME}/{file_name}"
    output_uri = f"gs://{BUCKET_NAME}/output/"

    # Transcoding-Auftrag erstellen
    job = {
        "input_uri": input_uri,
        "output_uri": output_uri,
        "config": {
            "elementary_streams": [
                {"key": "video-stream", "video_stream": {"h264": {"height_pixels": 1080, "width_pixels": 1920, "frame_rate": 30, "bitrate_bps": 8000000}}},
                {"key": "audio-stream", "audio_stream": {"codec": "aac", "bitrate_bps": 324000}},
            ],
            "mux_streams": [
                {
                    "key": "HLS",
                    "container": "ts",
                    "elementary_streams": ["video-stream", "audio-stream"],
                    "segment_settings": {
                        "segment_duration": {"seconds": 3}
                    }
                },
                {
                    "key": "HD",
                    "container": "mp4",
                    "elementary_streams": ["video-stream", "audio-stream"]
                }
            ],
            "manifests": [
                {
                    "file_name": "manifest.m3u8",
                    "type": "HLS",
                    "mux_streams": ["HLS"]
                }
            ]
        },
    }

    response = transcoder_client.create_job(
        parent=f"projects/{PROJECT_ID}/locations/{REGION}",
        job=job,
    )

    # Job-Daten speichern
    job_store[response.name] = {"input_uri": input_uri, "output_uri": output_uri}

    return {
        "message": "Transcoding process started! Use GET /job_status to see the progress",
        "job_name": response.name,
        "input_uri": input_uri,
        "output_uri": output_uri,
    }

@app.route("/job_status", methods=["GET"])
def job_status():
    job_name = request.args.get("job_name")
    if not job_name:
        return {"error": "Job name was not provided"}, 400

    try:
        # Job-Status abrufen
        job = transcoder_client.get_job(name=job_name)

        # Input- und Output-URIs aus dem Speicher abrufen
        job_details = job_store.get(job_name, {"input_uri": "", "output_uri": ""})

        return {
            "job_name": job.name,
            "state": job.state.name,
            "start_time": job.start_time.timestamp() if job.start_time else None,
            "end_time": job.end_time.timestamp() if job.end_time else None,
            "input_uri": job_details["input_uri"],
            "output_uri": job_details["output_uri"],
        }    
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))