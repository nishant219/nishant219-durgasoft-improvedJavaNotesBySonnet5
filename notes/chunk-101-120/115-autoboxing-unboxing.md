# Video 115

## Video info

**Title:** Core Java With OCJP/SCJP: java.lang.package Part-10 || Autoboxing and Unboxing

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP (java.lang package series) |
| Position | 115 of 203 |
| Series | java.lang.package |
| Topic | Autoboxing; autounboxing; -128..127 cache; == on wrappers |
| Instructor | Durga Sir |
| Duration | 1h 17m 44s |
| Video ID | gk1bQSgiBpw |
| Watch | https://www.youtube.com/watch?v=gk1bQSgiBpw |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

### 00:05 — Definitions (formal + intuitive)

**Intuitive (box metaphor — don't say this in interview):**

- Put primitive **inside a box** → autoboxing
- Remove box to get primitive → autounboxing
**Formal interview answer:**

**Autoboxing:** **Automatic conversion of primitive → wrapper object by the compiler** (Java **1.5+**).

**Autounboxing:** **Automatic conversion of wrapper object → primitive by the compiler**.

### 02:01 — Autoboxing example & compiler rewrite

```java
Integer I = 10;  // primitive int assigned to Integer reference — valid from 1.5
```

Compiler rewrites to:

```java
Integer I = Integer.valueOf(10);
```

**Internal implementation:** autoboxing uses **`valueOf()`** methods.

### 07:34 — Autounboxing example & compiler rewrite

```java
Integer I = new Integer(10);
int i = I;  // wrapper → primitive
```

Compiler rewrites to:

```java
int i = I.intValue();
```

**Internal implementation:** autounboxing uses **`xxxValue()`** methods.

**Diagram summary:**

```java
primitive ──(autoboxing / valueOf)──► wrapper object
wrapper object ──(autounboxing / xxxValue)──► primitive
```

### 15:00 — Example 1: static field, method param, assignment chain

```java
class Test {
    static Integer I = 10;           // autoboxing

    public static void main(String[] args) {
        int i = I;                   // autounboxing
        m1(i);                       // autoboxing (int → Integer)
    }

    public static void m1(Integer k) {
        int m = k;                   // autounboxing
        System.out.println(m);
    }
}
```

**Output:** `10`

**Conversion map:**

| Line | Conversion |
|---|---|
| static Integer I = 10 | primitive → wrapper (autoboxing) |
| int i = I | wrapper → primitive (autounboxing) |
| m1(i) | int → Integer (autoboxing) |
| int m = k | Integer → int (autounboxing) |

**Java 1.4:** **4 compile-time errors** (incompatible types throughout).

Compile 1.4 explicitly:

```java
javac -source 1.4 Test.java
# CE: incompatible types found: int required: Integer (and 3 similar)
```

**From 1.5 onward:** valid — primitives and wrappers **interchangeable** where conversion applies.

### 25:26 — Example 2: default values trap (`null` vs `0`)

**Case A — explicit zero:**

```java
class Test {
    static Integer I = 0;
    public static void main(String[] args) {
        int m = I;
        System.out.println(m);
    }
}
```

**Output:** `0`

**Case B — no explicit assignment:**

```java
class Test {
    static Integer I;  // default for object ref = null
    public static void main(String[] args) {
        int m = I;     // autounboxing on null
        System.out.println(m);
    }
}
```

**Runtime:** **`NullPointerException`** (not `0`).

**Rule:** Autounboxing on **`null` reference** → **NPE**.

After compilation, `int m = I` becomes `int m = I.intValue()` — calling method on **null**.

### 32:05 — Example 3: `x++` on wrapper — immutability

```java
class Test {
    public static void main(String[] args) {
        Integer x = 10;
        Integer y = x;
        x++;
        System.out.println(x);           // 11
        System.out.println(y);           // 10
        System.out.println(x == y);      // false
    }
}
```

**Why not 11, 11, true?** All **wrapper objects are immutable** (like String):

- `x++` creates **new** Integer object with value 11
- `x` reassigned to new object
- `y` still points to original **10** object
### 39:36 — Example 4: `==` on Integer — five cases (cache buffer)

```java
// Case 1
Integer x = new Integer(10);
Integer y = new Integer(10);
System.out.println(x == y);  // false — two heap objects via new

// Case 2
Integer x = new Integer(10);
Integer y = 10;              // autoboxing
System.out.println(x == y);  // false — new vs cached/boxed

// Case 3
Integer x = 10;
Integer y = 10;              // both autoboxing
System.out.println(x == y);  // true — same cached object (within range)

// Case 4
Integer x = 100;
Integer y = 100;
System.out.println(x == y);  // true — 100 in -128..127 cache

// Case 5
Integer x = 1000;
Integer y = 1000;
System.out.println(x == y);  // false — outside cache, two objects
```

**Answer key:** `false`, `false`, `true`, `true`, `false`

**Use `equals()` for value comparison; `==` compares references.**

### 52:21 — Internal mechanism: Integer cache buffer at class loading

To support autoboxing efficiently, at **wrapper class loading** a **buffer of pre-created wrapper objects** is created (shown for **`Integer`** static block).

**Default Integer cache range:** **-128 to +127** (256 objects).

**Autoboxing algorithm:**

1. Need Integer object for value `v`
1. JVM checks: is `v` already in buffer?
1. **Yes** → reuse existing object
1. **No** → create **new** object on heap
Hence Case 3 & 4 → **same reference** (`true`); Case 5 → two objects (`false`).

### 59:27 — Buffer applicability by type

| Wrapper | Cache / buffer behavior |
|---|---|
| Byte | Always (entire byte range fits -128..127) |
| Short | -128 to +127 |
| Integer | -128 to +127 |
| Long | -128 to +127 |
| Character | 0 to 127 |
| Boolean | Always (only true and false needed) |
| Float, Double | No buffer — always new objects |

**Outside these ranges:** always **new object** for autoboxing.

### 1:02:45 — Why cache limited to -128..127?

**Memory / performance tradeoff:**

- Extending cache to e.g. -1 crore..+1 crore would force creating **2 crore Integer objects at class loading** — huge memory waste for programs using only a few values
- **-128..127** = commonly used range in real code (0, 10, 100, etc.)
**Why no Float/Double cache?**

- Between **0.0 and 1.0** alone there are **infinite** floating-point values → impossible to buffer
### 1:08:02 — More `==` examples with cache boundaries

```java
Integer x = 127, y = 127;
System.out.println(x == y);  // true — upper bound of cache

Integer x = 128, y = 128;
System.out.println(x == y);  // false — outside cache

Boolean x = false, y = false;
System.out.println(x == y);  // true — Boolean cache always

Double x = 10.0, y = 10.0;
System.out.println(x == y);  // false — no Double cache
```

### 1:12:13 — Buffer applies to `valueOf`, not `new`

Autoboxing implemented via **`valueOf`** → buffer applies to **`valueOf`** too.

**Recommended:** use **`Integer.valueOf(10)`** over **`new Integer(10)`** for performance (reuse).

| Creation style | Cache used? | Typical == same value |
|---|---|---|
| new Integer(10) twice | No | false |
| Autobox 10 twice | Yes (in range) | true |
| Integer.valueOf(10) twice | Yes | true |
| Mixed autobox + valueOf | Yes | true |

```java
Integer a = new Integer(10);
Integer b = new Integer(10);
System.out.println(a == b);  // false

Integer c = 10;
Integer d = 10;
System.out.println(c == d);  // true

Integer e = Integer.valueOf(10);
Integer f = Integer.valueOf(10);
System.out.println(e == f);  // true

Integer g = 10;
Integer h = Integer.valueOf(10);
System.out.println(g == h);  // true
```

**Constructors do NOT participate in cache** — always fresh heap objects.

### 1:17:08 — Session end

Covers autoboxing/autounboxing definitions, compiler transforms, 1.4 vs 1.5, NPE on null unboxing, wrapper immutability with `++`, `==` vs cache, buffer ranges, and **`valueOf` preferred over `new`**.

## ASR decode notes

| Heard | Intended |
|---|---|
| Auto boxing / wer object | autoboxing / wrapper object |
| comper / compar | compiler |
| iphon Source 1.4 | -source 1.4 |
| p jvm / custom jvm | JVM |
| subject / object (buffer context) | object |
| Sun Micro Systems | historical JDK vendor reference |

**Java code block count:** 11
