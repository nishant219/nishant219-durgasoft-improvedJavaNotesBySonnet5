# Video 103

## Video info

**Title:** Core Java With OCJP/SCJP: Innerclass  Part- 4||normal java class vs inner class

| Field | Value |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | 103 of 203 |
| Series | Inner Classes · Part 4 |
| Topic | Normal Java class vs anonymous inner class; GUI event handling; static nested classes |
| Instructor | Durga Sir |
| Duration | 1h 13m 48s |
| Video ID | yB7dt-DDOgI |
| Watch | https://www.youtube.com/watch?v=yB7dt-DDOgI |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

### 00:03 — Recap: three types of anonymous inner classes

Previous session covered **anonymous inner classes** — three categories:

1. Anonymous class that **extends** a class
1. Anonymous class that **implements** an interface
1. Anonymous class defined **inside method arguments**
This session: **Normal Java class vs anonymous inner class**, then introduces **static nested classes** (4th type).

### 00:44 — Normal Java class vs anonymous inner class

Topic heading: **Normal Java class vs Anonymous inner class** — small behavioral differences.

### 01:19 — Difference 1: extends only one class (SAME)

**Normal Java class:**

```java
class A extends B { }
```

A normal class can extend **only one class** at a time.

**Anonymous inner class extending a class:**

```java
Popcorn p = new Popcorn() { };
// writing a class that extends Popcorn — only one superclass
```

```java
Thread t = new Thread() { };
// anonymous class extends Thread — only one class
```

**Conclusion:** Both normal and anonymous can extend **only one class** — **no difference** on this point.

### 02:29 — Difference 2: implementing interfaces (DIFFERENT)

**Normal Java class:**

```java
class A implements B, C, D { }
// any number of interfaces simultaneously
```

**Anonymous inner class:**

```java
Runnable r = new Runnable() {
    public void run() { }
};
// writing a class that implements Runnable — only ONE interface
```

**Conclusion:**

| | Normal Java class | Anonymous inner class |

|--|-------------------|----------------------|

| Implements interfaces | **Any number** | **Only one** |

### 03:37 — Difference 3: extend + implement simultaneously (DIFFERENT)

**Normal Java class — valid:**

```java
class A extends B implements C, D, E { }
// extend one class AND implement any number of interfaces — valid
```

**Anonymous inner class:**

Can **extend a class** OR **implement an interface** — **not both simultaneously** (only one "slot").

**Conclusion:**

| | Normal Java class | Anonymous inner class |

|--|-------------------|----------------------|

| Extend + implement together | Yes | **No** — one or the other |

### 04:48 — Board summary: first three points

1. Normal class extends **one** class; anonymous also extends **one** class → **same**
1. Normal class implements **any number** of interfaces; anonymous implements **one** → **different**
1. Normal class can extend + implement together; anonymous **cannot** → **different**
### 08:35 — Difference 4: constructors

**Normal Java class:**

```java
class Test {
    Test() { }
    Test(int i) { }
    // any number of constructors — valid
}
```

**Anonymous inner class:**

```java
Thread t = new Thread() {
    // Thread() { }  // CE: cannot write constructor — no class name
};
```

**Rule:** Constructor name must match class name. Anonymous inner class has **no name** → programmer **cannot write any constructor explicitly**.

- Compiler may generate constructors calling super — but **at programmer level**, constructor concept **not applicable**
- Must depend on **parent class constructor** only, e.g. `new Thread() { }` calls `Thread()` super constructor
**Conclusion:**

| | Normal Java class | Anonymous inner class |

|--|-------------------|----------------------|

| Constructors | Any number explicitly | **Cannot write** explicitly |

### 12:30 — When to use normal vs anonymous

**Normal top-level class** — when:

- Requirement is **standard**
- Required **several times** (reused across application)
**Anonymous inner class** — when:

- Requirement is **temporary**
- Required **only once** (instant / one-time use)
### 15:12 — Best suitable area: GUI event handling

Anonymous inner classes are **best suitable** in **GUI-based applications** for **event handling**.

Example: ATM-style screen with buttons — Withdraw, Get Balance, Change PIN, Mini Statement. Each button needs **different one-time behavior** tied to that button only.

### 17:31 — GUI example: `MyGUIFrame` with ActionListener

```java
import javax.swing.*;
import java.awt.event.*;

class MyGUIFrame extends JFrame {
    JButton b1, b2, b3, b4, b5, b6;
    // ... frame setup ...

    void setupListeners() {
        b1.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // B1-specific functionality only
            }
        });

        b2.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // B2-specific functionality only
            }
        });
    }
}
```

**Without anonymous classes:** Need separate top-level classes:

```java
class MyActionListener1 implements ActionListener { ... } // for B1
class MyActionListener2 implements ActionListener { ... } // for B2
// one top-level class per button — unnecessary
```

**With anonymous classes:** Define B1 logic right at `b1.addActionListener(...)`, B2 logic at `b2.addActionListener(...)` — **one top-level GUI class** suffices.

**Board note:** `ActionListener` is an **interface**; `ActionEvent` relates to event classes. Pattern same as `new Runnable() { ... }`.

### 26:41 — Live demo: `JarDemo.java` (WindowAdapter)

```java
import java.awt.*;
import java.awt.event.*;

class JarDemo {
    public static void main(String[] args) {
        Frame f = new Frame();
        f.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                for (int i = 1; i <= 10; i++) {
                    System.out.println("closing window");
                }
                System.exit(0);
            }
        });
        f.add(new Label("I can create executable jar file"));
        f.setSize(300, 200);
        f.setVisible(true);
    }
}
// On window close: prints "closing window" ten times, then JVM shuts down
```

**What this is:** Anonymous inner class that **extends** `WindowAdapter` (class, not interface).

**Demo flow:**

1. `javac JarDemo.java` — compiles
1. `java JarDemo` — window appears with label text
1. Close window → `windowClosing` fires → prints "closing window" 10 times → `System.exit(0)`
**Takeaway:** GUI apps use anonymous inner classes **frequently** for event handling — no long explanation needed beyond seeing the pattern.

### 30:51 — Fourth type: static nested classes

After normal, method-local, and anonymous — **fourth category:**

**Static nested classes**

### 31:16 — Why "nested" instead of "inner"?

Terminology shift is **intentional**, not accidental.

**Analogy with variables:**

```java
class Test {
    int x = 10;        // instance variable — exists only with object
    static int y = 20; // static variable — may exist without object
}
```

- Instance variable: no `Test` object → no `x`
- Static variable: `Test` class loaded → `y` may exist without any object
**Apply same logic to nested types:**

```java
class Outer {
    class Inner { }           // non-static inner — like instance variable
    static class Nested { }   // static nested — like static member
}
```

| Type | Association with outer object |
|---|---|
| Normal inner class | Without outer object → no inner object. Inner object strongly associated with outer object |
| Static nested class | Without outer object → may create nested object. Not strongly associated with outer object |

**Definition:** Inner class declared with **`static`** modifier → **static nested class**.

"**Nested**" = class physically inside another class, but **no strong lifecycle binding** to outer instance (like static members).

### 33:57 — First property: creating static nested object without outer object

```java
class Outer {
    static class Nested {
        public void m1() {
            System.out.println("static nested class method");
        }
    }

    public static void main(String[] args) {
        Nested n = new Nested(); // no Outer object required
        n.m1();
    }
}
// prints static nested class method
```

Compare to normal inner class — would require:

```java
Outer o = new Outer();
Outer.Inner i = o.new Inner();
```

**Internally** compiler still generates `Outer$Nested.class` — don't worry about bytecode name at usage time.

**From outside outer class:**

```java
Outer.Nested n = new Outer.Nested();
n.m1();
```

Static member access pattern: **`OuterClassName.NestedType`**.

### 43:46 — Live compile/run (class renamed `Test` on board)

```java
class Test {
    static class Nested {
        public void m1() {
            System.out.println("static nested class method");
        }
    }

    public static void main(String[] args) {
        Nested n = new Nested();
        n.m1();
    }
}
// prints static nested class method
```

Within same outer class, class name prefix optional for static nested type: `Nested n = new Nested();`

### 48:57 — Second difference: static members allowed (including `main`)

**Normal inner class:**

```java
class Outer {
    class Inner {
        static int x = 10; // CE: Inner classes cannot have static declarations
    }
}
```

**Static nested class:**

```java
class Test {
    static class Nested {
        public static void main(String[] args) {
            System.out.println("static nested class main method");
        }
    }

    public static void main(String[] args) {
        System.out.println("outer class main method");
    }
}
```

**Running from command prompt:**

```java
javac Test.java
java Test
# prints outer class main method

java Test$Nested
# prints static nested class main method
```

**Rules:**

- Normal inner class → **cannot** declare static members → **cannot** declare `main` → **cannot** run inner class directly from command prompt
- Static nested class → **can** declare static members including `main` → invoke with **`java OuterClass$NestedClass`**
### 51:32 — Live demo of dual main

Compiled `Test.java`:

- `java Test` → **outer class main method**
- `java Test$Nested` → **static nested class main method**
Confirmed on execution.

### 56:37 — Third difference: accessing outer class members

**Normal inner class** — can access **both** static and non-static outer members directly.

**Static nested class** — static context → **only static** outer members:

```java
class Test {
    int x = 10;
    static int y = 20;

    static class Nested {
        public void m1() {
            System.out.println(x); // CE: non-static variable x cannot be referenced from a static context
            System.out.println(y); // prints 20
        }
    }
}
// CE: non-static variable x cannot be referenced from a static context
```

Live compile confirmed exact CE message.

### 58:41 — Board rules: member access comparison

**From normal/regular inner class:**

- Access **both** static and non-static members of outer class **directly**
**From static nested class:**

- Access **only static** members of outer class directly
- **Cannot** access non-static (instance) members directly
### 1:03:15 — Summary table: normal inner vs static nested

Durga Sir builds comparison table — **four rows:**

| # | Normal / regular inner class | Static nested class |
|---|---|---|
| 1. Object without outer instance | Without outer object → no inner object. Inner object strongly associated with outer object | Without outer object → may exist nested object. Not strongly associated with outer |
| 2. Static members inside | Cannot declare static members | Can declare static members |
| 3. main / command prompt | Cannot declare main; cannot invoke inner class directly from command prompt | Can declare main; invoke with java Outer$Nested |
| 4. Access outer members | Both static and non-static directly | Only static directly; non-static → CE |

### 1:05:20 — Table completion (board dictation)

Full table written point-by-point on board for exam revision — same four conclusions as above, expanded in sentence form for each column.

### 1:13:17 — Closing: four types of inner classes complete

With static nested classes, all **four types** covered:

1. Normal / regular inner class
1. Method-local inner class
1. Anonymous inner class
1. Static nested class
Session ends after differences table between normal inner and static nested.

**Java block count:** 20
