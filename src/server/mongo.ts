import { MongoClient } from "mongodb";

const MONGO_URI: string = process.env.MONGO_URI!;
const MONGO_DB = process.env.MONGO_DB;

interface GlobalMongo {
  conn: any; // Replace 'any' with the appropriate type for your MongoDB connection
  promise: Promise<any> | null; // Replace 'any' with the appropriate type for your MongoDB promise
}

declare const global: {
  mongo: GlobalMongo;
};

if (!MONGO_URI) {
  throw new Error("Please define the MONGO URI in the environment variables");
}

if (!MONGO_DB) {
  throw new Error("Please define MONGO_DB in the environment variables");
}

let cached = global.mongo;

if (!cached) {
  cached = global.mongo = { conn: null, promise: null };
}

export async function connectToDatabase() {
  if (cached.conn) {
    return cached.conn;
  }

  if (!cached.conn) {
    cached.promise = MongoClient.connect(MONGO_URI).then((client) => {
      return {
        client,
        db: client.db(MONGO_DB),
      };
    });
  }

  cached.conn = await cached.promise;
  return cached.conn;
}