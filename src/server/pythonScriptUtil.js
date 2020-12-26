const { spawn } = require("child_process");
const GLOBAL = require("../global/global.json");
const path = require("path");
function runPythonScripts(inputYamlFile) {
  return new Promise((resolve, reject) => {
    
    const command = `python3 ${path.join(
      __dirname,
      GLOBAL.pathToYamlValidotorPython
    )} ${path.join(__dirname, inputYamlFile)}`;
    
    const childProcess = spawn(command, { shell: true });
    childProcess.stdout.on("data", (stdOutput) => {
      resolve(stdOutput.toString());
    });
    childProcess.on("error", (error) => {
      console.error(error.toString());
    });
    childProcess.stderr.on("data", (stdError) => {
      console.error(stdError.toString());

      reject(stdError);
    });
  });
}
module.exports = runPythonScripts;
