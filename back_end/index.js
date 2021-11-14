var app = require('./controller/app.js');

var server = app.listen(process.env.PORT || 5001, function () {
    console.log(`App online on port: ${process.env.PORT}`);
});