# Video 177 — Generics Part-5: Generic Methods

## Video info

## Session overview

Final major Generics lecture. Builds on Video 176 (wildcards). Topics:

- Recap — role of wildcard ?
- Generic methods — type parameter at method level
- Bounded type parameters at method level (same rules as class level)
- Communication with non-generic code — behavior follows location
- Purpose of generics — type safety + resolve type-casting problems
- Generics applicable only at compile time — type erasure proofs
- Name clash / same erasure — duplicate method signatures after erasure
Durga Sir closes by calling Generics one of the two most dangerous SCJP topics (with inner classes). Expect 1–2 exam questions.

Prerequisite: Videos 173–176 (generic classes, bounded types, wildcards).

## 00:05 — Recap: wildcard `?` and next topic

Last session covered wildcard character ?. This session: generic methods — when you want type safety at method level only, not at class level.

## 00:49 — Generic class vs generic method

### Generic class — type parameter at class level

```java
class Test<T> {
    // T declared just after class name
    // We can use T anywhere within this class based on requirement
}
```

- Declaring type parameter at class level
- Parameterized class = generic class
### Generic method — type parameter at method level only

```java
class Test {   // normal (non-generic) class

    public <T> void m1(T t) {
        // T declared just BEFORE return type
        // We can use T anywhere within this method based on requirement
    }
}
```

- Class is normal; only the method is generic
- Use when you need type safety for one particular method, not the whole class
### Where to declare type parameter

Board note: We can declare type parameter in two places — either at class level or at method level.

## 08:18 — Bounded types at method level

Same bounded-type rules as class level apply at method level.

### Valid bounded method declarations

```java
class Test {
    public <T extends Number> void m1(T t) { }
    public <T extends Runnable> void m2(T t) { }
    public <T extends Number & Runnable> void m3(T t) { }
    public <T extends Comparable & Runnable> void m4(T t) { }
    public <T extends Number & Comparable & Runnable> void m5(T t) { }
}
```

### Invalid bounded method declarations

```java
// INVALID — interface before class
public <T extends Runnable & Number> void bad1(T t) { }

// INVALID — cannot extend more than one class
public <T extends Number & Thread> void bad2(T t) { }
```

### Rules (same as class level)

- First bound must be a class (if any class is present)
- Then interfaces with &
- Cannot extend more than one class
Board note: We can define bounded types even at method level also. These are not new rules — copy-paste from class-level generics.

## 15:30 — Communication with non-generic code

### Core principle: behavior depends on location

The location in which the object is present — based on that, behavior will be defined.

Analogy (Durga Sir's classroom story): Same person behaves differently at Shashi's house (pure vegetarian) vs at Durga Sir's house (non-vegetarian). Person is the same; location changes behavior.

Applied to generics:

## 25:19 — Live demo: generic list passed to non-generic method

```java
import java.util.*;

public class GenericNonGenericDemo {

    public static void main(String[] args) {
        // GENERIC AREA — main method
        ArrayList<String> l = new ArrayList<>();
        l.add("Durga");
        l.add("Ravi");
        // l.add(10);  // CE — generic area enforces String

        M1(l);   // pass generic object to non-generic method

        // Back in GENERIC AREA
        // l.add(10.5);  // CE — again type-safe
        System.out.println(l);
    }

    // NON-GENERIC AREA
    public static void M1(ArrayList l) {   // raw type — no type parameter
        l.add(10);
        l.add(10.5);
        l.add(true);
        // end of M1
    }
}
```

### Step-by-step behavior

After M1 returns, l contains: [Durga, Ravi, 10, 10.5, true] — but in main you still cannot add 10.5 because the reference type is ArrayList<String>.

### Why is passing generic → raw allowed?

Backward compatibility with pre-1.5 (1.4) code. Old libraries use raw types; new generic objects must interoperate.

Board notes:

- If we send a generic object to non-generic area → it starts behaving like non-generic object
- If we send a non-generic object to generic area → it starts behaving like generic object
## 35:06 — Conclusions: purpose and compile-time nature of generics

### Main purpose of generics

- Provide type safety
- Resolve type-casting problems
Both are compile-time concerns:

- Wrong type added → compile-time error
- Missing cast where required → compile-time error
### Generics applicable only at compile time, NOT at runtime

Generics is a template — like an architect's plan:

- Plan needed at the beginning (compile time) to build the building
- Once building exists, you live in the building — not in the plan
- At runtime, no generic concept exists for JVM
Board note: Generics concept is applicable only at compile time, but not at runtime.

### Type erasure — last step of compilation

At the time of compilation, as the last step, generic syntax is removed. For JVM, ArrayList<String> becomes plain ArrayList.

## 40:16 — Proof 1: raw reference + generic object

```java
import java.util.*;

public class ErasureProof1 {
    public static void main(String[] args) {
        ArrayList l = new ArrayList<String>();  // raw ref, generic object
        l.add(10);
        l.add(10.5);
        l.add(true);
        System.out.println(l);   // [10, 10.5, true]
    }
}
```

If generics existed at runtime, adding Integer to a String list would throw exception. It does not — proving erasure.

## 47:07 — Proof 2: all raw declarations equal at runtime

These are functionally equal at runtime (JVM ignores type arguments):

```java
ArrayList l1 = new ArrayList();
ArrayList l2 = new ArrayList<String>();
ArrayList l3 = new ArrayList<Integer>();
ArrayList l4 = new ArrayList<Double>();
```

Compiler checks reference type on LHS. All references are raw ArrayList → all equal for assignment/add rules at compile time when LHS is raw.

Board note: Hence the following declarations are equal (for runtime/JVM perspective after erasure).

## 50:55 — Proof 3: generic LHS enforces type at compile time

ArrayList<String> l1 = new ArrayList<String>();
ArrayList<String> l2 = new ArrayList<>();   // diamond — same

Both equal — compiler always checks l is ArrayList<String>. Only String objects can be added.

## 53:55 — Proof 4: name clash / same erasure

Normal Java — duplicate signatures illegal:

```java
class Test {
    public int m1(int i) { return 10; }
    public int m1(int i) { return 20; }  // CE: m1(int) already defined
}
```

Method signature = method name + argument types (return type not part of signature).

### With generics — erasure causes clash

```java
import java.util.*;

class Test {
    public static void m1(ArrayList<String> l) { }
    public static void m1(ArrayList<Integer> l) { }  // CE after erasure!
}
```

Compiler steps at compile time:

- Compile code normally considering generic syntax — both methods look distinct
- Remove generic syntax (erasure)
- Compile resultant code again — both become m1(ArrayList l) → duplicate signature
Compile error:

name clash: both methods have the same erasure

Erasure = method signature after removing generic syntax.

If generics existed at runtime, these would be two different methods — no clash. The error itself proves compile-time-only generics.

## Live execution proof (from transcript)

```java
import java.util.*;

public class ErasureDemo {
    public static void main(String[] args) {
        ArrayList l = new ArrayList<String>();
        l.add(10);
        l.add(10.5);
        l.add(true);
        System.out.println(l);
    }
}
```

- javac ErasureDemo.java — compiles fine
- java ErasureDemo — runs fine, prints 10, 10.5, true
- No runtime exception despite "String list" on RHS
## Full generic method example

```java
class GenericMethodDemo {

    // Generic method — T scoped to this method only
    public static <T> void printArray(T[] arr) {
        for (T element : arr) {
            System.out.println(element);
        }
    }

    // Bounded generic method
    public static <T extends Number> double sum(T[] arr) {
        double total = 0;
        for (T n : arr) {
            total += n.doubleValue();
        }
        return total;
    }

    public static void main(String[] args) {
        String[] names = {"A", "B"};
        Integer[] nums = {1, 2, 3};

        printArray(names);
        printArray(nums);
        System.out.println(sum(nums));
    }
}
```

## OCJP exam traps (Video 177)

## Summary

Video 177 completes the Generics arc. Generic methods declare <T> before the return type when only one method needs parameterization. Bounded types at method level mirror class-level rules. Location determines behavior when generic and raw code interact — a generic ArrayList<String> passed to raw M1(ArrayList l) allows any add inside M1. Generics exists only at compile time; the compiler erases type parameters so JVM sees raw types — demonstrated by no runtime exception on "wrong" adds and by name clash errors when erasure produces duplicate signatures. This is the last Generics lecture; Durga Sir advises watching Generics videos at least twice.

## What's next

Video 178 begins Garbage Collection — introduction and agenda for ~4 sessions.

End of Video 177 notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Title | Core Java With OCJP/SCJP: Generics Part-5 \ | \ | generics method |
| URL | https://www.youtube.com/watch?v=OddYBiLxZ9Y |  |  |
| Video ID | OddYBiLxZ9Y |  |  |
| Duration | 1h 05m 52s |  |  |
| Position | 177 of 203 |  |  |
| Source | YouTube auto-captions (yt-dlp + node PO token) |  |  |
| Instructor | Durga Sir (OCJP/SCJP) |  |  |

| Level | Syntax position | Example |
|---|---|---|
| Class level | Just after class name | class Test<T> |
| Method level | Just before return type | public <T> void m1(T t) |

| Movement | Behavior |
|---|---|
| Generic object → non-generic area | Starts behaving like non-generic object |
| Non-generic object → generic area | Starts behaving like generic object |

| Location | l reference type | Can add 10? | Can add "Durga"? |
|---|---|---|---|
| main (generic) | ArrayList<String> | No (CE) | Yes |
| Inside M1 (non-generic) | Raw ArrayList | Yes | Yes |
| Back in main (generic) | ArrayList<String> | No (CE) | Yes |

| Question | Answer |
|---|---|
| Compile error? | No — compiler checks reference type (ArrayList raw) |
| Runtime exception? | No — JVM sees plain ArrayList, any object OK |
| Output | 10, 10.5, true |

| Trap | Correct understanding |
|---|---|
| Type parameter location | Class: after name; Method: before return type |
| T extends Runnable & Number | Invalid — class must come first |
| Generic → raw method call | Allowed (compatibility); loses type safety inside raw method |
| Generics at runtime? | No — erasure removes type args |
| ArrayList l = new ArrayList<String>(); l.add(10); | Compiles — ref is raw |
| Two methods differing only by type arg | Name clash after erasure |
| Purpose of generics | Type safety + eliminate casting; compile-time only |
