import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import React from 'react'
import { InsertData } from '@/server/utils'
import {redirect} from "next/navigation"
import { currentUser } from '@clerk/nextjs'

const AddJob = () => {
     async function submitForm (formData: FormData) {
        "use server"
        const user = await currentUser();
        const title = formData.get("title")
        const description = formData.get("description")
        const response = {title: title, description: description, user: user}
        const res = await InsertData("jobs", JSON.parse(JSON.parse(JSON.stringify(response))))
        console.log(res)
        redirect('/')
    }
  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-1/2">
    <h1 className="text-2xl">Create new job</h1>
    <form action={submitForm}>
        <Input name="title" type="text" className="mt-5 text-black" placeholder="Job title" />
        <Textarea name="description" className="mt-5 text-black" placeholder="Job description" />
        <Button type="submit" className="w-full bg-white text-slate-950 mt-5 hover:bg-slate-300">Submit</Button>
    </form>
  </div>
  )
}

export default AddJob