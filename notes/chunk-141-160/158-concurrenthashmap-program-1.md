# Video 158 — Concurrent Collections Part-5: ConcurrentHashMap Program-1

## Video info

## Session overview

This is a short, hands-on demo lecture — the first program in the ConcurrentHashMap practical series. Sir does not introduce new theory here; he executes a single example end-to-end to show how the three special methods of `ConcurrentMap` behave when used through a `ConcurrentHashMap` instance.

Prerequisites (covered in earlier videos in this module):

What this video covers (~4½ minutes):

- Recap reminder — ConcurrentMap defines three special methods beyond normal Map
- Package/import — java.util.concurrent
- Create ConcurrentHashMap referenced as ConcurrentMap
- Step-by-step demo: put, putIfAbsent, remove(key, value), replace(key, oldValue, newValue)
- Predict final map contents
- Live compile & run — verify output matches prediction
- Important note — iteration order is not guaranteed (hash-based, not insertion order)
What this video does NOT cover: constructors, concurrency level, locking internals, multi-threaded scenarios — those were in Video 157; more programs likely follow in Video 159+.

## 00:16 — Recap: three special `ConcurrentMap` methods

Sir opens by connecting back to the `ConcurrentMap` interface discussion (Video 156):

In ConcurrentHashMap, we already covered that there are three methods in the `ConcurrentMap` interface. You have remembered `putIfAbsent`, `remove`, and `replace`.

### Hierarchy reminder

Map  (java.util)
 └── ConcurrentMap  (java.util.concurrent)
      └── ConcurrentHashMap  (implementation class)

- `ConcurrentHashMap` implements `ConcurrentMap`.
- `ConcurrentMap` extends `Map`.
- All normal `Map` methods (put, get, remove(key), etc.) work on ConcurrentHashMap.
- `ConcurrentMap` adds three atomic, thread-safe conditional methods that behave differently from their Map counterparts.
### The three methods (quick reference)

These methods exist specifically for multi-threaded, lock-free-style conditional updates — a core OCJP/SCJP exam topic when comparing Map vs ConcurrentMap.

## 00:37 — Package and import

Sir writes:

```java
import java.util.concurrent.*;
```

Why this package?

- `ConcurrentHashMap` lives in `java.util.concurrent`, not java.util.
- The star import pulls in ConcurrentHashMap, ConcurrentMap, and other concurrent utilities.
Board note: All concurrent collections (ConcurrentHashMap, CopyOnWriteArrayList, BlockingQueue implementations, etc.) are in `java.util.concurrent`.

## 00:53 — Creating the map

```java
ConcurrentMap<Integer, String> m = new ConcurrentHashMap<>();
```

Key points Sir emphasizes:

Using the `ConcurrentMap` interface type is valid because ConcurrentHashMap is its implementation class — same pattern as Map m = new HashMap().

## 01:01 — Step 1: `put(1, "A")`

m.put(1, "A");   // key 1 added

Normal `Map.put` behavior — if key absent, add; if key present, replace old value and return old value.

## 01:04 — Step 2: `put(2, "B")`

m.put(2, "B");   // key 2 added

Two entries now. Order in toString() output may vary — Sir repeats this later.

## 01:12 — Step 3: `putIfAbsent(3, "C")`

m.putIfAbsent(3, "C");

### `putIfAbsent` behavior (from Video 156, applied here)

Analysis for this call:

- Key 3 is not in the map yet.
- Therefore entry (3, "C") is added.
### Contrast with `put`

If we had written m.put(3, "C") instead — same result here because key 3 was absent. The difference shows up only when the key already exists (next step).

## 01:33 — Step 4: `putIfAbsent(1, "D")` — key already present

m.putIfAbsent(1, "D");

Analysis:

- Key 1 already exists with value "A".
- putIfAbsent rule: key already available → don't do anything.
- Value "D" is NOT added; "A" remains.
### `put` vs `putIfAbsent` side-by-side (exam favourite)

## 01:47 — Step 5: `remove(1, "D")` — conditional remove fails

m.remove(1, "D");

### Two overloads of `remove` — do not confuse

Analysis for `remove(1, "D")`:

- Key 1 is present ✓
- But associated value is `"A"`, not `"D"` ✗
- Key–value pair (1, "D") does not exist in the map
- Therefore: nothing is removed
Return value: false (removal did not happen).

### When would it succeed?

m.remove(1, "A");   // key 1 present AND value is "A" → entry removed → returns true

After that, map would be {2=B, 3=C}.

## 02:12 — Step 6: `replace(2, "B", "E")` — conditional replace succeeds

m.replace(2, "B", "E");

### `replace` behavior (three-parameter form)

Analysis:

- Is there an entry with key 2 and value "B"? Yes.
- Key matched ✓, value matched ✓
- Replace "B" with "E"
Return value: true.

### Failed replace example (for contrast)

m.replace(2, "B", "E");   // AFTER B was already replaced → value is "E", not "B" → false, no change
m.replace(1, "D", "X");   // key 1 value is "A", not "D" → false, no change

## 02:38 — Step 7: print the map

```java
System.out.println(m);
```

### Expected final contents (entries, not order)

Sir states the three entries that must be present:

Logical contents: {1=A, 2=E, 3=C}

### Order is NOT guaranteed

Sir explicitly warns (critical exam/interview point):

Here it is ConcurrentHashMap, right? Order-wise we can't give the guarantee because it is based on hash code of the keys. But entries — these three will be there.

Sample possible outputs (all valid):

```java
{1=A, 2=E, 3=C}
{3=C, 1=A, 2=E}
{2=E, 3=C, 1=A}
```

All three entries present; only order varies.

## Complete demo program (as Sir writes on board)

```java
import java.util.concurrent.*;

public class Test {
    public static void main(String[] args) {
        ConcurrentMap<Integer, String> m = new ConcurrentHashMap<>();

        m.put(1, "A");                    // add 1→A
        m.put(2, "B");                    // add 2→B

        m.putIfAbsent(3, "C");            // key 3 absent → add 3→C
        m.putIfAbsent(1, "D");            // key 1 present → no change

        m.remove(1, "D");                 // key 1 value is A, not D → no remove

        m.replace(2, "B", "E");             // key 2 value B matched → B replaced with E

        System.out.println(m);
        // Entries: {1=A, 2=E, 3=C} — order not guaranteed
    }
}
```

## 03:16 — Live execution

Sir switches to the IDE/terminal and runs the same program:

javac Test.java
java Test

### Observed output (from live run)

Sir reads the console — entries match prediction:

- 1 → A
- 2 → E (was B, replaced)
- 3 → C
Example console line (order may differ):

```java
{3=C, 2=E, 1=A}
```

Sir confirms:

Same entries — 1=A, 2=E, 3=C. Order-wise we can't give the guarantee, but all three entries are there. Key 2 associated value is E (not B anymore).

Verification checklist:

## Trace table — full program state after each line

## Method deep-dive summary (OCJP exam sheet)

### 1. `putIfAbsent(K key, V value)`

V putIfAbsent(K key, V value);

- Purpose: Atomically add entry only when key is missing — avoids "check-then-act" race in multi-threaded code.
- If key absent: inserts mapping, returns null.
- If key present: map unchanged, returns existing value.
- vs `put`: put always overwrites; putIfAbsent never overwrites.
### 2. `boolean remove(Object key, Object value)`

```java
boolean remove(Object key, Object value);
```

- Purpose: Atomically remove only when both key and value match — safe conditional delete.
- Returns `true`: entry found with exact key–value pair and removed.
- Returns `false`: no such mapping (wrong key, wrong value, or both).
- vs `remove(key)`: single-arg remove deletes by key alone regardless of value.
### 3. `boolean replace(K key, V oldValue, V newValue)`

```java
boolean replace(K key, V oldValue, V newValue);
```

- Purpose: Atomically swap value only when current value matches expected — compare-and-swap style update.
- Returns `true`: replacement happened.
- Returns `false`: key missing or value didn't match.
- Note: ConcurrentMap also has replace(K key, V value) (two-arg) — replaces unconditionally if key exists; the demo uses the three-arg conditional form.
## Why these methods matter for `ConcurrentHashMap`

In a multi-threaded environment, this pattern is unsafe:

```java
// NOT thread-safe "check then act"
if (!map.containsKey(key)) {
    map.put(key, value);
}
```

Between containsKey and put, another thread can insert the same key → lost update or inconsistent state.

`putIfAbsent` performs the check-and-insert as one atomic operation on ConcurrentHashMap — no external synchronization needed.

Same logic applies to conditional `remove` and `replace` — they prevent removing/replacing the wrong state when another thread intervenes.

## Common auto-caption / transcription corrections

YouTube auto-captions garbled several terms in this short video. Correct readings:

## Key takeaways (copy for revision)

- `ConcurrentHashMap` is in `java.util.concurrent`; implement `ConcurrentMap`.
- `ConcurrentMap` adds exactly three special methods: `putIfAbsent`, `remove(key, value)`, `replace(key, oldValue, newValue)`.
- This demo uses all three conditionals in one program — trace each call against current map state.
- `putIfAbsent(1, "D")` when key 1 exists → no change (unlike put).
- `remove(1, "D")` when value is "A" → no removal (both key AND value must match).
- `replace(2, "B", "E")` when entry is 2=B → success → 2=E.
- Final map always has three entries: 1=A, 2=E, 3=C.
- `ConcurrentHashMap` does not preserve insertion order in toString() — hash-based bucket layout.
- Live compile/run confirms theory — entries match; order may shuffle.
- This is Program-1 — more ConcurrentHashMap programs follow in subsequent videos.
## OCJP / SCJP quick quiz (self-check)

Q1. After m.put(1,"A"); m.putIfAbsent(1,"D"); — what is m.get(1)?

A: "A"

Q2. After m.put(2,"B"); m.remove(2, "X"); — is key 2 still in map?

A: Yes — value didn't match "X".

Q3. After m.put(2,"B"); m.replace(2, "B", "E"); — what is m.get(2)?

A: "E"

Q4. Can ConcurrentHashMap guarantee {1=A, 2=E, 3=C} print order every run?

A: No — order depends on hash codes and internal table layout.

Q5. Which interface defines putIfAbsent?

A: ConcurrentMap (since Java 5 / 1.5).

Q6. Does normal HashMap have putIfAbsent?

A: Yes — putIfAbsent was added to `Map` itself in Java 8 as a default method. But the conditional remove/replace variants and their atomic thread-safe semantics on ConcurrentHashMap remain the exam focus in this Durga Sir module. (Sir teaches the Java 5 ConcurrentMap story where these three were special to concurrent maps.)

## Connection to next videos

Sir closes with:

This is the first example to demonstrate how we can use `ConcurrentMap` interface methods for `ConcurrentHashMap`. That's all — this is the first example.

Expect Program-2 and beyond (Video 159+) to cover additional scenarios — likely iterators, concurrent reads/writes, or more complex multi-threaded demos building on Video 157 theory.

## One-page revision diagram

ConcurrentHashMap Demo Program-1 (Video 158)
============================================
import java.util.concurrent.*;

ConcurrentMap m = new ConcurrentHashMap();

  put(1,"A")           →  {1=A}
  put(2,"B")           →  {1=A, 2=B}
  putIfAbsent(3,"C")   →  {1=A, 2=B, 3=C}     ← key 3 was free
  putIfAbsent(1,"D")   →  {1=A, 2=B, 3=C}     ← key 1 taken → skip
  remove(1,"D")        →  {1=A, 2=B, 3=C}     ← value A≠D → skip
  replace(2,"B","E")   →  {1=A, 2=E, 3=C}     ← match → replace

println → three entries, order NOT guaranteed

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Playlist position | 158 of 203 |  |  |
| Title | Core Java With OCJP/SCJP: Concurrent Collections Part-5 \ | \ | ConcurrentHashMap Program-1 |
| YouTube URL | https://www.youtube.com/watch?v=y52gqOfral0 |  |  |
| Video ID | y52gqOfral0 |  |  |
| Duration | 4m 34s |  |  |
| Captions | English (YouTube auto-generated via yt-dlp) |  |  |
| Output file | 158-concurrenthashmap-program-1 |  |  |

| Video | Topic |
|---|---|
| 156 | ConcurrentMap interface — putIfAbsent, conditional remove, conditional replace |
| 157 | ConcurrentHashMap internals — thread safety, segment/bucket locking, concurrency level, constructors |

| # | Method signature | One-line behavior |
|---|---|---|
| 1 | V putIfAbsent(K key, V value) | Add entry only if key is absent; if key exists, do nothing |
| 2 | boolean remove(Object key, Object value) | Remove entry only if key exists AND value matches |
| 3 | boolean replace(K key, V oldValue, V newValue) | Replace value only if key exists AND current value equals oldValue |

| Point | Detail |
|---|---|
| Reference type | ConcurrentMap (interface) — polymorphic reference |
| Object type | ConcurrentHashMap (concrete implementation) |
| Empty map | Default constructor → empty ConcurrentHashMap with default initial capacity 16, load factor 0.75, concurrency level 16 (from Video 157) |
| Generics | Demo uses integer keys and string values (autocaptions garble types; code uses Integer/String) |

| After this call | Map state |
|---|---|
| Entries | {1=A} |
| Return value | null (key was not previously present) |

| After this call | Map state |
|---|---|
| Entries | {1=A, 2=B} |

| Condition | Action |
|---|---|
| Key not already in map | Add (key, value) → returns null |
| Key already in map | Do nothing → returns existing value |

| After this call | Map state |
|---|---|
| Entries | {1=A, 2=B, 3=C} |

| After this call | Map state |
|---|---|
| Entries | {1=A, 2=B, 3=C} — unchanged from previous step |

| Scenario | put(1, "D") | putIfAbsent(1, "D") |
|---|---|---|
| Key 1 absent | Adds 1=D, returns null | Adds 1=D, returns null |
| Key 1 present with "A" | Replaces → 1=D, returns "A" | No change → stays 1=A, returns "A" |

| Method | Behavior |
|---|---|
| remove(Object key) | Remove entry for key regardless of value (normal Map remove) |
| remove(Object key, Object value) | Remove only if key exists AND associated value equals specified value (ConcurrentMap special method) |

| After this call | Map state |
|---|---|
| Entries | {1=A, 2=B, 3=C} — still unchanged |

| Condition | Action | Return |
|---|---|---|
| Key present AND current value == oldValue | Replace with newValue | true |
| Key absent OR value mismatch | No change | false |

| After this call | Map state |
|---|---|
| Entries | {1=A, 2=E, 3=C} |

| Key | Value | How it got there |
|---|---|---|
| 1 | "A" | put(1, "A"); putIfAbsent(1,"D") skipped; remove(1,"D") failed |
| 2 | "E" | put(2, "B") then replace(2, "B", "E") |
| 3 | "C" | putIfAbsent(3, "C") |

| Map type | Insertion order guaranteed? |
|---|---|
| LinkedHashMap | Yes (insertion-order or access-order) |
| TreeMap | Yes (sorted by key) |
| HashMap | No |
| ConcurrentHashMap | No (hash-table based, like HashMap) |
| Hashtable | No |

| Check | Result |
|---|---|
| Entry count = 3 | ✓ |
| Key 1 = "A" (not "D") | ✓ — putIfAbsent and conditional remove worked as expected |
| Key 2 = "E" (not "B") | ✓ — replace succeeded |
| Key 3 = "C" | ✓ — putIfAbsent added new key |
| Order matches insertion order | ✗ — not expected for ConcurrentHashMap |

| Step | Code | Map contents {key=value} | Notes |
|---|---|---|---|
| 0 | (new map) | {} | empty |
| 1 | put(1, "A") | {1=A} | normal put |
| 2 | put(2, "B") | {1=A, 2=B} | normal put |
| 3 | putIfAbsent(3, "C") | {1=A, 2=B, 3=C} | key 3 was absent |
| 4 | putIfAbsent(1, "D") | {1=A, 2=B, 3=C} | key 1 exists → skip |
| 5 | remove(1, "D") | {1=A, 2=B, 3=C} | value mismatch → skip |
| 6 | replace(2, "B", "E") | {1=A, 2=E, 3=C} | match → replace |
| 7 | println(m) | print {1=A, 2=E, 3=C} | order varies |

| Caption heard | Intended |
|---|---|
| "puts in remove" | putIfAbsent, remove, replace |
| "put if option" | putIfAbsent |
| "java util concurrent start" | java.util.concurrent.* |
| "1 or 2 B" | key 2, value "B" |
| "1 or three" | key 3 |
| "one or two B" | key 2, value "B" |
| "yda put if option of 1.1 comma d" | putIfAbsent(1, "D") |
| "ash concurrent map" | ConcurrentMap |
| "concurrent Ash map" | ConcurrentHashMap |
