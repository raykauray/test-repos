const express = require("express");
const router = require("./api");

const app = express();
app.use("/", router);

app.listen(6659, () => {
  console.log("listenig on 6659");
});
