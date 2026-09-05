# Video 071 — Default Exception Handling

## Video info

**Title:** Core Java with OCJP/SCJP: Exception Handling Part-2 || Default Exception Handling

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 71 of 203 |
| Series | Exception Handling · Part 2 |
| Topic | Default Exception Handling |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 15m 44s |
| Video ID | 46VtqhXIaeA |
| Watch | https://www.youtube.com/watch?v=46VtqhXIaeA |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Video 070 stopped right where something goes wrong. This video answers it:
**default exception handling** — what the JVM does when no `try-catch`
anywhere in the call chain deals with the problem. It has three parts: a
bike-accident analogy that walks a three-method program through JVM-driven
stack unwinding; seven formal board points plus the console output format;
and a first pass at the **exception hierarchy** — `Throwable`, `Exception`
vs. `Error`, and a partial class tree.

---

## 00:04 — Recap, then the fault: `10 / 0` inside `doMoreStuff`

Video 070's example never threw — it just printed `Hello` and returned
normally. The new question: **if something goes wrong, what happens, and how
do you handle it?** Sir builds the answer on the same three-method program,
first with no fault:

```java
class Test {
    public static void main(String[] args) {
        doStuff();
    }

    public static void doStuff() {
        doMoreStuff();
    }

    public static void doMoreStuff() {
        System.out.println("Hello");
    }
}
// compiles fine, prints Hello, normal termination — no problem at all
```

Then he swaps the body of `doMoreStuff` for a division by zero:

```java
class Test {
    public static void main(String[] args) {
        doStuff();
    }

    public static void doStuff() {
        doMoreStuff();
    }

    public static void doMoreStuff() {
        System.out.println(10 / 0);  // ArithmeticException — division by zero
    }
}
```

`10 / 0` is nothing but an exception — something has gone wrong.

## 01:34 — Runtime stack for the main thread

The JVM creates a separate runtime stack for the main thread:

| Stack (bottom → top) | How it got there |
|---|---|
| main | Entry point — always present by default |
| doStuff | main internally calls doStuff |
| doMoreStuff | doStuff internally calls doMoreStuff |

Inside `doMoreStuff`, `10 / 0` executes and throws — an "accident" in that
method's territory. If nobody handles it, you get **default exception
handling** — compulsory knowledge for every Java programmer, which is why
Sir reaches for an analogy before the formal rules.

## 02:38 — Analogy part 1: the bike accident (Hyderabad → Vijayawada)

Two people are riding a bike from Hyderabad toward Vijayawada. Past
Choutuppal they take a left turn, and a heavy truck coming the other way
hits them head-on — both riders go down on the road, badly hurt. That's
the shape of an exception: an **unexpected, unwanted event** that disturbs
what was otherwise a normal ride.

## 04:04 — Analogy part 2: who calls 108?

Immediately after the crash: **108** is the ambulance/emergency number in
India, **100** is the police. The victims can't call anyone themselves — it
has to be a local, responsible bystander. If nobody at the scene makes that
call, no help arrives on its own; **something has to trigger the response.**

## 05:21 — Personal experience: a real 108 call

Sir shares a real accident he witnessed: a car swerved to avoid a lorry and
hit a culvert, badly injuring the two people inside. He called 108 with the
location; an ambulance was promised in about 20 minutes. Police called back
within two minutes to confirm 108 had been informed and to ask about
traffic. Over the next ten minutes he got roughly ten follow-up calls from
different departments — traffic police, hospital coordination, 108 itself.
When the injured later left for treatment in Guntur in another car, he had
to call 108 again just to close the case — only then did the calls stop.

**The Java point:** when a serious problem occurs and the local handler does
nothing, responsibility escalates up the chain until some default handler —
108, or the JVM's own default exception handler — takes over.

## 08:07 — Analogy part 3: police arrive, formalities begin

After 15–20 minutes, police (100) arrive. First check: is anyone alive? In
the story, both are dead. Then come the time-consuming formalities —
identifying the victims, checking their phones for contacts. That's the
mapping onto the call chain:

```
main  →  calls  →  doStuff  →  calls  →  doMoreStuff
                                              ↑
                                    ArithmeticException here (accident)
```

`10 / 0` is the accident. If it happens and nobody handles it locally,
default handling kicks in — and the rest of the lecture works out exactly
what that means, one board point at a time.

## 09:07 — Board point 1: the method where it happens creates the object

**Inside any method, if an exception occurs, that method is responsible for
creating an Exception object** containing:

| Field in object | Example for `10/0` in `doMoreStuff` |
|---|---|
| Name of exception | ArithmeticException |
| Description | `/ by zero` (division by zero) |
| Location (stack trace) | doMoreStuff ← called by doStuff ← called by main |

That method then hands the object over to the **JVM**.

## 10:48 — JVM visits `doMoreStuff`: any handling code?

The JVM goes straight to the method where the problem occurred and asks:
*"Do you have any exception handling code?"* `doMoreStuff` has none. The
JVM's response:

1. **Terminate this method abnormally** — even with a thousand lines left,
   none of them run.
2. **Remove** the corresponding stack frame.

```java
public static void doMoreStuff() {
    System.out.println(10 / 0);
    System.out.println("This line NEVER runs");  // skipped — abnormal termination
}
```

## 12:01 — JVM escalates to the caller: `doStuff`

`doMoreStuff` didn't call itself — the JVM identifies its caller, `doStuff`,
and asks the same question. No handling code there either, so the JVM
terminates `doStuff` abnormally and removes its stack entry too, again
skipping anything left after the `doMoreStuff()` call.

## 13:44 — JVM escalates to `main`

`doStuff`'s caller is `main`. Sir's framing: **`main` gives the JVM a "red
carpet welcome"**, because `main` and the JVM are best friends — the JVM is
the one that invoked `main` in the first place. The JVM asks the same
question anyway: *"Do you have handling code?"* `main` doesn't — it doesn't
even know what happened deep inside `doMoreStuff`.

## 15:48 — Rule is rule: `main` gets terminated too

`main` pleads its friendship. The JVM's answer, in Sir's Telugu phrase,
**"Dharmam dharmam"** — rule is rule, friend or not. The JVM terminates
`main` abnormally and removes its stack entry. Now no method anywhere in
the chain has handled the exception.

## 16:19 — The Default Exception Handler

Since no method handled it, the JVM itself has to respond. The JVM keeps an
assistant for exactly this — the **Default Exception Handler** — and hands
it the exception object with instructions: handle this, because nobody else
did. That handler does exactly two things:

1. **Print exception information** to the console (stderr).
2. **Terminate the program abnormally.**

## 17:15 — Console output format (first live run)

For `10/0` inside `doMoreStuff`:

```text
Exception in thread "main" java.lang.ArithmeticException: / by zero
    at Test.doMoreStuff(Test.java:9)
    at Test.doStuff(Test.java:6)
    at Test.main(Test.java:3)
```

| Line | Meaning |
|---|---|
| `Exception in thread "main"` | Which thread had the problem |
| `java.lang.ArithmeticException: / by zero` | Name + description |
| `at Test.doMoreStuff(...)` | Stack trace — where, and who called whom |

Who prints this? The **Default Exception Handler**. What kind of
termination is this? **Abnormal** — not a clean `main` return.

## 18:21 — One-minute recap

1. Exception rises in a method → that method creates the Exception object →
   hands it to the JVM.
2. JVM checks that method for handling code → none → terminate abnormally,
   pop the stack frame.
3. Repeat for the caller, then the caller's caller, … up to `main`.
4. If `main` also has no handler → terminate `main`, pop its frame.
5. JVM hands off to the Default Exception Handler → print → abnormal exit.

**Debugging tip:** don't panic and re-read the source twenty times blind.
Read the exception message two or three times first — thread name, exception
name, description, and stack trace tell you exactly where to look.

## 19:36 — Live demo: compile and run

```java
class Test {
    public static void main(String[] args) {
        doStuff();
    }

    public static void doStuff() {
        doMoreStuff();
    }

    public static void doMoreStuff() {
        System.out.println(10 / 0);
    }
}
```

```text
javac Test.java   # compiles fine — division by zero is NOT a compile-time error
java Test         # runtime: default handler output, abnormal exit
```

Compilation succeeds because `10/0` is legal syntax; the failure is a
**runtime** event. Swap it back to `Hello` and the program prints `Hello`
and terminates normally, no default handler involved.

## 23:24 — Formal board notes begin

Sir switches to board terminology for exam and interview prep — the same
flow as the analogy, restated as seven numbered points.

## 23:32 — Board point 1 (restated): create the Exception object

> **Inside a method, if any exception occurs, the method in which it is
> raised is responsible to create an Exception object, including:**
> 1. **Name of the exception**
> 2. **Description of the exception**
> 3. **Location at which the exception occurs** (the stack trace)

```java
// Conceptual — you never write this; the JVM constructs it internally
// new ArithmeticException("/ by zero")
//   + stack trace elements:
//       Test.doMoreStuff(Test.java:line)
//       Test.doStuff(Test.java:line)
//       Test.main(Test.java:line)
```

## 25:46 — Board point 2: hand the object to the JVM

> **After creating the Exception object, the method hands it over to the
> JVM.**

The raising method never prints anything itself in default handling — it
delegates upward immediately.

## 26:17 — Board point 3: JVM checks the current method for handling code

> **The JVM checks whether that method contains exception handling code.**
> If not, the **JVM terminates that method abnormally** and **removes its
> entry from the stack.**

```java
public static void doMoreStuff() {
    System.out.println(10 / 0);
    System.out.println("This line NEVER runs");  // skipped — abnormal termination
}
```

## 28:06 — Board point 4: identify the caller, repeat

> **The JVM identifies the caller method and checks it too.** No handling
> code there either → terminate the caller abnormally, remove its stack
> entry.

```java
public static void doStuff() {
    doMoreStuff();
    System.out.println("Never reached if doMoreStuff threw");  // skipped in Example 1
}
```

## 30:04 — Board point 5: continue until `main`

> **This process continues until the `main` method.**

For Example 1 (`10/0` inside `doMoreStuff`), the chain is:

| Step | Method | Handling code? | Action |
|---|---|---|---|
| 1 | doMoreStuff | No | Terminate + pop |
| 2 | doStuff | No | Terminate + pop |
| 3 | main | No | Terminate + pop |

## 30:26 — Board point 5, continued: `main` also terminates

> **If `main` also has no handling code, the JVM terminates `main`
> abnormally and removes its entry from the stack too.**

After this, the runtime stack for the thread is empty of application frames
— there's no user code left to run.

## 31:53 — Board point 6: hand off to the Default Exception Handler

> **The JVM then hands over responsibility to the Default Exception
> Handler.**

The default handler is part of the JVM, not your application code.

## 32:55 — Board point 7: print and terminate

> **The Default Exception Handler prints exception information to the
> console in a fixed format, then terminates the program abnormally.**

## 33:36 — The output format formula

General template (`xxx` = thread name — usually `"main"`, but any thread
name is possible):

```text
Exception in thread "xxx" : <name of exception> : <description>
    <stack trace>
```

Concrete instance for this program:

```text
Exception in thread "main" java.lang.ArithmeticException: / by zero
    at Test.doMoreStuff(Test.java:9)
    at Test.doStuff(Test.java:6)
    at Test.main(Test.java:3)
```

**Memorize:** name of exception · description · stack trace.

## 35:06 — Board rewrite: Example 1 restated

```java
class Test {
    public static void main(String[] args) {
        doStuff();
    }

    public static void doStuff() {
        doMoreStuff();
    }

    public static void doMoreStuff() {
        System.out.println(10 / 0);
    }
}
```

Call chain: `main` → `doStuff` → `doMoreStuff`, problem in `doMoreStuff`,
same expected output as above.

## 39:35 — Example 1 analysis: how many methods terminated how?

All three methods (`main`, `doStuff`, `doMoreStuff`) terminate **abnormally**
when the exception originates in `doMoreStuff` and there's no `try-catch`
anywhere. The program termination is abnormal too.

## 39:57 — Variant A: move the fault to `doStuff`

Print `Hello` successfully inside `doMoreStuff`; move the division by zero
to `doStuff`, after the call to `doMoreStuff` returns:

```java
class Test {
    public static void main(String[] args) {
        doStuff();
    }

    public static void doStuff() {
        doMoreStuff();
        System.out.println(10 / 0);  // exception HERE, after doMoreStuff returns
    }

    public static void doMoreStuff() {
        System.out.println("Hello");
    }
}
```

**Flow:** `doMoreStuff` prints `Hello`, completes normally, its frame is
popped. Control returns to `doStuff`; `10/0` throws there. `doStuff` has no
handler → abnormal termination → pop. `main` has no handler → abnormal
termination → pop. The default handler's stack trace is now rooted at
`doStuff`, not `doMoreStuff`:

```text
Hello
Exception in thread "main" java.lang.ArithmeticException: / by zero
    at Test.doStuff(Test.java:7)
    at Test.main(Test.java:3)
```

| Terminated normally | Terminated abnormally |
|---|---|
| `doMoreStuff` (1) | `doStuff`, `main` (2) |

The program still ends abnormally overall — one abnormal method is enough.

## 42:08 — Live demo: Variant A confirmed

`Hello` prints first, then the exception block — and the stack trace shows
only `Test.doStuff` and `Test.main`, because `doMoreStuff` already finished
cleanly and left no trace behind.

## 43:07 — Variant B: two lines in `doMoreStuff` before the fault

Add a second print statement in `doMoreStuff`, after `Hello`:

```java
class Test {
    public static void main(String[] args) {
        doStuff();
    }

    public static void doStuff() {
        doMoreStuff();
        System.out.println(10 / 0);
    }

    public static void doMoreStuff() {
        System.out.println("Hello");
        System.out.println("Hi");
    }
}
```

`doMoreStuff` prints `Hello`, then `Hi`, and completes normally — pop. Then
`doStuff` hits `10/0`, and both `doStuff` and `main` terminate abnormally:

```text
Hello
Hi
Exception in thread "main" java.lang.ArithmeticException: / by zero
    at Test.doStuff(Test.java:8)
    at Test.main(Test.java:3)
```

| Terminated normally | Terminated abnormally |
|---|---|
| `doMoreStuff` (1) | `doStuff`, `main` (2) |

## 45:06 — Live demo: Variant B confirmed

Output order confirmed on screen: `Hello` → `Hi` → the exception block.

## 46:13 — Example 2: `10/0` directly in `main`

Move the fault into `main` itself; `doStuff` and `doMoreStuff` just print:

```java
class Test {
    public static void main(String[] args) {
        doStuff();
        System.out.println(10 / 0);  // exception in main, after doStuff returns
    }

    public static void doStuff() {
        doMoreStuff();
    }

    public static void doMoreStuff() {
        System.out.println("Hello");
        System.out.println("Hi");
    }
}
```

**Flow:** `main` → `doStuff` → `doMoreStuff` prints `Hello`, `Hi`, and every
call returns normally all the way back up. Then, back in `main`, `10/0`
throws. Only `main` lacks a handler, so only `main` terminates abnormally —
but that's still enough to make the whole program's termination abnormal.

```text
Hello
Hi
Exception in thread "main" java.lang.ArithmeticException: / by zero
    at Test.main(Test.java:4)
```

The stack trace shows only `Test.main` — the inner methods already
completed and left no frame behind.

| Terminated normally | Terminated abnormally |
|---|---|
| `doMoreStuff`, `doStuff` (2) | `main` (1) |

## 47:25 — Example 2, conceptually: code after the fault in `main`

If `main` had a line after the fault, it simply would not run:

```java
class Test {
    public static void main(String[] args) {
        doStuff();
        System.out.println(10 / 0);
        System.out.println("main completed");  // NEVER prints
    }

    public static void doStuff() {
        doMoreStuff();
    }

    public static void doMoreStuff() {
        System.out.println("Hello");
        System.out.println("Hi");
    }
}
```

Students often expect `"main completed"` to appear — it doesn't, because
abnormal termination skips every remaining statement in `main`.

## 48:29 — Two rules for the notebook: method vs. program termination

### Rule A — at least one abnormal method ⇒ abnormal program

> **If at least one method in a program terminates abnormally, the program's
> termination is abnormal.**

```java
// Even if doMoreStuff and doStuff finish normally,
// one abnormal main ⇒ the whole JVM exit is abnormal
public static void main(String[] args) {
    doStuff();
    System.out.println(10 / 0);
}
```

### Rule B — every method normal ⇒ normal program

> **If every method terminates normally, the program's termination is
> normal.**

```java
class Test {
    public static void main(String[] args) {
        doStuff();
        System.out.println("main completed");
    }

    public static void doStuff() {
        doMoreStuff();
    }

    public static void doMoreStuff() {
        System.out.println("Hello");
    }
}
// prints: Hello
//         main completed
// (normal program termination)
```

## 50:44 — End of default handling; preview of custom handling

**Summary:** with no `try-catch` written anywhere, the JVM performs default
exception handling — unwind the stack, print diagnostics, exit abnormally.
If that's not acceptable, the next topic is **customized exception handling
with `try-catch`** — covered starting Video 072.

## 50:49 — Transition: the exception hierarchy

New heading: **Java's exception hierarchy** — "the most valuable concept" in
Sir's framing. Interview question: **which class is the root of the Java
exception hierarchy?** Answer: **`Throwable`**. Note the distinction: for
*all* Java classes the root is `Object`; for the *exception hierarchy
specifically*, the root is `Throwable`.

## 51:42 — `Throwable` in detail

```java
// java.lang.Throwable — a CLASS, not an interface, despite the "-able" name
// pattern shared with Serializable, Cloneable, Runnable
class Throwable extends Object { /* ... */ }
```

`Throwable` is the root for every Java exception **and** every error, and it
has exactly two direct child classes: **`Exception`** and **`Error`**.

## 53:07 — `Exception` vs. `Error`

| Aspect | Exception | Error |
|---|---|---|
| Usually caused by | Our program (a programmatic mistake) | Not our program — lack of system resources |
| Recoverable? | Yes | No |
| Programmer action | Can often catch and recover | Cannot fix in code — needs an admin or more memory |
| Examples | `FileNotFoundException`, `ArithmeticException` | `OutOfMemoryError`, `StackOverflowError` |

## 54:45 — Exceptions: caused by the program, recoverable

Most of the time, exceptions come from our own program. **Recoverable**
means: after the exception, you can take an alternate action and continue
the rest of the program normally. Sir's running scenario: read data from a
remote file located in London.

```java
import java.io.*;

class RemoteFileReader {
    public static void main(String[] args) {
        try {
            readDataFromRemoteFile("London/data.txt");
        } catch (FileNotFoundException e) {
            useLocalFile("local/data.txt");  // RECOVER: use local fallback
        }
        System.out.println("Rest of program continues normally");
    }

    static void readDataFromRemoteFile(String path) throws FileNotFoundException {
        FileInputStream fis = new FileInputStream(path);
        // read...
    }

    static void useLocalFile(String path) {
        System.out.println("Using local file: " + path);
    }
}
```

If the remote file is missing, `FileNotFoundException` is caused by our
code's assumption, but we recover with a local file and keep going. Without
`try-catch` the default handler would kill the program; with it, the
exception is recoverable — no problem at all, catch it, continue.

> ⚠️ **Modern Java — close the stream, don't just catch the exception.**
> `readDataFromRemoteFile` above opens a `FileInputStream` and never closes
> it — fine for illustrating the exception, but a real resource leak if the
> `try` body threw partway through reading. Since **Java 7**, the fix is
> **try-with-resources**, and since **Java 9** the resource variable doesn't
> even need to be declared inside the parentheses if it's already effectively
> final:
> ```java
> static void readDataFromRemoteFile(String path) throws IOException {
>     try (FileInputStream fis = new FileInputStream(path)) {
>         // read... — fis.close() runs automatically, even if an exception is thrown
>     }
> }
> ```
> Sir's own `try (...)` syntax for this arrives later in the series
> (Video 079); flag it here because this is the first place in the lecture a
> stream is opened and left dangling.

## 57:00 — Errors: not caused by the program, non-recoverable

Errors are usually **not** caused by our program — they come from a lack of
system resources — and they are **non-recoverable** from application code.

```java
// StackOverflowError — infinite / too-deep recursion, no base case
class StackOverflowDemo {
    public static void main(String[] args) {
        recursive();
    }
    static void recursive() {
        recursive();  // each call pushes a frame until the stack is exhausted
    }
}
```

```java
// OutOfMemoryError — heap cannot allocate more objects
import java.util.*;

class OutOfMemoryDemo {
    public static void main(String[] args) {
        List<byte[]> list = new ArrayList<>();
        while (true) {
            list.add(new byte[10_000_000]);  // eventually the heap is exhausted
        }
    }
}
```

If `OutOfMemoryError` occurs, there's nothing meaningful a programmer can do
in code to keep going — the program terminates abnormally, and a system or
server admin has to increase heap memory (`-Xmx`, server config).
**Spelling note:** `OutOfMemoryError` — no space in the middle, an exam
detail Sir calls out explicitly.

## 1:02:50 — Exception vs. Error, side by side

```java
// EXCEPTION path — catch and recover
try {
    readRemote("London/server.dat");
} catch (FileNotFoundException e) {
    readLocal("backup.dat");  // continue
}

// ERROR path — nothing useful to catch as a recovery
// OutOfMemoryError → stop; call the admin for more heap
```

|  | Exception | Error |
|---|---|---|
| Cause | Program logic / environment interaction we coded | JVM / system resource exhaustion |
| Fix | Fix the code, or catch and take an alternate path | Increase memory, fix recursion, JVM tuning |
| Catch in practice? | Yes (`try-catch`) | Technically catchable, but never treat it as recoverable |

## 1:06:35 — Child classes under `Exception`

Sir lists the direct children of `Exception` on the board, then the notable
classes underneath each:

| Direct child of Exception | Notable descendants |
|---|---|
| `RuntimeException` | ArithmeticException, NullPointerException, ClassCastException, ArrayIndexOutOfBoundsException, StringIndexOutOfBoundsException, IllegalArgumentException, NumberFormatException |
| `IOException` | EOFException, `FileNotFoundException`, InterruptedIOException, `RemoteException` |
| `SQLException` | (database errors) |
| `ServletException` | (web) |
| `InterruptedException` | (thread interrupt) |

```java
// ArithmeticException
int x = 10 / 0;

// NullPointerException
String s = null;
s.length();

// ClassCastException
Object o = "hello";
Integer i = (Integer) o;

// ArrayIndexOutOfBoundsException
int[] a = new int[3];
a[10] = 1;

// StringIndexOutOfBoundsException
"abc".charAt(10);

// NumberFormatException (child of IllegalArgumentException)
Integer.parseInt("abc");
```

```java
import java.io.*;

// FileNotFoundException
new FileInputStream("missing.txt");

// EOFException — reading past end of file
// InterruptedIOException — I/O interrupted during a thread interrupt
```

> ❗ **Correction — this tree flattens two real intermediate classes.**
> Checked with `javap` against the JDK actually installed here:
> - **`ArrayIndexOutOfBoundsException`** and **`StringIndexOutOfBoundsException`**
>   both extend **`IndexOutOfBoundsException`**, which extends
>   `RuntimeException` — they are grandchildren of `RuntimeException`, not
>   direct children.
> - **`RemoteException`** (RMI) extends **`IOException`**, not `Exception`
>   directly — it belongs under the `IOException` row above, not as a sibling
>   of it.
>
> None of this changes any exam answer about *which root class* something
> ultimately descends from — `RuntimeException` either way — but "is X a
> direct child of Y" is exactly the kind of question OCJP likes to ask, and
> the honest tree has one more layer than the board sketch. Every class name
> here is otherwise correct and unchanged in current Java.

> ⚠️ **Modern Java — the `NullPointerException` example now tells you which
> reference was `null`.** Since **Java 14** (JEP 358, on by default from 15),
> an uncaught NPE names the exact expression that was `null`:
> ```text
> Exception in thread "main" java.lang.NullPointerException:
>     Cannot invoke "String.length()" because "s" is null
>     at NPE.main(NPE.java:4)
> ```
> The variable name (`"s"` above) only appears when the class was compiled
> with debug info (the default from an IDE, or `javac -g`); otherwise you
> get a slot number like `"<local1>"`. Same exception class, same hierarchy
> position — just a far more useful message than the bare stack trace Sir is
> teaching against here.

## 1:09:31 — Child classes under `Error`

| Direct child of Error | Notable descendants |
|---|---|
| `VirtualMachineError` | `StackOverflowError`, `OutOfMemoryError` |
| `LinkageError` | `ExceptionInInitializerError` |

```java
// ExceptionInInitializerError — a static initializer throws
class BadStaticInit {
    static {
        if (true) throw new RuntimeException("init failed");
    }
    public static void main(String[] args) {
        new BadStaticInit();  // triggers ExceptionInInitializerError
    }
}
```

> ❗ **Correction — `ExceptionInInitializerError` is not a direct child of
> `Error`.** It extends **`LinkageError`**, which extends `Error` — one more
> layer than the board diagram shows. Confirmed by actually compiling and
> running the example above on JDK 26:
> ```text
> Exception in thread "main" java.lang.ExceptionInInitializerError
> Caused by: java.lang.RuntimeException: init failed
>     at BadStaticInit.<clinit>(BadStaticInit.java:3)
> ```
> Two more things worth noticing in that real output: the failure happens
> during class initialization (`<clinit>`) — *before* `main`'s body ever
> runs the `new BadStaticInit()` line, because just calling `main` already
> triggers the class to initialize — and the default handler prints a
> `Caused by:` chain, not the flat single-exception format taught earlier in
> this lecture. `Throwable`'s cause-chaining (`getCause()`) is a Java 1.4
> feature the board notes don't mention at all; it is why the printed output
> here has two blocks instead of one.

Also on the board, but not part of `Error`'s **direct** children: Sir
mentions `AssertionError` as another notable exception-hierarchy class —
it *is* a direct child of `Error` (unlike `ExceptionInInitializerError`),
raised by a failed `assert` statement.

## 1:10:34 — Partial hierarchy diagram (corrected)

```text
                                    Object
                                      |
                                  Throwable
                                 /         \
                          Exception         Error
                         /    \                \
            RuntimeException  IOException    VirtualMachineError   LinkageError    AssertionError
               /  |  |  \           \          /         \              |
ArithmeticException |  |  IndexOutOfBoundsException  StackOverflow  OutOfMemory  ExceptionInInitializerError
NullPointerException|  |     /            \
ClassCastException  |  |  ArrayIndexOutOfBounds  StringIndexOutOfBounds
        IllegalArgumentException      FileNotFoundException, EOFException,
                |                     InterruptedIOException, RemoteException
        NumberFormatException
```

**Also under `Exception` (direct):** `SQLException`, `ServletException`,
`InterruptedException`, …

Sir has the class copy the full tree from the board for exam prep (OCJP /
SCJP); the version above folds in the `IndexOutOfBoundsException` and
`LinkageError` layers from the correction above so the diagram matches what
actually compiles.

## 1:11:24 — Hierarchy review questions

Quick oral revision, straight from the lecture:

1. **Root of the exception hierarchy?** → `Throwable`
2. **Two children of `Throwable`?** → `Exception`, `Error`
3. **Difference between Exception and Error?** → program-caused and
   recoverable, vs. resource/system-caused and non-recoverable
4. **`RuntimeException` descendants?** → arithmetic, NPE, class cast, index
   bounds, illegal argument, number format, …
5. **`IOException` descendants?** → EOF, file not found, interrupted IO,
   remote, …
6. **`VirtualMachineError` descendants?** → stack overflow, out of memory

## 1:14:22 — Session wrap-up

Video 071 closes out default exception handling — theory, demos, and a
partial exception hierarchy tree. Next in the playlist: checked vs.
unchecked exceptions, then `try-catch`, `finally`, `throw`/`throws`, and the
rest of the exception-handling block (Videos 072+).

---

## Exam and interview points

1. **The seven-point default-handling formula, in order:** the method where
   the exception rises creates the Exception object (name, description,
   stack trace) → hands it to the JVM → JVM checks that method for handling
   code, terminates it and pops the frame if there is none → repeats for
   each caller up to `main` → if `main` also has none, terminates `main` too
   → JVM hands off to the Default Exception Handler → handler prints and
   the program exits abnormally.
2. **Output format to recognize instantly:**
   `Exception in thread "<name>" <ExceptionType>: <description>` followed by
   the stack trace — thread, type, message, then top-of-stack = where it
   broke.
3. **Method termination vs. program termination are different questions.**
   If *at least one* method in the chain terminates abnormally, the whole
   program's termination is abnormal — even if every other method finished
   cleanly. Only if *every* method terminates normally does the program.
4. **Root of the exception hierarchy is `Throwable`** (a class, not an
   interface, despite the `-able` name), with exactly two direct children:
   `Exception` and `Error`.
5. **Exception vs. Error, memorized as a pair:** Exception — usually our
   program's fault, recoverable, catch and continue. Error — usually a lack
   of system resources, non-recoverable, needs an admin or more memory, not
   a code fix.
6. **The "direct child" hierarchy has more layers than the board sketch
   shows.** `ArrayIndexOutOfBoundsException` / `StringIndexOutOfBoundsException`
   go through `IndexOutOfBoundsException`; `ExceptionInInitializerError`
   goes through `LinkageError`; `RemoteException` goes through `IOException`.
   Verified against the actual JDK class hierarchy, not just the board
   diagram — useful if an interviewer asks "is that a *direct* subclass?"
7. **Since Java 14, an uncaught `NullPointerException` names the exact
   `null` reference** in its message instead of just pointing at a line
   number — same exception, much better diagnostics, and the variable name
   only shows up when the class carries debug info.
8. **Spell `OutOfMemoryError` with no space** — a named exam trap.

---

**Next:** Video 072 — Checked vs unchecked exceptions
