let db = require('./databaseConfig.js');
const client = require('../config.js');

const footfall = {
    getFootfallInTimeframe: async function (location, startTime, endTime, callback) {
        await client.connect();
        client.query("SELECT * FROM footfall where location = $1 and (time BETWEEN $2::timestamp and $3::timestamp);", [location, startTime, endTime], (err, res) => {
            client.end();
            if (err) {
                return callback(err, null);
            }
            else {
                return callback(null, res.rows);
            }
        });
    },
    getLatestFootfall: async function (location, callback) {
        await client.connect();
        client.query("SELECT * FROM footfall where location = $1 ORDER BY footfall_id DESC LIMIT 1;", [location], (err, res) => {
            client.end();
            if (err) {
                return callback(err, null);
            }
            else {
                return callback(null, res.rows);
            }
        });
    },
    // getFootfallByTime: function (time, callback) {
    //     return db.query("SELECT * FROM footfall WHERE time = ?", [time], callback);
    // },
    insertFootfall: function (footfall, currentfootfall, callback) {
        let footfall_id = footfall.footfall_id;
        let location = footfall.location;
        let time = footfall.time;

        client.connect();
        client.query("INSERT INTO footfall (footfallid, time, currentfootfall, location) VALUES ($1,$2,$3,$4);", [footfall_id, time, currentfootfall, location], (err, res) => {
            client.end();
            if (err) {
                return callback(err, null);
            }
            else {
                return callback(null, res.rows);
            }
        });
    }
};

module.exports = footfall;