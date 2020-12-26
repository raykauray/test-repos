const express = require("express");
const router = express.Router();
const YamlValidator = require("./controller");

router.get("/", async (req, res) => {
  try {
    const result = await YamlValidator.initProcess(req.query);
    console.log(req.query);
    console.log(result);
    res.status(200).json({
      ...result,
    });
  } catch (error) {
    console.error(error);
  }
});

module.exports = router;
