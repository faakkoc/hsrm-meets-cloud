# CI/CD Pipeline @ Google Cloud Plattform
Dieses Repository stellt eine Flask Applikation zur Verfügung und dient der Darstellung einer CI/CD-Pipeline zur Google Cloud

## Genutzte Services
- **Cloud Build**
    Trigger werden genutzt, um Docker Images zu erstellen, in die Artifact Registry zu pushen und in Cloud Deploy zu deployen
- **Cloud Run**
    Hostet die Anwendung
- **Cloud Deploy**
    Hierüber wird das Deployment in mehreren Stages verwaltet
- **Artifact Registry**
    Enthält das Docker-Repository mit den Container-Images