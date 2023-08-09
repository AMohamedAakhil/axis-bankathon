import JobTable from "@/components/JobTable";
import { GetData } from "@/server/utils"

export default async function Home() {
  const data = await GetData("test", 100);
  console.log(data);
  return (
    <main className="p-5">
      <h1 className="text-xl">Dashboard</h1>
      <div className="mt-5">
      <JobTable />
      </div>
    </main>
  )
}
