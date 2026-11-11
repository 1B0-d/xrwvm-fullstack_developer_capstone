const fs = require('fs');
const path = require('path');
const mongoose = require('mongoose');
const Reviews = require('./review');
const Dealerships = require('./dealership');

async function main() {
  if (!process.env.MONGODB_URI) throw new Error('MONGODB_URI must explicitly select the target database');
  await mongoose.connect(process.env.MONGODB_URI, {serverSelectionTimeoutMS: 10000});
  for (const [model, filename, field] of [[Dealerships,'dealerships.json','dealerships'], [Reviews,'reviews.json','reviews']]) {
    const existing = await model.countDocuments();
    if (existing > 0) { console.log(`${model.modelName}: ${existing} records exist, no changes`); continue; }
    const rows = JSON.parse(fs.readFileSync(path.join(__dirname,'data',filename),'utf8'))[field];
    await model.insertMany(rows);
    console.log(`${model.modelName}: inserted ${rows.length} sample records`);
  }
  await mongoose.disconnect();
}
main().catch(async error => { console.error(error.message); await mongoose.disconnect(); process.exitCode = 1; });
