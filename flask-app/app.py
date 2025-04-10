import os

from flask import Flask, request, render_template, jsonify
from google.cloud import storage
from google.cloud.video import transcoder_v1

app = Flask(__name__)

# Google Cloud Clients
storage_client = storage.Client()
transcoder_client = transcoder_v1.TranscoderServiceClient()

# Error-Handler für alle Exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500

# GCP-Konfiguration
'''PROJECT_ID = "hsrm-cloud-1"
REGION = "us-central1"
BUCKET_NAME = "hsrm-cloud-bucket"
'''
PROJECT_ID = os.environ.get("PROJECT_ID", "hsrm-cloud-1")
REGION = os.environ.get("REGION", "us-central1")
BUCKET_NAME = os.environ.get("BUCKET_NAME", "hsrm-cloud-bucket")

# Globaler Speicher für Job-Details
job_store = {}

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html") # "Welcome! Transcode a video via POST to /transcode-video\n"

@app.route("/player/<job_id>", methods=["GET"])
def player(job_id):
    # Job-Details abrufen
    try:
        job = transcoder_client.get_job(name=job_id)
        job_details = job_store.get(job_id, {"input_uri": "", "output_uri": ""})
        
        # Nur wenn der Job erfolgreich abgeschlossen wurde
        if job.state.name == "SUCCEEDED":
            # Aus der Output-URI den Pfad zu den DASH-Dateien extrahieren
            output_uri = job_details["output_uri"]
            # URL zum Bucket extrahieren (ohne gs://)
            bucket_name = output_uri.replace("gs://", "").split("/")[0]
            
            # Pfad extrahieren (alles nach dem Bucket-Namen)
            output_path = "/".join(output_uri.replace("gs://", "").split("/")[1:])
            if not output_path.endswith("/"):
                output_path += "/"
            
            # MPD-Pfad für DASH-Streaming
            mpd_path = f"{output_path}manifest.mpd"
            
            # Öffentliche URL zum MPD-File
            mpd_url = f"https://storage.googleapis.com/{bucket_name}/{mpd_path}"
            
            return render_template("player.html", mpd_url=mpd_url)

        elif job.state.name != "SUCCEEDED":
            return jsonify({"error": f"Job not completed. Current state: {job.state.name}"}), 400
            
        else:
            return {"error": f"Job not completed. Current state: {job.state.name}"}, 400
    
    except Exception as e:
        return {"error": str(e)}, 500

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
                    "key": "DASH",
                    "container": "fmp4",
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
                    "file_name": "manifest.mpd",
                    "type": "DASH",
                    "mux_streams": ["DASH"]
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

    return jsonify({
        "message": "Transcoding process started! Use GET /job_status to see the progress",
        "job_name": response.name,
        "player_url": f"/player/{response.name}",
        "input_uri": input_uri,
        "output_uri": output_uri,
    })

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

        response_data = {
            "job_name": job.name,
            "state": job.state.name,
            "start_time": job.start_time.timestamp() if job.start_time else None,
            "end_time": job.end_time.timestamp() if job.end_time else None,
            "input_uri": job_details["input_uri"],
            "output_uri": job_details["output_uri"],
        }
        
        # Wenn der Job abgeschlossen ist, füge Player-URL hinzu
        if job.state.name == "SUCCEEDED":
            response_data["player_url"] = f"/player/{job.name}"
            
        return jsonify(response_data)
    
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))