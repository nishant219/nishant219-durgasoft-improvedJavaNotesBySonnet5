# Video 125

## Video info

Title: Core Java With OCJP/SCJP: Serialization Part- 1 || Introduction

### 00:06 — Serialization syllabus for this playlist block

Topics to cover (in order):

- Introduction ← this video
- Object graphs in serialization
- Customized serialization
- Serialization with respect to inheritance
- Externalization
- serialVersionUID
Exam vs industry split:

- Classroom/industry often stops at introduction
- SCJP/OCJP: must know all serialization topics through inheritance + externalization + serialVersionUID
- Last two topics (externalization, serialVersionUID) are interview-oriented — not on SCJP exam per Sir, but compulsory to know the terminology and differences
### 03:23 — What is serialization? (common definitions first)

Students give typical answers (all acceptable in interviews, but not the strict definition):

Deserialization / de-serialization: reverse — read object from file or network.

Sir: these work at a general/top level, but strictly speaking there is a finer meaning.

### 05:05 — Balloon analogy (strict definition build-up)

Story setup: Kid studying in Bangalore calls father: "Send a big balloon — bigger than friend Ravi's balloon."

Father goes to shopping mall → asks for biggest balloon regardless of price → gets huge balloon (~₹1,500).

Problem: Cannot carry/send inflated balloon to Bangalore — not transport-supported form.

DTDC courier rejection:

- Cannot send money, gold, illegal items (courier rules)
- Balloon occupies huge space in flight cargo
- Needle/pressure can burst balloon in transit
- Verdict: "Not in transport-supported form"
Courier solution:

- Deflate balloon (remove air) → becomes small foldable piece
- Put in cover, write to/from address → ship for ~₹25–30
- Next day reaches Bangalore
- Kid must re-inflate at destination to use
Mapping to Java:

### 15:37 — Strict definitions (board)

Serialization (strict):

Process of converting an object from Java-supported form into either file-supported form OR network-supported form.

Deserialization (strict):

Process of converting an object from file or network supported form back into Java-supported form.

Loose vs strict:

- Loose: "writing object to file" / "sending across network"
- Strict: emphasizes form conversion — original Java object representation ≠ on-wire/on-disk representation
### 19:05 — Notes written under "Introduction → Serialization"

General definition (exam/interview short answer):

The process of writing state of an object to a file is called serialization.

But strictly speaking:

It is the process of converting an object from Java-supported form into either file-supported form or network-supported form.

Deserialization — general:

The process of reading state of an object from a file is called deserialization.

Deserialization — strict:

Converting from file/network supported form → Java-supported form.

### 21:14 — Which streams? Saving object to file `abc.ser`

Setup: File `abc.ser` (convention — not mandatory; abc.txt also valid; Java extensions don't matter like Unix).

Object = binary data → cannot use Reader/Writer (text). Need Streams.

Step 1 — binary bytes to file:

```java
FileOutputStream fos = new FileOutputStream("abc.ser");
```

Step 2 — write object (not just raw bytes):

ObjectOutputStream oos = new ObjectOutputStream(fos);
oos.writeObject(d1);   // Dog object d1

Board diagram flow:

Dog object (d1)  --serialization-->  abc.ser (file)
     i=10, j=20                        (binary state)

Summary line (board):

By using FileOutputStream and ObjectOutputStream classes we can implement serialization.

### 26:03 — Deserialization streams (reverse)

General definition:

The process of reading state of an object from the file is called deserialization.

Strict:

Converting from file/network supported form → Java-supported form.

```java
FileInputStream fis = new FileInputStream("abc.ser");
ObjectInputStream ois = new ObjectInputStream(fis);
Dog d2 = (Dog) ois.readObject();
```

Board summary:

By using FileInputStream and ObjectInputStream classes we can implement deserialization.

Stream roles clarified:

### 30:43 — Convert theory to executable program: `SerializeDemo`

Sir asks students to turn full discussion into runnable code.

### 31:13 — `Dog` class and `SerializeDemo` skeleton

```java
class Dog {
    int i = 10;
    int j = 20;
}
class SerializeDemo {
    public static void main(String[] args) throws Exception {
        Dog d1 = new Dog();          // i=10, j=20

        // --- SERIALIZATION (3 lines) ---
        FileOutputStream fos = new FileOutputStream("abc.ser");
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(d1);

        // --- DESERIALIZATION (3 lines) ---
        FileInputStream fis = new FileInputStream("abc.ser");
        ObjectInputStream ois = new ObjectInputStream(fis);
        Dog d2 = (Dog) ois.readObject();

        System.out.println(d2.i + ".." + d2.j);
    }
}
```

Expected output (after fixes): 10..20 (Sir uses .. as separator on board)

### 35:36 — Why cast `(Dog)` on `readObject()`?

readObject() return type is `Object` — generic API (could be Dog, Cat, Account, anything).

Must cast to concrete type:

Dog d2 = (Dog) ois.readObject();

### 37:33 — Required additions before compile/run

1. Import:

```java
import java.io.*;
```

2. Checked exception:

```java
public static void main(String[] args) throws Exception {
```

writeObject / readObject may throw `IOException`.

### 38:42 — Quiz: will this compile?

Sir asks class — students split yes/no.

Answer: YES, it compiles.

But at runtime → `NotSerializableException` because:

An object is said to be serializable if and only if the corresponding class implements `Serializable` interface.

Dog does not implement Serializable → runtime failure when writeObject(d1) executes.

### 40:44 — Fix: `implements Serializable`

```java
class Dog implements Serializable {
    int i = 10;
    int j = 20;
}
```

`Serializable` facts (board conclusions):

- Interface in `java.io` package
- No methods → marker interface
- We can serialize only serializable objects
- Non-serializable object → runtime exception: java.io.NotSerializableException
Rule (board):

If we are trying to serialize a non-serializable object → runtime exception saying `NotSerializableException`.

### 41:14 — Live demo: exception then fix

Without `implements Serializable`:

```java
// Runtime (not compile error):
Exception in thread "main" java.io.NotSerializableException: Dog
```

With `implements Serializable`:

```java
// Compile & run SerializeDemo.java
// Output:
10..20
```

Sir deliberately omits implements Serializable first to show runtime exception, then adds it.

### 49:09 — Conclusions block (board notes)

- We can serialize only serializable objects
- Object is serializable iff class implements Serializable
- Serializable in `java.io`, no methods, marker interface
- Serializing non-serializable object → `NotSerializableException` at runtime (compile succeeds)
### 53:01 — Next keyword: `transient`

In serialization context, `transient` plays a very important role for security.

Applicable only to variables — NOT methods, NOT classes.

### 54:01 — Why transient? Permanent storage security

Serialization saves object state to file on hard disk = permanent storage (survives shutdown).

Risk: Sensitive fields (password, PIN) must not be saved permanently.

Analogies Sir uses:

- ATM card: OK to carry card; never write PIN on back (friend lost ₹25k–30k this way)
- Email password: username shareable; password never share/write
- Marriage/password news article humor — password secrecy as security practice
Rule:

At serialization time, if you don't want to save a variable's value for security, declare it `transient`.

Example mapping in Dog:

int i = 10;              // username — OK to serialize
transient int j = 20;    // password — do NOT serialize original value

### 06:00 — Behavior of transient at serialization

When JVM serializes:

- Checks each variable — is it transient?
- If yes → ignore original value, save default value to file
- For int j → default 0 (not 20)
After deserialize + print:

System.out.println(d2.i + ".." + d2.j);
// Output: 10..0   (when j is transient)
// Output: 10..20 (when j is NOT transient)

Mnemonic (board):

Hence transient means: not to serialize (that variable's original value).

### 07:08 — Demo: transient on `j`

Sir runs with transient int j → output `10..0`.

If both secured:

transient int i = 10;
transient int j = 20;
// Output after deserialize: 0..0

### 08:11 — Board notes: transient rules

When to use:

At the time of serialization, if we don't want to save the value of a particular variable to meet security constraint → declare that variable as `transient`.

JVM behavior:

While performing serialization, JVM ignores original value of transient variable and saves default value to the file.

### 71:11 — `transient` vs `static`

```java
class Dog implements Serializable {
    int i = 10;
    static int j = 20;
}
```

Facts:

- Static variable = class-level data → NOT part of object state
- Serialization applies to object state only
- Static variables do not participate in serialization
- j value 20 comes from method area / class data after deserialize, not from file
Print after deserialize:

System.out.println(d2.i + ".." + d2.j);
// Output: 10..20
// i from file; j from class static memory

Declaring `static transient int j` → NO USE / NO IMPACT

Reason: static already excluded from serialization; transient only affects serialized fields.

Board conclusion:

Static variable is not part of object state → won't participate in serialization → declaring static variable as transient → there is no use.

Demo confirms: static transient still prints `10..20`.

Instance transient demo:

transient int i = 10;
static int j = 20;
// Output: 0..20

### 71:49 — `transient` vs `final`

Final variable compile-time behavior (Operators class recap):

final int x = 10;
int y = 20;
System.out.println(x);  // after compile → replaced with literal 10
System.out.println(y);  // y read at runtime

Every final variable replaced by its value at compile time — not kept as variable at runtime.

In serialization:

```java
class Dog implements Serializable {
    int i = 10;
    final int j = 20;
}
```

- Final j participates as value 20 directly (not as "variable j")
- JVM cannot check "is this final field transient?" at runtime — it's already a constant value
- `transient final int j = 20` → no impact; output still `10..20`
Board conclusion:

Final variables participate in serialization directly by the value → declaring final variable as transient → there is no impact.

Demo trace:

### 74:16 — Summary diagram: declaration vs output

Sir builds a declaration → corresponding output table (after serialize + deserialize + print d2.i and d2.j):

```java
// Case 1: Normal
int i = 10;
int j = 20;
// Output: 10..20

// Case 2: transient instance i
transient int i = 10;
int j = 20;
// Output: 0..20

// Case 3: transient static (no effect on static j behavior)
transient static int i = 10;   // ASR/board: instance transient i
int j = 20;
// Output: 0..20  (i transient; j normal)

// Case 4: transient static j — NO USE
int i = 10;
transient static int j = 20;
// Output: 10..20  (unchanged)

// Case 5: transient final j — NO USE
int i = 10;
transient final int j = 20;
// Output: 0..20 if i transient; j still 20 from final value
```

Final summary board (Sir's closing table):

### 48:29 — Complete reference program (SerializeDemo final form)

```java
import java.io.*;

class Dog implements Serializable {
    int i = 10;
    int j = 20;
    // variations: transient int j; static int j; final int j; etc.
}

class SerializeDemo {
    public static void main(String[] args) throws Exception {
        Dog d1 = new Dog();

        // SERIALIZATION — 3 lines
        FileOutputStream fos = new FileOutputStream("abc.ser");
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(d1);

        // DESERIALIZATION — 3 lines
        FileInputStream fis = new FileInputStream("abc.ser");
        ObjectInputStream ois = new ObjectInputStream(fis);
        Dog d2 = (Dog) ois.readObject();

        System.out.println(d2.i + ".." + d2.j);
    }
}
```

CE notes:

- Compiles even without Serializable → fails at `writeObject`
- readObject() needs cast
- File name `abc.ser` is convention only
### 1:29:06 — Session end

Video covers Introduction portion of serialization:

- Definitions (loose + strict)
- Balloon analogy
- FileOutputStream + ObjectOutputStream / FileInputStream + ObjectInputStream
- `Serializable` marker interface
- `NotSerializableException`
- `transient` for security (default value saved)
- `transient` vs `static` vs `final`
Next videos: object graphs, customized serialization, inheritance, externalization, serialVersionUID.

## Quick reference card

Java code block count: 20

## Tables (placement lost -- re-place these in context)

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP |
| Position | 125 of 203 |
| Series | Core Java With OCJP/SCJP |
| Topic | Serialization — Part 1 (Introduction, Serializable, Transient) |
| Instructor | Durga Sir |
| Duration | 1h 29m 26s |
| Video ID | JTdqJ1RC65M |
| Watch | https://www.youtube.com/watch?v=JTdqJ1RC65M |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

| Loose definition | Direction |
|---|---|
| Process of sending an object across a network | Java → network |
| Process of writing an object to a file | Java → file |
| Process of saving state of an object to a file | Java → file |

| Real world | Java concept |
|---|---|
| Inflated balloon (usable, not shippable) | Java-supported form (live object in JVM heap) |
| Deflated balloon (shippable, not playable) | Network/file supported form (serialized bytes) |
| Deflate before shipping | Serialization |
| Inflate after receiving | Deserialization |

| Task | Stream |
|---|---|
| Write binary data | FileOutputStream |
| Write object | ObjectOutputStream |
| Read binary data | FileInputStream |
| Read object | ObjectInputStream |

| Declaration | Output d2.i .. d2.j |
|---|---|
| Normal i, j | 10..20 |
| final int j = 20 | 10..20 |
| transient final int j = 20 | 10..20 |
| transient int i = 10, normal j | 0..20 |

| Fields in Dog | After deserialize print |
|---|---|
| i=10, j=20 | 10, 20 |
| transient i=10, j=20 | 0, 20 |
| transient static on static field | no change vs non-transient static |
| transient final j=20 | j still 20 |

| Concept | Key point |
|---|---|
| Serialization | Java form → file/network form |
| Deserialization | file/network form → Java form |
| Serialize API | ObjectOutputStream.writeObject(obj) |
| Deserialize API | (Type) ObjectInputStream.readObject() |
| Serializable | class must implements Serializable (java.io, marker) |
| Failure mode | NotSerializableException at runtime |
| transient | skip original value; save default |
| transient + static | useless (static not serialized anyway) |
| transient + final | useless (final inlined as constant) |
