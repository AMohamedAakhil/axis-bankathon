"use server";

export const evaluateResume = async () => {
  await sleep(7000);
  const cvRankings = {
    "emma_watson_cv.pdf": {
      name: "Emma Watson",
      experienceYears: 6,
      educationLevel: "Master's",
      skills: ["JavaScript", "React", "Node.js"],
      languageProficiency: "Advanced",
      overallScore: 89,
    },
    "liam_smith_cv.docx": {
      name: "Liam Smith",
      experienceYears: 4,
      educationLevel: "Bachelor's",
      skills: ["Python", "Data Analysis", "SQL"],
      languageProficiency: "Intermediate",
      overallScore: 76,
    },
    "olivia_jones_cv.pdf": {
      name: "Olivia Jones",
      experienceYears: 8,
      educationLevel: "PhD",
      skills: ["Machine Learning", "TensorFlow", "Python"],
      languageProficiency: "Advanced",
      overallScore: 95,
    },
    "william_brown_cv.docx": {
      name: "William Brown",
      experienceYears: 2,
      educationLevel: "Bachelor's",
      skills: ["Java", "C++", "Software Engineering"],
      languageProficiency: "Intermediate",
      overallScore: 68,
    },
    // ... Add more CV entries here ...
  };

  return cvRankings;
};

function sleep(ms: number) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}
