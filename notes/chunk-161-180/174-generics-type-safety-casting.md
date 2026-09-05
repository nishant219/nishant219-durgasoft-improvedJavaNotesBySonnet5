# Video 174 — Generics Part-2: Type Safety & Type Casting

## Video info

ASR decode notes: time safety = type safety; gen / genic / gener = generics; erist / aist / arist / alist / y = ArrayList / add; Stringer = String; compat = compile-time; meod = method; whoops = OOPs; CH = child; Paka = pakka (definitely); bloody = emphatic (Object argument); template = C++ templates analogy; W / OB = obj variable; Deo / Jan = Gen / GenDemo; keep subing = board note.

## Session overview

Part-2 builds directly on Video 173's two objectives. Sir demonstrates how generic syntax delivers type safety and removes type casting, then covers two introduction-level conclusions, and finally explains internal implementation — how ArrayList<T> replaces Object with a type parameter. The lecture ends with defining your own generic class (Gen<T>) and a live GenDemo execution.

What this session covers:

- Recap — purpose of generics (type safety + type casting)
- Generic syntax: ArrayList<String> — type safety in action
- Generic syntax — no type casting at retrieval
- Comparison table: non-generic vs generic ArrayList
- Conclusion 1: Polymorphism applies to base type only, not parameter type
- Conclusion 2: Type parameter must be class or interface — not primitive
- End of introduction; transition to generic classes
- Pre-1.5 ArrayList: add(Object), get() → Object — root cause of both problems
- Java 1.5 ArrayList<T>: add(T), get() → T; T replaced at compile time
- Meaningful compile error: cannot find symbol: method add(Integer)
- Generic class = parameterized class = template (C++ analogy)
- Custom generic class Gen<T> + GenDemo with String, Integer, Double
What continues in Part-3 (Video 175):

- Bounded types (T extends Number)
- Multiple bounds and invalid combinations
### 00:04 — Recap and generic syntax for type safety

Recap (spell out): Main purpose of generics → provide type safety and resolve type casting problems.

Non-generic (NOT type safe):

ArrayList l = new ArrayList();   // can add any type; cast required on get

Requirement: Hold only String objects.

Generic version:

```java
ArrayList<String> l = new ArrayList<String>();
```

Type safety demonstration:

```java
import java.util.*;

public class GenericTypeSafetyDemo {
    public static void main(String[] args) {
        ArrayList<String> l = new ArrayList<String>();

        l.add("Durga");              // valid
        l.add("Ravi");               // valid
        // l.add(new Integer(10));  // COMPILE ERROR

        l.add("Shiva");              // corrected after seeing CE
    }
}
```

Board pattern (memorize — put in box):

```java
ArrayList<String> l = new ArrayList<String>();
```

Compile error on wrong add: Sir notes the exact message is explained soon; at this stage knowing CE occurs is enough.

### 07:46 — Generic syntax resolves type casting problem

After adding strings, retrieval without explicit cast:

ArrayList<String> l = new ArrayList<String>();
l.add("Durga");
// ... more adds ...

String name1 = l.get(0);   // valid — NO type casting required

Compiler reasoning:

- L is ArrayList<String> (list of String type)
- l.get(0) → first element is always String — there is a guarantee
- Direct assignment to String variable is valid
Board note:

At the time of retrieval we are not required to perform type casting.

Through generics we can solve the type casting problem — because there is a guarantee for the type of element.

Full example:

```java
import java.util.*;

public class GenericNoCastDemo {
    public static void main(String[] args) {
        ArrayList<String> l = new ArrayList<String>();
        l.add("Durga");
        l.add("Ravi");

        String name1 = l.get(0);   // no cast
        String name2 = l.get(1);   // no cast
    }
}
```

### 11:20 — Non-generic vs generic ArrayList (exam comparison table)

This three-row table is a favorite interview / exam question.

### 17:41 — Conclusion 1: Polymorphism — base type only, NOT parameter type

#### OOPs polymorphism recap

From OOPs: usage of parent reference to hold child object = polymorphism.

List l = new ArrayList();        // valid
List l = new LinkedList();       // valid
List l = new Vector();           // valid
List l = new Stack();            // valid

Same List reference can point to different List implementations.

#### Generic version — base type polymorphism works

ArrayList<String> l = new ArrayList<String>();           // valid
List<String> l = new ArrayList<String>();                // valid — parent ref
Collection<String> l = new ArrayList<String>();          // valid — further up

Here:

- Base type = ArrayList, List, Collection (the collection class)
- Parameter type = String (the type argument inside <>)
#### Parameter type polymorphism does NOT work

```java
// INVALID — compile error:
ArrayList<Object> l = new ArrayList<String>();
```

Reason: Polymorphism concept is applicable only for the base type, but NOT for the parameter type.

If reference is ArrayList<Object>, RHS must be ArrayList<Object>.

If reference is ArrayList<String>, RHS must be ArrayList<String>.

String is NOT substitutable for Object in generic parameter position (invariance).

Compile error:

incompatible types
found:    ArrayList<String>
required: ArrayList<Object>

Board conclusion (copy exactly):

Conclusion 1: Polymorphism concept applicable only for the base type, but not for parameter type.

(Polymorphism = usage of parent reference to hold child object.)

Valid vs invalid examples:

```java
import java.util.*;

public class GenericPolymorphismDemo {
    public static void main(String[] args) {
        // VALID — base type polymorphism
        List<String> l1 = new ArrayList<String>();
        List<String> l2 = new LinkedList<String>();
        Collection<String> c = new ArrayList<String>();

        // INVALID — parameter type polymorphism
        // ArrayList<Object> bad = new ArrayList<String>();  // CE
    }
}
```

### 27:15 — Conclusion 2: Type parameter — class/interface only, NOT primitive

For the type parameter in ArrayList<X>, `X` can be any class or interface name — but not a primitive type.

Collections hold objects only, not primitives.

```java
// INVALID:
ArrayList<int> x = new ArrayList<int>();   // CE
```

Compile error:

unexpected type
found:    int
required: reference

Board conclusion (copy exactly):

Conclusion 2: For the type parameter we can provide any class or interface name, but not primitives. If we try to provide a primitive → compile-time error.

Valid type parameters:

ArrayList<String> a = new ArrayList<String>();
ArrayList<Integer> b = new ArrayList<Integer>();    // wrapper, not int
ArrayList<Student> c = new ArrayList<Student>();
ArrayList<Runnable> d = new ArrayList<Runnable>();  // interface OK

End of generics introduction — next topic: internal implementation / generic classes.

### 34:55 — Internal implementation: non-generic ArrayList (until Java 1.4)

Until Java 1.4, no generics. How was ArrayList declared?

Conceptual pre-1.5 declaration:

```java
class ArrayList {
    // boolean add(Object o);   — add method takes Object
    // Object get(int index);   — get returns Object
}
```

Consequences:

Sir's explanation: "Because of this Object argument we can add any type of object — we are missing type safety. Because return type of get is Object — at retrieval compulsory we should perform type casting."

Why old ArrayList is not type safe: the `Object` argument.

Why type casting problem: the `Object` return type.

### 41:00 — Internal implementation: generic ArrayList (Java 1.5+)

Generic declaration (conceptual):

```java
class ArrayList<T> {    // T = type parameter
    // boolean add(T t);
    // T get(int index);
}
```

- T = type parameter
- add takes T type argument
- get returns T type
Key rule: Based on runtime requirement, every `T` will be replaced with our provided type.

```java
Example: ArrayList<String> l = new ArrayList<String>();
```

Compiler considers this version of ArrayList class:

```java
class ArrayList<String> {   // every T → String
    // boolean add(String s);
    // String get(int index);
}
```

Hence:

- Add only String → type safety
- Get returns String → no cast needed
Meaningful compile error on wrong add:

ArrayList<String> l = new ArrayList<String>();
l.add("Durga");              // OK
l.add(new Integer(10));      // CE — cannot find symbol

Error message (exam):

cannot find symbol
symbol:   method add(java.lang.Integer)
location: class ArrayList<String>

Meaning: In ArrayList<String> there is no add method that takes Integer as argument.

Retrieval without cast:

String name1 = l.get(0);   // return type is String — no cast

### 47:24 — Generic class definition; template analogy

In generics we are associating a type parameter to the class.

Such parameterized classes are called:

- Generic classes, or
- Template classes (C++ uses the word templates — same idea)
Template behavior: Not a fixed class — based on requirement, T is replaced:

- ArrayList<String> → every T = String
- ArrayList<Integer> → every T = Integer
- ArrayList<Student> → every T = Student
Board note:

In generics we are associating a type parameter to the class. Such type of parameterized classes are nothing but generic classes or template classes.

Generics not only for collections — can apply to normal Java classes (Account<T>, etc.).

### 1:00:09 — Custom generic class: `Account<T>` (preview)

Brief preview before full Gen<T> example:

```java
class Account<T> { }

Account<GoldAccount> a1 = new Account<GoldAccount>();
Account<PlatinumAccount> a2 = new Account<PlatinumAccount>();
```

Based on requirement we can define our own generic classes.

### 1:03:12 — Custom generic class `Gen<T>` — full implementation

```java
class Gen<T> {
    T obj;                          // variable of type T

    Gen(T obj) {                    // constructor takes T
        this.obj = obj;
    }

    public void show() {
        System.out.println("The type of obj is: " + obj.getClass().getName());
    }

    public T getObj() {
        return obj;                 // return type is T
    }
}
```

Terminology:

Same pattern as ArrayList<T>: type parameter used for field type, constructor arg, and method return type.

### 1:07:02 — `GenDemo` — creating generic objects

```java
class GenDemo {
    public static void main(String[] args) {
        // String version — every T replaced with String
        Gen<String> g1 = new Gen<String>("Durga");
        g1.show();                        // The type of obj is: java.lang.String
        System.out.println(g1.getObj());  // Durga

        // Integer version — every T replaced with Integer
        Gen<Integer> g2 = new Gen<Integer>(10);   // autoboxing: int → Integer
        g2.show();                        // The type of obj is: java.lang.Integer
        System.out.println(g2.getObj());  // 10

        // Double version
        Gen<Double> g3 = new Gen<Double>(10.5);
        g3.show();                        // The type of obj is: java.lang.Double
        System.out.println(g3.getObj());  // 10.5
    }
}
```

Execution output:

The type of obj is: java.lang.String
Durga
The type of obj is: java.lang.Integer
10
The type of obj is: java.lang.Double
10.5

How to create object: Gen<String> g1 = new Gen<String>("Durga"); — pass String to constructor because T = String.

## Key conclusions summary (Video 174)

### Introduction conclusions (end of intro section)

### Implementation conclusions

## OCJP/SCJP exam checklist (Video 174)

- [ ] Write generic declaration: ArrayList<String> l = new ArrayList<String>();
- [ ] Explain type safety via generic add restriction
- [ ] Explain no cast needed: String s = l.get(0);
- [ ] Three-row comparison: non-generic vs generic ArrayList
- [ ] Conclusion 1: List<String> l = new ArrayList<String>() valid; ArrayList<Object> l = new ArrayList<String>() invalid
- [ ] Conclusion 2: ArrayList<int> invalid; ArrayList<Integer> valid
- [ ] Know pre-1.5: add(Object), get() → Object
- [ ] Know post-1.5: T replaced with provided type at compile time
- [ ] Recognize CE: cannot find symbol: method add(Integer) on ArrayList<String>
- [ ] Define generic class = parameterized class = template
- [ ] Write simple Gen<T> with field, constructor, getObj()
## Interview Q&A (rapid fire)

Q: Difference between `ArrayList l = new ArrayList()` and `ArrayList<String> l = new ArrayList<String>()`?

A: First is non-generic (any type, cast required); second is generic (String only, no cast).

Q: Can `ArrayList<Object> l = new ArrayList<String>()` compile?

A: No. Polymorphism works for base type only, not type parameter.

Q: Can we use `int` as type parameter?

A: No. Only reference types (class/interface). Use Integer.

Q: Why was old ArrayList not type safe?

A: add accepted Object; any type could be added.

Q: How does compiler achieve type safety internally?

A: Replaces type parameter T with the supplied type (e.g. String) for that usage.

## Cross-references (playlist)

## Board diagrams to reproduce

### Diagram 1: T replacement at compile time

```java
Source code:     ArrayList<String> l = new ArrayList<String>();
                          ↓
Compiler sees:   class ArrayList<String> {
                     boolean add(String e);
                     String get(int i);
                 }
```

### Diagram 2: Polymorphism scope

Base type (ArrayList, List, Collection):  POLYMORPHISM ✓
     List<String> l = new ArrayList<String>();

Parameter type (String vs Object):        POLYMORPHISM ✗
     ArrayList<Object> l = new ArrayList<String>();  // CE

### Diagram 3: Object vs T (root cause)

Pre-1.5:  add(Object)  → any type in  → no safety
          get() → Object → cast out    → casting headache

Post-1.5: add(T)       → T only in   → type safety
          get() → T     → direct use  → no cast

## Summary (one paragraph)

Video 174 shows how generic syntax fulfills the two objectives from Part-1. ArrayList<String> accepts only strings (compile error on add(Integer)) and returns String from get() without casting. A three-row table contrasts non-generic vs generic ArrayList for version, type safety, and casting. Conclusion 1: parent references work for collection hierarchy (List<String> ref = new ArrayList<String>()), but ArrayList<Object> cannot reference ArrayList<String>. Conclusion 2: type parameters must be reference types — ArrayList<int> fails with "unexpected type; required reference". Internally, pre-1.5 ArrayList used Object for add/get (cause of both problems); Java 1.5 ArrayList<T> substitutes T with the declared type so the compiler enforces String-only adds and String returns. Sir implements a custom Gen<T> class and runs GenDemo with String, Integer, and Double to prove the template model. Introduction to generics ends here; bounded types follow in Part-3.

End of Video 174 notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |  |  |
|---|---|---|---|---|---|
| Position | 174 of 203 |  |  |  |  |
| Title | Core Java With OCJP/SCJP: Generics Part-2 \ | \ | type safety \ | \ | type casting |
| Instructor | Durga Sir (OCJP/SCJP) |  |  |  |  |
| Duration | 1h 18m 49s |  |  |  |  |
| Video ID | Z2h34SQCo4k |  |  |  |  |
| Watch URL | https://www.youtube.com/watch?v=Z2h34SQCo4k |  |  |  |  |
| Playlist | Core Java With OCJP/SCJP |  |  |  |  |
| Notes source | YouTube auto-captions (yt-dlp + node PO token) |  |  |  |  |
| Transcript | .transcripts/174-Z2h34SQCo4k.txt |  |  |  |  |
| Output | 174-generics-type-safety-casting.doc |  |  |  |  |

| Rule | Detail |
|---|---|
| For this ArrayList<String> | We can add only String objects |
| By mistake adding other type | Compile-time error |
| Through generics | We get type safety |

| # | ArrayList l = new ArrayList() | ArrayList<String> l = new ArrayList<String>() |
|---|---|---|
| 1 | Non-generic version of ArrayList | Generic version of ArrayList |
| 2 | Can add any type of object → not type safe | Can add only String → type safe |
| 3 | At retrieval: type casting required | At retrieval: type casting NOT required |

| Design choice | Effect |
|---|---|
| Argument to add is Object | Can add any type → missing type safety |
| Return type of get is Object | At retrieval → must perform type casting |

| Method | After T → String |
|---|---|
| add | Takes String only |
| get | Returns String |

| Symbol | Meaning |
|---|---|
| T | Type parameter — can be any type based on requirement |
| obj | Variable of type T |
| Constructor | Expects same type T as argument |
| getObj() | Return type is T |

| # | Conclusion |
|---|---|
| 1 | Polymorphism applicable only for base type, not parameter type |
| 2 | Type parameter: any class or interface, not primitive |

| Topic | Pre-1.5 | Post-1.5 (generics) |
|---|---|---|
| Class declaration | class ArrayList | class ArrayList<T> |
| add argument | Object | T |
| get return | Object | T |
| Type safety | No | Yes (when type arg specified) |
| Cast on get | Required | Not required |
| Wrong add error | None (runtime CCE possible) | Compile error (cannot find symbol) |

| Topic | Video | Notes file |
|---|---|---|
| Generics intro — two objectives | 173 | 173-generics-introduction.doc |
| OOPs polymorphism | 051–055 | chunk-041-060 |
| Autoboxing (Integer from 10) | 115 | 115-autoboxing-unboxing.doc |
| Bounded types | 175 | 175-generics-type-safety-examples.doc |
