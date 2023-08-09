import { utapi } from "uploadthing/server";
import { redirect } from 'next/navigation'
import { InsertData } from "@/server/utils";
import { currentUser } from "@clerk/nextjs";
import UploadButton from "./UploadButton";
 
async function uploadFiles(formData: FormData) {
  "use server";
  console.log("uploading")
  const user = await currentUser();
  const files: any = formData.getAll("files");
  utapi.uploadFiles(files).then((res) => {
    const dbres = {res, user: user}
    InsertData("newtest", dbres)
    console.log(dbres);
  }).catch((err) => {
    console.log(err)
  })
   
}
 
export default function Upload() {
  return (
    <form action={uploadFiles}>
      <div className="flex flex-col">
      <input name="files" type="file" multiple />
      <UploadButton type="submit" className="w-full bg-white text-slate-950 mt-5 hover:bg-slate-300" />
      </div>
    </form>
  );
}