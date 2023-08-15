"use client"

import React, {useState} from 'react';
import { GetData, GetPipelineData } from "@/server/utils";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { evaluateResumes } from './action';
import CVCard from './CVCard';
import { useParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { sendEmails } from './action';

const CVDisplay = () => {
    const params = useParams()
    const [startLoad, setStartLoad] = useState(false);
    const [res, setRes] = useState<any>(null);
    const [invalidFlag, setInvalidFlag] = useState(false);
    const [buttonLoad, setButtonLoad] = useState(false);
    const handleStart = async () => {
        setButtonLoad(true);
        const cvData: any = await GetPipelineData("resume", 10, params.pipelineID);
        console.log(params.pipelineID)
        console.log(cvData);
        if (cvData.length === 0) {
            setInvalidFlag(true);
            return;
        }
        console.log(params.pipelineID)
        const urlList: string[] = [];
        for (const item of cvData[0].response) {
            urlList.push(item.url); // Use item.fileUrl instead of item.url
        }
        const jobData: any = await GetPipelineData("jobs", 10, params.pipelineID);
        console.log("NIGGA JOB DATA", jobData)
        const job_title = jobData[0].job_title;
        const job_description = jobData[0].job_description;
        const res = await evaluateResumes(job_title, job_description, urlList);
        sendEmails("a.aakhilmohamed@gmail.com", "hi nigga")
        setRes(res);
        console.log("res", res)
        res ? setStartLoad(true) : setStartLoad(false);
        setButtonLoad(false);
    }
  
  return (<div>{invalidFlag ? "Pipeline does not exist" : <div className="p-5">{startLoad ? 
    <Card className="bg-black text-white">
      <CardHeader>
        <CardTitle>Applicant Ranking</CardTitle>
        <CardDescription>The ranking according to the CVs submitted for each applicant. </CardDescription>
      </CardHeader>
      <CardContent className='grid grid-cols-1 gap-4'>
{res && res.length > 0 ? 
  res
    .sort((a: any, b: any) => parseInt(b.score) - parseInt(a.score)) // Sort in descending order
    .map((evaluation: any, index: number) => (
      <CVCard
        key={index+1}
        contact_info={evaluation.contact_info}
        score={evaluation.score}
        summary={evaluation.short_summary}
        rank={index + 1} // Calculate rank based on array index
      />
    ))
  : <CardDescription>Loading.</CardDescription>
}
</CardContent>



    </Card> : 
    <div className="grid h-screen place-items-center">
      <Button className="w-1/4 bg-white text-black hover:bg-slate-200 -mt-20" onClick={handleStart}>
      {buttonLoad ? (
        <div role="status">
          <svg
            aria-hidden="true"
            className="inline w-5 h-5 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-gray-600 dark:fill-gray-300"
            viewBox="0 0 100 101"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
              fill="currentColor"
            />
            <path
              d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
              fill="currentFill"
            />
          </svg>
          <span className="sr-only">Loading...</span>
        </div>
      ) : (
        "Start Evaluation"
      )}
      </Button>
    </div>}
  </div> }
   
  </div>
   
  );
};

export default CVDisplay;
