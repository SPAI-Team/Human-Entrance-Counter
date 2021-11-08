let db = require('./databaseConfig.js');
const client = require('../config.js');

const footfall = {
    getFootfall: function (location, timestamp, callback) {
        client.connect();
        client.query('SELECT * FROM footfall where timestamp = $1 and location = $2', [timestamp, location], (err, res) => {
            client.end();
            if (err) {
                return callback(err, null);
            }
            else {
                return callback(null, res.rows);
            }
        });
    },
    getLatestFootfall: function (callback) {
        return db.query("SELECT * FROM footfall where location = ? ORDER BY footfall_id DESC LIMIT 1", [location], callback);
    },
    getFootfallByTimestamp: function (timestamp, callback) {
        return db.query("SELECT * FROM footfall WHERE timestamp = ?", [timestamp], callback);
    },
    insertFootfall: function (footfall, callback) {
        return db.query('INSERT INTO footfall (footfall_id, timestamp, number_of_people, location) VALUES (?,?,?,?)', [footfall.footfall_id, footfall.timestamp, footfall.number_of_people, footfall.location], callback);
    },
    // Delete Footfall of a particular date and time
    deleteFootfall: function (timestamp, callback) {
        return db.query('DELETE FROM footfall WHERE timestamp = ?', [timestamp], callback);
    },
    updateFootfall: function (footfall, callback) {
        return db.query('UPDATE footfall SET timestamp ?, number_of_people = ?, location = ? WHERE footfall_id = ?', [footfall.timestamp, footfall.number_of_people, footfall.footfall_id, footfall.location], callback);
    },
};

module.exports = footfall;