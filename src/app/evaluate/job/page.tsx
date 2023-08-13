import { evaluateJob } from "./actions";
import { GetData } from "@/server/utils";
import EvalJobForm from "./form";

const EvaluateJob = async () => {
  const jobs = await GetData("jobs");
  return (
    <div className="p-5">
      <EvalJobForm jobs={jobs} />
    </div>
  );
};

export default EvaluateJob;
