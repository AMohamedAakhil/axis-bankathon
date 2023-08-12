"use server"

export const evaluateJob = async (title: string, description: string) => {
    const requestData = {
        job_title: title,
        job_description: description
    };

    const response = await fetch('http://127.0.0.1:8000/job_desc_score/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData), // Serialize the data as JSON
        cache: 'no-store'
    });

    const jsonResponse = await response.json();
    return jsonResponse;
}

