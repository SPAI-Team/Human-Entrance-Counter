const { Client } = require('pg');
const config = require('../config.js');

const client = new Client({
    connectionString: config.DATABASE_URL,
    ssl: {
      rejectUnauthorized: false
    }
  });

module.exports = client;