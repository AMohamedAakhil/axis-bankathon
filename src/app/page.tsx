import JobTable from "@/components/JobTable";
import RedirectButton from "@/components/redirectButton";
import { GetData } from "@/server/utils";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default async function Home() {
  const data = await GetData("jobs", 100);
  return (
    <main className="p-5 mt-1">
      <div className="flex justify-between">
        <h1 className="text-2xl">Dashboard</h1>
        <RedirectButton
          className="bg-white text-black hover:bg-slate-200"
          to="/createpipeline/job"
          text="Create New Pipeline"
        />
      </div>
      <div className="mt-5">
        <Card className="bg-black text-white">
          <CardHeader>
            <CardTitle>Your Pipelines</CardTitle>
            <CardDescription>
              View, create and edit your pipelines here
            </CardDescription>
          </CardHeader>
          <CardContent className="-mt-10 grid grid-cols-2 gap-4">
            {data.map((job: any) => {
              if (job.title) {
                const formattedDescription = job.description.replace(
                  /\n/g,
                  "<br/>",
                ); // Replace \n with <br/> for line breaks
                return (
                  <Card key={job.title} className="mt-10 bg-black text-white border-dashed hover:border-solid">
                    <CardHeader>
                      <CardTitle>Job Title: {job.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p
                        dangerouslySetInnerHTML={{
                          __html: formattedDescription,
                        }}
                      ></p>
                    </CardContent>
                  </Card>
                );
              }
              return null; // Don't render rows without a job title
            })}
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
