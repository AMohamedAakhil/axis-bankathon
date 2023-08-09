import { utapi } from "uploadthing/server";
import { redirect } from 'next/navigation'
import { InsertData } from "@/server/utils";
import { currentUser } from "@clerk/nextjs";
import UploadButton from "./UploadButton";
import { Input } from "@/components/ui/input";

async function uploadFiles(formData: FormData) {
  "use server";
  console.log("uploading")
  const user = await currentUser();
  const files: any = formData.getAll("files");
  const response = await utapi.uploadFiles(files)
  const dbres = {response, user: user}
  InsertData("newertest", dbres)
  console.log(dbres);
  redirect('/')
}
 
export default function Upload() {
  return (
    <div className="">
    <form action={uploadFiles}>
          <div className="flex flex-col">
          <Input name="files" type="file" className="mt-5 text-black" multiple />
          <UploadButton type="submit" className="w-full bg-white text-slate-950 mt-5 hover:bg-slate-300" />
          </div>
        </form>
    </div>
    
  );
}