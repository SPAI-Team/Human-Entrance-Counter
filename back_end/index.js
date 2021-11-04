var app = require('./controller/app.js');
var port = 8081;

var server = app.listen(port, function () {
    console.log("App hosted at localhost:" + port);
});