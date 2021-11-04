const express = require("express");
const app = express();
app.use(express.static(__dirname + '/public'));
app.listen(process.env.PORT || 4000, () => {
    console.log(`Client server has started listening on port ${process.env.PORT}`);
});