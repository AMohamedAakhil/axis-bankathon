import { UserButton } from '@clerk/nextjs'
import React from 'react'
import Link from 'next/link'
import Image from 'next/image'

const Navbar = () => {
  return (
    <div className="bg-black border-bottom border-b text-white p-5 flex justify-between">
        <Link href="/" className=""><Image alt="logo" src="/logo.png" width={50} height={50}></Image></Link>
        <div className="flex gap-8 items-center">
            <Link href="/add" className="text-gray-300">Add Resume</Link>
            <Link href="/addjob" className="text-gray-300">Add Job</Link>
            <UserButton afterSignOutUrl="/"/>
        </div>
    </div>
  )
}

export default Navbar