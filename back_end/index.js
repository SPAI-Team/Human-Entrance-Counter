var app = require('./controller/app.js');
let config = require('./config.js')
var port = 8081;

var server = app.listen(config.PORT || 5000, function () {
    console.log("App online");
});