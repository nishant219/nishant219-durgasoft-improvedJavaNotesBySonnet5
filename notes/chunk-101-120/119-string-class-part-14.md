# Video 119

## Video info

**Title:** Core Java With OCJP/SCJP: java.lang.package Part-14 ||String class

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP (java.lang package series) |
| Position | 119 of 203 |
| Series | Core Java With OCJP/SCJP — java.lang package |
| Topic | String class — heap vs SCP, compile-time constants, intern(), SCP importance, FAQs |
| Instructor | Durga Sir |
| Duration | 1h 33m 29s (from transcript) |
| Video ID | oEAiBx_06SA |
| Watch | https://www.youtube.com/watch?v=oEAiBx_06SA |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

### 00:08 — Session opener: practical proof for heap vs SCP

Previous session explained **where String objects are created** (heap vs **String Constant Pool / SCP**) theoretically but **without running code**. This session provides **executable proof** and extends into **interning**, **SCP importance**, and **entry-room FAQs**.

(ASR note: *SCP*, *SAP*, *SP* in captions = **String Constant Pool**.)

### 01:21 — Diagram setup: two `new String(...)` lines

```java
String s1 = new String("you cannot change me");
String s2 = new String("you cannot change me");
```

**Memory diagram (board):**

| Area | Objects |
|---|---|
| SCP | One literal "you cannot change me" (for future reuse) |
| Heap | Two separate String objects (one per new) |

**Total from two lines:** **3 objects** — 2 heap + 1 SCP.

Reference variables: `s1` → heap object #1; `s2` → heap object #2.

### 03:48 — Reference comparisons: `s1`, `s2`, `s3`, `s4`

```java
System.out.print(s1 == s2);  // false — different heap objects

String s3 = "you cannot change me";   // SCP reuse
System.out.print(s1 == s3);           // false — heap vs SCP

String s4 = "you cannot change me";   // reuses same SCP object as s3
System.out.print(s3 == s4);           // true — same SCP object
```

**Rules demonstrated:**

- `new` → **always** new heap object.
- String literal assignment → SCP; **reuse** if literal already exists.
### 05:54 — Compile-time constant concatenation: `s5`

```java
String s5 = "you cannot" + " change me";
System.out.print(s3 == s5);  // true
```

**Critical insight (exam trap):**

- `"you cannot"` and `" change me"` are **compile-time constants**.
- **`+` evaluated at compile time** → entire line becomes equivalent to:
```java
String s5 = "you cannot change me";
```

- **No runtime heap object** for the concatenation result.
- `s5` points to **same SCP object** as `s3` → `s3 == s5` is **true**.
Analogy from earlier operators topic:

```java
System.out.println(20 + 30);     // compiles as SOP(50)
System.out.println("ab" + "cd"); // compiles as SOP("abcd")
```

> *If ***all*** operands are compile-time constants, operation happens ***at compile time*** — JVM performance improves.*

### 09:46 — Runtime concatenation with normal variable: `s6`, `s7`

```java
String s6 = "you cannot";              // SCP literal
String s7 = s6 + " change me";         // s6 is NORMAL variable (not final)
System.out.print(s3 == s7);            // false
```

**Why runtime:**

- `s6` is a **normal variable** — may be reassigned (`s6 = "something else"`), so compiler cannot treat it as constant.
- At least **one non-constant** operand → `+` runs at **runtime**.
- `" change me"` still goes to SCP, but result `"you cannot change me"` is a **new heap object**.
- `s3` (SCP) vs `s7` (heap) → **`false`**.
**Three-line special-care summary (board):**

| Line pattern | When evaluated | Object location |
|---|---|---|
| "a" + "b" (both constants) | Compile time | SCP (reuse) |
| s6 + " change me" (s6 normal var) | Runtime | Heap |
| final String s8 = "you cannot"; s9 = s8 + " change me" | Compile time | SCP (reuse) |

### 13:06 — `final` variable restores compile-time folding: `s8`, `s9`

```java
final String s8 = "you cannot";
String s9 = s8 + " change me";
System.out.print(s3 == s9);   // true

System.out.print(s6 == s8);   // true — both refer to same SCP "you cannot"
```

**Reason:** `final` variable replaced by its value at compile time → both operands constants → fold to `"you cannot change me"` in SCP.

### 17:07 — Full `Test` program executed on board

```java
class Test {
    public static void main(String[] args) {
        String s1 = new String("you cannot change me");
        String s2 = new String("you cannot change me");
        System.out.print(s1 == s2);           // false

        String s3 = "you cannot change me";
        System.out.print(s1 == s3);           // false

        String s4 = "you cannot change me";
        System.out.print(s3 == s4);           // true

        String s5 = "you cannot" + " change me";
        System.out.print(s3 == s5);           // true

        String s6 = "you cannot";
        String s7 = s6 + " change me";
        System.out.print(s3 == s7);           // false

        final String s8 = "you cannot";
        String s9 = s8 + " change me";
        System.out.print(s3 == s9);           // true

        System.out.print(s6 == s8);           // true
    }
}
```

**Executed concatenated output:** `false` `false` `true` `true` `false` `true` `true`

Durga Sir confirms: **`false true true false true true`** (seven boolean prints).

**Object count in program:** **6 objects total** in heap+SCP diagram; **3 distinct constants** in SCP: `"you cannot change me"`, `"you cannot"`, `" change me"`.

### 19:02 — Diagram snapshot: heap vs SCP object tally

Board diagram labels:

- **Heap area:** `s1` object, `s2` object, `s7` result object (runtime concat).
- **SCP area:** `"you cannot change me"`, `"you cannot"`, `" change me"` — literals/constants only.
Durga Sir asks students to photograph diagram showing **6 total objects** and **3 constants** in SCP.

### 25:05 — Board notes: compile-time vs runtime for string `+`

**Line 1 type** (`"you cannot" + " change me"`):

> *Operation performed ***yet compile time only*** because both arguments are compile-time constants.*

**Line 2 type** (`s6 + " change me"`):

> *Performed ***yet runtime only*** because at least one argument is a ***normal variable***.*

**Line 3 type** (`s8 + " change me"` with `final s8`):

> *Performed ***at compile time only*** — both arguments become compile-time constants.*

### 29:18 — Interning of String objects

**Problem:** `new String("durga")` → reference points to **heap** object. How to get the **corresponding SCP reference** for that content?

**Solution:** **`intern()` method**

```java
String s1 = new String("durga");   // s1 → heap; "durga" also in SCP
String s2 = s1;                    // s2 → heap (same as s1)
String s2b = s1.intern();          // s2b → SCP reference for "durga"

System.out.print(s1 == s2);        // true (both heap if s2 = s1)
System.out.print(s1 == s2b);       // false — heap vs SCP

String s3 = "durga";               // s3 → SCP
System.out.print(s2b == s3);       // true — both SCP
```

**Purpose of `intern()`:**

> *By using ***heap object reference***, if you want ***corresponding SCP object reference***, call ***`intern()`***.*

Board wording:

> *We can use *`intern()`* to get corresponding SCP object reference by using heap object reference.*

### 38:41 — `intern()` when no SCP entry exists yet (runtime `concat`)

```java
String s1 = new String("durga");
String s2 = s1.concat("software");   // runtime → heap "durgasoftware"; NO SCP entry yet
String s3 = s2.intern();             // creates "durgasoftware" IN SCP, returns it

String s4 = "durgasoftware";
System.out.print(s2 == s3);   // false — s2 heap, s3 SCP
System.out.print(s3 == s4);   // true — same SCP object
```

**Loophole / rule:**

> *If corresponding SCP object is ***not available***, ***`intern()` itself creates*** that object in SCP and returns the reference.*

**Not every heap object has a pre-existing SCP twin** — runtime-created strings may exist **only in heap** until `intern()` is called.

### 44:50 — Importance of String Constant Pool (SCP)

**Motivation:** String is the **most commonly used object** in Java (forms, JSP parameters, voter registration example with ~11 strings per voter × crores of users → memory disaster without optimization).

**Why SCP exists only for `String`, not `StringBuffer`:**

> *String is the ***most commonly used*** object → special memory management (SCP) provided.*

> *StringBuffer is ***rarely used*** → no special pool needed.*

**Advantage of SCP:**

> *Instead of creating a ***separate object for every requirement***, create ***one object*** and ***reuse*** for repeated literals (e.g. city name *`"Hyderabad"`* shared by 1 crore voters).*

→ **Memory utilization** and **performance** improve.

**Disadvantage / problem:**

- Many references (`v1…v1cr`) share **one** `"Hyderabad"` object in SCP.
- If **one** reference could **mutate** shared content, **all** voters’ city names would change → program behaves **abnormally**.
**Solution → immutability:**

> *String objects implemented as ***immutable*** — cannot change existing object. Any “change” creates a ***new object***; only that reference reassigned. Other references unaffected.*

**Trade-off:**

| SCP gives | SCP costs |
|---|---|
| Memory + performance | Immutability required — every change creates new object |

> **SCP is the only reason*** for immutability of String objects. Without SCP, immutability would not be required.*

### 1:02:01 — Formal SCP advantage/disadvantage board lines

Durga Sir writes extended theory:

**If string repeatedly required:**

- Not recommended: separate object every time → memory + performance problems.
- Recommended: **one object, reuse** → utilization improves (**because of SCP**).
**Main advantages of SCP:** memory utilization + performance **improved**.

**Main problem with SCP:** several references → same object; one reference changing content would affect **all** → solved by **immutability** (each change → **new object**).

**Hence:** SCP is the **only reason** for immutability of String objects.

### 1:01:53 — Board theory: reuse vs separate objects

If a String is **repeatedly required** in program:

- **Not recommended:** separate object per use → performance + memory problems.
- **Recommended:** one object, reuse → improved utilization (possible because of SCP).
### 1:11:12 — Entry-room FAQs (frequently asked questions)

#### FAQ 1 — Difference between `String` and `StringBuffer`?

- `String` → **immutable**
- `StringBuffer` → **mutable**
#### FAQ 2 — Explain immutability and mutability with example?

Already covered in course (SCP + change creates new object).

#### FAQ 3 — Difference: `new String("durga")` vs `"durga"`?

| Form | Objects | Where |
|---|---|---|
| new String("durga") | 2 — SCP literal + heap String | Reference usually points to heap |
| "durga" | 1 — SCP only | Reference points to SCP |

#### FAQ 4 — Other differences besides immutability?

- `String.equals()` → **content** comparison (overridden)
- `StringBuffer.equals()` → **reference** comparison (not overridden)
#### FAQ 5 — What is SCP?

> *Specially designed memory area ***for String objects*** (String Constant Pool).*

#### FAQ 6 — Advantage of SCP?

Memory utilization + performance **improved** (reuse).

#### FAQ 7 — Disadvantage of SCP?

Forces **immutability** — every change needs new object.

#### FAQ 8 — Why SCP only for String, not StringBuffer?

String = most commonly used → special management. StringBuffer = not commonly used.

#### FAQ 9 — Why String immutable but StringBuffer mutable?

**String:** SCP → one object shared by many references → mutation would affect all → immutability required.

**StringBuffer:** no SCP → **separate object per requirement** → changing one does not affect others → mutability OK.

### 1:26:29 — String vs StringBuffer diagram (why mutability differs)

**String + SCP:** voters `v1…v1cr` share **one** `"Hyderabad"` SCP object — memory win, mutation danger.

**StringBuffer:** each voter gets **separate** `"Hyderabad"` object (`v1`, `v2`, `v3` …) — if `v3` changes to `"Vijayawada"`, others unaffected → **no need for immutability**.

Board lines:

> *But in StringBuffer there is ***no concept like SCP***. Hence for every requirement a ***separate object*** will be created. By using one reference, if we change content, ***no effect*** on remaining references → immutability concept ***not required*** for StringBuffer.*

> **All wrapper class objects*** (*`Byte`*, *`Short`*, *`Integer`*, *`Long`*, *`Float`*, *`Double`*, *`Character`*, *`Boolean`*) are also immutable.*

#### FAQ 11–14 — Preview only (deferred to later API session)

- Is it possible to create our own immutable class? → **Yes**
- How to create immutable class with example? → deferred
- Immutable means **non-changeable**
- Difference between **`final`** and **`immutable`**? → deferred (both “non-changeable” at surface but different concepts — covered later)
### 1:33:08 — Session close

Next: complete **String API** concepts, then immutable-class design and `final` vs `immutable` in detail.

**Java block count:** 10
