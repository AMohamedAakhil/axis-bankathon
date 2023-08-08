import { GetData } from "@/server/utils"

export default async function Home() {
  const data = await GetData("test", 100);
  console.log(data);
  return (
    <main className="text-4xl">
      Dashboard
    </main>
  )
}
