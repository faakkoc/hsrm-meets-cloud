# CI/CD Pipeline @ Google Cloud Plattform
Dieses Repository stellt eine Flask Applikation zur Verfügung und dient der Darstellung einer CI/CD-Pipeline zur Google Cloud.
Die Applikation nutzt die Transcoder API, um Videos aus Cloud Storage Buckets zu transkodieren.

## Genutzte Services
- **Cloud Build**
    Trigger werden genutzt, um Docker Images zu erstellen, in die Artifact Registry zu pushen und in Cloud Deploy zu deployen
- **Cloud Run**
    Hostet die Anwendung
- **Artifact Registry**
    Enthält das Docker-Repository mit den Container-Images
- **Transcoder API**
    Die Anwendung nutzt die Transcoder API von Google für die Transkodierung von Videos