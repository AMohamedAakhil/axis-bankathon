import React from "react";
import Form from "./form";
import { InsertData } from "@/server/utils";
import { redirect } from "next/navigation";
import { currentUser } from "@clerk/nextjs";

const CreatePipeline = async () => {
  const user = await currentUser();
  async function submitForm(formData: FormData) {
    "use server";
    const user = await currentUser();
    const title = formData.get("title");
    const description = formData.get("description");
    console.log(title, description);
    const response = { title: title, description: description, user: user };
    const res = await InsertData("jobs", response);
    console.log(res);
    redirect("/");
  }
  return (
    <div className="p-5">
      <Form user={user} />
    </div>
  );
};

export default CreatePipeline;
