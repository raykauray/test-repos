const { spawn } = require("child_process");
const GLOBAL = require("../global/global.json");
const path = require("path");
const os = require("os");
function getPythonNameByOS() {
  let thisOS = os.platform();
  if (thisOS === "win32") return "python";
  if (thisOS === "linux" || thisOS === "darwin") return "python3";
}

function runPythonScripts(inputYamlFile) {
  return new Promise((resolve, reject) => {
    let pythonName = getPythonNameByOS();
    let pythonScriptResponse = "";
    const command = `${pythonName} ${path.join(
      __dirname,
      GLOBAL.pathToYamlValidotorPython
    )} ${inputYamlFile}`;

    const childProcess = spawn(command, { shell: true });

    childProcess.stdout.on("data", (stdOutput) => {
      pythonScriptResponse += stdOutput.toString();
    });

    childProcess.on("error", (error) => {
      console.error(error.toString());
    });
    childProcess.on("exit", (code) => {
      resolve(pythonScriptResponse);
    });
    childProcess.stderr.on("data", (stdError) => {
      console.error(stdError.toString());

      reject(stdError);
    });
  });
}
module.exports = runPythonScripts;
