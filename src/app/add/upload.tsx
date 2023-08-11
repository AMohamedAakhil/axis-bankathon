import { utapi } from "uploadthing/server";
import { redirect } from 'next/navigation'
import { InsertData } from "@/server/utils";
import { currentUser } from "@clerk/nextjs";
import UploadButton from "./UploadButton";
import { Input } from "@/components/ui/input";
import { GetData } from "@/server/utils";

async function uploadFiles(formData: FormData) {
  "use server";
  console.log("uploading")
  const user = await currentUser();
  const files: any = formData.getAll("files");
  const response = await utapi.uploadFiles(files)
  const dbres = {response, user: user}
  InsertData("resume", dbres)
  console.log(dbres);
  redirect('/')
}
 
export default async function Upload() {
  const jobs = await GetData("jobs")
  console.log(jobs)
  return (
    <form action={uploadFiles} className="">
          <Input name="files" type="file" className="mt-5 text-black" multiple />
          <select className="mt-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-3 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
            <option value="" disabled selected>Choose a job title</option>
            {jobs.map((job: any) => {
              if (job.title) { // Check if title is not empty
                return <option key={job.title} value={job.title}>{job.title}</option>;
              }
              return null; // Don't render empty titles
            })}
          </select>
          <UploadButton type="submit" className="w-full bg-white text-slate-950 mt-5 hover:bg-slate-300" />
        </form>
    
  );
}