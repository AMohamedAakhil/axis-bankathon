"use client"

import { Button } from '@/components/ui/button';
import React, { useState } from 'react';
import { evaluateJob } from './actions';

const EvalJobForm = ({ jobs }: any) => {
  const [selectedJob, setSelectedJob] = useState<any>(null); // Initialize with null or an empty object
  const [evaluation, setEvaluation] = useState(null);
  const handleSubmit = async (e: any) => {
    e.preventDefault();
    if (selectedJob) {
      const data = await evaluateJob(selectedJob.title, selectedJob.description);
      setEvaluation(data);
    }
  };

  return (
    <div>
      <form>
        <select
          onChange={(e) => setSelectedJob(JSON.parse(e.target.value))}
          className="mt-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-3 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        >
          <option value="" disabled selected>
            Choose a job title
          </option>
          {jobs.map((job: any) => {
            if (job.title) {
              return (
                <option key={job.title} value={JSON.stringify(job)}>
                  {job.title}
                </option>
              );
            }
            return null;
          })}
        </select>
        <Button
          onClick={(e) => handleSubmit(e)}
          className="w-full bg-white text-slate-950 mt-5 hover:bg-slate-300"
        >
          Submit
        </Button>
      </form>
      <div className="mt-5 flex justify-center items-center">
        {evaluation && (
          <>
                    <h1 className="text-xl">{evaluation}</h1>
          </>
        )}
      </div>
    </div>
  );
};

export default EvalJobForm;
