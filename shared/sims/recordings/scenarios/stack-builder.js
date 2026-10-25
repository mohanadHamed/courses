// Stack Builder: Android, one wrong layer first, then the right order.
await wait(900); SB.pick("Java/Kotlin API framework"); await wait(1600);
for (const n of ["Linux kernel", "Hardware abstraction layer (HAL)", "Native libraries and Android Runtime (ART)", "Java/Kotlin API framework", "Apps"]) { SB.pick(n); await wait(750); }
await wait(1500);
