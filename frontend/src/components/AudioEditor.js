import React, { useRef, useEffect } from "react";
import WaveSurfer from "wavesurfer.js";

const AudioEditor = ({ audioFile, onWaveformReady }) => {
  const waveformRef = useRef(null);

  useEffect(() => {
    const wavesurfer = WaveSurfer.create({
      container: waveformRef.current,
      waveColor: "violet",
      progressColor: "purple",
    });

    if (audioFile) {
      const reader = new FileReader();
      reader.onload = (event) => wavesurfer.load(event.target.result);
      reader.readAsDataURL(audioFile);

      wavesurfer.on("ready", () => {
        onWaveformReady(wavesurfer);
      });
    }

    return () => wavesurfer.destroy();
  }, [audioFile, onWaveformReady]);

  return <div ref={waveformRef}></div>;
};

export default AudioEditor;
