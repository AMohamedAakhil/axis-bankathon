import { UserButton } from '@clerk/nextjs'
import React from 'react'
import Link from 'next/link'

const Navbar = () => {
  return (
    <div className="bg-slate-950 text-white p-4 flex justify-between">
        <Link href="/" className="text-2xl">Axis Bankathon</Link>
        <div className="flex gap-8 items-center">
            <Link href="/add">Add Resume</Link>
            <UserButton afterSignOutUrl="/"/>
        </div>
    </div>
  )
}

export default Navbar