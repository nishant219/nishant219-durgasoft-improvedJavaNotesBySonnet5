# Video 156 — Concurrent Collections Part-3: ConcurrentMap Methods

## Video info

ASR decode (this lecture): ENT your room = interview room; concurrent Dash map = ConcurrentMap; Ash map = HashMap; put if option / put if abent = putIfAbsent; Legend = listen; sop = System.out.println; not1 / one one = key 101; dur / Dura / DGA = value "Durga"; sha / Shiva = value "Shiva"; car open and close / C open and close = {} (empty map); kga = Durga.

## Session overview

This is Part-3 of the Concurrent Collections series.

Agenda for this video:

- Introduce ConcurrentMap interface — child of Map, parent of ConcurrentHashMap
- Explain that all normal Map methods are inherited and usable
- Deep-dive into 3 special methods defined only in ConcurrentMap:
- putIfAbsent
- remove(key, value) (conditional remove)
- replace(key, oldValue, newValue) (conditional replace)
- Preview: after these methods, next session covers ConcurrentHashMap ("most valuable thing for the interview room")
Exam importance (Durga Sir): ConcurrentMap interface and these three methods are most valuable for the interview room. Do not feel burdened — the interface itself is small; mastery of these three method behaviors is the key.

## 00:29 — Context: Why ConcurrentMap before ConcurrentHashMap?

The first concurrent collection to study in depth is ConcurrentHashMap — but before jumping to the implementation class, we must understand the ConcurrentMap interface first.

Reason: ConcurrentHashMap implements ConcurrentMap. The interface defines the contract; the class provides the thread-safe, high-performance implementation. OCJP/SCJP questions often test method behavior at the interface level (especially the three special methods), not internal segment locking.

## 00:56 — Package and type hierarchy

### Package

All concurrent collections live in:

java.util.concurrent

(Not in `java.util` alone — that package has traditional collections; concurrent variants are in the sub-package `concurrent`.)

### Interface hierarchy (board diagram)

Map                          (java.util)
 └── ConcurrentMap           (java.util.concurrent)
      └── ConcurrentHashMap  (implementation class)

Key rule: Whatever methods exist in Map, they are by default available to ConcurrentMap and can be applied happily. But ConcurrentMap additionally defines 3 special methods whose behavior differs from (or extends) the ordinary Map versions.

## 02:04 — The three special methods (summary)

Normal Map has put, remove(key), and no conditional replace with old-value check. These ConcurrentMap methods exist for atomic, thread-safe conditional updates — critical in multi-threaded code where check-then-act must be one operation.

## 03:01 — Method 1: `putIfAbsent`

### Signature (board)

V putIfAbsent(K key, V value)

Return type: `V` (the value type parameter of the map).

Parameters: key, value — one key-value pair to add.

### Purpose vs normal `put`

Both put and putIfAbsent are used to add one key-value entry to the map. The difference is what happens when the key already exists.

Map rule reminder: Duplicate keys are not allowed. If you put with an existing key, the old value is replaced with the new value. That is standard put behavior (already covered in HashMap lectures).

putIfAbsent rule: If the key is not already available, then only add. If the key is already there, don't do anything.

### Demo 1 — Normal `put` overwrites

```java
import java.util.concurrent.*;

public class PutVsPutIfAbsentDemo {
    public static void main(String[] args) {
        ConcurrentMap<Integer, String> m = new ConcurrentHashMap<>();

        m.put(101, "Durga");
        m.put(101, "Shiva");   // key 101 already exists → old value replaced

        System.out.println(m);  // {101=Shiva}
    }
}
```

Walkthrough:

- m.put(101, "Durga") → map = {101=Durga}
- m.put(101, "Shiva") → key 101 already present → Durga replaced with Shiva
- Output: `{101=Shiva}`
### Demo 2 — `putIfAbsent` does not overwrite

```java
import java.util.concurrent.*;

public class PutIfAbsentDemo {
    public static void main(String[] args) {
        ConcurrentMap<Integer, String> m = new ConcurrentHashMap<>();

        m.put(101, "Durga");
        m.putIfAbsent(101, "Shiva");   // key already present → do nothing

        System.out.println(m);  // {101=Durga}
    }
}
```

Walkthrough:

- m.put(101, "Durga") → map = {101=Durga}
- m.putIfAbsent(101, "Shiva") → key 101 already available → don't do anything
- Nothing new added; existing entry kept
- Output: `{101=Durga}` (NOT Shiva)
### Side-by-side comparison (same starting state)

```java
// After: put(101,"Durga") then put(101,"Shiva")     → {101=Shiva}
// After: put(101,"Durga") then putIfAbsent(101,"Shiva") → {101=Durga}
```

### Return value (API detail — beyond lecture, useful for exams)

putIfAbsent returns:

- null if there was no previous mapping for the key (entry was inserted), or if the previous value was null and null is a valid value
- The previous value associated with the key if the key was already present (and putIfAbsent did nothing)
### When to use `putIfAbsent`

- Initialize a map entry only once (e.g. lazy creation of a per-key object)
- Avoid overwriting a value another thread may have set
- Atomic alternative to: if (!map.containsKey(k)) map.put(k, v); (which is not thread-safe on ordinary HashMap)
### Board note (copy exactly)

putIfAbsent: If the key is not already available, then only add. If the key is already available, don't do anything.

## 07:18 — Method 2: `remove(key, value)` (conditional remove)

### Signature (board — "Legend sir")

boolean remove(Object key, Object value)

Return type: `boolean` — true if an entry was removed, false otherwise.

Parameters: key, value — both must match for removal.

### Purpose vs normal `remove(key)`

Conditional remove rule: The key should be present, and under that key the value should be the specified value only — then only remove. If the key is not associated with the specified value, don't remove.

### Demo 3 — Normal `remove(key)` removes unconditionally

```java
import java.util.concurrent.*;

public class NormalRemoveDemo {
    public static void main(String[] args) {
        ConcurrentMap<Integer, String> m = new ConcurrentHashMap<>();

        m.put(101, "Durga");
        m.remove(101);   // removes entry for key 101 — value doesn't matter

        System.out.println(m);  // {}
    }
}
```

Output: `{}` (empty map — Durga Sir: "curly open and close")

Entry associated with key 101 is already removed. Normal remove needs only the key.

### Demo 4 — `remove(key, value)` when value does NOT match → no removal

```java
import java.util.concurrent.*;

public class ConditionalRemoveNoMatchDemo {
    public static void main(String[] args) {
        ConcurrentMap<Integer, String> m = new ConcurrentHashMap<>();

        m.put(101, "Durga");
        m.remove(101, "Shiva");   // key 101 exists but value is Durga, not Shiva

        System.out.println(m);  // {101=Durga}
    }
}
```

Walkthrough:

- Key 101 is present, associated with Durga, not Shiva
- remove(101, "Shiva") → key present but not associated with Shiva → won't remove
- Output: `{101=Durga}`
### Demo 5 — `remove(key, value)` when value matches → removal happens

```java
import java.util.concurrent.*;

public class ConditionalRemoveMatchDemo {
    public static void main(String[] args) {
        ConcurrentMap<Integer, String> m = new ConcurrentHashMap<>();

        m.put(101, "Durga");
        m.remove(101, "Durga");   // key AND value both match

        System.out.println(m);  // {}
    }
}
```

Walkthrough:

- Key 101 present, value = Durga
- remove(101, "Durga") → key matched, value matched → entry removed
- Output: `{}`
### Summary table — remove methods

### Board note

remove(key, value): Key should be there, and that key should be associated with this value only — then only remove. Key and value both must match.

## 11:01 — Method 3: `replace(key, oldValue, newValue)`

### Signature (board)

boolean replace(K key, V oldValue, V newValue)

Return type: `boolean` — true if replacement succeeded, false otherwise.

Parameters:

- key — must exist in the map
- oldValue — current value must equal this
- newValue — value to set if oldValue matches
### Purpose

Replace the value for a key only if the key is present and the current value equals oldValue. If both match, replace old value with new value.

This is an atomic compare-and-swap style update: "if the map still has what I expect, change it to this."

### Demo 6 — `replace` when oldValue does NOT match → no replacement

```java
import java.util.concurrent.*;

public class ReplaceNoMatchDemo {
    public static void main(String[] args) {
        ConcurrentMap<Integer, String> m = new ConcurrentHashMap<>();

        m.put(101, "Durga");
        m.replace(101, "Shiva", "Ravi");   // oldValue Shiva ≠ actual Durga

        System.out.println(m);  // {101=Durga}
    }
}
```

Walkthrough:

- Key 101 exists, associated with Durga
- replace(101, "Shiva", "Ravi") — you specify oldValue as Shiva, but map has Durga
- Key matched, value did not match → replacement won't happen
- Output: `{101=Durga}`
### Demo 7 — `replace` when oldValue matches → replacement happens

```java
import java.util.concurrent.*;

public class ReplaceMatchDemo {
    public static void main(String[] args) {
        ConcurrentMap<Integer, String> m = new ConcurrentHashMap<>();

        m.put(101, "Durga");
        m.replace(101, "Durga", "Shiva");   // key matched, oldValue matched

        System.out.println(m);  // {101=Shiva}
    }
}
```

Walkthrough:

- Key 101 present, value = Durga
- replace(101, "Durga", "Shiva") → key matched, value matched
- Old value Durga replaced with new value Shiva
- Output: `{101=Shiva}`
### Board note

replace(key, oldValue, newValue): Key and value both should be matched in the map. If both matched, then only replace old value with new value.

## Complete combined demo (all three methods)

```java
import java.util.concurrent.*;

public class ConcurrentMapThreeMethodsDemo {
    public static void main(String[] args) {
        ConcurrentMap<Integer, String> m = new ConcurrentHashMap<>();

        // --- putIfAbsent ---
        m.put(101, "Durga");
        m.putIfAbsent(101, "Shiva");       // no-op: key exists
        System.out.println("After putIfAbsent: " + m);  // {101=Durga}

        m.putIfAbsent(102, "Ravi");        // adds: key absent
        System.out.println("After putIfAbsent 102: " + m);  // {101=Durga, 102=Ravi}

        // --- conditional remove ---
        m.remove(101, "Shiva");            // no-op: value mismatch
        System.out.println("After remove(101,Shiva): " + m);  // {101=Durga, 102=Ravi}

        m.remove(101, "Durga");            // removes: both match
        System.out.println("After remove(101,Durga): " + m);  // {102=Ravi}

        // --- conditional replace ---
        m.replace(102, "Shiva", "Kohli");  // no-op: oldValue Shiva ≠ Ravi
        System.out.println("After replace fail: " + m);       // {102=Ravi}

        m.replace(102, "Ravi", "Kohli");   // success
        System.out.println("After replace ok: " + m);         // {102=Kohli}
    }
}
```

## Master comparison: Map vs ConcurrentMap special methods

Important: Normal Map does have put, remove(key), etc., but does not define these three methods with this conditional behavior. They were added in `ConcurrentMap` (Java 5) for thread-safe atomic conditional operations. Java 8 later added some similar methods to the base Map interface as default methods — but for OCJP in this course, focus on ConcurrentMap semantics as taught.

## Why these methods matter (concurrency angle)

In a multi-threaded program, this pattern is unsafe on a plain HashMap:

```java
// NOT thread-safe — two threads can both pass the check
if (!map.containsKey(key)) {
    map.put(key, value);
}
```

putIfAbsent performs the check-and-insert as one atomic operation on ConcurrentHashMap (and other ConcurrentMap implementations).

Similarly:

```java
// NOT atomic on HashMap
if ("Durga".equals(map.get(101))) {
    map.put(101, "Shiva");
}
```

→ Use replace(101, "Durga", "Shiva") instead.

And:

```java
// NOT atomic
if ("Durga".equals(map.get(101))) {
    map.remove(101);
}
```

→ Use remove(101, "Durga") instead.

Durga Sir's emphasis in this video is behavior and output prediction for exam questions, not segment-level locking (that comes with ConcurrentHashMap in Video 157).

## Exam-style output prediction drills

```java
Assume: ConcurrentMap<Integer,String> m = new ConcurrentHashMap<>();
```

## Quick revision checklist

- [ ] ConcurrentMap extends Map; lives in java.util.concurrent
- [ ] ConcurrentHashMap is the main implementation class (next video)
- [ ] All inherited Map methods work on ConcurrentMap
- [ ] 3 special methods: putIfAbsent, remove(key,value), replace(key,old,new)
- [ ] putIfAbsent: add only if key absent; existing key → no change
- [ ] remove(key,value): remove only if key and value match
- [ ] replace(key,old,new): replace only if key and oldValue match
- [ ] Normal put overwrites; normal remove(key) ignores value
- [ ] Empty map prints as {}
## 13:44 — Session closing summary (Durga Sir)

ConcurrentMap interface — do not feel burdened; these are most valuable for the interview room.

Defines 3 methods:

- putIfAbsent
- remove (two-argument conditional form)
- replace (three-argument conditional form)
These are new methods — they won't behave the same as the familiar put / remove(key) on a normal map. The behavior is a bit different — that difference is exactly what OCJP tests.

Next video (157): ConcurrentHashMap details — internal structure, concurrency level, and the "most valuable" implementation class.

## Related imports for lab / exam code

```java
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.ConcurrentHashMap;
```

Use ConcurrentHashMap as the concrete type when you need a live map for demos or tests; declare as ConcurrentMap when programming to the interface.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Playlist position | 156 of 203 |  |  |
| Title | Core Java With OCJP/SCJP: Concurrent Collections Part-3 \ | \ | ConcurrentMap Methods |
| YouTube URL | https://www.youtube.com/watch?v=5Ypy0iQ27gs |  |  |
| Duration | 14m 44s |  |  |
| Source captions | YouTube auto-generated (yt-dlp + node PO token) |  |  |

| Part | Video | Topic covered |
|---|---|---|
| Part-1 (154) | Need of Concurrent Collections | Three problems with traditional collections: not thread-safe, poor performance of legacy thread-safe classes, ConcurrentModificationException |
| Part-2 (155) | Diff B/W Traditional & Concurrent Collections | Side-by-side comparison of how concurrent collections solve those three problems |
| Part-3 (156) | ConcurrentMap Methods | ConcurrentMap interface and its 3 special atomic methods |
| Part-4 (157) | ConcurrentHashMap Details | Full ConcurrentHashMap implementation (next video) |

| Type | Role |
|---|---|
| Map | Root map interface — put, get, remove(key), containsKey, etc. |
| ConcurrentMap | Child interface of Map — inherits all Map methods plus 3 special atomic methods |
| ConcurrentHashMap | Implementation class of ConcurrentMap (covered in Video 157) |

| # | Method | One-line purpose |
|---|---|---|
| 1 | putIfAbsent(key, value) | Add entry only if key is not already present; if key exists, do nothing |
| 2 | remove(key, value) | Remove entry only if key exists AND is mapped to the specified value |
| 3 | replace(key, oldValue, newValue) | Replace value only if key exists AND current value equals oldValue |

| Scenario | put(key, value) | putIfAbsent(key, value) |
|---|---|---|
| Key not present | Adds the entry | Adds the entry |
| Key already present | Old value replaced with new value | Does nothing — existing entry unchanged |

| Method | Behavior |
|---|---|
| remove(key) | Removes the entire entry associated with that key, regardless of value |
| remove(key, value) | Removes only if key is present and that key is associated with this exact value |

| Call | Map before | Map after | Removed? |
|---|---|---|---|
| remove(101) | {101=Durga} | {} | Yes — key enough |
| remove(101, "Shiva") | {101=Durga} | {101=Durga} | No — value mismatch |
| remove(101, "Durga") | {101=Durga} | {} | Yes — key and value match |

| Operation | Normal Map | ConcurrentMap special method |
|---|---|---|
| Add / update entry | put(k,v) — always sets (overwrites if key exists) | putIfAbsent(k,v) — sets only if key absent |
| Remove by key | remove(k) — removes entry for key | remove(k,v) — removes only if mapping is exactly (k,v) |
| Replace value | No standard conditional replace in pre-Java 8 Map | replace(k, old, new) — replaces only if current value equals old |

| Code sequence | Output of System.out.println(m) |
|---|---|
| put(101,"A"); put(101,"B"); | {101=B} |
| put(101,"A"); putIfAbsent(101,"B"); | {101=A} |
| put(101,"A"); remove(101); | {} |
| put(101,"A"); remove(101,"B"); | {101=A} |
| put(101,"A"); remove(101,"A"); | {} |
| put(101,"A"); replace(101,"B","C"); | {101=A} |
| put(101,"A"); replace(101,"A","C"); | {101=C} |
