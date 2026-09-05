# Video 070 — Exception Handling Introduction

## Video info

**Title:** Core Java with OCJP/SCJP: Exception Handling Part-1 || Introduction

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 70 of 203 |
| Series | Exception Handling · Part 1 |
| Topic | Introduction |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 54m 53s |
| Video ID | zg4jYJjNEYI |
| Watch | https://www.youtube.com/watch?v=zg4jYJjNEYI |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Sir calls exception handling "the most valuable concept in the total Java"
and opens with the full roadmap for the whole series — roughly 20 subtopics,
15–20 hours of material. This Part-1 video itself only gets through the
**first two** of those: the plain-language definition of an exception, and
the runtime-stack mechanism on a program where nothing goes wrong. He
announces **default exception handling** as the next heading at 53:54 and
stops there — the JVM's default handler, `printStackTrace`, and what happens
to `main` on an uncaught exception are all Video 071's job, not this one.

---

## 00:04 — Next topic: exception handling

Exception handling is next, and Sir flags it as one of his favorite topics —
his promise is that after this series you should have every point related to
it. He starts, as usual, with the agenda, and tells the class to cross-check
it later against what actually gets covered.

## 00:37 — The spoken agenda (the whole series, not just this video)

1. What is an **exception**, and what is the meaning of **exception handling**.
2. **Runtime stack mechanism** — a runtime stack exists per thread; how it
   plays a role in exception handling.
3. **Default exception handling in Java** — what Java does by default when
   you handle nothing.
4. **Exception hierarchy** — `Throwable` as parent, `Exception` and `Error`
   as children; exception vs. error; checked vs. unchecked.
5. **Customized exception handling with try-catch** — the role of `try` and
   `catch`.
6. **Control flow in try-catch** — what happens when an exception is raised
   and the catch matches, when it doesn't match, and when nothing is raised.
7. **Methods to print exception information** — three of them.
8. **try with multiple catch blocks** — when, and under which rules.
9. **`finally` block.**
10. Interview favorite: **`final` vs. `finally` vs. `finalize`.**
11. **Control flow in try-catch-finally**, then **nested try-catch-finally.**
12. **Every combination of try-catch-finally** — Sir counts roughly 24–25 of
    them: try-catch-finally, try without catch, finally without try, try-catch
    inside finally, and so on.
13. **`throw` and `throws`.**
14. **Exception-handling keyword summary.**
15. **Compile errors in exception handling** — roughly eight or nine, each one
    an interview question in its own right.
16. **Customized / user-defined exceptions** — how to define and use your own.
17. **Ten case studies** of commonly occurring exceptions — his named example:
    `NullPointerException`, when you get it, checked or unchecked.
18. **Java 1.7 enhancements** — try-with-resources and the multi-catch block.

His guarantee: get through these ~20 topics and you can call yourself king of
exception handling.

> ⚠️ **Modern Java — three agenda items have moved since this recording.**
> - **Item 10 (`finalize`)**: `Object.finalize()` was marked `@Deprecated`
>   in **Java 9**, and **Java 18** (JEP 421) deprecated the whole
>   finalization mechanism **for removal**. It still runs today — nothing
>   was disabled by default — but the JDK itself now warns you off it:
>   ```text
>   warning: [removal] finalize() in Object has been deprecated and marked for removal
>   ```
>   By the time you reach a "when would you use `finalize`" interview
>   question, the honest current answer is "never — use `try`-with-resources
>   or a `Cleaner`."
> - **Item 17 (`NullPointerException`)**: since **Java 14** (JEP 358,
>   default from 15), an uncaught `NullPointerException` tells you exactly
>   which reference was `null` — e.g. `Cannot invoke "String.length()"
>   because "s" is null` — instead of just a bare stack trace pointing at a
>   line number. Same exception class, far less guesswork.
> - **Item 18 (try-with-resources)**: introduced in Java 7 as this course
>   already teaches, then improved in **Java 9** — a resource variable that
>   is already effectively final can be used directly, without redeclaring
>   it inside the `try(...)`:
>   ```java
>   FileReader fr = new FileReader("local-file.txt");
>   try (fr) {           // Java 9+ — fr itself, not "try (FileReader fr2 = fr)"
>       // use fr
>   }
>   ```

## 08:32 — The agenda is itself a big topic

Even by Sir's own count the agenda runs 17–20 subtopics, and he estimates
15–20 hours of lecture time to get through all of it. He calls out the first
four items — introduction, runtime stack mechanism, default exception
handling, exception hierarchy — as purely theoretical and "a bit boring";
everything after that gets more hands-on.

## 11:08 — Introduction: "Can you define what is an exception?"

He asks the class for a definition of *exception* precise enough that
nobody needs a follow-up question. The answers he gets back — "runtime",
"unexpected situation", "abnormal termination", "runtime error" — are all
**relevant** but not yet the exact definition. He builds that definition
through three stories.

## 12:01 — Story 1: the Vanasthalipuram student and `SleepingException`

A student travels 30–40 km from Vanasthalipuram for a 7:00 a.m. class in
Ameerpet: alarm at 2:00, awake at 5:30, bus by 6:00, in the classroom by
7:00 — everything according to plan. Five to ten minutes into class, he
falls asleep. That's the disturbance: an **unexpected, unwanted event that
disturbs the normal flow of execution.** Sir names it `SleepingException` and
is immediate about one thing: **don't go looking for this in the Java API —
it's a name he made up for the story, not a real exception class.**

```java
class SleepingExceptionDemo {
    public static void main(String[] args) {
        System.out.println("class started — listen to faculty");
        System.out.println("use the concept in interview / job");
        // 5-10 minutes in: unexpected, unwanted event —
        // "SleepingException" is a classroom name only, not in the Java API
        System.out.println("SleepingException — remaining flow disturbed");
    }
}
// prints class started — listen to faculty
// prints use the concept in interview / job
// prints SleepingException — remaining flow disturbed
```

## 15:26 — Story 2: the Madhapur commuter and `TirePuncturedException`

A second student starts closer, from Madhapur, leaving at 6:30 on a
two-wheeler for the same 7:00 class, planning to go straight to the office
at 9:00. After Masab Tank he takes a left turn and the tire punctures — no
repair shop open that early, so he has to walk the bike back and misses
class entirely. Same shape of event, same made-up name pattern:
`TirePuncturedException`.

```java
class TirePuncturedExceptionDemo {
    public static void main(String[] args) {
        System.out.println("6:30 start from Madhapur on two-wheeler");
        System.out.println("after Masab Tank take left — 7:00 class, 9:00 office");
        // unexpected, unwanted event — classroom name, not in the API
        System.out.println("TirePuncturedException — walk back, miss the class");
    }
}
```

## 17:19 — The technical example: a missing file at London

Now a real Java case. The requirement is to read data from a remote file
located at London. The program starts fine, but at runtime the file simply
isn't there — an unexpected event disturbing the normal flow, and this time
it has a real name: **`FileNotFoundException`**. Without the data, the
program can't continue and terminates abnormally.

```java
import java.io.FileNotFoundException;
import java.io.FileReader;

class ReadLondonFile {
    public static void main(String[] args) throws FileNotFoundException {
        System.out.println("program started normally");
        FileReader fr = new FileReader("london-file.txt"); // not there at runtime
        System.out.println("this line is not reached");
    }
}
// program started normally
// Exception in thread "main" java.io.FileNotFoundException: london-file.txt (No such file or directory)
```

He hasn't taught checked-vs-unchecked yet, so the `throws` clause here is
just what makes the file compile — the point he wants is only the runtime
story: file missing → `FileNotFoundException` → abnormal termination. An
exception, he says, can be `SleepingException`, `TirePuncturedException`,
`FileNotFoundException`, `SQLException` — anything that disturbs the normal
flow of the program.

## 18:54 — Board definition of "exception"

He dictates this repeatedly for the notebook:

> *An **unexpected unwanted event** that **disturbs the normal flow of the
> program** is called **exception**.*
>
> Examples: `TirePuncturedException`, `SleepingException`,
> `FileNotFoundException`.

## 20:46 — Is handling recommended? Yes — graceful termination

**Is it recommended to handle exceptions? Highly recommended** — it's the
whole name of the topic. So what's the purpose?

"Something goes wrong" is very common, Sir says — if programs never failed,
neither he nor the class would need to be here. When something does go
wrong, the requirement is: **don't miss anything, don't lose anything,
continue normally.** His example: two hours into a project report, with an
adjusted diagram and unsaved work, the power goes. Ten or fifteen minutes
later it's back, and everything typed is gone — you retype, having lost
real work, because nothing caught that failure gracefully.

## 23:00 — Programmatic version: an SQL exception leaks a DB connection

A three-step program — open a DB connection, read data, close the
connection — hits an `SQLException` while reading. Unhandled, the program
terminates right there, and nothing ever runs `closeTheDatabase()`. One
connection stays open and wasted. Ten runs of the same bug wastes ten
connections; if the server caps out at ten, the eleventh caller can't get a
connection at all, and the whole application goes down.

```java
class OpenDbReadClose {
    public static void main(String[] args) {
        openDbConnection();
        readTheData();          // SQLException here if unhandled
        closeTheDatabase();     // never reached — connection leaked
    }

    static void openDbConnection() { System.out.println("open DB connection"); }

    static void readTheData() {
        System.out.println("read the data");
        throw new RuntimeException("SQLException while reading"); // stands in for SQLException
    }

    static void closeTheDatabase() { System.out.println("close the database"); }
}
// prints open DB connection
// prints read the data
// then: uncaught exception, program dies — closeTheDatabase() never runs
```

## 24:29 — Main purpose: close, then stop

**The main objective of exception handling is graceful termination:** if an
exception occurs, close the database connection first and *then* stop the
program — free the resource for the next caller instead of blocking it
forever. He hasn't taught `catch` syntax formally yet, but the idea he wants
on the board is exactly a `catch` block that closes first and stops second:

```java
class OpenDbGraceful {
    public static void main(String[] args) {
        openDbConnection();
        try {
            readTheData();
            closeTheDatabase();
        } catch (RuntimeException e) { // stands in for SQLException here
            closeTheDatabase();        // close first
            return;                    // then stop — connection is free again
        }
    }

    static void openDbConnection() { System.out.println("open DB connection"); }

    static void readTheData() {
        System.out.println("read the data");
        throw new RuntimeException("SQLException while reading");
    }

    static void closeTheDatabase() { System.out.println("close the database"); }
}
// prints open DB connection
// prints read the data
// prints close the database
```

The laptop-UPS version of the same idea: five minutes of battery is enough
to save your work and shut down cleanly, so nothing is lost when power comes
back. **Graceful termination** — don't miss anything, don't lose anything.

## 26:56 — The meaning of exception handling: not repairing

Next question: does "handling" mean *repairing* the exception? Sir answers
with a third version of the Madhapur puncture, now at 6:45 a.m., with three
possible responses:

| Approach | Result | Handling? |
|---|---|---|
| Leave the bike on the road, take an auto to class | Bike may or may not still be there afterward | No — you're missing something |
| Walk the bike back to the room first | You miss the class | No — you're missing something |
| Park it at a friend's place nearby, tell the friend, take an auto | Keep the class *and* the bike, minutes lost | **Yes — this is handling** |

The third option is the only one where nothing is actually lost. That's the
definition: **defining an alternative way to continue the rest of the
program normally** — not fixing the underlying problem.

## 29:12 — Alternative paths: bus, train, flight

No bus ticket? Try a train ticket; failing that, a flight — the journey
itself must not stop, and arranging your own bus is not your job. Same
pattern in code: catch the failure on one path, and take another.

```java
class BusThenTrain {
    public static void main(String[] args) {
        try {
            takeBus();
        } catch (RuntimeException busTicketNotAvailable) {
            takeTrain(); // alternative path — the journey isn't stopped
        }
    }

    static void takeBus() { throw new RuntimeException("bus ticket not available"); }

    static void takeTrain() {
        System.out.println("train ticket — continue the journey normally");
    }
}
// prints train ticket — continue the journey normally
```

The classroom's own 5-hour generator backup makes the same point: power
goes, but the session doesn't stop, because there's an alternative supply
ready to take over.

## 30:17 — Programmatic meaning: London file missing → use a local file

Back to the London file. At runtime, if it's missing, the program should
*not* terminate abnormally — the `catch` block should reach for a local file
kept on standby and continue normally. **Exception handling does not mean
repairing the exception** — Sir is explicit that he's not responsible for
putting the London file back; he's only responsible for having a fallback.
The board version he has the class copy:

```java
import java.io.FileNotFoundException;

class ReadLondonOrLocal {
    public static void main(String[] args) {
        try {
            readDataFromRemoteFileLocatedAtLondon();
        } catch (FileNotFoundException e) {
            useLocalFileAndContinue();
        }
    }

    static void readDataFromRemoteFileLocatedAtLondon() throws FileNotFoundException {
        throw new FileNotFoundException("london-file.txt"); // file missing at runtime
    }

    static void useLocalFileAndContinue() {
        System.out.println("use local file and continue rest of the program normally");
    }
}
// prints use local file and continue rest of the program normally
```

Same idea, one more time: no morning-show ticket, then try the evening
show — an alternative way to continue, not a repair.

## 37:29 — Recap of the introduction

Three questions, three answers, and Sir calls the whole block done:

1. **What is an exception?** An unwanted, unexpected event that disturbs the
   normal flow of the program.
2. **What is the purpose of exception handling?** Graceful termination —
   don't miss anything, don't lose anything.
3. **What is the meaning of exception handling?** Not repairing the
   exception — defining an alternative way to continue the rest of the
   program normally.

## 38:25 — Runtime stack mechanism

New heading. **For every thread, the JVM creates one runtime stack.** To
show how that stack fills up, Sir writes a three-method program on the
board: `main` calls `doStuff`, which calls `doMoreStuff`, which prints
`"Hello"`.

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
// prints Hello
```

## 40:32 — Only one thread here, and its stack

This program has exactly **one thread — the main thread** — so the JVM
creates exactly one runtime stack for it. **Every method call performed by
that thread is stored in the corresponding stack:** first `main` (the main
thread's own first call), then `doStuff` (called from inside `main`), then
`doMoreStuff` (called from inside `doStuff`) — three entries, stacked in
call order.

> ⚠️ **Modern Java — "one runtime stack per thread" gets a second, cheaper
> shape from Java 21.** What Sir describes is exactly right for a **platform
> thread**: the JVM gives it a large, fixed-size call stack backed by the
> OS, which is why platform threads are expensive to create by the thousand.
> **Virtual threads** (Java 21, JEP 444) still use frames and stack
> semantics the same way, but their stack data lives on the heap and grows
> only as deep as the call chain actually goes — which is how a JVM can run
> **millions** of virtual threads where it could only run a few thousand
> platform threads. The mechanics Sir is about to teach (frames pushed on
> call, popped on return) hold for both; what changed is the cost of the
> stack itself, not the model.

## 42:01 — Each stack entry: stack frame or activation record

**Each entry in the stack is called a stack frame, or an activation
record** — both names are standard and Sir uses them interchangeably.

## 42:23 — The happy path: print, then pop each frame in order

Inside `doMoreStuff`, the `println` runs and `Hello` prints. Nothing else is
left to execute in `doMoreStuff`, so it **completes normally** (no
exception — normal termination) and its frame is **removed from the
stack**. Control returns to `doStuff`; nothing left there either, so its
frame is removed too. Control returns to `main`; same thing — its frame is
removed, and the stack is now empty.

```java
class Test {
    public static void main(String[] args) {
        doStuff();
        // after doStuff returns: pop doStuff, then pop main — stack empty
    }

    public static void doStuff() {
        doMoreStuff();
        // after doMoreStuff returns: pop doMoreStuff
    }

    public static void doMoreStuff() {
        System.out.println("Hello");
        // completed normally — this frame is removed
    }
}
// push order:  main → doStuff → doMoreStuff
// prints Hello
// pop order:   doMoreStuff → doStuff → main → stack empty
```

**Just before the main thread terminates, the JVM destroys that now-empty
stack.** That's the whole mechanism, for the case where everything goes
fine:

1. For every thread, the JVM creates one runtime stack.
2. Every method call by that thread is stored in that stack.
3. Each entry is a stack frame (activation record).
4. When a method completes, its entry is removed.
5. Once every call has completed, the stack is empty, and the JVM destroys
   it just before the thread terminates.

## 53:54 — Where the "happy path" stops

If everything goes fine, that's the flow above. **If something goes wrong,
what happens by default in Java?** That's the next heading — **default
exception handling in Java** — and Sir stops there. This video does not
cover `Throwable`, the JVM's default handler, or what happens to an uncaught
exception; that's Video 071.

---

## Exam and interview points

1. **Definition to memorize verbatim:** an exception is an unexpected,
   unwanted event that disturbs the normal flow of a program.
2. **Exception handling ≠ repairing the exception.** It means defining an
   alternative way to continue the rest of the program normally — the
   London-file-to-local-file and bus-to-train examples are the two to
   recall on the spot.
3. **The main objective of exception handling is graceful termination:** if
   something fails, release any held resources first, then stop — don't
   miss or lose data, and don't block resources other callers need.
4. **For every thread, the JVM creates exactly one runtime stack**; every
   method call by that thread is pushed onto it, and each entry is called a
   **stack frame** or **activation record** — both terms are fair game on
   an exam or in an interview.
5. **A completed method's frame is removed immediately**, and once a
   thread's stack is empty the JVM destroys it just before the thread
   terminates — this is the mechanism that later explains how the JVM finds
   a handler when something *does* go wrong.
6. **`SleepingException` and `TirePuncturedException` are classroom names,
   not Java API classes** — don't repeat them as if they exist outside this
   lecture. `FileNotFoundException` and `SQLException` are the real,
   checked exceptions used alongside them.
7. **Since Java 14, an uncaught `NullPointerException` names the exact null
   reference** in its message — worth knowing before you reach the ten
   exception case studies later in this series.
8. **`finalize()` has been deprecated since Java 9 and deprecated for
   removal since Java 18** — when this series reaches `final`/`finally`/
   `finalize`, treat `finalize()` as legacy trivia, not a pattern to use.

---

**Next:** Video 071 — Default exception handling
