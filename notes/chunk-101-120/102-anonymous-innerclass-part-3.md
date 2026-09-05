# Video 102

## Video info

| Field | Value |  |  |
|---|---|---|---|
| Title: | Core Java With OCJP/SCJP: Innerclass Part-3 \ | \ | anonymous inner class |
| Position | 102 of 203 |  |  |
| Series | Inner Classes · Part 3 |  |  |
| Instructor | Durga Sir |  |  |
| Duration | 1h 31m 18s |  |  |
| Video ID | QSvPY-Y71-k |  |  |
| Watch | https://www.youtube.com/watch?v=QSvPY-Y71-k |  |  |
| Playlist | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |  |  |
| Notes source | Local Whisper STT |  |  |

### 00:03 — Session opening: third category of inner classes

Up to this point in the inner-class series, **two categories** were already covered:

1. **Normal / regular inner class**
1. **Method-local inner class**
The **third category** — and the most valuable, most repeatedly used — is **Anonymous Inner Classes**.

### 00:32 — What is an Anonymous Inner Class?

**Definition:** An inner class **without a name**.

- Sometimes we can declare an inner class **without giving it a name**.
- Such nameless inner classes are called **Anonymous Inner Classes**.
**Immediate doubt:** *Without a name, how can we access or use it?*

Answer: There is a clear usage pattern — discussed next.

### 01:10 — Real-life analogy: one-time help, no contact details

**Scenario (Canara Bank / demo-class analogy):**

- You ask someone on the road: *"Where is Canara Bank building?"*
- He replies: *"Two minutes walk, right-hand side."*
- You find the building, attend the demo — but you **never ask his name, mobile number, or address**.
**Why?** Because you need him **only once** — instant use, one-time usage. You are not going to meet him again in your life, so there is **no need to record his contact information**.

**Same idea in Java:** Classes created purely for **instant / one-time use** do not need a permanent name → **Anonymous Inner Classes**.

### 05:04 — Bus conductor analogy (reinforcement)

- You travel by city bus, buy a ticket from the conductor, get down at your stop.
- You never ask the conductor's name, mobile, or email.
- **Tomorrow** another conductor will be on a different bus — you use whoever is available **at that moment**.
- If you tried to permanently "recruit" a conductor for a one-time trip, it would be meaningless.
**Conclusion:** One-time-usage classes → **anonymous** (nameless).

### 05:22 — Two anonymous constructs in Java

In Java there are **two** anonymous constructs:

1. **Anonymous inner class**
1. **Anonymous array** *(covered elsewhere)*
### 05:31 — Main purpose of Anonymous Inner Classes

> **Just for instant use / one-time usage.**

Not for permanent, repeated use.

### 08:18 — Three types of Anonymous Inner Classes

| # | Type | Declaration form |
|---|---|---|
| 1 | Anonymous inner class that extends a class | new SuperClass() { ... } |
| 2 | Anonymous inner class that implements an interface | new InterfaceName() { ... } |
| 3 | Anonymous inner class defined inside arguments | Passed directly as a method argument |

Based on **declaration / behavior**, there are exactly **three** categories.

### 12:36 — New syntax introduction (critical)

Sir emphasizes: **some new syntax** appears here. Take special care — once this syntax is clear, anonymous inner classes become easy.

### 12:56 — Syntax pattern 1: extends `Popcorn`

Normal object creation:

```java
Popcorn p = new Popcorn();  // CE: OK — creates Popcorn object
```

Anonymous inner class syntax (extends a class):

```java
Popcorn p = new Popcorn() {   // CE: OK — anonymous subclass of Popcorn
};                             // semicolon AFTER closing brace — mandatory
```

**What happens (two activities):**

1. A **nameless class** is declared that **extends `Popcorn`**.
1. An **object of that child class** is created, held by a **parent reference** (`Popcorn p`).
**Key twist:** Even though `new Popcorn()` appears, it is **NOT** a plain Popcorn object — it is a **child-class object** with **parent reference**.

### 15:37 — Syntax pattern 2: extends `Thread`

Normal:

```java
Thread t = new Thread();  // CE: OK
```

Anonymous (extends Thread):

```java
Thread t = new Thread() {  // CE: OK — anonymous subclass of Thread
};
```

Same two activities: declare unnamed class extending `Thread`, create child object with parent reference.

### 17:13 — Syntax pattern 3: implements `Runnable`

```java
Runnable r = new Runnable();  // CE: cannot instantiate interface
```

**Why semicolon alone fails:** `Runnable` is an **interface** — you cannot create an object with `new Runnable();` alone.

Correct anonymous form:

```java
Runnable r = new Runnable() {  // CE: OK — anonymous class implementing Runnable
    public void run() { }
};
```

**What happens:**

1. A nameless class **implements `Runnable`**.
1. Object of that implementing class is created with **interface reference**.
**Summary of three syntax demos:**

| Reference type | Syntax | Actual object type |
|---|---|---|
| Popcorn p | new Popcorn() { } | Child class object (anonymous subclass) |
| Thread t | new Thread() { } | Child class object (anonymous subclass) |
| Runnable r | new Runnable() { } | Implementing class object (anonymous) |

### 19:17 — Category 1 deep dive: Anonymous inner class that **extends a class**

Recap points before the Popcorn example:

- Anonymous inner class = inner class **without name**
- Purpose = **instant / one-time use**
- Three types: extends class, implements interface, inside arguments
### 21:46 — `Popcorn` base class (board)

`Popcorn` is a class with a `taste()` method (and ~100 other methods in the real-world analogy):

```java
class Popcorn {
    public void taste() {
        System.out.println("salty");  // default salty implementation
    }
    // ... ~100 more methods available as-is ...
}
```

**Movie-theatre context:** Popcorn at big cinemas can cost ₹450–500 for 2 cokes + 3 popcorns (~₹100–150 each). Default taste printed: **salty**.

### 24:34 — When overriding is needed

**Requirement:** Popcorn functionality is needed, but **not** the default salty `taste()` — want **spicy** instead. All other ~100 methods should remain unchanged.

**Permanent requirement → named top-level child class:**

```java
class SpicyPopcorn extends Popcorn {
    public void taste() {
        System.out.println("spicy");  // override only taste()
    }
    // remaining 100 methods inherited from Popcorn as-is
}
```

- People wanting **salty** → `new Popcorn()` and call methods.
- People wanting **spicy** → `new SpicyPopcorn()` and call methods.
- This is classic **method overriding**.
**Problem:** If spicy taste is needed **only once**, creating a separate top-level class is **not recommended** — like buying a bus for a once-in-five-months trip, or hiring a permanent doctor for a once-a-year fever.

### 27:51 — One-time vs permanent requirement (decision rule)

| Requirement | Approach |
|---|---|
| Permanent — needed several times, by many people | Top-level named class |
| Temporary / one-time — needed only once, at one place | Anonymous inner class at that exact location |

### 28:15 — Full `Test` class: spicy via anonymous inner class

```java
class Test {
    public static void main(String[] args) {
        // One-time spicy requirement — anonymous inner class
        Popcorn p = new Popcorn() {
            public void taste() {
                System.out.println("spicy");  // override taste() only
            }
        };  // end anonymous class + object creation

        p.taste();  // prints: spicy  (overriding method runs — child object via parent ref)
    }
}
```

**Polymorphism / overriding:** Parent reference `p` holds child object → `p.taste()` invokes **overridden spicy** implementation.

**Output:** `spicy`

### 30:42 — Salty: normal Popcorn object

Student asks: *What if I want salty (default), not spicy?*

```java
Popcorn p1 = new Popcorn();
p1.taste();  // prints: salty
```

Normal Popcorn object → Popcorn class `taste()` method → **salty**.

### 31:18 — Sweet: second anonymous inner class (one-time)

Sweet taste is also a **one-time requirement** → anonymous inner class again:

```java
Popcorn p2 = new Popcorn() {
    public void taste() {
        System.out.println("sweet");
    }
};
p2.taste();  // prints: sweet
```

### 32:38 — Complete program on screen (compile & run)

Full combined program Sir runs (`Test.java`):

```java
class Popcorn {
    public void taste() {
        System.out.println("salty");
    }
    // 100+ more methods exist conceptually
}

class Test {
    public static void main(String[] args) {
        // Anonymous — spicy (one-time)
        Popcorn p = new Popcorn() {
            public void taste() {
                System.out.println("spicy");
            }
        };
        p.taste();  // → spicy

        // Normal Popcorn — salty
        Popcorn p1 = new Popcorn();
        p1.taste();  // → salty

        // Anonymous — sweet (one-time)
        Popcorn p2 = new Popcorn() {
            public void taste() {
                System.out.println("sweet");
            }
        };
        p2.taste();  // → sweet
    }
}
```

**Compile:** `javac Test.java` — CE: OK

**Run:** `java Test`

**Output (in order):**

```java
spicy
salty
sweet
```

### 34:41 — Decision recap: top-level class vs anonymous

- **Permanent requirement, several times** → top-level class
- **One-time / temporary requirement, only once** → anonymous inner class
### 35:06 — How many `.class` files are generated?

For the program above, **four** `.class` files:

| Generated file | For what |
|---|---|
| Popcorn.class | Popcorn class |
| Test.class | Test class (outer class) |
| Test$1.class | 1st anonymous inner class in Test (spicy) |
| Test$2.class | 2nd anonymous inner class in Test (sweet) |

**Naming rule:** Anonymous inner classes get compiler-generated names:

- Format: **`OuterClass$N.class`**
- `N` = sequential number (1, 2, 3, …) for each anonymous class **within that outer class**
- No human-readable name exists for the inner class itself
**Mapping:**

- `p` (spicy anonymous) → object of class **`Test$1`**, NOT plain `Popcorn`
- `p1` (normal) → object of class **`Popcorn`**
- `p2` (sweet anonymous) → object of class **`Test$2`**
### 38:33 — Proving runtime class names with `getClass().getName()`

Sir adds SOP lines to show actual classes programmatically:

```java
class Popcorn {
    public void taste() {
        System.out.println("salty");
    }
}

class Test {
    public static void main(String[] args) {
        Popcorn p = new Popcorn() {
            public void taste() {
                System.out.println("spicy");
            }
        };
        Popcorn p1 = new Popcorn();
        Popcorn p2 = new Popcorn() {
            public void taste() {
                System.out.println("sweet");
            }
        };

        p.taste();   // spicy
        p1.taste();  // salty
        p2.taste();  // sweet

        System.out.println(p.getClass().getName());   // Test$1
        System.out.println(p1.getClass().getName());  // Popcorn
        System.out.println(p2.getClass().getName());  // Test$2
    }
}
```

**Output:**

```java
spicy
salty
sweet
Test$1
Popcorn
Test$2
```

**Key insight:** `Popcorn p = new Popcorn() { ... }` — reference type is `Popcorn`, but **runtime object class** is `Test$1` (anonymous subclass).

### 47:10 — Analysis board: three activities in full anonymous + override code

For the complete spicy example:

```java
Popcorn p = new Popcorn() {
    public void taste() {
        System.out.println("spicy");
    }
};
```

**Three activities:**

1. **Declare** a class that extends `Popcorn` **without a name** → **anonymous inner class**
1. **Override** `taste()` method inside that class
1. **Create an object** of that child class with **parent reference** (`Popcorn p`)
### 48:08 — Analysis board: two activities in empty-body anonymous

For syntax without override:

```java
Popcorn p = new Popcorn() {
};
```

**Two activities:**

1. Declare anonymous class extending `Popcorn` (no name)
1. Create child object with parent reference
### 53:21 — Multithreading + Anonymous Inner Classes (exam-hot topic)

Sir states: **Multi-threading and anonymous inner classes** is a **very common exam combination** — must know clearly.

**Two ways to define a thread:**

1. By **extending `Thread` class**
1. By **implementing `Runnable` interface**
Both will be shown with **normal class approach** and **anonymous inner class approach**.

### 54:15 — Normal class approach: extend `Thread`

**Step 1 — Define thread by extending Thread:**

```java
class MyThread extends Thread {
    public void run() {
        for (int i = 0; i < 10; i++) {
            System.out.println("child thread");
        }
    }
}
```

- Write a class extending `Thread`
- Override `run()` method
- Code inside `run()` = **job of the thread**
**Step 2 — Use in demo:**

```java
class ThreadDemo {
    public static void main(String[] args) {
        MyThread t = new MyThread();  // main thread creates child thread object
        t.start();                     // main thread starts child thread

        for (int i = 0; i < 10; i++) {
            System.out.println("main thread");
        }
    }
}
```

**After `t.start()`:** **Two threads** — main thread + child thread.

- **Child thread** → executes `run()` job (prints "child thread")
- **Main thread** → executes remaining code (prints "main thread")
- Both run **simultaneously** → **mixed / interleaved output** (order not guaranteed)
Example mixed output pattern: `main thread`, `child thread`, `child thread`, `main thread`, …

### 58:47 — Anonymous inner class approach: extend `Thread` (one-time job)

If the thread job is **temporary / one-time only**, do **not** create top-level `MyThread` — use anonymous inner class:

```java
class ThreadDemo {
    public static void main(String[] args) {
        Thread t = new Thread() {           // anonymous class extends Thread
            public void run() {
                for (int i = 0; i < 10; i++) {
                    System.out.println("child thread");
                }
            }
        };                                   // end anonymous class + object

        t.start();                           // now 2 threads

        for (int i = 0; i < 10; i++) {
            System.out.println("main thread");
        }
    }
}
```

**Same pattern as Popcorn:** extends class without name, optionally override method (`run` here), create object with parent reference, use immediately.

Sir also writes equivalent in `Test.java` and runs it — mixed output observed; exact order varies on each run due to thread scheduling.

### 1:02:12 — Runnable anonymous preview (extends Thread run demo)

Executed `Test.java` with anonymous `Thread` — output interleaves `child thread` and `main thread` lines; not always same order each execution.

### 1:05:34 — Normal vs Anonymous thread-defining approaches (summary)

| Approach | When |
|---|---|
| Normal class approach | Permanent job, reused many times |
| Anonymous inner class approach | Temporary / one-time job |

Both must be known for the exam.

### 1:09:23 — Category 2: Anonymous inner class that **implements an interface**

Second type: **Anonymous inner class that implements an interface**.

Example chosen: **Defining a thread by implementing `Runnable` interface**.

### 1:10:48 — Normal class approach: implement `Runnable`

**Step 1 — `MyRunnable` class:**

```java
class MyRunnable implements Runnable {
    public void run() {
        for (int i = 0; i < 10; i++) {
            System.out.println("child thread");
        }
    }
}
```

- `Runnable` interface has one method: `run()`
- Provide implementation in `run()`
**Step 2 — `ThreadDemo` using Runnable:**

```java
class ThreadDemo {
    public static void main(String[] args) {
        MyRunnable r = new MyRunnable();   // Runnable target object (like a "car")
        Thread t = new Thread(r);          // Thread "drives" the Runnable — has start()
        t.start();                         // 2 threads after start

        for (int i = 0; i < 10; i++) {
            System.out.println("main thread");
        }
    }
}
```

**Key multithreading concepts (recap):**

- `MyRunnable` object alone has **no `start()`** — like a car without a driver
- **`Thread` class** has `start()` capability
- `new Thread(r)` → thread will execute **`r.run()`** as its job when started
- `r` = **target Runnable**
**Output:** Mixed — main thread + child thread interleaved.

### 1:15:08 — Anonymous inner class approach: implement `Runnable`

One-time temporary job → anonymous `Runnable`:

```java
class ThreadDemo {
    public static void main(String[] args) {
        Runnable r = new Runnable() {        // anonymous class implements Runnable
            public void run() {
                for (int i = 0; i < 10; i++) {
                    System.out.println("child thread");
                }
            }
        };                                   // Runnable target ready

        Thread t = new Thread(r);            // wrap with Thread for start()
        t.start();

        for (int i = 0; i < 10; i++) {
            System.out.println("main thread");
        }
    }
}
```

**Common student doubt:** `Runnable r = new Runnable() { ... }` — is this a Runnable object or implementing-class object?

**Answer:** It is an **implementing-class object** (anonymous), held by **interface reference** `Runnable r`. You cannot do `new Runnable();` alone (interface), but anonymous class body makes it valid.

### 1:18:28 — Runnable anonymous demo in `Test.java` (executed)

Sir writes and runs in `Test.java` with labels `child thread 1` / `main thread 1` for clarity:

```java
class Test {
    public static void main(String[] args) {
        Runnable r = new Runnable() {
            public void run() {
                for (int i = 0; i < 10; i++) {
                    System.out.println("child thread 1");
                }
            }
        };

        Thread t = new Thread(r);
        t.start();

        for (int i = 0; i < 10; i++) {
            System.out.println("main thread 1");
        }
    }
}
```

**CE:** OK. **Output:** Mixed; example run showed interleaved main/child lines.

### 1:20:11 — Category 2 summary

Both options for Runnable-based threads:

1. **Normal class approach** — `class MyRunnable implements Runnable`
1. **Anonymous inner class approach** — `new Runnable() { public void run() { ... } }`
Core concept: **Anonymous class that implements an interface**.

### 1:23:38 — Category 1 (Thread extends) completed; transition to Category 3

By extending `Thread` class — completed.

### 1:23:59 — Category 3: Anonymous inner class **defined inside arguments**

Third type: **Anonymous inner class that is defined inside arguments** — declared **directly as a method argument**, not stored in a separate variable first.

### 1:24:37 — Same Runnable example, inlined into `Thread` constructor

Instead of:

```java
Runnable r = new Runnable() { ... };
Thread t = new Thread(r);
t.start();
```

**Inline inside the argument of `new Thread(...)`:**

```java
class ThreadDemo {
    public static void main(String[] args) {
        new Thread(new Runnable() {          // anonymous Runnable passed as argument
            public void run() {
                for (int i = 0; i < 10; i++) {
                    System.out.println("child thread");
                }
            }
        }).start();                          // .start() chained on same statement

        for (int i = 0; i < 10; i++) {
            System.out.println("main thread");
        }
    }
}
```

**What happens:**

1. Anonymous class implementing `Runnable` is declared **inside the constructor argument**
1. Object created and **passed directly** to `Thread` constructor
1. `.start()` called immediately via chaining
1. After `start()` → **2 threads** (main + child)
1. Child executes `run()`; main executes the for-loop
Sir notes: code looks unusual but is **perfectly valid, acceptable Java** — he compiles and executes it successfully.

### 1:28:24 — Category 3 demo in `Test.java` (executed)

```java
class Test {
    public static void main(String[] args) {
        new Thread(new Runnable() {
            public void run() {
                for (int i = 0; i < 10; i++) {
                    System.out.println("child thread 2");
                }
            }
        }).start();

        for (int i = 0; i < 10; i++) {
            System.out.println("main thread 2");
        }
    }
}
```

**Compile & run:** CE: OK.

**Sample output:** `main thread 2` and `child thread 2` lines interleaved (exact order varies).

Sir humorously warns: *"Don't show this code everywhere — people may ask if it's Java or not"* — but confirms it **is** valid Java, executed in class.

### 1:30:45 — Session wrap-up

**All three types of Anonymous Inner Classes covered:**

| # | Type | Example pattern |
|---|---|---|
| 1 | Extends a class | Popcorn p = new Popcorn() { ... }; |
| 2 | Implements an interface | Runnable r = new Runnable() { ... }; |
| 3 | Defined inside arguments | new Thread(new Runnable() { ... }).start(); |

**Universal rules to remember:**

- **Purpose:** instant / one-time use only
- **No class name** — compiler assigns `Outer$1`, `Outer$2`, …
- **Reference vs object:** parent/interface reference may hold anonymous child/implementor object
- **Overriding:** override methods inside `{ }` body as needed
- **Permanent need** → named top-level class; **one-time need** → anonymous inner class at point of use
- **Multithreading combo** (extends `Thread` / implements `Runnable` + anonymous) is **high-frequency for OCJP/SCJP**
## Quick reference — Anonymous inner class syntax cheat sheet

```java
// Type 1: extends class
SuperType ref = new SuperType() {
    // optional method overrides
};

// Type 2: implements interface
InterfaceType ref = new InterfaceType() {
    // must implement abstract methods
};

// Type 3: inside arguments
someMethod(new SomeType() {
    // body
});
// e.g. threading:
new Thread(new Runnable() {
    public void run() { /* job */ }
}).start();
```

**Java code block count: 26**
