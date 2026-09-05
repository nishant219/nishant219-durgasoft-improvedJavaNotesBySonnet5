# Video 043 — Interface vs Abstract Class vs Concrete Class

## Video info

**Title:** Core Java With OCJP/SCJP: Declarations and Access Modifiers Part-14|| interfaces-4

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 43 of 203 |
| Series | Declarations and Access Modifiers · Part 14 |
| Topic | interfaces-4 |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 39m 46s |
| Video ID | VUQGdiKSYKI |
| Watch | https://www.youtube.com/watch?v=VUQGdiKSYKI |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. **When to reach for which** of interface, abstract class, and concrete
   class — the "requirement spec / partial implementation / ready to ship"
   ladder, taught through the `Servlet` → `GenericServlet`/`HttpServlet` →
   `MyServlet` chain and a building-construction analogy.
2. **Eight syntactic differences** between interface and abstract class —
   methods, variables, blocks, constructors — the single most-asked
   interview question in this whole course, by Sir's own count.
3. **Why abstract class can have a constructor it can never call directly**
   — a long `Person` → `Student`/`Teacher` example, proved with
   `hashCode()`, that the parent constructor runs *for the child object*,
   not for a separate parent object.
4. **When everything is abstract, prefer interface over abstract class** —
   two technical reasons (single inheritance is precious; an abstract-class
   chain is not free to instantiate), dramatized as hiring an IAS officer to
   sweep floors.

This lecture is the **Java 1.4 / OCJP-era** story: interface = specification
only, full stop. Sir explicitly does **not** teach Java 8 `default` /
`static` interface methods here — that context is added below in callouts,
not on the board. It matters more here than in most videos, because Java 8
partially dissolves the exact line this lecture spends 90 minutes drawing —
see the callout at 14:38.

### 00:04 — Keep writing: interface vs abstract class vs concrete class

Next topic. Very very important. Board heading (he says **keep subing**):

**interface vs abstract class vs concrete class**

He writes it several times so everyone copies it (`intas versus interface versus abstract class` / `conrete class` in the captions). Make sure you people are aware of the difference. Compulsory you should have clarity.

Three characters are there, but in reality **at the end of the cinema** which thing we have to use is **concrete class only**. With only interface or only abstract class we cannot do anything. At the end the compulsory required concept is concrete class.

Question of this video:

- when we should go for **interface**
- when we should go for **abstract class**
- when we should go for **concrete class**
```java
// three characters — but service is provided only by a concrete class
interface Spec { }          // requirement only
abstract class Partial { }  // partial implementation
class Concrete { }          // full implementation, ready to provide service
```

### 00:48 — Thumb rule: when we should go for which

**Thumb rule** (he says “thumber rule”):

1. **I don’t know anything about implementation.** Just we have **requirement specification**. Then go for **interface**. Interface never talks about implementation. “Boss, this is the requirement — these are the things you require to implement.”
```java
interface Requirement {
    void service1();
    void service2();
    // no body — specification only
    // “I don’t know anything about implementation”
}
```

1. **I want to talk about implementation, but not completely — partial implementation.** Then go for **abstract class**.
```java
abstract class PartialImpl implements Requirement {
    public void service1() {
        System.out.println("I can implement this much");
    }
    // service2() still not implemented — partial only
}
```

1. **I am talking about implementation completely, and I am ready to provide service.** Then go for **concrete class**.
```java
class FullImpl extends PartialImpl {
    public void service2() {
        System.out.println("complete implementation — ready to provide service");
    }
}

class Test {
    public static void main(String[] args) {
        FullImpl obj = new FullImpl();
        obj.service1();
        obj.service2();
        // prints I can implement this much
        // prints complete implementation — ready to provide service
    }
}
```

### 02:06 — Best example: Servlet / GenericServlet / HttpServlet / my servlet

Best example he wants on the board: **Servlet**.

**Servlet** never talks about any implementation. It only tells: if you want to develop your own Servlet, these are the **five methods** you require to implement. That specification is available inside the interface.

```java
interface Servlet {
    void init();
    void service();
    void destroy();
    String getServletConfig();
    String getServletInfo();
    // 5 methods — specification only
    // Servlet never talks about implementation
}
```

Next: “Sir I’m talking about implementation — but not completely.” That next level is **abstract class**.

- **GenericServlet** talks about implementation, but not completely.
- **HttpServlet** talks about implementation, but not completely.
These two are **abstract classes** which implement the Servlet interface.

```java
abstract class GenericServlet implements Servlet {
    public void init() {
        System.out.println("GenericServlet: some implementation");
    }
    public void destroy() {
        System.out.println("GenericServlet: some implementation");
    }
    public String getServletConfig() {
        return "config";
    }
    public String getServletInfo() {
        return "generic";
    }
    // service() still abstract — talks about implementation, but not completely
}

abstract class HttpServlet extends GenericServlet {
    public void service() {
        System.out.println("HttpServlet: protocol dispatch — still not a finished servlet");
        doGet();
    }
    protected abstract void doGet();
    // talks about implementation, but not completely
}
```

“I’m talking about implementation **completely**, and ready to provide service” → **concrete class**. Example: **my own Servlet**, which **extends HttpServlet**.

```java
class MyServlet extends HttpServlet {
    protected void doGet() {
        System.out.println("MyServlet: complete implementation — ready to provide service");
    }
}

class Test {
    public static void main(String[] args) {
        // at the end of the cinema we need a concrete class
        MyServlet s = new MyServlet();
        s.init();
        s.service();
        // prints GenericServlet: some implementation
        // prints HttpServlet: protocol dispatch — still not a finished servlet
        // prints MyServlet: complete implementation — ready to provide service
    }
}
```

### 04:06 — Repeat the three rules once

He repeats so it sticks:

- Don’t know anything about implementation — just requirement specification → **interface**.
- Talking about implementation but not completely (partial) → **abstract class**.
- Talking about implementation completely and ready to provide service → **concrete class**.
Best example for that cinema is the Servlet line above.

### 04:44 — Building analogy (plan / 600 floors / fully completed)

Small analogy so you can understand easily.

He wants to construct a **1000-floor building**. First thing required is a **plan**. No one starts construction directly. At plan level everything is ready, then construction starts.

**Plan never talks about implementation.** It only highlights: boss, this is the specification. The plan itself is the **interface** concept.

```java
interface BuildingPlan {
    int TOTAL_FLOORS = 1000;
    // plan never talks about implementation
    // just specification: 1000 floors, this layout, ...
}
```

He started construction, but not completely. Requirement is 1000 floors; **600 floors completed**, still in construction. That is a **partially completed building** → **abstract class**. Partially completed building is the next level of the plan.

```java
abstract class PartialBuilding implements BuildingPlan {
    int completedFloors = 600;
    // 600 of 1000 done — still under construction
    // partial implementation
}
```

He continued the remaining part. One fine day the building is **fully completed** and **ready to accommodate** — today you can enter, stay, start your business. Fully completed building and ready to use → **concrete class**.

```java
class CompletedBuilding extends PartialBuilding {
    CompletedBuilding() {
        completedFloors = 1000;
    }

    void startBusiness() {
        System.out.println("fully completed building — ready to use");
    }
}

class Test {
    public static void main(String[] args) {
        CompletedBuilding b = new CompletedBuilding();
        b.startBusiness();
        // prints fully completed building — ready to use
    }
}
```

### 07:06 — Terminology recap

He hopes the terminology is now clear:

| Concept | Meaning in this lecture |
|---|---|
| interface | don’t know implementation; only requirement specification (the plan) |
| abstract class | talking about implementation, but not completely (partially completed building) |
| concrete class | complete implementation and ready to provide service (fully completed building, ready to use) |

### 07:42 — Board point 1: requirement specification → interface

He asks whether to take the diagram first or theory first. **Theory first.**

Board (he dictates slowly, repeats each line):

**If we don’t know anything about implementation, just we have requirement specification, then we should go for interface.**

Example: **Servlet**.

```java
interface Servlet {
    void init();
    void service();
    void destroy();
    String getServletConfig();
    String getServletInfo();
    // if we don’t know anything about implementation
    // just we have requirement specification
    // then we should go for interface
}
```

### 08:41 — Board point 2: partial implementation → abstract class

**If we are talking about implementation but not completely (partial implementation), then we should go for abstract class.**

Example: **GenericServlet**, **HttpServlet**, etc.

```java
abstract class GenericServlet implements Servlet {
    public void init() { }
    public void destroy() { }
    public String getServletConfig() { return null; }
    public String getServletInfo() { return null; }
    // service() still open — partial implementation
}

abstract class HttpServlet extends GenericServlet {
    public void service() {
        // some HTTP-specific implementation — still not complete
    }
}
```

### 09:52 — Board point 3: complete implementation, ready to provide service → concrete class

**If we are talking about implementation completely and ready to provide service, then we should go for concrete class.**

Example: **my own Servlet**.

```java
class MyServlet extends HttpServlet {
    public void service() {
        System.out.println("my own Servlet — ready to provide service");
    }
}

class Test {
    public static void main(String[] args) {
        new MyServlet().service();
        // prints my own Servlet — ready to provide service
    }
}
```

### 10:51 — Board diagram: Servlet hierarchy

He draws (pause / music while the class copies):

```java
interface          abstract class          concrete class
Servlet    →       GenericServlet    →     MyServlet
                   HttpServlet
```

That is interface, abstract class, concrete class. That’s all for **when we should go for** which concept.

```java
interface Servlet { void service(); }

abstract class GenericServlet implements Servlet { }

abstract class HttpServlet extends GenericServlet { }

class MyServlet extends HttpServlet {
    public void service() {
        System.out.println("concrete class at the end of the cinema");
    }
}

class Test {
    public static void main(String[] args) {
        Servlet s = new MyServlet();
        s.service();
        // prints concrete class at the end of the cinema
    }
}
```

### 13:02 — Keep writing: differences between interface and abstract class

Next terminology. Board heading (**keep uping** / **keep subing**):

**differences between interface and abstract class**

Table form: **interface** | **abstract class**.

Listen to the conclusions first; you can document at last. First points are already known — he is not going to keep any new thing at the start.

### 14:07 — Difference 1: purpose (when to use)

Same “when” as the first half of the class.

- Interface: don’t know anything about implementation; just requirement specification.
- Abstract class: talking about implementation but not completely (partial implementation).
```java
interface I {
    void m1();
    // purpose: requirement specification only
}

abstract class A {
    void m1() {
        System.out.println("partial implementation");
    }
    abstract void m2();
    // purpose: implementation, but not completely
}
```

### 14:38 — Difference 2: methods always public and abstract vs need not be

**Every method present inside interface is always `public` and `abstract`**, whether we are declaring or not. Hence **interface is also considered as 100% pure abstract class**. 100% pure abstract class is nothing but interface.

Every method present inside **abstract class need not be public and abstract**. We can take **concrete methods also**.

```java
interface Inter {
    void m1();
    // compiler treats as: public abstract void m1();
    // whether we are declaring or not
    // hence interface = 100% pure abstract class
}

abstract class Abs {
    abstract void m1();           // abstract — allowed
    public void m2() { }          // concrete — allowed
    void m3() { }                 // concrete, default access — allowed
    // every method need NOT be public and abstract
}

class Test extends Abs {
    void m1() {
        System.out.println("impl");
    }
    public static void main(String[] args) {
        new Test().m2();
    }
}
```

> ⚠️ **Modern Java — interfaces stopped being "100% pure abstract classes" in Java 8.**
> `default` methods (Java 8) and `static` methods (Java 8) let an interface
> carry a real, non-abstract method body; `private` and `private static`
> methods (Java 9, JEP 213) let it carry a body nobody outside the interface
> can even see. "Every method is always public and abstract" is now true
> only of a method declared with **no body** — which is exactly what OCJP
> still tests, so Sir's rule survives for that one case:
>
> ```java
> interface Modern {
>     void spec();                                  // still public abstract, implicitly
>     default void m() { helper(); util(); }        // NOT abstract — has a body
>     static void util() { System.out.println("u"); } // NOT abstract, NOT instance
>     private void helper() { System.out.println("h"); } // NOT public
> }
> ```
>
> A bodyless method is still forced to `public abstract`. A method with a
> body is exempt from both — that's the actual modern rule.

### 15:27 — Difference 3: illegal method modifiers vs no restriction

Because every interface method is always public and abstract, **we cannot declare an interface method with the following modifiers** (he lists them; last session already covered this):

```java
private
```

```java
protected
```

```java
final
```

```java
static
```

```java
synchronized
```

```java
native
```

```java
strictfp
```

No such type of restriction on **abstract class** method modifiers. Inside abstract class you can take private method, static method, synchronized method. **No restrictions on abstract class method modifiers.**

```java
interface Inter {
    private void m1();
    // CE (Java 6/7): modifier private not allowed here
    // CE (Java 9+): private method requires a body — see Modern Java note below
}
```

```java
interface Inter {
    protected void m1();
    // CE: modifier protected not allowed here
}
```

```java
interface Inter {
    final void m1();
    // CE: modifier final not allowed here
}
```

```java
interface Inter {
    static void m1();
    // CE (Java 6/7): modifier static not allowed here
    // CE (Java 8+): static method requires a body — see Modern Java note below
}
```

```java
interface Inter {
    synchronized void m1();
    // CE: modifier synchronized not allowed here
}
```

```java
interface Inter {
    native void m1();
    // CE: modifier native not allowed here
}
```

```java
interface Inter {
    strictfp void m1();
    // CE: modifier strictfp not allowed here
}
```

```java
abstract class Abs {
    private void m1() {
        System.out.println("private method OK in abstract class");
    }
    static void m2() {
        System.out.println("static method OK in abstract class");
    }
    synchronized void m3() {
        System.out.println("synchronized method OK in abstract class");
    }
    public abstract void m4();
    // he said: no restrictions on abstract class method modifiers
}

class Test extends Abs {
    public void m4() { }
    public static void main(String[] args) {
        Abs.m2();
        // prints static method OK in abstract class
    }
}
```

> ⚠️ **Modern Java — `private` and `static` came off this illegal list; `protected`, `final`, `synchronized`, `native` never did.**
> Java 8 added `static` interface methods (JEP-free, just a language change)
> and Java 9 added `private`/`private static` interface methods (JEP 213) —
> both *with a method body*. So the modifier itself is legal today. What's
> still illegal — in every Java version, then and now — is a **bodyless**
> `private` or `static` method, because a private method can't be
> polymorphic (nothing to override) and neither can a static one. Compiled
> and confirmed on JDK 26:
> ```java
> interface Inter {
>     private void m1();     // still CE — "missing a method body"
>     static void m2();       // still CE — "missing a method body"
> }
> interface Modern {
>     private void helper() { System.out.println("legal since Java 9"); }
>     static void util()     { System.out.println("legal since Java 8"); }
>     default void run() { helper(); util(); }
> }
> ```
> `protected`, `final`, `synchronized`, and `native` remain flatly illegal on
> an interface method in every release — confirmed the same way. `strictfp`
> is also still illegal on a bodyless interface method, but since **Java 17**
> (JEP 306) it is a no-op everywhere it *is* legal (e.g. on a `default`
> method) — `javac` compiles it with a warning, not an error, and it changes
> no floating-point behavior any more.
>
> ❗ One thing unaffected by any of this: **interface fields are still
> always `public static final`**, so `private int x = 10;` at the field
> level is still a compile error today — `private` only stopped being
> illegal for *methods*.

These two points talk about **interface methods**. First point talks about **purpose**. Next he will go for **interface variables**.

### 16:36 — Board: writing the method half of the table

He dictates the table again so you copy it (lots of ASR repeats — same three method points).

**Interface column**

1. If I don’t know anything about implementation and just we have requirement specification, then we should go for interface.
1. Inside interface every method is always public and abstract, whether we are declaring or not. Hence interface is considered as **100% pure abstract class**.
1. As every interface method is always public and abstract, we can’t declare with the following modifiers: **private, protected, final, static, synchronized, native, strictfp**.
**Abstract class column**

1. If we are talking about implementation but not completely (partial implementation), then we should go for abstract class.
1. Every method present inside abstract class need not be public and abstract. We can take concrete methods also.
1. There are **no restrictions on abstract class method modifiers**.
```java
interface Inter {
    void m1();
    // always public abstract, whether we declare or not
    // 100% pure abstract class
}

abstract class Abs {
    void concrete() {
        System.out.println("concrete method also allowed");
    }
    abstract void leftover();
}

class Test extends Abs {
    void leftover() { }
    public static void main(String[] args) {
        new Test().concrete();
        // prints concrete method also allowed
    }
}
```

### 21:49 — Difference 4: variables always public static final vs need not be

Last two points talked about methods. Next points talk about **variables**.

Every **interface variable is always `public static final`**, whether we are declaring or not.

Every variable present inside **abstract class need not be public static final**. We can take non-public / private variables, **instance variables**, **non-final variables** also. No problem at all.

```java
interface Inter {
    int x = 10;
    // compiler treats as: public static final int x = 10;
    // whether we are declaring or not
}

abstract class Abs {
    int instanceVar;          // instance — allowed
    private int secret;       // private — allowed
    int notFinal = 20;        // non-final — allowed
    static int s = 30;        // static — allowed, but NOT forced
    // need NOT be public static final
}

class Test extends Abs {
    public static void main(String[] args) {
        Test t = new Test();
        t.instanceVar = 99;
        t.notFinal = 100;
        System.out.println(Inter.x);
        System.out.println(t.notFinal);
        // prints 10
        // prints 100
    }
}
```

### 22:32 — Difference 5: illegal variable modifiers vs no restriction

As every interface variable is always public static final, **we cannot declare it with**:

```java
private
```

```java
protected
```

```java
volatile
```

```java
transient
```

No such type of restrictions for **abstract class variables**. Abstract class variable can be private, can be transient, can be volatile. No problem at all.

```java
interface Inter {
    private int x = 10;
    // CE: modifier private not allowed here
}
```

```java
interface Inter {
    protected int x = 10;
    // CE: modifier protected not allowed here
}
```

```java
interface Inter {
    volatile int x = 10;
    // CE: modifier volatile not allowed here
}
```

```java
interface Inter {
    transient int x = 10;
    // CE: modifier transient not allowed here
}
```

```java
abstract class Abs {
    private int a = 1;
    protected int b = 2;
    transient int c = 3;
    volatile int d = 4;
    // no restrictions on abstract class variable modifiers
}

class Test extends Abs {
    public static void main(String[] args) {
        Test t = new Test();
        System.out.println(t.b);
        // prints 2
    }
}
```

### 23:05 — Difference 6: initialization at declaration vs not required

One rule from earlier sessions: for **interface variable, compulsory we should perform initialization at the time of declaration**, otherwise compile-time error.

For abstract class variables: **no such restriction**. Happily later point of time also we can initialize. No problem at all.

```java
interface Inter {
    int x;
    // CE: = expected (must initialize at declaration)
}
```

```java
interface Inter {
    int x = 10; // compulsory initialization at declaration
}

abstract class Abs {
    int y; // not required to initialize at declaration
}

class Test extends Abs {
    public static void main(String[] args) {
        Test t = new Test();
        t.y = 50; // later point of time — allowed
        System.out.println(Inter.x);
        System.out.println(t.y);
        // prints 10
        // prints 50
    }
}
```

### 23:40 — Board: writing the variable half of the table

He dictates (remaining three variable points):

**Interface**

- Every variable present inside interface is always **public static final**, whether we are declaring or not.
- As every interface variable is always public static final, we can’t declare with: **private, protected, volatile, transient**.
- For interface variables, compulsory we should perform initialization **at the time of declaration only**, otherwise we will get **compile-time error**.
**Abstract class**

- Every variable present inside abstract class need not be public static final.
- There are **no restrictions on abstract class variable modifiers**.
- For abstract class variables we are **not required** to perform initialization at the time of declaration.
```java
interface Inter {
    int x = 10; // public static final, initialized at declaration
}

abstract class Abs {
    int y; // instance, uninitialized at declaration — OK
}

class Test extends Abs {
    public static void main(String[] args) {
        System.out.println(Inter.x);
        System.out.println(new Test().y);
        // prints 10
        // prints 0
    }
}
```

### 28:24 — Six points done; next points are important

Up to this, **six points**. Now the next points are important. Listen.

### 28:30 — Difference 7: static and instance blocks

Inside interface, can I take a **static block**? Covered already in the last session. **Static block, instance block — such type of terminology not applicable** inside interface.

Inside abstract class, happily you can take instance block, static block. No problem at all.

```java
interface Inter {
    static {
        System.out.println("static block");
    }
    // CE: static initializers not allowed in interfaces
}
```

```java
interface Inter {
    {
        System.out.println("instance block");
    }
    // CE: instance initializers not allowed in interfaces
}
```

```java
abstract class Abs {
    static {
        System.out.println("static block OK in abstract class");
    }
    {
        System.out.println("instance block OK in abstract class");
    }
}

class Test extends Abs {
    public static void main(String[] args) {
        new Test();
        // prints static block OK in abstract class
        // prints instance block OK in abstract class
    }
}
```

### 29:01 — Difference 8: constructors

Inside interface, can I take a **constructor**? No. Constructor concept not applicable.

Inside abstract class, can I take a constructor? Yes. Happily we can take constructor inside abstract class. No problem at all. **What is the need?** He will explain — not required to worry at this point.

```java
interface Inter {
    Inter() {
    }
    // CE: interfaces cannot have constructors
}
```

```java
abstract class Abs {
    Abs() {
        System.out.println("abstract class constructor OK");
    }
}

class Test extends Abs {
    public static void main(String[] args) {
        new Test();
        // prints abstract class constructor OK
    }
}
```

### 29:23 — Board: writing points 7 and 8

He starts writing “we can declare static and instance blocks” then immediately: **sorry sorry sorry — we CAN’T declare**.

**Interface**

- Inside interface we **can’t declare static and instance blocks**.
- Inside interface we **can’t declare constructors**.
**Abstract class**

- Inside abstract class we **can declare static and instance blocks**.
- Inside abstract class we **can declare constructor**.
That’s all. If any person asks what is the difference between interface and abstract class, **spell out all these eight points**. Syntactical things — whatever we covered. Most valuable question for the **interview room**. If you attend 10 interviews, **minimum eight interviews** this type of question is there. That much worthy.

There are some **loopholes** he will discuss anyway.

Completed 8-point board (study table of what he wrote):

| # | Interface | Abstract class |
|---|---|---|
| 1 | Don’t know implementation; only requirement specification | Talking about implementation, but not completely (partial) |
| 2 | Every method always public abstract (declared or not) → 100% pure abstract class | Methods need not be public abstract; concrete methods allowed |
| 3 | Can’t use private, protected, final, static, synchronized, native, strictfp on methods | No restrictions on method modifiers |
| 4 | Every variable always public static final (declared or not) | Variables need not be public static final |
| 5 | Can’t use private, protected, volatile, transient on variables | No restrictions on variable modifiers |
| 6 | Must initialize variable at declaration, else CE | Not required to initialize at declaration |
| 7 | Can’t declare static / instance blocks | Can declare static / instance blocks |
| 8 | Can’t declare constructors | Can declare constructor |

```java
interface Inter {
    void m1();
    int x = 10;
    // no blocks, no constructors
}

abstract class Abs {
    int y;
    Abs() { }
    static { }
    { }
    void concrete() { }
    abstract void leftover();
}
```

### 31:50 — We cannot create object, but constructor is allowed — what is the need?

Very very important point.

**We can’t create an object for abstract class, but abstract class can contain constructor.**

What is the need / what is the purpose? Better to take it in question form. Board:

**Anyway we can’t create object for abstract class, but abstract class can contain constructor. What is the need?**

```java
abstract class Abs {
    Abs() {
        System.out.println("constructor exists — but not for new Abs()");
    }
}

class Test {
    public static void main(String[] args) {
        Abs a = new Abs();
        // CE: Abs is abstract; cannot be instantiated
    }
}
```

### 33:06 — One-line answer

Forget lengthy explanation first. Keep this one-line answer in mind (lengthy example comes next):

**Abstract class constructor will be executed whenever we are creating child class object, for child object initialization only.**

I’m creating child class object. For that child object I require initialization. For that child object initialization, **parent constructor also will work**. Abstract class constructor also will work.

Some properties may be **inherited from parent**. For the child object, to perform initialization of **those** (inherited) properties, abstract class can contain constructor.

Is taking constructor inside abstract class advantageous? **Yes — code reusability** is the big benefit. That part he explains with an example.

As of now just remember: when the abstract class constructor will be executed — **whenever we are creating child object, for child object initialization only**.

Board (he dictates):

**Abstract class constructor will be executed whenever we are creating child class object to perform initialization of child class object.**

```java
abstract class Parent {
    Parent() {
        System.out.println("abstract parent constructor — for child object init");
    }
}

class Child extends Parent {
    Child() {
        System.out.println("child constructor");
    }
}

class Test {
    public static void main(String[] args) {
        new Child();
        // prints abstract parent constructor — for child object init
        // prints child constructor
        // one child object; parent constructor ran for THAT object
    }
}
```

Child constructor is there — what is the need of parent constructor? Some properties may be inherited from parent. To initialize those, parent constructor is needed.

### 35:37 — Approach 1: abstract class Person without constructor

He will suggest **two approaches**: without taking constructor in abstract class, and with taking constructor in abstract class. Which is advantageous, you will see with the example.

**Approach 1 — without abstract class constructor.**

`class Person` — every person contains several properties. Person is abstract because we are not telling a particular type of person.

Every person contains hundreds of properties: **name, age, color, height, weight, qualification, …** Assume for the example **100 properties**.

Why didn’t he take a constructor? “I’m not creating an object for abstract class — what is the need of taking constructor? I don’t want to take any constructor inside abstract class.” What is the problem / what is the advantage if we *do* take one? He will show.

```java
abstract class Person {
    String name;
    int age;
    String color;
    // ... 100 properties (name, age, color, height, weight, qualification, ...)
    // NO constructor — approach 1
}
```

### 37:49 — Approach 1: Student (101 constructor lines)

First child: **`class Student extends Person`**.

Student-specific property: **`int rollNumber`**. Assume only one extra property.

Total properties for a student object: **101** (100 from parent + 1 child).

Constructor must initialize **all 101**, because those 100 parent properties are also part of the student object.

```java
class Student extends Person {
    int rollNumber;

    Student(String name, int age, String color, int rollNumber) {
        this.name = name;
        this.age = age;
        this.color = color;
        // ... 97 more this.xxx = xxx;   ← first 100 lines from parent
        this.rollNumber = rollNumber;     // 101st line
    }
}

class Test {
    public static void main(String[] args) {
        Student s1 = new Student("Ravi", 22, "fair", 101);
        // pass 101 properties; constructor has 101 assignment lines
        System.out.println(s1.name + " " + s1.rollNumber);
        // prints Ravi 101
    }
}
```

Parent class: 100 properties. Child: 1 extra. Total 101. Creating child object: pass 101 arguments. Inside constructor: 101 lines (`this.name = name; this.age = age; ... this.rollNumber = rollNumber`).

### 41:06 — Approach 1: Teacher (same 100 lines again)

Same cinema, one more child: **`class Teacher extends Person`**.

Teacher-specific property: **`String subject`** (he says we could also take experience, salary — he restricts to one property).

Total again **101 properties**. Constructor again: first 100 assignments copied, last line `this.subject = subject`.

```java
class Teacher extends Person {
    String subject;

    Teacher(String name, int age, String color, String subject) {
        this.name = name;
        this.age = age;
        this.color = color;
        // ... 97 more parent assignments — SAME 100 lines again
        this.subject = subject;
    }
}

class Test {
    public static void main(String[] args) {
        Teacher t = new Teacher("Durga", 40, "fair", "Java");
        System.out.println(t.name + " " + t.subject);
        // prints Durga Java
    }
}
```

He lists the 100 lines as: `this.name`, `this.age`, `this.color`, `this.motherName`, `this.fatherName`, `this.height`, `this.weight`, … — 101 properties we have to keep.

### 44:22 — 1000 child classes → 100 lines written 1000 times

One parent, 100 properties. Those 100 are required for **every** child.

Assume **1000 child classes**: Teacher, Student, Principal, Father, Mother, …

In **every** child, constructor is compulsory. If every child has one extra property, every child constructor has **101 lines**. The **first 100 lines are common**.

You write those 100 lines in Student, again in Teacher, again in the next child — **1000 times**, because there are 1000 child classes.

This code is **not programmer friendly**. `this.name`, `this.age`, … 100 lines in every child class. Unnecessary complexity of the programming is going to rise.

That’s why: parent already contains those properties, parent is abstract class — **why don’t you shift those 100 lines to the parent?** If you write them in the parent, they apply by default for every child. Then you are **not required to write those 100 lines 1000 times separately**.

```java
// approach 1 pain (same 100 assignments in EVERY child)
class Student extends Person {
    int rollNumber;
    Student(String name, int age, int rollNumber) {
        this.name = name; // copied
        this.age = age;   // copied
        this.rollNumber = rollNumber;
    }
}

class Teacher extends Person {
    String subject;
    Teacher(String name, int age, String subject) {
        this.name = name; // copied AGAIN
        this.age = age;   // copied AGAIN
        this.subject = subject;
    }
}

class Principal extends Person {
    Principal(String name, int age) {
        this.name = name; // copied AGAIN — × 1000 children
        this.age = age;
    }
}
```

### 46:11 — Approach 2: constructor inside abstract Person

Same example, but **with parent constructor**.

He warns: not that much easy. In last batches **only 30 to 40% of the people** could understand this example. Take special care. Nothing easy — lengthy example.

**`abstract class Person`** — still 100 properties (`String name`, `int age`, …).

Initialization of those 100 properties: perform **here only**. Take **Person constructor** with 100 parameters; inside it, 100 lines: `this.name = name; this.age = age; ...`

```java
abstract class Person {
    String name;
    int age;
    String color;
    // ... 100 properties

    Person(String name, int age, String color) {
        this.name = name;
        this.age = age;
        this.color = color;
        // ... 100 lines of code — written ONCE in the parent
    }
}
```

Biggest advantage of taking constructor inside abstract class — he shows with the children.

### 47:50 — Approach 2: Student with `super(...)`

**`class Student extends Person`**. Child has `int rollNumber` only.

Whenever we are creating child object, child constructor still receives **101 properties** (100 from parent + 1 specific). But inside the body: **not** 100 times `this.name = name`. Only one line:

**`super(` 100 properties `);`** then `this.rollNumber = rollNumber;`

Call goes to the parent; parent’s 100 lines execute.

```java
class Student extends Person {
    int rollNumber;

    Student(String name, int age, String color, int rollNumber) {
        super(name, age, color); // 100 properties → parent constructor
        this.rollNumber = rollNumber; // only 2 lines in the child constructor
    }
}

class Test {
    public static void main(String[] args) {
        Student s1 = new Student("Ravi", 22, "fair", 101);
        // 101 args in; 100 go to parent constructor; 1 assigned here
        System.out.println(s1.name + " " + s1.rollNumber);
        // prints Ravi 101
    }
}
```

**Does parent constructor work for the student object?** Yes. Which object are we creating? **Student object.** Whenever we create student object, student constructor executes, and **as part of that**, parent constructor executes. **Parent constructor and child constructor both will work for the child object purpose only.** Remember this.

How many constructors got executed? **Two.** How many objects created? **Only one.** Both parent and child constructor work for child object purpose only.

### 51:02 — Approach 2: Teacher with `super(...)`

**`class Teacher extends Person`**, `String subject`.

Constructor still takes 101 properties. Inside: **not** 100 times `this.name`. Only:

`super(` 100 properties `);` then `this.subject = subject;`

```java
class Teacher extends Person {
    String subject;

    Teacher(String name, int age, String color, String subject) {
        super(name, age, color); // 100 properties
        this.subject = subject;
    }
}

class Test {
    public static void main(String[] args) {
        Teacher t = new Teacher("Durga", 40, "fair", "Java");
        System.out.println(t.name + " " + t.subject);
        // prints Durga Java
    }
}
```

Teacher constructor runs; as part of it, 100 properties initialized in parent constructor, remaining one in child. Total 101 initialized for **this teacher object**.

### 52:56 — Second approach is advantageous; both constructors serve the child object

Which code is the lengthy code — first approach or second? **First approach is the lengthy code.**

How many child classes? **1000.** In each child constructor we require to write **only two lines** (`super(...)` + the one child assignment). In the first case every child constructor needed **101 lines**.

Which is the advantageous feature? **Second one.**

Abstract class can contain constructor, **but this constructor will work for child object purpose only**.

Constructor purpose is **to initialize an object, not to create object**. Don’t get confused. This (parent) constructor is initializing the properties which are coming from the parent. This (child) constructor is initializing the remaining properties. Total 101 properties assigned to the teacher object / student object.

This is the **role of constructor present in abstract class**.

```java
abstract class Person {
    String name;
    int age;
    Person(String name, int age) {
        this.name = name; // inherited properties — initialized here
        this.age = age;
    }
}

class Student extends Person {
    int rollNumber;
    Student(String name, int age, int rollNumber) {
        super(name, age);           // parent constructor: inherited fields
        this.rollNumber = rollNumber; // child constructor: remaining fields
    }
}

class Test {
    public static void main(String[] args) {
        new Student("Ravi", 22, 101);
        // 2 constructors executed, 1 object created
    }
}
```

### 54:34 — Wrong claim: “parent object is also created”

Even some books, some faculty members may tell: whenever we are creating child object, **automatically parent object will be created**, because parent constructor got executed. Some people may use that word. **It’s wrong.**

**Parent constructor will execute for child object purpose only.**

Importance of abstract class constructor: suppose if this constructor is not there, programmer life is very horrible — 101 properties here, 101 there, 101 there.

### 55:16 — Board: Approach 1 (not recommended — more code, redundancy)

He asks if they want this example on the board. Yes. Better to keep at the beginning.

Board heading:

**Approach 1 — without having constructor in abstract class**

He can **blame this code**: length of the code is more; **code redundancy** problems are there. Better to add comments: **this code is not recommended — more code and code redundancy problem is there.**

Not that much easy thing — take it clearly. Abstract class Person, total 100 properties. Class Student extends Person, `int rollNumber`. Student constructor: `String name, int age, ...` — 101 properties.

```java
// APPROACH 1 — without constructor in abstract class
// NOT recommended: more code + code redundancy

abstract class Person {
    String name;
    int age;
    // ... 100 properties
}

class Student extends Person {
    int rollNumber;

    Student(String name, int age, int rollNumber) {
        this.name = name;       // 100 common lines
        this.age = age;
        this.rollNumber = rollNumber;
    }
}

class Teacher extends Person {
    String subject;

    Teacher(String name, int age, String subject) {
        this.name = name;       // same 100 lines AGAIN
        this.age = age;
        this.subject = subject;
    }
}

class Test {
    public static void main(String[] args) {
        Student s1 = new Student("Ravi", 22, 101);
        Teacher t = new Teacher("Durga", 40, "Java");
        System.out.println(s1.rollNumber);
        System.out.println(t.subject);
        // prints 101
        // prints Java
    }
}
```

### 1:00:40 — Board: Approach 2 (highly recommended — less code, reusability)

**Keep writing: Approach 2 — with constructor inside abstract class.**

Here I’m taking constructor inside abstract class. **This constructor will work for every child object creation.**

In every child constructor we have to take only **two lines**. In the first approach, every child constructor had **101 lines**.

**This code is highly recommended.**

Why recommended? **Less code and code reusability.**

```java
// APPROACH 2 — with constructor inside abstract class
// HIGHLY recommended: less code + code reusability
// this constructor will work for every child object creation

abstract class Person {
    String name;
    int age;
    // ... 100 properties

    Person(String name, int age) {
        this.name = name;
        this.age = age;
        // 100 lines — once
    }
}

class Student extends Person {
    int rollNumber;

    Student(String name, int age, int rollNumber) {
        super(name, age); // only 2 lines in child
        this.rollNumber = rollNumber;
    }
}

class Teacher extends Person {
    String subject;

    Teacher(String name, int age, String subject) {
        super(name, age); // only 2 lines in child
        this.subject = subject;
    }
}

class Test {
    public static void main(String[] args) {
        new Student("Ravi", 22, 101);
        new Teacher("Durga", 40, "Java");
        // parent constructor reused for every child object
    }
}
```

### 1:06:18 — Need of constructor inside abstract class

At this point you should be aware: what is the need of constructor inside abstract class. Big example, big picture. Importance of abstract class constructor.

### 1:06:34 — Directly or indirectly we cannot create abstract-class object

Can I use this word: we can’t create object for abstract class **directly**, but **indirectly** we can create object for abstract class internally?

**No.** Take a note:

**Either directly or indirectly, we can’t create object for abstract class.**

```java
abstract class Abs {
    Abs() {
        System.out.println("runs for child object — does NOT mean Abs object exists");
    }
}

class Child extends Abs { }

class Test {
    public static void main(String[] args) {
        // direct:
        // Abs a = new Abs();
        // CE: Abs is abstract; cannot be instantiated

        // creating Child does NOT secretly create an Abs object either
        Child c = new Child();
        System.out.println(c instanceof Abs);
        // prints true   (child IS-A Abs — still ONE object, the child)
    }
}
```

`instanceof` being true does **not** mean a second parent object was created. One child object; it is also of parent type. He proves that with hashCode next.

### 1:07:39 — Interview: why constructor in abstract class but not in interface?

Maybe a chance to ask in the interview room:

**We can’t create object for abstract class and interface. But abstract class can contain constructor, but interface doesn’t contain constructor. What is the reason?**

Simple reason: **the main purpose of constructor is to initialize instance variables.**

Inside abstract class there may be instance variables, which are required for the child. To perform initialization of those instance variables, constructor is required inside abstract class.

Inside interface, every variable is always **public static final**. There is **no chance of existing instance variable**. No instance variable means constructor concept is **not required** for the interface.

```java
abstract class Abs {
    int x; // instance variable possible — constructor needed to init it for the child
    Abs(int x) {
        this.x = x;
    }
}

interface Inter {
    int x = 10; // always public static final — NOT an instance variable
    // Inter() { }  // CE: no constructor — none needed
}

class Test extends Abs {
    Test() {
        super(10);
    }
    public static void main(String[] args) {
        System.out.println(new Test().x);
        System.out.println(Inter.x);
        // prints 10
        // prints 10
    }
}
```

### 1:08:48 — Board: reason (instance variables vs public static final)

He dictates the interview question and the reason:

**Anyway we can’t create object for abstract class and interface, but abstract class can contain constructor, but interface doesn’t contain constructor. What is the reason?**

- The main purpose of constructor is **to perform initialization of instance variables** (instance variable is the part of object).
- Abstract class can contain instance variables which are required for child object. To perform initialization of those instance variables, **constructor is required for abstract class**.
- But every variable present inside interface is always **public static final**, whether we are declaring or not. There is **no chance of existing instance variable inside interface**. Hence **constructor concept is not required for interface**.
Why constructors are not required for interface — now the reason is clear.

```java
abstract class Abs {
    String name; // instance — part of child object
    Abs(String name) {
        this.name = name; // constructor exists for this reason
    }
}

interface Inter {
    String TYPE = "spec";
    // public static final only — constructor concept not required
}

class Test extends Abs {
    Test() {
        super("child");
    }
    public static void main(String[] args) {
        System.out.println(new Test().name);
        System.out.println(Inter.TYPE);
        // prints child
        // prints spec
    }
}
```

### 1:14:21 — Creating child object does not create parent object

One more statement you people should be aware:

**Whenever we are creating child class object, parent constructor will be executed, but parent object won’t be created.**

Some faculty members draw a diagram as if a parent object is also created, memory structure and so on. **No.**

Whenever we are creating child class object, parent constructor will be executed. Reason you already saw in the big Person example: some properties coming from parent to child; to initialize those properties which are required for the **child object**, parent class can contain constructor. **It doesn’t mean we are creating object for parent class.**

Where is the proof? Maybe a chance to ask. Board:

**Whenever we are creating child class object, parent object won’t be created. Just parent class constructor will be executed for the child object purpose only.**

### 1:16:37 — Proof: `this.hashCode()` in parent, child, and after `new C()`

Simple proof example. **`class P`**. Inside parent constructor, print **`this.hashCode()`** — then you immediately know: this constructor got executed on **which object**, what is the hash code of that object.

**`class C extends P`**. Inside C constructor (whether we take it or not, super will be there anyway), also `System.out.println(this.hashCode())`.

**`class Test`** with `main`. Create **child** object: `C c = new C();` then `System.out.println(c.hashCode())`.

```java
class P {
    P() {
        System.out.println(this.hashCode());
    }
}

class C extends P {
    C() {
        System.out.println(this.hashCode());
    }
}

class Test {
    public static void main(String[] args) {
        C c = new C();
        System.out.println(c.hashCode());
        // prints SAME number three times (example: 12345678)
        // prints 12345678
        // prints 12345678
        // only ONE object — the child
    }
}
```

How many objects are we creating? **Only one** — the child object (`C c = new C()`). If we create child object, because of `super`, parent constructor runs. Parent constructor and child constructor will work **only for child object purpose**.

**Assume** (wrong theory): whenever we create child object, parent object also got created. Then parent constructor would work for parent object, child constructor for child object — **two hash codes**, separate hash code here, separate hash code there. And `c.hashCode()` would match only the child one.

If we execute this code we **won’t get different hash codes**. **Only one hash code.** Suppose we get `100` in parent constructor — that means child object. Same `100` in child constructor. Same `100` from `c.hashCode()`. If we are getting the **same hash code**, you should accept: **all these constructors will work for the same object only, and that object is the child object only.**

Whenever we are creating child object, automatically parent constructor will be executed **for child object purpose**, and **parent object won’t be created**. Proof: execute this example. You are going to get **only one hash code, not two**, because how many objects we created? Only one.

### 1:20:26 — He types, compiles, and runs `Test.java`

He types it on the machine (classroom path he says: `C:\Durga classes\Test.java`).

```java
class P {
    P() {
        System.out.println(this.hashCode());
    }
}

class C extends P {
    C() {
        System.out.println(this.hashCode());
    }
}

class Test {
    public static void main(String[] args) {
        C c = new C();
        System.out.println(c.hashCode());
    }
}
```

`javac Test.java` — compiles fine. `java Test`.

How many objects are we creating? Only one. Whenever we are creating child object, parent constructor **will** be executed, but parent object **won’t** be created.

Observe: how many numbers are we getting? **Only one number** — of course **three numbers are same**. Then how many objects got created? **Only one object.**

Whenever we are creating child class object, parent constructor will be executed for the child object purpose, but parent object won’t be created.

```java
class Test {
    public static void main(String[] args) {
        C c = new C();
        System.out.println(c.hashCode());
        // prints <same>
        // prints <same>
        // prints <same>
        // three SOPs, one object
    }
}
```

### 1:22:54 — Board: all three SOPs print the same number

Take this example clearly.

Parent constructor will work for child object only. Child constructor also will work for child object only. **Both constructors will work for the same child object purpose only.**

In all three cases, **same number**. Need not be 100, but whatever number we are getting, **same number will be there in all three SOPs**. Same number by default will be there.

```java
class P {
    P() {
        System.out.println(this.hashCode()); // same
    }
}

class C extends P {
    C() {
        System.out.println(this.hashCode()); // same
    }
}

class Test {
    public static void main(String[] args) {
        C c = new C();
        System.out.println(c.hashCode()); // same
        // prints <n>
        // prints <n>
        // prints <n>
    }
}
```

That’s all: whenever we are creating child object, parent object won’t be created — just parent constructor will be executed.

### 1:24:27 — If everything is abstract, go for interface

Last one more concept.

**If everything is abstract, then we should go for interface.**

Doubt: even inside interface every method is always abstract. If you want, inside abstract class also we can take **only abstract methods**. Concrete methods we *can* take — “I don’t want to take. I want to take only abstract methods inside abstract class.” Then **what is the difference between interface and abstract class?**

Inside interface we can take only abstract methods. If you want, inside abstract class also I can take only abstract methods. Then **can I replace interface concept with abstract class?**

```java
interface Inter {
    void m1();
    void m2();
    // every method is always abstract
}

abstract class Abs {
    abstract void m1();
    abstract void m2();
    // only abstract methods — also possible
}
```

### 1:27:17 — Can we replace interface with abstract class?

**Replacement is possible, but it’s not a good programming practice.**

If everything is abstract, **highly recommended to go for interface. Don’t go for abstract class.**

> ⚠️ **Modern Java — one old reason to reach for a class here is gone: sealed interfaces (17, JEP 409).**
> Before Java 17, an interface's implementer list was open to anyone,
> anywhere — a real reason some teams chose an abstract class instead,
> since a class hierarchy could at least be kept `final`/package-private.
> `sealed` removes that trade-off: an interface can now name exactly which
> classes may implement it, closing the family without giving up "requirement
> specification only":
> ```java
> sealed interface Shape permits Circle, Square { }
> final class Circle implements Shape { }
> final class Square implements Shape { }
> // any third class writing `implements Shape` is now a compile error
> ```
> Confirmed on JDK 26. This doesn't change Sir's rule — everything abstract
> still means interface — it just removes the last technical excuse for
> reaching for an abstract class instead.

### 1:27:31 — IAS officer recruited for sweeping

Why? Analogy.

DurgaSoft has multiple venues. Every day after classes, sweeping is required. Newspaper: **wanted sweepers** for DurgaSoft. Qualification: compulsory should be **IAS officer**, minimum **15 years of government experience**.

Can I keep this type of thing for sweeper activity? If that appears in the newspaper, definitely some officer will call: “You are going to recruit an IAS officer for sweeping activity?”

Strictly speaking: **can an IAS officer sweep?** Maybe at home, years ago as a bachelor he did all the work. Strictly speaking, officer **can** perform sweeping. No problem. The problem: **it’s not good programming practice. We are misusing the role** of sweeper activity. IAS person used for sweeping = misusing his role.

Same: in the place of interface, if I go for abstract class, **we are misusing the role of abstract class**. When should we go for abstract class? If we are talking about implementation. If we **never** talk about implementation, choosing abstract class is the **worst kind of programming practice**.

```java
// everything abstract — CAN be written as abstract class
abstract class SweeperRole {
    abstract void sweep();
}

// but the specification-only job belongs to interface
interface SweeperRoleSpec {
    void sweep();
}

class Test implements SweeperRoleSpec {
    public void sweep() {
        System.out.println("use interface when everything is abstract");
    }
    public static void main(String[] args) {
        new Test().sweep();
        // prints use interface when everything is abstract
    }
}
```

### 1:29:31 — Board: possible, but not good programming practice

Board (he dictates):

**We can replace interface with abstract class, but it is not a good programming practice.**

This is something like **recruiting IAS officer for sweeping activity**.

**If everything is abstract, then it is highly recommended to go for interface.**

```java
interface Inter {
    void m1();
    void m2();
}

abstract class Abs {
    abstract void m1();
    abstract void m2();
}

class Impl1 implements Inter {
    public void m1() { }
    public void m2() { }
}

class Impl2 extends Abs {
    void m1() { }
    void m2() { }
    // possible — but not a good programming practice
    // if everything is abstract, go for Inter, not Abs
}
```

### 1:31:19 — Two technical problems (abstract class X vs interface X)

“I want to go for abstract class only — what is the problem?” Technical problems now.

If everything is abstract, two choices: interface, or abstract class. If I go for interface — what advantage. If I go for abstract class — what problem.

He takes **`abstract class X`** (everything abstract) **and `interface X`**. Either you can go for this or that; **interface is recommended, not abstract class**. Two problems.

```java
abstract class X {
    abstract void m1();
}

interface XI {
    void m1();
}
```

### 1:32:09 — Problem 1: missing inheritance benefit

**Approach 1 (abstract class):** `class Test extends X` — we have to implement those methods.

Our class extending X: **is it possible to extend any other class?** No. **We are missing inheritance benefit.** Java won’t allow extending two classes.

**Approach 2 (interface):** `class Test implements X`.

Our class implementing X: **is it possible to extend any other?** Yes. You **won’t miss any inheritance benefit**.

While extending abstract class we can’t extend any other — we are missing. While implementing interface, happily we can extend any other class — inheritance benefit is there.

```java
abstract class X {
    abstract void m1();
}

class Other {
    void help() {
        System.out.println("parent class we wanted to keep");
    }
}

class Test extends X {
    void m1() { }
    // class Test extends X, Other  — CE: cannot extend two classes
    // we are missing inheritance benefit
}

class Test2 extends Other implements XI {
    public void m1() { }
    // implementing interface — we can still extend some other class
}

interface XI {
    void m1();
}

class Demo {
    public static void main(String[] args) {
        new Test2().help();
        // prints parent class we wanted to keep
    }
}
```

```java
class Test extends X {
    void m1() { }
    // already extends X — cannot also extend Other
}

class TestOk extends Other implements XI {
    public void m1() { }
    // while implementing interface we can extend some other class
    // hence we won’t miss any inheritance benefit
}
```

### 1:33:18 — Problem 2: object creation is costly (2 minutes vs 2 seconds)

Second problem. `Test t = new Test();`

Whenever we are creating child class object, automatically **parent constructor will execute** and **parent instance control flow will execute** and so on. Assume **2 minutes** time is required to create Test object (when Test **extends** abstract class X).

Whenever Test **implements** interface X: parent constructor, parent instance control flow — **nothing**, because it is an interface. Interface doesn’t contain instance block. Interface doesn’t contain constructor. `Test t = new Test();` — just in **2 seconds** my object is ready.

**Object creation is costly** in the abstract-class case. **Object creation is not costly** in the interface case. 2 minutes vs 2 seconds.

Which approach is recommended? **Interface approach.** If everything is abstract, highly recommended to go for **interface, but not for abstract class**.

```java
abstract class X {
    {
        // instance control flow — runs on every new child
        System.out.println("parent instance block");
    }
    X() {
        System.out.println("parent constructor");
    }
    abstract void m1();
}

class Test extends X {
    void m1() { }
    public static void main(String[] args) {
        Test t = new Test();
        // object creation is COSTLY
        // parent instance block + parent constructor always run
        // prints parent instance block
        // prints parent constructor
        // (he said: assume 2 minutes)
    }
}
```

```java
interface X {
    void m1();
    // no constructor, no instance block
}

class Test implements X {
    public void m1() { }
    public static void main(String[] args) {
        Test t = new Test();
        // object creation is NOT costly
        // (he said: 2 seconds — object is ready)
        System.out.println("ready");
        // prints ready
    }
}
```

### 1:34:42 — Board: approach 1 vs approach 2 side by side

He repeats: if everything is abstract, highly recommended to go for interface, **but not for abstract class**.

Take this part: **Approach 1 | Approach 2** side by side. If we go for abstract class | if we go for interface.

```java
// Approach 1 — everything abstract, but we chose abstract class (NOT recommended)
abstract class X {
    abstract void m1();
}

class Test extends X {
    void m1() { }
    public static void main(String[] args) {
        Test t = new Test(); // costly + we already used our one extends
    }
}
```

```java
// Approach 2 — everything abstract, we chose interface (HIGHLY recommended)
interface X {
    void m1();
}

class Test implements X {
    public void m1() { }
    public static void main(String[] args) {
        Test t = new Test(); // not costly + we can still extend some other class
    }
}
```

### 1:36:02 — Board notes: inheritance + cost

**Approach 1 (abstract class)**

- While extending abstract class, it is **not possible to extend any other class**, and hence **we are missing inheritance benefit**.
- In this case **object creation is costly**. Example: `Test t = new Test();` — just spell out sample board: **2 minutes**.
**Approach 2 (interface)**

- While implementing interface we **can extend some other class**, and hence **we won’t miss any inheritance benefit**.
- In this case **object creation is not costly**. `Test t = new Test();` — **2 seconds**.
```java
abstract class X { abstract void m1(); }
class Other { }

// approach 1 — missing inheritance benefit
class TestAbs extends X {
    void m1() { }
    // cannot also extend Other
}

// approach 2 — won’t miss inheritance benefit
interface XI { void m1(); }
class TestIf extends Other implements XI {
    public void m1() { }
}

class Demo {
    public static void main(String[] args) {
        TestAbs a = new TestAbs();     // costly (parent ctor / instance flow)
        TestIf i = new TestIf();       // not costly
        System.out.println("done");
        // prints done
    }
}
```

### 1:38:54 — Recommendation

If everything is abstract, highly recommended to go for **interface**, but not for abstract class. Seems we *can* use abstract class also, but **it’s not a good programming practice**.

```java
// if everything is abstract → interface, not abstract class
interface X {
    void m1();
}

class Test implements X {
    public void m1() {
        System.out.println("highly recommended: interface");
    }
    public static void main(String[] args) {
        new Test().m1();
        // prints highly recommended: interface
    }
}
```

### 1:39:09 — End of Declarations and Access Modifiers; before OOPs

That’s all. This is about **Declarations and Access Modifiers** concept.

**Before OOPs** (`whoops` in the captions) what you have to learn: all these things. Then learning OOPs will become very easy.

What this whole chapter covered (he recaps):

- all modifiers whatever are there in Java
- what is Java source file structure
- what about interface — almost on the interface concept only, **around 5 hours** we spent, so that each and every **loophole** by default you got
That’s all.

```java
class Test {
    public static void main(String[] args) {
        System.out.println("Declarations and Access Modifiers complete — next: OOPs");
        // prints Declarations and Access Modifiers complete — next: OOPs
    }
}
```

---

## Exam and interview points

1. **The three-way thumb rule:** no known implementation → interface; some
   implementation, not all → abstract class; full implementation, ready to
   serve → concrete class. Only a concrete class can ever be instantiated.
2. **The eight interface-vs-abstract-class differences**, in order: (1)
   purpose, (2) methods always `public abstract` vs need not be, (3) illegal
   method modifiers (`private, protected, final, static, synchronized,
   native, strictfp`) vs none, (4) variables always `public static final`
   vs need not be, (5) illegal variable modifiers (`private, protected,
   volatile, transient`) vs none, (6) mandatory initialization at
   declaration vs optional, (7) no static/instance blocks vs allowed, (8) no
   constructors vs allowed. Sir's own estimate: **8 of 10 interviews** ask
   this.
3. **An abstract class constructor runs only for the child object being
   created — a separate parent object is never built.** Proved with
   `hashCode()`: parent constructor, child constructor, and
   `child.hashCode()` all print the *same* number, because there is only
   ever one object.
4. **Why interfaces have no constructor but abstract classes do:** a
   constructor's job is initializing instance variables, interfaces can
   never have an instance variable (every field is implicitly `public
   static final`), so the concept doesn't apply.
5. **If everything is abstract, prefer interface over abstract class** —
   choosing abstract class there is possible but "misuses the role," like
   hiring an IAS officer to sweep floors. Two concrete costs: you burn your
   one `extends` on it (interfaces don't cost you inheritance), and
   instantiating through an abstract-class chain runs its constructors and
   instance blocks, while an interface has none to run.
6. **Modern Java already broke the clean three-way split once:** Java 8
   `default`/`static` methods let an interface carry real implementation,
   and Java 9 `private`/`private static` methods let it hide helper code —
   the OCJP-era claim "every interface method is public and abstract" now
   holds only for bodyless method declarations. Interface *fields* are
   unaffected — still always `public static final`.
7. **`private`/`static` interface methods still fail without a body** —
   `private void m1();` and `static void m2();` are compile errors in every
   Java version, but the reason changed: pre-8/9 it was "modifier not
   allowed," now it's "missing a method body." `protected`, `final`,
   `synchronized`, `native` on an interface method are illegal in every
   version, no exceptions.
8. **`strictfp` on any interface or class member has been a no-op since
   Java 17** (JEP 306) — still parses, changes nothing, `javac -Xlint`
   flags it as unnecessary.
9. **Sealed interfaces (17)** let you name the exact permitted implementers
   (`sealed interface Shape permits Circle, Square`), closing the one gap
   that used to tempt people toward abstract classes for "controlled"
   hierarchies — without giving up "interface = specification only."

---

**Next:** Video 044 — new vs Constructor
