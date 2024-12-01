import React from "react";

const Controls = ({ onPlay, onPause, onExport }) => {
  return (
    <div style={{ marginTop: "10px" }}>
      <button onClick={onPlay}>Play</button>
      <button onClick={onPause}>Pause</button>
      <button onClick={onExport}>Export</button>
    </div>
  );
};

export default Controls;
