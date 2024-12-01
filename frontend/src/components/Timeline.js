import React from "react";

const Timeline = ({ duration, currentTime, onSeek }) => {
  const handleSeek = (e) => {
    const seekTime = (e.nativeEvent.offsetX / e.target.offsetWidth) * duration;
    onSeek(seekTime);
  };

  return (
    <div
      style={{
        background: "#ddd",
        height: "10px",
        margin: "20px 0",
        position: "relative",
        cursor: "pointer",
      }}
      onClick={handleSeek}
    >
      <div
        style={{
          background: "purple",
          width: `${(currentTime / duration) * 100}%`,
          height: "100%",
        }}
      ></div>
    </div>
  );
};

export default Timeline;
