var app = require('./controller/app.js');

var server = app.listen(parseInt(process.env.PORT)+1 || 5001, function () {
    console.log(`App online on port: ${parseInt(process.env.PORT)+1}`);
});