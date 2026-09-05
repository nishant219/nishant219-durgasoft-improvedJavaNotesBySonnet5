# Video 126

## Video info

Title: Core Java With OCJP/SCJP: Serialization Part- 2||Serialazation in the case of object graphs

### 00:05 — Recap: single-object serialization

Durga Sir continues from the previous lecture (Serialization Part 1).

- In the last example, only one object was serialized — a single Dog object written to a file.
- Students confirmed they understand serialization (object → file) and deserialization (file → object).
Question posed: Is it possible to serialize multiple objects to the same file?

Answer: Yes — we can serialize any number of objects to a file; there is no restriction to one object only.

### 00:54 — Rule for multiple-object serialization

When serializing multiple objects, there is one important restriction/rule about order.

### 01:02 — Example: serializing Dog, Cat, and Rat (three objects)

Three separate objects are created and all written to the same file abc.ser:

Dog d1 = new Dog();
Cat c1 = new Cat();
Rat r1 = new Rat();

FileOutputStream fos = new FileOutputStream("abc.ser");
ObjectOutputStream oos = new ObjectOutputStream(fos);

oos.writeObject(d1);   // 1st object written
oos.writeObject(c1);   // 2nd object written
oos.writeObject(r1);   // 3rd object written

File contents (`abc.ser`): three objects in order — Dog → Cat → Rat.

Key point 1: We can serialize any number of objects to the file. Serialization is not limited to a single object.

### 03:18 — Deserialization must follow the same order

To read all three objects back:

FileInputStream fis = new FileInputStream("abc.ser");
ObjectInputStream ois = new ObjectInputStream(fis);

Dog d2 = (Dog) ois.readObject();    // 1st read → Dog (matches 1st write)
Cat c2 = (Cat) ois.readObject();    // 2nd read → Cat (matches 2nd write)
Rat r2 = (Rat) ois.readObject();    // 3rd read → Rat (matches 3rd write)

Rule: Objects are deserialized in the same order they were serialized.

- First writeObject → first readObject returns that object.
- Second writeObject → second readObject, and so on.
If you call readObject() once, you always get the first serialized object (Dog in this example), regardless of what type you cast to.

### 05:46 — ClassCastException when order is wrong

If deserialization order is interchanged by mistake:

```java
// WRONG: trying to read Cat first when Dog was written first
Cat c2 = (Cat) ois.readObject();  // first readObject() still returns Dog!
```

- First readObject() still returns the Dog object (first serialized).
- Casting it to Cat → `ClassCastException`.
Conclusion: Order of objects is critical during deserialization. Always read in the same order as write.

### 06:31 — Board note (theory)

We can serialize any number of objects to the file, but in which order we serialized, in the same order only we have to perform deserialization.

Order of objects is important in serialization.

### 08:13 — Reiteration of Dog → Cat → Rat example

Durga Sir rewrites the full example on the board for clarity:

```java
Dog d1 = new Dog();
Cat c1 = new Cat();
Rat r1 = new Rat();

FileOutputStream fos = new FileOutputStream("abc.ser");
ObjectOutputStream oos = new ObjectOutputStream(fos);
oos.writeObject(d1);
oos.writeObject(c1);
oos.writeObject(r1);
```

Deserialization (same order):

```java
FileInputStream fis = new FileInputStream("abc.ser");
ObjectInputStream ois = new ObjectInputStream(fis);

Dog d2 = (Dog) ois.readObject();
Cat c2 = (Cat) ois.readObject();
Rat r2 = (Rat) ois.readObject();
```

### 10:40 — Problem: unknown serialization order

Scenario: Person A serializes objects in the morning. Person B deserializes in the evening but does not know the order in which objects were written.

Question: How to handle deserialization when order of objects in the file is unknown?

### 12:06 — Solution: parent reference + `instanceof`

When order is unknown, read each object into a parent reference (Object), then use `instanceof` to identify the actual type:

```java
FileInputStream fis = new FileInputStream("abc.ser");
ObjectInputStream ois = new ObjectInputStream(fis);

Object o = (Object) ois.readObject();   // parent reference holds any type

if (o instanceof Dog) {
    Dog d2 = (Dog) o;
    // perform dog-specific functionality
} else if (o instanceof Cat) {
    Cat c2 = (Cat) o;
    // perform cat-specific functionality
} else if (o instanceof Rat) {
    Rat r2 = (Rat) o;
    // perform rat-specific functionality
}
```

Why `Object` reference? Parent reference can hold any child object (Dog, Cat, or Rat). But with a parent reference alone, you can only call methods declared in the parent — not child-specific methods. Hence `instanceof` + downcast.

Loop variant: To avoid repeating code for every object, wrap in a loop:

```java
Object o;
while ((o = ois.readObject()) != null) {
    if (o instanceof Dog) {
        Dog d2 = (Dog) o;
        // dog-specific work
    } else if (o instanceof Cat) {
        Cat c2 = (Cat) o;
        // cat-specific work
    } else if (o instanceof Rat) {
        Rat r2 = (Rat) o;
        // rat-specific work
    }
}
```

(Note: Durga Sir mentions a while-loop pattern; in practice EOF is usually caught via `EOFException` rather than null return — the teaching intent is to loop over all objects without hard-coding order.)

Board note:

If we don't know order of objects in serialization: read into Object reference, use instanceof to identify type, then downcast and process.

### 17:30 — End of multiple-objects topic; transition

Summary of Part 1 of this video:

- How to serialize multiple objects.
- Order matters for typed reads.
- instanceof approach when order is unknown.
### 18:16 — New subtopic: Object Graphs in Serialization

Next subtopic after serialization introduction: Object Graphs in Serialization.

### 18:57 — Object graph: class structure (Dog → Cat → Rat chain)

Three classes linked by reference instance variables:

```java
class Dog {
    Cat c = new Cat();   // Dog has Cat reference → Cat object created with Dog
}

class Cat {
    Rat r = new Rat();   // Cat has Rat reference → Rat object created with Cat
}

class Rat {
    int j = 20;          // Rat has primitive int (not an object reference)
}
```

Real-world analogy (ASR decoded):

- Dog sees Cat → runs.
- Cat sees Rat → runs.
- Rat has j = 20 — chain stops at primitive.
Object creation chain: When new Dog() is called:

- Dog object created.
- Automatically Cat object created (instance variable c in Dog).
- Automatically Rat object created (instance variable r in Cat).
- j = 20 assigned in Rat.
Explicitly created: 1 object (Dog d1 = new Dog()).

Internally created: 3 objects total — Dog, Cat, Rat.

### 21:58 — Serializing one Dog object serializes the whole graph

Dog d1 = new Dog();

FileOutputStream fos = new FileOutputStream("abc.ser");
ObjectOutputStream oos = new ObjectOutputStream(fos);
oos.writeObject(d1);   // only d1 is passed explicitly

Question: Will only the Dog object be serialized, or the entire group?

Answer: The entire group (object graph) is serialized automatically.

Definition — Object Graph:

Whenever we are serializing an object, the set of all objects which are reachable from this object will be serialized automatically. This group of objects is called an object graph.

Reachable from `d1`: Dog → Cat → Rat → j=20 (primitive stored inside Rat).

File `abc.ser` contains: Dog, Cat, Rat (and field values including j=20).

### 24:03 — Deserialization restores the entire graph

```java
FileInputStream fis = new FileInputStream("abc.ser");
ObjectInputStream ois = new ObjectInputStream(fis);

Dog d2 = (Dog) ois.readObject();
```

After deserialization:

- d2 is the Dog object.
- d2.c → Cat object (automatically restored).
- d2.c.r → Rat object (automatically restored).
- d2.c.r.j → 20.
Verification print:

System.out.println(d2.c.r.j);   // CE/print: 20

### 25:54 — Practical proof via NotSerializableException

Durga Sir demonstrates with live code (SerializeDemo2.java) that the entire graph is serialized by observing which class triggers NotSerializableException.

Step 1 — No class implements Serializable:

```java
class Dog {
    Cat c = new Cat();
}
class Cat {
    Rat r = new Rat();
}
class Rat {
    int j = 20;
}

// main: oos.writeObject(d1);
```

- CE: compiles fine.
- Runtime: NotSerializableException for Dog — because Dog doesn't implement Serializable.
Step 2 — Only Dog implements Serializable:

```java
class Dog implements Serializable {
    Cat c = new Cat();
}
```

- Runtime: NotSerializableException for Cat — proves Cat is also being serialized internally even though only Dog was written.
Step 3 — Dog and Cat implement Serializable:

```java
class Dog implements Serializable { Cat c = new Cat(); }
class Cat implements Serializable { Rat r = new Rat(); }
```

- Runtime: NotSerializableException for Rat — proves Rat is also serialized as part of the graph.
Step 4 — All three implement Serializable:

```java
class Dog implements Serializable { Cat c = new Cat(); }
class Cat implements Serializable { Rat r = new Rat(); }
class Rat implements Serializable { int j = 20; }
```

- Runs successfully.
- CE/print: 20
Practical proof conclusion: Exceptions name the non-serializable class in the graph, proving JVM serializes all reachable objects, not just the root.

### 29:01 — Rule: every object in the graph must be Serializable

In an object graph, every object should be Serializable.

- If at least one reachable object is not Serializable → runtime exception: `NotSerializableException`.
- All three (Dog, Cat, Rat) must implement Serializable for the example to work.
### 29:26 — Live demo: SerializeDemo2.java walkthrough

Full program on screen:

```java
import java.io.*;

class Dog {
    Cat c = new Cat();
}
class Cat {
    Rat r = new Rat();
}
class Rat {
    int j = 20;
}

class SerializeDemo2 {
    public static void main(String[] args) throws Exception {
        Dog d1 = new Dog();

        FileOutputStream fos = new FileOutputStream("abc.ser");
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(d1);

        FileInputStream fis = new FileInputStream("abc.ser");
        ObjectInputStream ois = new ObjectInputStream(fis);
        Dog d2 = (Dog) ois.readObject();

        System.out.println(d2.c.r.j);   // after all implement Serializable → 20
    }
}
```

Progressive fix: add implements Serializable to Dog, then Cat, then Rat — each step reveals the next failing class in the graph.

### 32:53 — Board theory notes (object graph)

Whenever we are serializing an object, the set of all objects which are reachable from that object will be serialized automatically. This group of objects is nothing but object graph.

In object graph, every object should be Serializable. If at least one object is not Serializable, then we will get runtime exception saying `NotSerializableException`.

### 35:40 — Final complete program (all Serializable)

```java
import java.io.*;

class Dog implements Serializable {
    Cat c = new Cat();
}

class Cat implements Serializable {
    Rat r = new Rat();
}

class Rat implements Serializable {
    int j = 20;
}

class SerializeDemo2 {
    public static void main(String[] args) throws Exception {
        Dog d1 = new Dog();

        FileOutputStream fos = new FileOutputStream("abc.ser");
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(d1);

        FileInputStream fis = new FileInputStream("abc.ser");
        ObjectInputStream ois = new ObjectInputStream(fis);
        Dog d2 = (Dog) ois.readObject();

        System.out.println(d2.c.r.j);   // CE/print: 20
    }
}
```

### 36:31 — Brief aside: network serialization (RMI, CORBA)

Durga Sir mentions that heap data must be converted to a network-supported format for remote use. Technologies like RMI, EJB, CORBA use marshalling/unmarshalling — analogous to serialization but for network transport; middleware handles it. For file-based serialization, the java.io serialization API (ObjectOutputStream/ObjectInputStream) is used.

### 39:14 — Diagram to copy (object graph visualization)

Before serialization (heap):

d1 (Dog) → c (Cat) → r (Rat) → j = 20

File: abc.ser contains the entire graph.

After deserialization (heap):

d2 (Dog) → c (Cat) → r (Rat) → j = 20

Same structure restored — references preserved across serialization boundary.

### 41:17 — Additional board notes

In the above program, whenever we are serializing dog object, automatically cat and rat objects got serialized — because these are part of object graph of dog.

Among dog, cat, and rat objects — if at least one object is not Serializable, then we will get runtime exception saying `NotSerializableException`.

### 43:28 — Video conclusion

Topics covered in Video 126:

- Multiple object serialization — any number of objects; order matters; wrong order → ClassCastException; unknown order → Object + instanceof.
- Object graphs — serializing one object automatically serializes all reachable objects; every object in the graph must implement Serializable; proof via progressive NotSerializableException messages.
Java code block count: 17

## Tables (placement lost -- re-place these in context)

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP |
| Position | 126 of 203 |
| Series | Serialization |
| Topic | Serialization in the case of object graphs (multiple objects + object graphs) |
| Instructor | Durga Sir |
| Duration | 43m 46s |
| Video ID | oEUlY-gFFcU |
| Watch | https://www.youtube.com/watch?v=oEUlY-gFFcU |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
