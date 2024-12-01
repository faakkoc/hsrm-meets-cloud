const ffmpeg = require("fluent-ffmpeg");
const path = require("path");

const processAudio = (inputPath, outputPath, startTime, duration) => {
  return new Promise((resolve, reject) => {
    ffmpeg(inputPath)
      .setStartTime(startTime)
      .setDuration(duration)
      .output(outputPath)
      .on("end", resolve)
      .on("error", reject)
      .run();
  });
};

module.exports = { processAudio };
