"use server";

import { connectToDatabase } from "./mongo";
import { ObjectId } from "mongodb";
import { currentUser } from "@clerk/nextjs";

export async function GetData(collection: string, limit: number = 30) {
  const user = await currentUser();
  const { db } = await connectToDatabase();
  const coll = await db.collection(collection);
  const results = await coll
    .find({ "user.id": user!.id })
    .limit(limit)
    .toArray();
  return results;
}

export async function GetPipelineData(collection: string, limit: number = 30, pipelineID: any) {
  const user = await currentUser();
  const { db } = await connectToDatabase();
  const coll = await db.collection(collection);
  const results = await coll
    .find({ "pipelineID": pipelineID })
    .limit(limit)
    .toArray();
  return results;
}


export async function GetEvalData(collection: string, limit: number = 30) {
  const user = await currentUser();
  const { db } = await connectToDatabase();
  const coll = await db.collection(collection);
  const results = await coll
    .find({ "user.id": user!.id })
    .limit(limit)
    .toArray();
  return results;
}

export async function InsertData(collection: string, data: any) {
  const { db } = await connectToDatabase();
  const coll = await db.collection(collection);
  const results = await coll.insertOne(data);
  return results;
}

export async function UpdateData(
  collection: string,
  stringId: string,
  formData: any,
) {
  const { db } = await connectToDatabase();
  const coll = await db.collection(collection);
  const id = new ObjectId(stringId);
  const existingData = await coll.findOne({ _id: id });
  if (!existingData) {
    throw new Error("Data not found.");
  }
  const updatedData = { ...existingData, ...formData };
  const results = await coll.updateOne({ _id: id }, { $set: updatedData });
  return results;
}

export async function DeleteData(collection: string, stringId: string) {
  const { db } = await connectToDatabase();
  const coll = await db.collection(collection);
  const id = new ObjectId(stringId);
  const results = await coll.deleteOne({ _id: id });
  return results;
}
