import React from "react";
import Upload from "./upload";
import "@uploadthing/react/styles.css";

const Add = () => {
  return (
    <div className="flex justify-center items-center p-5">
      <div className="w-full">
        <h1 className="text-2xl">Add new resume</h1>
        <Upload />
      </div>
    </div>
  );
};

export default Add;
