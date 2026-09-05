# Video 116 — Autoboxing & autounboxing part 2 (overloading)

## Video info

Title: Core Java With OCJP/SCJP: java.lang.package Part-11 || Autoboxing||Autounboxing-2

### 00:05 — Session focus: overloading + autoboxing climax

This video completes the autoboxing/autounboxing topic. Autoboxing was covered in video 115 — definitions, valueOf, cache buffer, == traps are assumed known here.

New focus: How autoboxing interacts with method overloading, together with:

- Widening — primitive promotion (smaller type → bigger type); exists since Java 1.0
- Varargs (int...) — variable-argument methods; introduced in Java 1.5 (same release as autoboxing)
SCJP/OCJP relevance: Compiler resolution order among overloaded methods is a frequent exam trap.

Prerequisites recap:

Widening chain (primitives only):

byte → short → int → long → float → double
char → int → long → float → double

### 02:39 — Baseline: calling `m1(int)` with varargs

Before the fight cases, establish that m1(int... x) accepts any number of int arguments including zero:

```java
class Test {
    static void m1(int... x) { }

    public static void main(String[] args) {
        m1();           // valid — zero arguments
        m1(10);         // valid
        m1(10, 20);     // valid
        m1(10, 20, 30, 40);  // valid
    }
}
```

### 04:37 — Case 1: Autoboxing vs widening

Two overloaded methods — one takes Integer, one takes long:

```java
class Test {
    static void m1(Integer i) {
        System.out.println("autoboxing");
    }

    static void m1(long l) {
        System.out.println("widening");
    }

    public static void main(String[] args) {
        int x = 10;
        m1(x);
    }
}
```

Argument: int x = 10 passed to m1(x).

Two possible conversions:

- int → Integer via autoboxing → matches m1(Integer)
- int → long via widening → matches m1(long)
Question: Which method is invoked?

Answer: `m1(long)` — widening wins.

Why? When both an old concept (widening, Java 1.0) and a new concept (autoboxing, Java 1.5) compete, the compiler gives priority to the older mechanism for backward compatibility with pre-1.5 code. Metaphor: "19+ years experience vs fresher" — experience (widening) wins.

```java
// prints: widening
```

Rule — Case 1: Widening dominates autoboxing.

### 11:25 — Case 2: Widening vs varargs

Same pattern, but second method uses varargs:

```java
class Test {
    static void m1(int... x) {
        System.out.println("varargs");
    }

    static void m1(long l) {
        System.out.println("widening");
    }

    public static void main(String[] args) {
        int x = 10;
        m1(x);
    }
}
```

Conversions available:

- int → long widening → m1(long)
- int → varargs (int...) — wraps single int in array
Answer: `m1(long)` — widening again.

Even when varargs is present, widening still beats varargs.

```java
// prints: widening
```

Rule — Case 2: Widening dominates varargs.

### 14:30 — Case 3: Autoboxing vs varargs

```java
class Test {
    static void m1(int... x) {
        System.out.println("varargs");
    }

    static void m1(Integer i) {
        System.out.println("autoboxing");
    }

    public static void main(String[] args) {
        int x = 10;
        m1(x);
    }
}
```

Both concepts are Java 1.5 — no "old vs new" tie-breaker.

Key rule from prior lectures: Varargs has the least priority among overload resolution strategies — analogous to `default` in a `switch`: it runs only when no other case matches.

Here m1(Integer) already matches via autoboxing, so varargs is not chosen.

```java
// prints: autoboxing
```

Rule — Case 3: Autoboxing dominates varargs.

Varargs least-priority rule (general):

If any other overload matches without needing varargs, the varargs method is not selected. Only when no other method matches does the varargs overload get the call — exactly like default in switch.

### 19:30 — Master priority order (★ exam note)

While resolving overloaded methods, the compiler gives precedence in this order:

Mnemonic: W → A → V (Widening, Autoboxing, Varargs)

Walk-through example with all three present:

```java
class Test {
    static void m1(long l)       { System.out.println("widening"); }
    static void m1(Integer i)    { System.out.println("autoboxing"); }
    static void m1(int... x)     { System.out.println("varargs"); }

    public static void main(String[] args) {
        int x = 10;
        m1(x);  // widening wins
    }
}
```

Remove widening:

```java
class Test {
    static void m1(Integer i)  { System.out.println("autoboxing"); }
    static void m1(int... x)   { System.out.println("varargs"); }

    public static void main(String[] args) {
        int x = 10;
        m1(x);  // autoboxing wins
    }
}
```

Only varargs left:

```java
class Test {
    static void m1(int... x) { System.out.println("varargs"); }

    public static void main(String[] args) {
        int x = 10;
        m1(x);  // varargs — only option
    }
}
```

### 23:10 — Case 4: `int` to `Long` (wrapper) — chained conversions

Trap question: Can int be passed to m1(Long L) where L is `java.lang.Long` (wrapper)?

```java
class Test {
    static void m1(Long L) {
        System.out.println("Long wrapper");
    }

    public static void main(String[] args) {
        int x = 10;
        m1(x);  // CE — does NOT compile
    }
}
```

Students often propose two conversion paths:

Path A (invalid):

int → Integer (autoboxing) → Long (???)

Integer and Long are sibling wrapper classes under Number. There is no widening or inheritance link from `Integer` to `Long`. This path does not work.

Path B (also invalid in Java):

int → long (widening) → Long (autoboxing)

Logically: primitive widen first, then box. But Java does NOT implement widening followed by autoboxing.

Compile error:

```java
// CE: incompatible types: int cannot be converted to java.lang.Long
```

Critical chained-conversion rules:

Memory aid: After W then A → invalid. After A then W → valid.

Related assignment examples:

```java
// CE — int cannot assign to Long wrapper directly
Long L = 10;

// CE — same reason
Long L = 10L;  // long literal, still primitive long → Long needs boxing of long, but int literal 10 to Long also fails for int arg

// Valid — primitive widening only
long l = 10;   // int → long widening

// Valid — widening then nothing else needed
Long L2 = 10L; // long literal 10L → autobox to Long
```

Clarification on long L = 10:

long L = 10;   // valid — int literal → long variable (widening)

Clarification on Long L = 10:

Long L = 10;   // CE: incompatible types found: int required: Long

### 31:08 — Theory summary: chained conversion policy

Widening followed by autoboxing  →  NOT allowed in Java
Autoboxing followed by widening  →  ALLOWED

Diagram (conceptual):

int ──widening──► long ──autobox──► Long     ✗ NOT supported as a chain for overload/assignment

int ──autobox──► Integer ──???──► Long       ✗ No conversion between wrapper siblings

int ──autobox──► Integer ──widening──► Object ✓ Allowed (child → parent reference)

### 35:28 — Case 5: Autoboxing followed by widening (`int` → `Object`)

```java
class Test {
    static void m1(Object o) {
        System.out.println("object version");
    }

    public static void main(String[] args) {
        int x = 10;
        m1(x);
    }
}
```

Conversion chain:

- int → Integer (autoboxing)
- Integer → Object (widening — subclass reference to superclass reference; Integer extends Number extends Object)
A then W is allowed → method call succeeds.

```java
// prints: object version
```

Equivalent valid assignments (same A→W pattern):

Object o = 10;        // valid — autoboxing + widening to Object
Number n = 10;        // valid — autoboxing + widening to Number

### 40:02 — Assignment validity quiz (10 options)

Decide valid/invalid and name the concept or compile error.

Error messages:

int i = 10L;
// CE: possible loss of precision
// found: long, required: int

Long L = 10;
// CE: incompatible types
// found: int, required: java.lang.Long

Double D = 10;
// CE: incompatible types
// found: int, required: java.lang.Double

Full quiz program:

```java
class AssignmentQuiz {
    public static void main(String[] args) {
        int i = 10;           // ✓ normal
        Integer I = 10;       // ✓ autoboxing
        // int j = 10L;       // ✗ possible loss of precision
        Long L1 = 10L;        // ✓ autoboxing
        // Long L2 = 10;      // ✗ incompatible types
        long l = 10;          // ✓ widening
        Object o = 10;        // ✓ autoboxing + widening
        double d = 10;        // ✓ widening
        // Double D = 10;     // ✗ incompatible types
        Number n = 10;        // ✓ autoboxing + widening
    }
}
```

### 45:31 — Session wrap-up

java.lang package topics covered across Parts 1–11:

- Object class hierarchy
- toString(), hashCode(), equals()
- String, StringBuffer, StringBuilder
- Wrapper classes
- Autoboxing & autounboxing (Parts 10–11)
Part 11 key takeaways:

- Overload resolution priority: Widening > Autoboxing > Varargs
- Old concept (widening) beats new (autoboxing) when both match
- Varargs = lowest priority (like switch default)
- Widening → Autoboxing chain: not allowed
- Autoboxing → Widening chain: allowed (e.g. int → Integer → Object)
- No direct conversion between sibling wrappers (Integer → Long)
- Long L = 10 fails; long l = 10 and Long L = 10L work
Next: Object class deep dive continues in video 117 (equals(), hashCode() contract).

## ASR decode notes

Java code block count: 14

### Overload resolution cheat sheet

### Chained conversion reference

## Tables (placement lost -- re-place these in context)

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 116 of 203 |
| Series | java.lang.package · Part 11 |
| Topic | Overloading with autoboxing, widening, and varargs |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 46m 01s |
| Video ID | tcHVFR5OzD8 |
| Watch | https://www.youtube.com/watch?v=tcHVFR5OzD8 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (no YouTube auto-captions) |

| Concept | Meaning | Since |
|---|---|---|
| Widening | Assign smaller primitive to larger primitive variable (e.g. byte → short → int → long → float → double) | Java 1.0 |
| Autoboxing | Primitive → wrapper object (int → Integer) | Java 1.5 |
| Varargs | Method accepts zero or more arguments of a type (m1(int... x)) | Java 1.5 |

| Priority | Mechanism | Notes |
|---|---|---|
| 1 (highest) | Widening | Primitive promotion |
| 2 | Autoboxing | Primitive → wrapper |
| 3 (lowest) | Varargs | Last resort; like switch default |

| Chain | Allowed? |
|---|---|
| Widening → Autoboxing (W then A) | NO — not implemented |
| Autoboxing → Widening (A then W) | YES — allowed |

| # | Statement | Valid? | Concept / Error |
|---|---|---|---|
| 1 | int i = 10; | ✓ | Normal int assignment |
| 2 | Integer I = 10; | ✓ | Autoboxing |
| 3 | int i = 10L; | ✗ | long → int narrowing — possible loss of precision |
| 4 | Long L = 10L; | ✓ | Autoboxing (long → Long) |
| 5 | Long L = 10; | ✗ | Incompatible types — int cannot convert to Long |
| 6 | long l = 10; | ✓ | Widening (int literal → long) |
| 7 | Object o = 10; | ✓ | Autoboxing followed by widening |
| 8 | double d = 10; | ✓ | Widening (int → double) |
| 9 | Double D = 10; | ✗ | Incompatible types — int cannot convert to Double |
| 10 | Number n = 10; | ✓ | Autoboxing followed by widening |

| Heard (Whisper) | Intended |
|---|---|
| over loading / we are loading | overloading |
| wearer / where are the methods | varargs |
| Vyrrach / Virarke / Verarca | varargs |
| why the name / why dening / why the new | widening |
| Dominate Sato boxing | dominates autoboxing |
| out of boxing | autoboxing |
| compelte / compultimate | compile |
| chavada blank dot long | java.lang.Long |
| pen (integer to object) | hierarchy (Integer is child of Object) |
| possible loss of precision found the long | possible loss of precision: found long, required int |

| Case | Methods | Winner |
|---|---|---|
| 1 | m1(Integer) vs m1(long) + int arg | Widening (long) |
| 2 | m1(int...) vs m1(long) + int arg | Widening (long) |
| 3 | m1(int...) vs m1(Integer) + int arg | Autoboxing (Integer) |
| 4 | m1(Long) + int arg | Compile error |
| 5 | m1(Object) + int arg | Autoboxing → Widening |

| From | To | Steps | Valid? |
|---|---|---|---|
| int | long | Widening | ✓ |
| int | Integer | Autoboxing | ✓ |
| int | Long | W→A or A→sibling | ✗ |
| int | Object | A→W | ✓ |
| int | Number | A→W | ✓ |
| long | int | Narrowing | ✗ (loss of precision) |
