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

const Resume = async () => {
    var cvs = [
        `
        John Doe
        Address: 123 Main Street, City, State ZIP
        Phone: (123) 456-7890
        Email: john.doe@email.com
        
        Summary:
        Dedicated and motivated professional with 5+ years of experience in project management. Proven track record of successfully leading cross-functional teams and delivering projects on time and within budget. Excellent communication and problem-solving skills.
        
        Experience:
        Project Manager | ABC Company | City, State | Jan 2020 - Present
        - Led a team of 10 to execute projects from initiation to closure, resulting in a 20% increase in on-time project delivery.
        - Developed and monitored project plans, budgets, and schedules, ensuring adherence to quality standards.
        - Collaborated with stakeholders to define project scope and objectives, and managed scope changes effectively.
        
        Assistant Project Manager | XYZ Corporation | City, State | Jun 2017 - Dec 2019
        - Assisted in planning and executing various projects, contributing to a 15% improvement in team productivity.
        - Coordinated project activities, including resource allocation and progress tracking.
        - Prepared status reports and presentations for senior management, facilitating informed decision-making.
        
        Education:
        Bachelor of Science in Business Management | University of ABC | Graduated May 2017
        
        Skills:
        - Project Planning and Execution
        - Team Leadership
        - Risk Management
        - Communication
        - Budgeting and Financial Analysis
        
        Certifications:
        - Project Management Professional (PMP)
        - Agile Certified Practitioner (ACP)
        `,
        `
        Jane Smith
        Address: 456 Elm Avenue, Town, State ZIP
        Phone: (987) 654-3210
        Email: jane.smith@email.com
        
        Summary:
        Results-oriented marketing professional with a strong background in digital marketing strategies. Skilled in developing and implementing data-driven marketing campaigns that drive engagement and conversions. Proficient in social media management and content creation.
        
        Experience:
        Digital Marketing Manager | DEF Agency | Town, State | Feb 2018 - Present
        - Managed end-to-end digital marketing campaigns for clients, achieving an average 30% increase in online sales.
        - Analyzed campaign performance metrics and adjusted strategies to optimize ROI and conversion rates.
        - Oversaw social media accounts, creating engaging content and growing follower base by 40%.
        
        Marketing Specialist | GHI Solutions | City, State | Aug 2015 - Jan 2018
        - Assisted in creating and executing marketing campaigns, resulting in a 25% increase in website traffic.
        - Conducted market research to identify trends and opportunities, contributing to product development decisions.
        - Collaborated with design team to create visually appealing marketing collateral.
        
        Education:
        Bachelor of Arts in Marketing | University of XYZ | Graduated June 2015
        
        Skills:
        - Digital Marketing
        - Social Media Management
        - Data Analysis
        - Content Creation
        - Market Research
        
        Certifications:
        - Google Ads Certification
        - HubSpot Inbound Marketing Certification
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
        <CardContent className=' grid grid-cols-2 gap-4'>{res ? 
          res.map((evaluation: any) => (
            <Card key={evaluation.contact_info} className="bg-black text-white p-5 mb-5">
              <CardTitle>{evaluation.contact_info}</CardTitle>
              <CardTitle>{evaluation.score}</CardTitle>
              <CardDescription>{evaluation.short_summary}</CardDescription>
            </Card>
          )) : <CardDescription>No CVs to display.</CardDescription>}
        </CardContent>
      </Card>
    </div>
  );
};

export default Resume;
