const { Client } = require('pg');

const client = new Client({
  connectionString: process.env.DATABASE_URL || 'postgres://vnewerqkqtbast:51fca90455f8a3729f4c19a2311e4240a43583a6cff0c00b0b7816fd8a2a8176@ec2-52-22-81-147.compute-1.amazonaws.com:5432/d2tkadpbl1og3m',
  ssl: {
    rejectUnauthorized: false
  }
});

module.exports = client;