import React from "react";

const VideoEditor = ({ videoFile }) => {
  if (!videoFile) return null;

  const videoUrl = URL.createObjectURL(videoFile);

  return (
    <div>
      <video controls width="100%" src={videoUrl}></video>
    </div>
  );
};

export default VideoEditor;
