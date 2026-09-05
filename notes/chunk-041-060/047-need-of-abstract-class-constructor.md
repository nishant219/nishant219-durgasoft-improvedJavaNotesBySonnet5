# Video 047 — Need of Abstract Class Constructor

## Video info

**Title:** Java - Interface and Abstract class Loopholes Part-4 || Need of Abstract class constructor

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | 47 of 203 |
| Series | Interface and Abstract class Loopholes · Part 4 |
| Topic | Need of Abstract class constructor |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 28m 13s |
| Video ID | OGbUXeQ92q4 |
| Watch | https://www.youtube.com/watch?v=OGbUXeQ92q4 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Video 044 put five loophole questions on the board and answered none of them.
This video closes out two of the five:

1. *(Question 2)* We can't create an object for an abstract class directly —
   can we create one **indirectly**?
2. *(Question 1)* We can't create an object for an abstract class at all, so
   **why is an abstract class allowed to declare a constructor**?

Sir answers the second question with one worked example told in two halves:
the same `Person` → `Student`/`Teacher` hierarchy built **without** a
constructor in the abstract class, then rebuilt **with** one — so the
difference is visible directly in how much code each child constructor needs.

---

### 00:28 — Open

Captions are noise until he starts talking.

### 01:03 — Directly not possible; indirectly?

Is it possible to create an object for an abstract class? **Directly: not
possible**, because it's an abstract class. But **indirectly** — possible or
not? He polls the room before answering.

### 01:32 — Neither directly nor indirectly

**Neither.** An abstract class means a **partially implemented class** — if
the implementation isn't complete, there's nothing to build an object from.
Either directly or indirectly, you cannot create an object for an abstract
class.

```java
abstract class Person {
    String name;
    int age;
}

class Test {
    public static void main(String[] args) {
        Person p = new Person();
        // CE: Person is abstract; cannot be instantiated
    }
}
```

### 02:01 — Then what is the need of a constructor inside an abstract class?

If you can never instantiate it, why can an abstract class declare a
constructor at all? He promises a ten-minute example that answers this
properly — the most valuable point of the video.

---

## First half: without a constructor in the abstract class

### 03:03 — `abstract class Person` — a hundred properties, stuck at two

Every real person has dozens of properties — name, age, height, weight,
father's name, gender, address, qualification. For the board he keeps only
two, `name` and `age`, and generalizes later.

```java
abstract class Person {
    String name;
    int age;
}
```

No constructor here yet — the point of this half is to show what happens
without one.

### 04:36 — `Student extends Person`

`Student` inherits `name` and `age` automatically, and adds two of its own:
`rollNumber`, `marks` — four properties total. Since `Person` has no
constructor, **the child constructor alone** is responsible for
initializing all four:

```java
abstract class Person {
    String name;
    int age;
}

class Student extends Person {
    int rollNumber;
    int marks;

    Student(String name, int age, int rollNumber, int marks) {
        this.name = name;
        this.age = age;
        this.rollNumber = rollNumber;
        this.marks = marks;
    }
}
```

### 06:47 — `Student s1 = new Student("Durga", 48, 101, 90);`

The `Student` constructor is the only one that runs, and it does all four
assignments: `name = "Durga"`, `age = 48`, `rollNumber = 101`, `marks = 90`.

### 07:45 — Second child: `Teacher extends Person`

Same story with a different child. `Teacher` also inherits `name` and `age`,
and adds `double salary` and `String subject` — four properties again, all
initialized by the `Teacher` constructor because the parent still has none:

```java
class Teacher extends Person {
    double salary;
    String subject;

    Teacher(String name, int age, double salary, String subject) {
        this.name = name;
        this.age = age;
        this.salary = salary;
        this.subject = subject;
    }
}
```

### 09:31 — `Teacher t = new Teacher("Nagoor", 47, 25000, "Java");`

Again, one constructor, four assignments, no parent constructor involved.

### 10:35 — End of "without constructor": still simple, so far

Two child classes, two more properties each — the `Student` and `Teacher`
constructors did all the initialization because `Person` has none. Not a
problem yet at this scale.

### 11:12 — Generalize: 100 properties, 1000 child classes

Now stretch the numbers to something realistic: `Person` has **100**
properties (not 2), and there are **1,000** child classes — `Student`,
`Teacher`, `Principal`, `Employee`, and on and on.

### 12:00 — The redundancy problem

If `Person` has no constructor, every one of those 1,000 child constructors
must open with the **same 100 assignment lines** —
`this.name = name; this.age = age; …` — before it even gets to its own
fields. That's the same code copy-pasted a thousand times: **duplicate code,
code redundancy**. How do you avoid writing it a thousand times?

### 13:22 — Solution: put the constructor inside the abstract class

---

## Second half: with a constructor in the abstract class

### 13:50 — `Person` gets a constructor

```java
abstract class Person {
    String name;
    int age;

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}
```

### 14:44 — `Student extends Person` — one line replaces two

`Student` still has four properties total, but now the first line of its
constructor is a **`super` call**, and the parent constructor takes care of
`name` and `age`. The child only initializes what's actually its own:

```java
class Student extends Person {
    int rollNumber;
    int marks;

    Student(String name, int age, int rollNumber, int marks) {
        super(name, age);        // parent constructor takes name, age
        this.rollNumber = rollNumber;
        this.marks = marks;
    }
}
```

Before, the `Student` constructor had four assignment lines. Now it has
three lines and one of them is a call. If `Person` had 100 properties
instead of 2, that's 100 lines you no longer write in every child — just
one `super(...)` call.

### 16:43 — `Student s = new Student("Durga", 48, 101, 90);`

**The parent constructor** initializes `name` and `age`; the child
constructor initializes `rollNumber` and `marks`. Scale that up: if `Person`
carried 100 properties, all 100 would be initialized at the parent level,
and the child would still need only the one `super` line.

### 17:48 — `Teacher extends Person` — same pattern

```java
class Teacher extends Person {
    double salary;
    String subject;

    Teacher(String name, int age, double salary, String subject) {
        super(name, age);
        this.salary = salary;
        this.subject = subject;
    }
}
```

### 19:01 — `Teacher t = new Teacher("Nagoor", 47, 25, "Java");`

`super(name, age)` runs first and sets `name = "Nagoor"`, `age = 47`; the
`Teacher` constructor then sets `salary = 25`, `subject = "Java"`.

### 19:44 — With vs. without: the 100-line comparison, side by side

Without a constructor in `Person`: every one of the 1,000 child constructors
repeats the same 100 initialization lines. With a constructor in `Person`:
every child constructor replaces those 100 lines with **one** `super(...)`
call. The abstract class constructor does the shared work exactly once.

### 20:46 — The advantage, named: code reusability

The same parent-initialization code is reused by every child class instead
of being duplicated in each one. Shorter constructors, less duplicate code,
better readability. **Code reusability is the whole point** of giving an
abstract class a constructor — the constructor exists purely to serve the
**child object's** initialization, even though the abstract class itself can
never be instantiated.

### 21:48 — Board dictation: the exam answer

Sir has the class copy this down slowly, repeating it several times:

> **Anyway we can't create an object for an abstract class, either directly
> or indirectly — but an abstract class can contain a constructor. What is
> the need?**
>
> **The main objective of an abstract class constructor is to perform
> initialization for the instance variables which are inheriting from the
> abstract class to the child class.**
>
> **Whenever we create a child class object, the abstract class constructor
> is automatically executed to perform initialization for the instance
> variables inherited from the abstract class — code reusability.**

### 25:20 — Recap with the numbers one more time

Without the constructor, 1,000 child classes each separately initialize the
same 100 inherited properties. With it, every child constructor needs only
one line — `super(...)` — and the abstract class constructor handles all
100 properties once. That's the benefit: **code reusability**.

### 26:31 — "We can create it indirectly" is 100% wrong

A common wrong belief: since an abstract class can have a constructor, maybe
you *can* create its object indirectly, and the constructor is proof of
that. **100% wrong.** The constructor's existence has nothing to do with
whether the abstract class can be instantiated — it can't be, directly or
indirectly, ever. The constructor exists solely to initialize the fields a
**child** object inherits.

### 26:52 — Copy the full example: first half, second half, total

The board is copied in three passes — the without-constructor version, the
with-constructor version, then both side by side. Full compiling picture of
both halves:

```java
// ----- WITHOUT a constructor in the abstract class -----
abstract class Person {
    String name;
    int age;
}

class Student extends Person {
    int rollNumber;
    int marks;

    Student(String name, int age, int rollNumber, int marks) {
        this.name = name;
        this.age = age;
        this.rollNumber = rollNumber;
        this.marks = marks; // 100 parent fields -> 100 duplicated lines per child
    }
}

class Teacher extends Person {
    double salary;
    String subject;

    Teacher(String name, int age, double salary, String subject) {
        this.name = name;
        this.age = age;
        this.salary = salary;
        this.subject = subject;
    }
}
```

```java
// ----- WITH a constructor in the abstract class (code reusability) -----
abstract class Person {
    String name;
    int age;

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}

class Student extends Person {
    int rollNumber;
    int marks;

    Student(String name, int age, int rollNumber, int marks) {
        super(name, age);     // one line for every inherited property
        this.rollNumber = rollNumber;
        this.marks = marks;
    }
}

class Teacher extends Person {
    double salary;
    String subject;

    Teacher(String name, int age, double salary, String subject) {
        super(name, age);
        this.salary = salary;
        this.subject = subject;
    }
}

class Test {
    public static void main(String[] args) {
        Student s = new Student("Durga", 48, 101, 90);
        Teacher t = new Teacher("Nagoor", 47, 25, "Java");
        // Person.<init> runs first in both cases, then the child body
    }
}
```

> ⚠️ **Modern Java — sealed classes formalize exactly the hierarchy this
> lecture builds.**
> The `Person → Student, Teacher, Principal, Employee, …` shape — one
> abstract superclass, an open-ended list of subclasses anyone could add —
> is precisely what **sealed classes (Java 17, JEP 409)** let you close down
> on purpose:
> ```java
> sealed abstract class Person permits Student, Teacher
>         extends Object {
>     String name;
>     int age;
>     Person(String name, int age) { this.name = name; this.age = age; }
> }
> final class Student extends Person {
>     Student(String name, int age) { super(name, age); }
> }
> final class Teacher extends Person {
>     Teacher(String name, int age) { super(name, age); }
> }
> ```
> `permits` names the only classes allowed to extend `Person`; a `switch`
> over a sealed hierarchy can then be exhaustive without a `default` branch
> (pattern matching for switch, Java 21). None of this changes the
> constructor-chaining mechanics Sir teaches — `super(...)` still runs first
> and still does the shared initialization — it only changes whether new
> subclasses can show up later without your permission.

> ⚠️ **Modern Java — records do not replace this pattern.**
> A **record** (Java 16, JEP 395) also auto-generates a constructor that just
> assigns fields, which sounds like the same "reusability" win. It isn't a
> fit here: a record is implicitly `final` and **cannot extend another
> class** (it can only implement interfaces), so `Student` and `Teacher`
> could never be records of a `Person` superclass. Records solve boilerplate
> for a flat, final data holder with no shared parent; this lecture's problem
> — a real class hierarchy sharing state through inheritance — still needs
> exactly the abstract-superclass-constructor-plus-`super()` pattern taught
> here, unchanged since Java 1.0.

---

## Exam and interview points

1. **An abstract class can never be instantiated, either directly or
   indirectly** — not even by giving it a constructor. `new Person()` is
   always a compile error when `Person` is abstract.
2. **"Indirectly, yes" is a trap answer.** The constructor's presence is not
   evidence that indirect instantiation is possible; it exists only to
   initialize the fields a **child** object inherits.
3. **The main objective of an abstract class constructor:** to initialize
   the instance variables that a child class inherits from it. Whenever a
   child object is created, the abstract class constructor runs
   automatically to do this.
4. **The advantage is code reusability.** With N properties in the abstract
   class and M child classes, skipping the constructor means N × M lines of
   duplicated initialization across every child; putting the constructor in
   the abstract class collapses each child's share of that to one
   `super(...)` call.
5. **Watch for the anonymous-class trick question:** `Person p = new
   Person() { };` compiles even though `Person` is abstract — but it creates
   an object of an unnamed **subclass** of `Person`, not of `Person` itself
   (`p.getClass() == Person.class` is `false`). It does not contradict "an
   abstract class can never be instantiated."
6. **`super(...)` must be the first statement (explicit or implicit) in a
   constructor** — this is why the child constructors here open with it
   rather than repeating the parent's assignments.
7. This answers two of the five video-044 loophole questions; question 4
   (abstract class vs. interface constructors) and question 5 (what an
   interface gives you that an abstract class doesn't) are still open for
   the videos ahead.

---

**Next:** Video 048 — Abstract class vs Interface wrt constructor
