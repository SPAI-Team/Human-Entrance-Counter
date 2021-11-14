const express = require("express");
const app = express();
app.use(express.static(__dirname ));

app.listen(process.env.PORT || 5000, () => {
    console.log(`Client server has started listening on port ${process.env.PORT || 5000}`);
});