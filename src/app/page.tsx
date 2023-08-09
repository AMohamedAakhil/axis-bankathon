import { GetData } from "@/server/utils"

export default async function Home() {
  const data = await GetData("test", 100);
  console.log(data);
  return (
    <main className="p-5">
      <h1 className="text-xl">Dashboard</h1>
    </main>
  )
}
