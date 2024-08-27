const express = require('express');
const redis = require('redis');
const kue = require('kue');
const { promisify } = require('util');

// Create Redis client and promisify functions
const client = redis.createClient();
const reserveSeat = promisify(client.set).bind(client);
const getCurrentAvailableSeats = promisify(client.get).bind(client);

// Create Kue queue
const queue = kue.createQueue();

// Initialize seats and reservation status
let reservationEnabled = true;
const initialSeats = 50;

// Set initial seats when starting the application
reserveSeat('available_seats', initialSeats);

// Express server setup
const app = express();
const port = 1245;

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats('available_seats');
  res.json({ numberOfAvailableSeats: availableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

// Route to process the queue
app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats('available_seats');
    const seatsLeft = parseInt(availableSeats, 10);

    if (seatsLeft <= 0) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }

    const newSeats = seatsLeft - 1;
    await reserveSeat('available_seats', newSeats);

    if (newSeats === 0) {
      reservationEnabled = false;
    }

    done();
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
