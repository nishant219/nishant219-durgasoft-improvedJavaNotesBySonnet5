# Video 045 — Child object vs parent constructor (part 1)

## Video info

**Title:** Java -  Interface  and Abstract class Loopholes Part-2 || Child Object Vs Parent Constructor-1

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 45 of 203 |
| Series | Interface and Abstract class Loopholes · Part 2 |
| Topic | Child Object Vs Parent Constructor-1 |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 15m 43s |
| Video ID | c55db2_fFLo |
| Watch | https://www.youtube.com/watch?v=c55db2_fFLo |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

**Continuity.** Video 044 raised the loophole "whenever we create a child object,
is a parent object created?" and covered `new` vs constructor. This video answers
*why the parent constructor runs* when you create a **child** object, using one
`Person` / `Student` board example that carries into the next video too.

---

## 00:23 — Recap: both constructors run, but is a parent object created?

Whenever a **child class object** is created, both the **parent** constructor and
the **child** constructor execute.

```java
class Parent {
    Parent() {
        System.out.println("Parent constructor");
    }
}

class Child extends Parent {
    Child() {
        System.out.println("Child constructor");
    }
}

class Test {
    public static void main(String[] args) {
        Child c = new Child();
        // Parent constructor
        // Child constructor
        // only ONE object exists: the Child — no separate Parent object
    }
}
```

`Child()` never calls `super()` itself, yet "Parent constructor" still prints —
the compiler inserts an implicit `super()` as the first statement of any
constructor that doesn't explicitly start with `this(...)` or `super(...)`.

The question this video answers: that parent constructor clearly *runs* — but
does it mean a separate **parent object** gets created? The rest of the lecture
argues no: the parent constructor runs to initialize the child object's
*inherited* fields, not to build a second object.

### 00:35 — Core question

Why do we need to execute the **parent** constructor when creating a **child**
class object? The child constructor is already there to do initialization — so
what is the parent constructor's job? Sir walks through one board example to
answer it.

---

## 00:58 — Board: class `Person` (common properties)

Every person shares some properties — name, age, height, weight, colour. For the
board Sir keeps it to two: `name` and `age`.

```java
class Person {
    String name;
    int age;

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}
```

`Person` has two instance variables; the constructor's whole job is initializing
those two.

## 02:15 — Board: `Student extends Person`

```java
class Student extends Person {
    // name, age inherited from Person
}
```

Because `Student` **is-a** `Person`, `name` and `age` come to the student
automatically. Student-specific properties, applicable only to a student:

- `int rollNo`
- `int marks`

| Class | Properties |
|---|---|
| Person | 2 → name, age |
| Student | 4 → name, age, rollNo, marks |

Two inherited + two student-specific = four properties on a `Student` object.

## 03:16 — The child constructor must cover all four properties

The constructor responsible for building a `Student` has to be able to
initialize all four:

```java
class Student extends Person {
    int rollNo;
    int marks;

    Student(String name, int age, int rollNo, int marks) {
        // filled in below
    }
}
```

## 03:49 — Creating one `Student` object

```java
class Test {
    public static void main(String[] args) {
        Student s = new Student("Durga", 48, 101, 90);
        // one Student object; all four properties live on that same object
    }
}
```

Which constructor starts running for `new Student(...)`? The **child**
(`Student`) constructor — but it will hand the inherited part off to the parent
constructor.

## 05:06 — Inside the child constructor: don't re-init parent fields, call `super`

Sir does **not** want the `Student` constructor to re-do the initialization of
`name` and `age` — the parent constructor already exists for exactly that job.
So the `Student` constructor calls **`super(name, age)`**, which runs
`Person`'s constructor and sets `name` and `age` from the values passed in
(`"Durga"`, `48`).

**Who initializes `name` and `age`?** The parent constructor — not any
assignment statement written in the child constructor.

```java
class Person {
    String name;
    int age;

    Person(String name, int age) {
        this.name = name; // performed by the parent constructor
        this.age = age;
    }
}

class Student extends Person {
    int rollNo;
    int marks;

    Student(String name, int age, int rollNo, int marks) {
        super(name, age); // parent constructor runs here
        // child-specific fields next...
    }
}
```

## 06:32 — Child constructor initializes the child-specific properties

After `super(...)` returns, the remaining two properties — `rollNo` and
`marks` — are initialized by the child constructor itself:

```java
class Student extends Person {
    int rollNo;
    int marks;

    Student(String name, int age, int rollNo, int marks) {
        super(name, age);       // parent takes name + age
        this.rollNo = rollNo;   // performed by the child constructor
        this.marks = marks;     // performed by the child constructor
    }
}
```

| Properties | Initialized by |
|---|---|
| `name`, `age` (from parent) | Parent constructor |
| `rollNo`, `marks` (child-specific) | Child constructor |

---

## 07:29 — Answering the core question

- How many objects did we create? **Only one** — the `Student` object.
- How many properties does that one object have? **Four** — name, age, rollNo,
  marks.

Whenever a student object is created, the **child** constructor runs to perform
initialization. For the properties **coming from the parent**, the parent
constructor does the initializing; the remaining child-specific properties are
initialized by the child constructor.

**Both** parent and child constructors are responsible for initializing only
**the one child class object** — its complete set of instance variables, both
inherited and its own.

**Is a parent object created? No.** Parent properties simply come to the child;
to initialize *those* properties, the parent constructor is executed on the
child object.

## 08:48 — Board rule

> Whenever we are creating a **child class object**, automatically the
> **parent constructor will be executed** to perform **initialization** for the
> **instance variables which are inheriting from the parent**.

```java
// Rule (conceptual):
// new Child(...)  →  Child constructor starts running
//                 →  super(...) (explicit or compiler-inserted) runs first
//                 →  Parent constructor initializes the inherited fields
//                 →  rest of Child constructor initializes child-specific fields
//                 →  still only ONE object: the Child
```

## 10:12 — Compact restatement

- Parent constructor → initialization of **parent-specific** properties (on the
  child object).
- Child constructor → initialization of **child-specific** properties.

**Parent constructor executed ≠ parent object created.** The parent constructor
runs for the **child object's** sake only.

## 11:25 — The diagram to keep

```java
Student s = new Student("Durga", 48, 101, 90);
// after construction, on that one object:
// name   = "Durga"   // by the parent constructor
// age    = 48        // by the parent constructor
// rollNo = 101        // by the child constructor
// marks  = 90         // by the child constructor
```

Full picture, matching the board:

```java
class Person {
    String name;
    int age;

    Person(String name, int age) {
        this.name = name; // performed by the parent constructor
        this.age = age;   // performed by the parent constructor
    }
}

class Student extends Person {
    int rollNo;
    int marks;

    Student(String name, int age, int rollNo, int marks) {
        super(name, age);      // parent constructor: name + age
        this.rollNo = rollNo;  // performed by the child constructor
        this.marks = marks;    // performed by the child constructor
    }
}

class Test {
    public static void main(String[] args) {
        Student s = new Student("Durga", 48, 101, 90);
        System.out.println(s.name + " " + s.age + " " + s.rollNo + " " + s.marks);
        // prints: Durga 48 101 90
    }
}
```

> ⚠️ **Modern Java — records generate exactly this boilerplate, but can't stand in for it here.**
> Since **Java 16**, a `record Person(String name, int age) { }` auto-generates a
> canonical constructor that does precisely what `Person`'s constructor above
> does by hand — assign each parameter to the matching field. For a plain,
> immutable data holder that would be less code to write.
>
> It does not fit *this* lecture's shape, though: a record is implicitly
> `final` and cannot extend another class or be extended (it only ever extends
> the hidden `java.lang.Record`), so `Student` could not `extends Person` if
> `Person` were a record. Confirmed by compiling:
> ```text
> record Student(...) extends Person {}
> // error: '{' expected  — a record header cannot say `extends <class>`
> ```
> The parent/child constructor chaining this video teaches is specifically a
> **class**-inheritance mechanic; records solve the "boilerplate constructor for
> a data holder" problem in the no-inheritance case only.

## 13:43 — Interview / board Q1

**Q:** In the program above, both parent and child constructors executed — for
what?

**A:** Both executed for **child object initialization only** — not because a
separate parent object was created.

```java
// Q: both Parent and Student constructors ran when we did:
Student s = new Student("Durga", 48, 101, 90);
// A: they ran for child-object initialization only
//    — not because a separate Parent object was created
```

## 14:36 — Final repeat

Whenever a **child class object** is created:

- **Parent object created?** → **No.**
- **Parent constructor executed?** → **Yes**, for initialization of the
  **child** object only.
- **For which variables?** → Whatever variables come from the parent; the
  **parent constructor** takes care of those.

**Final one-liner:** whenever we create a child class object, what is the need
of executing the parent class constructor? — this whole story: initializing the
inherited instance variables, on the child object.

---

## Exam and interview points

1. **Creating `new Student(...)` creates one object — a `Student` — never a
   separate `Person` object.** Nothing in Java's object model allocates a
   standalone superclass instance during subclass construction.
2. **The parent constructor still runs**, via an explicit `super(...)` call or
   an implicit compiler-inserted `super()`, and its job is to initialize the
   **inherited** fields on that one object.
3. **The child constructor initializes only the fields declared in the child
   class** — the ones the parent constructor didn't already handle.
4. **"Parent constructor executed" is not "parent object created."** This is
   the loophole OCJP tests and the one interviewers phrase as "does
   inheritance create a hidden parent object?" — the answer is no.
5. **Constructors are never inherited.** `Student` does not inherit `Person`'s
   constructor as a member; it can only *call* it via `super(...)`, which is
   why `Student` must declare its own constructor to accept and forward
   `name`/`age`.
6. **Records (Java 16+)** auto-generate this exact "assign each constructor
   parameter to a field" boilerplate for plain data carriers — but a record
   cannot extend a class, so it cannot replace this parent/child chaining
   pattern; it only replaces the *non-inherited* version of the same problem.

---

**Next:** Video 046 — Child object vs parent constructor (part 2)
