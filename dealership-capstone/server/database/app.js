const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const app = express();
const port = Number(process.env.PORT || 3030);
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
const Reviews = require('./review');
const Dealerships = require('./dealership');

// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API")
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({dealership: req.params.id});
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const documents = await Dealerships.find({ state: req.params.state });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const documents = await Dealerships.find({ id: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

//Express route to insert review
app.post('/insert_review', async (req, res) => {
  try {
    const data = req.body;
    if (!data || typeof data !== 'object' || Array.isArray(data)) {
      return res.status(400).json({error: 'Expected a JSON object'});
    }
    const last = await Reviews.findOne().sort({ id: -1 });
    const review = new Reviews({ ...data, id: last ? last.id + 1 : 1 });
    const saved = await review.save();
    return res.json(saved);
  } catch (error) {
    return res.status(error.name === 'ValidationError' ? 400 : 500)
      .json({ error: 'Could not insert review' });
  }
});

// Normal startup connects only; it never deletes or seeds collections.
async function start() {
  const uri = process.env.MONGODB_URI || 'mongodb://mongo_db:27017/dealershipsDB';
  await mongoose.connect(uri, { serverSelectionTimeoutMS: 10000 });
  const server = app.listen(port, process.env.HOST || '127.0.0.1', () => console.log(`API listening on ${port}`));
  const shutdown = () => server.close(() => {
    mongoose.disconnect().then(() => process.exit(0)).catch(() => process.exit(1));
  });
  process.once('SIGTERM', shutdown);
  process.once('SIGINT', shutdown);
}
if (require.main === module) {
  start().catch(error => { console.error('MongoDB connection failed:', error.message); process.exitCode = 1; });
}
module.exports = { app, start };
