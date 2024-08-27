const kue = require('kue');
const redis = require('redis');

// Create a Redis client
const redisClient = redis.createClient({
  host: 'localhost', // Your Redis server host
  port: 6379,        // Your Redis server port
  password: 'your_redis_password' // Replace with your actual Redis password if required
});

// Create a Kue queue instance
const queue = kue.createQueue({
  redis: redisClient
});

// Define the job data
const jobData = {
  phoneNumber: '4153518780',
  message: 'This is the code to verify your account'
};

// Create a job in the queue
const job = queue.create('push_notification_code', jobData).save((err) => {
  if (err) {
    console.error('Error creating job:', err);
  } else {
    console.log(`Notification job created: ${job.id}`);
  }
});

// Handle job completion
queue.on('job complete', (id) => {
  console.log(`Notification job ${id} completed`);
});

// Handle job failure
queue.on('job failed', (id, err) => {
  console.log(`Notification job ${id} failed: ${err.message}`);
});
