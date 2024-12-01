const express = require("express");
const multer = require("multer");
const { processAudio } = require("./ffmpegService");
const path = require("path");
const fs = require("fs");

const app = express();
const upload = multer({ dest: "uploads/" });

app.post("/upload", upload.single("file"), async (req, res) => {
  const inputPath = req.file.path;
  const outputPath = path.join("processed", `${Date.now()}-output.mp3`);

  try {
    await processAudio(inputPath, outputPath, "00:00:05", 10);
    res.download(outputPath, () => {
      fs.unlinkSync(inputPath);
      fs.unlinkSync(outputPath);
    });
  } catch (err) {
    res.status(500).send("Processing failed");
  }
});

app.listen(3000, () => console.log("Server running on port 3000"));
