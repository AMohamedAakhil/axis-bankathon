"use client";

import React from "react";
import { Button } from "./ui/button";
import { useRouter } from "next/navigation";

const RedirectButton = ({ className, to, text }: any) => {
  const router = useRouter();
  return (
    <>
      <Button
        className={className}
        onClick={() => {
          router.push(to);
        }}
      >
        {text}
      </Button>
    </>
  );
};

export default RedirectButton;
