"use client"

import React, {useState} from 'react'

const InterviewForm = ({user} : any) => {
  return (
    <div>{user.emailAddresses[0].emailAddress}</div>
  )
}

export default InterviewForm