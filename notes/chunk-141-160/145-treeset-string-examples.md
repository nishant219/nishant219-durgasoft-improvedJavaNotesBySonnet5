# Video 145 — Collections Part-10: String Object in TreeSet — Comparator Examples Marathon

## Video info

## Session overview

This is the marathon Comparator examples session that Video 144 explicitly promised. At the end of Video 144, Durga Sir stated:

"Just for the first example like this we are going to cover another five to six examples so that you can get much clarity."

Video 145 delivers that entire block. Where Video 144 spent ~1 hour on one flagship example (TreeSet + Integer + descending order + seven compare implementations), Video 145 applies the same mental model across String natural sorting, multiple String Comparators, StringBuffer (non-Comparable), custom Person/Employee objects, inter-conversion, heterogeneous traps, and null rules with/without Comparator.

Exam mantra from Sir: If you understood Video 144's Integer descending example and the "JVM is blind" analogy, every program in this session is a variation on the same theme. If you missed Video 144, go back before continuing.

### What this lecture covers

- Recap — TreeSet + String + default natural sorting (Unicode, capitals before lowercase, duplicates via compareTo returning 0)
- SCJP-style MCQ — "one", "two", "three", "four" → output [four, one, three, two] (not alphabetical!)
- Insertion order vs sorted output — live demos proving TreeSet never preserves insertion order
- String Comparator examples — reverse alphabetical, sort by length, sort by last character
- Multiple compare() implementation styles — +1/-1/0, subtraction trick, Integer.compare()
- TreeSet with StringBuffer using Comparator — fixing the ClassCastException from Video 143
- TreeSet with custom Person/Employee + Comparator by name, by id
- Inter-conversion — ArrayList → TreeSet via TreeSet(Collection c) constructor
- Mixed Integer + String heterogeneous → ClassCastException (with and without Comparator)
- Null in TreeSet — with vs without Comparator (Java 7+ rules)
- Interview questions from this entire Comparator block (143–145)
### Connection to prior sessions

## 00:04 — Opening recap: why we need more examples

Durga Sir opens by reinforcing the thumb rule from Videos 143–144:

If default natural sorting order is not available, OR if we are not satisfied with default natural sorting order, then we can go for customized sorting by using `Comparator`.

Two scenarios recap:

LINE ONE theory (memorize permanently):

Sir's message: Video 144 gave you the engine (Comparator + compare + JVM blind). Video 145 gives you six different cars (String, StringBuffer, Person, ArrayList conversion, etc.) — same engine, different payloads.

## 05:12 — Recap: TreeSet + String + default natural sorting

### Program: TreeSetDemo String recap

```java
import java.util.*;

class TreeSetStringRecap {
    public static void main(String[] args) {
        TreeSet t = new TreeSet();   // LINE ONE — no Comparator
        t.add("A");
        t.add("A");   // duplicate — compareTo returns 0 → ignored
        t.add("B");
        t.add("Z");
        t.add("L");
        System.out.println(t);
    }
}
```

Constructor used: No-argument → default natural sorting order.

Object type: String — implements Comparable<String> → valid for natural sorting.

Insertion sequence: A, A, B, Z, L

Output: [A, B, L, Z]

Why NOT `[A, A, B, Z, L]`? TreeSet does NOT preserve insertion order. Elements appear in sorting order (in-order traversal of internal balanced tree).

### Unicode / lexicographic sorting — exam critical

String's natural order (compareTo) is lexicographic based on Unicode values, NOT "human alphabetical intuition."

Board rule: Capital letters come before lowercase letters because 65–90 < 97–122.

### Demo: capitals before lowercase

```java
import java.util.*;

class TreeSetCaseDemo {
    public static void main(String[] args) {
        TreeSet t = new TreeSet();
        t.add("a");   // lowercase — Unicode 97
        t.add("A");   // capital  — Unicode 65
        t.add("b");
        t.add("B");
        System.out.println(t);
    }
}
```

Output: [A, B, a, b]

NOT [A, a, B, b] — comparison is character-by-character on Unicode values; all capitals (65–90) precede all lowercase (97–122).

### Duplicate detection via compareTo

When compareTo() returns 0, TreeSet treats objects as equal for sorting purposes → duplicate → not inserted (silently ignored, no exception).

System.out.println("A".compareTo("A"));  // 0 → duplicate

Internal mechanism (from Video 143):

- obj1 = object being inserted (new element)
- obj2 = object already in tree (existing element)
- compareTo returns 0 → JVM stops → duplicate not inserted
### compareTo quick reference

```java
class CompareToQuickRef {
    public static void main(String[] args) {
        System.out.println("A".compareTo("Z"));   // negative (-25)
        System.out.println("Z".compareTo("K"));   // positive (+1)
        System.out.println("A".compareTo("A"));   // zero (0)
        // System.out.println("A".compareTo(null)); // NullPointerException
    }
}
```

Sign matters, magnitude does not: -25 and -1 both mean "before."

## 18:30 — SCJP-style MCQ: one two three four

This is one of the most famous TreeSet String exam questions in the Durga Sir / OCJP canon.

### The question

```java
import java.util.*;

class TreeSetMCQ {
    public static void main(String[] args) {
        TreeSet t = new TreeSet();
        t.add("one");
        t.add("two");
        t.add("three");
        t.add("four");
        System.out.println(t);
    }
}
```

What is the output?

### Student trap

Most students pick B — they assume "alphabetical order" means the words sorted as humans expect: one, two, three, four.

Correct answer: A — `[four, one, three, two]`

### Why? Character-by-character Unicode comparison

TreeSet uses String.compareTo() — lexicographic order on each character position, left to right.

Step 1 — sort by first character:

- 'f' (102) → "four" comes first
- 'o' (111) → "one" comes second
- 't' (116) → "three" and "two" tie on first character
Step 2 — break tie between "three" and "two":

- Compare second character: 'h' (104) vs 'w' (119)
- 104 < 119 → "three" before "two"
Final sorted order: [four, one, three, two]

### Trace table

### Sir's board note

Never assume English dictionary word order in TreeSet String questions. Always trace Unicode character-by-character.

### Variation MCQ — with duplicates

TreeSet t = new TreeSet();
t.add("one");
t.add("one");   // duplicate
t.add("two");
System.out.println(t);  // [one, two] — only one "one"

### Variation MCQ — mixed case

TreeSet t = new TreeSet();
t.add("Apple");
t.add("apple");
t.add("Banana");
System.out.println(t);  // [Apple, Banana, apple]

Capitals before lowercase: 'A'(65) < 'B'(66) < 'a'(97).

## 28:45 — Insertion order vs sorted output (extended demo)

Durga Sir emphasizes repeatedly: TreeSet is NOT LinkedHashSet.

### Demo: insertion order completely ignored

```java
import java.util.*;

class InsertionVsSortedDemo {
    public static void main(String[] args) {
        TreeSet t = new TreeSet();
        System.out.println("Adding in order: Z, A, M, B, Y");
        t.add("Z");
        t.add("A");
        t.add("M");
        t.add("B");
        t.add("Y");
        System.out.println("TreeSet contents: " + t);
        // Output: [A, B, M, Y, Z] — sorted, NOT insertion order
    }
}
```

Output: [A, B, M, Y, Z]

### Side-by-side: TreeSet vs LinkedHashSet vs HashSet

```java
import java.util.*;

class SetComparisonDemo {
    public static void main(String[] args) {
        String[] input = {"Z", "A", "M", "B", "Y"};

        TreeSet ts = new TreeSet();
        LinkedHashSet lhs = new LinkedHashSet();
        HashSet hs = new HashSet();

        for (String s : input) {
            ts.add(s);
            lhs.add(s);
            hs.add(s);
        }

        System.out.println("TreeSet:       " + ts);  // [A, B, M, Y, Z] sorted
        System.out.println("LinkedHashSet: " + lhs); // [Z, A, M, B, Y] insertion order
        System.out.println("HashSet:       " + hs);  // unpredictable order
    }
}
```

### Internal BST trace for Z, A, M, B, Y

Using natural String order:

- Add "Z" → root (no comparison)
- Add "A" → compare "A" with "Z" → negative → left of Z
- Add "M" → compare with "Z" → negative → left; compare with "A" → positive → right of A
- Add "B" → navigates tree via compareTo calls
- Add "Y" → navigates tree via compareTo calls
In-order traversal (Left → Root → Right): A, B, M, Y, Z

Output confirms: sorting order, not insertion order.

## 38:20 — Comparator Example 1: Reverse alphabetical String sort

### Problem statement

Insert String objects into TreeSet where sorting order is reverse alphabetical (Z → A).

Default natural order gives A → Z. We are not satisfied → go for Comparator.

### Solution — if-else style (same pattern as Integer descending from Video 144)

```java
import java.util.*;

class ReverseAlphaComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        String s1 = (String) obj1;
        String s2 = (String) obj2;

        if (s1.compareTo(s2) > 0)       // s1 alphabetically after s2
            return -1;                   // s1 should come BEFORE s2 (reverse)
        else if (s1.compareTo(s2) < 0)  // s1 alphabetically before s2
            return +1;                   // s1 should come AFTER s2 (reverse)
        else
            return 0;                    // equal → duplicate
    }
}
```

### Full program

```java
import java.util.*;

class TreeSetReverseAlpha {
    public static void main(String[] args) {
        TreeSet t = new TreeSet(new ReverseAlphaComparator());  // LINE ONE with Comparator
        t.add("A");
        t.add("Z");
        t.add("L");
        t.add("B");
        t.add("M");
        System.out.println(t);
    }
}

class ReverseAlphaComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        String s1 = (String) obj1;
        String s2 = (String) obj2;
        if (s1.compareTo(s2) > 0)
            return -1;
        else if (s1.compareTo(s2) < 0)
            return +1;
        else
            return 0;
    }
}
```

Output: [Z, M, L, B, A]

### Shortcut implementations (from Video 144 pattern)

```java
// Style 1: negate natural compareTo
return -(s1.compareTo(s2));

// Style 2: reverse arguments
return s2.compareTo(s1);

// Style 3: negate reversed arguments (double reversal = natural again — NOT what we want)
return -(s2.compareTo(s1));  // this gives natural order, NOT reverse
```

Best one-liner for reverse alphabetical:

```java
class ReverseAlphaShort implements Comparator {
    public int compare(Object o1, Object o2) {
        String s1 = (String) o1;
        String s2 = (String) o2;
        return s2.compareTo(s1);   // reverse arguments
    }
}
```

### Trace: inserting "A" then "Z" with reverse Comparator

- Add "A" → root (no comparison)
- Add "Z" → compare("Z", "A"):
- s1="Z", s2="A"
- s2.compareTo(s1) = "A".compareTo("Z") = negative
- JVM: negative → Z goes before A
- Final output: [Z, A] for just these two
JVM is blind — it only sees the return value, not "Z is after A alphabetically."

## 48:10 — Comparator Example 2: Sort String by length

### Problem statement

Insert String objects into TreeSet sorted by length (shortest first). If two strings have the same length, break tie by natural alphabetical order.

### Demo data

Input: "Java", "C", "Python", "Go", "C"

Expected output by length: "C"(1), "Go"(2), "Java"(4), "Python"(6)

### Implementation 1: if-else with +1/-1/0

```java
import java.util.*;

class LengthComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        String s1 = (String) obj1;
        String s2 = (String) obj2;

        if (s1.length() < s2.length())
            return -1;    // shorter comes first
        else if (s1.length() > s2.length())
            return +1;    // longer comes after
        else
            return s1.compareTo(s2);  // same length → alphabetical tie-break
    }
}
```

### Full program

```java
import java.util.*;

class TreeSetSortByLength {
    public static void main(String[] args) {
        TreeSet t = new TreeSet(new LengthComparator());
        t.add("Java");
        t.add("C");
        t.add("Python");
        t.add("Go");
        t.add("C");       // duplicate of "C" → compare returns 0 → not inserted
        System.out.println(t);
    }
}

class LengthComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        String s1 = (String) obj1;
        String s2 = (String) obj2;
        if (s1.length() < s2.length())
            return -1;
        else if (s1.length() > s2.length())
            return +1;
        else
            return s1.compareTo(s2);
    }
}
```

Output: [C, Go, Java, Python]

### Implementation 2: subtraction trick

```java
class LengthComparatorSubtract implements Comparator {
    public int compare(Object obj1, Object obj2) {
        String s1 = (String) obj1;
        String s2 = (String) obj2;
        int diff = s1.length() - s2.length();
        return (diff != 0) ? diff : s1.compareTo(s2);
    }
}
```

How subtraction trick works:

Warning: Subtraction trick works safely for small int values like length. For large integer differences that overflow int range, prefer Integer.compare().

### Implementation 3: Integer.compare (Java 7+ — recommended)

```java
class LengthComparatorIntegerCompare implements Comparator {
    public int compare(Object obj1, Object obj2) {
        String s1 = (String) obj1;
        String s2 = (String) obj2;
        int cmp = Integer.compare(s1.length(), s2.length());
        return (cmp != 0) ? cmp : s1.compareTo(s2);
    }
}
```

Why Integer.compare is preferred:

- No overflow risk (subtraction of large ints can overflow)
- Readable intent
- Returns -1, 0, or +1 consistently
### Descending by length variation

```java
class LengthDescendingComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        String s1 = (String) obj1;
        String s2 = (String) obj2;
        return Integer.compare(s2.length(), s1.length());  // reverse: longer first
    }
}
```

## 58:40 — Comparator Example 3: Sort String by last character

### Problem statement

Sort strings by their last character. If last characters are equal, use natural order as tie-breaker.

### Demo

Input: "cat", "dog", "bat", "rat"

Last characters: 't', 'g', 't', 't'

Sorted by last char: "dog"('g'), then "bat"/"cat"/"rat"(all end in 't') → tie-break alphabetically among bat, cat, rat.

### Implementation 1: if-else style

```java
import java.util.*;

class LastCharComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        String s1 = (String) obj1;
        String s2 = (String) obj2;

        char c1 = s1.charAt(s1.length() - 1);
        char c2 = s2.charAt(s2.length() - 1);

        if (c1 < c2)
            return -1;
        else if (c1 > c2)
            return +1;
        else
            return s1.compareTo(s2);
    }
}
```

### Full program

```java
import java.util.*;

class TreeSetSortByLastChar {
    public static void main(String[] args) {
        TreeSet t = new TreeSet(new LastCharComparator());
        t.add("cat");
        t.add("dog");
        t.add("bat");
        t.add("rat");
        System.out.println(t);
    }
}

class LastCharComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        String s1 = (String) obj1;
        String s2 = (String) obj2;
        char c1 = s1.charAt(s1.length() - 1);
        char c2 = s2.charAt(s2.length() - 1);
        if (c1 < c2)
            return -1;
        else if (c1 > c2)
            return +1;
        else
            return s1.compareTo(s2);
    }
}
```

Output: [dog, bat, cat, rat]

- "dog" last char 'g' (103) — smallest
- "bat", "cat", "rat" all end in 't' (116) — tie-break: bat < cat < rat
### Implementation 2: subtraction trick on char (promoted to int)

```java
class LastCharComparatorSubtract implements Comparator {
    public int compare(Object obj1, Object obj2) {
        String s1 = (String) obj1;
        String s2 = (String) obj2;
        char c1 = s1.charAt(s1.length() - 1);
        char c2 = s2.charAt(s2.length() - 1);
        int diff = c1 - c2;
        return (diff != 0) ? diff : s1.compareTo(s2);
    }
}
```

Note: char - char promotes to int automatically in Java.

### Implementation 3: Integer.compare on char values

```java
class LastCharComparatorIntegerCompare implements Comparator {
    public int compare(Object obj1, Object obj2) {
        String s1 = (String) obj1;
        String s2 = (String) obj2;
        char c1 = s1.charAt(s1.length() - 1);
        char c2 = s2.charAt(s2.length() - 1);
        int cmp = Integer.compare(c1, c2);
        return (cmp != 0) ? cmp : s1.compareTo(s2);
    }
}
```

## 1:08:15 — compare() implementation styles master table (String edition)

Durga Sir revisits the seven styles from Video 144, now applied to String length sorting.

Given insertion order: "Java", "C", "Python", "Go"

### Dangerous implementations — Sir's warnings carry forward

```java
// DANGEROUS: always +1 → insertion order, duplicates allowed
public int compare(Object o1, Object o2) { return +1; }

// DANGEROUS: always -1 → reverse insertion order
public int compare(Object o1, Object o2) { return -1; }

// DANGEROUS: always 0 → only first element survives
public int compare(Object o1, Object o2) { return 0; }
```

JVM never validates your logic. If you return +1 for equal strings, TreeSet will store both — breaking the Set contract in practice.

### Style comparison: when to use which

## 1:15:30 — TreeSet with StringBuffer using Comparator

### Problem (from Video 143 recap)

TreeSet t = new TreeSet();  // no Comparator
t.add(new StringBuffer("A"));
// ClassCastException: StringBuffer cannot be cast to Comparable

StringBuffer is homogeneous-safe but NOT Comparable. Default natural sorting fails.

### Solution: supply Comparator

Since StringBuffer lacks compareTo(), we define comparison logic externally.

```java
import java.util.*;

class TreeSetStringBufferDemo {
    public static void main(String[] args) {
        TreeSet t = new TreeSet(new StringBufferComparator());  // LINE ONE with Comparator
        t.add(new StringBuffer("Z"));
        t.add(new StringBuffer("A"));
        t.add(new StringBuffer("L"));
        t.add(new StringBuffer("B"));
        System.out.println(t);
    }
}

class StringBufferComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        StringBuffer sb1 = (StringBuffer) obj1;
        StringBuffer sb2 = (StringBuffer) obj2;
        // Convert to String for comparison, or use StringBuffer's content
        return sb1.toString().compareTo(sb2.toString());
    }
}
```

Output: [A, B, L, Z]

### Key points

### Alternative: compare StringBuffer content without toString()

```java
class StringBufferComparatorV2 implements Comparator {
    public int compare(Object obj1, Object obj2) {
        StringBuffer sb1 = (StringBuffer) obj1;
        StringBuffer sb2 = (StringBuffer) obj2;
        int len1 = sb1.length();
        int len2 = sb2.length();
        int min = Math.min(len1, len2);
        for (int i = 0; i < min; i++) {
            char c1 = sb1.charAt(i);
            char c2 = sb2.charAt(i);
            if (c1 != c2)
                return c1 - c2;
        }
        return len1 - len2;
    }
}
```

Note: This manual approach mirrors what String.compareTo does internally. Using toString().compareTo() is simpler and sufficient for exams.

### StringBuilder — same story

StringBuilder also does NOT implement Comparable. Identical Comparator approach required.

## 1:22:45 — TreeSet with custom Person/Employee objects

### Problem statement

Create a Person class with name and id. Insert Person objects into TreeSet sorted by name (alphabetical). Then repeat with a different Comparator sorted by id (numerical).

### Person class

```java
class Person {
    String name;
    int id;

    Person(String name, int id) {
        this.name = name;
        this.id = id;
    }

    public String toString() {
        return name + "-" + id;
    }
}
```

Person does NOT implement Comparable — customized sorting via Comparator only.

### Comparator 1: sort by name

```java
import java.util.*;

class TreeSetPersonByName {
    public static void main(String[] args) {
        TreeSet t = new TreeSet(new PersonNameComparator());
        t.add(new Person("Durga", 101));
        t.add(new Person("Ravi", 103));
        t.add(new Person("Anil", 102));
        t.add(new Person("Shiva", 104));
        System.out.println(t);
    }
}

class Person {
    String name;
    int id;
    Person(String name, int id) { this.name = name; this.id = id; }
    public String toString() { return name + "-" + id; }
}

class PersonNameComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        Person p1 = (Person) obj1;
        Person p2 = (Person) obj2;
        return p1.name.compareTo(p2.name);
    }
}
```

Output: [Anil-102, Durga-101, Ravi-103, Shiva-104]

Sorted by name alphabetically. IDs are irrelevant for this Comparator.

### Comparator 2: sort by id (numerical ascending)

```java
import java.util.*;

class TreeSetPersonById {
    public static void main(String[] args) {
        TreeSet t = new TreeSet(new PersonIdComparator());
        t.add(new Person("Durga", 101));
        t.add(new Person("Ravi", 103));
        t.add(new Person("Anil", 102));
        t.add(new Person("Shiva", 104));
        System.out.println(t);
    }
}

class PersonIdComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        Person p1 = (Person) obj1;
        Person p2 = (Person) obj2;
        return Integer.compare(p1.id, p2.id);
        // or: return p1.id - p2.id;  (subtraction trick — safe for small ids)
    }
}
```

Output: [Durga-101, Anil-102, Ravi-103, Shiva-104]

Sorted by id numerically.

### Same data, different Comparator → different output

This proves: TreeSet sort order is entirely determined by the Comparator you pass at LINE ONE.

### Employee example — sort by salary descending

```java
import java.util.*;

class TreeSetEmployeeBySalary {
    public static void main(String[] args) {
        TreeSet t = new TreeSet(new EmployeeSalaryComparator());
        t.add(new Employee("Durga", 50000));
        t.add(new Employee("Ravi", 75000));
        t.add(new Employee("Anil", 60000));
        System.out.println(t);
    }
}

class Employee {
    String name;
    int salary;
    Employee(String name, int salary) { this.name = name; this.salary = salary; }
    public String toString() { return name + "-" + salary; }
}

class EmployeeSalaryComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        Employee e1 = (Employee) obj1;
        Employee e2 = (Employee) obj2;
        // descending salary: higher salary comes first
        return Integer.compare(e2.salary, e1.salary);
    }
}
```

Output: [Ravi-75000, Anil-60000, Durga-50000]

### Duplicate Person with same name

t.add(new Person("Anil", 102));
t.add(new Person("Anil", 999));  // same name, different id
// PersonNameComparator: name.compareTo → 0 → DUPLICATE → second not inserted

Critical: With name-based Comparator, two persons with same name are duplicates even if ids differ. If you want uniqueness by id, sort by id or use a composite Comparator.

### Composite Comparator (sort by name, then by id)

```java
class PersonNameThenIdComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        Person p1 = (Person) obj1;
        Person p2 = (Person) obj2;
        int cmp = p1.name.compareTo(p2.name);
        return (cmp != 0) ? cmp : Integer.compare(p1.id, p2.id);
    }
}
```

## 1:32:10 — Inter-conversion: ArrayList to TreeSet

### Constructor 3 recap (from Video 143)

```java
TreeSet t = new TreeSet(Collection c);
```

- Used for inter-conversion between collection objects
- Source collection (e.g., ArrayList) has no inherent sorting
- TreeSet applies default natural sorting order to those elements
### Demo program

```java
import java.util.*;

class ArrayListToTreeSetDemo {
    public static void main(String[] args) {
        ArrayList al = new ArrayList();
        al.add("Z");
        al.add("A");
        al.add("M");
        al.add("B");
        al.add("Y");

        System.out.println("ArrayList (insertion order): " + al);
        // [Z, A, M, B, Y]

        TreeSet ts = new TreeSet(al);   // Constructor 3 — inter-conversion
        System.out.println("TreeSet (sorted): " + ts);
        // [A, B, M, Y, Z]
    }
}
```

Output:

ArrayList (insertion order): [Z, A, M, B, Y]
TreeSet (sorted): [A, B, M, Y, Z]

### Key observations

### Inter-conversion with Integer

ArrayList al = new ArrayList();
al.add(10);
al.add(5);
al.add(20);
al.add(0);

TreeSet ts = new TreeSet(al);
System.out.println(ts);  // [0, 5, 10, 20] — natural ascending

### Inter-conversion with custom Comparator

If you want sorted-by-length when converting from ArrayList:

ArrayList al = new ArrayList();
al.add("Java");
al.add("C");
al.add("Python");

TreeSet ts = new TreeSet(new LengthComparator());
ts.addAll(al);   // addAll also works
System.out.println(ts);  // [C, Java, Python]

Note: new TreeSet(al) uses natural order only. For custom order, create TreeSet with Comparator first, then addAll(al).

### Inter-conversion failure — non-Comparable elements

ArrayList al = new ArrayList();
al.add(new StringBuffer("A"));
al.add(new StringBuffer("Z"));

TreeSet ts = new TreeSet(al);  // ClassCastException at runtime

StringBuffer in ArrayList is fine (ArrayList allows anything). TreeSet constructor tries natural sorting → fails.

## 1:38:50 — Heterogeneous objects: Integer + String → ClassCastException

### Rule (from Video 143 — reinforced here)

TreeSet does NOT allow heterogeneous objects when using default natural sorting.

Only TreeSet and TreeMap enforce this in the entire Collections Framework.

### Demo: natural sorting — ClassCastException

```java
import java.util.*;

class HeterogeneousTreeSetDemo {
    public static void main(String[] args) {
        TreeSet t = new TreeSet();   // no Comparator — natural sorting
        t.add("A");
        t.add("B");
        t.add(10);   // Integer after Strings → ClassCastException
        System.out.println(t);
    }
}
```

Exception:

Exception in thread "main" java.lang.ClassCastException:
    java.lang.Integer cannot be cast to java.lang.String

Why? JVM tries to compare Integer with String using compareTo — types are incompatible.

### Reverse order also fails

TreeSet t = new TreeSet();
t.add(10);
t.add("A");   // ClassCastException — Integer already in tree

### With Comparator — still problematic

TreeSet t = new TreeSet(new MyComparator());
t.add("A");
t.add(10);   // MyComparator must cast both to same type — still CCE or logic error

Even with Comparator, if your compare method casts to String, Integer will fail at cast. Heterogeneous objects are fundamentally incompatible with TreeSet's comparison model unless Comparator explicitly handles multiple types (never done in exam questions).

### Preview from Video 144: return +1 always

Sir previewed: if compare always returns +1, heterogeneous objects can all be added:

```java
class AlwaysPlusOne implements Comparator {
    public int compare(Object o1, Object o2) { return +1; }
}

TreeSet t = new TreeSet(new AlwaysPlusOne());
t.add("A");
t.add(10);
t.add(new Person("X", 1));
System.out.println(t);  // [A, 10, X-1] — insertion order, NOT sorted
```

This is NOT valid sorted TreeSet usage — it's a trick question demonstrating JVM blindness. Normal TreeSet requires homogeneous, mutually comparable objects.

### Heterogeneous summary table

## 1:42:30 — Null in TreeSet: with vs without Comparator

### Without Comparator (natural sorting) — complete rules

From Video 143 (star note):

Modern exam answer (Java 8+): null is NOT allowed in TreeSet at all with natural sorting.

TreeSet t = new TreeSet();
t.add(null);   // NullPointerException (Java 7+)

TreeSet t = new TreeSet();
t.add("A");
t.add(null);   // NullPointerException — must compare null with "A"

### With Comparator — null behavior

When Comparator is supplied, JVM calls compare(obj1, obj2). If either argument is null:

TreeSet t = new TreeSet(new MyComparator());
t.add(null);   // compare(null, null) or no comparison for first element?

Case 1: null as first element with Comparator (Java 7+):

TreeSet t = new TreeSet(new StringLengthComparator());
t.add(null);   // Still NullPointerException in Java 7+

TreeSet internally may still reject null even with Comparator in modern Java.

Case 2: non-empty TreeSet + null with Comparator:

TreeSet t = new TreeSet(new ReverseAlphaComparator());
t.add("A");
t.add(null);   // NullPointerException — compare(null, "A") → NPE in your compare method

Case 3: Comparator that handles null explicitly (theoretical — not exam focus):

```java
class NullSafeComparator implements Comparator {
    public int compare(Object o1, Object o2) {
        if (o1 == o2) return 0;
        if (o1 == null) return -1;
        if (o2 == null) return +1;
        String s1 = (String) o1;
        String s2 = (String) o2;
        return s1.compareTo(s2);
    }
}
```

Even with null-safe Comparator, TreeSet in Java 7+ generally rejects null at the collection level before compare is called. Do not rely on null in TreeSet for exams.

### Null summary — board note

Interview one-liner: "Null is not allowed in TreeSet (Java 7 onwards), regardless of whether Comparator is present."

## 1:47:00 — Session summary and exam checklist

### Programs covered in this session

### OCJP / SCJP exam checklist (Videos 143–145 combined)

- [ ] TreeSet underlying DS = Balanced Tree (Red-Black Tree)
- [ ] Duplicates not allowed; insertion order not preserved
- [ ] Heterogeneous objects → ClassCastException (TreeSet and TreeMap only)
- [ ] Default natural sorting requires homogeneous + Comparable
- [ ] String natural order = Unicode lexicographic (capitals before lowercase)
- [ ] MCQ: one/two/three/four → [four, one, three, two]
- [ ] LINE ONE without Comparator → compareTo(); with Comparator → compare()
- [ ] Comparator package = java.util; Comparable package = java.lang
- [ ] Implement Comparator → only compare() required (equals inherited from Object)
- [ ] compare return: negative = before, positive = after, zero = duplicate
- [ ] Reverse sort shortcuts: -(a.compareTo(b)) or b.compareTo(a)
- [ ] Subtraction trick: a - b for int/char; overflow risk for large ints
- [ ] Integer.compare(a, b) — preferred over subtraction
- [ ] StringBuffer/StringBuilder need Comparator (not Comparable)
- [ ] Custom objects need Comparator for any sort key (name, id, salary)
- [ ] TreeSet(Collection c) = inter-conversion with natural sorting
- [ ] Null NOT allowed in TreeSet (Java 7+)
- [ ] return +1 always → insertion order (dangerous trick)
- [ ] return 0 always → only first element survives
- [ ] JVM is blind — only trusts compare/compareTo return value
## Interview questions from this block (143–145)

### Basic TreeSet

Q1: What is the underlying data structure of TreeSet?

→ Balanced Tree (Red-Black Tree internally). O(log n) for add, remove, contains.

Q2: Does TreeSet preserve insertion order?

→ No. Elements are stored and printed in sorting order.

Q3: Are duplicates allowed in TreeSet?

→ No. When compareTo/compare returns 0, duplicate is silently not inserted.

Q4: Are heterogeneous objects allowed?

→ No. ClassCastException. TreeSet and TreeMap are the only collections with this restriction.

### String sorting traps

Q5: What is the output of TreeSet with "one", "two", "three", "four"?

→ [four, one, three, two] — lexicographic Unicode order, not English word order.

Q6: How does TreeSet sort "A" and "a"?

→ "A" comes before "a" because capital A (65) < lowercase a (97).

Q7: Why is String sorting called lexicographic and not alphabetical?

→ It compares Unicode values character-by-character, which differs from dictionary word order for multi-character strings starting with different letters.

### Comparable vs Comparator

Q8: What is the difference between Comparable and Comparator?

→ Comparable = default natural sorting (internal, compareTo). Comparator = customized sorting (external, compare).

Q9: Which package contains Comparable? Comparator?

→ Comparable: java.lang. Comparator: java.util.

Q10: When implementing Comparator, must you implement equals()?

→ No. equals() is inherited from Object.

Q11: What method does JVM call when Comparator is passed to TreeSet constructor?

→ compare(obj1, obj2) on your Comparator object.

Q12: In compare(obj1, obj2), which object is being inserted?

→ obj1 is the new element being inserted; obj2 is an existing element in the tree.

### Comparator implementation

Q13: Write a Comparator to sort strings by length.

→ Compare lengths; tie-break with compareTo. Use Integer.compare for safety.

Q14: One-line Comparator for reverse alphabetical String sort?

```java
→ return s2.compareTo(s1); or return -(s1.compareTo(s2));
```

Q15: What happens if compare() always returns +1?

→ Insertion order (not sorted). Duplicates allowed. JVM doesn't validate.

Q16: What happens if compare() always returns 0?

→ Only the first inserted element survives; all others treated as duplicates.

Q17: Subtraction trick vs Integer.compare — which is safer?

→ Integer.compare — no integer overflow risk.

### StringBuffer and custom objects

Q18: Can you store StringBuffer in TreeSet with default constructor?

→ No. ClassCastException — StringBuffer doesn't implement Comparable.

Q19: How to store StringBuffer in TreeSet?

→ Pass a Comparator that compares StringBuffer contents (e.g., via toString().compareTo()).

Q20: Can Person objects go into TreeSet without Comparator?

→ No (unless Person implements Comparable). Need Comparator for customized sort by name/id.

Q21: Two Person objects with same name but different id — duplicate in name-based Comparator?

→ Yes. compare returns 0 when names match → second Person not inserted.

### Inter-conversion and null

Q22: How to convert ArrayList to TreeSet with natural sorting?

→ TreeSet ts = new TreeSet(arrayList); — Constructor 3.

Q23: Is null allowed in TreeSet?

→ No (Java 7+). NullPointerException regardless of Comparator.

Q24: Difference between TreeSet(Comparator) and TreeSet(Collection)?

→ Comparator constructor: empty set with custom sort. Collection constructor: populated set with natural sort from collection elements.

### Advanced / trick

Q25: TreeSet with String and Integer — what happens?

→ ClassCastException with natural sorting. Cannot compare incompatible types.

Q26: If Comparator casts to String but Integer is added, what happens?

→ ClassCastException at the cast inside compare().

Q27: How is TreeSet output order determined?

→ Entirely by compareTo (natural) or compare (Comparator). JVM performs in-order traversal of internal BST.

Q28: Will TreeMap use the same Comparable/Comparator concepts?

→ Yes — identical terminology. Constructor 1 = natural, Constructor 2 = Comparator. (Preview for later sessions.)

## Homework / self-test

- Predict output of TreeSet MCQ (one, two, three, four) without running code.
- Write reverse alphabetical Comparator three ways: if-else, negation, reversed args.
- Write length Comparator using all three styles: if-else, subtraction, Integer.compare.
- Implement TreeSet with StringBuffer + Comparator from memory.
- Create Person class with name and id; write two Comparators (by name, by id).
- Convert ArrayList ["Z","A","M"] to TreeSet and predict output.
- Explain why t.add(10) after t.add("A") throws ClassCastException.
- Explain null behavior in TreeSet for Java 8.
- Predict output when compare always returns +1 with elements "C", "A", "B".
- Draw BST after inserting "K", "Z", "A", "A" with natural String order.
### Self-test program template

```java
import java.util.*;

public class Video145SelfTest {
    public static void main(String[] args) {
        // Test 1: MCQ
        TreeSet mcq = new TreeSet();
        for (String s : new String[]{"one", "two", "three", "four"})
            mcq.add(s);
        System.out.println("MCQ: " + mcq);
        // Expected: [four, one, three, two]

        // Test 2: reverse alpha
        TreeSet rev = new TreeSet(new Comparator() {
            public int compare(Object a, Object b) {
                return ((String)b).compareTo((String)a);
            }
        });
        for (String s : new String[]{"A", "Z", "L", "B"})
            rev.add(s);
        System.out.println("Reverse: " + rev);
        // Expected: [Z, L, B, A]

        // Test 3: by length
        TreeSet byLen = new TreeSet(new Comparator() {
            public int compare(Object a, Object b) {
                String s1 = (String) a, s2 = (String) b;
                int c = Integer.compare(s1.length(), s2.length());
                return c != 0 ? c : s1.compareTo(s2);
            }
        });
        for (String s : new String[]{"Java", "C", "Python", "Go"})
            byLen.add(s);
        System.out.println("By length: " + byLen);
        // Expected: [C, Go, Java, Python]

        // Test 4: StringBuffer
        TreeSet sb = new TreeSet(new Comparator() {
            public int compare(Object a, Object b) {
                return a.toString().compareTo(b.toString());
            }
        });
        sb.add(new StringBuffer("Z"));
        sb.add(new StringBuffer("A"));
        System.out.println("StringBuffer: " + sb);
        // Expected: [A, Z]

        // Test 5: ArrayList inter-conversion
        ArrayList al = new ArrayList();
        al.add("Z"); al.add("A"); al.add("M");
        TreeSet converted = new TreeSet(al);
        System.out.println("Converted: " + converted);
        // Expected: [A, M, Z]
    }
}
```

## Connection to Video 146 (next session)

Video 146 begins the Map module — the second half of the Collections Framework. Sir's opening recap in 146 confirms:

- Comparable/Comparator is the crown jewel of the Collection half
- Set terminology (TreeSet block) is complete after this session
- TreeMap (coming later) reuses identical Comparable/Comparator constructor terminology
Before starting Map: ensure every program in this session (145) runs correctly in your IDE from memory.

## Durga Sir's emphasis points (write in notebook)

- "Five to six more examples" — this session IS that promise from Video 144
- "JVM is blind" — applies to String, StringBuffer, Person, everything
- "LINE ONE" — with or without Comparator determines compare vs compareTo
- MCQ trap — one/two/three/four is NOT alphabetical word order
- Unicode capitals before lowercase — always check case in String TreeSet questions
- StringBuffer looks like String but is NOT Comparable — Comparator fixes it
- Same data, different Comparator → different output — Person by name vs by id
- ArrayList → TreeSet — Constructor 3 applies natural sort to unsorted collection
- Heterogeneous → ClassCastException — TreeSet and TreeMap only
- Null NOT allowed — Java 7+ regardless of Comparator
- Subtraction trick vs Integer.compare — know both, prefer Integer.compare
- return +1/0/-1 always — dangerous tricks; JVM never validates your logic
## Quick reference card

### TreeSet constructor decision tree

Need TreeSet?
│
├─ Have existing Collection to convert?
│   └─ new TreeSet(collection) → natural sort applied
│
├─ Need default natural order (Comparable objects)?
│   └─ new TreeSet() → JVM calls compareTo()
│
└─ Need custom order?
    └─ new TreeSet(new MyComparator()) → JVM calls compare()

### compare() return contract (same as compareTo)

### String Comparator recipes

End of Video 145 study notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Position | 145 of 203 |  |  |
| Playlist | Core Java With OCJP/SCJP |  |  |
| Title | Collections Part-10 \ | \ | string object in Treeset Example |
| Instructor | Durga Sir |  |  |
| Duration | 1h 50m 08s |  |  |
| Video ID | zHKqmFyuaKI |  |  |
| URL | https://www.youtube.com/watch?v=zHKqmFyuaKI |  |  |
| Notes source | Synthesized from adjacent lectures + standard syllabus (captions unavailable; Whisper blocked) |  |  |
| Prerequisite | Video 143 (TreeSet fundamentals), Video 144 (Comparator interface + Integer descending + seven compare styles) |  |  |
| Next session | Video 146 (Map introduction — HashMap, Hashtable) |  |  |

| Session | Focus | Status |
|---|---|---|
| Video 143 | TreeSet properties, constructors, String natural sort, StringBuffer CCE, null rules, Comparable/compareTo | ✅ Prerequisite |
| Video 144 | Comparator interface, Integer descending, seven compare styles, JVM-blind analogy | ✅ Prerequisite |
| Video 145 | String + custom object Comparator marathon (this session) | ✅ Today |
| Video 146 | Map introduction — HashMap, Hashtable | ⏳ Next |

| Scenario | Example | Solution |
|---|---|---|
| Natural order not available | StringBuffer (no Comparable) | Pass Comparator to TreeSet constructor |
| Natural order not satisfactory | String A→Z but you want Z→A | Pass Comparator to TreeSet constructor |

| LINE ONE | JVM internally calls | Sorting type |
|---|---|---|
| TreeSet t = new TreeSet(); | compareTo() | Default natural sorting |
| TreeSet t = new TreeSet(new MyComparator()); | compare() | Customized sorting |

| Character | Unicode (decimal) |
|---|---|
| 'A' (capital) | 65 |
| 'Z' (capital) | 90 |
| 'a' (lowercase) | 97 |
| 'z' (lowercase) | 122 |

| Option | Output |
|---|---|
| A | [four, one, three, two] |
| B | [one, two, three, four] |
| C | [one, three, two, four] |
| D | Compilation fails |

| String | First char | Unicode |
|---|---|---|
| "four" | 'f' | 102 |
| "one" | 'o' | 111 |
| "three" | 't' | 116 |
| "two" | 't' | 116 |

| Comparison | Result | Reasoning |
|---|---|---|
| "four".compareTo("one") | negative | 'f'(102) < 'o'(111) |
| "one".compareTo("three") | negative | 'o'(111) < 't'(116) |
| "three".compareTo("two") | negative | 'h'(104) < 'w'(119) at index 1 |

| Collection | Order preserved? | Sorting? |
|---|---|---|
| TreeSet | No | Yes — always sorted |
| LinkedHashSet | Yes — insertion order | No |
| HashSet | No | No |

| Expression | Result | Meaning |
|---|---|---|
| 3 - 5 | -2 (negative) | obj1 shorter → before |
| 7 - 2 | +5 (positive) | obj1 longer → after |
| 4 - 4 | 0 | same length → need tie-breaker |

| # | compare() body | Output | Notes |
|---|---|---|---|
| 1 | return s1.compareTo(s2); | Natural alphabetical | Same as no Comparator |
| 2 | return -(s1.compareTo(s2)); | Reverse alphabetical | One-line reverse |
| 3 | return s2.compareTo(s1); | Reverse alphabetical | Reverse args |
| 4 | return Integer.compare(s1.length(), s2.length()); | Sort by length ascending | Subtraction safe via Integer.compare |
| 5 | return s1.length() - s2.length(); | Sort by length ascending | Subtraction trick |
| 6 | return +1; always | Insertion order | NOT sorted — [Java, C, Python, Go] |
| 7 | return 0; always | Only first element | [Java] only |

| Style | Use when | Risk |
|---|---|---|
| +1/-1/0 if-else | Learning, interviews, explicit logic | Verbose |
| Subtraction a - b | Small int/char differences | Overflow for large ints |
| Integer.compare(a, b) | Production code, exam best practice | None for ints |
| s1.compareTo(s2) | Delegating to natural order | None |
| -(s1.compareTo(s2)) | Reversing natural order | None |

| Aspect | Without Comparator | With Comparator |
|---|---|---|
| StringBuffer in TreeSet | ClassCastException | Works |
| JVM calls | compareTo (fails) | compare (your logic) |
| Comparison basis | N/A | Whatever you define in compare() |

| Comparator | Sort key | Output order |
|---|---|---|
| PersonNameComparator | name | Anil, Durga, Ravi, Shiva |
| PersonIdComparator | id | Durga(101), Anil(102), Ravi(103), Shiva(104) |

| Aspect | ArrayList | TreeSet |
|---|---|---|
| Order | Insertion order preserved | Sorted order |
| Duplicates | Allowed | Not allowed |
| Underlying DS | Dynamic array | Balanced tree |

| Scenario | Result |
|---|---|
| String + Integer, no Comparator | ClassCastException |
| String + Integer, with normal Comparator | ClassCastException (at cast) |
| Any mix, compare always +1 | All added — insertion order (exam trick) |
| String + String | OK |
| Integer + Integer | OK |

| Scenario | Java 6 | Java 7+ |
|---|---|---|
| Empty TreeSet, add null first | Allowed [null] | NullPointerException |
| Non-empty TreeSet, add null | NullPointerException | NullPointerException |
| TreeSet has null, add anything else | NullPointerException | NullPointerException |

| TreeSet type | null allowed? (Java 8+) |
|---|---|
| new TreeSet() natural | No — NullPointerException |
| new TreeSet(comparator) | No — NullPointerException |
| HashSet | Yes — one null allowed |
| ArrayList | Yes — multiple nulls allowed |

| # | Class / Topic | Comparator? | Key output |
|---|---|---|---|
| 1 | String natural sorting recap | No | [A, B, L, Z] |
| 2 | MCQ one/two/three/four | No | [four, one, three, two] |
| 3 | Insertion vs sorted demo | No | Sorted, not insertion order |
| 4 | Reverse alphabetical String | Yes | [Z, M, L, B, A] |
| 5 | Sort by length | Yes | [C, Go, Java, Python] |
| 6 | Sort by last character | Yes | [dog, bat, cat, rat] |
| 7 | StringBuffer + Comparator | Yes | [A, B, L, Z] |
| 8 | Person by name | Yes | Alphabetical by name |
| 9 | Person by id | Yes | Numerical by id |
| 10 | Employee by salary desc | Yes | Highest salary first |
| 11 | ArrayList → TreeSet | No (Constructor 3) | Natural sort applied |
| 12 | Heterogeneous String+Integer | No | ClassCastException |
| 13 | Null acceptance | Both | NullPointerException (Java 7+) |

| Return | Meaning | TreeSet action |
|---|---|---|
| Negative | obj1 before obj2 | Go left in BST |
| Positive | obj1 after obj2 | Go right in BST |
| Zero | obj1 equals obj2 | Duplicate — skip |

| Goal | One-liner |
|---|---|
| Natural alpha | s1.compareTo(s2) |
| Reverse alpha | s2.compareTo(s1) |
| By length asc | Integer.compare(s1.length(), s2.length()) |
| By length desc | Integer.compare(s2.length(), s1.length()) |
| By last char | Integer.compare(c1, c2) where c = charAt(len-1) |
