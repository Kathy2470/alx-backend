import redis from 'redis';

// Create a Redis client
const client = redis.createClient();

// Handle successful connection
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Handle connection errors
client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err}`);
});

// Define hash key and values
const hashKey = 'HolbertonSchools';
const hashValues = {
  Portland: '50',
  Seattle: '80',
  'New York': '20',
  Bogota: '20',
  Cali: '40',
  Paris: '2'
};

// Function to set hash values
function createHash() {
  for (const [field, value] of Object.entries(hashValues)) {
    client.hset(hashKey, field, value, redis.print);
  }
}

// Function to display hash values
function displayHash() {
  client.hgetall(hashKey, (err, obj) => {
    if (err) {
      console.error(`Error fetching the hash: ${err}`);
    } else {
      console.log(obj);
    }
  });
}

// Execute functions
createHash();
displayHash();
