"use client";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { InsertData } from "@/server/utils";
import { redirect } from "next/navigation";
import { BsStars } from "react-icons/bs";
import { AiOutlineArrowRight } from "react-icons/ai";
import { evaluateJob } from "./actions";
import { useParams } from 'next/navigation'

const Form = ({ user }: any) => {
  const formatUser = JSON.parse(user);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [afterEval, setAfterEval] = useState(false);
  const [editedDescription, setEditedDescription] = useState("");
  const [evalData, setEvalData] = useState<any>([]);
  const params = useParams()
  console.log(params)
  const submitForm = async () => {
    setLoading(true);
    const response = { pipelineID: params.pipelineID, title: title, description: description, user: formatUser };
    const res = await InsertData("jobs", response);
    setLoading(false);
    redirect(`/createpipeline/${params.pipelineID}/resume_upload`);
  };
  const [startEval, setStartEval] = useState(false);
  const [evalLoading, setEvalLoading] = useState(false);
  const evalHandleClick = async () => {
    setLoading(true);
    setEvalLoading(true);
    setStartEval(true);
    const data = await evaluateJob(title, description);
    setEvalData(data);
    setEditedDescription(data[3]);
    setAfterEval(true);
    console.log(data);
    setEvalLoading(false);
    setStartEval(false);
    setLoading(false);
  };
  return (
    <Card className="bg-black text-white mt-5">
      <CardHeader>
        <div className="flex justify-between">
          <div>
            <CardTitle>Create New Job Opening</CardTitle>
            <CardDescription>
              You can start creating your pipeline by making a new job opening.
            </CardDescription>
          </div>
          <Button
            onClick={evalHandleClick}
            className="bg-white text-black hover:bg-slate-200"
          >
            {evalLoading ? (
              <div role="status">
                <svg
                  aria-hidden="true"
                  className="inline w-20 h-5 text-gray-200 animate-spin dark:text-gray-600 fill-gray-600 dark:fill-gray-300"
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
              </div>
            ) : (
              <>
                Evaluate
                <BsStars className="ml-2" />
              </>
            )}
          </Button>
        </div>
      </CardHeader>
      <CardContent className="w-full">{
        afterEval ? (
          <>
          <form action={submitForm}>
            <div className="mb-8">
              <CardTitle className="mb-2">Score: {evalData[0]}</CardTitle>
              <CardDescription className="text-md text-slate-400">Job Purpose: {evalData[1]["Job Purpose"]}</CardDescription>
              <CardDescription className="text-md text-slate-400">Educational Qualification: {evalData[1]["Educational_Qualification"]}</CardDescription>
              <CardDescription className="text-md text-slate-400">Experience Qualification: {evalData[1]["Experience_Qualification"]}</CardDescription>
              <CardDescription className="text-md text-slate-400">Key Responsibilities: {evalData[1]["Key Responsibilities"]}</CardDescription>
              <CardDescription className="text-md text-slate-400">Location: {evalData[1]["Location"]}</CardDescription>
              <CardDescription className="text-md text-slate-400">Salary and Benefits: {evalData[1]["Salary and Benefits"]}</CardDescription>
              <CardDescription className="text-md text-slate-400">Skill Qualifications: {evalData[1]["Skill_Qualifications"]}</CardDescription>
              
              <CardDescription className="text-md text-slate-400 mt-8" style={{ whiteSpace: 'pre-line' }}>
                <CardTitle className="text-white -mb-3">Recommendations: </CardTitle>
                {evalData[2]}
              </CardDescription>
            </div>
            <div className="grid w-full items-center gap-1.5">
              <Label htmlFor="email">Job Title</Label>
              <Input required
                value={title}
                onChange={(e) => {
                  setTitle(e.target.value);
                }}
                name="title"
                className="bg-black text-white"
                placeholder="Enter Job Title"
              />
            </div>
            <div className="mt-5 grid w-full items-center gap-1.5">
              <Label htmlFor="email">Job Description</Label>
              <Textarea required
                value={description}
                onChange={(e) => {
                  setDescription(e.target.value);
                }}
                name="description"
                className="bg-black text-white"
                placeholder="Enter Job Description"
                style={{ whiteSpace: 'pre-line' }}
              />
            </div>
            <div className="mt-5 grid w-full items-center gap-1.5">
              <div className="flex justify-between items-center mb-2">
              <Label htmlFor="email">Edited Job Description</Label>
              <Button type="button" className="bg-white text-black hover:bg-slate-200" onClick={(e) => {
      e.preventDefault();
      const formattedValue = editedDescription.replace(/ {2,}/g, ' ');
      setDescription(formattedValue);
              }
                }>Use Edited Description</Button>
              </div>
              <Textarea disabled
                value={editedDescription}
                name="editedDescription"
                style={{ whiteSpace: 'pre-line' }}
                className="bg-black text-white"
              />
            </div>
            <Button
              className="bg-white text-black hover:bg-slate-200 mt-5 w-full"
              type="submit"
            >
              {loading ? (
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
                </div>
              ) : (
                <>
                  <h1 className="mr-2">Create and Continue</h1>{" "}
                  <AiOutlineArrowRight />
                </>
              )}
            </Button>{" "}
          </form>
        </>
        ) : !startEval ? (
          <>
            <form action={submitForm}>
              <div className="grid w-full items-center gap-1.5">
                <Label htmlFor="email">Job Title</Label>
                <Input required
                  value={title}
                  onChange={(e) => {
                    setTitle(e.target.value);
                  }}
                  name="title"
                  className="bg-black text-white"
                  placeholder="Enter Job Title"
                />
              </div>
              <div className="mt-5 grid w-full items-center gap-1.5">
                <Label htmlFor="email">Job Description</Label>
                <Textarea required
                  value={description}
                  onChange={(e) => {
                    setDescription(e.target.value);
                  }}
                  name="description"
                  style={{ whiteSpace: 'pre-line' }}
                  className="bg-black text-white"
                  placeholder="Enter Job Description"
                />
              </div>
              <Button
                className="bg-white text-black hover:bg-slate-200 mt-5 w-full"
                type="submit"
              >
                {loading ? (
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
                  </div>
                ) : (
                  <>
                    <h1 className="mr-2">Create and Continue</h1>{" "}
                    <AiOutlineArrowRight />
                  </>
                )}
              </Button>{" "}
            </form>
          </>
        ) : (
          <>
            <div role="status" className="w-full flex items-center">
              <svg
                aria-hidden="true"
                className="flex justify-center items-center w-5 h-5 text-gray-200 animate-spin dark:text-gray-600 fill-gray-600 dark:fill-gray-300"
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
              <h1 className="ml-5">Evaluating Job Description..</h1>
            </div>
          </>
        )}
        
      </CardContent>
    </Card>
  );
};

export default Form;
