# Video 072 — Checked vs unchecked exceptions

## Video info

**Title:** Core Java with OCJP/SCJP: Exception Handling Part-3A || Checked vs Unchecked Exceptions

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 72 of 203 |
| Series | Exception Handling · Part 3A |
| Topic | Checked vs Unchecked Exceptions |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 02m 44s |
| Video ID | piqjRl-Dngc |
| Watch | https://www.youtube.com/watch?v=piqjRl-Dngc |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

**Scope.** This is Exception Handling **Part 3A**. He does **not** teach the
syntax of `try`-`catch` or the full meaning of `throws` here (`throws` is "I
will discuss soon") — he only names both as the two fixes the compiler error
points at. He types **one** live program (`PrintWriter` → `abc.txt`), shows
the **unreported exception** compile error, then adds `throws
FileNotFoundException` plus `10 / 0` to prove `ArithmeticException` is
unchecked. The rest of the hour is definition, three running stories
(a 10th-class exam morning, a car trip, a family function), the exception
hierarchy revisited from a checked/unchecked angle, fully- vs.
partially-checked, and a closing oral drill. No `try`-`catch` solution is
written on this board — don't invent one.

### 00:05 — Next topic: checked vs unchecked (most valuable)

Next topic: **checked exception vs unchecked exception**. He calls it the most valuable concept. If you understand this, the remaining exception syllabus becomes easy.

### 00:22 — Why you must get the complete picture now

In the **next** sessions: `throw` / `throws`. Have you observed — **`throws` is purely meant for checked exceptions only**. If you do not know what a checked exception is, `throws` is nothing; you cannot understand it easily.

Next: **customized / user-defined exceptions** — that topic also purely talks about checked vs unchecked.

Make sure: **which are checked, which are unchecked, what is checked, what is unchecked.** Clear idea required.

> ❗ **Correction — "`throws` is purely meant for checked exceptions" overstates the rule.**
> The compiler only *requires* a `throws` clause (or a `try`-`catch`) for
> **checked** exceptions — that direction is exactly right, and is this whole
> lecture's point. But nothing stops a programmer from writing `throws` for
> an **unchecked** type too; it compiles, it is simply optional documentation
> the compiler never enforces:
> ```java
> class ThrowsUnchecked {
>     public static void main(String[] args) throws ArithmeticException {
>         System.out.println(10 / 0);   // throws clause here is optional, not required
>     }
> }
> // compiles (verified against javac 26)
> // runtime: Exception in thread "main" java.lang.ArithmeticException: / by zero
> ```
> So the safe rule is "checked ⇒ `throws` is compulsory," never the reverse
> ("named after `throws` ⇒ must be checked"). That reverse reading is exactly
> what trips people up later in this lecture (17:53) and in real interviews.

### 00:51 — Interview: two compulsory exception questions

He asks the room: what is the difference between checked exception and unchecked exception?

Most valuable, **repeatedly asked** in the **interview**. In the exception area, only **three** questions are compulsory in every interview, and these should be there.

Top-most important from exception handling, his priority:

1. **Priority one:** what is the difference between **checked exception and unchecked exception**
2. **Priority two:** what is the difference between **`final`, `finally`, `finalize`**

Compulsory you people should have clear clarity.

### 01:47 — The wrong answer everyone gives

He asks: what is checked exception? What is unchecked? What is the difference?

A student-style answer he puts on the table:

> *Checked exceptions are the exceptions which occur at ***compile time***. Unchecked exceptions are the exceptions which occur at ***runtime***.*

He repeats it: checked will occur at compile time, unchecked at runtime. **Correct or not?**

Majority of the people are going to fail this. Luckily, he says, you are not failing yet — he is about to stop you.

```java
class WrongInterviewLine {
    public static void main(String[] args) {
        // WRONG — majority fail in the interview with this line:
        // "Checked exceptions occur at compile time.
        //  Unchecked exceptions occur at runtime."
        System.out.println("this statement is 100% pakka wrong");
    }
}
// prints this statement is 100% pakka wrong
```

### 02:21 — 100% pakka wrong: every exception occurs at runtime

**100% pakka this statement is wrong.**

Whether it is a checked exception or an unchecked exception, **every exception should occur at runtime only**. There is **no chance** of occurring any exception at compile time.

**Compile-time errors are syntactical mistakes.** What we are getting there are **not exceptions**.

So: whether checked or unchecked, compulsory that exception should occur **at runtime only**. There is no chance of occurring any exception at compile time.

Then: *sir, can you tell what is the checked exception?* Take a bit special care to understand this concept.

```java
class EveryExceptionIsRuntime {
    public static void main(String[] args) {
        // NOTE he will write again at 42:39:
        // whether checked or unchecked, every exception occurs at runtime only
        // compile-time errors = syntactical mistakes, not exceptions
        System.out.println("exceptions occur at runtime only");
        System.out.println("compile-time errors are syntactical mistakes");
    }
}
// prints exceptions occur at runtime only
// prints compile-time errors are syntactical mistakes
```

### 02:57 — 10th class: first real public exams (setup)

I hope you people completed 10th class. Direct SCJP? No — 10th completed.

In your lifetime, **first time you wrote public exams is 10th class only**. Seventh class is a **namesake** public exam. Can you please show at least one student who failed in seventh class? Never. But he can show hundreds who failed in 10th. Real public exams are 10th; 7th is namesake.

### 04:03 — Golden days vs neighbors: job and marriage

10th class days are **golden days** — not much responsibility, just go to school, read. Now: number of responsibilities.

Festival day, travel to native place, the **neighbor** asks: when will you get the job? Course already completed. Some people did not go to native place for four days / five days because everyone is asking: one year back you completed B.Tech or M.Tech or MCA — when will you get the job? With family members not much problem; with neighbors much problem. Two questions: **when will you get the job**, **when will be your marriage**. Until getting the job, some decided they don’t want to go to native place. Some students spend **more than 3 years in Ameerpet** without going to native place just because of this.

Compared with these days, 10th class days are golden days: no one asks marriage or job.

### 05:40 — First exam day: panic, including parents

10th class exams: first time public exams, everyone is a bit panic, including parents. Most people feel 10th is a **life turning point** with respect to education.

That day is the **first exam** — maybe local language paper. Ready to go, but before starting, at the house any number of **formalities** by default.

### 06:03 — Formalities: hall ticket, pen, puja, coconut, seven hills

- **ID card / hall ticket and a pen**
- **Special puja** should be required
- **Coconut**
- Special **agreement with the god**: if I will get **500 marks**, then I will come to **seven hills** (Tirupati). God will tell: okay I will take care, please continue
- Mother or sister, sentimental kind of thing, by default on first exam day
- Brother or father may come **up to the exam hall** — at least for the first exam
Very important stage: 10th class public exams.

### 07:22 — Mother: have you took hall ticket? Cross check

You are ready to start. Immediately mother may ask: **have you took hall ticket or not? Can you please cross check?**

You check your pocket: yeah I took hall ticket. You showed.

### 08:11 — HallTicketMissingException — problem at runtime

If really you are **missing hall ticket**, when will be the problem? The problem at **runtime**. Examiner **won’t allow inside** the exam hall.

If the mother is going to check at the beginning, at runtime my execution of the program will be smooth.

**Hall ticket missing exception** is a very common exception. Mother: there may be a chance of hall-ticket-missing exception; can you please cross check whether you took hall ticket or not.

If we are checking at the beginning, at runtime execution becomes very smooth.

He says: single word, **don’t give space in the middle** — `HallTicketMissingException`.

```java
class HallTicketMissingExceptionDemo {
    public static void main(String[] args) {
        System.out.println("first 10th exam — ready to start");
        System.out.println("mother: have you took hall ticket? cross check");
        System.out.println("pocket check — yes I took hall ticket");
        // if really missing: problem at RUNTIME — examiner won't allow inside
        System.out.println("HallTicketMissingException is a very common exception");
    }
}
// prints first 10th exam — ready to start
// prints mother: have you took hall ticket? cross check
// prints pocket check — yes I took hall ticket
// prints HallTicketMissingException is a very common exception
```

Classroom name only for the story type — **not** in the Java API. The Java type he will compile next is `FileNotFoundException`.

### 08:40 — PenNotWorkingException — extra pens

You conveyed to mother: I took hall ticket, no problem. Second question: while writing exam there may be a chance of **pen not working**. **Pen not working exception** is a very common exception. Do you have extra pen or not? Can you please check?

Immediately you show **four pens**: yes I’m taking extra four pens, not required to worry.

If the mother will check all these things at the beginning, at runtime my execution of the program will be very smooth.

```java
class PenNotWorkingExceptionDemo {
    public static void main(String[] args) {
        System.out.println("mother: pen not working is very common");
        System.out.println("do you have extra pen? check");
        System.out.println("show four pens — not required to worry");
        System.out.println("PenNotWorkingException");
    }
}
// prints mother: pen not working is very common
// prints do you have extra pen? check
// prints show four pens — not required to worry
// prints PenNotWorkingException
```

### 09:07 — Compiler plays the mother role — what is a checked exception

The exceptions which are **checked by mother** for smooth execution of the program at runtime — these exceptions are by default considered **checked exceptions**.

**Who is going to play mother role here? Compiler.**

The exceptions which are **checked by compiler** for smooth execution of the program at runtime. These exceptions are by default considered as **checked exceptions**.

He repeats that sentence so the room can say it.

```java
class CompilerPlaysMother {
    public static void main(String[] args) {
        // BOARD meaning (he writes the long form at 18:52):
        // The exceptions which are checked by compiler
        // for smooth execution of the program at runtime
        // are called checked exceptions.
        System.out.println("compiler = mother");
        System.out.println("checked = checked by compiler for smooth runtime");
    }
}
// prints compiler = mother
// prints checked = checked by compiler for smooth runtime
```

### 09:55 — Board program: `PrintWriter` writes `hello` to `abc.txt`

Let me write a simple program so you can get away what is the checked exception.

`class Test`, `public static void main(String[] args)`.

Target: write **hello** to **`abc.txt`**.

`PrintWriter` is available inside **`java.io`** — `import java.io` also he is taking.

```java
import java.io.*;

class Test {
    public static void main(String[] args) {
        PrintWriter pw = new PrintWriter("abc.txt");
        pw.println("hello");
    }
}
// CE: unreported exception java.io.FileNotFoundException; must be caught or declared to be thrown
```

He also mentions an SOP statement and then says that SOP is **anyway not required** for this target — the target is only write hello to the file. The compile error below is about `PrintWriter`, not about a `println` on the console.

### 11:06 — Compiler: I can’t compile until you show how you handle it

He asks compiler: can you please compile this code?

Immediately compiler gives **left and right**: I can’t compile this code. What is the problem?

You are trying to write hello to `abc.txt`. At runtime there may be a chance `abc.txt` may not be available, and there may be a chance of **`FileNotFoundException`**.

It **doesn’t mean compulsory** that exception is going to occur. **There may be a chance.** If `FileNotFoundException` occurs, **how you are going to handle — let me know, then only I can compile.**

Compiler is telling very decently: boss there is a possibility; if you are not preparing mentally how to handle, at runtime you may face a big problem. First show how you are going to handle, then only I can compile.

### 12:11 — Exact compile-time error (read it)

Exact compile-time error. Observe:

**unreported exception `java.io.FileNotFoundException` must be caught or declared to be thrown.**

That is the compile-time error by default we are going to get.

Read it: unreported exception `java.io.FileNotFoundException` must be caught or declared to be thrown.

**It doesn’t mean `FileNotFoundException` occurs.** You **didn’t report** about `FileNotFoundException`. There is a possibility — you should **catch** or **declare to be thrown**. That is the compile-time error.

```java
import java.io.*;

class UnreportedExceptionMessage {
    public static void main(String[] args) {
        PrintWriter pw = new PrintWriter("abc.txt");
        pw.println("hello");
        // compiler is NOT saying FileNotFoundException occurs
        // compiler is saying: UNREPORTED — you didn't report about this possibility
    }
}
// CE: unreported exception java.io.FileNotFoundException; must be caught or declared to be thrown
```

> ⚠️ **Modern Java — the message text has been trimmed.** Verified on JDK 26
> (`javac` from OpenJDK 26): the same program today reads `unreported
> exception FileNotFoundException; must be caught or declared to be thrown`
> — the fully-qualified `java.io.` prefix Sir reads off his screen has since
> been dropped from this particular diagnostic, leaving just the simple
> class name. The requirement, the fix, and the underlying rule are all
> unchanged — only the wording got shorter.

### 13:21 — Same sentence in mother language

There may be a chance of hall-ticket-missing exception. If it is going to come, how you can handle — first let me know, then only I’m allow you to go for the exam.

There may be a chance of pen-not-working exception. If it occurs, how you can handle — let me show the solution, then I’m allow you — because these are **very common problems**.

There may be a chance of `FileNotFoundException`. If it occurs, how you can handle — let me know, then only I can compile. Compiler is going to tell that.

### 13:53 — Frequently occurred → compiler objects → checked

For **frequently occurred** exceptions, compiler will object whether you are handling or not. These type of exceptions are by default considered **checked exceptions**.

Definition again: the exceptions which are checked by compiler for smooth execution of the program at runtime are called checked exceptions.

### 14:16 — Live compile of `Test.java` (one-minute pause)

He takes one minute and types the same program again: `class Test`, `PrintWriter pw = new PrintWriter("abc.txt")`, `pw.println("hello")`, `import java.io`, save as **`test.java`**.

`javac Test.java` (he says “Java C tester on Java”). Compiler: DA, there may be a chance of `FileNotFoundException`. How you can handle first? Let me know. Then only I can compile.

Read this compile error (he reads it off the screen):

**unreported exception `java.io.FileNotFoundException` must be caught or declared to be thrown.**

```java
import java.io.*;

class Test {
    public static void main(String[] args) {
        PrintWriter pw = new PrintWriter("abc.txt");
        pw.println("hello");
    }
}
// CE: unreported exception java.io.FileNotFoundException; must be caught or declared to be thrown
```

Same point: **it doesn’t mean `FileNotFoundException` occurs.**

### 16:05 — If there is any chance of checked: try-catch or throws, or CE

What is checked exception? The exceptions which are checked by compiler for smooth execution of the program at runtime. These are by default considered checked exceptions.

In our program if there is any chance of rising checked exception, **compulsory programmer should handle** — either by **try-catch** or by **`throws` keyword** (I will discuss anyway).

- **must be caught** means: use **try-catch**
- **declared to be thrown** means: you have to use **`throws` keyword**
We should handle, otherwise the code won’t compile — compile-time error by default. It doesn’t mean `FileNotFoundException` occurs.

He does **not** write a `try-catch` on this board. He only names the two options from the error message.

```java
import java.io.*;

class MustBeCaughtOrDeclared {
    public static void main(String[] args) {
        PrintWriter pw = new PrintWriter("abc.txt");
        pw.println("hello");
        // must be caught  = try-catch   (he will discuss later)
        // declared thrown = throws      (he types throws at 23:35)
    }
}
// CE: unreported exception java.io.FileNotFoundException; must be caught or declared to be thrown
```

### 16:43 — Why people fail by seeing that CE line

Most of the people, by seeing this line — unreported exception `java.io.FileNotFoundException` must be caught or declared to be thrown — are going to fail:

> *Exceptions which occur at compile time are called checked. Exceptions which occur at runtime are called unchecked. *`ArithmeticException`* never comes at compile time that’s why it is unchecked. *`FileNotFoundException`* occurs at compile time that’s why it is checked.*

**No.** Here the compiler is **not** telling `FileNotFoundException` occurs. Compiler is telling: **there may be a chance** of `FileNotFoundException`. You **didn’t report** about this exception. Observe the **terminology**.

Can you tell what is checked exception? The exceptions which are **checked by compiler** for smooth execution of the program at runtime. These are by default considered as checked exceptions.

In our program if there is any chance of rising checked exception, compulsory we should handle — either by try-catch or by `throws` — otherwise the code won’t compile. Compile-time error we are getting.

```java
class CompilerDidNotSayItOccurs {
    public static void main(String[] args) {
        // CE line is NOT: FileNotFoundException occurs at compile time
        // CE line IS:     unreported exception ... must be caught or declared to be thrown
        System.out.println("unreported = you didn't report the possibility");
        System.out.println("there may be a chance — not: it occurs now");
    }
}
// prints unreported = you didn't report the possibility
// prints there may be a chance — not: it occurs now
```

### 17:53 — Examples of checked exceptions

Can you please give an example for checked exception?

In our scope whatever we discussed:

1. **HallTicketMissingException** — checked (very common)
1. **PenNotWorkingException** — checked (very common)
1. **`FileNotFoundException`** — checked
1. **`ServletException`**, **`RemoteException`**, **`SQLException`**
There are several. **Wherever `throws` followed by some exception** — all these predefined exceptions are **checked exceptions only**. `throws` followed by something is there — it is the checked exception only. (The useful direction of this rule is "checked ⇒ `throws` is compulsory" — see the correction at 00:22 for why the reverse isn't quite true.)

```java
class CheckedExamplesHeNamed {
    public static void main(String[] args) {
        System.out.println("HallTicketMissingException"); // classroom name, not in API
        System.out.println("PenNotWorkingException");     // classroom name, not in API
        System.out.println("FileNotFoundException");
        System.out.println("ServletException");
        System.out.println("RemoteException");
        System.out.println("SQLException");
        System.out.println("throws followed by X  =>  X is checked");
    }
}
// prints HallTicketMissingException
// prints PenNotWorkingException
// prints FileNotFoundException
// prints ServletException
// prints RemoteException
// prints SQLException
// prints throws followed by X  =>  X is checked
```

### 18:29 — Board heading: checked vs unchecked (five stars)

Keeping: **checked exceptions versus unchecked exceptions**. The most valuable concept — **at least five stars** you have to give.

Long copy pause. He dictates the checked definition many times, slowly.

### 18:52 — Board dictation: what is a checked exception

Keep writing.

**The exceptions which are checked by compiler for smooth execution of the program are called checked exceptions.**

Example (single word, don’t give space in the middle):

```java
HallTicketMissingException
```

```java
PenNotWorkingException
```

- `FileNotFoundException` etc.
```java
class CheckedExceptionBoard {
    public static void main(String[] args) {
        // BOARD:
        // The exceptions which are checked by compiler
        // for smooth execution of the program
        // are called checked exceptions.
        //
        // Example: HallTicketMissingException
        //          PenNotWorkingException
        //          FileNotFoundException etc.
        System.out.println("checked = checked by compiler for smooth execution");
    }
}
// prints checked = checked by compiler for smooth execution
```

### 20:40 — Board dictation: if chance of checked, handle or CE

In our program if there is a chance of occurring checked exception, compulsory we should handle either by try-catch or by `throws` keyword, otherwise the code won’t compile.

Compile-time, boss: it doesn’t mean `FileNotFoundException` occur. Boss there is a **possibility**, there is a **chance** — where you are handling first let me know, then only I can compile.

Keep writing:

**In our program, if there is a chance of rising checked exception, then compulsory we should handle that checked exception (either by try-catch or by `throws` keyword) otherwise we will get compile-time error.**

`throws` we will discuss in the future — not required to worry now.

What is checked exception? What is the meaning? Is it clear for all of you?

```java
class HandleCheckedOrCE {
    public static void main(String[] args) {
        // BOARD:
        // In our program if there is a chance of rising checked exception
        // then compulsory we should handle that checked exception
        // (either by try-catch or by throws keyword)
        // otherwise we will get compile time error.
        System.out.println("chance of checked => handle (try-catch or throws) or CE");
    }
}
// prints chance of checked => handle (try-catch or throws) or CE
```

### 22:35 — Unchecked: some exceptions compiler does not check

There are some exceptions which are **not checked by compiler**. Maybe **very rarely occurred** exceptions, or **until runtime I don’t know**.

Those exceptions are by default considered as **unchecked**. Compiler **not checked** these exceptions — pass — whether you are handling or not.

**The exceptions which are not checked by compiler whether the programmer handling or not. These exceptions are by default considered as unchecked exceptions.**

### 23:09 — Same `Test` + `10 / 0` + `throws FileNotFoundException`

Same program he is taking. Also `System.out.println(10 / 0)`.

He asks compiler: can you please compile this code?

Immediately compiler will give left and right **only** about: there may be a chance of rising `FileNotFoundException`. How you can handle?

What he did: he kept **`throws FileNotFoundException`**.

Will the code compile or not? **Yes.** Compiler **happily** the code is going to compile **even though there is a chance of raising `ArithmeticException`**. `10 / 0` — there may be a chance of raising `ArithmeticException`, but **compiler won’t object**. Happily compiler is going to compile, because compiler will check only `FileNotFoundException` but **not** `ArithmeticException`.

`ArithmeticException`: checked or unchecked? **Unchecked exception.**

```java
import java.io.*;

class Test {
    public static void main(String[] args) throws FileNotFoundException {
        PrintWriter pw = new PrintWriter("abc.txt");
        pw.println("hello");
        System.out.println(10 / 0);
    }
}
// compiles — compiler objects only about FileNotFoundException
// runtime: ArithmeticException
```

He says: I will explain what is the need of `throws` later — just showing the basic idea / purpose.

### 24:25 — Live: compiles; run gets `ArithmeticException`

He types `System.out.println(10 / 0)`. Compiler is always going to object about `FileNotFoundException` — unreported exception — so he takes `throws FileNotFoundException`.

Compile: **happily the code compiles fine.** There may be a chance of `ArithmeticException`, but why is compiler not objecting? Because compiler will check only file-not-found, **not** arithmetic. `ArithmeticException` is **unchecked**.

Let me run. Really at runtime we got **`ArithmeticException`**, but compiler **unable to identify** this exception. Even though we are getting at runtime arithmetic, compiler unable to identify. Such type of exceptions are by default considered **unchecked exceptions**.

```java
import java.io.*;

class Test {
    public static void main(String[] args) throws FileNotFoundException {
        PrintWriter pw = new PrintWriter("abc.txt");
        pw.println("hello");
        System.out.println(10 / 0);
    }
}
// compiles
// runtime: ArithmeticException
```

```java
class ArithmeticExceptionIsUnchecked {
    public static void main(String[] args) {
        System.out.println(10 / 0);
    }
}
// compiles — compiler does not ask how you handle ArithmeticException
// runtime: ArithmeticException
```

He did **not** type the second class on the board. The live file is still `Test` with `PrintWriter` + `throws FileNotFoundException` + `10 / 0`. The tiny class is the same 10/0 rule in isolation: unchecked means the compiler does not object.

There are some exceptions which are not checked by compiler whether programmer handling or not — these are unchecked.

### 25:46 — Unchecked examples; mother still checks hall ticket

Example for unchecked: **`ArithmeticException`**, **`NullPointerException`**, **`ClassCastException`**.

Best example: mother can ask — there may be a chance of hall-ticket-missing exception. Have you took hall ticket? Cross check. If you miss hall ticket, compulsory you should be aware how to get **duplicate hall ticket**. If hall-ticket-missing exception, you can handle — let me know — then I can compile.

If you don’t know how to handle: no problem, **20 rupees you can pay in the office**, then they will issue a **duplicate hall ticket**. You are not required to be panic. If you know that process, at runtime if really you miss the ticket — no problem — you are in a position to handle that situation.

Pen not working: already duplicate pen; with that I can able to run the show.

Mother can ask hall-ticket-missing, pen-not-working — maybe a chance.

```java
class DuplicateHallTicketFor20Rupees {
    public static void main(String[] args) {
        System.out.println("HallTicketMissingException — how will you handle?");
        System.out.println("20 rupees in the office — duplicate hall ticket");
        System.out.println("PenNotWorkingException — already extra pen");
    }
}
// prints HallTicketMissingException — how will you handle?
// prints 20 rupees in the office — duplicate hall ticket
// prints PenNotWorkingException — already extra pen
```

### 27:02 — Exam started: bomb blast — mother never asks

Exam started. You are writing the paper.

Meanwhile, just beside you, there’s a **big bomb blast** happening. Then how you can handle?

If the mother can ask this type of question to the exam student — **never**. Because: there may be a chance of **bomb blast exception** in the exam hall, maybe a chance, but how many times is it possible? Out of **one crore**, maybe **one time**. **Very rarely occurred.** Mother is not going to check; not required to check.

In India as of today, in the exam hall bomb blast **not reported**. Maybe in the future I don’t know. If we are keeping bomb in the classroom it may blast — bomb doesn’t aware whether it is the temple or the masjid or the classroom — wherever you are keeping, blast is going to happen. **Still the mother never going to ask.**

By mistake if the mother asked: if bomb-blast exception how you can handle? Then while writing, my mind is always nearby — is there any bomb or not — **definitely I will be the failed student** in that exam.

That’s why there are some exceptions which are **not checked by compiler**, because maybe **rarely occurred**, or maybe **until runtime we don’t know**. Such type of exceptions are by default considered **unchecked exceptions**.

He says: single word, don’t give space — `BombBlastException`.

```java
class BombBlastExceptionDemo {
    public static void main(String[] args) {
        System.out.println("exam started — writing the paper");
        // mother NEVER asks: if bomb blast how will you handle?
        // out of 1 crore maybe one time — as of today not reported in exam hall
        System.out.println("BombBlastException — rarely occurred — unchecked");
    }
}
// prints exam started — writing the paper
// prints BombBlastException — rarely occurred — unchecked
```

### 28:38 — Oral quiz on the stories

- **BombBlastException** — checked or unchecked? **Unchecked**
- **HallTicketMissingException** — **Checked**
- **PenNotWorkingException** — **Checked**
- **`ArithmeticException`** — **Unchecked**
Clear for all of you at this point.

```java
class StoryQuiz {
    public static void main(String[] args) {
        System.out.println("BombBlastException — unchecked");
        System.out.println("HallTicketMissingException — checked");
        System.out.println("PenNotWorkingException — checked");
        System.out.println("ArithmeticException — unchecked");
    }
}
// prints BombBlastException — unchecked
// prints HallTicketMissingException — checked
// prints PenNotWorkingException — checked
// prints ArithmeticException — unchecked
```

### 29:07 — Board dictation: what is an unchecked exception

Keep writing. He repeats each fragment many times for copy.

**The exceptions which are not checked by compiler whether programmer handling or not, such type of exceptions are called unchecked exceptions.**

Example:

```java
ArithmeticException
```

- `BombBlastException` etc.
(Single word, don’t give space in the middle.)

Terminology is very very clear. What is checked, what is unchecked. Still he adds one or two examples so you get much much clarity.

```java
class UncheckedExceptionBoard {
    public static void main(String[] args) {
        // BOARD:
        // The exceptions which are not checked by compiler
        // whether programmer handling or not,
        // such type of exceptions are called unchecked exceptions.
        //
        // Example: ArithmeticException
        //          BombBlastException etc.
        System.out.println("unchecked = compiler does not check handling");
    }
}
// prints unchecked = compiler does not check handling
```

### 30:59 — Vijayawada 4 a.m. by car: father checks diesel

Assume you required to travel to **Vijayawada**. Early morning at **4:00** you have to start by car. You are **alone** traveling. Ready to start. Father also came down from the house, just to give the send-off. Early morning 4:00 father also woke up, came near to the car.

Immediately father may ask a number of questions.

**Can you please cross check whether diesel is there or not?** If diesel not there, don’t depend on highway. Better to within the city only, better to **full tank**. Otherwise you may face a problem at highway — maybe a chance if the petrol bunks got closed, then you will be in the trouble.

If diesel not there, the problem is at **runtime**. If father is going to check at the beginning, at runtime my execution of the program will become very smooth.

**Diesel completed exception / diesel not available exception** is a **checked exception**, because it is a **very common problem**.

```java
class DieselNotAvailableExceptionDemo {
    public static void main(String[] args) {
        System.out.println("4:00 start alone by car to Vijayawada");
        System.out.println("father: cross check diesel — full tank in the city");
        System.out.println("don't depend on highway if bunks closed");
        System.out.println("DieselNotAvailableException — very common — checked");
    }
}
// prints 4:00 start alone by car to Vijayawada
// prints father: cross check diesel — full tank in the city
// prints don't depend on highway if bunks closed
// prints DieselNotAvailableException — very common — checked
```

### 32:33 — Stepney / spare tyre (checked)

Second: **have you took stepney (spare tyre) or not?** Can you please cross check? While traveling, tyre got **punctured** — then it’s very horrible. If it is the bike, no problem; if it is the car, viable? If the stepney is not there, then what we have to do? Leave the car there, travel to near city, go and come back — until that whether the car is secured or not — a number of problems.

That’s why: can you please cross check whether stepney is there or not? Yes it is there, not required to worry.

If I’m not checking at the beginning, problem is at runtime.

```java
class StepneyNotAvailableExceptionDemo {
    public static void main(String[] args) {
        System.out.println("father: have you took stepney or not? cross check");
        System.out.println("car tyre punctured without spare — leave the car — horrible");
        System.out.println("StepneyNotAvailableException — common — checked");
    }
}
// prints father: have you took stepney or not? cross check
// prints car tyre punctured without spare — leave the car — horrible
// prints StepneyNotAvailableException — common — checked
```

### 33:20 — Mineral water from the house (still father checking)

Don’t take water anywhere outside. Better to take **mineral water bottle** only, or please bring the bottle from the house only.

If the father is going to check, at runtime I won’t face any problem.

These kind of things the father can check — by default considered **checked exceptions**.

**It doesn’t mean tyre-punctured exception occurs.** It not occurs — **maybe a chance**. Can you please prepare mentally with the stepney. Diesel-complete exception not happen — maybe a chance — prepare mentally how to handle.

At the beginning if the father is going to check, at runtime my execution of the program will be very smooth. Such type of exceptions are checked exceptions.

```java
class MineralWaterFromHouse {
    public static void main(String[] args) {
        System.out.println("father: don't take water outside — bottle from the house");
        System.out.println("father checks at beginning => runtime is smooth");
        System.out.println("does not mean the exception occurs — maybe a chance");
    }
}
// prints father: don't take water outside — bottle from the house
// prints father checks at beginning => runtime is smooth
// prints does not mean the exception occurs — maybe a chance
```

### 34:15 — AccidentException — father must not ask (unchecked)

Suppose father may ask: while traveling, suddenly some **accident** happened, you gone, then how you can…?

Father is going to ask that **early morning 4:00 just before starting**? If father can ask, even we can’t see the father — we will give **left and right** — because the father **can’t ask** this one.

But there may be a chance: every day several people are dying in accidents, maybe a chance. **But the father should not ask**, because **very rarely occurred** exceptions.

**Accident exception** — checked or unchecked? **Unchecked.**

If it is a checked exception, why these many accidents are happening? It is **not checked**. We can’t expect that; accidentally it is happening. This type of thing is unchecked exception.

You have to get complete picture in your mind; then the remaining things will become easy.

```java
class AccidentExceptionDemo {
    public static void main(String[] args) {
        System.out.println("4:00 send-off — father must NOT ask accident-how-to-handle");
        System.out.println("people die in accidents every day — maybe a chance");
        System.out.println("AccidentException — rarely / unexpected — unchecked");
    }
}
// prints 4:00 send-off — father must NOT ask accident-how-to-handle
// prints people die in accidents every day — maybe a chance
// prints AccidentException — rarely / unexpected — unchecked
```

### 35:16 — House function: father to Delhi, you lead, grandfather monitors

One more last example, then he finishes this terminology.

Assume in your house there is a **big function** scheduled in another **one week**. Father is responsible to arrange all the activities. Suddenly father got some urgent work. He required to travel somewhere. He will come back **only on function day**.

Father called you: I require to travel to **Delhi**. You are responsible. Take the responsibility for all these function activities. This is money — if you want, contact **accountant**, accountant will provide how much you required, no problem. Take each and everything very much care — almost I invited several guests, maybe a chance of problem.

First time in your life he gave the opportunity for leading this activity. You felt very happy: dad not required to worry, happily you can go, I will take care each and everything. You gave the word. Father felt very happy.

What father did: he called **his** father — your **grandfather**. Dad, I give complete responsibility for my kid. He is not having experience whether he’s doing activities properly or not. **Can you please monitor.** If he’s not doing any activity properly, **please guide**. Still if he’s not listening, then **make a phone call to me**, I will give left and right to this kid.

For monitoring purpose, father arranged his father at the **corner**. In our functions also, **white-haired people** are always sitting in the corner and observing the things, because they have experience.

Grandfather observing: you got first time in your life leadership activity, almost you are **flying in the air** — do that, do this. Grandfather felt very happy: yes this kid is doing good.

**Grandfather = compiler** (monitor in the corner). You = programmer. Father = the one who assigned the work.

```java
class GrandfatherMonitorsTheFunction {
    public static void main(String[] args) {
        System.out.println("father to Delhi — kid leads the function");
        System.out.println("grandfather sits in the corner and monitors");
        System.out.println("if not proper: guide; still not listening: phone the father");
        System.out.println("grandfather = compiler");
    }
}
// prints father to Delhi — kid leads the function
// prints grandfather sits in the corner and monitors
// prints if not proper: guide; still not listening: phone the father
// prints grandfather = compiler
```

### 38:01 — Exactly 452 invitation cards

After some time grandfather: Durga can you please come? Have you preparing the dinner all the things properly? Oh perfect. Now I have one doubt: **for how many members** you are preparing the dinner?

Immediately: **exactly 452 members**, grandpa.

Grandfather gave left and right: exactly 452 members — **how you got that number?**

Because I distributed exactly **452 invitation cards**. That’s why I’m expecting 452 members.

### 39:19 — InsufficientDinnerException (checked) — prepare for 500

Grandpa: suppose you give invitation card to your friend; while coming your friend bring his **parents** also. Then are you going to stop — this invitation only for you but not for your parents? I can’t.

Then there may be a chance of count **more than 452**. Then **insufficient dinner exception** occurs. There is a possibility. In the functions it is a **very common problem**. If a minimum **100 functions** are happening, **70 functions** this type of problem is there.

How you can handle? Let me know. Grandfather reasonably correct.

Solution: 452 members right? **Prepare for 500 members.** If 500, okay; if more than that, max 500, then no problem.

Immediately instructed catering: not 452, **500 members**, can you please prepare dinner.

```java
class InsufficientDinnerExceptionDemo {
    public static void main(String[] args) {
        int cardsIssued = 452;
        int preparedFor = 500; // grandfather: common problem — prepare extra
        System.out.println("cards issued " + cardsIssued);
        System.out.println("InsufficientDinnerException is very common — checked");
        System.out.println("handle: prepare for " + preparedFor + " members");
    }
}
// prints cards issued 452
// prints InsufficientDinnerException is very common — checked
// prints handle: prepare for 500 members
```

### 40:21 — Function day: 487 came — program can handle

Runtime: function started. That day **487 members came**. Can you tell: is my program in a position to handle or not? **Yes.**

That’s what: if compiler is going to check at the beginning, happily my program will be smooth.

**Insufficient dinner exception** — checked or unchecked? **Checked exception.**

```java
class FunctionDay487 {
    public static void main(String[] args) {
        int preparedFor = 500;
        int came = 487;
        if (came <= preparedFor) {
            System.out.println("487 came, prepared 500 — program can handle");
        }
    }
}
// prints 487 came, prepared 500 — program can handle
```

### 40:50 — Short-circuit / fire-accident (unchecked)

After some time grandpa called: can you please come? You went for **colorful lighting** all these things. There may be a chance of **short circuit exception** occurs, all the people who came for the function **got died**. How you can handle?

Is the grandfather can ask this type of thing? By mistake if grandpa asked this, I will give **left and right** to grandpa and intimate to father: grandfather is asking this one, what I have to do.

**Fire accident exception** maybe a chance in the functions, maybe a chance — but how many times? Out of **one crore**, **one or two times**. Such type of **rarely occurred** exceptions we are **not required to check**. These kind of exceptions are by default **unchecked exceptions**.

Complete examples covered. In your mind: what is checked, what is unchecked — clear. Advantage of compiler checking some exception — you also know (runtime becomes smooth).

```java
class ShortCircuitExceptionDemo {
    public static void main(String[] args) {
        System.out.println("colorful lighting — grandpa must NOT ask short-circuit deaths");
        System.out.println("FireAccidentException / ShortCircuitException");
        System.out.println("out of 1 crore one or two times — unchecked");
    }
}
// prints colorful lighting — grandpa must NOT ask short-circuit deaths
// prints FireAccidentException / ShortCircuitException
// prints out of 1 crore one or two times — unchecked
```

### 41:54 — Spoken summary (both definitions)

**Checked exception:** the exceptions which are checked by compiler for smooth execution of the program at runtime are called checked exception.

Example: `FileNotFoundException`, HallTicketMissingException, PenNotWorkingException.

**Unchecked exception:** the exceptions which are not checked by compiler whether programmer handling or not. These are by default considered unchecked exception.

`BombBlastException`, `ArithmeticException`, `NullPointerException`. These are unchecked exceptions.

Clear for all of you?

```java
class SpokenSummary {
    public static void main(String[] args) {
        System.out.println("checked: FileNotFoundException, HallTicketMissingException, PenNotWorkingException");
        System.out.println("unchecked: BombBlastException, ArithmeticException, NullPointerException");
    }
}
// prints checked: FileNotFoundException, HallTicketMissingException, PenNotWorkingException
// prints unchecked: BombBlastException, ArithmeticException, NullPointerException
```

### 42:39 — Note 1: whether checked or unchecked, occurs at runtime only

First point: whether the exception is checked or unchecked, **compulsory this exception should occur at runtime only**. There is **no chance** of occurring any exception at compile time. Compile time = **syntactical mistakes**.

Keep writing. **Note.** He repeats every fragment.

**Whether it is checked or unchecked, every exception occurs at runtime only. There is no chance of occurring any exception at compile time.**

Point number one is clear.

```java
class Note1EveryExceptionAtRuntime {
    public static void main(String[] args) {
        // BOARD NOTE 1:
        // Whether it is checked or unchecked,
        // every exception occurs at runtime only.
        // There is no chance of occurring any exception at compile time.
        System.out.println("checked or unchecked => runtime only");
        System.out.println("no exception occurs at compile time");
    }
}
// prints checked or unchecked => runtime only
// prints no exception occurs at compile time
```

### 44:09 — Last class hierarchy back on the board

Second one — listen. In the last session somewhere I took **exception hierarchy**. We remember.

Which class acts as the **root**? **`Throwable`.**

`Throwable` contains **`Exception`** and second class **`Error`**.

Under `Exception` several child classes. **`RuntimeException`**. For `RuntimeException`: `ArithmeticException`, `NullPointerException`, `ClassCastException`, `IndexOutOfBoundsException` … several.

Here **`IOException`** is there. Same diagram only. `IOException` child classes: **`EOFException`**, **`FileNotFoundException`**, **`InterruptedIOException`**.

Next: **`InterruptedException`** — child of `Exception` only. **`ServletException`**, **`RemoteException`**, dot dot dot. Several. We covered this diagram somewhere in the last class.

For `Error` also several: **`VirtualMachineError`**, **`StackOverflowError`**, **`OutOfMemoryError`**. Next: **`ExceptionInInitializerError`**, **`AssertionError`**, dot dot dot.

Now among all, **which are checked and which are unchecked** — compulsory you should just observe. Think a bit logically. Don’t remember the conclusion blindly.

```java
class ExceptionHierarchyBoard {
    public static void main(String[] args) {
        // BOARD (same diagram as last class):
        // Throwable
        //   Exception
        //     RuntimeException
        //       ArithmeticException
        //       NullPointerException
        //       ClassCastException
        //       IndexOutOfBoundsException
        //     IOException
        //       EOFException
        //       FileNotFoundException
        //       InterruptedIOException
        //     InterruptedException
        //     ServletException
        //     RemoteException
        //   Error
        //     VirtualMachineError
        //       StackOverflowError
        //       OutOfMemoryError
        //     ExceptionInInitializerError
        //     AssertionError
        System.out.println("root = Throwable; children = Exception and Error");
    }
}
// prints root = Throwable; children = Exception and Error
```

### 45:57 — Errors: not our program; lack of system resources; non-recoverable

Have you observed `Error`. In the last class: most of the times **errors are not caused by our program**. These are due to **lack of system resources**. Errors are **non-recoverable**.

If **`OutOfMemoryError`** occurs, being a programmer we **can’t do anything**. The program is going to be **shut down**. The program will be **terminated abnormally**. Being a programmer we can’t do anything.

```java
class OutOfMemoryErrorIsNotOurJob {
    public static void main(String[] args) {
        // if OutOfMemoryError occurs: programmer can't do anything
        // program shut down / terminated abnormally
        // due to lack of system resources — non-recoverable
        System.out.println("Error = lack of system resources, non-recoverable");
    }
}
// prints Error = lack of system resources, non-recoverable
```

### 46:36 — Compiler must not ask how you handle `OutOfMemoryError`

If the compiler can ask: was there may be a chance of `OutOfMemoryError`, how you can handle, can you please let me know? If the compiler will ask like this, **I will give left and right.**

**Handling error is my responsibility? No.** I’m not responsible for that. These are due to lack of system resources. Being a programmer, what I can do? It’s not my job. It’s not my responsibility.

That’s why these are checked or unchecked? **Unchecked.** Compiler **should not ask** how you can handle the error.

```java
class CompilerMustNotAskAboutError {
    public static void main(String[] args) {
        // compiler must NOT ask: OutOfMemoryError — how will you handle?
        System.out.println("handling Error is not the programmer's job");
        System.out.println("Error and child classes are unchecked");
    }
}
// prints handling Error is not the programmer's job
// prints Error and child classes are unchecked
```

### 47:10 — Invigilator not came — not the student’s job

Mother can ask hall-ticket-missing, pen-not-working — these mother can ask.

**Invigilator not came exception** — how you can handle? Mother **cannot** ask this type of thing, because if invigilator not came, is it **my** responsibility to handle that? **No.** My **management** is going to take care. Why I have to worry about that.

If `Error` occurs, **programmer not responsible**. My **system admin or server admin** is the responsible. That’s why in the case of errors, how you can handle — **compiler never going to ask the programmer**. That’s why these are **unchecked**. **All errors are unchecked.**

```java
class InvigilatorNotCameExceptionDemo {
    public static void main(String[] args) {
        System.out.println("InvigilatorNotCameException — not the student's job");
        System.out.println("management / admin will take care");
        System.out.println("Error => system admin / server admin, not programmer");
    }
}
// prints InvigilatorNotCameException — not the student's job
// prints management / admin will take care
// prints Error => system admin / server admin, not programmer
```

### 47:51 — Note 2: `RuntimeException` + `Error` (+ children) are unchecked; remaining checked

Next: `RuntimeException` and its child classes.

Keep writing. **Second note.**

**`RuntimeException` and its child classes, `Error` and its child classes, are unchecked. Except these, remaining are checked.**

Which are unchecked, which are checked — you people should have clarity. Meaning of unchecked, meaning of checked — clear.

```java
class Note2UncheckedRule {
    public static void main(String[] args) {
        // BOARD NOTE 2:
        // RuntimeException and its child classes,
        // Error and its child classes,
        // are unchecked.
        // Except these, remaining are checked.
        System.out.println("unchecked: RuntimeException + children, Error + children");
        System.out.println("remaining are checked");
    }
}
// prints unchecked: RuntimeException + children, Error + children
// prints remaining are checked
```

So from the diagram:

- Unchecked: `RuntimeException`, `ArithmeticException`, `NullPointerException`, `ClassCastException`, `IndexOutOfBoundsException`, `Error`, `VirtualMachineError`, `StackOverflowError`, `OutOfMemoryError`, `ExceptionInInitializerError`, `AssertionError`
- Checked (the remaining): `Throwable`, `Exception`, `IOException`, `EOFException`, `FileNotFoundException`, `InterruptedIOException`, `InterruptedException`, `ServletException`, `RemoteException`, …
### 49:13 — Fully checked vs partially checked (inside checked only)

There is another point. **Fully checked versus partially checked.** In the **checked only** there is another division: fully checked and partially checked.

Keep writing the heading: **fully checked versus partially checked**.

Checked and unchecked only we are facing the problem — but what is the second category? Fully checked and partially checked. Simple. What is full checking, what is partial checking? Just observe.

### 50:05 — Shopping mall vs Shamshabad airport

Assume you went to the **shopping mall** with your kid. Do you have the kids? Soon. Assume you went to the shopping with your kid.

These days **security checking** is very common. Security people checked **you** with the scanner. You required to walk through **metal detector**. But for your **kid**, security people **won’t check** — kid wearing the bombs and so on, very rare. They never going to check the kids; only parents are going to be checked.

This type of checking is **partial checking** or full checking? **Partial checking.**

Next: if you go for **Shamshabad airport**, international airport. He went with his kid, required to travel to **America**. Compulsory in the airport checking should be happened. In the airport checking, whether **parent or kid**, compulsory **each and every person should be checked**.

Such type of checking is by default **full check**. Parent should be checked **and** the kid also should be checked = **full checking**.

Parent should be checked but kid not required to check = **partial checking**.

```java
class PartialVsFullCheckingStory {
    public static void main(String[] args) {
        System.out.println("shopping mall: parent scanned, kid not checked = partial");
        System.out.println("Shamshabad airport: parent and kid both checked = full");
    }
}
// prints shopping mall: parent scanned, kid not checked = partial
// prints Shamshabad airport: parent and kid both checked = full
```

### 51:49 — `IOException` fully checked; `Exception` partially checked

Observe a bit carefully. **`IOException`** is there. Is it checked or not? **Checked** — because `RuntimeException` and `Error` these categories are unchecked; except that all the remaining are checked. So checked.

All the childs checked or not? All the childs checked.

**A checked exception is said to be fully checked if and only if all its child classes are also checked.**

`IOException` is checked, all its children also checked. That’s why this one is **fully checked exception**.

Here **`Exception`** is there. It is checked (it’s not under runtime). But **some child classes are checked, some child classes are unchecked**. Some childs checked, some childs unchecked. This type of checking is **partial checking**.

Full check / partial check — I hope you people can identify the difference already.

```java
class IoExceptionFullyExceptionPartially {
    public static void main(String[] args) {
        // IOException: checked, and EOFException / FileNotFoundException /
        // InterruptedIOException are also checked  => fully checked
        // Exception: checked, but RuntimeException child is unchecked
        //            and IOException child is checked  => partially checked
        System.out.println("IOException — fully checked");
        System.out.println("Exception — partially checked");
    }
}
// prints IOException — fully checked
// prints Exception — partially checked
```

### 52:58 — Board dictation: fully checked

Keep writing.

**A checked exception is said to be fully checked if and only if all its child classes are also checked.**

Example: **`IOException`**. Next: **`InterruptedException`**. Sir, only parent is there, **no child** — it’s **always fully checked only**. `InterruptedException` is fully checked.

```java
class FullyCheckedBoard {
    public static void main(String[] args) {
        // BOARD:
        // A checked exception is said to be fully checked
        // if and only if all its child classes are also checked.
        //
        // Example: IOException
        //          InterruptedException  (no child => always fully checked)
        System.out.println("fully checked: IOException, InterruptedException");
    }
}
// prints fully checked: IOException, InterruptedException
```

### 54:12 — Board dictation: partially checked

Second.

**A checked exception is said to be partially checked if and only if some of its child classes are unchecked.**

Example: **`Exception`** — some of its child classes are unchecked.

Second example: **`Throwable`**. Some child classes are unchecked, some child classes are checked. **`Throwable`.**

That’s all. Take a note.

```java
class PartiallyCheckedBoard {
    public static void main(String[] args) {
        // BOARD:
        // A checked exception is said to be partially checked
        // if and only if some of its child classes are unchecked.
        //
        // Example: Exception
        //          Throwable
        System.out.println("partially checked: Exception, Throwable");
    }
}
// prints partially checked: Exception, Throwable
```

### 55:22 — Quiz: any three partially checked? Trap on the board

Note. Can you tell **any three** partially checked exceptions?

Just now two I spelled out. One is `Exception`. The other one is `Throwable`. **Third one.** Can you tell? Already there on the board. I can able to see. Already there on the board.

Third partially checked exception other than `Exception` and `Throwable`?

He walks the board so they don’t pick the wrong boxes:

- **`IOException`** is **fully checked** — it is checked; if any child is there, checked only, because this area is checked area only
- **`InterruptedException`** we listed already — checked, **fully checked**
- **`Error`** is **unchecked** — fully checked and partially checked **applicable only for checked, not for unchecked exceptions**
Long pause (~56:37–56:49) while the room hunts for a third name.

Which are checked, which are partially checked, which are fully checked. Any **three** partially checked exceptions?

`RuntimeException` is **unchecked**. `RuntimeException` and child classes are unchecked. Next `Error` and its child classes are unchecked.

Don’t break your heads.

```java
class NoThirdOnTheBoard {
    public static void main(String[] args) {
        // students hunt the hierarchy for a third partially checked name
        // IOException — fully checked (not the answer)
        // InterruptedException — fully checked (not the answer)
        // Error — unchecked — fully/partially does not apply
        // RuntimeException — unchecked
        System.out.println("fully/partially applies only to checked exceptions");
    }
}
// prints fully/partially applies only to checked exceptions
```

### 57:16 — Note: the only possible partially checked exceptions in Java are two

Use the word **note**.

**The only possible partially checked exceptions in Java are: first one `Exception`, second one `Throwable`.**

That’s all. Third one is **not there**. `Exception`, second one `Throwable` — that’s all. Because all the remaining are either **fully checked** or **unchecked**. Partially checked exceptions in Java: only **two** things are there. One is `Throwable`. Second one is `Exception`.

This holds because `RuntimeException` is the *only* place where "checked"
turns into "unchecked" anywhere under `Exception`, and `Error` is unchecked
in its entirety — so `Exception` and `Throwable` are structurally the only
two classes that can straddle both sides. No JDK release since has added a
standard-library checked class with both checked and unchecked children
anywhere else in the tree, so the count is still exactly two today.

Make sure you people should be aware: checked, unchecked, partially checked, fully checked. Now you have clarity.

```java
class OnlyTwoPartiallyChecked {
    public static void main(String[] args) {
        // BOARD NOTE:
        // The only possible partially checked exceptions in Java are
        // Exception and Throwable.
        System.out.println("partially checked in Java: Exception, Throwable");
        System.out.println("no third — remaining are fully checked or unchecked");
    }
}
// prints partially checked in Java: Exception, Throwable
// prints no third — remaining are fully checked or unchecked
```

### 58:13 — Exercise: describe the behavior of the following exceptions

Now I will give some list of exceptions. You have to describe the behavior: whether it is checked or unchecked, fully checked or partially checked.

Better to take a bit style. Keep writing:

**Describe the behavior of following exceptions.**

Take this list first and then we will decide. “Take this.” Long copy silence (~58:59–59:52) while the list goes on the board.

### 59:52 — The list (then answers)

Completed right. So that we will discuss: which are checked, which are unchecked, which are partially checked, which are fully checked.

The list he spells:

```java
IOException
```

```java
RuntimeException
```

```java
InterruptedException
```

```java
Error
```

```java
Throwable
```

```java
ArithmeticException
```

```java
NullPointerException
```

…and then as he answers he also does **`Exception`** and **`FileNotFoundException`**.

### 1:00:22 — Answers, one by one (spell out in that style)

Better to spell out in that style.

| Exception | What he wants you to say |
|---|---|
| IOException | Checked (fully checked) |
| RuntimeException | Unchecked |
| InterruptedException | Checked (fully checked) |
| Error | Unchecked |
| Throwable | Checked (partially checked) |
| ArithmeticException | Unchecked |
| NullPointerException | Unchecked |
| Exception | Checked (partially checked) |
| FileNotFoundException | Checked (fully checked) |

`IOException`: checked or unchecked first? Checked. Within bracket, fully or partially? **Fully checked.** Spell out: **checked, fully checked**.

`RuntimeException`: checked or unchecked? **Unchecked.**

`InterruptedException`: checked, but fully or partially? **Fully checked.** Checked, fully checked.

`Error`: checked or unchecked? **Unchecked.**

`Throwable`: **checked**, within bracket **partially checked**.

`ArithmeticException`: **unchecked**.

`NullPointerException`: **unchecked**. Same.

`Exception`: **checked**, within bracket **partially checked**.

`FileNotFoundException`: **checked**, within bracket **fully checked**.

That’s all. Are you able to understand?

```java
class DescribeTheBehavior {
    public static void main(String[] args) {
        System.out.println("IOException — checked (fully checked)");
        System.out.println("RuntimeException — unchecked");
        System.out.println("InterruptedException — checked (fully checked)");
        System.out.println("Error — unchecked");
        System.out.println("Throwable — checked (partially checked)");
        System.out.println("ArithmeticException — unchecked");
        System.out.println("NullPointerException — unchecked");
        System.out.println("Exception — checked (partially checked)");
        System.out.println("FileNotFoundException — checked (fully checked)");
    }
}
// prints IOException — checked (fully checked)
// prints RuntimeException — unchecked
// prints InterruptedException — checked (fully checked)
// prints Error — unchecked
// prints Throwable — checked (partially checked)
// prints ArithmeticException — unchecked
// prints NullPointerException — unchecked
// prints Exception — checked (partially checked)
// prints FileNotFoundException — checked (fully checked)
```

### 1:02:16 — Close: terminology clear; next things get easy

This is what you people should require. What is the difference between **checked, unchecked, partially checked, fully checked**. Now the terminology is clear. If you are able to understand now, the **next things will become very easy** for you. That’s what you have to remember.

Video ends **1:02:44**. He does not start `throw` / `throws` syntax in this Part-3A.

---

## Board recap

**Interview (priority one from exception handling):** difference between checked and unchecked. (Priority two, named only: `final` vs `finally` vs `finalize`.)

**Wrong line:** “checked occur at compile time, unchecked at runtime.” **100% pakka wrong.**

**Note 1:** whether checked or unchecked, **every exception occurs at runtime only**. No exception at compile time. Compile-time errors are syntactical mistakes.

**Checked:** exceptions **checked by compiler** for smooth execution of the program at runtime. If there is a chance of a checked exception, compulsory handle (**try-catch** or **`throws`**), otherwise **compile-time error**. The CE **unreported exception … must be caught or declared to be thrown** does **not** mean the exception occurs.

This video’s live checked demo:

```java
import java.io.*;

class Test {
    public static void main(String[] args) {
        PrintWriter pw = new PrintWriter("abc.txt");
        pw.println("hello");
    }
}
// CE: unreported exception java.io.FileNotFoundException; must be caught or declared to be thrown
```

**Unchecked:** exceptions **not checked by compiler** whether programmer handling or not (rarely occurred, or unknown until runtime). `ArithmeticException`, `NullPointerException`, `ClassCastException`, `BombBlastException` (classroom name).

Live proof compiler ignores unchecked:

```java
import java.io.*;

class Test {
    public static void main(String[] args) throws FileNotFoundException {
        PrintWriter pw = new PrintWriter("abc.txt");
        pw.println("hello");
        System.out.println(10 / 0);
    }
}
// compiles
// runtime: ArithmeticException
```

**Note 2:** `RuntimeException` and its child classes, `Error` and its child classes, are **unchecked**. Except these, remaining are **checked**. All **errors** are unchecked (not caused by our program; lack of system resources; non-recoverable; system/server admin, not programmer).

**Fully checked** (checked only): a checked exception is fully checked iff **all its child classes are also checked**. Examples: `IOException`, `InterruptedException` (no child ⇒ always fully checked). Leaf checked types like `FileNotFoundException` he also spells **checked (fully checked)**.

**Partially checked:** a checked exception is partially checked iff **some of its child classes are unchecked**. **The only possible partially checked exceptions in Java are `Exception` and `Throwable`.** No third.

**Stories → Java names he wrote (single word, no spaces):** `HallTicketMissingException`, `PenNotWorkingException`, `BombBlastException` — classroom names, not API. Real API types he compiled or listed: `FileNotFoundException`, `SQLException`, `ServletException`, `RemoteException`, `IOException`, `EOFException`, `InterruptedIOException`, `InterruptedException`, `ArithmeticException`, `NullPointerException`, `ClassCastException`, `IndexOutOfBoundsException`, `Error`, `OutOfMemoryError`, `StackOverflowError`, `ExceptionInInitializerError`, `AssertionError`, `Throwable`, `Exception`, `RuntimeException`.

---

## Exam and interview points

1. **The universal interview trap:** "checked occurs at compile time,
   unchecked at runtime" is **100% wrong**. Every exception — checked or
   unchecked — occurs at runtime only; compile-time problems are syntactical
   or semantic mistakes, not exceptions at all.
2. **Checked = checked by the compiler, for smooth runtime execution.** If
   there's any chance of a checked exception, the programmer must handle it
   (`try`-`catch`) or declare it (`throws`), or the code fails to compile.
3. **`unreported exception ... must be caught or declared to be thrown`
   means "there is a possibility," never "this exception occurred."**
   Misreading that line as "the exception happened at compile time" is
   exactly what sinks most candidates on this question.
4. **Unchecked = not checked by the compiler at all** — whether the
   programmer handles it or not — because it's rare, or because the
   compiler cannot know about it until runtime.
5. **The one rule that classifies the entire hierarchy:** `RuntimeException`
   and its child classes, plus `Error` and its child classes, are unchecked;
   everything else under `Throwable` is checked. Learn the rule, not a list
   of class names — it generalizes to exception types the lecture never
   mentions.
6. **Fully checked vs. partially checked applies only inside the checked
   side.** Fully checked = every child class is also checked (`IOException`,
   `InterruptedException`). Partially checked = at least one child is
   unchecked — and across the entire Java hierarchy there are only **two**
   such classes: `Exception` and `Throwable`. There is no third, then or now.
7. **`throws` does not, by itself, mean "checked."** The compiler only
   *requires* `throws` for checked exceptions — `throws
   ArithmeticException` for an unchecked type compiles fine, it's simply
   never mandatory. Read "wherever `throws` appears, it's checked" as a rule
   of thumb about *this lecture's examples*, not a language guarantee.
8. **Classroom names are memory hooks, not API classes.**
   `HallTicketMissingException`, `PenNotWorkingException`,
   `BombBlastException`, and the rest of the car/function-story names don't
   exist in the JDK. The real checked examples from this lecture are
   `FileNotFoundException`, `SQLException`, `ServletException`,
   `RemoteException`; the real unchecked examples are `ArithmeticException`,
   `NullPointerException`, `ClassCastException`.
9. **All `Error`s are unchecked because handling them isn't the
   programmer's job.** `OutOfMemoryError` and its siblings come from
   resource exhaustion the JVM cannot recover from in application code —
   that's a system/server-admin problem, the same way an absent invigilator
   is management's problem, not the student's.

---

**Next:** Video 073 — Customized exception handling (try-catch)
