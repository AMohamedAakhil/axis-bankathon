"use server";

export const evaluateJob = async (title: string, description: string) => {
  const requestData = {
    job_title: title,
    job_description: description,
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/job_desc_score/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData), // Serialize the data as JSON
      cache: "no-store",
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData = await response.json();

    return responseData; // This will include the score, components, and edited description
  } catch (error) {
    console.error("An error occurred:", error);
    return null;
  }
};
