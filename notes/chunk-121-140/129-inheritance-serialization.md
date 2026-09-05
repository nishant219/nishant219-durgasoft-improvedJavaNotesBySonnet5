# Video 129

## Video info

### Topic placement in serialization syllabus

This video is Part 5 of serialization. Prior videos covered introduction, object graphs, customized serialization, etc. This lecture covers serialization with respect to inheritance — two cases with four important rules ("loopholes") that frequently appear on SCJP/OCJP exams.

## 00:05 — Introduction: Serialization with respect to inheritance

Durga Sir opens by asking students what the next topic is:

Serialization with respect to inheritance

There are two cases under this topic:

Sir writes both cases on the board and works through each with live demos (SerializeDemo5, SerializeDemo6).

# CASE 1 — Parent is Serializable, Child is NOT Serializable

## 01:00 — Class hierarchy setup (Case 1)

```java
class Animal implements Serializable {
    int i = 10;
}

class Dog extends Animal {   // does NOT implement Serializable
    int j = 20;
}
```

Inheritance diagram (board):

Animal  (implements Serializable)
           |
           i = 10
           |
        Dog   (does NOT implement Serializable)
           |
           j = 20

Key observation from Sir:

- Parent class Animal → implements Serializable ✓
- Child class Dog → does NOT implement Serializable ✗
## 02:04 — Creating and serializing a Dog object

Dog d1 = new Dog();
// d1.i = 10  (inherited from Animal)
// d1.j = 20  (defined in Dog)

Object state in heap (before serialization):

Serialization code:

```java
FileOutputStream fos = new FileOutputStream("abc.ser");
ObjectOutputStream oos = new ObjectOutputStream(fos);
oos.writeObject(d1);
```

Deserialization code:

```java
FileInputStream fis = new FileInputStream("abc.ser");
ObjectInputStream ois = new ObjectInputStream(fis);
Dog d2 = (Dog) ois.readObject();

System.out.println(d2.i + ".." + d2.j);
```

## 03:52 — Quiz: Is this code valid?

Sir asks the class: Is the above program valid or invalid?

Many students feel it is invalid because:

- They are trying to serialize a Dog object
- Dog class does not implement Serializable
- So how can serialization work?
Sir's answer: 100% VALID — no problem at all.

## 05:28 — Core rule for Case 1 (board conclusion)

If the parent implements `Serializable`, then automatically every child by default implements `Serializable`.

Serializable nature is inheriting from parent to child.

Formal board notes (Case 1):

If a parent is Serializable,
    then by default every child is Serializable.

Serializable nature is inheriting from parent to child.

Even though child class does not implement Serializable, we can serialize child class object — because the parent (Animal) already implements Serializable.

## 06:01 — Live demo: `SerializeDemo5.java`

```java
import java.io.*;

class Animal implements Serializable {
    int i = 10;
}

class Dog extends Animal {
    int j = 20;
}

class SerializeDemo5 {
    public static void main(String[] args) throws Exception {
        Dog d1 = new Dog();
        System.out.println(d1.i + ".." + d1.j);   // 10..20

        // Serialization
        FileOutputStream fos = new FileOutputStream("abc.ser");
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(d1);

        // Deserialization
        FileInputStream fis = new FileInputStream("abc.ser");
        ObjectInputStream ois = new ObjectInputStream(fis);
        Dog d2 = (Dog) ois.readObject();
        System.out.println(d2.i + ".." + d2.j);   // 10..20
    }
}
```

Compile: ✓ fine

Run output:

10..20
10..20

Conclusion: Even though Dog does not implement Serializable, serialization and deserialization work perfectly because `Animal` (parent) implements `Serializable`.

## 14:12 — Case 1 summary (board point)

In the above example, even though Dog class does not implement Serializable, we can serialize Dog object because it is parent — `Animal` class implements `Serializable`.

## 15:28 — Important doubt: Does `Object` implement Serializable?

Sir raises a critical exam/interview question:

Object class implements Serializable or not?

If `Object` implemented `Serializable`:

- Every class in Java extends Object
- Therefore every Java class would automatically be serializable
- Then why would we need to explicitly write implements Serializable?
Answer (take a note):

Object class does NOT implement Serializable interface.

Implication: Serializable is not inherited from Object. Only when a class (or its ancestor) explicitly implements Serializable does the serializable nature propagate down the hierarchy.

## 16:45 — Case 1 recap (student spell-out)

Sir asks students to repeat Case 1:

- If parent class is Serializable → by default every child class is Serializable
- Serializable nature inherits from parent to child
- Child need not declare implements Serializable explicitly
# CASE 2 — Parent is NOT Serializable, Child IS Serializable

## 17:09 — Class hierarchy setup (Case 2)

```java
class Animal {                    // does NOT implement Serializable
    int i = 10;
}

class Dog extends Animal implements Serializable {
    int j = 20;
}
```

Inheritance diagram (board):

Animal  (NOT Serializable)
           |
           i = 10
           |
        Dog   (implements Serializable)
           |
           j = 20

Key observation:

- Parent Animal → NOT Serializable
- Child Dog → implements Serializable
## 18:32 — Quiz: Can we serialize Dog object now?

Sir asks: Is it possible to serialize child class object?

Some students think: "To serialize child class object, parent class should be Serializable — is that a rule?"

Sir's answer: NO such rule exists.

Reasoning:

- For all Java classes, the ultimate parent is Object
- Object does not implement Serializable
- If the rule were "parent must be Serializable to serialize child," we could never serialize any Java object
- Therefore: parent need NOT be Serializable to serialize a child that implements Serializable
## 19:49 — Rule 1 (Case 2, Point 1)

Even though parent class doesn't implement Serializable, we can serialize child class object if child class implements Serializable interface.

Formal board notes:

To serialize child class object,
    parent class need NOT be Serializable.

There is NO rule that says: "To serialize child class object, compulsory parent class should be Serializable."

If child class implements Serializable → child object can be serialized regardless of parent's serializable status.

## 21:28 — Setting up the tricky example (Case 2 demo)

Sir creates a Dog object and changes field values before serialization:

Dog d1 = new Dog();
// Initially: i = 10, j = 20

d1.i = 39;   // change inherited field
d1.j = 39;   // change child field
// Now: i = 39, j = 39

Serialization:

```java
FileOutputStream fos = new FileOutputStream("abc.ser");
ObjectOutputStream oos = new ObjectOutputStream(fos);
oos.writeObject(d1);
```

Deserialization:

```java
System.out.println("Deserialization started");

FileInputStream fis = new FileInputStream("abc.ser");
ObjectInputStream ois = new ObjectInputStream(fis);
Dog d2 = (Dog) ois.readObject();

System.out.println(d2.i + ".." + d2.j);
```

## 24:53 — Expected output quiz (the trap)

Students naively expect:

39..39

Sir says: "I am sure we are NOT going to get 39..39."

There are loopholes (special JVM rules) at serialization and deserialization time.

## 25:36 — Rule 2 (Case 2, Point 2): At serialization time

At the time of serialization, JVM will check: is any variable inheriting from non-serializable parent?

If any variable is inheriting from non-serializable parent, then JVM ignores original value and saves default value to the file.

Which variable comes from non-serializable parent?

→ `i` (declared in Animal, which is NOT Serializable)

What happens to `i` at serialization?

Formal board notes:

At the time of serialization:

If any variable inheriting from non-serializable parent,
    then JVM ignores original value
    and saves default value to the file.

Naive expectation after Rule 2 alone: output would be 0..39

Sir again warns: "We are NOT going to get 0..39 either." There is another twist at deserialization.

## 29:55 — Rule 3 (Case 2, Point 3): At deserialization time (the twist)

At the time of deserialization, JVM will check: is any parent class non-serializable?

If any parent class is non-serializable, then JVM will execute instance control flow in every non-serializable parent and share its instance variables to the current object.

### What is Instance Control Flow (ICF)?

Sir defines instance control flow as three steps:

- Identification of instance members
- Execution of instance variable assignments and instance blocks
- Execution of constructor
At deserialization, for each non-serializable parent (`Animal`):

- JVM runs instance control flow in Animal
- This effectively re-initializes parent's instance variables
- Parent's instance variables are shared/assigned to the current deserialized object
For `Animal`:

- Instance variable i gets its default initialization value = 10 (from int i = 10;)
- NOT 0 (that was only what went to the file)
- NOT 39 (that was never saved)
For `Dog`:

- j = 39 comes from the file (child is serializable)
Final output:

10..39

Formal board notes:

At the time of deserialization:

If any parent class is non-serializable,
    then JVM will execute instance control flow
    in every non-serializable parent
    and share its instance variables to the current object.

## 33:52 — Rule 4 (Case 2, Point 4): No-arg constructor requirement

Question: Who is responsible for executing instance control flow in non-serializable parent?

→ JVM

As part of instance control flow, JVM will always call no-argument constructor.

Therefore:

Every non-serializable class should compulsory contain no-argument constructor.

The no-arg constructor may be:

- Default constructor generated by compiler (if programmer writes no constructor), OR
- Explicitly provided by the programmer
If non-serializable parent does NOT contain no-arg constructor:

→ Runtime exception: `InvalidClassException`

Formal board notes:

While executing instance control flow of non-serializable parent,
    JVM will always call no-argument constructor.

Hence every non-serializable class should compulsory contain
    no-argument constructor.

    (default constructor generated by compiler
     OR explicitly provided by programmer)

Otherwise → RuntimeException: InvalidClassException

## 38:50 — Four rules recap (harmonic conclusions)

Sir asks students to read back all four points:

## 40:15 — Enhanced demo with constructor SOPs: `SerializeDemo6.java`

Sir adds constructor print statements to prove instance control flow runs at deserialization:

```java
import java.io.*;

class Animal {
    int i = 10;

    Animal() {
        System.out.println("Animal constructor called");
    }
}

class Dog extends Animal implements Serializable {
    int j = 20;

    Dog() {
        System.out.println("Dog constructor called");
    }
}

class SerializeDemo6 {
    public static void main(String[] args) throws Exception {
        Dog d1 = new Dog();
        d1.i = 39;
        d1.j = 39;

        // Serialization
        FileOutputStream fos = new FileOutputStream("abc.ser");
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(d1);

        System.out.println("Deserialization started");

        // Deserialization
        FileInputStream fis = new FileInputStream("abc.ser");
        ObjectInputStream ois = new ObjectInputStream(fis);
        Dog d2 = (Dog) ois.readObject();

        System.out.println(d2.i + ".." + d2.j);
    }
}
```

## 42:00 — Output walkthrough (SerializeDemo6)

### Phase 1: Object creation (`new Dog()`)

When child object is created, both parent and child constructors execute (normal inheritance rule):

Animal constructor called
Dog constructor called

### Phase 2: Serialization

Object with i=39, j=39 is serialized silently (no extra output).

At serialization:

- i (from non-serializable Animal) → 0 saved to file
- j (from serializable Dog) → 39 saved to file
### Phase 3: Deserialization

Deserialization started
Animal constructor called        ← EXTRA line! (instance control flow)
10..39

Why "Animal constructor called" appears again at deserialization?

- At deserialization, JVM detects Animal is non-serializable
- JVM executes instance control flow in Animal
- Part of ICF → calls Animal() no-arg constructor → prints "Animal constructor called"
- Animal.i re-initialized to 10 and shared to d2
- Dog.j restored from file as 39
Note: Dog constructor called does NOT run again at deserialization (only the non-serializable parent's ICF runs).

## 51:21 — Final output diagram (board)

Animal constructor called     ← object creation
Dog constructor called        ← object creation
Deserialization started
Animal constructor called     ← ICF at deserialization (non-serializable parent)
10..39

Field values in d2 after deserialization:

## 53:05 — InvalidClassException demo: parameterized constructor in parent

Sir demonstrates what happens when non-serializable parent lacks a no-arg constructor:

```java
class Animal {
    int i = 10;

    Animal(int x) {    // ONLY parameterized constructor — NO no-arg constructor
        this.i = x;
        System.out.println("Animal constructor called");
    }
}

class Dog extends Animal implements Serializable {
    int j = 20;

    Dog() {
        super(10);     // must call super — otherwise compile error
        System.out.println("Dog constructor called");
    }
}
```

Compile: ✓ fine (because Dog() calls super(10))

Run — up to serialization: works fine

At deserialization:

Deserialization started
Exception in thread "main" java.io.InvalidClassException: ...
    no valid constructor

Why?

- At deserialization, JVM needs to run ICF in non-serializable Animal
- ICF requires calling no-argument constructor of Animal
- Animal has only Animal(int x) — no no-arg constructor exists
- → `InvalidClassException` at runtime
Key point: Code compiles and serialization succeeds; failure happens only at deserialization when JVM tries to invoke the missing no-arg constructor.

## 55:34 — End-of-lecture summary: Case 1 vs Case 2

Sir closes: "Serialization with respect to inheritance — Case 1 and Case 2 — that's all."

## Quick reference — All board conclusions

### Case 1

If parent implements Serializable,
    automatically every child implements Serializable.
Serializable nature is inheriting from parent to child.

Object class does NOT implement Serializable.

### Case 2 — Four rules

1. To serialize child class object,
       parent class need NOT be Serializable.

2. At serialization time:
       If any variable inheriting from non-serializable parent,
           JVM ignores original value
           and saves default value to the file.

3. At deserialization time:
       If any parent class is non-serializable,
           JVM executes instance control flow
           in every non-serializable parent
           and shares its instance variables to the current object.

4. While executing ICF of non-serializable parent,
       JVM always calls no-argument constructor.
   Hence every non-serializable class must contain no-arg constructor.
   Otherwise → InvalidClassException (runtime).

## Exam traps & interview one-liners

- "Dog doesn't implement Serializable — can we serialize it?"
- Case 1: Yes, if parent implements Serializable.
- Case 2: Yes, if child implements Serializable (parent need not).
- "What value of `i` after deserialization in Case 2?"
- NOT the value before serialization (39)
- NOT the default int value written to file (0)
- YES → value from parent's instance control flow (10)
- "Does Object implement Serializable?" → No.
- "When does InvalidClassException occur?"
- Non-serializable parent missing no-arg constructor
- Thrown at deserialization, not compile time
- "Which constructor runs at deserialization for non-serializable parent?"
- Only no-argument constructor (part of instance control flow)
- "Does child constructor run at deserialization in Case 2?"
- No — only non-serializable parent's ICF runs
- Child fields restored directly from file
## Programs covered in this video

## Connection to prior serialization videos

## Diagrams to copy for revision

### Case 1 — Serializable inheritance flow

Animal implements Serializable
    int i = 10
         ↓ extends (Serializable nature inherited)
Dog (no implements clause needed)
    int j = 20

Serialize Dog d1 → file stores i=10, j=20
Deserialize → Dog d2 → i=10, j=20  ✓

### Case 2 — Serialization + deserialization field lifecycle

BEFORE SERIALIZATION (heap):
    d1.i = 39, d1.j = 39

AT SERIALIZATION (what goes to file):
    i → 0  (default; original 39 ignored — from non-serializable Animal)
    j → 39 (from serializable Dog)

AT DESERIALIZATION:
    1. JVM detects Animal is non-serializable
    2. Runs ICF in Animal → Animal() called → i = 10
    3. Restores j = 39 from file
    RESULT: d2.i = 10, d2.j = 39

End of Video 129 notes — Serialization Part 5: Inheritance serialization (Case 1 & Case 2)

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Title | Core Java With OCJP/SCJP: Serialization Part- 5 \ | \ | Inheritance serialization |
| Position | 129 of 203 |  |  |
| Duration | 56m 02s |  |  |
| URL | https://www.youtube.com/watch?v=Y5KXGLbCzbc |  |  |
| Notes source | Local Whisper STT |  |  |
| Playlist block | Serialization unit — inheritance rules (Case 1 & Case 2) |  |  |

| Case | Parent | Child | Focus of this video |
|---|---|---|---|
| Case 1 | Implements Serializable | Does not implement Serializable | Serializable nature inherits parent → child |
| Case 2 | Does not implement Serializable | Implements Serializable | Four rules about parent fields, deserialization, and no-arg constructor |

| Variable | Value | Declared in |
|---|---|---|
| i | 10 | Animal (parent) |
| j | 20 | Dog (child) |

| Variable | Source | Serializable? | Saved to file |
|---|---|---|---|
| i = 39 | Animal (non-serializable parent) | Parent not serializable | Default value `0` (original 39 ignored) |
| j = 39 | Dog (serializable child) | Child is serializable | 39 (original value saved) |

| # | When | Rule |
|---|---|---|
| 1 | General | Even though parent doesn't implement Serializable, we can serialize child object if child implements Serializable. Parent need NOT be Serializable. |
| 2 | Serialization time | If any variable inheriting from non-serializable parent → JVM ignores original value, saves default value to file. |
| 3 | Deserialization time | If any parent is non-serializable → JVM executes instance control flow in every non-serializable parent and shares instance variables to current object. |
| 4 | Deserialization time | Non-serializable parent must have no-arg constructor; otherwise → InvalidClassException. |

| Field | Value | Why |
|---|---|---|
| d2.i | 10 | From ICF in non-serializable parent Animal (not 39, not 0) |
| d2.j | 39 | Restored from serialized file (child field) |

|  | Case 1 | Case 2 |
|---|---|---|
| Parent | Serializable | NOT Serializable |
| Child | NOT Serializable | Serializable |
| Can serialize child? | ✓ Yes (serializable nature inherited) | ✓ Yes (child implements Serializable) |
| Parent field at serialization | Saved normally | Default value saved (original ignored) |
| Parent field at deserialization | Restored from file | ICF runs in parent; parent vars re-initialized |
| No-arg constructor in parent | Not required for this rule | Compulsory (else InvalidClassException) |

| Program | Purpose | Key output |
|---|---|---|
| SerializeDemo5 | Case 1: parent Serializable, child not | 10..20 before and after |
| SerializeDemo6 | Case 2: parent not Serializable, child Serializable | Animal constructor called ×2, then 10..39 |
| SerializeDemo6 (variant) | Parent with only parameterized constructor | InvalidClassException: no valid constructor at deserialization |

| Video topic | Relevance to this lecture |
|---|---|
| Serialization intro (125) | Serializable marker interface, writeObject/readObject |
| Object graphs (126) | Inheritance is part of object graph structure |
| Customized serialization (127–128) | transient keyword — related but different rules |
| This video (129) | Inheritance-specific serialization rules |
| Externalization (130) | Alternative to serialization — next topic |
| serialVersionUID (131) | Version control for serialized classes |
