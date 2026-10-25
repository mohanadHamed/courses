// Package Checker: mark the rows, check, then fix the failing rows.
await wait(800); PK.mark(0, true); await wait(300); PK.mark(1, false); await wait(300); PK.mark(2, false); await wait(300); PK.mark(3, true); await wait(300); PK.mark(4, true); await wait(300); PK.mark(5, false); await wait(500); PK.check(); await wait(1500);
PK.mark(3, false); await wait(400); PK.check(); await wait(1200); PK.fixAll(); await wait(1800);
