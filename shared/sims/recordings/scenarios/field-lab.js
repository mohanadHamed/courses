// Field Lab: Name as Number (wrong), then Short Text; Price as Currency.
const t = (x) => click(`#types [data-t="${x}"]`);
await wait(800); t("Number"); await wait(1400); t("Short Text"); await wait(2000); t("Currency"); await wait(2200);
