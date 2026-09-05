# Video 107

## Video info

Title: Core Java With OCJP/SCJP: java.lang.package Part-3 || equals() || overridden methods of equals

Series: java.lang.package (Object class methods — continues from Part-2)

Instructor: Durga Sir

Duration: 1h 28m 24s

Video ID: izDt7L4009k

Watch: https://www.youtube.com/watch?v=izDt7L4009k

Transcript source: Local Whisper STT (.transcripts/107-izDt7L4009k.txt)

### 00:08 — Session opener: `equals()` method (continued from Part-2)

This lecture is Part-3 of the java.lang Object-class series. The previous session started equals(); this video completes the concept, shows how to override it properly, and ends with a high-value String vs StringBuffer exam question.

## Part A — Purpose of `equals()` and default `Object` behavior

### 00:27 — What is the purpose of `equals()`?

We can use the `equals()` method to check equality of two objects.

If two references obj1 and obj2 exist, calling:

obj1.equals(obj2);

answers: Are these two objects equal or not?

Board line:

We can use equals() method to check equality of two objects.

### 01:07 — Which `equals()` runs if our class does NOT override?

If our class does not contain an equals() method, then `Object` class `equals()` method will be executed (inherited default).

Every class ultimately inherits from Object, so this default is always available unless overridden.

### 01:27 — Setup: `Student` class (no `equals()` override yet)

```java
class Student {
    String name;
    int rollNumber;

    Student(String name, int rollNumber) {
        this.name = name;
        this.rollNumber = rollNumber;
    }
}
```

### 04:08 — Main program: four references, three comparisons

```java
public static void main(String[] args) {
    Student s1 = new Student("Durga", 101);
    Student s2 = new Student("Ravi", 102);
    Student s3 = new Student("Durga", 101);   // same name + roll as s1, different object
    Student s4 = s1;                           // alias — same reference as s1

    System.out.println(s1.equals(s2));
    System.out.println(s1.equals(s3));
    System.out.println(s1.equals(s4));
}
```

Memory diagram (board):

s1 ──► [ Student: name=Durga, rollNumber=101 ]
s3 ──► [ Student: name=Durga, rollNumber=101 ]   ← different heap object
s2 ──► [ Student: name=Ravi,  rollNumber=102 ]
s4 ──► (points to same object as s1)

### 06:53 — Predict outputs BEFORE running (with default `Object.equals()`)

Output: false, false, true

### 07:03 — Critical distinction: `==` vs `.equals()` (recap from earlier classes)

Durga Sir's memory hook from prior lectures:

- == → reference comparison
- .equals() → intended for content comparison (but default Object version is still reference)
### 08:14 — Real-world vs Java answer for `s1.equals(s3)`

Real world: Two students with same name "Durga" and same roll number 101 → logically equal.

Java (without override): Returns false — because Object.equals() only checks whether both references point to the same object, not whether name/rollNumber match.

### 09:07 — How `Object.equals()` is implemented (conceptually)

```java
// Conceptual behavior of Object.equals(Object obj)
public boolean equals(Object obj) {
    // Reference / address comparison only
    // Returns true ONLY if both references point to the same object
    // Returns false if objects are different — even if content is identical
}
```

Board summary:

Object class equals() method is meant for reference comparison (address comparison), but not for content comparison.

Rules:

- If two references point to the same object → returns true
- If objects are different (different addresses) → returns false, regardless of content
### 10:14 — Why override `equals()`?

Default Object.equals() → reference comparison.

We usually want content comparison — e.g., two Student objects with same name and roll number should be considered equal.

If we are not satisfied with reference comparison, we can override `equals()` in our class for content comparison.

Reference comparison is already handled by `==`. Most of the time we need content comparison, not reference comparison, from equals().

## Part B — Overriding `equals()` for content comparison

### 22:53 — Step 1: Decide the meaning of "equality" for YOUR class

Before writing code, decide what makes two objects equal in your requirement.

For Student in this lecture:

- Equality rule: same name and same rollNumber → equal.
Other requirements might need more fields:

- Same name + roll + father + mother + address → equal
- Or only roll number → equal
Requirement to requirement, the meaning of equality changes. You must decide first.

### 24:11 — Step 2: Basic override signature

```java
public boolean equals(Object obj) {
    // obj is the "other" object passed as argument
    // "this" is the object on which equals() was called
}
```

Call flow for `s1.equals(s2)`:

Two objects are involved; argument arrives as `Object` type (parent reference).

### 25:31 — Step 3: Extract current object's fields (`this`)

```java
String name1 = this.name;
int rollNumber1 = this.rollNumber;
```

### 26:02 — Step 4: Downcast argument to `Student`

Argument is Object; to access name and rollNumber we must typecast:

```java
Student s = (Student) obj;
String name2 = s.name;
int rollNumber2 = s.rollNumber;
```

Object reference cannot tell "what is your name?" — only Student reference can.

### 27:14 — Step 5: Compare fields and return

```java
if (name1.equals(name2) && rollNumber1 == rollNumber2) {
    return true;
} else {
    return false;
}
```

Why `name1.equals(name2)` but `rollNumber1 == rollNumber2`?

### 28:53 — Full Version 1: basic content-comparison override

```java
class Student {
    String name;
    int rollNumber;

    Student(String name, int rollNumber) {
        this.name = name;
        this.rollNumber = rollNumber;
    }

    public boolean equals(Object obj) {
        String name1 = this.name;
        int rollNumber1 = this.rollNumber;

        Student s = (Student) obj;
        String name2 = s.name;
        int rollNumber2 = s.rollNumber;

        if (name1.equals(name2) && rollNumber1 == rollNumber2) {
            return true;
        } else {
            return false;
        }
    }

    public static void main(String[] args) {
        Student s1 = new Student("Durga", 101);
        Student s2 = new Student("Ravi", 102);
        Student s3 = new Student("Durga", 101);
        Student s4 = s1;

        System.out.println(s1.equals(s2));  // false — different name and roll
        System.out.println(s1.equals(s3));  // true  — same name and roll (CONTENT match)
        System.out.println(s1.equals(s4));  // true  — same reference AND same content
    }
}
```

Output with override: false, true, true

Compare to default Object.equals() output: false, false, true

### 32:18 — Demo: comment out override → back to `Object` behavior

If you comment out the overridden equals():

- Which method runs? → `Object` class `equals()`
- Output: `false`, `false`, `true` (reference comparison)
Uncomment override:

- Which method runs? → Our `equals()`
- Output: `false`, `true`, `true` (content comparison)
## Part C — Edge cases: heterogeneous types and `null`

### 33:34 — Trap: comparing `Student` with `String`

```java
System.out.println(s1.equals("Durga"));
```

These are heterogeneous (different, unrelated types for this comparison).

With our Version 1 override:

Student s = (Student) obj;   // obj is actually a String — INVALID cast

Result: ClassCastException at runtime.

Compile: fine. Run: `Exception in thread "main" java.lang.ClassCastException`

### 35:35 — How `Object.equals()` handles heterogeneous types

If we comment out our override and use default Object.equals():

System.out.println(s1.equals("Durga"));  // false — no exception

Gap: Our override throws ClassCastException; Object.equals() returns false.

Fix: Handle ClassCastException → return false:

```java
public boolean equals(Object obj) {
    try {
        String name1 = this.name;
        int rollNumber1 = this.rollNumber;

        Student s = (Student) obj;
        String name2 = s.name;
        int rollNumber2 = s.rollNumber;

        if (name1.equals(name2) && rollNumber1 == rollNumber2) {
            return true;
        } else {
            return false;
        }
    } catch (ClassCastException e) {
        return false;
    }
}
```

If we pass a different type of object, our equals() should not raise ClassCastException — it should return false, same as Object.equals().

### 38:22 — Trap: comparing with `null`

```java
System.out.println(s1.equals(null));
```

With Version 1 + try/catch for ClassCastException only:

Student s = (Student) obj;   // obj is null
String name2 = s.name;       // NPE — cannot ask null for name/rollNumber

Result: NullPointerException

Default Object.equals(null) → returns false (no exception).

Fix: Add second catch block:

```java
} catch (ClassCastException e) {
    return false;
} catch (NullPointerException e) {
    return false;
}
```

Do NOT use catch (Exception e) { return false; } — that is too broad and not the proper way.

After both catch blocks:

System.out.println(s1.equals(null));  // false

## Part D — Three mandatory concerns when overriding `equals()`

### 41:29 — Board summary: proper way of overriding `equals()`

While overriding equals() for content comparison, take care of the following three things:

Board heading:

The following is the proper way of overriding `equals()` method for Student class content comparison.

### 47:02 — Full Version 2: proper override with try/catch (board code)

```java
public boolean equals(Object obj) {
    try {
        String name1 = this.name;
        int rollNumber1 = this.rollNumber;

        Student s = (Student) obj;
        String name2 = s.name;
        int rollNumber2 = s.rollNumber;

        if (name1.equals(name2) && rollNumber1 == rollNumber2) {
            return true;
        } else {
            return false;
        }
    } catch (ClassCastException e) {
        return false;
    } catch (NullPointerException e) {
        return false;
    }
}
```

Comments Durga Sir adds on board:

- // obj → second object (s2 in s1.equals(s2))
- // this → first object (s1)
- Cast line → runtime exception risk without handling
- NPE line → runtime exception when obj is null
Test matrix with Version 2:

## Part E — Simplified versions of `equals()`

### 53:42 — Version 3: use implicit `this` inside instance method

Inside an instance method, accessing name directly is same as this.name:

```java
// In instance method m1():
SOP(x);        // same as this.x — current object's x
```

So in equals() we can drop name1, rollNumber1 and write:

```java
public boolean equals(Object obj) {
    try {
        Student s = (Student) obj;

        if (name.equals(s.name) && rollNumber == s.rollNumber) {
            return true;
        } else {
            return false;
        }
    } catch (ClassCastException e) {
        return false;
    } catch (NullPointerException e) {
        return false;
    }
}
```

Four lines removed — same output: false, true, true, false, false.

### 1:00:57 — Version 4: replace try/catch with `instanceof`

Key rules about `instanceof` and `null`:

null instanceof Student   // false — always
obj instanceof Student    // false if obj is null OR not a Student

So one if handles both wrong-type and null:

```java
public boolean equals(Object obj) {
    if (obj instanceof Student) {
        Student s = (Student) obj;
        if (name.equals(s.name) && rollNumber == s.rollNumber) {
            return true;
        } else {
            return false;
        }
    } else {
        return false;   // not Student type OR null
    }
}
```

Flow walkthrough:

No try/catch needed when using instanceof guard.

Output: `false`, `true`, `true`, `false`, `false` — same as Version 2.

### 1:10:03 — Version 5 (more simplified structure)

```java
public boolean equals(Object obj) {
    if (obj instanceof Student) {
        Student s = (Student) obj;
        return name.equals(s.name) && rollNumber == s.rollNumber;
    }
    return false;
}
```

## Part F — Performance optimization: reference check first

### 1:10:19 — Problem: wasteful comparison when references are identical

Consider s1.equals(s4) where s4 = s1 (same object).

Even with content-based equals(), the code still:

- Checks instanceof
- Casts
- Compares name and rollNumber
But if both references point to the same object, name and roll are guaranteed equal — no need to compare field by field.

Worst case: Suppose 1000 fields (or comparing two large collections with 1000 elements each). You might compare all 1000 properties for an hour, only to discover at the end they were the same object all along.

### 1:13:24 — Fix: add reference check at the **beginning** of `equals()`

```java
if (obj == this) {
    return true;
}
```

Board note:

To make equals() methods more efficient, at the beginning inside equals() method, write:

```java
if (obj == this) return true;
```

Meaning:

If both references point to the same object, then without performing any comparison, return true.

### 1:15:11 — Version 6 (final recommended form)

```java
public boolean equals(Object obj) {
    if (obj == this) {
        return true;
    }
    if (obj instanceof Student) {
        Student s = (Student) obj;
        return name.equals(s.name) && rollNumber == s.rollNumber;
    }
    return false;
}
```

Order matters:

- `obj == this` → fast path for same reference
- `instanceof Student` → safe type check (handles null + wrong type)
- Field comparison → content equality
This is the standard recommended approach used by JDK classes.

## Part G — `String.equals()` source: JDK follows the same pattern

### 1:16:48 — Open `String.java` and inspect `equals()`

Durga Sir opens the `String` class source (public final class String).

```java
public boolean equals(Object anObject) {
    if (this == anObject) {
        return true;
    }
    if (anObject instanceof String) {
        // ... content comparison logic for char sequences ...
        return true/false;
    }
    return false;
}
```

Same style as our final version:

- == this check first
- instanceof type check
- Content comparison inside
- Otherwise false
Some people (including JDK authors) follow our style — this is the standard approach to override equals().

## Part H — EXAM QUESTION: `String` vs `StringBuffer` with `==` and `equals()`

### 1:19:12 — Side-by-side demo (VERY IMPORTANT for OCJP / interviews)

```java
class Test {
    public static void main(String[] args) {
        // --- String case ---
        String s1 = new String("Durga");
        String s2 = new String("Durga");

        System.out.println(s1 == s2);         // false — different heap objects
        System.out.println(s1.equals(s2));    // true  — String.equals() = content comparison

        // --- StringBuffer case ---
        StringBuffer sb1 = new StringBuffer("Durga");
        StringBuffer sb2 = new StringBuffer("Durga");

        System.out.println(sb1 == sb2);       // false — different objects
        System.out.println(sb1.equals(sb2));  // false — Object.equals() = reference comparison
    }
}
```

Output:

false
true
false
false

### 1:22:10 — Universal exam rule

If s1.equals(s2) is true (content equal), then s1 == s2 is automatically false when they are different objects with same content.

Conversely:

- == true → always same reference
- equals true with == false → different objects, same content (only possible when equals() is overridden for content)
### 1:22:46 — Theory board (both columns)

String class:

In String class, equals() method is overridden for content comparison.

Hence, even though objects are different, if content is the same, then equals() returns true.

StringBuffer class:

In StringBuffer class, equals() method is NOT overridden for content comparison.

Hence, if objects are different, equals() returns false, even though content is the same.

Why StringBuffer doesn't override `equals()`: Mutable objects are generally not used as keys in hash-based collections the same way; identity/reference semantics are often sufficient for mutable buffers. For exam purposes: memorize the behavior, not the design philosophy.

## Part I — Version progression summary

## Part J — Quick revision checklist (OCJP)

- [ ] Purpose of equals(): check equality of two objects
- [ ] Default Object.equals(): reference comparison only
- [ ] == also does reference comparison — use equals() override when you need content
- [ ] Decide meaning of equality before coding
- [ ] Override signature: public boolean equals(Object obj)
- [ ] Argument is Object; use cast or instanceof before accessing subclass fields
- [ ] Compare String fields with .equals(), primitives with ==
- [ ] Wrong type → return false (not ClassCastException)
- [ ] null argument → return false (not NullPointerException)
- [ ] instanceof returns false for null
- [ ] Add if (obj == this) return true; at start for efficiency
- [ ] JDK String.equals() follows same pattern
- [ ] `String.equals()` → content; `StringBuffer.equals()` → reference (not overridden)
## ASR decode notes (this video)

Whisper STT artifacts decoded in these notes:

Java code block count: 15+

## Metadata

## Tables (placement lost -- re-place these in context)

| Expression | Answer | Why |
|---|---|---|
| s1.equals(s2) | false | Different objects, different content |
| s1.equals(s3) | false | Same content but different objects |
| s1.equals(s4) | true | Both references point to the same object |

| Operator / method | Comparison type |
|---|---|
| `==` (double equal) | Reference comparison (address comparison) |
| `.equals()` (default in Object) | Also reference comparison in Object class |
| `.equals()` (when overridden) | Content comparison (based on your rule) |

| Role | Reference |
|---|---|
| Object on which method is called (this) | s1 |
| Argument passed (obj) | s2 |

| Field | Type | Comparison |
|---|---|---|
| name | String (object) | name1.equals(name2) — String.equals() is already overridden for content comparison |
| rollNumber | int (primitive) | rollNumber1 == rollNumber2 — primitives have no methods; use == |

| Reference | Type |
|---|---|
| s1 | Student |
| "Durga" | String |

| # | Concern | Rule |
|---|---|---|
| 1 | Meaning of equality | Decide which fields define equality (name only? roll only? both? all fields?) |
| 2 | Different type of object | Our equals() must not raise ClassCastException → handle it → return false |
| 3 | `null` argument | Our equals() must not raise NullPointerException → handle it → return false |

| Call | Result |
|---|---|
| s1.equals(s2) | false |
| s1.equals(s3) | true |
| s1.equals(s4) | true |
| s1.equals("Durga") | false |
| s1.equals(null) | false |

| Call | obj instanceof Student | Result |
|---|---|---|
| s1.equals(s2) | true (Student, different content) | false |
| s1.equals(s3) | true (Student, same content) | true |
| s1.equals(s4) | true (Student, same ref + content) | true |
| s1.equals("Durga") | false (String, not Student) | false |
| s1.equals(null) | false (null instanceof Student is false) | false |

| Class | equals() overridden? | Different objects, same text | sb1.equals(sb2) |
|---|---|---|---|
| String | Yes — content | "Durga" vs "Durga" | true |
| StringBuffer | No — uses Object.equals() | "Durga" vs "Durga" | false |

| Version | Technique | try/catch | instanceof | obj == this |
|---|---|---|---|---|
| V1 | Basic cast + compare | No | No | No |
| V2 | + CCE/NPE handling | Yes | No | No |
| V3 | Implicit this fields | Yes | No | No |
| V4 | instanceof guard | No | Yes | No |
| V5 | Compact return | No | Yes | No |
| V6 (final) | Full recommended | No | Yes | Yes |

| Heard (caption) | Intended |
|---|---|
| equal sum of that / equal cement / equal smithere | equals() method |
| O be J / boBJ / goBJ | Object obj |
| reference comparison / address comparison | same concept |
| class cash / clashed | ClassCastException |
| null point or / null pointer | NullPointerException |
| in instance of / inistence of | instanceof |
| Singh Buffal / string of buffer | StringBuffer |
| eqals (title typo) | equals() |
| Durga / Ravi / Raja | example student names |
| keep sabading / legend | listen carefully |
| content comparison / condense comparison | content comparison |
| ebc and the way | efficient way |

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP (java.lang package series) |
| Position | 107 of 203 |
| Series | java.lang.package Part-3 |
| Topic | Object.equals() — default behavior, overriding for content comparison, edge cases, simplifications, String vs StringBuffer |
| Instructor | Durga Sir |
| Duration | 1h 28m 24s |
| Video ID | izDt7L4009k |
| Watch | https://www.youtube.com/watch?v=izDt7L4009k |
| Transcript | .transcripts/107-izDt7L4009k.txt (Local Whisper STT) |
| Related videos | Part-2 (106): Object methods intro; Part-12 (117): == vs equals() relation + hashCode contract |
