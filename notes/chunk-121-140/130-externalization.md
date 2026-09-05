# Video 130

## Video info

Title: Core Java With OCJP/SCJP: Serialization Part- 6||Externalization

### 00:07 — Session opening: why Externalization exists

- Durga Sir opens Externalization (ASR often says "externalization" / "calization" for serialization).
- Most programmers know Serialization but not Externalization, even though it is very useful.
- Core question: Serialization already exists — when/why go for Externalization?
Serialization recap (JVM-driven):

- In Serialization, the JVM reads every instance variable (i, j, …), writes them to the file, and reads them back on deserialization.
- Programmer writes essentially one line: oos.writeObject(obj); — JVM handles everything else.
- Advantage: complexity is low; even a beginner can serialize.
- Problem: programmer has no control over which fields are saved or how they are saved.
### 00:44 — Serialization: JVM owns everything

Board point (decoded ASR):

In Serialization, everything is taken care of by the JVM. The programmer has no control.

- Programmer does not know how many properties exist, how values are stored in the file, etc.
- Only calls writeObject / readObject.
### 02:16 — Motivating example: Account object with 1000 properties

Scenario: An Account object has ~1000 properties (holder name, address, PIN, account number, …).

- If you serialize the whole object → all 1000 properties go to the file.
- On deserialization → all 1000 come back.
- Requirement: save/read only account number; fetch remaining data from a local database when needed.
- Unnecessary network/file I/O for 999 fields you do not need.
Serialization limitation:

- Cannot save only 1 or 2 properties.
- Compulsory: total object is always saved/restored.
Performance analogy (Durga Sir's math):

- Assume 1 minute to read/write one property.
- 1000 properties → 1000 minutes read + 1000 minutes write = 2000 minutes.
- Actual need: 1 property → 2 minutes work.
- Wasting 1998 minutes → performance goes down.
Formal problem statement:

In Serialization, whether required or not, it is always possible to save the total object to the file. It is not possible to save part of the object.

### 05:16 — SCJP course registration analogy

Same idea:

- Serialization = forced full package (total object).
- Externalization = pick only what you need (part of object).
### 06:52 — Three differences (verbal, before board)

When to choose which:

- Save total object → Serialization is best.
- Save part of object → Externalization is best.
### 11:18 — Board notes: Serialization problems → Externalization solution

In Serialization:

- Everything takes care by JVM; programmer doesn't have any control.
- It is always possible to save total object to the file; not possible to save part of the object — which may create performance problems.
- To overcome this problem → go for Externalization.
Main advantage of Externalization over Serialization:

- Everything takes care by programmer; JVM doesn't have any control.
- Based on our requirement, we can save either total object or part of the object — which improves performance of the system.
### 15:59 — Serializable vs Externalizable interfaces

Externalizable interface — 2 methods:

- writeExternal(ObjectOutput out)
- readExternal(ObjectInput in)
Important hierarchy (board diagram):

Externalizable is a child interface of Serializable.

Both introduced in Java 1.1 (same version).

Why Serialization is more popular than Externalization:

- Laziness / complexity of the programmer — two big methods must be implemented manually.
- Programmer thinks: "JVM will take care; why should I worry about performance?"
### 23:51 — Demo program: `ExternalizableDemo`

Durga Sir begins the main board program. Class has 3 instance variables: String s, int i, int j.

```java
// Board: class skeleton
class ExternalizableDemo implements Externalizable {
    String s;
    int i;
    int j;

    // Parameterized constructor (for creating T1)
    ExternalizableDemo(String s, int i, int j) {
        this.s = s;
        this.i = i;
        this.j = j;
    }
}
```

Main method — create object and serialize:

```java
public static void main(String[] args) throws Exception {
    ExternalizableDemo t1 = new ExternalizableDemo("Durga", 10, 20);
    // t1: s="Durga", i=10, j=20

    FileOutputStream fos = new FileOutputStream("abc.ser");
    ObjectOutputStream oos = new ObjectOutputStream(fos);
    oos.writeObject(t1);   // serialization trigger
}
```

Requirement (key teaching point):

- Object has 3 properties, but we want to save only `s` and `i` to abc.ser.
- Remaining property `j` should not be written to the file.
- → This is exactly why we use Externalization.
### 28:33 — Serialization flow when class implements Externalizable

When `oos.writeObject(t1)` is called:

- JVM checks: does class of t1 implement Serializable or Externalizable?
- If Serializable → save total object (default JVM mechanism).
- If Externalizable → JVM understands: programmer does not want total object; only selected fields → JVM calls `writeExternal(...)` automatically.
Implement `writeExternal`:

```java
public void writeExternal(ObjectOutput out) throws IOException {
    out.writeObject(s);   // save s  ("Durga")
    out.writeInt(i);      // save i  (10)
    // j is intentionally NOT written
}
```

Conclusions about `writeExternal` (board, highlighted box):

- Executed automatically at the time of serialization.
- Inside this method, programmer writes code to save required variables to the file.
File contents (Externalization): only required properties (s, i) — not all three.

### 32:24 — First half complete; start deserialization (second half)

Deserialization code:

```java
FileInputStream fis = new FileInputStream("abc.ser");
ObjectInputStream ois = new ObjectInputStream(fis);
ExternalizableDemo t2 = (ExternalizableDemo) ois.readObject();
```

Critical Externalization deserialization flow:

- JVM checks: class implements Externalizable?
- File does not contain a full serialized object — only partial data (s, i).
- readObject() return type is Object, but file lacks complete object state.
- Extra JVM step: create a new separate object by invoking `public no-arg constructor`.
- On that new object, JVM calls `readExternal(ObjectInput in)`.
Why public no-arg constructor is mandatory:

```java
// MUST exist in every Externalizable class
public ExternalizableDemo() {
    System.out.println("public no-arg Constructor");
    // default values: s=null, i=0, j=0
}
```

- After no-arg ctor: t2.s = null, t2.i = 0, t2.j = 0.
- Then readExternal fills in saved fields.
```java
public void readExternal(ObjectInput in)
        throws IOException, ClassNotFoundException {
    s = (String) in.readObject();  // null → "Durga"
    i = in.readInt();              // 0 → 10
    // j was never written → stays default 0
}
```

Conclusions about `readExternal` (board, highlighted box):

- Executed automatically at the time of deserialization.
- Programmer writes code to read required variables from the file and assign to the current object.
Strict deserialization order (board):

- JVM creates new object via public no-arg constructor.
- On that object, JVM calls `readExternal`.
Rule:

Every Externalizable-implemented class must compulsorily contain a public no-arg constructor.

Otherwise → `InvalidClassException` at runtime ("no valid constructor" — same family of error as in prior Serialization sessions*).

Contrast with Serializable:

- Serializable class not required to have public no-arg constructor (file already has total object).
### 48:51 — Print results after deserialization

System.out.println(t2.s);  // Durga
System.out.println(t2.i);  // 10
System.out.println(t2.j);  // 0  (never saved/restored)

- j = 0 is expected — we chose not to externalize j.
- Student question: "Why is j zero?" → Because only s and i were required.
### 49:44 — Live execution

Compile & run (Externalizable):

```java
// CE: javac ExternalizableDemo.java
// Run: java ExternalizableDemo
public no-arg Constructor
Durga
10
0
```

- CE: compiles fine with implements Externalizable, both methods, public no-arg ctor.
- Print: no-arg ctor message first (deserialization), then field values.
### 51:47 — Change to Serializable: compare output

Change class to implements Serializable (remove writeExternal / readExternal logic conceptually — JVM default serialization):

```java
class ExternalizableDemo implements Serializable {
    String s;
    int i;
    int j;
    // constructors ...
}
```

Output:

Durga
10
20

- All three fields restored.
- Public no-arg constructor NOT called (no print of ctor message).
- File already contained total object.
### 52:38 — Remove public no-arg constructor (Externalizable)

If class implements Externalizable but no public no-arg constructor:

Exception in thread "main" ...
InvalidClassException: ExternalizableDemo; no valid constructor

- Code compiles fine.
- Runtime failure on deserialization.
### 56:03 — Recap: only 2 of 1000 properties saved

Central methods of Externalization:

```java
public void writeExternal(ObjectOutput out) throws IOException { /* ... */ }

public void readExternal(ObjectInput in)
        throws IOException, ClassNotFoundException { /* ... */ }
```

Full working demo (consolidated board + screen):

```java
import java.io.*;

class ExternalizableDemo implements Externalizable {
    String s;
    int i;
    int j;

    public ExternalizableDemo() {
        System.out.println("public no-arg Constructor");
    }

    ExternalizableDemo(String s, int i, int j) {
        this.s = s;
        this.i = i;
        this.j = j;
    }

    public void writeExternal(ObjectOutput out) throws IOException {
        out.writeObject(s);
        out.writeInt(i);
    }

    public void readExternal(ObjectInput in)
            throws IOException, ClassNotFoundException {
        s = (String) in.readObject();
        i = in.readInt();
    }

    public static void main(String[] args) throws Exception {
        ExternalizableDemo t1 = new ExternalizableDemo("Durga", 10, 20);

        FileOutputStream fos = new FileOutputStream("abc.ser");
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(t1);

        FileInputStream fis = new FileInputStream("abc.ser");
        ObjectInputStream ois = new ObjectInputStream(fis);
        ExternalizableDemo t2 = (ExternalizableDemo) ois.readObject();

        System.out.println(t2.s);
        System.out.println(t2.i);
        System.out.println(t2.j);
    }
}
```

Print (Externalizable):

```java
public no-arg Constructor
Durga
10
0
```

### 1:01:08 — Summary diagram: Serializable vs Externalizable outputs

### 1:03:49 — Re-run demo; when to use Externalization

- Use Externalization when you want to save part of the object.
- Performance-wise, Externalization is better when only subset needed.
### 1:05:07 — File size experiment: 54 bytes vs 88 bytes

Durga Sir inspects abc.ser on disk (ls -l / column listing):

In Serialization more data is saved; in Externalization less data is saved.

### 1:07:32 — Who saves data? Role of `transient`

Serialization:

- JVM saves data to file.
- To exclude a sensitive field → declare it `transient` (tell JVM: don't save this variable).
```java
// Serializable example — transient excludes fields from JVM serialization
class Account implements Serializable {
    transient String s;
    transient int i;
    transient int j;
}
// Output after deserialization: null, 0, 0
```

Externalization:

- Programmer saves data (inside writeExternal).
- If you don't want a field saved → simply don't write it in writeExternal.
- `transient` keyword has NO role in Externalization.
Demo — all fields marked transient but Externalizable with manual save of s, i:

```java
class ExternalizableDemo implements Externalizable {
    transient String s;
    transient int i;
    transient int j;

    public void writeExternal(ObjectOutput out) throws IOException {
        out.writeObject(s);  // still writes — transient ignored here
        out.writeInt(i);
    }
    // readExternal restores s, i ...
}
```

Output unchanged:

```java
public no-arg Constructor
Durga
10
0
```

Whether variables are transient or not → no effect in Externalization.

Board note:

- In Serialization → transient keyword will play a role.
- In Externalization → transient keyword won't play any role; not required.
### 1:14:50 — Eight differences: Serialization vs Externalization (final table)

Durga Sir dictates full comparison for notes/interview:

Terminology mapping:

- Serialization = default serialization (JVM-driven).
- Externalization = customized serialization (programmer-driven).
- Externalizable extends Serializable — child interface.
### 1:28:24 — Session close

- Total 8 differences covered — must be able to explain in interview ("enter your room" phrasing).
- Externalization is rarely asked on OCJP/SCJP exam itself but important for interviews and performance-sensitive designs.
- Most developers don't know this concept — Durga Sir emphasizes clarity.
## Quick reference

```java
// Minimal Externalizable pattern
class MyClass implements Externalizable {
    // fields...

    public MyClass() { }  // REQUIRED: public no-arg

    public void writeExternal(ObjectOutput out) throws IOException {
        // write ONLY what you need
    }

    public void readExternal(ObjectInput in)
            throws IOException, ClassNotFoundException {
        // read ONLY what you wrote; assign to this object
    }
}
```

Java code block count: 13

## Tables (placement lost -- re-place these in context)

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP |
| Position | 130 of 203 |
| Series | Core Java With OCJP/SCJP |
| Topic | Serialization — Part 6: Externalization |
| Instructor | Durga Sir |
| Duration | 1h 29m 02s |
| Video ID | hMJzf0E_ut4 |
| Watch | https://www.youtube.com/watch?v=hMJzf0E_ut4 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

| Policy | Effect |
|---|---|
| Must join entire Java package to attend SCJP | Very few students join |
| Can register only SCJP (or only Advanced Java, etc.) based on need | Many more students join |

| # | Serialization | Externalization |
|---|---|---|
| 1 | Everything by JVM; programmer has no control | Everything by programmer; JVM has no control |
| 2 | Always saves total object; cannot save part | Can save total or part based on requirement |
| 3 | Relatively lower performance (when only subset needed) | Relatively higher performance |

|  | Serializable | Externalizable |
|---|---|---|
| To give ability | Class must implements Serializable | Class must implements Externalizable |
| Interface type | Marker interface (0 methods) | Functional interface (2 methods) |
| Who does the work | JVM | Programmer |

| Mechanism | What file contains |
|---|---|
| Serialization | All properties |
| Externalization | Only required properties |

| If class implements | File saves | Output |
|---|---|---|
| Serializable | Total object | Durga 10 20 |
| Externalizable (save s, i only) | Only required vars | public no-arg Constructor then Durga 10 0 |

| Implementation | File size | Reason |
|---|---|---|
| Externalizable (only s, i) | 54 bytes | Less data — only required variables |
| Serializable (all fields) | 88 bytes | More data — total object metadata + all fields |

| # | Serialization | Externalization |
|---|---|---|
| 1 | Meant for default serialization | Meant for customized serialization |
| 2 | Everything by JVM; programmer has no control | Everything by programmer; JVM has no control |
| 3 | Always save total object; cannot save part | Can save total or part based on requirement |
| 4 | Relatively low performance (when subset needed) | Relatively high performance |
| 5 | Best choice if you want to save total object | Best choice if you want to save part of object |
| 6 | Serializable — marker interface, no methods | Externalizable — 2 methods: writeExternal, readExternal |
| 7 | Serializable class not required to have public no-arg constructor | Externalizable class must have public no-arg constructor; else InvalidClassException |
| 8 | transient keyword plays a role | transient keyword won't play any role / not required |
