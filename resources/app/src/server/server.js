const express = require("express");
const router = require("./api");
const cors = require("cors");
const app = express();
app.use(cors());
app.use("/", router);

function startServer() {
  console.log("starting server");
  app.listen(6659, () => {
    console.log("listenig on 6659");
  });
}
module.exports = startServer;
