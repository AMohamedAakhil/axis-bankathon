"use client"

import React from 'react'
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card";

import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
  

type params = {
    contact_info: string,
    score: string,
    summary: string
    rank: number
    key: number
    element_wise_score: number[],
}

const CVCard = ({contact_info, score, summary, rank, key, element_wise_score}: params) => {
  return (
    <Dialog>
<DialogTrigger className="bg-black">
<Card key={key} className="bg-black h-full text-white p-5 mb-5 hover:border-dashed hover:bg-slate-950" >
    <CardTitle className="text-right h-full flex justify-between" style={{ whiteSpace: 'pre-line' }}>
      <div className="text-start">
      <h1 className="text-2xl">Rank: {rank}</h1>
      <h1 className="text-6xl">{score}/100</h1>
      </div>
      <div className="font-light">
      {contact_info}
      </div>
      </CardTitle>
  </Card>
</DialogTrigger>
<DialogContent className="bg-black">
    <DialogHeader>
    <h1 className="text-2xl">Rank: {rank}</h1>
      <h1 className="text-6xl">{score}/100</h1>    </DialogHeader>
      <h1 className="font-extralight" style={{ whiteSpace: 'pre-line' }}><h1 className="text-xl mb-2 font-medium">Personal Information: </h1>{contact_info}</h1>
      <h1 className="font-extralight" style={{ whiteSpace: 'pre-line' }}><h1 className="text-xl font-medium">Element Wise Score: </h1></h1>
      <div>
      {Object.keys(element_wise_score).map((key: any) => (
        <h1 className="font-extralight" key={key}>
          {key}: {element_wise_score[key]}
        </h1>
      ))}
      </div>
      <h1 className="font-extralight" style={{ whiteSpace: 'pre-line' }}><h1 className="text-xl font-medium">Summary: </h1>{summary}</h1>
</DialogContent>
    
  </Dialog>

  )
}

export default CVCard