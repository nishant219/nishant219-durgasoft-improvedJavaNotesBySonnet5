# Video 117

## Video info

**Title:** Core Java With OCJP/SCJP: java.lang.package Part-12 || object class || equals() || Hashcode()

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP (java.lang package series) |
| Position | 117 of 203 |
| Series | Core Java With OCJP/SCJP — java.lang package |
| Topic | Object class — == vs equals(), differences table, equals()–hashCode() contract |
| Instructor | Durga Sir |
| Duration | 1h 28m 45s (from transcript) |
| Video ID | wJgua6AobQU |
| Watch | https://www.youtube.com/watch?v=wJgua6AobQU |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

### 00:07 — Session opener: `equals()` postmortem continues

Durga Sir resumes from the previous session’s **postmortem on `equals()`**.

- Default `Object.equals()` performs **reference comparison** (same object in memory).
- We **can override** `equals()` for **content comparison**.
- Today’s focus: **relation between `==` and `.equals()`**, then **differences**, then **`equals()`–`hashCode()` contract**.
### 01:43 — Relation between `==` and `.equals()`: four conclusions

Board heading: *Relation between double equal operator and dot equals method.*

**Setup:** `R1` and `R2` are object references.

#### Conclusion 1 — `==` true ⇒ `.equals()` always true

If `R1 == R2` is **true** (both point to the **same object**), then `R1.equals(R2)` is **always true**:

- Without override: reference comparison → true.
- With content-based override: same object ⇒ same content ⇒ true.
> **Rule:*** If two objects are equal by *`==`*, they are ***always*** equal by *`.equals()`*.*

#### Conclusion 2 — `==` false ⇒ `.equals()` inconclusive

If `R1 == R2` is **false** (different objects), then `R1.equals(R2)` may be **true or false**:

- Without override: false (reference comparison).
- With content override: may still be **true** if contents match.
> **Rule:*** If not equal by *`==`*, we ***cannot conclude*** anything about *`.equals()`*.*

#### Conclusion 3 — `.equals()` true ⇒ `==` inconclusive

If `R1.equals(R2)` is **true**, then `R1 == R2` may be **true or false**:

- Same content, different objects ⇒ `equals` true, `==` false.
> **Rule:*** Equal by *`.equals()`* does ***not*** force equal by *`==`*.*

#### Conclusion 4 — `.equals()` false ⇒ `==` always false

If `R1.equals(R2)` is **false**, both are **not** the same object; therefore `R1 == R2` is **always false**.

> **Memory aid (internal concept, not rote):**

> *- *`==`* true → *`equals`* always true*

> *- *`==`* false → *`equals`* maybe*

> *- *`equals`* true → *`==`* maybe*

> *- *`equals`* false → *`==`* always false*

Exam tip: theoretical bits on these four rules are common in OCJP/SCJP-style interviews.

### 05:01 — Board writing: conclusion 2 (`==` false)

If `R1 == R2` is **false** → both references point to **different objects**.

Then `R1.equals(R2)`:

- **Cannot** say always false.
- **Cannot** say always true.
- **May return true or false** — depends on whether `equals()` is overridden for content.
Board line:

> *If two objects are ***not equal*** by *`==`*, we ***can't conclude anything*** about *`.equals()`* — it may return true or false.*

### 08:27 — Board writing: conclusions 3 and 4 (reverse direction)

**Conclusion 3:** If `R1.equals(R2)` is **true** → `R1 == R2` **may** be true or false (content-equal but possibly different objects).

**Conclusion 4:** If `R1.equals(R2)` is **false** → references **cannot** point to same object → `R1 == R2` is **always false**.

Durga Sir stresses: **understand the internal concept**; do not memorize blindly.

Quick oral recap before moving on:

| `==` true | `equals` always true |

| `==` false | `equals` maybe |

| `equals` true | `==` maybe |

| `equals` false | `==` always false |

### 11:09 — Transition to differences + String/StringBuffer preview

After four relation rules, next topic: **differences between `==` and `.equals()`**.

Before the summary table, a **String vs StringBuffer** example proves type rules for `==` (incomparable types) vs permissive `.equals()`.

### 15:28 — Worked example: `String` vs `StringBuffer` with `==` and `equals()`

Board code (ASR decoded: *durka* / *da* = demo literal `"durga"`):

```java
String s1 = new String("durga");
String s2 = new String("durga");
StringBuffer sb1 = new StringBuffer("durga");
StringBuffer sb2 = new StringBuffer("durga");

System.out.print(s1 == s2);           // CE: none — prints false
System.out.print(s1.equals(s2));      // prints true
System.out.print(sb1 == sb2);         // prints false
System.out.print(sb1.equals(sb2));    // prints false
System.out.print(s1 == sb1);          // CE: incomparable types
System.out.print(s1.equals(sb1));     // prints false
```

**Line-by-line CE / print annotations:**

| Expression | Result | Reason |
|---|---|---|
| s1 == s2 | false | Different heap objects |
| s1.equals(s2) | true | String.equals() overridden for content |
| sb1 == sb2 | false | Different objects |
| sb1.equals(sb2) | false | StringBuffer does not override equals() → Object.equals() → reference comparison |
| s1 == sb1 | Compile-time error | incomparable types: java.lang.String and java.lang.StringBuffer |
| s1.equals(sb1) | false | No compile/runtime error; unrelated types → false |

**Critical rule for `==` on references:**

> *To use *`==`* between reference types, there must be a ***type relation***: same type, or parent–child (up/down castable). Otherwise → ***compile-time error: incomparable types***.*

For `.equals()`: **no such rule** — pass any `Object`; returns `false` if not equal.

### 21:04 — Live demo: `class Test` through first four prints

```java
class Test {
    public static void main(String[] args) {
        String s1 = new String("durga");
        String s2 = new String("durga");
        StringBuffer sb1 = new StringBuffer("durga");
        StringBuffer sb2 = new StringBuffer("durga");

        System.out.print(s1 == s2);        // false
        System.out.print(s1.equals(s2)); // true
        System.out.print(sb1 == sb2);      // false
        System.out.print(sb1.equals(sb2)); // false

        // System.out.print(s1 == sb1);   // CE: incomparable types
        System.out.print(s1.equals(sb1));  // false
    }
}
```

**Executed output (concatenated prints):** `false` `true` `false` `false` `false`

Durga Sir runs `javac Test.java` and `java Test` — confirms the five boolean results.

### 23:58 — Board theory: type rules for `==` vs `equals()`

**To use `==` (reference types):**

- Compulsory: some relation between argument types — **child→parent**, **parent→child**, or **same type**.
- Otherwise: compile-time error saying **incomparable types**.
**If no relation between argument types:**

- `.equals()` → no compile/runtime error; simply returns **`false`**.
### 29:40 — Differences between `==` and `.equals()` (full table)

| # | == (equality operator) | .equals() (method) |
|---|---|---|
| 1 | Operator in Java; applicable to primitives and reference types | Method; applicable only to reference types (not primitives) |
| 2 | For references: always reference/address comparison | Default in Object: reference comparison; can override for content |
| 3 | Cannot override (no operator overloading in Java) | Can override for content comparison |
| 4 | Unrelated types → compile-time error (incomparable types) | Unrelated types → returns `false`, no error |

**Invalid primitive use (board):**

```java
// 10 == 20;           // valid — boolean result
// s1.equals(s2);      // valid
// 10.equals(20);      // CE: int cannot be dereferenced / invalid
```

**One-line interview answer:**

> *Use *`==`* for ***reference comparison***; use *`.equals()`* for ***content comparison*** (when overridden).*

### 33:58 — Writing the differences table on board (row by row)

Durga Sir builds the full comparison table live:

**Row 1 — Operator vs method / applicability**

- `==`: operator; primitives **and** references (`10 == 20` valid; `s1 == s2` valid when types comparable).
- `.equals()`: method; **objects only** — `10.equals(20)` → **compile error**.
**Row 2 — Reference semantics**

- `==`: always reference/address comparison for objects.
- `.equals()`: default in `Object` is reference; overridable for content.
**Row 3 — Overriding**

- `==`: **cannot** override (no operator overloading).
- `.equals()`: **can** override for content.
**Row 4 — Unrelated types**

- `==`: compile error **incomparable types**.
- `.equals()`: returns **`false`**, no error.
One-line entry-room answer added below table:

> *In general: *`==`* for reference comparison; *`.equals()`* for content comparison.*

### 42:00 — Similarity: comparing any reference with `null`

For **any** object reference `R`:

```java
Thread t = new Thread();
System.out.print(t == null);      // false
System.out.print(t.equals(null)); // false
```

**Note:** Both `R == null` and `R.equals(null)` **always return false** for any non-null reference `R`.

(This is the **one small similarity** between `==` and `.equals()`.)

### 44:49 — Hashing data structures and bucket rule (motivation for contract)

Before the contract, Durga Sir explains **hashing-related collections** (`HashSet`, `HashMap`, `Hashtable`):

- They use **bucket** terminology.
- Objects are placed in buckets based on **hash code**.
- **Fundamental rule:** Two **equivalent** objects (`equals` returns true) **must** be placed in the **same bucket**.
- **Converse is NOT true:** Objects in the same bucket **need not** be equal.
Board note:

> *Hashing related data structures follow: **Two equivalent objects should be placed in same bucket.*

> *But: **All objects in the same bucket need not be equal.*

### 50:06 — Contract between `equals()` and `hashCode()`

**Fundamental contract (one-line exam answer):**

> *If two objects are equal by *`.equals()`*, their ***hash codes must be equal***.*

> *Equivalently: ***Two equivalent objects must have the same hash code.**

Formal board lines:

- If two objects are equal by `.equals()` → their hash codes **must be equal**.
- If `R1.equals(R2)` is true → `R1.hashCode() == R2.hashCode()` must hold.
**Why override `hashCode()` when overriding `equals()`:**

- `Object.equals()` and `Object.hashCode()` **already satisfy** the contract (same object ⇒ same hash code).
- When you override `equals()` for content equality, you **must** override `hashCode()` so equivalent objects share hash codes.
> *★ ***Star note:*** Whenever we override *`equals()`*, compulsorily override *`hashCode()`* to satisfy the contract.*

> *No compile/runtime error if you skip it — but ***bad programming practice***; breaks hash-based collections.*

### 57:44 — Reverse / partial rules involving `hashCode()`

| Condition | Conclusion about .equals() |
|---|---|
| Equal by .equals() | Hash codes must be equal |
| Not equal by .equals() | No restriction on hash codes (may be same or different) |
| Hash codes equal | Cannot conclude about .equals() (may true or false) |
| Hash codes not equal | Objects are always not equal by .equals() |

Reason for last row: unequal hash codes ⇒ different buckets ⇒ cannot be equivalent objects.

### 1:03:22 — One-line contract answer + override obligation (exam star)

**Interview one-liner:**

> *Two equivalent objects must have the ***same hash code***.*

**Override rule (star note):**

> *To satisfy contract between *`equals()`* and *`hashCode()`*: whenever overriding *`equals()`*, ***compulsorily override `hashCode()`*** using the ***same logical fields***.*

- Skipping `hashCode()` → **no compile/runtime error**, but **bad practice** and breaks `HashMap`/`HashSet` behavior.
- Old OCJP direct MCQ: “When overriding `equals()`, which method must also be overridden?” → **`hashCode()`** (not `clone()`, not `toString()`).
Modern exams: given an `equals()` implementation, pick the **`hashCode()`** that keeps equal objects consistent.

### 1:06:10 — Demo: `String` — `equals()` and `hashCode()` both content-based

```java
String s1 = new String("durga");
String s2 = new String("durga");

System.out.println(s1.equals(s2));   // true
System.out.println(s1.hashCode());   // e.g. 95949803 (same on all JVMs for same content)
System.out.println(s2.hashCode());   // same value as s1.hashCode()
```

**Executed output:** `true` then two **identical** hash code integers (board showed `95949803` for both).

**Board theory:**

- In `String` class, `equals()` is overridden for **content comparison**.
- Hence `hashCode()` is also overridden to generate hash code **based on content**.
- Same content ⇒ same hash code on **every system** (deterministic).
### 1:10:43 — Demo: `StringBuffer` — no content `equals()`, identity hash codes

```java
StringBuffer sb1 = new StringBuffer("durga");
StringBuffer sb2 = new StringBuffer("durga");

System.out.println(sb1.equals(sb2));   // false
System.out.println(sb1.hashCode());      // e.g. 1962141457 (varies by JVM/address)
System.out.println(sb2.hashCode());      // different from sb1
```

**Executed output:** `false`, then **different** hash codes (board example: `1962141457` vs `4872882`).

**Board theory:**

- `StringBuffer.equals()` **not** overridden for content → reference comparison → false.
- `hashCode()` **not** overridden → based on **object address** → varies system to system.
Contrast: **`String` hash = content-based (fixed); `StringBuffer` hash = identity-based (variable).**

### 1:14:54 — Exam MCQ: appropriate `hashCode()` for a custom `Person` class

**`Person` with content `equals()` on `name` and `age`:**

```java
class Person {
    String name;
    int age;

    public boolean equals(Object obj) {
        if (obj instanceof Person) {
            Person p = (Person) obj;
            if (name.equals(p.name) && age == p.age)
                return true;
        }
        return false;
    }
}
```

**Which `hashCode()` is appropriate?**

```java
// Option 1 — WRONG
public int hashCode() { return 100; }
// Same hash for ALL persons → violates contract when equals differs

// Option 2 — WRONG
public int hashCode() { return age + socialSecurityNumber; }
// Two persons equal by name+age can have different SSN → different hash codes

// Option 3 — CORRECT
public int hashCode() { return name.hashCode() + age; }
// Equal persons (same name + age) → same hash code

// Option 4 — "No restrictions" — WRONG
```

**Counter-example for Option 2:** Two `Person` objects both named Shiva, age 30, equal by `equals()`, but SSN 60 vs 90 → hash 90 vs 120 → **contract violated**.

**Best practice note:**

> *Based on which parameters you override *`equals()`*, use the ***same parameters*** when overriding *`hashCode()`*.*

### 1:21:24 — Board note: `equals()` override recommendation + session close

In **all collection classes**, **all wrapper classes**, and **`String` class**, `equals()` is overridden for **content comparison**.

> *Hence it is ***highly recommended*** to override *`equals()`* in our classes for ***content comparison*** (and then *`hashCode()`* with matching fields).*

**Session recap (1:28:26):** `==` vs `.equals()` four rules, differences table, null similarity, hashing bucket motivation, **`equals()`–`hashCode()` contract**, `String` vs `StringBuffer` demos, `Person` MCQ, override recommendations.

**Java block count:** 8
