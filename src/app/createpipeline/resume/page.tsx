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
    var cvs = [
        `
        John Doe
        Address: 123 Main Street, City, State ZIP
        Phone: (123) 456-7890
        Email: john.doe@email.com
        
       
        `,
        `
        Jane Smith
        Address: 456 Elm Avenue, Town, State ZIP
        Phone: (987) 654-3210
        Email: jane.smith@email.com
        
        Summary:
        Results-oriented marketing professional with a strong background in digital marketing strategies. Skilled in developing and implementing data-driven marketing campaigns that drive engagement and conversions. Proficient in social media management and content creation.
        
        Skills:
        - Digital Marketing
        - Social Media Management
        - Data Analysis
        - Content Creation
        - Market Research
        
        Certifications:
        - Google Ads Certification
        - HubSpot Inbound Marketing Certification

        Summary:
        Dedicated and motivated professional with 5+ years of experience in project management. Proven track record of successfully leading cross-functional teams and delivering projects on time and within budget. Excellent communication and problem-solving skills.

        
        Skills:
        - Project Planning and Execution
        - Team Leadership
        - Risk Management
        - Communication
        - Budgeting and Financial Analysis
        `
    ];
    
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
