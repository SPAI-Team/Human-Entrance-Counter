var express = require('express');
var app = express();
const Footfall = require('../models/footfall.js');
const fs = require("fs");
var cors = require('cors');

app.options('*', cors());
app.use(cors());
app.use(express.json()); //parse appilcation/json data
app.use(express.urlencoded({ extended: false }));

// Get past analytics of Footfall within certain time frame
app.get("/history/:location/:pastTime", (req, res) => {
    Footfall.getAllFootfall(req.params.location, req.params.pastTime, (err, footfalls) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        res.status(200).send(footfalls);
    });
});

app.get('/', (req, res) => {
    res.send('Hello World!');
});


// Get latest Footfall analytics (last record in db)
app.get("/latest/:location", (req, res) => {
    Footfall.getLatestFootfall(req.params.location, (err, footfall) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        res.status(200).send(footfall);
    });
});

// // Get Footfall of a particular date
// app.get("/history/:date", (req, res) => {
//     Footfall.getFootfallByTimestamp(req.params.date, (err, footfall) => {
//         if (err) {
//             console.log(err);
//             res.status(500).send();
//         }
//         res.status(200).send(footfall);
//     });
// });

// Insert Footfall of a particular timestamp and location
app.post("/history", (req, res) => {
    Footfall.insertFootfall(req, (err, footfall) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        res.status(200).send(footfall);
    });
});

// Update Footfall of a particular timestamp and location
app.put("/history", (req, res) => {
    Footfall.updateFootfall(req, (err, footfall) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        res.status(200).send(footfall);
    });
});

// Delete Footfall of a particular date and time
app.delete("/history/:timestamp/:location", (req, res) => {
    Footfall.deleteFootfall(req.params.timestamp, req.params.location, (err, footfall) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        res.status(200).send(footfall);
    });
});

module.exports = app;