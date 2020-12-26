const { fstat } = require("fs");
const fs = require("fs");
const http = require("follow-redirects").https;
const GLOBAL = require("../global/global.json");
const path = require("path");
const runPythonScripts = require("./pythonScriptUtil");
class YAMLController {
  async initProcess(queryParams) {
    let keyNames = Object.keys(queryParams);
    let response = {};
    for (let i = 0; i < keyNames.length; i++) {
      const formattedUrl = this.formatUrl(queryParams[keyNames[i]]);
      let randomFileName = this.generateRandomFileName();
      const pathToFile = path.resolve(
        __dirname,
        GLOBAL.pathToTempDir,
        randomFileName
      );

      try {
        const resStream = await this.downloadFile(formattedUrl);
        await this.writeFileOnFs(resStream, pathToFile);
        const res = await runPythonScripts(pathToFile);
        response[keyNames[i]] = res;
      } catch (error) {
        console.error(error);
      }
      await this.deleteFile(pathToFile);
    }
    return response;
  }

  async deleteFile(pathToFile) {
    fs.unlink(pathToFile, () => {});
  }
  formatUrl(url) {
    return url.replace("blob", "raw");
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

  async writeFileOnFs(resStream, pathToFile) {
    return new Promise((resolve, reject) => {
      const fileStream = fs.createWriteStream(pathToFile);
      resStream.pipe(fileStream).on("finish", () => {
        resolve();
      });
    });
  }
  generateRandomFileName() {
    let randomString = (Math.random() + 1).toString(36).substr(2, 5);
    let extendedRamdomString = randomString + ".yaml";
    return extendedRamdomString;
  }
  checkYamlFile() {}
}
module.exports = new YAMLController();
// const obj = new YAMLController();
// obj.initProcess("https://github.com/raykauray/test-repos/blob/master/app.yaml");
