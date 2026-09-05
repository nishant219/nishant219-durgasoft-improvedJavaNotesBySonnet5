# Video 176 — Generics Part-4: Generic Methods & Wildcard Characters (?)

## Video info

## Session overview

Continuation of the Generics series. This session covers generic methods (brief intro before wildcards) and the full treatment of wildcard characters (`?`) — one of the two most dangerous OCJP topics (the other is inner classes).

Board sub-topics:

- Generic methods and wildcard character ?
- The problem of type-specific method overload explosion
- Four wildcard method-parameter forms and their calling rules
- For each form: what you can add inside the method
- Assignment compatibility with wildcards (LHS vs RHS rules)
- Live compile-time error messages from the IDE
Prerequisite: bounded type parameters at class level (T extends X), generic classes (class Test<T>).

## 00:05 — Topic introduction: generic methods & wildcard `?`

### Board heading

Generic methods and wildcard character (?)

Durga Sir marks this as a bit difficult — take special care. The ? symbol is described as a bit dangerous for the exam.

## 01:00 — The problem: one method per argument type

### Requirement walk-through

Suppose you have:

```java
import java.util.*;

class WildcardProblemDemo {
    public static void main(String[] args) {
        ArrayList<String> l = new ArrayList<>();
        M1(l);   // OK — matches M1(ArrayList<String>)

        ArrayList<Integer> l1 = new ArrayList<>();
        M1(l1);  // CE — no matching method

        ArrayList<Double> l2 = new ArrayList<>();
        M1(l2);  // CE

        ArrayList<Student> l3 = new ArrayList<>();
        M1(l3);  // CE

        ArrayList<Customer> l4 = new ArrayList<>();
        M1(l4);  // CE
    }

    // Only accepts ArrayList<String>
    public static void M1(ArrayList<String> l) { }
}
```

Every time the argument type changes, you need a new overload:

```java
public static void M1(ArrayList<String> l)   { }
public static void M1(ArrayList<Integer> l)  { }
public static void M1(ArrayList<Double> l)   { }
public static void M1(ArrayList<Student> l)  { }
public static void M1(ArrayList<Customer> l) { }
```

### Problems with overload explosion

### Solution — one method for any list type

Declare one method using wildcard ?:

```java
public static void M1(ArrayList<?> l) { }
```

Now you can call M1 with ArrayList of any type: String, Integer, Double, Student, Customer, etc.

## 06:56 — Four wildcard method-parameter forms (overview)

Durga Sir presents four method signatures. If you understand these four, nothing else remains in wildcard theory for methods.

### Critical distinction: `super` at method level vs class level

Most students feel ? super X is invalid because they confuse it with class-level bounds. At method level with `?`, super is allowed.

## 12:05 — Form 1: `ArrayList<String> l` — fixed type

### How to call

We can call this method by passing ArrayList of only String type. No other type is accepted.

### What you can do inside the method

```java
public static void M1(ArrayList<String> l) {
    l.add("a");    // VALID — String
    l.add(null);   // VALID — null is valid for any reference type
    l.add(10);     // CE — Integer not allowed
}
```

Board note: Within the method we can add only String type objects (and null). Any other type → compile-time error.

## 17:42 — Form 2: `ArrayList<?> l` — unbounded wildcard

### How to call

We can call this method by passing ArrayList of any unknown type — any type at all.

```java
public static void demoCalls() {
    ArrayList<String> l1 = new ArrayList<>();
    M1(l1);   // OK

    ArrayList<Integer> l2 = new ArrayList<>();
    M1(l2);   // OK

    ArrayList<Student> l3 = new ArrayList<>();
    M1(l3);   // OK
}

public static void M1(ArrayList<?> l) { }
```

### Universal rule: every advantage has a disadvantage

Advantage: Accept any ArrayList type.

Disadvantage: Inside the method, the exact element type is unknown at compile time.

```java
public static void M1(ArrayList<?> l) {
    l.add(10.5);   // CE
    l.add("a");    // CE
    l.add(10);     // CE
    l.add(null);   // VALID — only null allowed
}
```

Why 10.5 fails even if caller passed ArrayList<String>: the compiler does not know which type you will pass — it may be Integer, String, etc. So no element can be safely added except null.

### Best use case: read-only operations

```java
public static void M1(ArrayList<?> l) {
    System.out.println(l);   // read-only — perfectly fine
}
```

Board note: This type of method is best suitable for read-only operation, not for writing to the list.

## 28:02 — Form 3: `ArrayList<? extends X> l` — upper bounded wildcard

### How to call

X can be a class or interface.

Example with Number:

```java
public static void M1(ArrayList<? extends Number> l) { }

// Valid calls:
M1(new ArrayList<Integer>());   // Integer extends Number
M1(new ArrayList<Double>());    // Double extends Number
M1(new ArrayList<Number>());    // Number itself

// Invalid:
M1(new ArrayList<String>());    // CE — String is not child of Number
```

### What you can do inside the method

Same as unbounded ?: you don't know which child of X was passed.

```java
public static void M1(ArrayList<? extends Number> l) {
    l.add(10);      // CE
    l.add(10.5);    // CE
    l.add(null);    // VALID
}
```

Board note: Within the method we can't add anything to the list except null, because we don't know the type of X exactly. Best suitable for read-only operation.

## 33:09 — Form 4: `ArrayList<? super X> l` — lower bounded wildcard

### How to call — when X is a class

We can call this method by passing ArrayList of either X type or its super classes.

Example with String:

```java
public static void M1(ArrayList<? super String> l) { }

M1(new ArrayList<String>());   // OK
M1(new ArrayList<Object>());   // OK — Object is super class of String
```

### How to call — when X is an interface (special rule)

If X is an interface (e.g. Runnable), you can pass:

- ArrayList of X type (Runnable), or
- Super class of implementation class of X
Example chain from board:

Runnable (interface)
    ↑ implements
Thread
    ↑ extends
Object

For ? super Runnable, valid lists include ArrayList<Runnable>, ArrayList<Thread>, ArrayList<Object>.

Board statement: If X is an interface, we can call this method by passing a list of either X type or super class of implementation class of X.

### What you can do inside the method — the key flexibility

Unlike ? and ? extends X, `? super X` allows adding X-type objects:

```java
public static void M1(ArrayList<? super String> l) {
    l.add("a");     // VALID — X type (String)
    l.add(null);    // VALID
    l.add(10);      // CE — not String
}
```

Board note: Within the method we can add X type of objects and null to the list.

## 40:16 — Master comparison: all four forms

## 41:59 — Exam-style assignment compatibility

### Valid assignments

ArrayList<String> l = new ArrayList<String>();           // OK
ArrayList<?> l = new ArrayList<String>();                // OK — ? means any type on LHS
ArrayList<? extends Number> l = new ArrayList<Integer>(); // OK — Integer is child of Number
ArrayList<? super String> l = new ArrayList<Object>();   // OK — Object is super of String

### Invalid assignments

ArrayList<? extends Number> l = new ArrayList<String>();
// CE: incompatible types
// found:    ArrayList<String>
// required: ArrayList<? extends Number>

### RHS wildcard rule — critical exam trap

On the right-hand side of assignment, you cannot use bare ? or bounded wildcards. You must specify a concrete class or interface without bounds.

ArrayList<?> l = new ArrayList<?>();              // CE
ArrayList<?> l = new ArrayList<? extends Number>(); // CE

Compile error:

unexpected type
found:    ?
required: class or interface without bounds

Same error for ? extends Number on RHS — the compiler expects a real type name (String, Integer, Object, etc.), not a wildcard.

### Live demo summary (from transcript execution)

## Full reference program — all four method forms

```java
import java.util.*;

class Student { }
class Customer { }

public class WildcardMethodsDemo {

    // Form 1 — exact type
    public static void mExact(ArrayList<String> l) {
        l.add("Durga");
        l.add(null);
        // l.add(10);  // CE
    }

    // Form 2 — unbounded wildcard
    public static void mUnbounded(ArrayList<?> l) {
        System.out.println(l);  // read-only
        l.add(null);
        // l.add("x");  // CE
    }

    // Form 3 — upper bound
    public static void mExtends(ArrayList<? extends Number> l) {
        for (Number n : l) {
            System.out.println(n);
        }
        l.add(null);
        // l.add(10);  // CE
    }

    // Form 4 — lower bound
    public static void mSuper(ArrayList<? super Integer> l) {
        l.add(10);
        l.add(null);
        // l.add(10.5);  // CE
    }

    public static void main(String[] args) {
        mExact(new ArrayList<String>());
        mUnbounded(new ArrayList<Integer>());
        mExtends(new ArrayList<Integer>());
        mSuper(new ArrayList<Number>());
    }
}
```

## OCJP exam traps (Video 176)

- `? super` at method level is valid even though T super X at class level is not.
- `ArrayList<?>` inside method: only null can be added — not even String if parameter is <?>.
- `? super X` inside method: can add objects of type X (and null).
- RHS of assignment: never new ArrayList<?> or new ArrayList<? extends Number>.
- `? extends` call rule: child/implementation classes only — String is not a child of Number.
- Read-only methods: ? and ? extends → use for printing/iterating, not mutating.
## Summary

Video 176 solves the "one method per list element type" problem using wildcard ?. Four method-parameter patterns govern who can call and what can be added inside. Unbounded ? and ? extends X trade write flexibility for universal/read-upper-bound acceptance and are read-only safe. ? super X is the write-friendly lower bound — you may add X-type elements. Assignment compatibility separates wildcard-on-LHS (flexible) from concrete-type-on-RHS (required). The ? symbol is exam-critical; Durga Sir recommends revisiting this lecture at least twice.

## What's next

Video 177 continues Generics Part-5 with generic methods (type parameter at method level) and communication with non-generic code.

End of Video 176 notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |  |  |
|---|---|---|---|---|---|
| Title | Core Java With OCJP/SCJP: Generics Part-4 \ | \ | generics method \ | \ | generics wildcard characters (?) |
| URL | https://www.youtube.com/watch?v=ANzefryEvRo |  |  |  |  |
| Video ID | ANzefryEvRo |  |  |  |  |
| Duration | 57m 07s |  |  |  |  |
| Position | 176 of 203 |  |  |  |  |
| Source | YouTube auto-captions (yt-dlp + node PO token) |  |  |  |  |
| Instructor | Durga Sir (OCJP/SCJP) |  |  |  |  |

| Issue | Effect |
|---|---|
| Code length increases | Maintenance burden |
| Reusability decreases | Same logic duplicated |
| Every new type | Forces yet another method |

| # | Method signature | Call with |
|---|---|---|
| 1 | M1(ArrayList<String> l) | Only ArrayList<String> |
| 2 | M1(ArrayList<?> l) | ArrayList of any type |
| 3 | M1(ArrayList<? extends X> l) | ArrayList of X or its child classes (if X is class) or implementation classes (if X is interface) |
| 4 | M1(ArrayList<? super X> l) | ArrayList of X or its super classes (if X is class); special rule if X is interface |

| Location | super allowed? |
|---|---|
| Class-level type parameter T | No — T super Number is invalid |
| Method-level wildcard ? super X | Yes — valid syntax |

| Operation | Valid? | Reason |
|---|---|---|
| l.add("a") | Yes | L is ArrayList<String> |
| l.add(null) | Yes | Null is valid for every reference type |
| l.add(10) | No (CE) | Only String objects allowed |

| If X is… | You can pass ArrayList of… |
|---|---|
| Class | X type or its child classes |
| Interface | X type or its implementation classes |

| Form | How to call | Add inside method | Best for |
|---|---|---|---|
| ArrayList<String> | Only ArrayList<String> | String + null | Read + write (String only) |
| ArrayList<?> | Any ArrayList | null only | Read-only |
| ArrayList<? extends X> | X or child/impl | null only | Read-only |
| ArrayList<? super X> | X or super/impl-super | X + null | Write producer (add X) |

| Code | Result |
|---|---|
| ArrayList<?> l = new ArrayList<String>(); | Compiles |
| ArrayList<? extends Number> l = new ArrayList<String>(); | CE — incompatible types |
| ArrayList<? extends Number> l = new ArrayList<Integer>(); | Compiles |
| ArrayList<?> l = new ArrayList<?>(); | CE — unexpected type |
| ArrayList<?> l = new ArrayList<? extends Number>(); | CE — unexpected type |
