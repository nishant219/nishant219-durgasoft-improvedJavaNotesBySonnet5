# Video 175 — Generics Part-3: Type Safety & Type Casting Examples (Bounded Types)

## Video info

ASR decode notes: time safety = type safety; bound dat / bound data = bounded type; un founded = unbounded; exter / externs = extends; run / runable / unable = Runnable; interace = interface; CH class = child class; compar / comp meod = compile-time error; Paka = pakka (definitely); iner / in = Integer; leg / Len = listen; keep subing = board note.

## Session overview

Part-3 extends the Gen<T> / generic-class foundation from Video 174 with bounded types — restricting the type parameter to a particular range when the class logic only makes sense for certain types (e.g. arithmetic only on numbers).

Prerequisite (recap from prior session):

- Need and advantage of generics
- Type parameter concept
- Non-generic vs generic ArrayList class
- How to create our own generic class
What this session covers:

- Motivation: arithmetic on T requires numeric bound
- `T extends Number` — bounded type for numeric operations
- Unbounded vs bounded type parameters
- Syntax: class Test<T extends X>
- X as class vs interface — what types are allowed at instantiation
- Live compile demos with error messages
- Multiple bounds: T extends Number & Runnable
- More combinations: T extends Runnable & Comparable, T extends Number & Runnable & Comparable
- Invalid combinations and reasons (order, multiple classes)
- Three conclusions: extends-only keyword; any valid identifier for T; multiple type parameters (HashMap<K,V>)
### 00:05 — Recap and the bounded-type problem

Previous session covered: need of generics, type parameter, generic vs non-generic class, creating own generic class.

New twist — extension of prior `Test<T>` example:

Suppose:

```java
class Test<T> {
    public void m1() {
        T a, b;
        System.out.println(a + b);
        System.out.println(a * b);
        System.out.println(a / b);
    }
}
```

Problem: Arithmetic operations (+, *, /) apply only to numbers, not to arbitrary types.

- Two String objects: a + b OK (concatenation), but a * b and a / b are meaningless
- Two Student objects: all three operations meaningless
If functionality applies only to a particular boundary (numbers), we must bound the type parameter up to `Number` only.

Solution:

```java
class Test<T extends Number> {
    public void m1() {
        T a, b;
        // arithmetic meaningful only when T is Number or subclass
        System.out.println(a + b);
        System.out.println(a * b);
        System.out.println(a / b);
    }
}
```

At type parameter we can pass any type which is a child class of `Number`.

Child classes of `Number`: Byte, Short, Integer, Long, Float, Double (and Number itself).

### 03:47 — Bounded vs unbounded type parameters

We can bound the type parameter for a particular range by using the `extends` keyword.

Such types are called bounded types.

Board definition:

We can bound the type parameter for a particular range by using `extends` keyword. Such types are called bounded types.

### 06:49 — Unbounded example — any type allowed

```java
class Test<T> { }

Test<Integer> t1 = new Test<Integer>();   // valid
Test<String> t2 = new Test<String>();   // valid
```

For unbounded Test<T>:

- Type parameter we can pass any type
- There are no restrictions
- Hence it is an unbounded type
### 09:27 — Bounded example: `T extends Number`

```java
class Test<T extends Number> { }

Test<Integer> t1 = new Test<Integer>();   // valid — Integer is child of Number
Test<String> t2 = new Test<String>();     // INVALID — compile error
```

Compile error:

type parameter java.lang.String is not within its bound

(String is not a subclass of Number.)

### 10:08 — Wrong keywords: `implements` and `super` (not for bounded types)

Sir shows invalid syntax variants to trap exam mistakes:

```java
// WRONG — do not use for bounded types:
class Test<T implements Runnable> { }   // invalid terminology
class Test<T super String> { }          // super not applicable
```

Only this is correct for bounded types:

```java
class Test<T extends Number> { }        // valid
class Test<T extends Runnable> { }      // valid — extends works for interfaces too
```

Note: Wherever implements would seem natural, replace with `extends` — in generics, `extends` is used for both classes and interfaces.

### 12:37 — Syntax for bounded type (formal)

General syntax:

```java
class Test<T extends X> { }
```

`X` can be either class or interface.

Board (copy exactly):

Syntax for bounded type:

class Test<T extends X> { }

X can be either class or interface.

If X is a class:
  → at type parameter: X type or its child classes

If X is an interface:
  → at type parameter: X type or its implementation classes

### 16:13 — Examples: `T extends Number` and `T extends Runnable`

#### Example 1 — `T extends Number`

```java
class Test<T extends Number> { }

Test<Integer> t1 = new Test<Integer>();     // valid
Test<String> t2 = new Test<String>();       // CE: String not within bound
```

#### Example 2 — `T extends Runnable`

```java
class Test<T extends Runnable> { }

Test<Runnable> t1 = new Test<Runnable>();   // valid
Test<Thread> t2 = new Test<Thread>();       // valid — Thread implements Runnable
Test<Integer> t3 = new Test<Integer>();     // CE: Integer not in bound
```

Error for Integer on Runnable bound:

type parameter java.lang.Integer is not within its bound

Sir executes live in Test.java to confirm all compile errors.

### 26:38 — Multiple bounds (combination)

Requirement: Type parameter must be child class of Number AND implement Runnable — both conditions simultaneously.

Syntax:

```java
class Test<T extends Number & Runnable> { }
```

Not comma — use `&` between bounds.

More valid combinations:

```java
// Must implement BOTH interfaces:
class Test<T extends Runnable & Comparable> { }

// Child of Number AND implements both interfaces:
class Test<T extends Number & Runnable & Comparable> { }
```

### 32:43 — Invalid multiple-bound combinations

#### Invalid 1 — interface before class (wrong order)

```java
class Test<T extends Runnable & Number> { }   // INVALID
```

Reason: Same as normal Java class declaration — class first, then interfaces:

```java
class A extends B implements C { }   // valid
class A implements B extends C { }   // invalid
```

For bounded types: `extends Number` (class) must come before `& Runnable` (interface).

#### Invalid 2 — extending more than one class

```java
class Test<T extends Number & Thread> { }   // INVALID
```

Reason: Java does not support multiple inheritance of classes. Number and Thread are both classes — cannot extend two classes simultaneously (same rule as class A extends B, C).

Valid pattern summary:

Rules when defining bounded types in combination:

- My type parameter can extend one class and implement interface(s)
- My type parameter can implement more than one interface
- Class first, then interfaces (extends keyword chain)
- Not more than one class in the bound list
### 39:46 — Conclusions (three notes)

#### Note 1 — Bounded types defined only with `extends`

We can define bounded types only by using `extends` keyword.

- `implements` and `super` keywords are NOT allowed
- Where implements purpose is needed → replace with `extends`
```java
class Test<T extends Number> { }      // valid
class Test<T implements Runnable> { } // WRONG
class Test<T super String> { }          // WRONG
class Test<T extends Runnable> { }    // valid (interface via extends)
```

#### Note 2 — Type parameter name

The type parameter need not be `T` — any valid Java identifier:

```java
class Test<T> { }      // convention — T means Type parameter
class Test<X> { }      // valid
class Test<A> { }      // valid
class Test<Durga> { }  // valid
```

Convention: Use `T` because T starts with T and means type parameter — not compulsory.

#### Note 3 — Multiple type parameters

Based on requirement, we can declare any number of type parameters, separated by comma:

```java
class Test<A, B> { }
class Test<X, Y, Z> { }
```

Real API example — `HashMap`:

```java
class HashMap<K, V> { }   // K = key type, V = value type

HashMap<Integer, String> m = new HashMap<Integer, String>();
```

Two type parameters: K (key type), V (value type).

## Bounded types — complete reference table

## Compile error messages (exam)

## Full demo code — bounded types

```java
// Unbounded
class UnboundedTest<T> { }

// Bounded — numbers only
class NumberTest<T extends Number> {
    public void printSum(T a, T b) {
        System.out.println(a.doubleValue() + b.doubleValue());
    }
}

// Bounded — Runnable hierarchy
class RunnableTest<T extends Runnable> { }

// Multi-bound (conceptual — type must satisfy both)
class MultiBoundTest<T extends Number & Runnable> { }

public class BoundedTypeDemo {
    public static void main(String[] args) {
        UnboundedTest<Integer> u1 = new UnboundedTest<>();
        UnboundedTest<String> u2 = new UnboundedTest<>();

        NumberTest<Integer> n1 = new NumberTest<>();
        // NumberTest<String> n2 = new NumberTest<>();  // CE

        RunnableTest<Thread> r1 = new RunnableTest<>();
        // RunnableTest<Integer> r2 = new RunnableTest<>();  // CE

        NumberTest<Integer> nums = new NumberTest<>();
        nums.printSum(10, 20);
    }
}
```

## OCJP/SCJP exam checklist (Video 175)

- [ ] Define bounded type — restrict type parameter to a range via extends
- [ ] Distinguish unbounded (<T>) vs bounded (<T extends Number>)
- [ ] Syntax: class Test<T extends X> — X = class or interface
- [ ] If X is class → X or subclasses; if interface → X or implementors
- [ ] Know child classes of Number: Byte, Short, Integer, Long, Float, Double
- [ ] Multi-bound syntax: T extends Number & Runnable (use &, not comma)
- [ ] Invalid: T extends Runnable & Number (class must be first)
- [ ] Invalid: T extends Number & Thread (two classes)
- [ ] Cannot use implements or super for bounded types — only extends
- [ ] Type parameter name: any valid identifier; T is convention
- [ ] Multiple type parameters: HashMap<K,V>, comma-separated
- [ ] Error: "type parameter X is not within its bound"
## Interview Q&A (rapid fire)

Q: What is a bounded type?

A: A generic type parameter restricted to a range using extends, e.g. T extends Number.

Q: Unbounded vs bounded?

A: Unbounded <T> accepts any type; bounded <T extends Number> accepts Number and subclasses only.

Q: Can we write `T implements Runnable`?

A: No. Use T extends Runnable for both classes and interfaces in generics.

Q: Multiple bounds syntax?

A: T extends ClassBound & Interface1 & Interface2 — one class max, class first.

Q: Must type parameter be named T?

A: No. Any valid Java identifier; T is convention (Type parameter).

Q: Example of two type parameters?

A: HashMap<K, V> — K key type, V value type.

## Cross-references (playlist)

## Board diagrams to reproduce

### Diagram 1: Unbounded vs bounded

Unbounded:     class Test<T>           →  any type OK
Bounded:       class Test<T extends Number>  →  Number hierarchy only

### Diagram 2: Number hierarchy (allowed for T extends Number)

Number
       /  |  \
   Integer Long Double
     /      \
  Byte    Short Float

### Diagram 3: Multiple bounds

Valid:    T extends Number & Runnable & Comparable
          └─ one class ─┘   └── interfaces ──┘

Invalid:  T extends Runnable & Number     (class not first)
Invalid:  T extends Number & Thread       (two classes)

### Diagram 4: Three conclusions

1. Bounded types → extends ONLY (not implements/super)
2. Type param name → any identifier (T = convention)
3. Count → any number, comma-separated (HashMap<K,V>)

## Summary (one paragraph)

Video 175 introduces bounded types to restrict generic type parameters when class logic demands it — Sir's Test<T> with a + b, a * b, a / b only makes sense for numbers, so T extends Number limits arguments to Number and its subclasses (Integer, Double, etc.). Unbounded <T> accepts any type; bounded <T extends X> uses `extends` for both classes and interfaces. For a class bound, pass X or subclasses; for an interface, pass X or implementors. Live demos show Test<String> failing with "not within its bound" when bound is Number, and Test<Integer> failing when bound is Runnable. Multiple bounds use &: T extends Number & Runnable requires both conditions; class must come before interfaces, and only one class is allowed. Three conclusions: define bounds only with extends (not implements/super); type parameter name is any valid identifier (T is convention); declare multiple type parameters comma-separated as in HashMap<K,V>. Generic methods and wildcards continue in later videos.

End of Video 175 notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |  |  |
|---|---|---|---|---|---|
| Position | 175 of 203 |  |  |  |  |
| Title | Core Java With OCJP/SCJP: Generics Part-3 \ | \ | type safety \ | \ | type casting Examples |
| Instructor | Durga Sir (OCJP/SCJP) |  |  |  |  |
| Duration | 54m 19s |  |  |  |  |
| Video ID | JMneguQXeUE |  |  |  |  |
| Watch URL | https://www.youtube.com/watch?v=JMneguQXeUE |  |  |  |  |
| Playlist | Core Java With OCJP/SCJP |  |  |  |  |
| Notes source | YouTube auto-captions (yt-dlp + node PO token) |  |  |  |  |
| Transcript | .transcripts/175-JMneguQXeUE.txt |  |  |  |  |
| Output | 175-generics-type-safety-examples.doc |  |  |  |  |

| Declaration | Kind | Type argument restriction |
|---|---|---|
| class Test<T> | Unbounded | Any type — no restrictions |
| class Test<T extends Number> | Bounded | Number or its subclasses only |

| Bound target | Meaning at type parameter |
|---|---|
| T extends Number | Number or child classes |
| T extends Runnable | Runnable or implementation classes |
| T super String | Not applicable in Java generics |

| If X is… | At type parameter we can pass… |
|---|---|
| Class | X type or its child classes |
| Interface | X type or its implementation classes |

| Rule | Detail |
|---|---|
| Type argument | Any type that is subclass of Number and implements Runnable |
| Keyword between bounds | & |

| Pattern | Valid? |
|---|---|
| T extends Class & Interface | Yes |
| T extends Interface & Interface | Yes |
| T extends Interface & Class | No — class first |
| T extends Class & Class | No — only one class |

| Declaration | Bounded? | Valid type args | Invalid type args |
|---|---|---|---|
| Test<T> | Unbounded | Any reference type | — |
| Test<T extends Number> | Bounded | Integer, Double, Number, … | String |
| Test<T extends Runnable> | Bounded | Runnable, Thread, … | Integer |
| Test<T extends Number & Runnable> | Multi-bound | Types subclassing Number AND implementing Runnable | String, Integer alone |
| Test<T extends Runnable & Number> | — | Invalid syntax (class must be first) | — |
| Test<T extends Number & Thread> | — | Invalid (two classes) | — |

| Situation | Typical message |
|---|---|
| Wrong type for bound | type parameter java.lang.String is not within its bound |
| Primitive as type arg | unexpected type / required: reference |
| Wrong add on generic list | cannot find symbol: method add(Integer) |

| Topic | Video | Notes file |
|---|---|---|
| Generics introduction | 173 | 173-generics-introduction.doc |
| Generic classes & Gen<T> | 174 | 174-generics-type-safety-casting.doc |
| Number wrapper hierarchy | 113 | 113-wrapper-classes.doc |
| Runnable / Thread | 081–082 | chunk-081-100 |
| HashMap (K, V params) | collections Map lectures | chunk-141-160 |
