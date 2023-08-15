import React from 'react';
import { GetData } from "@/server/utils";
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

const Resume = async () => {
   const cvs = ["https://utfs.io/f/45df0eda-b356-4c3e-bf50-2eefe388b03b_Edited%20Kapton%20Tape.pdf", "https://utfs.io/f/d84ac0ac-8877-470b-b4aa-41f131f899be_oliviabrownresume.pdf"]
    
    const res = await evaluateResumes("Bank Manger", "Manage People", cvs);
    console.log(res);

  return (
    <div className="p-5">
      <Card className="bg-black text-white">
        <CardHeader>
          <CardTitle>Applicant Ranking</CardTitle>
          <CardDescription>The ranking according to the CVs submitted for each applicant. </CardDescription>
        </CardHeader>
        <CardContent className='grid grid-cols-2 gap-4'>
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
    : <CardDescription>No CVs to display.</CardDescription>
  }
</CardContent>



      </Card>
    </div>
  );
};

export default Resume;
