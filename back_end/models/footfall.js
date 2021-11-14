let db = require('./databaseConfig.js');
const pool = require('../config.js');

const footfall = {
    getFootfallInTimeframe: async function (location, startTime, endTime, callback) {
        pool.query("SELECT * FROM footfall where location = $1 and (time BETWEEN $2 and $3);", [location, startTime, endTime], (err, res) => {
            if (err) {
                return callback(err, null);
            }
            else {
                return callback(null, res.rows);
            }
        });
    },
    getLatestFootfall: async function (location, callback) {
        pool.query("SELECT * FROM footfall where location = $1 ORDER BY footfallid DESC LIMIT 1;", [location], (err, res) => {
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
        let location = footfall.location;
        let time = footfall.time;

        pool.query("INSERT INTO footfall (time, currentfootfall, location) VALUES ($1,$2,$3);", [time, currentfootfall, location], (err, res) => {
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