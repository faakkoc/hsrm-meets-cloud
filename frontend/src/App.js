import React, { useState } from "react";
import AudioEditor from "./components/AudioEditor";
import VideoEditor from "./components/VideoEditor";
import Controls from "./components/Controls";
import Timeline from "./components/Timeline";

function App() {
  const [audioFile, setAudioFile] = useState(null);
  const [videoFile, setVideoFile] = useState(null);
  const [audioPlayer, setAudioPlayer] = useState(null);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(1);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file.type.startsWith("audio/")) setAudioFile(file);
    if (file.type.startsWith("video/")) setVideoFile(file);
  };

  const handlePlay = () => audioPlayer && audioPlayer.play();
  const handlePause = () => audioPlayer && audioPlayer.pause();
  const handleSeek = (time) => audioPlayer && audioPlayer.setCurrentTime(time);

  const handleExport = () => {
    alert("Export-Funktion wird implementiert!");
  };

  return (
    <div>
      <h1>Online Audio/Video Editor</h1>
      <input type="file" accept="audio/*,video/*" onChange={handleFileChange} />
      <AudioEditor
        audioFile={audioFile}
        onWaveformReady={(player) => {
          setAudioPlayer(player);
          setDuration(player.getDuration());
        }}
      />
      <VideoEditor videoFile={videoFile} />
      <Timeline
        duration={duration}
        currentTime={currentTime}
        onSeek={handleSeek}
      />
      <Controls onPlay={handlePlay} onPause={handlePause} onExport={handleExport} />
    </div>
  );
}

export default App;
