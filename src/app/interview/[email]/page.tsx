import React from 'react'
import { currentUser } from '@clerk/nextjs/server'
import InterviewForm from './form'
import { getInterviewQuestions } from './actions'
import { GetCandidateData, GetData } from '@/server/utils'

const Interview = async () => {
    const user = await currentUser();
    const email = user?.emailAddresses[0]?.emailAddress;
    const selected_candidates = await GetCandidateData("selected_candidates", 10, email);
    //const questions = await getInterviewQuestions(selected_candidates.title, selected_candidates.description, selected_candidates.cv);  
    const questions = JSON.parse(`
    {
      "questions": [
        {
          "text": "Can you tell us about your experience in the banking industry?"
        },
        {
          "text": "What do you consider to be the most important skills for a successful bank manager?"
        },
        {
          "text": "How do you handle customer service and ensure client satisfaction?"
        },
        {
          "text": "Describe a situation where you had to resolve a conflict within your team or with a client. How did you handle it?"
        },
        {
          "text": "In a rapidly changing financial landscape, how do you stay updated on industry trends and regulatory changes?"
        },
        {
          "text": "Can you share an example of how you've effectively managed a team of bank employees?"
        },
        {
          "text": "What strategies would you implement to attract new customers and retain existing ones?"
        },
        {
          "text": "How do you ensure compliance with banking regulations and policies in your day-to-day operations?"
        },
        {
          "text": "Describe a time when you had to make a tough decision that had financial implications for the bank. How did you approach it?"
        }
      ]
    }
    `);
      return (
    <div>
        <InterviewForm user={user} questions={questions} />
    </div>
  )
}

export default Interview