const mongoose = require('mongoose');
require('dotenv').config();

const connections = {};

const connectDB = async () => {
  try {
    connections.region0 = await mongoose.createConnection(process.env.MONGODB_URI_REGION0);
    console.log("MongoDB Region 0 Connected…");

    connections.region1 = await mongoose.createConnection(process.env.MONGODB_URI_REGION1);
    console.log("MongoDB Region 1 Connected…");

    connections.region2 = await mongoose.createConnection(process.env.MONGODB_URI_REGION1);
    console.log("MongoDB Region 2 Connected…");

    connections.region3 = await mongoose.createConnection(process.env.MONGODB_URI_REGION1);
    console.log("MongoDB Region 3 Connected…");

    connections.region4 = await mongoose.createConnection(process.env.MONGODB_URI_REGION1);
    console.log("MongoDB Region 4 Connected…");

  } catch (err) {
    console.error("Error connecting to MongoDB: ", err);
    process.exit(1);
  }
};

module.exports = { connectDB, connections };