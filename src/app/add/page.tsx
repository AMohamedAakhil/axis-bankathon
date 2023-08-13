import React from "react";
import Upload from "./upload";
import "@uploadthing/react/styles.css";

const Add = () => {
  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2    ">
      <div className="w-full">
        <h1 className="text-2xl">Add new resume</h1>
        <Upload />
      </div>
    </div>
  );
};

export default Add;
