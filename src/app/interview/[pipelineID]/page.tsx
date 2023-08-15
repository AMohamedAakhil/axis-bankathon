import React from 'react'
import { currentUser } from '@clerk/nextjs/server'
import InterviewForm from './form'

const Interview = async () => {
    const user = await currentUser()
  return (
    <div>
        <InterviewForm user={user} />
    </div>
  )
}

export default Interview