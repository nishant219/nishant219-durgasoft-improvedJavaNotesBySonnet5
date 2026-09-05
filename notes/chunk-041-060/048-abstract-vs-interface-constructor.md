# Video 048 — Abstract Class vs Interface: Constructor

## Video info

**Title:** Interface and Abstract class Loopholes Part-5 || Abstract class vs Interface wrt constructor

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | 48 of 203 |
| Series | Interface and Abstract class Loopholes · Part 5 |
| Topic | Abstract class vs Interface wrt constructor |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 10m 50s |
| Video ID | Sztm3l_dmdU |
| Watch | https://www.youtube.com/watch?v=Sztm3l_dmdU |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is **question 4** from the five-question agenda video 044 put on the
board: we can't create an object for an abstract class *or* an interface, but
an abstract class can contain a constructor and an interface cannot — why?

Throughout this video Sir occasionally says "you **can** create object for
abstract class / interface" where the rest of the sentence, and the whole
arc of videos 044–047, make clear he means **can't**. That is an auto-caption
and speech slip repeated across this stretch, not a change in what he is
teaching — the notes below give the intended meaning directly.

---

### 00:33 — Recap of what's already answered

Before the new question, Sir checks off the first three from the video-044
list:

- **Q1 (need of an abstract-class constructor):** we can't create an object
  for an abstract class, but abstract class can contain a constructor — what
  is the need? **Completed** (video 047).
- **Q2 (directly vs. indirectly):** can an abstract-class object be created
  indirectly, even though direct creation is refused? **Invalid** — neither
  directly nor indirectly.
- **Q3 (child object vs. parent object):** does creating a child class object
  automatically create a parent class object? **Invalid** — the parent
  **constructor** runs, but no parent **object** is created (videos 045–046).

### 01:24 — Today's question: constructor for abstract class, not for interface

> We can't create an object for abstract class **and** interface, but abstract
> class can contain a constructor and interface doesn't. Why?

Sir's one-line answer up front: **the constructor concept is not applicable
to an interface.** The rest of the video is *why*.

### 02:00 — What a constructor is actually for

> The purpose of a constructor is to perform **initialization** — that is, to
> **provide values for instance variables**.

That single sentence is the whole argument. Everything that follows is just
checking which of the two — abstract class, interface — actually has instance
variables to initialize.

### 02:17 — Abstract class has instance variables, so it needs a constructor

An abstract class **can** declare instance variables, and a child class
depends on them:

```java
abstract class Person {
    String name;
    int age;

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}

class Student extends Person {
    Student(String name, int age) {
        super(name, age);   // Person's constructor runs for this Student object
    }
}

class Test {
    public static void main(String[] args) {
        Student s = new Student("Durga", 48);
        System.out.println(s.name + " " + s.age);   // Durga 48
        // Person's constructor executed; no Person object was ever created
    }
}
```

`name` and `age` live in `Person`, but only a `Student` (or other concrete
subclass) object ever actually exists carrying them. You still need a
constructor to put values into those fields — you just never get to call it
with `new Person(...)` directly, only via `super(...)` from a subclass
constructor. That is the constructor's whole reason to exist here: **instance
variables that belong to the abstract class, but only get initialized as
part of a real, concrete child object.**

### 03:44 — Interface: no instance variables, so no constructor

Now the other side. Every field declared inside an interface is implicitly
`public static final`, whether you write those modifiers or not:

```java
interface Inter {
    int x = 10;
    // compiler treats this exactly as:
    // public static final int x = 10;
}

class Test2 {
    public static void main(String[] args) {
        System.out.println(Inter.x);   // 10 — one shared class-level constant
        // Inter.x = 20;               // CE: cannot assign a value to final variable x
    }
}
```

`static` means the field belongs to the interface itself, not to any object —
there is exactly one `x`, shared by every implementer, never a
per-object copy. **There is no chance of an instance variable existing inside
an interface.** And if there's no instance variable, there's nothing for a
constructor to initialize — which is exactly why the constructor concept
does not apply to interfaces at all:

```java
interface Inter2 {
    Inter2() { }
    // CE: <identifier> expected
    // an interface constructor isn't a restricted feature — it's not a
    // recognized construct in an interface body at all
}
```

> ⚠️ **Modern Java — interfaces gained method bodies, but never gained state.**
> This lecture is Java 6/7, when an interface could only hold constants and
> abstract method signatures. Since then interfaces picked up real code:
> **default methods** (Java 8, run on an implementing object via `this`),
> **static methods** (Java 8), and **private methods** (Java 9, helpers for
> the default/static methods to share). None of that changes the reasoning
> above:
> ```java
> interface Inter3 {
>     int x = 10;
>     default int getX() { return this.x; }   // reads the one shared constant
> }
> class Impl implements Inter3 { }
> // new Impl().getX() -> 10
> ```
> `getX()` runs against `this`, but it still has no per-object field to read —
> it can only reach `static final` constants and whatever the *implementing
> class's own* instance variables expose through its methods. Interfaces
> still cannot declare instance variables and still cannot declare a
> constructor, unchanged from Java 6 through current Java. Default/static/
> private methods are new places to put behavior; they are not new state.

### 06:07 — Board answer, part one: the constructor's job

The main purpose of a constructor is to perform initialization of an object
— that is, to perform initialization for instance variables.

### 07:05 — Board answer, part two: abstract class side

Abstract class can contain instance variables, which are required for the
child class object. To perform initialization for these instance variables,
the constructor concept is required for abstract classes.

### 08:25 — Board answer, part three: interface side

Every variable present inside an interface is always `public static final`,
whether declared that way or not. Hence there is no chance of an instance
variable existing inside an interface. Because of this, the constructor
concept is not required — not applicable — for interfaces.

### 10:06 — Close

Abstract class can contain a constructor but interface doesn't — because
abstract class can hold instance variables that need initializing, and
interface, having only `static final` constants, never has anything for a
constructor to do.

---

## Exam and interview points

1. **A constructor's one job is initializing instance variables.** No
   instance variables means no reason for a constructor to exist.
2. **An abstract class can declare instance variables** (required by, and
   inherited into, its concrete subclasses), so it needs a constructor to
   initialize them — even though `new AbstractClass()` is never legal.
3. **Every interface field is implicitly `public static final`**, regardless
   of whether you write the modifiers. There is one shared copy, not a
   per-object one.
4. **An interface therefore cannot have instance variables**, and so has
   nothing for a constructor to initialize — the constructor concept simply
   does not apply. `interface I { I() { } }` is a compile error
   (`<identifier> expected`).
5. **Default, static, and private interface methods (Java 8/9) don't change
   this answer.** They add behavior, not per-object state — an interface
   still cannot hold an instance variable or declare a constructor today.
6. **The recurring exam trap is the flip side of Q3 (video 046):** a child
   object's construction runs the parent's constructor, but never creates a
   separate parent object — so "no instance variables" is really "no
   instance variables of its own to initialize," which is precisely why
   interfaces are excluded and abstract classes are not.

---

**Next:** Video 049 — Abstract Class vs Interface
