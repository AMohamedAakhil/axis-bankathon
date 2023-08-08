"use client"

import React from 'react'
import "@uploadthing/react/styles.css";
import { UploadButton } from '@/utils/uploadthing';
import { InsertData } from '@/server/utils';

const Add = () => {
  return (
    <div className="mt-8 p-5">
        <h1 className="text-2xl">Add new person</h1>
        <h1>Upload CV: </h1>
        <UploadButton
        endpoint="imageUploader"
        onClientUploadComplete={(res) => {
          console.log("Files: ", res);
          InsertData("test", res);
          alert("Upload Completed");
        }}
        onUploadError={(error: Error) => {
          alert(`ERROR! ${error.message}`);
        }}
      />
    </div>
  )
}

export default Add