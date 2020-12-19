const { fstat } = require("fs");
const fs = require("fs");
const http = require("http");
const GLOBAL = require("../global/global.json");
const path = require("path");
class YAMLController {
  async initProcess(url) {
    try {
      const resStream = await this.downloadFile(url);
      const pathToFile = path.resolve(__dirname, "../temp/file.yaml");
      this.writeFileOnFs(resStream, pathToFile);
      checkFile();
    } catch (error) {
      throw new Error(error);
    }
  }

  downloadFile(url) {
    return new Promise((resolve, reject) => {
      try {
        http.get(url, (res) => {
          resolve(res);
        });
      } catch (error) {
        reject(error);
      }
    });
  }

  writeFileOnFs(resStream, pathToFile) {
    const fileStream = fs.createWriteStream(pathToFile);
    resStream.pipe(fileStream).on("finish", () => {});
  }
}
const obj = new YAMLController();
obj.initProcess("http://www.google.com");
