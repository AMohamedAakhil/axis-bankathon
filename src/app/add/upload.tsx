import React, { useState } from "react";
import { redirect } from "next/navigation";
import { currentUser } from "@clerk/nextjs";
import UploadButton from "./UploadButton";
import { InsertData } from "@/server/utils";
import { GetData } from "@/server/utils";
import { utapi } from "uploadthing/server";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

function Upload({user} : any) {
  const [selectedFiles, setSelectedFiles] = useState<FileList | null>(null);

  async function uploadFiles() {
    console.log("uploading");
    const user = await currentUser();
    const filesArray = Array.from(selectedFiles!);
    const formData = new FormData();
    
    filesArray.forEach(file => {
      formData.append("files", file);
    });
    
    const response = await utapi.uploadFiles(filesArray);
    const dbres = { response, user: JSON.parse(user) };
    InsertData("resume", dbres);
    console.log(dbres);
    redirect("/");
  }

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const fileList = event.target.files;
    setSelectedFiles(fileList);
  }

  return (
    <form onSubmit={event => {
      event.preventDefault();
      uploadFiles();
    }} className="mt-5">
      <Label htmlFor="fileUpload">Choose files to upload:</Label>
      <Input
        id="fileUpload"
        name="files"
        type="file"
        className="text-black"
        multiple
        onChange={handleFileChange}
      />
      <UploadButton
        type="submit"
        className="w-full bg-white text-slate-950 mt-5 hover:bg-slate-300"
      />
    </form>
  );
}

export default Upload;
