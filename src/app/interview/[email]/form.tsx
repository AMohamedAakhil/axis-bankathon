"use client"

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label';
import { InsertData } from '@/server/utils';
import React, { useState } from 'react'

const InterviewForm = ({ user, questions }: any) => {
  const [questionState, setQuestionState] = useState<any>({});

  const handleInputChange = (questionText: string, value: string) => {
    setQuestionState((prevQuestionState: any) => ({
      ...prevQuestionState,
      [questionText]: value,
    }));
    console.log(questionState)
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    // Now you can do something with the captured questionState data, like sending it to a server.
    const insertRes = await InsertData("candidate_responses", questionState)
    console.log(insertRes);
  };

  if (!Array.isArray(questions.questions)) {
    return null; // Return some kind of error message or placeholder if questions is not an array.
  }

  return (
    <div className="p-5">
    <form onSubmit={handleSubmit}>
      <h1 className="mb-5 text-4xl font-semibold">Interview Questions</h1>
      <div>
        {questions.questions.map((question: any) => (
          <div className="mt-5">
          <Label className="text-white">{question.text}</Label>
          <Input
            key={question.text}
            name={question.text}
            type="text"
            placeholder={"Enter your answer here"}
            value={questionState[question.text] || ''}
            onChange={(e) => handleInputChange(question.text, e.target.value)}
            className="text-white bg-black mt-2"
          />
          </div>
        ))}
      </div>
      <Button type="submit" className="mt-5 bg-white text-black w-full hover:bg-slate-200">Submit</Button>
    </form>
    </div>
  );
}

export default InterviewForm;
