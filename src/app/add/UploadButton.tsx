"use client"
import React from 'react'
import { useState } from 'react'
import { Button } from '@/components/ui/button'

const UploadButton = ({className, type}: any) => {
    const [loading, setLoading] = useState(false)
    const handleClick = () => setLoading(true)
  return (
    <Button className={className} type={type} onClick={handleClick}>{loading? "loading" : "Upload"}</Button>
  )
}

export default UploadButton