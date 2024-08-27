import kue from 'kue';

const queue = kue.createQueue();

const jobData = {
  phoneNumber: '1234567890',
  message: 'Hello from Holberton!',
};

const job = queue.create('push_notification_code', jobData).save((err) => {
  if (err) {
    console.log(`Error creating job: ${err}`);
  } else {
    console.log(`Notification job created: ${job.id}`);
  }
});

queue.on('job complete', (id) => {
  console.log(`Notification job completed: ${id}`);
});

queue.on('job failed', (id, err) => {
  console.log(`Notification job failed: ${id} - ${err}`);
});
