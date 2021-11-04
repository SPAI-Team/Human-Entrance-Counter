let db = require('./databaseConfig.js');

const footfall = {
    getAllFootfall: function (callback) {
        return db.query("SELECT * FROM footfall", callback);
    },
    getLatestFootfall: function (callback) {
        return db.query("SELECT * FROM footfall ORDER BY footfall_id DESC LIMIT 1", callback);
    },
    getFootfallByDate: function (date, callback) {
        return db.query("SELECT * FROM footfall WHERE date = ?", [date], callback);
    },
    insertFootfall: function (footfall, callback) {
        return db.query('INSERT INTO footfall (footfall_id, date, time, number_of_people) VALUES (?,?,?,?)', [footfall.footfall_id, footfall.date, footfall.time, footfall.number_of_people], callback);
    },
    // Delete Footfall of a particular date and time
    deleteFootfall: function (date, time, callback) {
        return db.query('DELETE FROM footfall WHERE date = ? AND time = ?', [date, time], callback);
    },
    updateFootfall: function (footfall, callback) {
        return db.query('UPDATE footfall SET date = ?, time = ?, number_of_people = ? WHERE footfall_id = ?', [footfall.date, footfall.time, footfall.number_of_people, footfall.footfall_id], callback);
    },
};