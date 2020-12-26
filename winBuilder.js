const electronInstaller = require("electron-winstaller");
(async () => {
  try {
    await electronInstaller.createWindowsInstaller({
      appDirectory: "/home/zaheer/Desktop/Learning/electron_app_build",
      outputDirectory: "/home/zaheer/Desktop/Learning/electron_app_build/winBuild",
      authors: "My App Inc.",
      exe: "myapp.exe",
    });
    console.log("It worked!");
  } catch (e) {
    console.log(`No dice: ${e.message}`);
  }
})();
