// The Products table of the Sunrise shop database (Lecture 7 and Online activity 8).
window.SHOP = {
  fields: ["ProductID", "Name", "Type", "Price", "InStock"],
  types: { ProductID: "AutoNumber", Name: "Short Text", Type: "Short Text", Price: "Currency", InStock: "Yes/No" },
  rows: [
    [1, "Notebook", "Paper", 2, "Yes"], [2, "Pen", "Paper", 0.5, "Yes"], [3, "Bag", "Bags", 12, "Yes"],
    [4, "Water", "Drinks", 0.5, "No"], [5, "Juice", "Drinks", 1, "Yes"], [6, "Folder", "Paper", 1.5, "No"],
    [7, "Lunch box", "Bags", 6, "Yes"], [8, "Coffee", "Drinks", 1, "Yes"],
  ],
};
window.dbTable = (fields, rows) => `<table class="db"><tr>${fields.map((f) => `<th>${f}</th>`).join("")}</tr>${rows.map((r) => `<tr>${r.map((v) => `<td>${typeof v === "number" && v % 1 ? v.toFixed(2) : v}</td>`).join("")}</tr>`).join("")}</table>`;
