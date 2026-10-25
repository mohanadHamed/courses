// Emulator Lab: list and start the AVD, install, open, rotate, then read the log.
await wait(800); EL.run("emulator -list-avds"); await wait(700); EL.run("emulator -avd P5_API_30"); await wait(1000); EL.run("adb devices"); await wait(900);
EL.run("adb install PocketQuest_1.3.apk"); await wait(900); EL.open(); await wait(1500); EL.rotate(); await wait(1200); EL.run("adb logcat"); await wait(800); EL.shot(); await wait(1500);
