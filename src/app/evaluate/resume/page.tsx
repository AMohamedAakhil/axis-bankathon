import { GetData } from "@/server/utils";
import ResumeForm from "./form";

const EvaluateResume = async () => {
  const jobs = await GetData("jobs");
  return (
    <div className="p-5">
      <h1 className="text-2xl">Evaluate Resume</h1>
      <ResumeForm jobs={jobs} />
    </div>
  );
};

export default EvaluateResume;
