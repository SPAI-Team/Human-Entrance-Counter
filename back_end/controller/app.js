var express = require('express');
var app = express();
const Footfall = require('../models/footfall.js');
const fs = require("fs");
const path = require('path')
var cors = require('cors');
const whitelist = ['https://spai-human-counter.herokuapp.com', 'https://spai-human-counter-backend-api.herokuapp.com']
const corsOptions = {
  origin: (origin, callback) => {
    if (whitelist.indexOf(origin) !== -1) {
      callback(null, true)
    } else {
      callback(new Error())
    }
  }
}
// To enable whitelisting
//app.use(cors(corsOptions));

// Everyone able to access the API
app.use(cors());

app.use(express.json()); //parse appilcation/json data
app.use(express.urlencoded({ extended: false }));

// Get past analytics of Footfall within certain time frame
app.get("/history/:location/:startTime/:endTime", (req, res) => {
    Footfall.getFootfallInTimeframe(req.params.location, req.params.startTime, req.params.endTime, (err, footfalls) => {
        if (err) {
            console.log(err);
            return res.status(500).send(err);
        }
        return res.status(200).send(footfalls);
    });
});

// Get latest Footfall analytics (last record in db)
app.get("/latest/:location", (req, res) => {
    Footfall.getLatestFootfall(req.params.location, (err, footfall) => {
        if (err) {
            console.log(err);
            return res.status(500).send(err);
        }
        return res.status(200).send(footfall);
    });
});

// Get latest Footfall analytics for each hour for x no of hours
app.get("/latest/:location/:noHours", (req, res) => {
    Footfall.getLatestFootfallByHour(req.params.location, req.params.noHours, (err, footfalls) => {
        if (err) {
            console.log(err);
            return res.status(500).send(err);
        }
        return res.status(200).send(footfalls);
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
    let netFootfall = parseInt(req.body.netfootfall)
    Footfall.getLatestFootfall(req.body.location, (err, footfall) => {
        if (err) {
            console.log(err);
            return res.status(500).send(err);
        }
        // Check if there is a footfall record for the location and if it is a new day
        if(footfall && footfall.time.substring(0, 8) == req.body.time.substring(0,8)){
            netFootfall += footfall.currentfootfall;
        }

        Footfall.insertFootfall(req.body, netFootfall, (err, footfall) => {
            if (err) {
                console.log(err);
                return res.status(500).send(err);
            }
            return res.status(200).send(footfall);
        });
        
    });
    
});

module.exports = app;