var express = require('express');
var app = express();
const Footfall = require('../models/footfall.js');
const fs = require("fs");
var cors = require('cors');

app.options('*', cors());
app.use(cors());
app.use(express.json()); //parse appilcation/json data
app.use(express.urlencoded({ extended: false }));


// Testing get function (will get all records in db)
app.get("/", (req, res) => {
    Footfall.getAll((err, footfalls) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        res.status(200).send(footfalls);
    });
});


// Get past analytics of Footfall within certain time frame
app.get("/history/:location/:startTime/:endTime", (req, res) => {
    Footfall.getFootfallInTimeframe(req.params.location, req.params.startTime, req.params.endTime, (err, footfalls) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        res.status(200).send(footfalls);
    });
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
    let netFootfall = req.body.NetFootfall
    Footfall.getLatestFootfall(req.body.location, (err, footfall) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        if(footfall.length > 0){
            netFootfall += footfall.currentFootfall;
        }
    });

    Footfall.insertFootfall(req.body, netFootfall, (err, footfall) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        res.status(200).send(footfall);
    });
});


module.exports = app;