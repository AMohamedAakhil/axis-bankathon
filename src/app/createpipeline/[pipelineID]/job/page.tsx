import React from "react";
import Form from "./form";
import { InsertData } from "@/server/utils";
import { redirect } from "next/navigation";
import { currentUser } from "@clerk/nextjs";

const CreatePipeline = async () => {
  const user = await currentUser();
  return (
    <div className="p-5">
      <Form user={JSON.stringify(user)} />
    </div>
  );
};

export default CreatePipeline;
