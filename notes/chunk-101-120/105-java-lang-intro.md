# Video 105

## Video info

**Title:** Core Java With OCJP/SCJP: java.lang.package Part-1 || Introduction

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP (java.lang package series) |
| Position | 105 of 203 |
| Series | java.lang.package |
| Topic | Introduction to java.lang; Object class; toString() |
| Instructor | Durga Sir |
| Duration | 1h 26m 52s |
| Video ID | -qrKA1aWMZs |
| Watch | https://www.youtube.com/watch?v=-qrKA1aWMZs |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

### 00:06 — Series opener: why `java.lang` matters for interviews

Durga Sir opens by saying the next topic is **very important for the interview room** and also for **day-to-day coding**. He normally spends about **one week** on it when time permits.

**Agenda for `java.lang` package (full series roadmap):**

1. Introduction
1. `Object` class
1. `String` class
1. `StringBuffer` class
1. `StringBuilder` class (new in **Java 1.5**)
1. Wrapper classes
1. Autoboxing and autounboxing (also **1.5**)
He stresses: out of all Core Java / SCJP topics, **`java.lang` is priority #1** — not because he says every topic is equally important, but because this package is unavoidable in real programs.

### 00:40 — What is `java.lang`? (ASR: “java dlang” = `java.lang`)

- **`java.lang`** = **Java Language package**
- Contains the most commonly required **classes and interfaces** for writing any Java program — simple or complicated.
**Can you write Java without other packages?**

| Package | Can skip it? |
|---|---|
| java.util | Yes — many programs possible without it |
| java.io | Yes |
| `java.lang` | No — impossible |

Without `java.lang` you cannot:

- Use the **`class`** keyword (every class ultimately ties to `Object`)
- Write **`main(String[] args)`** (`String` is in `java.lang`)
- Use **`System.out.println`** (`System` is in `java.lang`)
### 05:15 — Board definition: grouped fundamentals

**For writing any Java program** (simple or complex), the most commonly required classes and interfaces are grouped into a separate package: **`java.lang`**.

### 11:46 — Special facility: no explicit import for `java.lang`

- We are **not required to import** `java.lang` explicitly.
- **Reason:** all classes/interfaces in `java.lang` are **by default available** to every Java program.
- Contrast: `java.util`, `java.io`, etc. require `import` when used.
**Interview line:** `java.lang` is a **basic requirement concept** for anything in Java.

### 14:15 — Transition to `Object` class

Next major topic: **`Object` class** — the most important first concept inside `java.lang`.

### 15:25 — Every class is a child of `Object`

**Rule:** Every class in Java is a child class of **`Object`** — either **directly** or **indirectly**.

- `String`, `StringBuffer`, `Student`, `Customer`, etc. — all extend `Object` (directly or indirectly).
- Only **`Object`** is the **root** of the Java class hierarchy — not `String`, not `StringBuffer`.
**Why `Object` is root:** It holds the **most commonly required methods** for **any Java object** (`hashCode`, `equals`, etc.). By making every class extend `Object`, those methods become **by default available** to every class.

**Why not make `String` the root?** `String` methods apply only to `String` objects. `Object` methods apply to **any** Java object.

### 23:21 — Interview trap: multilevel inheritance vs “two parents”

```java
class A extends B { }
// B extends Object
```

If interviewer says “A has two parents — B and Object,” clarify:

- This is **multilevel inheritance**, **not** multiple inheritance.
- Java **does not support multiple inheritance with respect to classes** (directly or indirectly).
**Direct vs indirect child of `Object`:**

| Situation | Relationship to Object |
|---|---|
| class A { } — does not extend any other class | Direct child of Object |
| class A extends B { } | Indirect child of Object (via B) |

### 31:43 — How many methods in `Object`? (Interview number: **11**)

**Strictly speaking:** `Object` contains **12** methods, but **`registerNatives()`** is:

```java
private static native void registerNatives()
```

- Internally required by JVM / `Object` class
- **Not available** to child classes
- **Not counted** in the usual “11 methods” answer
**The 11 methods (exam/interview list):**

```java
public String toString()
```

```java
public native int hashCode()
```

```java
public boolean equals(Object obj)
```

```java
protected native Object clone() throws CloneNotSupportedException
```

```java
protected void finalize() throws Throwable
```

```java
public final Class<?> getClass()
```

7–9. `public final void wait()` — **3 overloaded forms**

```java
public final native void notify()
```

```java
public final native void notifyAll()
```

**Reflection demo — count methods at runtime:**

```java
import java.lang.reflect.*;

class C {
    public static void main(String[] args) throws ClassNotFoundException {
        Class c = Class.forName("java.lang.Object");
        Method[] a = c.getDeclaredMethods();
        int count = 0;
        for (Method m1 : a) {
            System.out.println(m1.getName());
            count++;
        }
        System.out.println("The number of methods: " + count);
    }
}
// Prints: getClass, hashCode, equals, clone, toString, notify, notifyAll,
//         wait (x3), finalize, registerNatives
// Output count: 12
```

### 46:05 — `toString()` — purpose

**Purpose:** get **string representation of an object**.

**When invoked automatically:** whenever you **print an object reference**, internally:

```java
System.out.println(s);  // becomes effectively: System.out.println(s.toString());
```

### 50:54 — Default `toString()` behavior demo (`Student` without override)

```java
class Student {
    String name;
    int rollNumber;

    Student(String name, int rollNumber) {
        this.name = name;
        this.rollNumber = rollNumber;
    }

    public static void main(String[] args) {
        Student s1 = new Student("Durga", 101);
        Student s2 = new Student("Ravi", 102);
        System.out.println(s1);           // calls s1.toString()
        System.out.println(s1.toString()); // same
        System.out.println(s2);
    }
}
```

**Output (representative — hash varies by JVM/run):**

```java
Student@8759b751
Student@8759b751
Student@6e1408e
```

- Printing `s1` vs `s1.toString()` → **same output**
- Output is **not** name/rollNumber — it is **`className@hashCodeInHex`**
- Hex portion differs run-to-run / JVM-to-JVM
### 1:03:51 — How `Object.toString()` is implemented (source-level)

Durga Sir shows `Object.java`:

```java
public String toString() {
    return getClass().getName() + "@" + Integer.toHexString(hashCode());
}
```

**Format:** `className + '@' + hashCode in hexadecimal form`

Example decode: `Student@8759b751` → class name `Student`, `@`, then hex of `hashCode()`.

### 1:09:21 — Overriding `toString()` for meaningful output

**Requirement:** when printing a `Student` reference, show **name and roll number**, not `@hex`.

```java
class Student {
    String name;
    int rollNumber;

    Student(String name, int rollNumber) {
        this.name = name;
        this.rollNumber = rollNumber;
    }

    @Override
    public String toString() {
        return name + ".." + rollNumber;  // board: name + ".." + rollNumber
    }

    public static void main(String[] args) {
        Student s1 = new Student("Durga", 101);
        Student s2 = new Student("Ravi", 102);
        System.out.println(s1);
        System.out.println(s2);
    }
}
```

**Output:**

```java
Durga..101
Ravi..102
```

**More formatted override (commented alternative on board):**

```java
@Override
public String toString() {
    return "This is student with the name " + name + " and roll number " + rollNumber;
}
```

**Output:**

```java
This is student with the name Durga and roll number 101
This is student with the name Ravi and roll number 102
```

**Rule:** To provide **our own string representation**, **override `toString()`** in our class — highly recommended.

### 1:16:06 — Who already overrides `toString()`?

```java
class Test {
    public static void main(String[] args) {
        String s = new String("Durga");
        System.out.println(s);                    // Durga — String overrides toString

        Integer i = new Integer(10);
        System.out.println(i);                    // 10 — wrapper overrides toString

        java.util.ArrayList l = new java.util.ArrayList();
        l.add("a");
        l.add("b");
        System.out.println(l);                    // [a, b] — collection overrides

        Test t = new Test();
        System.out.println(t);                    // Test@... — NOT meaningful
    }
}
```

**Summary table:**

| Type | toString() overridden? | Print output |
|---|---|---|
| String | Yes | Content: Durga |
| Wrapper (Integer) | Yes | Content: 10 |
| Collections (ArrayList) | Yes | [a, b] |
| Our class (Test) | No (unless we override) | Test@hex |

After overriding in `Test`:

```java
@Override
public String toString() {
    return "This is the test object";
}
// Prints: This is the test object
```

**Note for all wrapper classes, all collection classes, `String`, `StringBuffer`, `StringBuilder`:** `toString()` is already overridden for meaningful representation — **we should do the same in our classes**.

### 1:25:30 — End of Part-1 (`toString()` completed)

Video ends after completing **`toString()`** as the first of the 11 `Object` methods. Remaining `Object` methods continue in later parts.

## ASR decode notes (this video)

| Heard (caption) | Intended |
|---|---|
| java dlang / java dl / javal | java.lang |
| yul / yut / util (mixed) | sometimes util, sometimes misheard lang — use context |
| ting / to sting | toString |
| ch method | toString method (child class context) |
| object java dt | Object in java.lang |
| vo / av class | every class |
| sh code | hashCode |
| register net / sus method | registerNatives() |
| Greek and Latin | meaningless default toString() output |

**Java code block count:** 9
