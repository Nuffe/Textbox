// Quick sanity tests for the ported data structures
const fs = require('fs');



const assert = require('assert');

// GapBuffer: basic insert
let b = new GapBuffer(10);
b.insert(0, "hello");
assert.strictEqual(b.textContent(), "hello");

// insert in the middle (forces gap move left)
b.insert(2, "XY");
assert.strictEqual(b.textContent(), "heXYllo");

// insert at end (gap move right)
b.insert(7, "!");
assert.strictEqual(b.textContent(), "heXYllo!");

// delete from middle
b.delete(4);                       // deletes 'Y'
assert.strictEqual(b.textContent(), "heXllo!");

// delete at 0 returns null, doesn't corrupt
assert.strictEqual(b.delete(0), null);
assert.strictEqual(b.textContent(), "heXllo!");

// the underscore bug is fixed
let u = new GapBuffer(5);
u.insert(0, "under__");
assert.strictEqual(u.textContent(), "under__");

// growth past initial size
let g = new GapBuffer(3);
g.insert(0, "abcdefghijklmnopqrstuvwxyz");
assert.strictEqual(g.textContent(), "abcdefghijklmnopqrstuvwxyz");
assert.strictEqual(g.length(), 26);

// heavy back-and-forth cursor movement
let m = new GapBuffer(10);
m.insert(0, "0123456789");
m.insert(5, "A"); m.insert(2, "B"); m.insert(10, "C");
assert.strictEqual(m.textContent(), "01B234A567C89");

// LineList
let list = new LineList();
let n1 = list.append("one"), n2 = list.append("two");
let mid = list.insertAfter(n1, "between");
assert.deepStrictEqual([...list].map(n => n.data), ["one", "between", "two"]);
assert.strictEqual(list.indexOf(mid), 1);
assert.strictEqual(list.tail, n2);

list.remove(mid);
assert.deepStrictEqual([...list].map(n => n.data), ["one", "two"]);
assert.strictEqual(list.contains(mid), false);

// insertOldNodeAfter (undo relink path)
list.insertOldNodeAfter(n1, mid);
assert.deepStrictEqual([...list].map(n => n.data), ["one", "between", "two"]);

// remove head and tail edge cases
list.remove(list.head);
list.remove(list.tail);
assert.strictEqual(list.size, 1);
assert.strictEqual(list.head, list.tail);

// insertAfter(null) on empty list
let e = new LineList();
let h = e.insertAfter(null, "solo");
assert.strictEqual(e.head, h); assert.strictEqual(e.tail, h);

console.log("All tests passed ✓");
