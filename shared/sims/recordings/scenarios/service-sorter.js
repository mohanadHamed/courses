// Service Sorter: service 1 as a booking (wrong), then an online store.
const k = (x) => click(`#kinds [data-k="${x}"]`);
await wait(900); k("booking"); await wait(1500); k("online store"); await wait(2400);
