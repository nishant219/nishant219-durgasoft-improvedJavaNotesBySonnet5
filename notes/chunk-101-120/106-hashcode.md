# Video 106 — `hashCode()` (Object class, Part 2)

## Video info

## Session overview

This is Part 2 of the java.lang / Object class series. In the previous session (Video 105), Durga Sir covered `toString()`. This session covers the second Object method: `hashCode()`.

Agenda for this video:

- What is hashCode()? (definition, myths, JVM usage)
- Why hashing matters — linear vs binary vs hashing search
- Default Object.hashCode() — native method, address-based generation
- Overriding hashCode() — proper vs improper ways
- Relation between toString() and hashCode()
- Three board demo programs with exact/predictable outputs
## 00:06 — Continuation from Part 1 (`toString()` done)

Durga Sir opens by recalling that in the last session the `java.lang` package and the first Object method — `toString()` — were covered. Some students may have found the theoretical portion a bit slow; this session moves to the second method, which he describes as shorter and easier: `hashCode()`.

## 00:46 — Opening question: What is hashCode?

Classroom poll: "What is hashCode of an object?"

Many students assume:

hashCode = address of the object

Durga Sir immediately challenges this with a logical trap:

- We can override hashCode() — e.g., return your phone number as hashCode.
- Can we override the address of an object? No.
- Therefore hashCode ≠ address. They are different concepts, not related.
## 01:52 — Java cannot expose object address or size

Key platform facts (interview-ready):

Why? Java is a programmer-friendly language, not a machine-friendly language. At the memory/machine level, Java deliberately hides low-level details.

- If you need address or object size → use C / C++ (low-level, machine-friendly languages).
- As a Java programmer, do not expect APIs for object address or size.
Takeaway: Because Java hides addresses, hashCode and object address are unrelated concepts.

## 02:56 — Definition of hashCode

Board definition:

For every object, JVM generates a unique number. That number is `hashCode`.

- hashCode does not represent the address of the object.
- It is a unique identifier number assigned/generated per object (by default, by JVM logic).
Immediate follow-up: Why does JVM need this unique number?

## 03:20 — Who uses hashCode? Hashing data structures

JVM uses hashCode when storing objects in hashing-related data structures:

### Bucket model (board diagram)

Durga Sir draws buckets numbered 1, 2, 3, … (conceptually infinite):

Bucket 1   Bucket 2   ...   Bucket 100   ...   Bucket 150
   |          |                    |                  |
 obj?       obj?              Student-1           Student-2

Insertion flow:

- Object wants to enter HashSet / HashMap / Hashtable.
- JVM asks: "Object, what is your hashCode?"
- Object answers, e.g., 100.
- JVM places the object in the 100th bucket.
- Second object with hashCode 150 → 150th bucket.
Rule: All objects in hashing collections are stored based on hashCode → which bucket they land in.

## 04:57 — Advantage: O(1) search (hashing = #1 search algorithm)

Advantage of hashCode-based storage:

- Search operation becomes very efficient — go directly to the correct bucket.
- HashMap / HashSet / Hashtable are the best choice when the frequent operation is search.
Durga Sir ranks search algorithms taught on the board:

### Linear search analogy [06:08–07:53]

- 1000 students → up to 1000 comparisons in worst case.
- Time grows linearly with number of elements → O(n).
- Simplest search, but worst performance for large data.
### Binary search analogy [08:13–10:35]

- Students sit in alphabetical order (sorted data required).
- Compare target with middle element:
- If R > middle → ignore first half, search second half.
- If R < middle → ignore second half.
- Each step eliminates half the remaining students → O(log n).
- Better than linear, but still depends on number of students.
### Hashing analogy [10:36–12:00]

- Ravi's hashCode = 100 → go directly to bucket 100.
- No need to check other buckets.
- Whether 10, 1000, or 1 crore elements — within ~1 step (conceptually O(1)).
- Most powerful search algorithm up to today: hashing.
## 12:02 — Board summary (hashCode fundamentals)

Durga Sir writes the consolidated board notes:

For every object → JVM generates a unique number → hashCode

hashCode ≠ address of object

JVM uses hashCode while saving objects into hashing-related
data structures (Hashtable, HashMap, HashSet, etc.)

Main advantage: search operation becomes easy
(most powerful search algorithm up to today = hashing)

## 16:27 — Default behavior: Object class hashCode()

Question: If we don't override hashCode, which method runs?

Answer: `Object` class `hashCode()` method.

### Declaration (from Object.java)

```java
public native int hashCode();
```

- `public` — accessible everywhere
- `native` — implemented in native (JVM/C) code, not Java source
- Return type `int`
### How Object.hashCode() generates the value [17:01–18:37]

- Object class hashCode is generated based on address of the object internally.
- Example thought experiment:
- Assume object address = 1024 (hypothetical — you cannot read this in Java).
- JVM runs some internal algorithm: 3 × 6 ÷ 2 × 10.75 ÷ 3.2 … → result e.g. 132.
- 132 is NOT the address 1024.
- The algorithm uses address as input, but the result is hashCode, not address.
Critical distinction:

## 18:40 — Overriding hashCode()

We can override hashCode() to return our own number instead of depending on Object's address-based algorithm.

Board note:

If you give the chance to Object class hashCode method,
it will generate hashCode based on address of the object.
It does NOT mean hashCode represents address.

Based on our requirement, we can override hashCode method
in our class to generate our own hashCode.

## 20:54 — Proper vs improper overriding

### Improper override — same hashCode for all objects [21:46–22:54]

```java
class Student {
    int rollNumber;
    String name;

    // IMPROPER — every Student returns 100
    public int hashCode() {
        return 100;
    }
}
```

Why improper?

- Student 1 → hashCode 100
- Student 2 → hashCode 100
- Student 3 → hashCode 100
- All objects share the same hashCode → violates uniqueness expectation.
### Proper override — unique hashCode per object [23:02–23:51]

```java
class Student {
    int rollNumber;
    String name;

    // PROPER — roll number differs per student
    public int hashCode() {
        return rollNumber;
    }
}
```

Why proper?

- Each student has a different roll number → different hashCode per object.
- Matches the spirit of JVM's default behavior (unique number per object).
## 24:00 — Why improper override breaks hashing [24:10–26:08]

Scenario: HashSet<Student> with improper hashCode() returning 100 for everyone.

HashSet internal buckets:
[...] [Bucket 100: Student1, Student2, Student3, ... thousands ...] [...]

- All students land in bucket 100 only.
- On search: JVM goes to bucket 100 → finds thousands of objects.
- Must ask each one: "Are you Ravi?" → degrades to linear search inside one bucket.
- Total hashing advantage is lost — search becomes very difficult.
Rule (board):

Overriding hashCode is proper if and only if we generate a unique / separate number (hashCode) for every object.

If all objects return the same hashCode → improper → spoils hashing algorithm performance.

## 26:33 — Board recap: overriding rules

Overriding hashCode method is said to be PROPER
if and only if for every object we generate a unique number as hashCode.

IMPROPER way:
  class Student {
      public int hashCode() { return 100; }  // same for all
  }
  → for all student objects, same number as hashCode

PROPER way:
  class Student {
      public int hashCode() { return rollNumber; }
  }
  → different hashCode for every object (because roll numbers differ)

## 31:21 — Relation: `toString()` vs `hashCode()` [31:21–35:45]

From Video 105, `Object.toString()` implementation:

```java
public String toString() {
    return getClass().getName() + "@" + Integer.toHexString(hashCode());
}
```

Student override example (from last class):

```java
class Student {
    String name;
    int rollNumber;

    public String toString() {
        return name + ".." + rollNumber;
    }
}
```

### Link between the two methods

Board heading: toString() vs hashCode()

If we give the chance to Object class toString method
  → it will internally call hashCode method.

If we are overriding toString method (our own implementation)
  → our toString may NOT call hashCode method.

This link is exam-critical — many trick questions depend on knowing which method chain executes.

## 36:04 — Board Demo Example 1: No overrides [36:10–39:16]

Code on board:

```java
class Test {
    int i;

    Test(int i) {
        this.i = i;
    }

    public static void main(String[] args) {
        Test t1 = new Test(10);
        Test t2 = new Test(100);
        System.out.println(t1);
        System.out.println(t2);
    }
}
```

### Which methods execute?

- Test class has no toString() override → Object version runs.
- Test class has no hashCode() override → Object native hashCode runs.
### Output

Exact output? NO — only format is guaranteed.

Test@<hex1>
Test@<hex2>

- Format: className + '@' + Integer.toHexString(hashCode())
- Hex values depend on JVM, memory layout, run — unpredictable.
- Example from live run (ASR): Test@12b6513, Test@4a5ab2 (illustrative only).
Exam answer: Cannot tell exact decimal/hex hashCode because Object.hashCode() executes (address-based, unknown).

## 39:17 — Board Demo Example 2: Override hashCode only [39:22–43:43]

Code on board:

```java
class Test {
    int i;

    Test(int i) {
        this.i = i;
    }

    public int hashCode() {
        return i;   // hashCode = instance variable value
    }

    public static void main(String[] args) {
        Test t1 = new Test(10);
        Test t2 = new Test(100);
        System.out.println(t1);
        System.out.println(t2);
    }
}
```

### Which methods execute?

Key insight: Even though we only overrode hashCode, Object.toString() still runs and uses our hashCode.

### Computing exact output

t1: hashCode = 10 → hex = Integer.toHexString(10) = `a`

t2: hashCode = 100 → hex = Integer.toHexString(100) = `64`

Test@a
Test@64

Hex quick reference (board): a=10, b=11, … f=15.

Durga Sir stresses: run on thousands of machines → same output every time, because the only variable part (hashCode) is fixed by our override.

## 43:43 — Board Demo Example 3: Override both toString and hashCode [43:53–49:55]

Code on board:

```java
class Test {
    int i;

    Test(int i) {
        this.i = i;
    }

    public String toString() {
        return i + "";   // NOT "return i;" alone — int vs String compile error
    }

    public int hashCode() {
        return i;
    }

    public static void main(String[] args) {
        Test t1 = new Test(10);
        Test t2 = new Test(100);
        System.out.println(t1);
        System.out.println(t2);
    }
}
```

### Compile trap: `return i;` in toString()

- toString() return type = `String`
- i is `int`
- return i; → compile error: incompatible types — int found, String required.
Fix (board):

```java
return i + "";           // string concatenation → String
// or
return String.valueOf(i);
// or
return Integer.toString(i);
```

### Which methods execute?

Important: hashCode() exists in the class but has no impact on println output in this example.

### Output

10
100

Not Test@a / Test@64 — because our toString returns just the int as String.

### Live IDE demonstration summary [47:02–49:55]

Durga Sir runs all three versions in IDE:

## 50:00 — Session snapshot (end board)

Final checklist — you should know:

- What is hashCode? Unique number per object (default: JVM-generated).
- hashCode ≠ address — Java cannot expose address.
- Who uses it? JVM / hashing collections (HashMap, HashSet, Hashtable).
- Advantage? O(1) search via buckets — hashing is the fastest search approach.
- Default impl? public native int hashCode() in Object — uses address internally, result is not address.
- Can we override? Yes — proper if unique per object; improper if same for all.
- toString vs hashCode? Object.toString() calls hashCode(); custom toString may not.
- Three demo patterns — know which methods run and whether output is exact or format-only.
## Complete runnable demo — all three examples

```java
// ========== Example 1: No overrides ==========
class Test1 {
    int i;
    Test1(int i) { this.i = i; }

    public static void main(String[] args) {
        Test1 t1 = new Test1(10);
        Test1 t2 = new Test1(100);
        System.out.println(t1);  // Test@<unpredictable hex>
        System.out.println(t2);  // Test@<unpredictable hex>
    }
}

// ========== Example 2: hashCode override only ==========
class Test2 {
    int i;
    Test2(int i) { this.i = i; }

    public int hashCode() { return i; }

    public static void main(String[] args) {
        Test2 t1 = new Test2(10);
        Test2 t2 = new Test2(100);
        System.out.println(t1);  // Test@a
        System.out.println(t2);  // Test@64
    }
}

// ========== Example 3: Both overridden ==========
class Test3 {
    int i;
    Test3(int i) { this.i = i; }

    public String toString() { return i + ""; }
    public int hashCode() { return i; }  // not used by println in this case

    public static void main(String[] args) {
        Test3 t1 = new Test3(10);
        Test3 t2 = new Test3(100);
        System.out.println(t1);  // 10
        System.out.println(t2);  // 100
    }
}
```

## Student improper/proper override demos

```java
import java.util.HashSet;

// IMPROPER — all students hash to bucket 100
class StudentBad {
    int rollNumber;
    StudentBad(int rollNumber) { this.rollNumber = rollNumber; }

    public int hashCode() { return 100; }  // WRONG: same for all

    public static void main(String[] args) {
        HashSet<StudentBad> set = new HashSet<>();
        set.add(new StudentBad(101));
        set.add(new StudentBad(102));
        set.add(new StudentBad(103));
        // All land in same bucket → search degrades
    }
}

// PROPER — unique hashCode per student
class StudentGood {
    int rollNumber;
    String name;

    StudentGood(int rollNumber, String name) {
        this.rollNumber = rollNumber;
        this.name = name;
    }

    public int hashCode() { return rollNumber; }  // unique per student

    public String toString() { return name + ".." + rollNumber; }

    public static void main(String[] args) {
        StudentGood s1 = new StudentGood(101, "Durga");
        StudentGood s2 = new StudentGood(102, "Ravi");
        System.out.println(s1);  // Durga..101  (custom toString, no hashCode in output)
        System.out.println(s2);  // Ravi..102
    }
}
```

## OCJP / SCJP exam traps

## Method dispatch decision tree (println)

System.out.println(obj)
        │
        ▼
   obj.toString()
        │
        ├─ Our class overrides toString?
        │     YES → our toString() executes
        │            └─ Does OUR code call hashCode()? Only if we wrote it.
        │
        └─ NO → Object.toString()
                  └─ ALWAYS calls hashCode()
                        ├─ Our class overrides hashCode? → our hashCode()
                        └─ else → Object.hashCode() (native, unpredictable int)

## Full transcript coverage (timestamp index)

## ASR decode notes (Whisper STT corrections)

## Quick reference card

hashCode()
├── Definition: unique int per object (default JVM-generated)
├── NOT equal to object memory address
├── Used by: HashMap, HashSet, Hashtable (bucket placement)
├── Default: Object.public native int hashCode() — address used internally
├── Override rules:
│     PROPER   → different hashCode per object (e.g., rollNumber)
│     IMPROPER → same hashCode for all (e.g., return 100)
└── vs toString():
      Object.toString() → calls hashCode()
      Custom toString() → may NOT call hashCode()

End of Video 106 notes — java.lang Part-2, Object.hashCode()

## Tables (placement lost -- re-place these in context)

| Field | Value |
|---|---|
| Title | Core Java With OCJP/SCJP: java.lang.package Part-2 — object class — Hashcode() |
| Playlist | Core Java With OCJP/SCJP |
| Position | 106 of 203 |
| Series | java.lang.package |
| Topic | Object class — hashCode(); relation with toString() |
| Instructor | Durga Sir |
| Duration | 51m 49s |
| Video ID | r6G5Pz0yMH4 |
| Watch | https://www.youtube.com/watch?v=r6G5Pz0yMH4 |
| Notes source | Local Whisper STT |

| Question | Answer in Java |
|---|---|
| What is the address of an object? | Impossible to find |
| What is the size of an object? | Impossible to find |

| Data structure | Package |
|---|---|
| Hashtable | legacy, synchronized |
| HashMap | most common map |
| HashSet | set backed by HashMap |

| Algorithm | How it finds "Ravi" in class | Time complexity |
|---|---|---|
| Linear search | Ask every student one by one: "Are you Ravi?" | O(n) |
| Binary search | Students sorted alphabetically; compare with middle; halve each step | O(log n) |
| Hashing | Ask Ravi his hashCode (e.g., 100); go directly to bucket 100 | O(1) |

| Statement | True/False |
|---|---|
| Object.hashCode() uses address internally | True |
| hashCode represents / equals address | False |
| If we don't override, hashCode comes from Object's native impl | True |

| Scenario | Which toString()? | Does it call hashCode()? |
|---|---|---|
| No override in our class | Object.toString() | Yes — internally calls hashCode() |
| We override toString() in our class | Our toString() | May not call hashCode() — depends on our code |

| Call | Method chain |
|---|---|
| System.out.println(t1) | t1.toString() → Object.toString() → internally Object.hashCode() |
| Same for t2 | Object.toString() → Object.hashCode() |

| Step | What happens |
|---|---|
| println(t1) | Calls t1.toString() |
| toString | Still Object.toString() (not overridden) |
| Inside Object.toString() | Calls hashCode() |
| hashCode | Test class hashCode() — because Test overrides it |

| Call | Method |
|---|---|
| println(t1) | Test.toString() — our override |
| hashCode() | NOT called — our toString does not invoke hashCode |

| Version | Output (representative) |
|---|---|
| Example 1 — no overrides | Test@12b6513, Test@4a5ab2 (hex varies) |
| Example 2 — hashCode only | Test@a, Test@64 |
| Example 3 — both overridden | 10, 100 |

| Trap question | Correct reasoning |
|---|---|
| "hashCode is object address" | False — can override hashCode; cannot override address |
| "Can we find object size in Java?" | No |
| print object with no toString override | Object.toString() → calls hashCode() |
| Override hashCode only, print object | Object.toString() still runs; uses your hashCode → predictable hex |
| Override toString only | Your toString runs; hashCode may not be called |
| return i; inside toString() when i is int | Compile error — need String |
| Same hashCode for all objects | Improper — destroys hashing performance |
| Time complexity of hashing search | O(1) (ideal case; collisions add cost) |
| Object.hashCode declaration | public native int hashCode() |

| Time | Topic |
|---|---|
| 00:06 | Recap: java.lang Part-1, toString() completed |
| 00:29 | Introduce hashCode() as second Object method |
| 00:46 | Poll: hashCode = address? (myth busting) |
| 01:20 | Can override hashCode; cannot override address |
| 01:52 | Java hides address & object size; use C/C++ for machine-level info |
| 02:56 | Definition: JVM unique number per object = hashCode |
| 03:20 | Why needed: hashing data structures |
| 03:42 | Hashtable, HashMap, HashSet |
| 04:03 | Bucket insertion model |
| 04:57 | Advantage: efficient search |
| 05:53 | Linear search O(n) — classroom analogy |
| 08:13 | Binary search O(log n) — sorted names analogy |
| 10:36 | Hashing O(1) — direct bucket jump |
| 12:02 | Board summary of hashCode definition & usage |
| 16:27 | Default: Object.hashCode() when not overridden |
| 16:48 | Declaration: public native int hashCode() |
| 17:01 | Native impl uses address in algorithm; result ≠ address |
| 18:40 | Can override to generate own hashCode |
| 20:54 | Proper vs improper overriding introduced |
| 21:46 | Improper: return 100 for all Student objects |
| 23:02 | Proper: return rollNumber |
| 24:10 | HashSet collision demo — all in bucket 100 |
| 26:08 | Same hashCode spoils hashing; search becomes hard |
| 31:21 | toString vs hashCode relation |
| 31:38 | Object.toString() source: getClass().getName() + "@" + hex(hashCode()) |
| 33:57 | Object.toString calls hashCode; custom toString may not |
| 36:04 | Example 1: Test class, no overrides |
| 37:29 | Object.toString + Object.hashCode; output format only |
| 39:17 | Example 2: override hashCode return i |
| 41:10 | Object.toString still; Test.hashCode used |
| 42:00 | Exact output: Test@a, Test@64 |
| 43:43 | Example 3: override both |
| 44:28 | return i compile error in toString |
| 44:54 | Fix: i + "" |
| 46:02 | Test.toString runs; hashCode not called |
| 46:45 | Output: 10, 100 |
| 47:02 | Live IDE run of all three examples |
| 50:07 | Final snapshot / wrap-up |

| Heard (Whisper) | Intended |
|---|---|
| Jawadhat Lang / javal | java.lang |
| has scored / ash code / ascord / escort | hashCode |
| address / a drasa / nathima | address |
| mission friendly | machine friendly |
| CRC++ | C / C++ |
| Javiyam / Jovie nyam | JVM |
| HASHESET / has set | HashSet |
| SETCH / such | search |
| Ashing / atima hashing | hashing |
| linear set / state gel | linear search |
| binary set / bhai | binary search |
| Adraf / a draw of n | O(n) |
| lag m base lagardhamic | O(log n) |
| a draft one | O(1) |
| twisting / two-sync / 2S | toString |
| Uchitushin / Uchmetan | Object.toString |
| Uchash code / Escort | hashCode |
| warrior main | void main |
| aaksa / A.A.A.C.A | args |
| RETUM / RETAM / written | return |
| S4P / print Lm | System.out.println |
| tested the rate / test at the rate | Test@ (className@hex in toString output) |
| XR is one / x-adish | hexadecimal |
| compalt / validator | compiler / valid |
| left hand right | classroom humor (wrong answer) |
