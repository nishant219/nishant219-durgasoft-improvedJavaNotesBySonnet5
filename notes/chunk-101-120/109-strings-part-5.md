# Video 109

## Video info

ASR note: Captions say SAP, SCP, ACP, SEP interchangeably — all mean String Constant Pool (SCP). SCJP / ICJP / OCJP refer to the same certification track.

## 00:08 — Why String is the most important `java.lang` topic

Durga Sir opens with a strong exam and career warning: String is the highest-value concept in Core Java for OCJP/SCJP, interviews, and daily coding.

### Kathy Sierra (K&B) book reference

- Best book for SCJP: Sun Certified Programmer for Java 6 by Kathy Sierra & Bert Bates (Head First Java / SCJP series).
- Kathy Sierra worked at Sun Microsystems for 6+ years and was on the panel that prepared SCJP exam questions.
- In the String introduction she writes (paraphrased): "If you are not familiar with String concepts, don't go for the SCJP exam — by default you will fail."
- Durga Sir initially disagreed (String seemed like a small topic), but after his own SCJP exam he underlined that line: 24–25 out of 60 questions came from String — directly or indirectly.
### Three conclusions before you proceed

- Not familiar with String → don't attend interviews — the difference between String and StringBuffer, and immutability with examples, is an ATM-standard question. Even one second of hesitation can disqualify you.
- Not familiar with String → don't sit OCJP/SCJP — same reason; exam weight is enormous.
- Not familiar with String → you cannot code confidently — String is the most commonly used object in any Java program (small or large).
### Why `main` takes `String[] args`

```java
public static void main(String[] args) { }
```

- The argument to main is String[] because ~90% of real programs need String handling.
- String was given priority over int, double, arrays, etc. — it is the universal entry-point type for command-line input.
Exam punch line: Every point in this video is as powerful as a boxing punch — listen to each one carefully. Some String vs StringBuffer ideas were touched in Object class lectures; this video summarizes and deepens them.

## 07:41 — Case 1: Immutability vs Mutability (`String` vs `StringBuffer`)

### Side-by-side code (board Example 1)

```java
// --- String (immutable) ---
String s = new String("Durga");
s.concat("Software");          // return value IGNORED
System.out.println(s);         // Durga

// --- StringBuffer (mutable) ---
StringBuffer sb = new StringBuffer("Durga");
sb.append("Software");
System.out.println(sb);        // DurgaSoftware
```

### Output

### Theory — Immutability (String)

- Once a String object is created, you cannot change the existing object.
- If you try to modify it (concat, +, etc.), a new object is created with the changed content.
- The original object remains unchanged.
- If the new object is not assigned to any reference variable, it becomes eligible for garbage collection.
String s = new String("Durga");
// s → [Durga]  (heap object)

s.concat("Software");
// Creates NEW object [DurgaSoftware] on heap — no reference → eligible for GC
// s STILL points to [Durga]

System.out.println(s);  // Durga

Immutable = non-changeable.

### Theory — Mutability (StringBuffer)

- Once a StringBuffer object is created, you can change the same object in place.
- Methods like append() modify the existing object — no new object required for the reference to see the change.
StringBuffer sb = new StringBuffer("Durga");
// sb → [Durga]  (mutable buffer)

sb.append("Software");
// SAME object now holds "DurgaSoftware"

System.out.println(sb);  // DurgaSoftware

Mutable = changeable.

### With assignment (String also "changes" the reference)

String s = new String("Durga");
s = s.concat("Software");      // s now points to NEW object
System.out.println(s);         // DurgaSoftware
// Old "Durga" heap object (from new String) may be eligible for GC if unreferenced

Interview answer template:

String objects are immutable; StringBuffer objects are mutable.

Immutable means once created, the content of the existing object cannot change — any modification creates a new object.

Mutable means the existing object can be modified in place.

## 20:28 — Case 2: `equals()` — String vs StringBuffer

### Side-by-side code (board KS-2)

```java
// --- String ---
String s1 = new String("Durga");
String s2 = new String("Durga");
System.out.println(s1 == s2);         // false
System.out.println(s1.equals(s2));    // true

// --- StringBuffer ---
StringBuffer sb1 = new StringBuffer("Durga");
StringBuffer sb2 = new StringBuffer("Durga");
System.out.println(sb1 == sb2);       // false
System.out.println(sb1.equals(sb2));  // false
```

### Output

### Memory picture

- new operator → two separate objects in both cases.
- s1 and s2 both point to different heap String objects, but content is "Durga".
- sb1 and sb2 both point to different StringBuffer objects with content "Durga".
### Why `equals()` differs — critical exam point

```java
// String.equals() — content
String a = new String("Java");
String b = new String("Java");
a.equals(b);   // true  (content "Java" == "Java")

// StringBuffer.equals() — reference (Object class behavior)
StringBuffer x = new StringBuffer("Java");
StringBuffer y = new StringBuffer("Java");
x.equals(y);   // false (different objects)
```

### `==` operator (both classes)

- Always reference comparison.
- true only when both references point to the same object.
### Second difference between String and StringBuffer (beyond immutability)

Highlight this in exam notes — interviewers often ask for differences beyond immutability.

## 31:11 — Case 3: `new String("Durga")` vs `String s = "Durga"`

### The two lines look similar — they are NOT the same

String s = new String("Durga");   // Line A
String s = "Durga";               // Line B

Many beginners assume Line B is a shortcut for Line A. Functionally and memory-wise they differ.

### Line A — `new String("Durga")` → **2 objects**

- new always creates a fresh object on the heap.
- The literal "Durga" is also placed in SCP for future literal assignments (explained below).
### Line B — `String s = "Durga"` → **1 object**

- No new → no separate heap object.
- s points directly to the SCP object.
### Diagram summary (board KS-3)

Line A:  new String("Durga")
         Heap:  [Durga]  ←── s
         SCP:   [Durga]  (no ref — future reuse)

Line B:  "Durga"
         SCP:   [Durga]  ←── s

## 38:18 — SCP rules: optional creation and reuse

### Rule 1 — Object creation in SCP is **optional**

Before creating a literal object in SCP, JVM checks:

- Is an object with the required content already present in SCP?
- If yes → reuse the existing object (no duplicate created).
- If no → create one new object in SCP.
String s3 = "Durga";   // SCP empty → create "Durga" in SCP
String s4 = "Durga";   // SCP has "Durga" → reuse same object
// s3 == s4  →  true  (same SCP object)

This reuse rule applies ONLY to SCP — NOT to the heap.

String s1 = new String("Durga");  // always new heap object
String s2 = new String("Durga");  // another new heap object
// s1 == s2  →  false

### Rule 2 — Why SCP object without reference is NOT garbage-collected

- The SCP "Durga" from new String("Durga") has no reference variable.
- Normally → eligible for GC.
- But GC does not collect SCP objects — they are saved for future literal reuse.
How is this possible?

Java memory areas (5):

- SCP is part of the method area, not the heap.
- Garbage Collector operates only on the heap — it cannot access SCP/method area.
- Therefore: even with zero references, SCP objects are not eligible for GC.
### Rule 3 — When are SCP objects destroyed?

- All SCP objects are destroyed automatically at JVM shutdown.
- For web applications → effectively at server shutdown.
- Production practice: scheduled server restarts (e.g., every second Sunday at 4 AM) so SCP does not grow unbounded forever in long-running servers.
- Cluster setups: stop/start instances one at a time so service continues.
## 48:17 — Example 2: Counting objects (S1–S4)

### Code

```java
String s1 = new String("Durga");
String s2 = new String("Durga");
String s3 = "Durga";
String s4 = "Durga";
```

### Step-by-step object creation

### Answer

### Key conclusions (board notes)

- `new` operator → compulsory new object on heap every time.
- Duplicate content on heap → possible (two heap "Durga" objects from two new calls).
- Duplicate content in SCP → NOT possible — JVM reuses existing literal.
- Duplicate objects possible in heap, but NOT in SCP.
## 56:37 — Example 3: Runtime concat + constant pool (Durga / Software / Solutions / Soft)

### Code

```java
String s1 = new String("Durga");
s1.concat("Software");
String s2 = s1.concat("Solutions");
s1 = s1.concat("Soft");
System.out.println(s1);
System.out.println(s2);
```

### Output

DurgaSoft
DurgaSolutions

### Line-by-line trace

### Why output is NOT `DurgaSoftware`

- concat() returns a new String — it does not modify s1 in place (immutability).
- First concat("Software") result is discarded → s1 still "Durga".
- s2 captures "Durga" + "Solutions" = "DurgaSolutions".
- Reassignment s1 = s1.concat("Soft") → "DurgaSoft".
### Object count — **8 total** (4 SCP + 4 heap)

SCP constants (compile-time string literals in double quotes):

Rule: For every string constant (literal in `"..."`), one object is placed in SCP.

Heap objects (runtime-created):

Rule: *Because of runtime operation (concat at runtime), if a new object is required, it is placed only in the heap, never in SCP.*

### Common wrong answer

Students often say 5 objects (1 heap + 4 SCP) — that misses runtime heap objects from concat. Correct answer: 4 + 4 = 8.

## 1:09:31 — Example 4: Seasons variant (same rules, different literals)

### Code

```java
String s1 = "Spring";
s1.concat("Summer");
String s2 = s1.concat("Winter");
s1 = s1.concat("Fall");
System.out.println(s1);
System.out.println(s2);
```

### Output

SpringFall
SpringWinter

### Trace

- s1 was still "Spring" until the final reassignment (immutability).
- "Spring" + "Fall" at runtime → "SpringFall".
- "Spring" + "Winter" → "SpringWinter" held by s2.
### SCP constants in this example: 4

"Spring", "Summer", "Winter", "Fall"

## Master rules sheet (exam compilation)

### Immutability & mutability

### `equals()` and `==`

### Heap vs SCP creation

### SCP vs heap rules

## Complete exam programs (copy-paste ready)

### Program 1 — Immutability demo

```java
class ImmutabilityDemo {
    public static void main(String[] args) {
        String s = new String("Durga");
        s.concat("Software");
        System.out.println("String s      : " + s);           // Durga

        StringBuffer sb = new StringBuffer("Durga");
        sb.append("Software");
        System.out.println("StringBuffer sb: " + sb);         // DurgaSoftware
    }
}
```

### Program 2 — equals() String vs StringBuffer

```java
class EqualsDemo {
    public static void main(String[] args) {
        String s1 = new String("Durga");
        String s2 = new String("Durga");
        System.out.println("String ==       : " + (s1 == s2));        // false
        System.out.println("String equals   : " + s1.equals(s2));     // true

        StringBuffer sb1 = new StringBuffer("Durga");
        StringBuffer sb2 = new StringBuffer("Durga");
        System.out.println("StringBuffer == : " + (sb1 == sb2));      // false
        System.out.println("StringBuffer eq : " + sb1.equals(sb2));   // false
    }
}
```

### Program 3 — new String vs literal

```java
class HeapVsScpDemo {
    public static void main(String[] args) {
        String a = new String("Durga");   // heap + SCP
        String b = "Durga";               // SCP only
        System.out.println("a == b : " + (a == b));   // false (heap vs SCP)
        System.out.println("a.equals(b): " + a.equals(b)); // true (same content)
    }
}
```

### Program 4 — Object count S1–S4

```java
class ObjectCountDemo {
    public static void main(String[] args) {
        String s1 = new String("Durga");  // heap + SCP
        String s2 = new String("Durga");  // heap only (SCP reuse)
        String s3 = "Durga";              // SCP reuse
        String s4 = "Durga";              // SCP reuse
        // Total: 3 objects (2 heap + 1 SCP)
        System.out.println("s3 == s4 : " + (s3 == s4));  // true
        System.out.println("s1 == s2 : " + (s1 == s2));    // false
    }
}
```

### Program 5 — Concat output (Durga / Software / Solutions / Soft)

```java
class ConcatDemo {
    public static void main(String[] args) {
        String s1 = new String("Durga");
        s1.concat("Software");
        String s2 = s1.concat("Solutions");
        s1 = s1.concat("Soft");
        System.out.println("s1: " + s1);   // DurgaSoft
        System.out.println("s2: " + s2);   // DurgaSolutions
    }
}
```

### Program 6 — Seasons output

```java
class SeasonsDemo {
    public static void main(String[] args) {
        String s1 = "Spring";
        s1.concat("Summer");
        String s2 = s1.concat("Winter");
        s1 = s1.concat("Fall");
        System.out.println("s1: " + s1);   // SpringFall
        System.out.println("s2: " + s2);   // SpringWinter
    }
}
```

## Quick FAQ (interview + OCJP)

Q: What is the difference between String and StringBuffer?

- String → immutable; StringBuffer → mutable.
- String equals() compares content; StringBuffer equals() compares references.
Q: Explain immutability with an example.

- Use Case 1: s.concat("X") without assignment leaves s unchanged.
Q: How many objects for `new String("Durga")`?

- Two: one heap (referenced by variable), one SCP literal (for reuse).
Q: How many objects for `String s = "Durga"`?

- One: SCP only.
Q: Can two identical literals share one SCP object?

- Yes — s3 == s4 is true when both are "Durga".
Q: Can two `new String("Durga")` share one heap object?

- No — each new creates a separate heap object.
Q: Where do runtime `concat` results go?

- Heap only — SCP holds compile-time constants (literals), not runtime concat results.
Q: Why isn't the extra SCP object from `new String("X")` garbage-collected?

- SCP is in the method area; GC runs only on the heap.
Q: When are SCP objects removed?

- At JVM shutdown (or server shutdown in production).
## What's next (Video 110+)

This video covers String fundamentals: immutability, equals() differences, heap vs SCP, and object-count puzzles. Video 110 continues with String constructors and important methods (charAt, concat, equalsIgnoreCase, substring, etc.).

Source: Local Whisper STT transcript · Video 109 of 203 · Durga Soft OCJP/SCJP `java.lang` playlist

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Title | Core Java With OCJP/SCJP: java.lang.package Part-5 \ | \ | Strings class |
| Position | 109 of 203 · Series java.lang · Part 5 |  |  |
| Duration | 1h 16m 07s (from transcript) |  |  |
| ID | cI2JVbEWGy8 |  |  |
| Watch | https://www.youtube.com/watch?v=cI2JVbEWGy8 |  |  |
| Playlist | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |  |  |

| Case | Output |
|---|---|
| String | Durga |
| StringBuffer | DurgaSoftware |

| Expression | String | StringBuffer |
|---|---|---|
| ref1 == ref2 | false | false |
| ref1.equals(ref2) | true | false |

| Class | equals() overridden? | Comparison type |
|---|---|---|
| String | Yes | Content comparison — same characters → true even if different objects |
| StringBuffer | No | Falls back to Object.equals() → reference (address) comparison only |

| # | String | StringBuffer |
|---|---|---|
| 1 | Immutable | Mutable |
| 2 | equals() → content comparison | equals() → reference comparison (not overridden) |

| # | Location | Content | Referenced by |
|---|---|---|---|
| 1 | Heap | "Durga" | s |
| 2 | SCP (String Constant Pool) | "Durga" | No reference (stored for future reuse) |

| # | Location | Content | Referenced by |
|---|---|---|---|
| 1 | SCP | "Durga" | s |

| Area | GC applicable? |
|---|---|
| Heap | Yes |
| Method area (where SCP lives) | No |
| Stack area | No |
| PC registers | No |
| Native method stacks | No |

| Line | Action | Heap | SCP |
|---|---|---|---|
| s1 = new String("Durga") | new → heap object; literal → SCP | +1 heap "Durga" | +1 SCP "Durga" |
| s2 = new String("Durga") | new → heap object; SCP already has "Durga" → reuse | +1 heap "Durga" | no new object |
| s3 = "Durga" | Literal; SCP has "Durga" → reuse | — | reuse |
| s4 = "Durga" | Literal; SCP has "Durga" → reuse | — | reuse |

| Metric | Count |
|---|---|
| Total objects | 3 |
| Heap | 2 (one per new) |
| SCP | 1 ("Durga") |

| Line | s1 points to | s2 | Notes |
|---|---|---|---|
| s1 = new String("Durga") | heap "Durga" | — | +heap object; +SCP "Durga" |
| s1.concat("Software") | still heap "Durga" | — | Runtime → heap "DurgaSoftware" created; no reference → GC-eligible |
| s2 = s1.concat("Solutions") | heap "Durga" | heap "DurgaSolutions" | "Solutions" → SCP constant; result on heap only |
| s1 = s1.concat("Soft") | heap "DurgaSoft" | heap "DurgaSolutions" | "Soft" → SCP; "DurgaSoft" on heap |

| Constant | In SCP? |
|---|---|
| "Durga" | Yes |
| "Software" | Yes |
| "Solutions" | Yes |
| "Soft" | Yes |

| Object | Referenced by | Notes |
|---|---|---|
| "Durga" (from new) | was s1, then orphaned when s1 reassigned | initially referenced |
| "DurgaSoftware" | none | orphan → GC-eligible |
| "DurgaSolutions" | s2 |  |
| "DurgaSoft" | s1 |  |

| Step | Detail |
|---|---|
| s1 = "Spring" | SCP "Spring"; s1 → SCP |
| s1.concat("Summer") | SCP "Summer"; runtime heap "SpringSummer" — discarded |
| s2 = s1.concat("Winter") | SCP "Winter"; heap "SpringWinter" → s2 |
| s1 = s1.concat("Fall") | SCP "Fall"; heap "SpringFall" → s1 |

|  | String | StringBuffer |
|---|---|---|
| Change existing object? | No | Yes |
| Modify operation effect | New object created | Same object updated |
| Term | Immutable | Mutable |

|  | == | equals() |
|---|---|---|
| String | Reference | Content (overridden) |
| StringBuffer | Reference | Reference (Object default) |

| Creation style | Objects | Where ref points |
|---|---|---|
| new String("X") | 2 (heap + SCP literal) | Heap copy |
| "X" (literal only) | 1 (SCP) | SCP |
| Runtime concat / + with variable | 1 on heap | Per assignment |

| Rule | Detail |
|---|---|
| SCP creation | Optional — reuse if content exists |
| Heap with new | Mandatory — always new object |
| Duplicates in heap | Allowed |
| Duplicates in SCP | Not allowed |
| GC on SCP | Never (method area) |
| SCP lifetime | Until JVM / server shutdown |
| Literal "..." | Always SCP (one per distinct constant) |
| Runtime concat result | Always heap only |
