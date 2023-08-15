"use client"

import React, { useState } from "react";
import { InsertData } from "@/server/utils";
import "@uploadthing/react/styles.css";
import { UploadDropzone } from "@uploadthing/react";
import { OurFileRouter } from "@/app/api/uploadthing/core";
import {useRouter} from "next/navigation"
import { useParams } from 'next/navigation'

function Upload({user} : any) {
  const [selectedFiles, setSelectedFiles] = useState<FileList | null>(null);
  const router = useRouter();
  const params = useParams();
  async function handleUploadComplete(res: any) {
    console.log("Files: ", res);
    const dbres = { response: res, user: JSON.parse(user), pipelineID: params.pipelineID };
    InsertData("resume", dbres);
    router.push(`/createpipeline/${params.pipelineID}/resume`);
  }

  function handleUploadError(error: Error) {
    alert(`ERROR! ${error.message}`);
  }

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const fileList = event.target.files;
    setSelectedFiles(fileList);
  }

  return (
    <div className="text-white *">
      <UploadDropzone<OurFileRouter>
        endpoint="imageUploader"
        onClientUploadComplete={handleUploadComplete}
        onUploadError={handleUploadError}
        className="bg-black border-white border-b text-white w-full mt-5 "
      />
    </div>
  );
}

export default Upload;
