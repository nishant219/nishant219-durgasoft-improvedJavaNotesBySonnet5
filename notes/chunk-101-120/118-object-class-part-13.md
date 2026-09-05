# Video 118

## Video info

**Title:** Core Java With OCJP/SCJP: java.lang.package Part-13 || object class || clone()

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP (java.lang package series) |
| Position | 118 of 203 |
| Series | Core Java With OCJP/SCJP — java.lang package |
| Topic | Object class — clone(), Cloneable, shallow vs deep cloning |
| Instructor | Durga Sir |
| Duration | 1h 29m 43s (from transcript) |
| Video ID | L-p-RGTNrZg |
| Watch | https://www.youtube.com/watch?v=L-p-RGTNrZg |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

### 00:07 — Transition from `equals()` to `clone()`

Previous session spent ~3 hours on `equals()` alone. This session: **`clone()` method** and cloning concepts.

### 00:48 — What is cloning? (real-world analogy)

- **Cloning** = process of creating an **exact duplicate** (Xerox copy) of an object/person.
- Real-world human cloning: scientists explored it in the late 1990s; **advantages < disadvantages** → governments **banned human cloning** (severe punishment in lecture narrative).
- **Cloning Java objects is legal** — no need to worry.
**Definition (board):**

> *The process of creating an ***exactly duplicate object*** is called ***cloning***.*

### 04:01 — Purpose of cloning (two main reasons)

1. **Maintain backup copy** — like keeping a Xerox of SCJP notes or a color photocopy of driving license/PAN instead of carrying originals. Perform risky operations on the **copy**; if something goes wrong, recover from the **original**.
1. **Preserve state of an object** at a particular instant — perform updates on a duplicate, then **compare updated values with original values** later. If you mutate the only original, initial values are lost.
**Summary:**

> *Main purposes: ***backup copy*** + ***preserve original state*** for later comparison.*

### 06:04 — Real-life backup examples (license, PAN, notes)

Durga Sir extends purpose with everyday examples:

- SCJP notes: keep **original** safe; use **Xerox copy** daily — if duplicate lost, take another Xerox from original.
- Driving license / PAN / voter ID: **never carry originals** in pocket; use **color Xerox** — original stays secured.
- Same idea in code: clone before risky mutation so you can **recover** from pristine copy.
### 09:58 — How to clone: `Object.clone()` prototype

`clone()` lives in **`Object` class** (continuing Object-class method series).

**Complete prototype (must know for exam):**

```java
protected native Object clone() throws CloneNotSupportedException;
```

| Part | Meaning |
|---|---|
| protected | Callable from subclass / same package (child can invoke on parent’s clone) |
| native | Not implemented in Java — JVM/platform native code |
| Return type Object | Returns duplicate as Object reference |
| throws CloneNotSupportedException | Checked exception — must catch or declare |

### 14:46 — First program skeleton: `class Test` — duplicate reference ≠ cloning

```java
class Test {
    int i = 10;
    int j = 20;

    public static void main(String[] args) throws CloneNotSupportedException {
        Test t1 = new Test();   // i=10, j=20

        // WRONG — NOT cloning:
        // Test t2 = t1;         // duplicate REFERENCE only; changes to t2 affect t1

        Test t2 = (Test) t1.clone();  // exactly duplicate OBJECT

        t2.i = 38;
        t2.j = 39;

        System.out.println(t1.i + "..." + t1.j);  // 10...20 — original unchanged
    }
}
```

**Key distinction:**

> *Creating duplicate ***reference variable*** (*`t2 = t1`*) is ***NOT*** cloning.*

> *Creating duplicate ***object*** (*`clone()`*) ***IS*** cloning.*

### 18:51 — Compile fixes required for `clone()` demo

Three issues when writing `Test t2 = (Test) t1.clone()`:

1. **Return type `Object`** → need **cast**: `(Test) t1.clone()`
- Without cast: `incompatible types: found java.lang.Object, required Test`
1. **`CloneNotSupportedException`** is checked → `throws CloneNotSupportedException` on `main` (or try/catch)
1. **`Cloneable` marker interface** — see below (runtime, not compile)
### 21:59 — `Cloneable` interface: compile succeeds without it; runtime fails

**Surprise:** Code **compiles** even if `Test` does **not** implement `Cloneable`.

At **runtime** without `Cloneable`:

```java
Exception in thread "main" java.lang.CloneNotSupportedException: Test
```

**Rules:**

- Cloning allowed **only for clonable objects**.
- An object is **clonable iff** its class **implements `Cloneable`**.
- `Cloneable` is in **`java.lang` package**.
- `Cloneable` has **zero methods** → **marker interface** (like `Serializable` pattern, but `Cloneable` is in `java.lang` not `java.io`).
> **Do not confuse:** `Cloneable`* does ***NOT*** declare *`clone()`* — *`clone()`* is in ***`Object`***, not in *`Cloneable`*. (Unlike *`Runnable`* which declares *`run()`*.)*

**Fix:**

```java
class Test implements Cloneable {
    // ...
}
```

After `implements Cloneable`: compiles **and** runs; output **`10...20`**.

### 31:24 — Board theory: cloning rules summary

- We can perform cloning **only for clonable objects**.
- Object is clonable **if and only if** class implements **`Cloneable`** (`java.lang`).
- `Cloneable` = marker interface (no methods).
- Cloning non-clonable object → **runtime** `CloneNotSupportedException` (not compile error).
**While using `clone()` take care of:**

1. Type casting `(TargetType) obj.clone()`
1. `throws CloneNotSupportedException` or try/catch
1. Class must implement `Cloneable`
### 28:00 — Live compile-error walkthrough (step by step)

Durga Sir saves `Test.java` without `Cloneable` and demonstrates compiler messages in order:

1. **Without cast:** `Test t2 = t1.clone();`
→ `incompatible types: found java.lang.Object, required Test`

1. **After cast, without throws:**
→ `unreported exception CloneNotSupportedException; must be caught or declared to be thrown`

1. **After `throws CloneNotSupportedException`, still no `Cloneable`:**
→ compiles; **`java Test`** throws `CloneNotSupportedException: Test`

1. **Add `implements Cloneable`:**
→ runs; prints **`10...20`**

Students asked “will it compile without Cloneable?” — answer: **yes compile, no run**.

### 34:58 — Shallow cloning vs deep cloning (advanced topic)

Most students **do not know** this — Durga Sir marks it as **very important**.

**Scenario:** `Dog` object with:

- primitive `i = 10`
- reference `Cat c` pointing to a `Cat` with `j = 20`
```java
Dog d1;  // i=10, c → Cat(j=20)
Dog d2 = (Dog) d1.clone();
```

#### Shallow cloning (`Object.clone()` default)

- New **Dog** object created.
- **Primitive `i`:** duplicate copy (10 in both).
- **Reference `c`:** duplicate **reference variable** pointing to **same old `Cat` object** — **no** duplicate `Cat`.
Also called **bitwise copy** of the original object.

**Problem:** Change via clone affects original’s contained object:

```java
d2.i = 38;      // only d2's primitive changes
d2.c.j = 39;    // changes SHARED Cat → d1.c.j also becomes 39
```

> **Object class `clone()` performs shallow cloning only.**

#### Deep cloning (programmer responsibility)

- Duplicate **Dog** **and** duplicate **contained `Cat`** — full independent graph.
- Changes through clone **do not** affect original’s nested objects.
> *If you want deep cloning → ***override `clone()`*** and implement duplication manually.*

### 49:12 — Shallow cloning live demo: `ShallowCloningDemo`

```java
class Cat {
    int j;
    Cat(int j) { this.j = j; }
}

class Dog implements Cloneable {
    int i;
    Cat c;
    Dog(Cat c, int i) { this.c = c; this.i = i; }

    public Object clone() throws CloneNotSupportedException {
        return super.clone();   // Object.clone() → shallow
    }
}

class ShallowCloningDemo {
    public static void main(String[] a) throws CloneNotSupportedException {
        Cat c = new Cat(20);
        Dog d1 = new Dog(c, 10);
        System.out.println(d1.i + "..." + d1.c.j);  // 10...20

        Dog d2 = (Dog) d1.clone();
        d2.i = 38;
        d2.c.j = 39;

        System.out.println(d1.i + "..." + d1.c.j);  // 10...39 — shared Cat mutated!
    }
}
```

**Executed output:** first line `10...20`, second line **`10...39`** (not `10...20`).

Board conclusion for shallow cloning:

> *By using cloned object reference, if we change the ***contained object***, those changes ***reflect to the main object***. Shallow cloning is ***not*** complete duplication when reference fields exist.*

### 1:03:08 — Shallow cloning theory on board (formal wording)

**Definition:**

> *The process of creating ***bitwise copy*** of an object is called ***shallow cloning***.*

**Rules:**

- Main object has **primitive** fields → duplicate primitives in clone.
- Main object has **reference** fields → duplicate **reference** only, pointing to **old contained object** (no new contained object).
**Default:**

> `Object`* class *`clone()`* method is meant for ***shallow cloning*** only.*

To overcome shared-reference problem → **deep cloning**.

### 1:05:22 — Deep cloning: override `clone()` — manual object creation

Same `Cat` / `Dog` structure, but **`clone()` builds new nested objects:**

```java
class Dog implements Cloneable {
    int i;
    Cat c;
    Dog(Cat c, int i) { this.c = c; this.i = i; }

    public Object clone() throws CloneNotSupportedException {
        Cat c1 = new Cat(this.c.j);       // NEW Cat with same j
        Dog d2 = new Dog(c1, this.i);       // NEW Dog
        return d2;
    }
}
```

**Demo driver (`DeepCloningDemo`):**

```java
Cat c = new Cat(20);
Dog d1 = new Dog(c, 10);
System.out.println(d1.i + "..." + d1.c.j);  // 10...20

Dog d2 = (Dog) d1.clone();
d2.i = 38;
d2.c.j = 39;

System.out.println(d1.i + "..." + d1.c.j);  // 10...20 — original intact
System.out.println(d2.i + "..." + d2.c.j);  // 38...39
```

**Executed output:** `10...20` and `10...20` (both prints for original) — clone changes isolated.

**Deep cloning board definition:**

> *Process of creating exactly duplicate ***independent*** copy ***including contained objects***.*

**Responsibility:**

| Type | Who implements |
|---|---|
| Shallow | `Object.clone()` (via super.clone()) |
| Deep | Programmer — override clone(), create nested copies manually |

### 1:24:59 — Which cloning is best? (thumb rule)

**Not always deep cloning** — deep cloning always is **not** good practice; that is why JDK provides shallow `Object.clone()`.

| Object shape | Best choice |
|---|---|
| Only primitive instance fields | Shallow cloning sufficient (Object.clone()) |
| Contains reference fields (contained objects) | Deep cloning recommended (custom clone()) |

> *Choose based on ***situation/requirement*** — “depends” is the correct mindset.*

### 1:29:14 — Session recap

Topics covered:

1. Definition and **purposes** of cloning
1. **`Object.clone()`** signature (`protected native`, checked exception)
1. **`Cloneable`** marker interface
1. Duplicate reference vs duplicate object
1. **Shallow vs deep** cloning with `Dog`/`Cat` programs and outputs
1. When to prefer each type
**Java block count:** 8
