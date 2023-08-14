"use client"

import React from 'react'
import { useState } from 'react'

const Dropzone = () => {
    const [uploaded, setUploaded] = useState(false)
    const uploadedFileType = 'PDF'
    const handleFileUpload = () => {
        setUploaded(false)
    }
  return (
    <div className="flex items-center justify-center w-full mt-5">
    <label
      htmlFor="dropzone-file"
      className={`flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer ${
        uploaded ? 'bg-green-300' : 'bg-black hover:bg-slate-950'
      }`}
    >
      <div className="flex flex-col items-center justify-center pt-5 pb-6">
        {uploaded ? (
          <svg
            className="w-8 h-8 mb-4 text-green-600"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill=""
            viewBox="0 0 20 16"
          >
            <path
              stroke="#34D399"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 5"
            />
          </svg>
        ) : (
          <svg
            className="w-8 h-8 mb-4"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill=""
            viewBox="0 0 20 16"
          >
            <path
              stroke="#6b7280"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
            />
          </svg>
        )}
        <p className={`mb-2 text-sm ${uploaded ? 'text-green-600' : 'text-slate-400'}`}>
          {uploaded ? 'File uploaded successfully' : <span className="font-semibold">Click to upload</span>}
        </p>
        {uploaded ? (
          <p className="text-xs text-green-600">File type: {uploadedFileType}</p>
        ) : (
          <p className="text-xs text-slate-500">PDF, DOC, DOCX</p>
        )}
      </div>
      <input
        id="dropzone-file"
        name="files"
        type="file"
        className="hidden"
        onChange={handleFileUpload}
        multiple
      />
    </label>
  </div>
  
  )
}

export default Dropzone