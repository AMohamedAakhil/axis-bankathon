import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { GetData } from "@/server/utils";

import React from "react";

const JobTable = async () => {
  const data = await GetData("jobs", 100);
  return (
    <>
      <Table>
        <TableCaption>A list of your recently created jobs.</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>Job Title</TableHead>
            <TableHead>Job Description</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((job: any) => {
            if (job.title) {
              const formattedDescription = job.description.replace(
                /\n/g,
                "<br/>",
              ); // Replace \n with <br/> for line breaks
              return (
                <TableRow key={job.id}>
                  <TableCell>{job.title}</TableCell>
                  <TableCell
                    dangerouslySetInnerHTML={{ __html: formattedDescription }}
                  />
                </TableRow>
              );
            }
            return null; // Don't render rows without a job title
          })}
        </TableBody>
      </Table>
    </>
  );
};

export default JobTable;
