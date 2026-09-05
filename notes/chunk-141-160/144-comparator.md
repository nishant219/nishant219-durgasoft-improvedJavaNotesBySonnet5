# Video 144 — Collections Part-9: Comparator Interface & Customized Sorting

## Video info

## Session overview

This is the Comparator deep-dive session in the Collections sorting block. Durga Sir spends roughly the first hour on one flagship example (TreeSet + Integer + descending order) and then a postmortem of seven different compare method implementations to prove that the JVM is blind — it only trusts your return value.

What this lecture covers:

- Comparator interface location, methods, and method prototypes
- Why only compare() needs implementation when implementing Comparator (equals is inherited)
- Comparable vs Comparator recap (natural vs customized sorting)
- Full program: insert Integer objects into TreeSet with descending order
- Line-one theory: with vs without Comparator object in TreeSet constructor
- Step-by-step trace of every compare() call during insertion
- TreeSet internal BST placement + in-order traversal output
- Various possible implementations of compare method — seven styles and their outputs
- JVM-as-blind-person analogy (negative = before, positive = after, zero = duplicate)
What continues in next sessions:

- Five to six more Comparator examples (String, custom objects, multiple comparators, etc.)
Exam mantra: If you understand this one TreeSet example and the seven compare implementations, every remaining Comparator program becomes easy. If you miss this session, the rest of the sorting block will feel impossible.

## 00:04 — Comparator interface: package and methods

### Board point 1: Package location

Board note: Comparator present in java.util package.

### Board point 2: Methods defined

The equals() in Comparator is the same concept as Object.equals() — same name, same role.

## 01:49 — Comparator method prototypes

### Method 1: compare (THE method you must master)

```java
public int compare(Object obj1, Object obj2)
```

Return value contract (identical logic to compareTo() — copy-paste behavior):

Durga Sir's emphasis: compare method behavior = compareTo method behavior. Same terminology, same rules.

### Method 2: equals (dummy for implementation purposes)

```java
public boolean equals(Object obj)
```

No special explanation required — standard Object-class-style equals. You do NOT implement this when implementing Comparator.

## 06:00 — Implementing Comparator: only compare() is compulsory

### The classroom question

"Sir, Comparator defines two methods. When I implement an interface, I must implement every method. So why don't I implement equals()?"

### Answer (inheritance reasoning)

```java
class MyComparator implements Comparator {
    // Must implement compare() only
}
```

- MyComparator is a child class of Object (every class extends Object).
- Object already contains equals() → inherited by default to every child.
- Therefore MyComparator already has equals() from Object.
- Remaining method to implement = `compare()` only.
### Board conclusion (must copy)

Whenever we are implementing Comparator interface, compulsory we should provide implementation only for compare method.

We are not required to provide implementation for equals method, because it is already available to our class from Object class through inheritance.

## 10:16 — Comparable vs Comparator: when to use which

Natural sorting = the class's own compareTo() logic (e.g., Integer ascending).

Customized sorting = your Comparator's compare() logic (e.g., Integer descending, sort by name length, etc.).

## 11:04 — Flagship example: TreeSet descending order for Integer

### Problem statement (board)

Write a program to insert Integer objects into TreeSet where the sorting order is descending order.

### Starter code (without Comparator — ascending by default)

```java
import java.util.*;

public class TreeSetDemo3 {
    public static void main(String[] args) {
        TreeSet t = new TreeSet();   // LINE ONE — mark this on your notes
        t.add(10);
        t.add(0);
        t.add(15);
        t.add(5);
        t.add(20);
        t.add(20);   // duplicate
        System.out.println(t);
    }
}
```

### Expected vs actual output

Sir's requirement: "I don't want this bloody ascending order. I want descending: 20, 15, 10, 5, 0."

## 14:57 — Solution: pass Comparator object to TreeSet constructor

### Step 1: Create Comparator class

```java
class MyComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        Integer I1 = (Integer) obj1;
        Integer I2 = (Integer) obj2;

        if (I1 < I2)
            return +1;      // smaller element → after (descending)
        else if (I1 > I2)
            return -1;      // bigger element → before (descending)
        else
            return 0;       // equal → duplicate
    }
}
```

### Step 2: Pass Comparator at LINE ONE

TreeSet t = new TreeSet(new MyComparator());   // LINE ONE with Comparator

### Critical rule: which method does JVM call?

Observe the difference: Without Comparator → compareTo. With Comparator → compare.

## 17:28 — Descending-order compare logic explained

### Mental model for descending order

When sorting descending (biggest first):

- Smaller value should come after larger value → return positive
- Larger value should come before smaller value → return negative
- Equal values → return zero (duplicate, not inserted in TreeSet)
### Logic table for descending Integer sort

Any positive number works (+1, +1000, etc.). Any negative number works (-1, -1000, etc.). Convention: use +1, -1, 0.

## 17:28 — Full insertion trace (step by step)

Elements added in order: 10, 0, 15, 5, 20, 20

### Insert 10 (first element)

- No comparison required for the first element.
- 10 becomes the root of the internal BST.
### Insert 0 — compare(0, 10)

- I1 = 0, I2 = 10
- 0 < 10 → return +1 (positive)
- Positive → 0 should come after 10
- 0 placed to the right of 10
10
        \
         0

### Insert 15 — compare(15, 10)

- I1 = 15, I2 = 10
- 15 > 10 → return -1 (negative)
- Negative → 15 should come before 10
- 15 placed to the left of 10
15
        \
        10
          \
           0

### Insert 5 — compare(5, 10) then compare(5, 0)

First: compare(5, 10)

- I1 = 5, I2 = 10 → 5 < 10 → return +1 → 5 goes right of 10
Second: compare(5, 0) (0 already on right side)

- I1 = 5, I2 = 0 → 5 > 0 → return -1 → 5 goes before 0
Result: 5 after 10, before 0.

15
        \
        10
       /
      5
        \
         0

### Insert 20 — compare(20, 10) then compare(20, 15)

First: compare(20, 10) → 20 > 10 → -1 → go left of 10

Second: compare(20, 15) → 20 > 15 → -1 → go left of 15

20
      \
      15
        \
        10
       /
      5
        \
         0

### Insert 20 (duplicate) — compare(20, 10) → compare(20, 15) → compare(20, 20)

- compare(20, 10) → -1 → go left
- compare(20, 15) → -1 → go left
- compare(20, 20) → 0 → duplicate, NOT inserted
### Final TreeSet output — in-order traversal

Durga Sir uses in-order traversal (Left → Root → Right) on the BST:

"First left, next root, next right..."

In-order on the tree above → [20, 15, 10, 5, 0]

## 26:40 — Central idea: JVM is the blind person

Durga Sir's famous analogy:

JVM is a blind person. JVM doesn't know anything about your sorting logic. JVM simply calls compare(). Based on what you return:

- Return negative → place element before

- Return positive → place element after

- Return zero → treat as duplicate, don't insert

JVM never checks whether your logic is "really" greater-than or less-than. JVM never validates duplicates. Your compare method controls everything.

## 27:04 — LINE ONE theory (board — must memorize)

### Case A: At LINE ONE, if we are NOT passing Comparator object

TreeSet t = new TreeSet();   // no Comparator

- Internally JVM will call compareTo() method
- compareTo() is meant for default natural sorting order
- Output: 0, 5, 10, 15, 20 (ascending for Integer)
### Case B: At LINE ONE, if we are passing Comparator object

```java
TreeSet t = new TreeSet(new MyComparator());
```

- Internally JVM will call compare() method (of your Comparator class)
- compare() is meant for customized sorting
- Output: 20, 15, 10, 5, 0 (descending in our example)
## 27:31 — Complete runnable program (verified in IDE)

```java
import java.util.*;

public class TreeSetDemo3 {
    public static void main(String[] args) {
        TreeSet t = new TreeSet(new MyComparator());
        t.add(10);
        t.add(0);
        t.add(15);
        t.add(5);
        t.add(20);
        t.add(20);
        System.out.println(t);   // [20, 15, 10, 5, 0]
    }
}

class MyComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        Integer I1 = (Integer) obj1;
        Integer I2 = (Integer) obj2;

        if (I1 < I2)
            return +1;
        else if (I1 > I2)
            return -1;
        else
            return 0;
    }
}
```

### Demo without Comparator (ascending)

Remove new MyComparator() → run again:

Output: [0, 5, 10, 15, 20]

### Demo with Comparator (descending)

Add new MyComparator() back → run:

Output: [20, 15, 10, 5, 0]

## 41:18 — Postmortem: various possible implementations of compare method

Durga Sir now explores seven different compare implementations using the same insertion sequence (10, 0, 15, 5, 20, 20) to show that output depends entirely on what compare returns.

Setup reminder:

- Without Comparator → JVM calls obj1.compareTo(obj2)
- With Comparator → JVM calls yourComparator.compare(obj1, obj2)
All examples below assume Comparator IS passed to TreeSet unless stated otherwise.

### Implementation 1: return I1.compareTo(I2)

```java
public int compare(Object obj1, Object obj2) {
    Integer I1 = (Integer) obj1;
    Integer I2 = (Integer) obj2;
    return I1.compareTo(I2);
}
```

Why? You are doing inside compare() exactly what JVM would do via compareTo() anyway.

### Implementation 2: return -(I1.compareTo(I2))

```java
return -(I1.compareTo(I2));
```

Trace example: compare(0, 10)

- 0.compareTo(10) returns negative (0 before 10 in natural order)
- Your minus sign flips it to positive
- JVM sees positive → 0 comes after 10 → descending behavior
Shortcut: One line for descending Integer sort instead of if-else blocks.

### Implementation 3: return I2.compareTo(I1) — reverse arguments

```java
return I2.compareTo(I1);
```

Trace example: compare(0, 10)

- Returns 10.compareTo(0) → positive (10 naturally after 0)
- JVM sees positive → 0 comes after 10 → descending
### Implementation 4: return -(I2.compareTo(I1)) — reverse + negate

```java
return -(I2.compareTo(I1));
```

One reversal (I2 vs I1) + minus sign = double reversal = natural order restored.

### Summary table: first four "sensible" implementations

### Implementation 5 (DANGEROUS): always return +1

return +1;   // always positive, no real comparison

This is insertion order, NOT sorted order!

- First element 10 inserted (no comparison)
- 0 compared → +1 → after 10
- 15 compared → +1 → after 0
- 5 compared → +1 → after 15
- 20 compared → +1 → after 5
- Second 20 compared → +1 → still inserted (compare says NOT duplicate!)
Trap: TreeSet allows "duplicate" 20 because your compare never returns 0. JVM doesn't decide duplicates — you do.

### Implementation 6 (DANGEROUS): always return -1

return -1;   // always negative

Sir uses term: reverse of insertion order.

Trace: each new element pushed to front because -1 always means "before."

### Implementation 7 (DANGEROUS): always return 0

return 0;   // always zero

- First 10 inserted (no comparison needed)
- Every subsequent add → compare returns 0 → JVM treats as duplicate → not inserted
- Only the first inserted element survives
Board note: Only first element will be inserted and all remaining are considered as duplicates.

## 58:47 — Master summary: seven implementations at a glance

## 58:56 — JVM dancing analogy (exam favorite)

Based on your return value, JVM can dance.

- Is it really duplicate? JVM doesn't worry.

- Is it really greater or less? JVM doesn't worry.

- You return positive → JVM places after.

- You return negative → JVM places before.

- You return zero → JVM skips as duplicate.

Central logic for customized sorting = inside compare method only.

## 1:01:04 — Heterogeneous objects note (preview)

Student question: What if we add different types of objects?

Sir's answer (brief — full rule in later session):

- If you add heterogeneous objects but your compare always returns +1, they will all be added (insertion-order behavior).
- TreeSet normally requires mutually comparable objects; Comparator gives you control, but wrong compare logic can break expectations.
- Detailed heterogeneous-object rules will be explained in upcoming examples.
## Quick reference tables

### Comparable vs Comparator (complete)

### compare() / compareTo() return contract

### TreeSet constructor decision tree

Need sorting in TreeSet?
│
├─ Default natural order (class's compareTo)
│   └─ TreeSet ts = new TreeSet();
│       JVM → compareTo()
│
└─ Custom order (your logic)
    └─ TreeSet ts = new TreeSet(new MyComparator());
        JVM → compare()

## OCJP / SCJP exam checklist

- [ ] State Comparator package: java.util (not java.lang)
- [ ] State Comparable package: java.lang
- [ ] Comparator defines 2 methods: compare and equals
- [ ] When implementing Comparator, implement compare() only — equals inherited from Object
- [ ] Write compare() prototype: public int compare(Object obj1, Object obj2)
- [ ] Negative = before, positive = after, zero = equal/duplicate
- [ ] Natural sorting → Comparable / compareTo(); Customized → Comparator / compare()
- [ ] TreeSet without Comparator → ascending for Integer
- [ ] TreeSet with descending Comparator → reverse of natural order
- [ ] return I1.compareTo(I2) inside compare = same as no Comparator
- [ ] return -(I1.compareTo(I2)) = descending shortcut
- [ ] return +1 always → insertion order (NOT sorted)
- [ ] return -1 always → reverse insertion order
- [ ] return 0 always → only first element survives
- [ ] JVM does NOT validate whether compare logic is "correct" — only trusts return value
- [ ] First element in TreeSet: no comparison performed
## Homework / self-test

- Write TreeSetDemo3 from memory: TreeSet + MyComparator + descending Integer sort.
- Trace compare(5, 10) and compare(5, 0) by hand for descending logic.
- Predict output for each of the seven compare implementations without running code.
- Explain why return +1 allows duplicate 20 in TreeSet but natural sorting does not.
- Convert descending if-else compare to one-line return -(I1.compareTo(I2)); and verify same output.
- Draw the BST after inserting 10, 0, 15, 5, 20 with descending Comparator.
- Write compare() for ascending String sort using return s1.compareTo(s2);.
### Self-test program template

```java
import java.util.*;

public class ComparatorSelfTest {
    public static void main(String[] args) {
        // Test 1: no Comparator
        TreeSet<Integer> natural = new TreeSet<>();
        for (int n : new int[]{10, 0, 15, 5, 20, 20})
            natural.add(n);
        System.out.println("Natural: " + natural);
        // Expected: [0, 5, 10, 15, 20]

        // Test 2: descending via negated compareTo
        TreeSet<Integer> desc = new TreeSet<>(new Comparator<Integer>() {
            public int compare(Integer a, Integer b) {
                return -(a.compareTo(b));
            }
        });
        for (int n : new int[]{10, 0, 15, 5, 20, 20})
            desc.add(n);
        System.out.println("Descending: " + desc);
        // Expected: [20, 15, 10, 5, 0]
    }
}
```

## Session closing

- This session is foundational for all remaining Comparator examples in the playlist.
- Sir will cover 5–6 more examples in follow-up videos (String sorting, multiple criteria, etc.).
- The one-hour investment on TreeSet + Integer + descending + seven compare styles is intentional — everything else builds on this.
- Take the method-call trace diagram and BST diagram from the board/screen into your notes alongside the code.
End of Video 144 study notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Position | 144 of 203 |  |  |
| Playlist | Core Java With OCJP/SCJP |  |  |
| Title | Collections Part-9 \ | \ | comparator |
| Instructor | Durga Sir |  |  |
| Duration | 1h 04m 58s |  |  |
| Video ID | uu9DHLJVRIs |  |  |
| URL | https://www.youtube.com/watch?v=uu9DHLJVRIs |  |  |
| Notes source | YouTube auto-captions |  |  |

| Interface | Package | Exam trap |
|---|---|---|
| Comparable | java.lang | Only one method: compareTo() |
| Comparator | java.util | NOT java.lang — always java.util |

| Interface | # Methods | Method names |
|---|---|---|
| Comparable | 1 | compareTo() |
| Comparator | 2 | compare() and equals() |

| Return value | Meaning |
|---|---|
| Negative | obj1 has to come before obj2 |
| Positive | obj1 has to come after obj2 |
| Zero | obj1 and obj2 are equal (duplicate for TreeSet) |

| Requirement | Go for | Package | Methods | Implementation burden |
|---|---|---|---|---|
| Default natural sorting order | Comparable | java.lang | 1 (compareTo) | Implement compareTo() in the class itself |
| Customized sorting order | Comparator | java.util | 2 (compare, equals) | Implement compare() only in a separate class |

| Constructor used | JVM calls | Sorting type | Output |
|---|---|---|---|
| new TreeSet() (no Comparator) | compareTo() | Default natural (ascending) | [0, 5, 10, 15, 20] |
| new TreeSet(new MyComparator()) | compare() | Customized (descending) | [20, 15, 10, 5, 0] |

| LINE ONE | JVM internally calls | Purpose |
|---|---|---|
| new TreeSet() | compareTo() on inserted objects | Default natural sorting order |
| new TreeSet(comparatorObj) | compare(obj1, obj2) on your Comparator | Customized sorting order |

| Condition | Meaning | obj1 position relative to obj2 | Return |
|---|---|---|---|
| I1 < I2 | obj1 is smaller | obj1 should come after obj2 | +1 (positive) |
| I1 > I2 | obj1 is bigger | obj1 should come before obj2 | -1 (negative) |
| I1 == I2 | equal | duplicate | 0 |

| Effect | Output |
|---|---|
| Same as default natural sorting | [0, 5, 10, 15, 20] ascending |

| Effect | Output |
|---|---|
| Negate natural order → descending | [20, 15, 10, 5, 0] |

| Effect | Output |
|---|---|
| Reversing arguments reverses order | [20, 15, 10, 5, 0] descending |

| Effect | Output |
|---|---|
| Two reversals = back to original | [0, 5, 10, 15, 20] ascending |

| # | Implementation | Output | Order name |
|---|---|---|---|
| 1 | return I1.compareTo(I2); | 0, 5, 10, 15, 20 | Ascending (natural) |
| 2 | return -(I1.compareTo(I2)); | 20, 15, 10, 5, 0 | Descending |
| 3 | return I2.compareTo(I1); | 20, 15, 10, 5, 0 | Descending |
| 4 | return -(I2.compareTo(I1)); | 0, 5, 10, 15, 20 | Ascending |

| Effect | Output |
|---|---|
| Every new element always goes after existing | [10, 0, 15, 5, 20, 20] |

| Effect | Output |
|---|---|
| Every new element always goes before existing | [20, 5, 15, 0, 10] |

| Effect | Output |
|---|---|
| First element inserted; all others treated as duplicates | [10] only |

| # | compare() body | Output for 10,0,15,5,20,20 | Order type |
|---|---|---|---|
| 1 | I1.compareTo(I2) | 0, 5, 10, 15, 20 | Ascending |
| 2 | -(I1.compareTo(I2)) | 20, 15, 10, 5, 0 | Descending |
| 3 | I2.compareTo(I1) | 20, 15, 10, 5, 0 | Descending |
| 4 | -(I2.compareTo(I1)) | 0, 5, 10, 15, 20 | Ascending |
| 5 | return +1; | 10, 0, 15, 5, 20, 20 | Insertion order |
| 6 | return -1; | 20, 5, 15, 0, 10 | Reverse insertion order |
| 7 | return 0; | 10 | Only first element |

| Feature | Comparable | Comparator |
|---|---|---|
| Package | java.lang | java.util |
| Methods | 1 (compareTo) | 2 (compare, equals) |
| Method to implement | compareTo() | compare() only |
| Sorting type | Default natural | Customized |
| Where logic lives | Inside the class itself | Separate Comparator class |
| TreeSet constructor | new TreeSet() | new TreeSet(comparatorObj) |
| JVM calls | compareTo() | compare() |

| Return | Placement rule | TreeSet meaning |
|---|---|---|
| Negative | obj1 before obj2 | Go left in BST |
| Positive | obj1 after obj2 | Go right in BST |
| Zero | obj1 equals obj2 | Duplicate — not inserted |
