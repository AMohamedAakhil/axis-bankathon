
import React from 'react'
import Upload from "./upload"
import "@uploadthing/react/styles.css";

const Add = () => {
  return (
    <div className="mt-8 p-5">
        <h1 className="text-2xl">Add new person</h1>
        <h1>Upload CV: </h1>
        <Upload />
    </div>
  )
}

export default Add