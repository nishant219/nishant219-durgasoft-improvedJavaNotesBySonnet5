# Video 114 — `java.lang` Part 9: Wrapper Utility Methods (`parseXXX`, `toString`), Partial Hierarchy, `Void`

## Video info

## Session overview

This is Part 9 of the java.lang wrapper-class series. Video 113 ended after valueOf() and xxxValue(). This session completes the four main wrapper utility method families:

- `valueOf()` — recap (primitive or String → wrapper object)
- `xxxValue()` — recap (wrapper object → primitive)
- `parseXXX()` — String → primitive (new in this video)
- `toString()` — wrapper object or primitive → String (new in this video)
Second half of the session covers:

- A conversion cheat sheet (String ↔ wrapper object ↔ primitive) — interview drill
- Partial hierarchy of java.lang package
- Key conclusions about wrapper classes (final, immutable, inheritance)
- Brief introduction to `Void` class (reflection use case)
## 00:05 — Recap: utility methods covered so far

Durga Sir opens by recalling the first two utility methods from the previous session:

Interview one-liners:

- `valueOf()` → primitive or String to wrapper object
- `xxxValue()` → wrapper object to primitive
## 01:02 — Utility method 3: `parseXXX()`

### Purpose (single word answer)

String → primitive

If you already have a String and want a primitive, use `parseXXX()` — not valueOf().

### Form 1 — `parseXXX(String s)` (decimal string)

Every wrapper class EXCEPT `Character` contains:

```java
public static primitive parseXXX(String s)
```

- Return type = corresponding primitive (int, double, boolean, …)
- Method name = parse + wrapper name (parseInt, parseDouble, parseBoolean, …)
- Argument = String representing a number/value in decimal (default base 10)
Board demo — Form 1 examples:

```java
class ParseForm1Demo {
    public static void main(String[] args) {
        int i = Integer.parseInt("10");
        double d = Double.parseDouble("10.5");
        boolean b = Boolean.parseBoolean("true");

        System.out.println(i);  // 10
        System.out.println(d);  // 10.5
        System.out.println(b);  // true
    }
}
```

Why no `Character.parseChar()`?

Whenever a String argument is involved, `Character` does not participate in the same static-parse pattern. Character wrapper is special (only one constructor taking char; no String-based parse in this family).

Classes with Form 1 `parseXXX(String)`:

Invalid string → runtime exception:

int bad = Integer.parseInt("ten");  // compiles; Runtime: NumberFormatException

### Form 2 — `parseXXX(String s, int radix)` (specified base)

Every integral-type wrapper class contains a second overload:

```java
public static primitive parseXXX(String s, int radix)
```

Integral wrappers only: Byte, Short, Integer, Long

- NOT available for Float / Double (floating-point bases don't apply)
- NOT available for Boolean / Character
Allowed radix range: 2 to 36

- Digits 0–9 for bases ≤ 10
- For bases 11–36, letters A–Z (case-insensitive) represent digit values 10–35
- Radix 37 → NumberFormatException
Why max 36? Need 36 distinct symbols: 0–9 + A–Z.

Board demo — binary string to int:

```java
class ParseForm2Demo {
    public static void main(String[] args) {
        // "1111" in base 2 (binary) = 1+2+4+8 = 15 decimal
        int i = Integer.parseInt("1111", 2);
        System.out.println(i);  // 15
    }
}
```

Another board example (Durga Sir writes on screen):

```java
class ParseRadixDemo {
    public static void main(String[] args) {
        int i = Integer.parseInt("1111", 2);
        System.out.println(i);  // 15

        // Any base 2..36 works:
        int base7 = Integer.parseInt("20", 7);   // 2*7 + 0 = 14
        int base16 = Integer.parseInt("FF", 16); // 255
        System.out.println(base7);   // 14
        System.out.println(base16);  // 255
    }
}
```

Summary — two forms of `parseXXX`:

One-word purpose: parseXXX = String to primitive

## 12:29 — Utility method 4: `toString()`

### Overall purpose

Object (wrapper) or primitive → String

Two directions, four forms total:

### Form 1 — instance `toString()`: wrapper object → String

Every wrapper class, including `Character`, contains:

```java
public String toString()
```

- Instance method (called on wrapper object reference)
- Overrides Object.toString() — in all wrapper classes, overridden to return content directly (not Integer@hashCode)
Board demo — wrapper object to String:

```java
class ToStringForm1Demo {
    public static void main(String[] args) {
        Integer i = new Integer(10);
        String s = i.toString();

        System.out.println(s);  // 10
        System.out.println(i);  // 10 — println calls i.toString() internally
    }
}
```

Key rule — printing wrapper references:

Whenever you print a wrapper object reference (System.out.println(i)), internally `toString()` is called.

```java
class PrintWrapperDemo {
    public static void main(String[] args) {
        Integer i = new Integer(10);
        String s = i.toString();

        System.out.println(s);  // 10
        System.out.println(i);  // 10 — same as i.toString()
    }
}
```

Why output is `10` not `Integer@1a2b3c`:

All wrapper classes override toString() to return the stored value as a String, not the default ClassName@hexHashCode from Object.

Relation to `Object` class:

- Object defines public String toString()
- Every wrapper class overrides it
- This is the overriding version of Object's toString()
### Form 2 — static `toString(primitive)`: primitive → String

Every wrapper class, including `Character`, contains:

```java
public static String toString(primitive p)
```

- Static method — call via class name
- Converts primitive to String (decimal representation by default)
Board demo — primitive to String:

```java
class ToStringForm2Demo {
    public static void main(String[] args) {
        String s1 = Integer.toString(10);
        String s2 = Boolean.toString(true);
        String s3 = Character.toString('a');

        System.out.println(s1);  // 10
        System.out.println(s2);  // true
        System.out.println(s3);  // a
    }
}
```

Contrast Form 1 vs Form 2:

| | Form 1 (instance) | Form 2 (static) |

|--|-------------------|-----------------|

| Input | wrapper object | primitive |

| Call style | obj.toString() | Integer.toString(10) |

| Available in | all wrappers incl. Character | all wrappers incl. Character |

### Form 3 — static `toString(primitive, int radix)`: primitive → radix String

Only two classes: Integer and Long

```java
public static String toString(primitive p, int radix)
```

- Converts primitive to String in the specified base
- Radix range: 2 to 36
Board demo — decimal 15 to binary string:

```java
class ToStringForm3Demo {
    public static void main(String[] args) {
        String s = Integer.toString(15, 2);  // 15 → binary
        System.out.println(s);  // 1111
    }
}
```

More radix examples:

```java
class ToStringRadixDemo {
    public static void main(String[] args) {
        System.out.println(Integer.toString(15, 2));   // 1111  (binary)
        System.out.println(Integer.toString(15, 7));   // 21    (base 7)
        System.out.println(Integer.toString(255, 16)); // ff    (hex)
    }
}
```

NOT available in: Byte, Short, Float, Double, Boolean, Character

### Form 4 — static `toBinaryString` / `toOctalString` / `toHexString`

Only two classes: Integer and Long

Shortcut methods for the three most common bases — no need to pass radix constant:

```java
public static String toBinaryString(primitive p)   // base 2
public static String toOctalString(primitive p)    // base 8
public static String toHexString(primitive p)       // base 16
```

Board demo — all three bases for decimal 10:

```java
class ToStringForm4Demo {
    public static void main(String[] args) {
        System.out.println(Integer.toBinaryString(10));  // 1010
        System.out.println(Integer.toOctalString(10));   // 12
        System.out.println(Integer.toHexString(10));     // a
    }
}
```

Board demo — binary string for 15 (shortcut vs Form 3):

```java
class BinaryStringDemo {
    public static void main(String[] args) {
        // Form 3 — general radix:
        String s1 = Integer.toString(15, 2);
        System.out.println(s1);  // 1111

        // Form 4 — shortcut:
        String s2 = Integer.toBinaryString(15);
        System.out.println(s2);  // 1111
    }
}
```

Octal and hex for 15:

```java
class OctalHexDemo {
    public static void main(String[] args) {
        System.out.println(Integer.toOctalString(15));  // 17
        System.out.println(Integer.toHexString(15));    // f
    }
}
```

Form 4 availability:

Only three bases have dedicated shortcut methods — not arbitrary radix like Form 3.

### Summary — four forms of `toString`

Total purpose in one line: wrapper object or primitive → String

## 34:28 — All four utility methods complete

Durga Sir confirms all four wrapper utility method families are now covered:

## 35:39 — Rapid-fire conversion drill (≤1 second answers)

Durga Sir runs a classroom speed drill. Compulsory clarity for interviews:

### Q&A flash cards

### Conversion diagram (three types dancing)

┌──────────┐
        │  String  │
        └────┬─────┘
             │ parseXXX()          valueOf(String)
             ▼                     ▲
        ┌──────────┐         ┌──────────┐
        │ Primitive│◄───────►│  Wrapper │
        └────┬─────┘ xxxValue│  Object  │
             │    valueOf()  └────┬─────┘
             │ toString(static)   │ toString(instance)
             ▼                     ▼
        ┌──────────┐         ┌──────────┐
        │  String  │         │  String  │
        └──────────┘         └──────────┘

### Complete conversion table

Interview rule: Given any conversion among String, wrapper object, and primitive — answer immediately without hesitation.

## 42:27 — Partial hierarchy of `java.lang` package

Durga Sir draws the partial hierarchy — not every class in java.lang, only what has been covered plus key wrapper structure.

### Hierarchy diagram

java.lang.Object                    ← root of all Java classes
├── String                          ← final
├── StringBuffer                    ← final
├── StringBuilder                   ← final
├── Number                          ← abstract
│   ├── Byte                        ← final wrapper
│   ├── Short                       ← final wrapper
│   ├── Integer                     ← final wrapper
│   ├── Long                        ← final wrapper
│   ├── Float                       ← final wrapper
│   └── Double                      ← final wrapper
├── Boolean                         ← final wrapper (NOT under Number)
├── Character                       ← final wrapper (NOT under Number)
└── Void                            ← final (sometimes treated as wrapper)

Also in `java.lang` but not shown in partial diagram:

- System, Runtime, Exception hierarchy, Thread, etc.
- Diagram is partial — only classes covered in the series so far
### Parent-child clarity table

## 46:44 — Conclusions from partial hierarchy

### Conclusion 1 — Wrappers NOT child of `Number`

Wrapper classes which are NOT child class of `Number`:

- Boolean
- Character
All numeric wrappers (Byte, Short, Integer, Long, Float, Double) extend Number.

### Conclusion 2 — Wrappers NOT direct child of `Object`

Wrapper classes which are NOT direct child class of `Object`:

- Byte, Short, Integer, Long, Float, Double
These extend Number first, then Number extends Object.

Direct children of Object among wrappers: Boolean, Character (and Void).

### Conclusion 3 — Final classes

Final classes (from diagram):

- String, StringBuffer, StringBuilder
- All wrapper classes are final
Cannot subclass any wrapper class.

### Conclusion 4 — Immutability

In addition to `String` objects, all wrapper class objects are also immutable.

- Cannot change the internal value after creation
- Operations like x++ on Integer create new objects (relevant for autoboxing session, Video 115)
```java
class ImmutabilityDemo {
    public static void main(String[] args) {
        Integer x = new Integer(10);
        Integer y = x;       // same reference
        x = new Integer(20); // x points to NEW object; y still holds 10
        System.out.println(y);  // 10
    }
}
```

### Conclusion 5 — `Void` as quasi-wrapper

Some books/sources also consider `Void` class as a wrapper class (debatable — very few members, special purpose).

## 51:05 — `Void` class introduction

### Why discuss `Void`?

- Some interviewers may ask: "Can you explain `Void` class?"
- Unlike String (hours of material) or Object (6–7 hours), Void is small — but worth knowing
- Sometimes treated as wrapper class alongside the eight standard wrappers
### Prototype / API structure

```java
public final class Void extends Object {
    // No methods declared in Void class

    public static final Class<Void> TYPE;
}
```

Properties:

### `Void` = class representation of `void` keyword

Analogy:

Just as Integer wraps int, `Void` is the class representation of the `void` keyword in Java.

### Where is `Void` used? — Reflection

Primary use case: Reflection API — checking whether a method's return type is void or not.

Board demo — reflection check:

```java
import java.lang.reflect.Method;

class VoidReflectionDemo {
    void m1() { System.out.println("void method"); }
    int m2() { return 10; }

    public static void main(String[] args) throws Exception {
        VoidReflectionDemo obj = new VoidReflectionDemo();

        Method method1 = obj.getClass().getMethod("m1");
        Method method2 = obj.getClass().getMethod("m2");

        System.out.println(method1.getReturnType() == Void.TYPE);  // true
        System.out.println(method2.getReturnType() == Void.TYPE);  // false
        System.out.println(method2.getReturnType() == int.class);  // true
    }
}
```

Key comparison:

method.getReturnType() == Void.TYPE   // true if return type is void
method.getReturnType() == void.class  // same — Void.TYPE equals void.class

### `Void` quick facts (interview)

## 59:19 — Session end

Session completes:

- All four wrapper utility methods (valueOf, xxxValue, parseXXX, toString)
- Conversion cheat sheet (String ↔ wrapper ↔ primitive)
- Partial java.lang hierarchy
- Wrapper conclusions (final, immutable, inheritance)
- Brief Void class overview
Next in series: Autoboxing / Autounboxing (Video 115).

## Combined board demo — all utility methods in one program

```java
class WrapperUtilityMethodsDemo {
    public static void main(String[] args) {
        // === valueOf: primitive/String → wrapper ===
        Integer w1 = Integer.valueOf(10);
        Integer w2 = Integer.valueOf("10");

        // === xxxValue: wrapper → primitive ===
        int p1 = w1.intValue();

        // === parseXXX: String → primitive ===
        int p2 = Integer.parseInt("10");
        int p3 = Integer.parseInt("1111", 2);  // 15

        // === toString Form 1: wrapper → String ===
        String s1 = w1.toString();

        // === toString Form 2: primitive → String ===
        String s2 = Integer.toString(10);

        // === toString Form 3: primitive → radix String ===
        String s3 = Integer.toString(15, 2);   // "1111"

        // === toString Form 4: shortcuts ===
        String s4 = Integer.toBinaryString(15); // "1111"
        String s5 = Integer.toOctalString(10);  // "12"
        String s6 = Integer.toHexString(10);    // "a"

        System.out.println("valueOf: " + w1 + ", " + w2);
        System.out.println("xxxValue: " + p1);
        System.out.println("parseInt: " + p2 + ", radix: " + p3);
        System.out.println("toString F1: " + s1);
        System.out.println("toString F2: " + s2);
        System.out.println("toString F3: " + s3);
        System.out.println("toString F4: " + s4 + ", " + s5 + ", " + s6);
    }
}
```

Expected output:

valueOf: 10, 10
xxxValue: 10
parseInt: 10, radix: 15
toString F1: 10
toString F2: 10
toString F3: 1111
toString F4: 1111, 12, a

## Full transcript coverage (timestamp index)

## ASR decode notes (Whisper STT corrections)

## Quick reference card

Wrapper utility methods (4 families)
├── valueOf()        → primitive or String → wrapper object
├── xxxValue()       → wrapper object → primitive
├── parseXXX()
│   ├── Form 1: parseXXX(String)           → decimal String to primitive (all except Character)
│   └── Form 2: parseXXX(String, int radix) → radix String to primitive (Byte, Short, Integer, Long)
└── toString()
    ├── Form 1: instance toString()                    → wrapper object to String (all wrappers)
    ├── Form 2: static toString(primitive)             → primitive to String (all wrappers)
    ├── Form 3: static toString(primitive, int radix)  → primitive to radix String (Integer, Long)
    └── Form 4: toBinaryString / toOctalString / toHexString (Integer, Long)

Conversion cheat sheet
├── String → primitive       : parseXXX()
├── String → wrapper object  : valueOf(String)
├── primitive → wrapper      : valueOf(primitive)
├── wrapper → primitive      : xxxValue()
├── wrapper → String         : toString() instance
└── primitive → String       : toString(primitive) static

java.lang partial hierarchy conclusions
├── NOT under Number: Boolean, Character
├── NOT direct child of Object: Byte, Short, Integer, Long, Float, Double (via Number)
├── All wrappers + String/StringBuffer/StringBuilder: final
├── All wrapper objects: immutable
└── Void: class representation of void; used in Reflection (Void.TYPE)

Radix rules (parseXXX Form 2 and toString Form 3)
└── Allowed range: 2 to 36 (digits 0-9, letters A-Z for 10-35)

## Interview trap questions

## Method availability matrix

### `parseXXX` availability

### `toString` availability

End of Video 114 notes — java.lang Part 9, wrapper utility methods (`parseXXX`, `toString`), partial hierarchy, Void class

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |  |  |
|---|---|---|---|---|---|
| Title | Core Java With OCJP/SCJP: java.lang.package Part-9 \ | \ | wrapper class \ | \ | Utility methods |
| Playlist | Core Java With OCJP/SCJP |  |  |  |  |
| Position | 114 of 203 |  |  |  |  |
| Series | java.lang.package |  |  |  |  |
| Topic | Wrapper utility methods (parseXXX, toString); conversion map; partial java.lang hierarchy; Void class |  |  |  |  |
| Instructor | Durga Sir |  |  |  |  |
| Duration | 59m 51s |  |  |  |  |
| Video ID | pmemJ6QfWjo |  |  |  |  |
| Watch | https://www.youtube.com/watch?v=pmemJ6QfWjo |  |  |  |  |
| Notes source | Local Whisper STT |  |  |  |  |

| Method | Direction | Purpose |
|---|---|---|
| valueOf() | primitive or String → wrapper object | Create wrapper object for given primitive or String |
| xxxValue() | wrapper object → primitive | Get primitive value from wrapper object |

| You have | You want | Method |
|---|---|---|
| String | primitive | parseXXX() |
| String | wrapper object | valueOf(String) |
| primitive | wrapper object | valueOf(primitive) |
| wrapper object | primitive | xxxValue() |

| Wrapper | Method | Example |
|---|---|---|
| Byte | parseByte(String) | Byte.parseByte("10") |
| Short | parseShort(String) | Short.parseShort("10") |
| Integer | parseInt(String) | Integer.parseInt("10") |
| Long | parseLong(String) | Long.parseLong("10") |
| Float | parseFloat(String) | Float.parseFloat("10.5") |
| Double | parseDouble(String) | Double.parseDouble("10.5") |
| Boolean | parseBoolean(String) | Boolean.parseBoolean("true") |
| ~~Character~~ | (none) | — |

| Form | Signature | Available in | Purpose |
|---|---|---|---|
| Form 1 | parseXXX(String s) | All wrappers except Character | Decimal string → primitive |
| Form 2 | parseXXX(String s, int radix) | Byte, Short, Integer, Long only | Radix string → primitive |

| Source | Method kind | Example |
|---|---|---|
| Wrapper object → String | instance toString() | i.toString() |
| Primitive → String | static toString(primitive) | Integer.toString(10) |
| Primitive → radix String | static toString(primitive, radix) | Integer.toString(15, 2) |
| Primitive → binary/octal/hex String | static toBinaryString / toOctalString / toHexString | Integer.toBinaryString(15) |

| Method | Base | Classes |
|---|---|---|
| toBinaryString(p) | 2 | Integer, Long |
| toOctalString(p) | 8 | Integer, Long |
| toHexString(p) | 16 | Integer, Long |

| Form | Signature | Instance/Static | Classes | Purpose |
|---|---|---|---|---|
| 1 | public String toString() | Instance | All wrappers incl. Character | Wrapper object → String |
| 2 | public static String toString(primitive p) | Static | All wrappers incl. Character | Primitive → String (decimal) |
| 3 | public static String toString(primitive p, int radix) | Static | Integer, Long only | Primitive → radix String |
| 4 | toBinaryString / toOctalString / toHexString | Static | Integer, Long only | Primitive → base 2/8/16 String |

| # | Method | Conversion |
|---|---|---|
| 1 | valueOf() | primitive or String → wrapper object |
| 2 | xxxValue() | wrapper object → primitive |
| 3 | parseXXX() | String → primitive |
| 4 | toString() | wrapper object or primitive → String |

| Question | Answer (method) |
|---|---|
| Purpose of parseXXX()? | String → primitive |
| Purpose of valueOf()? | primitive or String → wrapper object |
| Purpose of xxxValue()? | wrapper object → primitive |
| Wrapper object → String? | toString() (instance) |
| String → primitive? | parseXXX() |
| Primitive → wrapper object? | valueOf() |
| Wrapper object → primitive? | xxxValue() |
| Primitive → String? | toString() (static) |
| String → wrapper object? | valueOf(String) |

| From | To | Method |
|---|---|---|
| String | primitive | parseXXX() |
| String | wrapper object | valueOf(String) |
| primitive | wrapper object | valueOf(primitive) |
| wrapper object | primitive | xxxValue() |
| wrapper object | String | toString() (instance) |
| primitive | String | toString(primitive) (static) |

| Class | Direct parent |
|---|---|
| String, StringBuffer, StringBuilder | Object |
| Byte, Short, Integer, Long, Float, Double | Number → Object |
| Boolean, Character, Void | Object |
| Number | Object |

| Property | Value |
|---|---|
| Modifier | public final class |
| Extends | Object (direct child) |
| Methods | None |
| Variables | One only: public static final Class<Void> TYPE |

| Primitive / keyword | Class representation |
|---|---|
| int | Integer |
| boolean | Boolean |
| void | Void |

| Question | Answer |
|---|---|
| How many methods in Void? | Zero |
| How many variables? | One — TYPE |
| Is Void final? | Yes |
| Parent class? | Object |
| Main use? | Reflection — check void return type |
| Relationship to void keyword? | Class representation of void |

| Time | Topic |
|---|---|
| 00:05 | Recap: valueOf() and xxxValue() from previous session |
| 00:34 | Purpose of valueOf() — primitive or String → wrapper object |
| 00:43 | Purpose of xxxValue() — wrapper object → primitive |
| 01:02 | Introduce parseXXX() — third utility method |
| 01:25 | parseXXX purpose: String → primitive |
| 02:36 | Form 1: parseXXX(String) — every wrapper except Character |
| 03:48 | Form 1 signature: public static primitive parseXXX(String s) |
| 06:19 | Examples: Integer.parseInt("10"), Double.parseDouble("10.5"), Boolean.parseBoolean("true") |
| 07:11 | Form 2 introduced — radix overload |
| 07:31 | Binary example: Integer.parseInt("11111", 2) |
| 08:12 | Radix overload only in integral wrappers |
| 08:30 | Radix range 2–36 |
| 09:09 | Form 2: integral types Byte, Short, Integer, Long |
| 10:36 | Form 2 signature: parseXXX(String s, int radix) |
| 11:01 | Example: parseInt("1111", 2) → 15 |
| 11:29 | Two forms of parseXXX complete |
| 12:29 | Introduce toString() — fourth utility method |
| 12:47 | Purpose: wrapper object or primitive → String |
| 13:50 | Form 1: instance toString() — every wrapper incl. Character |
| 14:24 | Demo: Integer i = new Integer(10); String s = i.toString(); |
| 15:01 | Printing wrapper ref internally calls toString() |
| 15:15 | Overrides Object.toString() in all wrapper classes |
| 17:10 | Rule: print wrapper object → toString() called |
| 18:25 | Demo: SOP of s and SOP of i both print 10 |
| 19:34 | Form 1 complete |
| 19:44 | Form 2: static toString(primitive) — primitive → String |
| 20:08 | Demo: Integer.toString(10), Boolean.toString(true) |
| 20:55 | Every wrapper incl. Character has static toString(primitive) |
| 22:32 | Demo: Character.toString('a') |
| 23:09 | Form 3: primitive → specified radix String |
| 23:51 | Radix range 2–36 for toString(primitive, radix) |
| 24:05 | Demo: Integer.toString(15, 2) → "1111" |
| 25:09 | Form 3 only in Integer and Long |
| 28:25 | Form 4: toBinaryString, toOctalString, toHexString |
| 29:04 | Shortcut: Integer.toBinaryString(15) |
| 29:40 | Integer.toOctalString(15) |
| 29:57 | Integer.toHexString(15) |
| 30:23 | Form 4 only for bases 2, 8, 16; only Integer and Long |
| 31:49 | Demo: decimal 10 → binary "1010", octal "12", hex "a" |
| 34:24 | Four forms of toString — summary |
| 34:28 | All four utility methods covered |
| 35:39 | Rapid-fire conversion drill |
| 36:05 | parseXXX = String → primitive |
| 36:16 | valueOf = primitive or String → object |
| 36:31 | xxxValue = wrapper → primitive |
| 36:42 | Wrapper → String = toString |
| 37:14 | Complete conversion map on board |
| 40:45 | Compulsory clarity — no hesitation in interviews |
| 42:27 | Partial hierarchy of java.lang package |
| 43:17 | Object root; String, StringBuffer, StringBuilder |
| 44:03 | Number → Byte, Short, Integer, Long, Float, Double |
| 44:33 | Boolean, Character, Void |
| 44:52 | Partial only — System, Runtime, Exception also in java.lang |
| 46:44 | Conclusion: Boolean, Character not child of Number |
| 47:09 | Conclusion: numeric wrappers not direct child of Object |
| 47:20 | Conclusion: String, StringBuffer, StringBuilder, all wrappers are final |
| 50:05 | Conclusion: all wrapper objects immutable (like String) |
| 51:05 | Void class — sometimes considered wrapper |
| 52:48 | Void prototype: final class, extends Object, no methods |
| 53:37 | One variable: public static final Class<Void> TYPE |
| 55:16 | Void used in Reflection |
| 55:47 | Demo: getReturnType() == Void.TYPE |
| 56:36 | Void = class representation of void keyword |
| 56:53 | Analogy: Integer ↔ int, Void ↔ void |
| 59:19 | Session wrap-up |

| Heard (Whisper) | Intended |
|---|---|
| Parsec-Sex-Ex / parsecsex / parsa xa | parseXXX |
| twisting / two string / dissu-tosing | toString |
| rapper / upper / wer / Apper | wrapper |
| radics / radic / rarix / relics | radix |
| bullion / buan | Boolean |
| Indigida / integer data | Integer |
| Aata / art / octal | octal |
| hexastring / access string | hex string |
| immiotable | immutable |
| j-le / chaili / chile | child |
| wired / y by / VIDE | Void |
| ATMAT / atima type | Void.TYPE |
| reflections / reflections | Reflection API |
| string of buffer / string of builder | StringBuffer / StringBuilder |
| popcorn class | (unclear — ignore) |
| keep sabading | keep studying / write in notes |

| Trap | Correct answer |
|---|---|
| String "10" to int 10 | Integer.parseInt("10") — not valueOf (that gives Integer object) |
| int 10 to "10" | Integer.toString(10) — static method |
| Integer object to "10" | i.toString() — instance method |
| Which class has no parseXXX(String)? | Character |
| Which classes have radix parseXXX? | Byte, Short, Integer, Long only |
| Which classes have toString(primitive, radix)? | Integer, Long only |
| Print Integer ref — what method runs? | toString() (overridden) |
| Are wrapper classes final? | Yes — all eight |
| Are wrapper objects mutable? | No — immutable like String |
| Boolean/Character parent? | Object directly (not Number) |
| Integer parent? | Number → Object |
| What is Void.TYPE? | Class<Void> constant for void return type checks |
| How many methods in Void? | Zero |

| Wrapper | parseXXX(String) | parseXXX(String, radix) |
|---|---|---|
| Byte | ✓ | ✓ |
| Short | ✓ | ✓ |
| Integer | ✓ | ✓ |
| Long | ✓ | ✓ |
| Float | ✓ | ✗ |
| Double | ✓ | ✗ |
| Boolean | ✓ | ✗ |
| Character | ✗ | ✗ |

| Wrapper | instance toString() | static toString(p) | static toString(p, radix) | toBinary/Octal/HexString |
|---|---|---|---|---|
| Byte | ✓ | ✓ | ✗ | ✗ |
| Short | ✓ | ✓ | ✗ | ✗ |
| Integer | ✓ | ✓ | ✓ | ✓ |
| Long | ✓ | ✓ | ✓ | ✓ |
| Float | ✓ | ✓ | ✗ | ✗ |
| Double | ✓ | ✓ | ✗ | ✗ |
| Boolean | ✓ | ✓ | ✗ | ✗ |
| Character | ✓ | ✓ | ✗ | ✗ |
