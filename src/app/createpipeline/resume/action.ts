"use server";

export const evaluateResumes = async (title: string, description: string, cv_list: string[]) => {
  const requestData = {
    job_title: title,
    job_description: description,
    cv_list: cv_list
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/cv_ranking/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData), // Serialize the data as JSON
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
