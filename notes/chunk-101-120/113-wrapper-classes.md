# Video 113

## Video info

**Title:** Core Java With OCJP/SCJP: java.lang.package Part-8 || wrapper classes

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP (java.lang package series) |
| Position | 113 of 203 |
| Series | java.lang.package |
| Topic | Wrapper classes; wrapper object creation; constructors; valueOf; xxxValue |
| Instructor | Durga Sir |
| Duration | 1h 43m 38s |
| Video ID | UHq63fU4NVU |
| Watch | https://www.youtube.com/watch?v=UHq63fU4NVU |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

### 00:06 — Where we are in `java.lang`

Completed so far: **Object**, **String**, **StringBuffer**, **StringBuilder**.

Next: **Wrapper classes**, then **Autoboxing / Autounboxing** (Java **1.5**).

### 01:19 — What is a wrapper? (English → Java)

**Wrapper** = **cover** (chocolate wrapped in foil).

In Java: wrap a **primitive** so it can be treated as an **object**.

**Purpose:** convert **primitive → object form** to use primitives where only objects are allowed.

### 03:20 — Classic pre-1.5 Collections example

Until **Java 1.4**, collections hold **objects only**, not primitives:

```java
import java.util.*;

class Test {
    public static void main(String[] args) {
        ArrayList l = new ArrayList();
        // l.add(10);  // CE (1.4): required Object, found int

        Integer i = new Integer(10);  // wrap primitive 10
        l.add(i);                     // OK — now Object
    }
}
```

Java is OOP-oriented; **wrapper classes** let us handle primitives **like objects**.

### 05:45 — Two main objectives of wrapper classes

1. **Wrap primitive into object form** so primitives can be handled like objects (Collections, generics, etc.)
1. **Define utility methods** required for primitives (e.g. `Integer.toString(10)`) — primitives have no methods of their own
Example utility:

```java
String s = Integer.toString(10);
// Converts primitive 10 to String — method lives in Integer wrapper class
```

### 11:08 — Eight wrapper classes & constructors overview

**8 wrapper classes:** `Byte`, `Short`, `Integer`, `Long`, `Float`, `Double`, `Character`, `Boolean`

**Almost all** wrapper classes have **two constructors:**

1. Corresponding **primitive** argument
1. Corresponding **`String`** argument
```java
Integer i = new Integer(10);    // int primitive
Integer j = new Integer("10");  // String form
```

Same pattern for `Double`, etc.

### 15:57 — String constructor trap: `NumberFormatException`

If String argument **does not represent a valid number:**

```java
Integer i = new Integer("ten");  // compiles
// Runtime: NumberFormatException
```

### 19:56 — Constructor validity traps (Integer / Float / Double)

**Integer — `long` literal NOT accepted by Integer constructor:**

```java
Integer i = new Integer(10);    // valid
Integer j = new Integer(10L);   // CE — no Integer(int/long) ambiguity; 10L is long
```

**Float — three constructors (exception to “almost all have two”):**

```java
Float f1 = new Float(10.5F);        // float primitive — valid
Float f2 = new Float("10.5F");      // String — valid
Float f3 = new Float(10.5);         // double primitive — valid (Float has double ctor)
// 10.5 without F is double type; Float class accepts float OR String OR double
```

**Double — two constructors:** `double` or `String`

### 25:20 — Character: **only ONE** constructor

```java
Character ch = new Character('a');   // valid — char primitive
Character bad = new Character("a"); // CE — no String constructor in Character
```

**Character class contains only one constructor** — takes **`char` primitive** only.

### 28:29 — Boolean: two constructors + primitive vs String rules

**Primitive constructor** — only **`true`** or **`false`** (lowercase):

```java
Boolean b1 = new Boolean(true);   // valid
Boolean b2 = new Boolean(false);  // valid
Boolean b3 = new Boolean(True);   // CE — True is not boolean primitive
Boolean b4 = new Boolean("true"); // valid String form (different rules)
Boolean b5 = new Boolean("Durga"); // compiles; runtime → false internally
```

### 34:28 — Famous interview MCQ: `Boolean("yes")` vs `Boolean("no")`

```java
Boolean x = new Boolean("yes");
Boolean y = new Boolean("no");
System.out.println(x.equals(y));
```

**Most students guess:** `false` (content differs).

**Actual output:** **`true`**

**Why:** String-argument Boolean constructor rules:

- If content equals **`"true"`** case-insensitively → stored as **true**
- **All other strings** → stored as **false**
So both `x` and `y` internally hold **`false`** → `equals` → **true**.

**Live run (Durga Sir):**

```java
class Test {
    public static void main(String[] args) {
        Boolean x = new Boolean("yes");
        Boolean y = new Boolean("no");
        System.out.println(x);           // false
        System.out.println(y);           // false
        System.out.println(x.equals(y)); // true
    }
}
```

**Board rule — String type Boolean argument:**

- **Case and content both NOT important** (except `true` detection)
- If case-insensitive content equals `"true"` → **true**
- Otherwise → **false**
Examples:

- `"true"`, `"TRUE"`, `"TrUe"` → **true**
- `"yes"`, `"no"`, `"Durga"`, `"Malika"` → **false**
**Contrast — primitive boolean argument:** only **`true`** / **`false`** (case matters — must be lowercase keywords).

### 49:12 — Constructor summary table

| Wrapper | Constructor arguments |
|---|---|
| Byte | byte or String |
| Short | short or String |
| Integer | int or String |
| Long | long or String |
| Float | float, String, or `double` |
| Double | double or String |
| Character | `char` only |
| Boolean | boolean or String (special parsing rules) |

Variations: **Float** (3 ctors), **Character** (1 ctor), **Boolean** (String semantics).

### 51:49 — Printing wrapper refs: `toString()` & `equals()` overridden

In all wrapper classes:

- **`toString()`** overridden → returns **content directly** (`false`, not `Boolean@hex`)
- **`equals()`** overridden → **content comparison**
```java
Boolean x = new Boolean("yes");
System.out.println(x);  // false — not Boolean@hash
```

### 57:03 — Utility method 1: `valueOf()` — purpose

Same goal as **constructors:** create wrapper object from primitive or String.

```java
Integer i = new Integer(10);      // constructor
Integer j = Integer.valueOf(10);  // valueOf — preferred later (autoboxing uses this)
Integer k = Integer.valueOf("10");
```

**Three forms of `valueOf`:**

**Form 1 — String (every wrapper except Character):**

```java
public static Wrapper valueOf(String s)
```

**Form 2 — String + radix (integral wrappers only: Byte, Short, Integer, Long):**

```java
Integer i = Integer.valueOf("1010", 2);  // binary string → decimal 10
System.out.println(i);                   // 10
```

Allowed **radix range: 2 to 36** (digits 0–9, then A–Z for higher bases). **Radix 37** → `NumberFormatException`.

Why max 36? Need distinct digit symbols 0–9 + A–Z.

**Form 3 — primitive (all wrappers including Character):**

```java
Integer i = Integer.valueOf(10);
Character c = Character.valueOf('a');
Boolean b = Boolean.valueOf(true);
```

### 1:24:28 — Utility method 2: `xxxValue()` — wrapper → primitive

Reverse of wrapping: get primitive from wrapper object.

**On Integer (example) — six numeric conversion methods:**

```java
Integer i = new Integer(130);
System.out.println(i.byteValue());   // -126  (internal narrowing cast)
System.out.println(i.shortValue());  // 130
System.out.println(i.intValue());    // 130
System.out.println(i.longValue());   // 130
System.out.println(i.floatValue());  // 130.0
System.out.println(i.doubleValue()); // 130.0
```

**Every number-type wrapper class** (Byte, Short, Integer, Long, Float, Double) contains **these 6 methods** → **6 × 6 = 36** methods.

Plus:

- **Character:** `charValue()`
- **Boolean:** `booleanValue()`
**Total `xxxValue` methods: 38** = `6×6 + 1 + 1`

```java
Character ch = new Character('a');
char c = ch.charValue();  // 'a'

Boolean b = Boolean.valueOf("Durga");  // false internally
boolean bv = b.booleanValue();         // false
```

### 1:43:08 — End of session (mid utility-methods series)

Session ends after **`xxxValue`** summary. Remaining utility methods (`parseXxx`, `toString` static forms) continue in next video(s). Autoboxing follows wrapper utilities in series order.

## ASR decode notes

| Heard | Intended |
|---|---|
| rapper / wer / raer / Apper | wrapper |
| bullan / buan | Boolean |
| care / car | char |
| Ric / radics / radic | radix |
| sh value / in Value | shortValue, intValue |
| PKA / Paka | “100% sure” (Telugu-English) |

**Java code block count:** 17
