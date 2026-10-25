// Chart Lab: a column chart with a title, a wrong line chart of the types, then the line of the days and a pie.
await wait(1000); CL.set({ title: "Sales per type, one week" }); await wait(1800);
CL.set({ type: "line" }); await wait(1800); CL.set({ data: "day", title: "Sales per day" }); await wait(1800);
CL.set({ data: "type", type: "pie", title: "Part of each type" }); await wait(2200);
