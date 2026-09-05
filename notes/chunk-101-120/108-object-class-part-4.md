# Video 108 — Object class Part-4: `getClass()`, `finalize()`, `wait()` / `notify()` / `notifyAll()`

## Video info

## Session overview

This lecture completes the fifth Object-class method in depth (getClass()), then gives a high-level preview of the remaining Object methods that belong to other topics:

- `getClass()` — runtime class definition, Class object, Reflection API, JDBC vendor-class discovery (main content)
- `finalize()` — Garbage Collector cleanup hook (basic idea only; full GC series later)
- `wait()` / `notify()` / `notifyAll()` — inter-thread communication one-liner + producer–consumer sketch (detailed coverage deferred to Multi Threading)
Object methods completed before this video: toString(), hashCode(), equals(), clone().

After this video, the Object-class survey is complete at overview level; Strings begin in Video 109.

## Part A — `getClass()` method

### 00:05 — Transition: next Object method is `getClass()`

Durga Sir continues the Object-class method tour. The next method after clone() is `getClass()`.

Purpose (board definition):

Returns the runtime class definition of an object.

If you hold an object reference but do not know which concrete class it belongs to, getClass() gives you the `Class` object representing that class at runtime.

### 00:47 — Motivating scenario: `ArrayList` holding unknown element type

Setup:

ArrayList list = new ArrayList();
Object obj = list.get(0);   // element could be Student, Customer, String, anything

- ArrayList can hold any type of object.
- After get(0), you receive an `Object` reference because the element type is unknown at compile time.
- Requirement: discover the object's class — class name, method count, constructors, fields, parent class, etc.
Solution:

Class c = obj.getClass();   // runtime Class object for that instance

Once you have the Class object, you can query class-level properties.

### 02:14 — What you can ask the `Class` object

Example — print class name:

System.out.println(c.getName());
// e.g. "Student" or "java.lang.String"

Example — list declared methods:

```java
Method[] m = c.getDeclaredMethods();
for (Method m1 : m) {
    System.out.println(m1.getName());
}
```

Example — count methods:

```java
int count = 0;
for (Method m1 : m) {
    count++;
}
System.out.println("The number of methods: " + count);
```

Package note: Method is in java.lang.reflect — may require import java.lang.reflect.*; when using Method[] explicitly.

### 04:36 — Reflection API connection

Durga Sir names this concept Reflection. In advanced Java / frameworks, `getClass()` plays a central role in the Reflection API.

Exam/board summary:

- We can use `getClass()` to obtain the runtime class definition of an object.
- Using the returned `Class` object, we access class-level properties: fully qualified name, methods, constructors, variables, parent class, etc.
### 05:00 — JVM creates one `Class` object per loaded class

For every loaded `.class` file (Test, Customer, Student, String, Connection implementation, …), the JVM creates one object of type `java.lang.Class` on the heap.

After loading Test.class     → one Class object for Test
After loading String.class   → one Class object for String
After loading Student.class  → one Class object for Student

Programmers use this `Class` object to read class-level metadata at runtime.

`getClass()` usage frequency: very common in Reflection API code.

### 06:25 — Complete signature

```java
public final Class<?> getClass()
```

- `public` — callable from anywhere
- `final` — cannot be overridden (subclasses always use Object's implementation tied to actual runtime type)
- Return type: Class<?> (lecture writes Class c for simplicity)
### 08:21 — Example 1: introspect a `String` object

```java
import java.lang.reflect.*;

class Test {
    public static void main(String[] args) {
        Object o = new String("Durga");

        Class c = o.getClass();

        System.out.println("Fully qualified name of class:");
        System.out.println(c.getName());

        Method[] m = c.getDeclaredMethods();
        System.out.println("Methods information:");
        for (Method m1 : m) {
            System.out.println(m1.getName());
        }

        int count = 0;
        for (Method m1 : m) {
            count++;
        }
        System.out.println("The number of methods: " + count);
    }
}
```

Representative output (lecture run):

Fully qualified name of class:
java.lang.String
Methods information:
hashCode
equals
...
The number of methods: 73

(String declares many methods — lecture counts 73.)

Key takeaway: From a plain Object reference o, o.getClass() reveals the real runtime type (java.lang.String) and its members.

### 12:34 — Example 2: JDBC — discover vendor-specific `Connection` class

Problem: Connection is an interface. Code uses portable API:

Connection con = DriverManager.getConnection(url, user, password);

The actual object is a vendor implementation (MySQL driver class, Oracle driver class, …). You should not hard-code vendor class names — program would work only for one database.

Portable discovery:

```java
Connection con = DriverManager.getConnection(/* url, user, password */);

System.out.println(con.getClass().getName());
```

Method chaining: con.getClass() → Class object → .getName() → fully qualified implementation class name.

- MySQL environment → MySQL driver class name printed
- Oracle environment → Oracle driver class name printed
Same pattern works whenever you have an object but need underlying class information without naming the vendor class in source code.

### 22:50 — Object methods completed so far (checkpoint)

After getClass(), these five Object methods are done in the java.lang Object series:

Remaining Object methods get brief preview here; deep dives are in GC and Multi Threading modules.

## Part B — `finalize()` method (Garbage Collection preview)

### 23:07 — Not full GC context, but basic idea required

finalize() relates to Garbage Collection. Full finalization/GC internals (~2.5–3 hours) come in the Garbage Collection module; here only the story + contract.

### 23:27 — Eligibility for GC

An object with no reference variables pointing to it is eligible for garbage collection — a "useless" object.

### 24:03 — Durga Sir's GC narrative (memory hook)

- GC finds eligible object → "happy" (found food — useless objects).
- GC prepares to destroy the object.
- Object "panics" / has resources still open (DB connection, network socket, …).
- Compassionate GC asks: "Do you have any last wish?"
- Object asks to close connections before death.
- GC calls `finalize()` on the object to perform cleanup activities.
- After finalize() completes → GC destroys the object.
### 26:19 — Contract (board notes)

protected void finalize() throws Throwable

Interview one-liner: Just before destroying an object, GC calls finalize() to perform cleanup; once finalize completes, the object is destroyed.

Modern note (outside lecture): finalize() is deprecated since Java 9 and removed in recent JDKs; prefer try-with-resources / Cleaner / explicit close(). Durga Sir teaches the SCJP-era model for exam history and conceptual link to GC.

## Part C — `wait()`, `notify()`, `notifyAll()` (Multi Threading preview)

### 28:44 — Remaining Object methods

Object class still has: `wait()` (3 overloads), `notify()`, `notifyAll()`.

Full treatment (~3 hours) belongs in Multi Threading; here: purpose in one line.

### 29:17 — Inter-thread communication

These methods can be used for inter-thread communication.

### 29:26 — Producer–consumer sketch

```java
// Shared resource (e.g. Queue)
Queue q = ...;

// Thread T1 = Consumer — expects items in queue
// Thread T2 = Producer — adds items to queue
```

Flow:

- Consumer expects update but queue is empty → calls `wait()` → thread enters WAITING state ("notify me when someone updates").
- Producer produces item → calls `notify()` or `notifyAll()` → waiting consumer receives notification → continues with updated queue.
Responsibilities:

Board summary:

- We can use wait(), notify(), notifyAll() for inter-thread communication.
- Thread expecting updation → `wait()` → waiting state.
- Thread that performed updation → `notify()` → waiting thread gets notification and continues execution with those updates.
### 34:15 — Session close

At this stage, all 11 public Object methods (excluding private registerNatives()) have been introduced across the java.lang Object series. Next topic in playlist: String class (Video 109).

## Quick reference card

getClass()
├── Signature: public final Class<?> getClass()
├── Returns: runtime Class object for object's actual type
├── Use: Reflection — name, methods, constructors, superclass, ...
├── JVM: one Class object per loaded class file on heap
└── JDBC pattern: con.getClass().getName() → vendor driver class

finalize()
├── Called by: Garbage Collector (not normal application code)
├── When: just before object destruction
├── Purpose: cleanup activities (close resources)
└── After finalize(): object destroyed by GC

wait() / notify() / notifyAll()
├── Purpose: inter-thread communication
├── wait(): thread expecting update → WAITING state
└── notify()/notifyAll(): updater wakes waiting thread(s)

## Exam traps & interview lines

## Full transcript coverage (timestamp index)

## ASR decode notes (Whisper STT corrections)

End of Video 108 notes — java.lang Part-4: getClass(), finalize(), wait/notify preview

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| Title | Core Java With OCJP/SCJP: java.lang.package Part-4 \ | \ | object class \ | \ | finalize() \ | \ | getclass() \ | \ | notify() |
| Playlist | Core Java With OCJP/SCJP |  |  |  |  |  |  |  |  |
| Position | 108 of 203 |  |  |  |  |  |  |  |  |
| Series | java.lang.package Part-4 (Object class methods — continues Part-3 equals()) |  |  |  |  |  |  |  |  |
| Topic | getClass(), Reflection intro, Class objects, finalize(), inter-thread communication preview |  |  |  |  |  |  |  |  |
| Instructor | Durga Sir |  |  |  |  |  |  |  |  |
| Duration | 34m 29s |  |  |  |  |  |  |  |  |
| Video ID | 3gQdOltJ89k |  |  |  |  |  |  |  |  |
| Watch | https://www.youtube.com/watch?v=3gQdOltJ89k |  |  |  |  |  |  |  |  |
| Transcript source | Local Whisper STT (.transcripts/108-3gQdOltJ89k.txt) |  |  |  |  |  |  |  |  |

| Question | API (examples) |
|---|---|
| Fully qualified class name? | c.getName() |
| How many methods? | c.getDeclaredMethods() |
| Method names? | loop + m.getName() |
| Constructors, fields, superclass? | other Class APIs (mentioned conceptually) |

| # | Method | Status in series |
|---|---|---|
| 1 | toString() | covered (Part-1) |
| 2 | hashCode() | covered (Part-2) |
| 3 | equals() | covered (Part-3) |
| 4 | clone() | covered (Part-13 video 118) |
| 5 | getClass() | this video |

| Point | Detail |
|---|---|
| Who calls? | Garbage Collector (not the programmer directly in normal code) |
| When? | Just before destroying an object |
| Why? | To perform cleanup activities (close files, sockets, release native resources) |
| After finalize()? | GC automatically destroys the object |

| Thread role | Calls | Effect |
|---|---|---|
| Expecting update (consumer) | wait() | Enters waiting state until notified |
| Performing update (producer) | notify() / notifyAll() | Waiting thread(s) wake and continue |

| Trap / question | Answer |
|---|---|
| Return type of getClass()? | Class<?> (runtime class object) |
| Can we override getClass()? | No — final |
| Why Object obj = list.get(0) then obj.getClass()? | Discover real runtime type when compile-time type is only Object |
| One Class object or many per class? | One Class object per loaded class |
| Who calls finalize()? | Garbage Collector before destruction |
| Purpose of finalize()? | Cleanup activities |
| Where are wait/notify used? | Inter-thread communication (Multi Threading) |
| How many Object methods for exam? | 11 (exclude private registerNatives()) |

| Time | Topic |
|---|---|
| 00:05 | Introduce getClass() |
| 00:32 | Returns runtime class definition of an object |
| 00:47 | ArrayList / unknown element type scenario |
| 01:29 | Hold as Object; use getClass() for class info |
| 02:14 | Class c = obj.getClass() |
| 02:49 | c.getName(), c.getDeclaredMethods() |
| 04:36 | Reflection API; role of getClass() |
| 05:00 | JVM creates one Class object per loaded class |
| 06:15 | Board: use getClass for runtime class definition |
| 06:25 | Signature public final Class getClass() |
| 07:04 | Class-level properties via Class object |
| 08:21 | Example 1: String introspection program |
| 11:13 | Method in java.lang.reflect |
| 11:45 | Output: java.lang.String, 73 methods |
| 12:34 | Example 2: JDBC Connection vendor class |
| 13:18 | Do not hard-code vendor class names |
| 19:07 | con.getClass().getName() chaining |
| 19:59 | Board: JVM Class object creation on class load |
| 22:34 | getClass used frequently in Reflection |
| 22:50 | Five methods done: toString, hashCode, equals, clone, getClass |
| 23:07 | Introduce finalize() |
| 23:24 | Related to Garbage Collector |
| 23:40 | Eligible object (no references) |
| 24:03 | GC narrative — last wish / cleanup |
| 26:19 | GC calls finalize for cleanup before destroy |
| 27:10 | Full GC/finalization deferred to later module |
| 28:44 | Remaining: wait, notify, notifyAll |
| 29:17 | Inter-thread communication purpose |
| 29:26 | Producer–consumer / Queue analogy |
| 30:07 | Consumer calls wait() → waiting state |
| 30:18 | Producer calls notify() after update |
| 32:07 | Board: wait vs notify responsibilities |
| 34:00 | Preview only; detail in Multi Threading |
| 34:15 | All 11 Object methods surveyed — session end |

| Heard (Whisper) | Intended |
|---|---|
| get the class / get a class | getClass() |
| Uralist / URL list | ArrayList |
| getaf0 / get ab 0 | get(0) |
| object bo / O be J | Object obj |
| java dot length / Jawarat Lange | java.lang |
| class class object | Class object (type java.lang.Class) |
| reflections / reflection | Reflection API |
| Javiyam | JVM |
| Kanese / con | Connection con |
| my skill / vehicle | MySQL / Oracle (database vendors) |
| varicule | Oracle |
| APN names | API names |
| Pushing meta / hash core meta | toString(), hashCode() |
| Finalize meta / ice-mether | finalize() method |
| Carveic / Garbe / Gorbis collector | Garbage Collector |
| keep sabading / subtering | listen carefully |
| Aisium / conjomer / produsor | assume / consumer / producer |
| Weight method | wait() method |
| notified method | notify() method |
| eighth notified | wait(), notify() |
