import redis from 'redis';

const client = redis.createClient({
  host: '127.0.0.1',
  port: 6379
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

client.subscribe('holberton school channel', (err, count) => {
  if (err) {
    console.log(`Error subscribing to channel: ${err}`);
  } else {
    console.log(`Subscribed to holberton school channel`);
  }
});

client.on('message', (channel, message) => {
  console.log(`Received message ${message} from channel ${channel}`);
  if (message === 'KILL_SERVER') {
    client.unsubscribe();
    client.quit();
  }
});
