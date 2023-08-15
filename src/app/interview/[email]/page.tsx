import React from 'react'
import { currentUser } from '@clerk/nextjs/server'
import InterviewForm from './form'
import { getInterviewQuestions } from './actions'
import { GetCandidateData, GetData } from '@/server/utils'

const Interview = async () => {
    const user = await currentUser();
    const email = user?.emailAddresses[0]?.emailAddress;
    //const selected_candidates = await GetCandidateData("selected_candidates", 10, email);
    //const questions = await getInterviewQuestions(selected_candidates.title, selected_candidates.description, selected_candidates.cv);  
    const questions = JSON.parse("\n          {\n            \"questions\": [\n              {\n                \"text\": \"What programming languages are you experienced in?\"\n              },\n              {\n                \"text\": \"What projects have you worked on that involved software engineering?\"\n              },\n              {\n                \"text\": \"How would you describe your experience with software engineering?\"\n              },\n              {\n                \"text\": \"Do you have experience working with databases and web development?\"\n              },\n              {\n                \"text\": \"What processes do you use to ensure the quality of your work?\"\n              },\n              {\n                \"text\": \"What experience do you have with debugging and troubleshooting software?\"\n              },\n              {\n                \"text\": \"Describe a time when you encountered a difficult problem in software engineering and how you solved it.\"\n              }\n            ]\n          }") 
  return (
    <div>
        <InterviewForm user={user} questions={questions} />
    </div>
  )
}

export default Interview