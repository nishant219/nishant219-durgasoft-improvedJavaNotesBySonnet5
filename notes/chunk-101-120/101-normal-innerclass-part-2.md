# Video 101

## Video info

**Title:** Core Java With OCJP/SCJP: Innerclass  Part- 2||normal innerclass

| Field | Value |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | 101 of 203 |
| Series | Inner Classes · Part 2 |
| Topic | Normal / regular inner class (continued), nesting, method-local inner classes |
| Instructor | Durga Sir |
| Duration | 1h 30m 28s |
| Video ID | pRsqR3vQvBM |
| Watch | https://www.youtube.com/watch?v=pRsqR3vQvBM |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

### 00:05 — Recap: accessing inner class code

Durga Sir resumes after Part 1. Already covered:

- Calling inner-class code from the **static area** of the outer class
- From the **instance area** of the outer class
- From **outside** the outer class
This session adds more properties of **normal (regular) inner classes**.

### 00:27 — Inner class accessing outer static and instance members

```java
class Outer {
    int x = 10;          // instance variable of Outer
    static int y = 20;   // static variable of Outer

    class Inner {
        public void m1() {
            System.out.println(x); // prints 10
            System.out.println(y); // prints 20
        }
    }

    public static void main(String[] args) {
        new Outer().new Inner().m1();
    }
}
// prints 10
// prints 20
```

**Common trap:** Students see `SOP of y` (static member) inside inner class and think **invalid**, because they recall: *"Inner classes cannot have static declarations."*

**Clarification:**

- **Declaring** static members inside a normal inner class → **not allowed**
- **Accessing** static and non-static members of the **outer** class from inner class → **allowed directly**
Whether the outer member is static, instance, private, or public — from a normal inner class you can access **both** static and non-static members of the outer class directly.

Shortcut one-liner to call inner method from `main`:

```java
new Outer().new Inner().m1();
```

### 06:19 — The naming-conflict twist: three variables named `x`

```java
class Outer {
    int x = 10; // instance variable of Outer

    class Inner {
        int x = 100; // instance variable of Inner

        public void m1() {
            int x = 1000; // local variable of m1
            System.out.println(x); // prints 1000
        }
    }

    public static void main(String[] args) {
        new Outer().new Inner().m1();
    }
}
// prints 1000
```

Three variables, all named `x`, different contexts:

| Variable | Context |
|---|---|
| Outer.x | Instance variable of outer class |
| Inner.x | Instance variable of inner class |
| m1's x | Local variable of m1 |

**Nearest match wins:** bare `x` in `m1()` resolves to the **local variable** → **1000**.

### 08:43 — Printing inner instance variable (100)

Requirement: print **100** (inner class instance `x`), not 1000.

Within inner class, **`this`** always refers to the **current inner class object**:

```java
System.out.println(this.x); // prints 100
```

`this.x` → inner class object's instance variable.

### 09:50 — Printing outer instance variable (10)

Requirement: print **10** (outer class instance `x`).

**Cannot use `super.x`:** Outer is **not** the parent class; Inner is **not** a child class in inheritance terms. `super` is wrong here.

An outer object **must already exist** — you cannot enter inner instance code without a current outer object. To refer to the **current outer class object's** instance member:

```java
System.out.println(Outer.this.x); // prints 10
```

**Rules (naming conflict):**

| Need | Syntax |
|---|---|
| Local variable | x |
| Inner instance variable | this.x |
| Outer instance variable | OuterName.this.x |

Same style applies: `this` = current inner object; `Outer.this` = current outer object tied to this inner instance.

**Full shadowing example:**

```java
class Outer {
    int x = 10;

    class Inner {
        int x = 100;

        public void m1() {
            int x = 1000;
            System.out.println(x);            // prints 1000
            System.out.println(this.x);       // prints 100
            System.out.println(Outer.this.x); // prints 10
        }
    }

    public static void main(String[] args) {
        new Outer().new Inner().m1();
    }
}
// prints 1000
// prints 100
// prints 10
```

### 15:42 — Modifiers: outer class vs inner class

**Outer (top-level) class — applicable modifiers (5):**

- `public` (or default / package-private)
```java
final
```

```java
abstract
```

```java
strictfp
```

**Inner class — applicable modifiers (8):**

All outer-class modifiers **plus**:

```java
private
```

```java
protected
```

- `static` (→ static nested class; covered later)
Summary:

| Outer class | Inner class |
|---|---|
| public, default, final, abstract, strictfp | Same + private, protected, static |

### 18:43 — Nesting of inner classes

**Question:** Can we declare an inner class inside another inner class?

**Answer:** Yes — **nesting of inner classes** is possible (any number of levels).

```java
class A {
    class B {
        class C {
            public void m1() {
                System.out.println("innermost class method");
            }
        }
    }
}
```

To call `C.m1()` from outside:

1. Create **A** object
1. Using A, create **B** object
1. Using B, create **C** object
1. Call `m1()` on C
```java
class Test {
    public static void main(String[] args) {
        A a = new A();
        A.B b = a.new B();
        A.B.C c = b.new C();
        c.m1(); // prints innermost class method
    }
}
// prints innermost class method
```

**Dependency chain:** No C without B; no B without A.

### 25:07 — Second category: method-local inner classes

Four types of inner classes (this session introduces #2):

1. Normal / regular inner class *(Part 1)*
1. **Method-local inner class** *(this section)*
1. Anonymous inner class
1. Static nested class
**Definition:** Sometimes we declare an inner class **inside a method**. Such classes are **method-local inner classes**.

### 27:26 — Purpose: method-specific repeated functionality (nested-method workaround)

Scenario: large method `m1()` (~50,000 lines). Some functionality (e.g. `sum`) is needed **repeatedly inside `m1` only**, not elsewhere.

**Attempt — nested method (invalid):**

```java
class Test {
    public void m1() {
        public void sum(int x, int y) { // CE: method inside method not allowed
            System.out.println("The sum is: " + (x + y));
        }
        sum(10, 20);
    }
}
// CE: illegal start of expression (nested method)
```

**Java rule:** Nested **methods** are **not** allowed.

**Option 1:** Declare `sum` at **class level** and call it — works, but pollutes the class if needed only inside `m1`.

**Option 2 (method-local inner class):** Inside `m1`, declare a **class**; inside that class, declare the method:

```java
class Test {
    public void m1() {
        class Inner {
            public void sum(int x, int y) {
                System.out.println("The sum is: " + (x + y));
            }
        }
        Inner i = new Inner();
        i.sum(10, 20);
        i.sum(100, 200);
        i.sum(1000, 2000);
    }

    public static void main(String[] args) {
        new Test().m1();
    }
}
// prints The sum is: 30
// prints The sum is: 300
// prints The sum is: 3000
```

**Main purpose of method-local inner class:** Define **method-specific, repeatedly required** functionality.

**Best choice when:** You need **nested method** behavior — method-local inner classes meet that requirement.

### 34:20 — Scope: rarely used

Local variable of `m1` → accessible only inside `m1`.

Method-local inner class declared inside `m1` → accessible **only within that method**, not outside.

Because scope is very small, method-local inner classes are the **most rarely used** type of inner class.

**Most commonly used:** Anonymous inner classes (covered later).

**Conclusions written on board:**

- Access method-local inner class **only within the method where declared**
- Outside that method → **cannot access**
- Because of **lesser scope** → **most rarely used** type
### 38:37 — Full executable example (sum)

Complete program compiled and run live (`Test1.java`):

```java
class Test {
    public void m1() {
        class Inner {
            public void sum(int x, int y) {
                System.out.println("The sum is: " + (x + y));
            }
        }
        Inner i = new Inner();
        i.sum(10, 20);
        i.sum(100, 200);
        i.sum(1000, 2000);
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1();
    }
}
// prints The sum is: 30
// prints The sum is: 300
// prints The sum is: 3000
```

Confirmed output on execution: 30, 300, 3000.

### 45:38 — Instance method vs static method hosting method-local inner class

**Question:** Can inner class be declared inside a **static** method?

**Answer:** Yes — method-local inner class can be declared inside **both instance and static methods**. But behavior differs.

```java
class Test {
    int x = 10;
    static int y = 20;

    public void m1() { // instance method
        class Inner {
            public void m2() {
                System.out.println(x); // prints 10
                System.out.println(y); // prints 20
            }
        }
        Inner i = new Inner();
        i.m2();
    }

    public static void main(String[] args) {
        new Test().m1();
    }
}
// prints 10
// prints 20
```

**If `m1` is static:**

```java
class Test {
    int x = 10;
    static int y = 20;

    public static void m1() { // static method — entire block is static context
        class Inner {
            public void m2() {
                System.out.println(x); // CE: non-static variable x cannot be referenced from a static context
                System.out.println(y); // prints 20
            }
        }
        Inner i = new Inner();
        i.m2();
    }
}
// CE: non-static variable x cannot be referenced from a static context
```

**Rules:**

| Declared inside | From method-local inner class can access |
|---|---|
| Instance method | Both static and non-static members of outer class |
| Static method | Only static members of outer class directly |

### 58:18 — "Most dangerous point": local variables of enclosing method

```java
class Test {
    public void m1() {
        int x = 10; // local variable of m1

        class Inner {
            public void m2() {
                System.out.println(x); // CE: local variable x accessed from within inner class needs to be declared final
            }
        }
        Inner i = new Inner();
        i.m2();
    }

    public static void main(String[] args) {
        new Test().m1();
    }
}
// CE: Local variable x is accessed from within inner class; needs to be declared final
```

**Rule:** From method-local inner class, we **cannot** access local variables of the enclosing method **unless** that local variable is **`final`**.

**Fix:**

```java
final int x = 10;
// ... Inner.m2() can now use x — compiles; prints 10
```

### 1:09:36 — Internal reason (stack vs heap, final constant folding)

Hints for deep understanding:

1. Every **`final`** variable is replaced by its **value at compile time**
1. **Local variables** → **stack** memory
1. **Objects** → **heap** memory
**Timeline when `t.m1()` runs:**

- Local `x = 10` created on **stack**
- `Inner i = new Inner()` → object on **heap**
- While `m1` executes, `m2()` can read stack `x` — OK
**Problem scenario:**

- After `m1()` completes, local `x` is **destroyed** (stack frame gone)
- Inner object may **still exist on heap**
- If someone later calls `i.m2()` **directly** (without re-entering `m1`), `m2` tries to read `x` from stack — **x no longer exists**
That's why non-final local variables are forbidden.

**Why `final` works:**

- `final int x = 10` → compiler replaces `x` with literal **`10`** in inner class bytecode at compile time
- No runtime dependency on stack variable
- After `m1` ends, `m2` still prints **10** from embedded constant
### 1:15:40 — OCJP-style variable access quiz

```java
class Test {
    int i = 10;
    static int j = 20;

    public void m1() {
        int k = 30;
        final int m = 40;

        class Inner {
            public void m2() {
                // line 1 — which can we access directly?
                System.out.println(i); // OK — outer instance var; m1 is instance method
                System.out.println(j); // OK — outer static var
                System.out.println(k); // CE: local variable k needs to be final
                System.out.println(m); // OK — final local variable
            }
        }
    }
}
```

**Question 1 — `m1` instance method, at line 1:**

| Variable | Accessible? | Reason |
|---|---|---|
| i | Yes | Instance var of outer; instance context |
| j | Yes | Static var of outer |
| k | No | Local var of m1, not final |
| m | Yes | Local var declared final |

**Question 2 — if `m1` is `static`:**

| Variable | Accessible? |
|---|---|
| i | No — instance variable |
| j | Yes |
| k | No (not final) |
| m | Yes (final) |

**Question 3 — if `m2` is declared `static` inside Inner:**

```java
public static void m2() { ... }
```

→ **Compile-time error first** — cannot declare **static members** inside normal (non-static nested) inner class:

```java
// CE: modifier 'static' not allowed here (inner class static method)
// CE: Inner classes cannot have static declarations
```

Don't analyze variable access until code compiles — static `m2` fails before `i/j/k/m` logic matters.

### 1:26:19 — Modifiers for method-local inner classes

Parallel to **local variables**:

- Local variables: only modifier allowed is **`final`** (not public/private/protected)
- Method-local inner class: **public, private, protected, default, static** → **NOT applicable**
**Only applicable modifiers for method-local inner classes:**

```java
final
```

- `abstract` (not simultaneously with final)
```java
strictfp
```

Any other modifier → compile-time error.

### 1:29:36 — Session summary

**Normal inner class (this + prior session):**

- Access outer static & instance members directly
- `this` = inner object; `Outer.this` = enclosing outer object (shadowing)
- More modifiers than top-level class (private, protected, static)
- Nesting of inner classes allowed (A → B → C)
**Method-local inner class:**

- Class declared inside a method
- Purpose: method-specific repeated logic; nested-method substitute
- Accessible only in declaring method → rarely used
- Can host in instance or static method (static → only outer static members)
- Cannot read enclosing local vars unless **`final`**
- Modifiers: `final`, `abstract`, `strictfp` only
- **Most dangerous exam point:** final local variable rule + stack/heap lifetime
**Java block count:** 18
