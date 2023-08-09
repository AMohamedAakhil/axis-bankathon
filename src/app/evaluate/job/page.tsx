
const EvaluateJob = async () => {
    const jobTitle = "Software Engineer"
    const jobDescription = "We are looking for a software engineer to join our team. You will be working on a new project that will be used by millions of people. You will be working with a team of 5 other engineers. You will be working with React, Node, and TypeScript."
    const response: any = await fetch(`http://127.0.0.1:8000/job_desc_score?job_title=${jobTitle}&job_description=${jobDescription}`)
    const jsonResponse = await response.json()
    console.log(jsonResponse);
    
  return (
    <div>EvaluateJob</div>
  )
}

export default EvaluateJob