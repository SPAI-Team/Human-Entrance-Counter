var express = require('express');
var app = express();
const Footfall = require('../models/footfall');
const fs = require("fs");
var cors = require('cors');

app.options('*', cors());
app.use(cors());
app.use(express.json()); //parse appilcation/json data
app.use(express.urlencoded({ extended: false }));

// Get all past analytics of Footfall
app.get("/history/", (req, res) => {
    Footfall.getAllFootfalls((err, footfalls) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        res.status(200).send(footfalls);
    });
});

// Get latest Footfall analytics
app.get("/latest/", (req, res) => {
    Footfall.getLatestFootfall((err, footfall) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        res.status(200).send(footfall);
    });
});

// Get Footfall of a particular date
app.get("/history/:date", (req, res) => {
    Footfall.getFootfallByDate(req.params.date, (err, footfall) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        res.status(200).send(footfall);
    });
});

// Insert Footfall of a particular date and time
app.post("/history/:date/:time", (req, res) => {
    Footfall.insertFootfall(req, (err, footfall) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        res.status(200).send(footfall);
    });
});

// Update Footfall of a particular date and time
app.put("/history/:date/:time", (req, res) => {
    Footfall.updateFootfall(req, (err, footfall) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        res.status(200).send(footfall);
    });
});

// Delete Footfall of a particular date and time
app.delete("/history/:date/:time", (req, res) => {
    Footfall.deleteFootfall(req.params.date, req.params.time, (err, footfall) => {
        if (err) {
            console.log(err);
            res.status(500).send();
        }
        res.status(200).send(footfall);
    });
});

module.exports = app;