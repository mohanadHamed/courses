// Package Review: score the five criteria, compare, then correct the consistency score.
await wait(800); PR.score(0, 4); await wait(400); PR.score(1, 4); await wait(400); PR.score(2, 3); await wait(400); PR.score(3, 4); await wait(400); PR.score(4, 4); await wait(600); PR.compare(); await wait(1700); PR.score(1, 2); await wait(1800);
