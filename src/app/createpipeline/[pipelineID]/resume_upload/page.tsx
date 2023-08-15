import React from "react";
import Upload from "./upload";
import "@uploadthing/react/styles.css";
import { currentUser } from "@clerk/nextjs";

const Add = () => {
    const user = currentUser();
  return (
    <div className="flex justify-center items-center p-5 ">
      <div className="w-full">
        <h1 className="text-2xl">Upload CVs</h1>
        <Upload user={JSON.stringify(user)} />
      </div>
    </div>
  );
};

export default Add;
