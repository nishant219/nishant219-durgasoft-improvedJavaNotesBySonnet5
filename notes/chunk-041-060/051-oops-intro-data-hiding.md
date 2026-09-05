# Video 051 — OOPs Introduction and Data Hiding

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming)Part-1||Introduction||data hiding

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 51 of 203 |
| Series | OOPs · Part 1 |
| Topic | Introduction, data hiding |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 26m 39s |
| Video ID | Mp4Fy9TDU_Y |
| Watch | https://www.youtube.com/watch?v=Mp4Fy9TDU_Y |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

The YouTube title promises only "introduction and data hiding," but the board
work actually finishes the whole first OOPs module: **data hiding,
abstraction, encapsulation, tightly encapsulated class**. The first roughly
eight minutes are agenda-only — Sir names every topic the entire OOPs series
will eventually cover, purely theoretically, before writing a single class:
IS-A, HAS-A, method signature, overloading/overriding, static and instance
control flow, constructors and singletons, coupling and cohesion, object type
casting. None of those get answered here — they are markers for videos still
to come. Only once the map is on the board does he circle back and build the
four module-1 concepts properly, with definitions and small classes each. The
next video moves on to IS-A (inheritance).

---

### 00:05 — OOPs is the next topic (interview + daily coding)

OOPs is framed as the single most valuable concept for the **interview room**
and for **day-to-day coding**. Sir warns up front: the first few OOPs items
are theoretical, but they still have to be known cold.

### 00:41 — Agenda: four security-related features (module 1)

Board order for the first block:

1. **Data hiding**
1. **Abstraction**
1. **Encapsulation**
1. **Tightly encapsulated class**

These four are **module 1**. They all talk about **encapsulation / security**.
Data hiding and abstraction are **part of** encapsulation — he treats them one
at a time, then combines them.

### 02:02 — Module 2: IS-A relationship (inheritance)

**IS-A relationship** is also known as **inheritance** — that is module 2 by
itself. Only named here; the actual IS-A lecture is the next session.

### 02:24 — HAS-A relationship, composition, aggregation

**HAS-A** is a very commonly used relationship in Java. Under HAS-A he will
later discuss:

- what HAS-A is
- the advantage of HAS-A
- **composition** vs **aggregation**
- the difference between those two

Still agenda only — no HAS-A code in this video.

### 02:54 — Method signature

After the theoretical block: **method signature**. Later sessions repeat
"method signature must be same" / "method signature must be different"
constantly, so the plan is to first pin down what a method signature actually
is and which parts of a method are considered part of it. Flagged here, not
defined yet.

### 03:19 — Overloading and overriding (polymorphism)

Next major OOPs topics:

- **overloading** (~2.5 hours later)
- **overriding** (~4 hours later)

Both sit under **polymorphism** — the slogan: encapsulation, inheritance, and
under polymorphism, overloading and overriding. Overriding also drags in
**method hiding** and several related rules. Sir calls overloading and
overriding the **major** concepts of the whole OOPs series.

### 04:07 — Static control flow and instance control flow

Two follow-on questions once overloading/overriding are done:

- **static control flow** — if everything in a class is static, in which order
  does control flow happen?
- **instance control flow** — the same question when everything is instance

### 04:37 — Constructors (~4 hours) and singleton classes

**Constructors** are not a 45-minute side topic — Sir budgets about **4
hours** and promises a "postmortem" (deep, exam-style questioning) on them.
One named application area: **how to create singleton classes**, using a
**private constructor**. Syntactic constructor rules and singleton come
later.

### 05:22 — Coupling and cohesion; OOPs is not only three words

Most people, asked "what are OOPs features," only answer **encapsulation,
inheritance, polymorphism**. Sir's pushback: OOPs has roughly **13 features**
in total. **Coupling** and **cohesion** are OOPs features too — more
advanced, and they surface once you talk design patterns and frameworks (his
example: the Struts framework favoring high cohesion and loose coupling). You
still need the basic idea.

### 06:33 — Object type casting; full agenda recap

**Object type casting** — is a given cast valid, when should you reach for
it, what are the rules — gets roughly 1.5 hours later in the series.

| Block | Topics he listed |
|---|---|
| Module 1 (this video) | data hiding, abstraction, encapsulation, tightly encapsulated class |
| Module 2 | IS-A / inheritance |
| HAS-A | composition, aggregation |
| Later | method signature, overloading, overriding (method hiding) |
| Later | static control flow, instance control flow |
| Later | constructors, singleton (private constructor) |
| Later | coupling, cohesion |
| Later | object type casting |

Overloading and overriding are the major concepts; constructors get their own
postmortem. With the agenda spelled out, module 1 starts.

---

## 08:00 — Data hiding

Board heading: **data hiding**. A small, theoretical feature — look at the
word itself: **hiding of data**.

The meaning Sir wants:

- an **outside person** cannot access our **internal data** directly, **or**
- our internal data **should not go out** directly

If someone wants the data, they get it only **after validation /
authentication**, and only the **right person** gets it.

### 08:58 — Real example 1: Gmail inbox

Opening `gmail.com` never shows the inbox first — it asks for username and
password. Only correct credentials unlock the inbox. Even with a valid Gmail
account of his own, Sir cannot open **Charan's** inbox. That is data hiding
in daily life: after credentials, only *your* data.

```java
class GmailAccount {
    private String inbox = "Durga's private mail";
    private String username = "durga";
    private String password = "secret";

    public String getInbox(String u, String p) {
        if (username.equals(u) && password.equals(p)) {
            return inbox;
        }
        return "access denied";
    }
}

class GmailDemo {
    public static void main(String[] args) {
        GmailAccount a = new GmailAccount();
        System.out.println(a.getInbox("durga", "secret"));
        // prints Durga's private mail
        System.out.println(a.getInbox("charan", "anything"));
        // prints access denied
        // System.out.println(a.inbox);
        // CE: inbox has private access in GmailAccount
    }
}
```

Direct field read is a compile failure. The method path runs validation
first, and only then maybe returns data.

### 09:47 — Real example 2: ATM balance (your account only)

As a valid bank customer, swiping his card and entering his PIN shows Sir his
own balance — 25,000. He cannot check **Charan's** or **Pavan's** balance,
even though he is a valid customer of the *same* bank: valid customer is not
the same permission as *your* data. There is no `checkCharanBalance()` API —
if you want data, you call a method, and that method validates who is asking
before it hands anything back.

```java
class BankAccount {
    private double balance = 25000;

    public double checkBalance(int pin) {
        if (pin == 1234) {
            return balance;
        }
        return -1;
    }
}

class AtmDemo {
    public static void main(String[] args) {
        BankAccount mine = new BankAccount();
        System.out.println(mine.checkBalance(1234));
        // prints 25000.0
        System.out.println(mine.checkBalance(0000));
        // prints -1.0
        // System.out.println(mine.balance);
        // CE: balance has private access in BankAccount
    }
}
```

### 11:31 — Board definition of data hiding

**Outside person can't access our internal data directly. Or: our internal
data should not go out directly.** This OOPs feature is nothing but **data
hiding**.

Conclusion on the board:

- outside person cannot access internal data directly
- internal data should not go out directly
- after **validation or authentication**, the outside person *can* access
  internal data
- so the **right person** accesses data — internal data must not be misused

### 13:57 — Two examples copied onto the board

**Example 1:** After providing proper username and password, we can access
our Gmail inbox information.

**Example 2:** Even though we are a valid customer of the bank, we can access
*our* account information, and we cannot access others' account information.

```java
class BoardExample1Gmail {
    private String inbox = "inbox mails";

    public String openInbox(String user, String pass) {
        // after providing proper username and password
        if ("durga".equals(user) && "secret".equals(pass)) {
            return inbox;
        }
        return "login failed";
    }

    public static void main(String[] args) {
        BoardExample1Gmail g = new BoardExample1Gmail();
        System.out.println(g.openInbox("durga", "secret"));
        // prints inbox mails
    }
}
```

```java
class BoardExample2Bank {
    private double myBalance = 25000;

    public double getMyBalance() {
        return myBalance; // our account only
    }

    // no method: getCharanBalance() / getPavanBalance()

    public static void main(String[] args) {
        BoardExample2Bank a = new BoardExample2Bank();
        System.out.println(a.getMyBalance());
        // prints 25000.0
    }
}
```

### 16:09 — How to achieve data hiding in code: `private`

**Every data member is recommended to be declared `private`.** A private
field cannot be read directly from outside; the only path in is a method
(such as `getBalance()`), which validates first and returns data only once
the caller is confirmed to be the right person.

**By declaring every variable as private we can implement / achieve data
hiding.**

### 17:05 — First `Account` on the board (private field)

```java
public class Account {
    private double balance;
    // ...
}
```

Doubt: if it is private, how does an outside caller ever get the value?
Answer — a public getter that validates first:

```java
public class Account {
    private double balance;

    public double getBalance() {
        // validation: is this person a valid person?
        // if yes:
        return balance;
    }
}
```

### 18:23 — Board rule (copy this sentence)

**By declaring data member (variable) as private, we can achieve data
hiding.** "Data member" means **variable**.

### 19:06 — Same `Account` again, with validation then `return`

```java
public class Account {
    private double balance;

    public double getBalance() {
        // validation
        // if this person is valid, then provide access
        return balance;
    }
}
```

What happens if the field is **not** private — anyone reads it with a dot.
That is the insecure arrangement Sir argues against:

```java
public class InsecureAccount {
    public double balance = 25000;
}

class Anyone {
    public static void main(String[] args) {
        InsecureAccount a = new InsecureAccount();
        System.out.println(a.balance);
        // prints 25000.0
        // outsider reads internal data directly — no data hiding
    }
}
```

Private field + outsider class (what the compiler does):

```java
public class Account {
    private double balance = 25000;
}

class Outsider {
    public static void main(String[] args) {
        Account a = new Account();
        System.out.println(a.balance);
        // CE: balance has private access in Account
    }
}
```

Allowed path is the method, after validation:

```java
public class Account {
    private double balance = 25000;

    public double getBalance(boolean validPerson) {
        if (validPerson) {
            return balance;
        }
        return 0;
    }
}

class Customer {
    public static void main(String[] args) {
        Account a = new Account();
        System.out.println(a.getBalance(true));
        // prints 25000.0
        System.out.println(a.getBalance(false));
        // prints 0.0
    }
}
```

### 20:14 — Advantage of data hiding: security

Wherever hiding is there, the reason is **security** — the biggest advantage
of data hiding. Story: imagine a bank willing to hand out any customer's
information on request — username, password, balance, every transaction —
"I'm ready to give this for any person." How many people would open an
account there? None. The Swiss bank example makes the same point from the
other direction: banking secrecy is *why* people keep money there, so a
Swiss bank publishing balances on a website would empty itself overnight.
India's own push to trace undeclared ("black") money runs into the same wall
from the state's side — banks sit behind *n* number of security restrictions
and are simply not allowed to hand that information out, even to a
government asking for it. You can access your own account information;
nobody, however senior, gets to walk in and ask for someone else's.

### 22:25 — Board: main advantage of data hiding is security

**The main advantage of data hiding is security.**

### 22:53 — Highly recommended modifier for variables is `private`

**It is highly recommended to declare data member (variable) as private.**

```java
class JavaDefaultVsRecommended {
    int defaultAccess = 10;     // Java default (package) — NOT the recommendation
    private int hidden = 10;    // highly recommended for data members
}
```

Sir's C-language aside: in C, `int x = 10;` is "private by default." In Java
the same line is package-default, not private — so Java needs an explicit
`private` to get the same effect.

```java
class CStyleHeMentioned {
    // in Java, a bare "int x = 10;" is package-default, NOT private:
    int x = 10;
}

class SamePackageReader {
    public static void main(String[] args) {
        CStyleHeMentioned o = new CStyleHeMentioned();
        System.out.println(o.x);
        // prints 10
        // same-package outsider CAN read Java default — so this is NOT data hiding
    }
}
```

> ❗ **Correction — "in C, the default modifier for a variable is private" is not accurate.**
> C has no access-modifier keywords at all — no `private`, `public`, or
> `protected` exists in the language. What C actually does by default:
>
> - a **local** variable (declared inside a function) has block scope — only
>   code in that function can name it. That is ordinary lexical scoping, the
>   same rule Java's local variables follow, not an access-control feature.
> - a **global** variable (declared at file scope) has **external linkage** by
>   default — it is visible to *every other file* in the program unless you
>   explicitly mark it `static`, which then confines it to its own file. That
>   is the opposite of "private by default."
>
> Sir's point still lands as a teaching device — Java's package-private
> default is looser than most learners expect, and does need an explicit
> `private` to lock down — but "C defaults to private" is not something to
> repeat as fact.

---

## 24:16 — Abstraction

Second feature. Meaning of "abstract idea": **outline**, **central point**,
**top-level** information — not complete information. Property joke: "how
much property do you have?" — "around 4 crores" is the abstract, top-level
answer; listing every plot of land, gold, and share certificate is
**internal detail**, not abstraction.

```java
class PropertyAbstractView {
    public String topLevel() {
        return "around 4 crores"; // highlight only this
    }
}

class PropertyInternalDetails {
    String land = "...";
    String gold = "...";
    String cash = "...";
    String deposits = "...";
    String shares = "...";
    // listing this to the outsider is NOT abstraction
}
```

### 25:46 — Formal meaning: hide implementation, highlight services

**Hide internal implementation and just highlight the set of services what
we have — that is abstraction.**

### 26:12 — ATM card walkthrough (end-user view)

Swipe or insert the card, enter PIN `1234`, GUI screen appears, click
withdraw, enter an amount, choose savings or current, get a receipt, get the
money in about 10 seconds. That whole flow is the **service list** the user
sees — done hundreds of times without a second thought.

### 27:43 — Programmer doubts about what happens internally

Being a programmer (not a layman), the doubts start piling up the moment the
card goes in: is that magnetic-stripe read validated only on the ATM
terminal, or does the request go out to a server? Where is that server
sitting? Which request is actually triggering? Which database does it talk
to, and what are that database's own username and password? In which
language is the validation logic written? Entering the PIN raises the same
questions again — which query, which server — and so does the withdrawal
itself. None of this is visible to the end user, and none of it is supposed
to be.

### 30:22 — Help-desk story (do not ask implementation)

The bit Sir plays for laughs: walk up to a corporate bank's "May I help you"
desk and ask the question politely — validation, sure, but *in which
language* is the code written, and *which server* does the request hit? The
help-desk person's face goes blank; she does not know either, because it is
not her job to know. Push further — hand over a list of twenty such
questions on paper — and the answer changes from a blank stare to "please
wait two minutes," a phone call to the branch manager, and (Sir's punchline)
someone quietly wondering whether you're a hacker. As an end user, you are
responsible for knowing **how to use** the card, not how it is implemented —
even the people running the bank don't all know that. **Hiding internal
implementation and just highlighting the set of services offered is the
concept of abstraction.**

### 32:47 — Board definition of abstraction

**Hiding internal implementation and just highlight the set of services what
we are offering is the concept of abstraction.**

Data hiding vs abstraction, now distinct: one hides **data**; the other hides
**implementation** and shows **services**.

### 35:01 — Example: bank ATM GUI screen

Through the ATM GUI, a bank highlights its services — withdraw, deposit,
check balance, mini statement — without exposing the server, the database,
or the implementation language.

```java
interface AtmGuiScreen {
    void withdraw();
    void deposit();
    void checkBalance();
    void miniStatement();
}
```

That interface **is** the highlighted service set — no SQL, no server host,
no language name anywhere in it.

```java
class HiddenAtmEngine implements AtmGuiScreen {
    public void withdraw() {
        // magnetic stripe, server, Oracle/MySQL/DB2, PIN query...
        // end user never sees this
    }
    public void deposit() { }
    public void checkBalance() { }
    public void miniStatement() { }
}

class EndUser {
    public static void main(String[] args) {
        AtmGuiScreen screen = new HiddenAtmEngine();
        screen.withdraw();
        screen.checkBalance();
        // user only clicks services; implementation stays hidden
    }
}
```

### 36:49 — Board example sentence

**Through bank ATM GUI screen, bank people are highlighting the set of
services what they are offering, without highlighting internal
implementation.**

### 38:07 — Advantages of abstraction — (1) security

Not highlighting internal implementation means the outside person never knows
how the system works internally — which is, again, **security**.

### 39:02 — (2) Enhancement becomes easy (Java vs "Maava")

Sir's running joke: he built this feature in Java, performance is mediocre,
and a shinier new language ("Maava") comes along. Swapping the internal
implementation to Maava — without changing the GUI screen — has **no effect**
on the end user, because the end user only ever sees the service surface.
That is why **enhancement becomes easy**.

```java
interface AtmGuiScreen {
    void withdraw();
}

class JavaAtm implements AtmGuiScreen {
    public void withdraw() {
        // original Java implementation (slow, he says)
    }
}

class MaavaAtm implements AtmGuiScreen {
    public void withdraw() {
        // replacement language; GUI type is still AtmGuiScreen
    }
}

class BankCanSwitchEngine {
    public static void main(String[] args) {
        AtmGuiScreen screen = new JavaAtm();
        screen.withdraw();
        screen = new MaavaAtm(); // internal change
        screen.withdraw();       // same button for the end user
    }
}
```

### 39:47 — (3) easiness to use (4) maintainability

If using an ATM card required understanding its internal implementation, no
one would use ATM cards. Abstraction **improves easiness to use the system**.
It also **improves maintainability**, because internal changes never ripple
out to the caller. Even with all four advantages, the single most important
one is still **security**.

### 42:08 — Four advantages written on the board

**The main advantages of abstraction are:**

1. **We can achieve security** — because we are **not highlighting** our
   internal implementation.
1. **Without affecting outside person we can perform any type of changes in
   our internal system, and hence enhancement will become easy.**
1. **It improves maintainability of the application.**
1. **It improves easiness to use our system.**

```java
class AbstractionAdvantagesAsHeNumberedThem {
    // 1 security: implementation not highlighted
    // 2 enhancement easy: change internals, GUI stays
    // 3 maintainability improved
    // 4 easiness to use (no need to know internals)
}
```

### 45:08 — How do we implement abstraction in Java?

By using **GUI screens** — meaning **interfaces** — and **abstract classes**:

- **partial abstraction** → **abstract class**
- **full abstraction** → **interface**

**By using interfaces and abstract classes we can implement abstraction.**

```java
abstract class PartialAtm {
    abstract void withdraw();          // hidden elsewhere
    void insertCard() {                // some implementation present
        System.out.println("card in");
    }
}

class PartialDemo extends PartialAtm {
    void withdraw() {
        System.out.println("cash");
    }

    public static void main(String[] args) {
        PartialAtm a = new PartialDemo();
        a.insertCard(); // prints card in
        a.withdraw();   // prints cash
    }
}
```

```java
interface FullAtm {
    void withdraw();
    void checkBalance();
    // no method bodies — full abstraction of services
}

class FullDemo implements FullAtm {
    public void withdraw() {
        System.out.println("cash");
    }
    public void checkBalance() {
        System.out.println("25000");
    }

    public static void main(String[] args) {
        FullAtm a = new FullDemo();
        a.checkBalance(); // prints 25000
        a.withdraw();     // prints cash
    }
}
```

He does not open a full abstract-class-vs-interface syntax lesson here — just
the mapping: abstract class = partial, interface = full, and both are *how*
abstraction gets implemented.

> ⚠️ **Modern Java — "interface = full abstraction, 0% implementation" stopped being exactly true in Java 8.**
> On Java 6/7, an interface genuinely could contain no method bodies, which is
> what makes "full abstraction" a clean label for it. Since **Java 8**,
> interfaces can carry real code: `default` methods (with a body, inherited by
> implementers) and `static` methods; **Java 9** added `private` interface
> methods too, for sharing code between an interface's own default methods.
>
> ```java
> interface AtmGuiScreenModern {
>     void withdraw();                       // still abstract — a real service
>
>     default void printReceipt() {          // Java 8: interface method with a body
>         System.out.println("receipt printed");
>     }
>
>     static AtmGuiScreenModern noOp() {      // Java 8: static factory on the interface
>         return () -> System.out.println("noop withdraw");
>     }
> }
> ```
>
> The OCJP-era rule of thumb — "abstract class = partial abstraction, interface
> = full abstraction" — is still the exam's expected answer and still a useful
> mental model for *why* you'd pick one over the other. But the real modern
> distinction is narrower: an interface still cannot hold instance state
> (fields are implicitly `public static final`), and a class can implement
> many interfaces but extend only one abstract class. "Zero implementation
> allowed in an interface" has not been true for over a decade.

> ⚠️ **Modern Java — `sealed` (17) hands the abstraction author back control over who can implement the service surface.**
> On Java 6/7, any class anywhere could `implements AtmGuiScreen` or `extends
> PartialAtm` — the bank in the ATM story has no way to stop a rogue
> `HackedAtmEngine` from appearing in some other package and passing itself
> off as a legitimate implementer. **Java 17** adds `sealed`, which names the
> exact permitted subtypes:
>
> ```java
> sealed interface AtmGuiScreenSealed permits JavaAtm, MaavaAtm { }
>
> final class JavaAtm implements AtmGuiScreenSealed { }
> final class MaavaAtm implements AtmGuiScreenSealed { }
> // final class HackedAtmEngine implements AtmGuiScreenSealed { }
> // CE: class is not allowed to extend sealed interface AtmGuiScreenSealed
> // (HackedAtmEngine is not listed in its permits clause)
> ```
>
> This does not change what abstraction *is* — it changes who is trusted to
> provide an implementation of it, which is exactly the security story this
> section already tells about hiding internal implementation.

Be aware: what is abstraction, and what is data hiding. That is data hiding
and abstraction done.

---

## 46:42 — Encapsulation

Book definition, the kind found in any C++ or Java OOPs chapter:

**The process of binding data and corresponding behavior into a single
unit.**

### 47:38 — Coldact capsule analogy (layman)

The Coldact capsule holds every color of medicine required to cure a cold,
wrapped as one unit — that wrapping is the "capsule" in "encapsulation."
Java's version: bind a class's **data** and its corresponding **behavior**
(methods) into one capsule.

### 49:30 — `Student` class: data members + methods

Variables are also called **data members**. A `Student` needs properties
(name, age, roll number) and methods (`getAttendance`, `getMarks`,
`updateMarks`). **Behavior is nothing but methods.**

**The process of binding data members and corresponding methods into a single
unit is nothing but encapsulation.**

```java
class Student {
    String name;
    int age;
    int rollNumber;

    void getAttendance() { }
    void getMarks() { }
    void updateMarks() { }
}
```

Theoretically, **every Java class is an example of encapsulation**, because
everything in Java is written **within a class** — there is no such thing as
a free-floating variable or method outside one.

### 54:13 — Technical meaning: data hiding + abstraction

Theoretically acceptable, but technically Sir wants something sharper: if a
component follows the **last two features** — data hiding, then abstraction —
do not treat encapsulation as a third, unrelated idea. A **combination of
data hiding and abstraction** is encapsulation.

**If any component follows data hiding plus abstraction, that is
encapsulation.**

### 55:17 — Board: encapsulated component

**If any component follows data hiding and abstraction, such a type of
component is said to be encapsulated component.**

Then the equation:

**encapsulation = data hiding + abstraction**

### 56:49 — Encapsulated `Account`: private field + getter + setter

For every account, `private double balance` gives **data hiding**. Reading it
goes through `getBalance()`, which validates first; updating goes through
`setBalance(...)`, same validation. Because this class follows both data
hiding (the field is private) and abstraction (Sir keeps the class on the
server and projects only a GUI screen to the end user), it is an
**encapsulated component**.

```java
public class Account {
    private double balance;

    public double getBalance() {
        // validation
        return balance;
    }

    public void setBalance(double balance) {
        // validation
        this.balance = balance;
    }
}
```

Direct field use from outside is a compile error:

```java
class OutsidePerson {
    public static void main(String[] args) {
        Account a = new Account();
        a.balance = 10000;
        // CE: balance has private access in Account
        System.out.println(a.balance);
        // CE: balance has private access in Account
    }
}
```

The only legal conversation is through methods, after validation:

```java
public class Account {
    private double balance;

    public double getBalance(boolean valid) {
        if (!valid) {
            return 0;
        }
        return balance;
    }

    public void setBalance(double balance, boolean valid) {
        if (!valid) {
            return;
        }
        this.balance = balance;
    }
}

class AfterValidation {
    public static void main(String[] args) {
        Account a = new Account();
        a.setBalance(10000, true);
        System.out.println(a.getBalance(true));
        // prints 10000.0
        a.setBalance(1, false); // ignored
        System.out.println(a.getBalance(true));
        // prints 10000.0
    }
}
```

### 59:21 — Durga Bank GUI (abstraction half of the same example)

A **balance inquiry** button quietly calls `getBalance()`; an **update
balance** button quietly calls `setBalance()`. The end user just clicks —
never knowing whether the code underneath is Java, .NET, or anything else.
Data hiding plus abstraction, in one place, is encapsulation.

```java
class DurgaBankGui {
    private Account account = new Account();

    void balanceInquiry() {
        // button click — user does not see getBalance()
        System.out.println(account.getBalance());
    }

    void updateBalance() {
        // withdraw or deposit button — user does not see setBalance()
        account.setBalance(10000);
        System.out.println("transaction processed successfully");
    }
}

class DurgaBankCustomer {
    public static void main(String[] args) {
        DurgaBankGui screen = new DurgaBankGui();
        screen.updateBalance();
        // prints transaction processed successfully
        screen.balanceInquiry();
        // prints 10000.0
    }
}
```

(`Account` here is the single-argument `getBalance()`/`setBalance(double)`
version from 56:49.)

### 1:01:22 — Full `Account` copied again on the board

```java
public class Account {
    private double balance;

    public double getBalance() {
        // validation
        return balance;
    }

    public void setBalance(double balance) {
        // validation
        this.balance = balance;
    }
}
```

Balance inquiry → `getBalance()` path. Update balance → `setBalance(double)`
path. Data hiding and abstraction together, which is nothing but
encapsulation. Sir does not want to expose the Java methods directly to the
end user either — some interface concept, some GUI screen, highlighting only
the **set of services**:

```java
interface DurgaBankServices {
    void balanceInquiry();
    void updateBalance();
}

public class Account implements DurgaBankServices {
    private double balance;

    public double getBalance() {
        // validation
        return balance;
    }

    public void setBalance(double balance) {
        // validation
        this.balance = balance;
    }

    public void balanceInquiry() {
        getBalance();
    }

    public void updateBalance() {
        setBalance(10000);
    }
}
```

### 1:03:55 — Main advantages of encapsulation (same list as abstraction)

Because encapsulation *is* abstraction plus data hiding, its advantages are
the same list: **security** (the biggest), **easier enhancement**, and
**improved maintainability**.

**The main advantages of encapsulation are:**

1. **We can achieve security**
1. **Enhancement will become easy**
1. **It improves maintainability of the application**

(Easiness to use is in the spoken list too; the board itself only numbers
these three, matching abstraction's security / enhancement / maintainability
core.)

### 1:05:35 — Loophole: every advantage has a disadvantage

For every advantage, expect a disadvantage. The advantage here is
**security**; the disadvantage takes two stories to land.

### 1:05:56 — Example: online funds transfer (many authentication levels)

Transferring ₹10,000 online — a very ordinary requirement — means clearing
**four levels** of authentication in sequence: log in with a user ID and
password, enter the one-time password that lands on your phone, click funds
transfer, add or confirm the payee, key in the amount and a remark, enter a
separate **transaction password**, then submit and enter four digits from a
grid card (or the back of the ATM card) before the system finally says
"transaction processed successfully." Sir's arithmetic: just moving ₹10,000
now costs 5–10 minutes of your time, purely because of how many authentication
levels stand between you and the transfer. Advantage: only the right person
can move money — no chance of misuse by "some X person." Disadvantage: it is
**time-consuming** — and his own example of the cost: the OTP that arrives
after your class time is already up, forcing you to close the browser and
start the whole sequence again.

```java
class InsecureFastTransfer {
    void transfer(double amt) {
        System.out.println("sent " + amt);
        // one step — fast, but no security layers
    }

    public static void main(String[] args) {
        new InsecureFastTransfer().transfer(10000);
        // prints sent 10000.0
    }
}
```

```java
class EncapsulatedSlowTransfer {
    boolean userIdPasswordOk(String id, String pwd) { return true; }
    boolean otpOk(String otp) { return true; }
    boolean txnPasswordOk(String txn) { return true; }
    boolean gridDigitsOk(String four) { return true; }

    void transfer(String id, String pwd, String otp, String txn, String grid, double amt) {
        if (!userIdPasswordOk(id, pwd)) return;
        if (!otpOk(otp)) return;
        if (!txnPasswordOk(txn)) return;
        if (!gridDigitsOk(grid)) return;
        System.out.println("transaction processed successfully");
    }

    public static void main(String[] args) {
        new EncapsulatedSlowTransfer()
            .transfer("u", "p", "123456", "txn", "9876", 10000);
        // prints transaction processed successfully
        // four checks — longer code, slower execution (his disadvantage)
    }
}
```

### 1:09:29 — Layman example: classroom with four doors vs one security door

Picture this classroom with four doors instead of one. Students trickle in
from whichever door is nearest, 500 chairs fill up in 5–10 minutes, and class
starts. Now add a police constraint: every student must be checked before
entering. Close three of the four doors, and the one that stays open gets a
metal detector, then a scanner, then a bag check with a receipt — only after
that does the student actually sit down. Per student that is 3–5 minutes, and
500 students at that rate is roughly 2,500 minutes, which Sir rounds to
**4–5 hours** of pure security screening for a class that itself only runs
one hour. Advantage: security. Cost: it **slows execution** — the same
trade-off as encapsulation itself, just acted out with doors instead of
authentication screens.

```java
class FourDoorsFast {
    void enter() {
        System.out.println("sit"); // no checks — 5 to 10 minutes for 500 people
    }
}

class OneDoorSecure {
    void metalDetector() { }
    void scanner() { }
    void bagReceipt() { }

    void enter() {
        metalDetector();
        scanner();
        bagReceipt();
        System.out.println("sit");
        // 3 to 5 minutes per student — security up, speed down
    }

    public static void main(String[] args) {
        new OneDoorSecure().enter();
        // prints sit
    }
}
```

### 1:11:27 — Board: advantage vs disadvantage of encapsulation

**The main advantage of encapsulation is we can achieve security.**

**But the main disadvantage of encapsulation is it increases length of the
code and slows down execution.**

---

## 1:13:05 — Tightly encapsulated class

What is it? If a class gives data hiding maximum importance — **each and
every variable of the class is private** — that class is a **tightly
encapsulated class**. Whether it has a getter, a setter, or neither is
**irrelevant**. The only check is: is every variable private?

### 1:14:29 — `Account` as tightly encapsulated (getter is optional)

```java
public class Account {
    private double balance;

    public double getBalance() {
        return balance;
    }
}
```

Tightly encapsulated — yes. The one and only test (all variables private)
passes; whether `getBalance()` exists at all is beside the point:

```java
public class Account {
    private double balance;
}
```

is *equally* tightly encapsulated.

```java
public class Account {
    private double balance;

    public double getBalance() {
        return balance;
    }
}

class TightCheck {
    public static void main(String[] args) {
        Account a = new Account();
        System.out.println(a.getBalance());
        // prints 0.0
        // System.out.println(a.balance);
        // CE: balance has private access in Account
    }
}
```

### 1:15:48 — Board definition (and what we do *not* check)

**A class is said to be tightly encapsulated if and only if each and every
variable declared as private.**

**Whether class contains corresponding getter and setter methods or not, and
whether these methods are declared public or not — these things we are not
required to check.**

> ⚠️ **Modern Java — records give you a tightly encapsulated, encapsulated class for free.**
> A **record** (Java **16**) declares its state once and the compiler
> generates `private final` fields plus accessor methods automatically — every
> field is private by construction, so a record is always a tightly
> encapsulated class under Sir's own rule, with no boilerplate:
>
> ```java
> record Account(double balance) { }
>
> class RecordDemo {
>     public static void main(String[] args) {
>         Account a = new Account(25000);
>         System.out.println(a.balance());
>         // prints 25000.0 — accessor is balance(), not getBalance()
>         // a.balance = 1;  // there is no such field access — CE, no setter exists either
>     }
> }
> ```
>
> Two things change from the hand-written version above: the accessor is
> named after the field (`balance()`, not `getBalance()`), and there is no
> setter at all — a record's fields are `final`, so "encapsulated" here means
> immutable-by-default rather than "guarded by validation before mutation."
> For a genuinely mutable, validated `Account` like the one this lecture
> builds, the hand-written class is still the right tool; for a plain data
> carrier, a record is the modern default and skips the manual private-field-
> plus-getter dance entirely.

### 1:18:35 — Question 1: which of these classes are tightly encapsulated?

```java
class A {
    private int x = 10;
}

class B extends A {
    int y = 20; // default / package — NOT private
}

class C extends A {
    private int z = 30;
}
```

| Class | Tightly encapsulated? | Reason he gives |
|---|---|---|
| A | Yes | every variable is private (`x`) |
| B | No | non-private data is there (`y` is default) — an outside person can access it directly |
| C | Yes | child of A; from A every variable is private, and here `z` is also private |

```java
class WhichAreTight1 {
    public static void main(String[] args) {
        B b = new B();
        System.out.println(b.y);
        // prints 20
        // outsider in same package reads y directly → B is NOT tightly encapsulated

        // System.out.println(b.x);
        // CE: x has private access in A

        C c = new C();
        // System.out.println(c.x);
        // CE: x has private access in A
        // System.out.println(c.z);
        // CE: z has private access in C
    }
}
```

If every variable is private, the class is automatically tightly
encapsulated — presence or public-ness of getters/setters is never part of
the check.

### 1:21:58 — Question 2: parent has default `x`

```java
class A {
    int x = 10; // default — NOT private
}

class B extends A {
    private int y = 20;
}

class C extends B {
    private int z = 30;
}
```

- **A: no** — `x` is not private.
- **B: no** — child of `A`; `A`'s non-private `x` is available here by
  default.
- **C: no** — the same non-private `x` is still available, inherited through
  `B`.

```java
class WhichAreTight2 {
    public static void main(String[] args) {
        A a = new A();
        System.out.println(a.x);
        // prints 10
        // A's x is not private → A is NOT tightly encapsulated

        B b = new B();
        System.out.println(b.x);
        // prints 10
        // inherited non-private x is available → B is NOT tightly encapsulated
        // System.out.println(b.y);
        // CE: y has private access in B

        C c = new C();
        System.out.println(c.x);
        // prints 10
        // A's non-private x is still available through C → C is NOT tightly encapsulated
        // System.out.println(c.y);
        // CE: y has private access in B
        // System.out.println(c.z);
        // CE: z has private access in C
    }
}
```

### 1:24:04 — Conclusion: parent not tight ⇒ no child is tight

**If the parent class is not tightly encapsulated, then no child class is
tightly encapsulated** — because a parent class's non-private data is
available by default to every child.

```java
class ParentNotTight {
    int x = 10; // non-private
}

class ChildPrivateField extends ParentNotTight {
    private int y = 20;
}

class GrandChildPrivateField extends ChildPrivateField {
    private int z = 30;
}

class ParentRule {
    public static void main(String[] args) {
        GrandChildPrivateField g = new GrandChildPrivateField();
        System.out.println(g.x);
        // prints 10
        // parent not tight → this child cannot be called tightly encapsulated
    }
}
```

Contrast with question 1, where the parent *was* tight, so a child adding
only private fields *can* be tight too:

```java
class TightParent {
    private int x = 10;
}

class TightChild extends TightParent {
    private int z = 30;
}

class TightParentRule {
    public static void main(String[] args) {
        TightChild c = new TightChild();
        // System.out.println(c.x);
        // CE: x has private access in TightParent
        // System.out.println(c.z);
        // CE: z has private access in TightChild
        // TightParent tight, TightChild's own field private → TightChild is tight
    }
}
```

### 1:26:01 — Module 1 recap; next session is IS-A

Data hiding, abstraction, encapsulation, tightly encapsulated class — all
four talk about one word: **security**, the biggest advantage these OOPs
features work for. Next session: IS-A relationship / inheritance, and its
loopholes.

---

## Board recap (what he wanted in the notebook)

**Data hiding:** outside person can't access our internal data directly (or
internal data should not go out directly). After validation/authentication,
the right person can. Achieve it by declaring data members **private**. Main
advantage: **security**. Highly recommended modifier for variables:
**private**.

**Abstraction:** hide internal implementation; highlight the set of services
we are offering. Example: bank ATM GUI (withdraw, deposit, check balance,
mini statement) without showing server/DB/language. Implement with
**interfaces** (full) and **abstract classes** (partial). Advantages:
security; enhancement easy without affecting the outsider; maintainability;
easiness to use.

**Encapsulation:** process of binding data and corresponding methods into a
single unit (every Java class, theoretically). Technically: **encapsulation
= data hiding + abstraction**. Encapsulated `Account`: private `balance` +
`getBalance` / `setBalance` behind a GUI. Advantages: security, enhancement
easy, maintainability. Disadvantage: **increases length of the code and
slows down execution**.

**Tightly encapsulated class:** every variable is `private`. Do **not**
require getters/setters or public methods. If the parent is **not** tightly
encapsulated, **no child** is either.

---

## Exam and interview points

1. **Data hiding, abstraction, and encapsulation are three distinct, testable
   definitions** — outside data access blocked (data hiding), implementation
   hidden behind a service surface (abstraction), data + behavior bound
   together (encapsulation) — even though this course's own equation treats
   encapsulation as the sum of the first two.
2. **`private` is the mechanism for data hiding.** A private field cannot be
   read or written from outside its own class — only via methods that can
   validate first (`getBalance()`, `setBalance(...)`).
3. **Abstract class = partial abstraction, interface = full abstraction** is
   the OCJP-era answer and still the expected one — but see the Modern Java
   note above: interfaces have carried real code (`default`/`static` methods
   since 8, `private` methods since 9) for over a decade, so "zero
   implementation in an interface" is no longer literally true.
4. **A tightly encapsulated class has exactly one test: is every variable
   private?** Getters, setters, and their access modifiers are irrelevant to
   the label.
5. **If a parent class is not tightly encapsulated, no child class can be
   either** — a non-private inherited field is reachable through every
   subclass, regardless of how private the subclass's own fields are.
6. **Encapsulation's classic trade-off**: its main advantage is security: its
   main disadvantage is more code and slower execution, illustrated with the
   four-factor bank transfer and the single-door security-check analogies.
7. **Records (Java 16)** are the modern shortcut to a tightly encapsulated,
   encapsulated data class — private final fields and generated accessors for
   free — but they trade away setters entirely, so they fit immutable data
   carriers, not a mutable, validated `Account` like the one built in this
   video.
8. **`sealed` (Java 17)** is the modern answer to "who is allowed to
   implement my service interface" — a question this lecture's ATM story
   raises (a rogue implementer of `AtmGuiScreen`) but has no Java 6/7 keyword
   to answer.
9. **Every advantage in this module traces back to one word: security.** Data
   hiding, abstraction, encapsulation, and tightly encapsulated classes are
   four separate mechanisms converging on the same payoff — expect an
   interviewer to ask "why" after each one, and "security" is the answer
   every time.
10. **Method naming for accessors is a convention, not a compiler rule.**
    `getBalance()` / `setBalance(double)` follow the JavaBean pattern this
    course uses throughout; nothing in the language requires the `get`/`set`
    prefix — a record's `balance()` accessor (see the Modern Java note above)
    is proof the compiler only cares about visibility and validation, not
    naming.
11. **OOPs is not just encapsulation, inheritance, polymorphism.** Coupling,
    cohesion, and object type casting are OOPs topics too — worth naming if
    asked "what are OOPs concepts" to signal you know the field goes past the
    textbook three.

---

**Next:** Video 052 — Inheritance (IS-A)
