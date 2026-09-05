# Video 131

## Video info

### 00:04 — Session opening: why SerialVersionUID was added to the course

- This is the last concept in the Serialization series (Part 7).
- Durga Sir admits he did not cover serialVersionUID in earlier batches.
- When students asked "Sir, what is serialVersionUID?", his standard reply was: "It is internally required by the JVM; as a programmer we are not required to worry."
- One day a student came back and said: "Sir, in today's interview I faced this question."
- From that batch onward, Durga Sir added this topic — and while preparing it, he felt: "Why did I miss such a worthy concept for so many days?"
- Important framing: The concept is theoretical and students may feel bored — but it is very worthy for interviews and real distributed systems. Take special care.
### 02:39 — What is the role of serialVersionUID?

Before diving into UID, Durga Sir establishes three prerequisite conclusions from the ~10 serialization programs already covered in the classroom.

### 02:54 — Prerequisite #1: Sender and receiver need NOT be the same

Classroom demo context (same person, same machine):

- In the classroom, one person serializes on one machine, and the same person deserializes on the same machine.
- Person = same, mission (machine) = same, location = same.
Real-world distributed context (different person, different machine):

London (UK)                              Hyderabad (India)
┌─────────────────┐                      ┌─────────────────┐
│ Person A        │                      │ Person B        │
│ Windows / JVM   │  ── abc.ser file ──► │ Linux / JVM     │
│ Serializes Dog  │   (remote transfer)  │ Deserializes Dog│
└─────────────────┘                      └─────────────────┘

- Person A in London serializes an object to a file.
- Person B in Hyderabad receives the file (even a remote file) and tries to deserialize.
- Sender and receiver are different persons, different missions (machines), different locations.
Board conclusion (Point #1):

In serialization, both the sender and receiver:

- Need not be the same person

- Need not use the same mission (machine)

- Need not be from the same location

The person may be different, the missions may be different, and the locations may be different.

### 07:40 — Prerequisite #2: Which code runs where?

Sender-side code (serialization):

Dog d1 = new Dog();                                    // create object
FileOutputStream fos = new FileOutputStream("abc.ser");
ObjectOutputStream oos = new ObjectOutputStream(fos);
oos.writeObject(d1);                                   // serialize

Receiver-side code (deserialization):

FileInputStream fis = new FileInputStream("abc.ser");
ObjectInputStream ois = new ObjectInputStream(fis);
Dog d2 = (Dog) ois.readObject();                       // deserialize

- First block = sender code (runs on sender machine).
- Second block = receiver code (runs on receiver machine).
### 09:36 — Prerequisite #3: `.class` file must exist on BOTH machines

On sender machine — to create `Dog d1`:

- Compulsory: Dog.class must be available.
- Without Dog.class, you cannot compile or create a Dog object → cannot serialize.
On receiver machine — to declare `Dog d2`:

- Compulsory: Dog.class must be available.
- Without Dog.class, the receiver code will not even compile (reference variable type Dog requires the class).
Critical conclusion:

In serialization, the .class file must be present on both sender and receiver missions at the beginning (before serialization/deserialization).

What travels from sender to receiver? Only the state of the object — NOT the .class file.

Common mistake (interview trap):

- Many people think the .class file also travels over the network.
- Wrong. Receiver must already have the same class definition locally.
### 12:08 — Analogy: why not just `new Dog()` on the receiver side?

Dog class (both machines have this `.class` file):

```java
class Dog implements Serializable {
    int i = 10;
    int j = 20;
}
```

Scenario:

- Sender creates Dog d1 → i=10, j=20.
- Sender communicates with a database and updates state → i=38, j=39.
- Sender serializes the object (current state: i=38, j=39).
- Receiver gets the file.
Student doubt: "If receiver also has `Dog.class`, why not just `new Dog()` directly? Default values would be `i=10, j=20` anyway."

Answer:

- Receiver can create a new object with default values (i=10, j=20).
- But receiver cannot get the sender's updated state (i=38, j=39) without deserialization.
- Receiver may not have database credentials or access permissions to connect to sender's database.
- Serialization shares the updated state that only the sender had access to.
Board conclusion (repeated for notes):

In serialization, both sender and receiver should have the .class file at the beginning only.

Just the state of the object is traveling from sender to receiver. That's all.

### 16:18 — Prerequisite #4: Unique identity number at serialization time

Internal JVM behavior at serialization time:

- With every object being serialized, the JVM assigns a unique identity number.
- Who assigns it? JVM.
- How does JVM get this number? JVM generates it by analyzing the `.class` file` (structure, fields, methods, etc.).
- This unique identity number is saved into the serialized file along with the object.
At deserialization time (receiver side JVM):

- JVM reads the unique identity number from the file: "This object belongs to `Dog` class; its unique identifier is 101."
- Receiver-side JVM generates its own unique identifier for the local Dog.class file.
- If both numbers match (101 == 101) → deserialization proceeds happily.
- If numbers do NOT match (101 != 103) → JVM refuses: "This is not a valid object of this class" → `InvalidClassException` at runtime.
This unique identity number IS `serialVersionUID`.

### 19:20 — serialVersionUID defined

Why programmers often ignore it:

- Everything is handled internally by the JVM.
- Programmer does not explicitly write or compare the number.
- That is why Durga Sir previously said "not required for the programmer" — but interviewers do ask.
Board notes (central point):

At time of serialization:
  → With every object, sender-side JVM saves a unique identifier.
  → JVM generates this identifier based on that .class file.

At time of deserialization:
  → Receiver-side JVM compares unique identifier in file
    with unique identifier of local .class file.
  → If both match → deserialization performed.
  → Otherwise → InvalidClassException (runtime).

### 24:42 — OCJP course ID card analogy

Durga Sir uses the SCJP classroom registration analogy:

- You pay the fee and receive an ID card with a unique number (e.g., ID #107).
- At the classroom door, Instructor Sinjad asks: "Which class? SCJP? Show your ID card."
- He checks his register: "ID 107 belongs to which name?"
- If ID matches → allowed to enter class (deserialization succeeds).
- If photo on ID was replaced / ID doesn't match → "Not a valid student" → not allowed (InvalidClassException).
### 26:36 — Who generates serialVersionUID?

### 26:52 — Problems with DEFAULT (JVM-generated) serialVersionUID

Durga Sir warns: Do NOT depend on the default serialVersionUID generated by JVM. There are three problems.

#### Problem #1 — Different JVM / OS / vendor generates different UID

Scenario:

- Same .class file (bytecode identical).
- But sender JVM generates UID 111, receiver JVM generates UID 112.
- File says 111, local class says 112 → mismatch → receiver unable to deserialize.
Board conclusion (Problem #1):

If we depend on default serialVersionUID generated by JVM:

Both sender and receiver should use the same JVM with respect to:

- Vendor

- Platform (OS)

- Version

Otherwise receiver unable to deserialize because of different serialVersionUIDs.

- Sender in UK cannot force receiver in India to use Windows + JVM 1.6.
- This makes default UID unreliable in distributed / cross-platform systems.
#### Problem #2 — Class file modified after serialization

Scenario (same JVM on both sides — still fails):

- Sender and receiver both use same Windows + JVM 1.6.
- Sender serializes Dog with int i=10; int j=20; → file UID = 111.
- After serialization, someone modifies Dog.class on receiver side — adds int k=30;.
- Receiver JVM now generates UID 113 for the updated class (new field = different structure).
- File still has UID 111, local class has 113 → mismatch → InvalidClassException.
Board conclusion (Problem #2):

Both sender and receiver should use the same `.class` file version.

After serialization, if there is any change in .class file at receiver side → receiver unable to deserialize.

This is extremely common in real projects: you serialize today, deploy a new version of the class tomorrow, try to read old .ser files → crash.

#### Problem #3 — Performance impact

- To generate default serialVersionUID, JVM uses a complex algorithm.
- It must analyze every property (field, method signature, etc.) in the .class file.
- For every object serialized: generate UID + save it.
- For every object deserialized: generate local UID + compare.
- This may create performance problems on high-throughput systems.
Board note:

To generate serialVersionUID, internally JVM may use a complex algorithm, which may create performance problems.

### 39:40 — Solution: Configure your OWN serialVersionUID

Simple rule: Don't depend on JVM-generated UID. Configure your own.

private static final long serialVersionUID = 1L;

- If you declare this in your class, JVM will NOT generate its own — it always uses your number.
- All three problems above are solved.
### 42:26 — Demo Program 1: Default UID — class modification breaks deserialization

Three files:

#### `Dog1.java` (initial version)

```java
import java.io.Serializable;

class Dog1 implements Serializable {
    int i = 10;
    int j = 20;
}
```

#### `Sender.java`

```java
import java.io.*;

class Sender {
    public static void main(String[] args) throws Exception {
        Dog1 d1 = new Dog1();
        FileOutputStream fos = new FileOutputStream("abc.ser");
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(d1);
        System.out.println("Serialization completed");
    }
}
```

#### `Receiver.java`

```java
import java.io.*;

class Receiver {
    public static void main(String[] args) throws Exception {
        FileInputStream fis = new FileInputStream("abc.ser");
        ObjectInputStream ois = new ObjectInputStream(fis);
        Dog1 d2 = (Dog1) ois.readObject();
        System.out.println(d2.i + "..." + d2.j);
    }
}
```

Step 1 — Compile all (same class version):

javac Dog1.java
javac Sender.java Dog1.java
javac Receiver.java Dog1.java

Step 2 — Serialize:

java Sender
# Output: Serialization completed

Step 3 — Deserialize (no changes yet):

java Receiver
# Output: 10...20   ← works fine

Step 4 — Modify `Dog1.java` AFTER serialization (add field `k`):

```java
class Dog1 implements Serializable {
    int i = 10;
    int j = 20;
    int k = 30;   // NEW field added after .ser file was created
}
```

Step 5 — Recompile and try deserialize:

javac Dog1.java
java Receiver

Result:

Exception in thread "main" java.io.InvalidClassException: Dog1;
local class incompatible: stream classdesc serialVersionUID = <old>, local class serialVersionUID = <new>

- File contains old UID (generated when class had 2 fields).
- Local class has new UID (generated after adding k).
- Mismatch → InvalidClassException.
### 46:50 — Demo Program 2: Custom UID — class modification still works

Modify `Dog1.java` — declare explicit UID BEFORE adding fields:

```java
import java.io.Serializable;

class Dog1 implements Serializable {
    private static final long serialVersionUID = 1L;   // OUR number, not JVM's

    int i = 10;
    int j = 20;
}
```

Sender serializes → file stores UID = `1L`.

Then modify class (add more fields):

```java
class Dog1 implements Serializable {
    private static final long serialVersionUID = 1L;   // SAME value kept

    int i = 10;
    int j = 20;
    int k = 30;
    int l = 40;
}
```

At deserialization:

- File UID = 1L
- Local class UID = 1L (declared constant, not regenerated)
- Both match → deserialization succeeds even with extra fields.
Compile, serialize, modify, deserialize:

javac Dog1.java
javac Sender.java Dog1.java
java Sender
# Modify Dog1.java — add k, l — keep serialVersionUID = 1L
javac Dog1.java
javac Receiver.java Dog1.java
java Receiver
# Output: 10...20   ← works! (k, l get default 0 if not in file)

Key teaching point:

- Even though class structure changed (2 fields → 4 fields), deserialization works because UIDs match.
- Extra fields (k, l) get default values (0) since they were not in the original serialized stream.
### 50:59 — How to configure serialVersionUID (syntax)

Exact declaration (board line — memorize for exam):

private static final long serialVersionUID = 1L;

Rules:

- Must be declared inside the class that implements Serializable.
- JVM checks: "Does current class contain serialVersionUID?"
- Yes → use declared value; do not run generation algorithm.
- No → JVM generates one based on class structure.
### 57:23 — After configuring custom UID: what is NO LONGER required?

Once you set your own serialVersionUID:

Board conclusion:

We can solve / overcome the above problems by configuring our own serialVersionUID.

### 58:43 — IDE behavior (Eclipse and others)

- Modern IDEs (Eclipse, IntelliJ, etc.) prompt the programmer to enter serialVersionUID explicitly when a class implements Serializable.
- Warning message类似: "If you depend on JVM-generated serialVersionUID there may be a problem."
- Some IDEs automatically generate the line when you create a Serializable class:
private static final long serialVersionUID = 8929389482398234L;

- That auto-generated long value is IDE's calculation (similar to what JVM would do once) — you can replace it with your own simple value like 1L if you prefer stability across versions.
Board note:

Some IDEs prompt programmer to enter serialVersionUID explicitly.

Some IDEs may generate serialVersionUID automatically.

### 1:00:56 — Session summary: one line, big story

Durga Sir's closing message:

"Just only one line, this much story."

"Don't depend on default serialVersionUID."

"Whenever we take a class that implements Serializable, it is recommended to add this line so these problems are overcome by default."

With this video, the Serialization topic is complete (Parts 1–7).

## Complete demo program (consolidated — custom UID)

```java
// ========== Dog1.java ==========
import java.io.Serializable;

class Dog1 implements Serializable {
    private static final long serialVersionUID = 1L;

    int i = 10;
    int j = 20;
    // After serialization you MAY add: int k = 30; int l = 40;
}

// ========== Sender.java ==========
import java.io.*;

class Sender {
    public static void main(String[] args) throws Exception {
        Dog1 d1 = new Dog1();
        FileOutputStream fos = new FileOutputStream("abc.ser");
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(d1);
        System.out.println("Serialization completed");
    }
}

// ========== Receiver.java ==========
import java.io.*;

class Receiver {
    public static void main(String[] args) throws Exception {
        FileInputStream fis = new FileInputStream("abc.ser");
        ObjectInputStream ois = new ObjectInputStream(fis);
        Dog1 d2 = (Dog1) ois.readObject();
        System.out.println("i=" + d2.i + ", j=" + d2.j);
    }
}
```

Execution flow:

javac Dog1.java Sender.java Receiver.java
java Sender          # creates abc.ser with UID=1L, i=10, j=20
# (optional) modify Dog1.java — add fields, keep serialVersionUID=1L
javac Dog1.java Receiver.java
java Receiver        # i=10, j=20 — success

## Quick reference

### serialVersionUID lifecycle

SERIALIZATION (sender JVM)                    DESERIALIZATION (receiver JVM)
─────────────────────────                    ───────────────────────────────
1. Object created                            1. Read .ser file
2. JVM checks: serialVersionUID declared?    2. Read UID from file (e.g. 1L)
   YES → use 1L                               3. JVM checks local class:
   NO  → generate from .class analysis           serialVersionUID declared?
3. Save UID + object state into file              YES → use 1L
                                                  NO  → generate from .class
                                               4. Compare: file UID == local UID?
                                                  YES → deserialize
                                                  NO  → InvalidClassException

### Three problems of default UID vs one-line fix

### InvalidClassException — when it occurs

### Exam / interview one-liners

- What is serialVersionUID? — Unique identity number for a Serializable class, used to verify compatibility at deserialization.
- Who generates it by default? — JVM, based on class structure (fields, methods, etc.).
- Who compares it? — Receiver-side JVM at deserialization time.
- What if mismatch? — InvalidClassException (unchecked / runtime).
- How to declare? — private static final long serialVersionUID = 1L;
- Why declare explicitly? — Avoid cross-JVM, cross-version, and post-serialization class-change failures.
- Does `.class` file travel in serialization? — No. Only object state travels. Class must exist on both sides beforehand.
- Can sender and receiver be different machines? — Yes. Person, machine, and location can all differ.
### Relationship to prior serialization videos (121–130)

## Board notes (verbatim-style for revision)

Point 1 — Distributed serialization:

In serialization, both sender and receiver need not be the same person, need not use the same mission, need not be from the same location.

Point 2 — Class file vs state:

Both sender and receiver should have .class file at the beginning only. Just the state of object is traveling from sender to receiver.

Point 3 — UID at serialization:

At time of serialization, with every object, sender-side JVM will save a unique identifier. JVM generates this based on that .class file.

Point 4 — UID at deserialization:

At time of deserialization, receiver-side JVM compares unique identifier associated with object with local class unique identifier. If both matched → deserialization. Otherwise → InvalidClassException.

Point 5 — Problems of default UID:

1. Both sender and receiver should use same JVM (vendor, platform, version).

2. Both should use same .class file version; any change after serialization → fail.

3. JVM complex algorithm → performance problems.

Point 6 — Solution:

Configure our own serialVersionUID: private static final long serialVersionUID = 1L;

Point 7 — After custom UID:

Sender and receiver not required to maintain same JVM versions.

Java code block count: 8

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Playlist | Core Java With OCJP/SCJP |  |  |
| Position | 131 of 203 |  |  |
| Title | Serialization Part-7 \ | \ | SerialVersion UID |
| Instructor | Durga Sir |  |  |
| Duration | 1h 01m 39s |  |  |
| Video ID | 2kGvax307EM |  |  |
| Watch | https://www.youtube.com/watch?v=2kGvax307EM |  |  |
| Notes source | Local Whisper STT |  |  |

| What travels? | Answer |
|---|---|
| .class file | NO — must already exist on both sides |
| Object state (instance variable values) | YES — this is what serialization transfers |

| Term | Meaning |
|---|---|
| serialVersionUID | Unique identity number associated with a serializable class |
| Generated by | JVM (by default), based on .class file analysis |
| Saved when | At serialization time (embedded in .ser file) |
| Compared when | At deserialization time (file UID vs local class UID) |
| Match | Deserialization succeeds |
| Mismatch | InvalidClassException at runtime |

| Analogy | Serialization |
|---|---|
| ID card number | serialVersionUID in .ser file |
| Register at door | Local .class file UID generated by receiver JVM |
| Match → enter class | Match → deserialize |
| Mismatch → rejected | Mismatch → InvalidClassException |

| Question | Answer |
|---|---|
| Who generates? | JVM |
| Based on what? | That `.class` file (analyzes class structure) |
| Who compares? | JVM (receiver side) |
| Programmer role? | None (unless you configure your own) |

| Side | OS | JVM Version | Generated UID for same Dog.class |
|---|---|---|---|
| Sender | Windows | 1.6 | 111 |
| Receiver | Linux | 1.8 | 112 |

| Problem | How custom UID fixes it |
|---|---|
| Different JVM/OS/version | Both sides use your 1L, not JVM-calculated values |
| Class file modified after serialization | UID stays 1L even if you add fields (as long as you keep the same declared UID) |
| Performance | No complex algorithm — JVM just reads your constant |

| Modifier | Required? | Reason |
|---|---|---|
| private | Yes (convention) | Implementation detail of serialization |
| static | Yes | Belongs to class, not instance |
| final | Yes | Must never change once assigned |
| long | Yes | UID is a 64-bit long value |
| 1L | Example | Any long literal; 1L is common convention |

| Requirement | Still needed? |
|---|---|
| Same JVM version on sender & receiver | NO — your UID is used, not JVM-generated |
| Same OS / platform | NO |
| Same JVM vendor | NO |
| Same .class file version (no changes ever) | NO — you can add fields if UID stays same |
| Performance impact from UID algorithm | NO — constant lookup only |

| # | Problem (default JVM UID) | Fix (custom UID) |
|---|---|---|
| 1 | Different JVM vendor/platform/version → different UID → deserialize fails | Declare private static final long serialVersionUID = 1L; on both sides |
| 2 | Class modified after serialization → new UID → deserialize fails | Keep same declared UID even after adding/removing fields |
| 3 | JVM runs complex algorithm per object → performance hit | Constant value — no algorithm needed |

| Condition | Result |
|---|---|
| File UID == Local class UID | Deserialization OK |
| File UID != Local class UID | InvalidClassException |
| Local class not found at all | ClassNotFoundException (different exception) |

| Video | Topic | Link to 131 |
|---|---|---|
| 125 | Serialization intro | Foundation — Serializable marker interface |
| 126 | Serialization Part 2 | transient, static fields |
| 127 | Customized serialization | writeObject / readObject |
| 130 | Externalization | Separate mechanism; also implements Serializable hierarchy |
| 131 | serialVersionUID | Compatibility check at deserialize time |
