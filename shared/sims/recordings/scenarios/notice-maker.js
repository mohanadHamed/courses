// Notice Maker: title and headings, the list, the table, the picture's wrapping and alt text.
const tool = (t) => click(`[data-t="${t}"]`);
const blk = (i) => document.querySelectorAll("#page .blk")[i].click();
await wait(600); tool("title"); await wait(600); tool("h1"); await wait(600); tool("h1"); await wait(600);
tool("bul"); await wait(700);
blk(2); await wait(400); tool("num"); await wait(900); tool("table"); await wait(700);
blk(5); await wait(400); tool("square"); await wait(800); tool("alt"); await wait(400);
document.getElementById("altText").value = "a green park with trees"; click("#altOk"); await wait(2200);
