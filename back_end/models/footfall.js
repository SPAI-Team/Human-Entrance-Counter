let db = require('./databaseConfig.js');
const pool = require('../config.js');

const footfall = {
    getFootfallInTimeframe: async function (location, startTime, endTime, callback) {
        pool.query("SELECT *,  coalesce(currentfootfall - LAG(currentfootfall) OVER (ORDER BY time), currentfootfall) AS netfootfall FROM footfall where location = $1 and (time BETWEEN $2 and $3);", [location, startTime, endTime], (err, res) => {
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
                return callback(null, res.rows[0]);
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
    },
    getLatestFootfallByHour: function (location, noHours, callback) {
        pool.query("SELECT ff.time, ff.currentfootfall, ff.location from footfall as ff, (SELECT hourTime, max(minute) as maxMinute, max(second) as maxSecond from (SELECT SUBSTRING(time, 1, 10) as hourTime, SUBSTRING(time, 11, 2) as minute, SUBSTRING(time, 13, 2) as second FROM footfall) as sub1 GROUP BY hourTime ORDER BY hourtime DESC) as sub2 WHERE ff.time = CONCAT(sub2.hourtime, sub2.maxMinute, sub2.maxSecond) and ff.location = $2 LIMIT $1;", [noHours, location], (err, res) => {
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