// Site Planner: part 1 on Contact (wrong), then Home; part 2 on Service.
const p = (x) => click(`#btns [data-p="${x}"]`);
await wait(900); p("Contact"); await wait(1400); p("Home"); await wait(1400); p("Service"); await wait(2200);
