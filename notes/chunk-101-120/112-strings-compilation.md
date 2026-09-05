# Video 112 — String, StringBuffer & StringBuilder compilation

## Video info

**Title:** String, StringBuffer & StringBuilder for JAVA Certification & Interviews || by Durga Sir

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 112 of 203 |
| Series | java.lang package (mega compilation) |
| Topic | String, StringBuffer & StringBuilder for JAVA Certification & Interviews |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 6h 33m 07s (23587 seconds) |
| Video ID | P5tFJ9umhvk |
| Watch | https://www.youtube.com/watch?v=P5tFJ9umhvk |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

## Important: this is a mega compilation, not a new lecture

This upload is a ~6.5-hour re-package of the individual `java.lang` lectures already in the same playlist (videos **105–111** and **113–119**). It does not introduce new board material beyond those component videos.

**Captions:** YouTube has no usable auto-captions for this mega upload (none that can drive timestamped board-level notes). Do not treat this file as a full transcript rewrite of the 6h video.

**Where the real notes live:** Detailed caption-based lecture notes with Java board examples are in the component videos 105–111 and 113–119 under `notes/chunk-101-120/`. Study those files (and watch those shorter videos) for board timestamps, ASR-decoded board text, and full examples.

This file is only an **index + OCJP study checklist + exam-checklist snippets** for the compilation entry at position 112.

## Mapping: compilation topics → individual playlist videos

Watch URLs for component videos: `https://www.youtube.com/watch?v=<VideoID>` using IDs from `notes/playlist.tsv` (rows 105–111, 113–119).

| Compilation topic (java.lang stretch) | Playlist # | Video ID | Individual title (short) | Detailed notes file |
|---|---|---|---|---|
| java.lang intro; Object hierarchy; toString() | 105 | -qrKA1aWMZs | java.lang Part-1 — Introduction, Object, toString() | notes/chunk-101-120/105-java-lang-intro.doc / .docx |
| Object class — hashCode() | 106 | r6G5Pz0yMH4 | java.lang Part-2 — Object, Hashcode() | Component video 106 (same playlist); notes may be under chunk-101-120 when present |
| Object class — equals(); overridden methods | 107 | izDt7L4009k | java.lang Part-3 — equals(), overridden methods | Component video 107 (same playlist) |
| Object class — finalize(), getClass(), notify() | 108 | 3gQdOltJ89k | java.lang Part-4 — finalize(), getClass(), notify() | Component video 108 (same playlist) |
| String class — introduction & immutability | 109 | cI2JVbEWGy8 | java.lang Part-5 — Strings class | Component video 109 (same playlist) |
| String class — constructors | 110 | 7zeOxAl19bg | java.lang Part-6 — Strings class constructors | Component video 110 (same playlist) |
| StringBuffer & StringBuilder — constructors & methods | 111 | JEaVfaRJiZw | java.lang Part-7 — StringBuffer constructors | notes/chunk-101-120/111-strings-constructor.doc / .docx |
| Wrapper classes — objects, constructors, valueOf, xxxValue | 113 | UHq63fU4NVU | java.lang Part-8 — wrapper class, wrapper objects | notes/chunk-101-120/113-wrapper-classes.doc / .docx |
| Wrapper classes — utility methods (parseXxx, static toString) | 114 | pmemJ6QfWjo | java.lang Part-9 — wrapper class utility methods | Component video 114 (same playlist) |
| Autoboxing & autounboxing — definitions, cache buffer | 115 | gk1bQSgiBpw | java.lang Part-10 — Autoboxing, Autounboxing-1 | notes/chunk-101-120/115-autoboxing-unboxing.doc / .docx |
| Autoboxing & autounboxing — advanced traps | 116 | tcHVFR5OzD8 | java.lang Part-11 — Autoboxing, Autounboxing-2 | Component video 116 (same playlist) |
| Object class — == vs equals(); equals()–hashCode() contract | 117 | wJgua6AobQU | java.lang Part-12 — equals(), Hashcode() | notes/chunk-101-120/117-object-class-part-12.doc / .docx |
| Object class — clone() & Cloneable | 118 | L-p-RGTNrZg | java.lang Part-13 — clone() | notes/chunk-101-120/118-object-class-part-13.doc / .docx |
| String class — heap vs SCP, intern(), compile-time concat | 119 | oEAiBx_06SA | java.lang Part-14 — String class | notes/chunk-101-120/119-string-class-part-14.doc / .docx |

## OCJP study checklist (topics covered by this compilation)

Use this as a revision checklist; tick off after reading the matching component notes.

- [ ] `java.lang` — no explicit import; contains Object, String, System, wrappers, etc.
- [ ] Object class — every class extends Object; 11 exam-count methods (12 including private `registerNatives()`)
- [ ] `toString()` — default `className@hexHash`; override for meaningful output; already overridden in String, wrappers, collections
- [ ] `hashCode()` — identity-based in Object; content-based when overridden with `equals()`
- [ ] `equals()` — default reference comparison; override for content; relation rules with `==`
- [ ] `finalize()`, `getClass()`, `notify()` / `notifyAll()` / `wait()` — know purpose and prototype
- [ ] String immutability — any change creates new object; SCP sharing is why immutability exists
- [ ] String Constant Pool (SCP) — literal reuse; `new String("x")` creates heap + SCP entry
- [ ] String constructors — heap object from literal, char array, StringBuffer, etc.
- [ ] String methods — `length`, `charAt`, `substring`, `concat`, `equals`, `compareTo`, etc.
- [ ] Compile-time vs runtime string `+` — constant folding vs heap concat at runtime
- [ ] StringBuffer — mutable; default capacity 16; growth `(currentCapacity + 1) * 2`; all methods synchronized
- [ ] StringBuilder — same API as StringBuffer; non-synchronized; prefer when thread safety not needed
- [ ] String vs StringBuffer vs StringBuilder — fixed content vs changing content vs thread safety
- [ ] Wrapper classes — 8 types; wrap primitive for collections/generics; utility methods
- [ ] Wrapper constructors — two-arg pattern (primitive + String); traps: Character (char only), Boolean String rules, Float (3 ctors)
- [ ] `valueOf()` / `xxxValue()` — preferred creation; unboxing uses `intValue()` etc.
- [ ] Autoboxing / autounboxing — compiler rewrites to `valueOf` / `xxxValue`; Java 1.5+
- [ ] Integer cache — -128 to +127 reused; `new` bypasses cache; `==` on wrappers compares references
- [ ] `equals()`–`hashCode()` contract — equal objects must share hash code; override both together
- [ ] `==` vs `.equals()` — incomparable types CE for `==`; `.equals()` returns false safely
- [ ] `intern()` — heap reference → corresponding SCP reference (creates SCP entry if missing)
- [ ] `clone()` — `protected Object clone() throws CloneNotSupportedException`; class must implement `Cloneable`
## Exam-checklist snippets (not board timestamps from this mega video)

The following `java` blocks summarize **key OCJP points** from the component java.lang lectures (105–111, 113–119). They are **exam-checklist snippets**, not claimed board timestamps or a transcript of video `P5tFJ9umhvk`.

### 1) `java.lang` implicit + Object as root

```java
// No import java.lang.* required — String, System, Object are always available
class Demo {
    public static void main(String[] args) {
        String s = "durga";           // java.lang.String
        System.out.println(s);        // java.lang.System
        Demo d = new Demo();
        System.out.println(d instanceof Object); // true — every class extends Object
    }
}
```

### 2) Default vs overridden `toString()`

```java
class Student {
    String name = "Durga";
    // no toString override → Object.toString() → Student@hex
}
class Test {
    public static void main(String[] args) {
        Student s = new Student();
        System.out.println(s);              // Student@... (default)

        String str = new String("Durga");
        System.out.println(str);            // Durga — String overrides toString

        Integer i = Integer.valueOf(10);
        System.out.println(i);              // 10 — wrapper overrides toString
    }
}
```

### 3) `new String` vs literal — heap vs SCP

```java
class Test {
    public static void main(String[] args) {
        String s1 = new String("durga");  // heap object + SCP literal "durga"
        String s2 = new String("durga");  // another heap object, same SCP literal
        String s3 = "durga";              // SCP only

        System.out.println(s1 == s2);       // false — different heap objects
        System.out.println(s1 == s3);       // false — heap vs SCP
        System.out.println(s2 == s3);       // false — heap vs SCP
        System.out.println(s1.equals(s3));  // true — content comparison
    }
}
```

### 4) Compile-time vs runtime string concatenation

```java
class Test {
    public static void main(String[] args) {
        String s3 = "you cannot change me";

        String s5 = "you cannot" + " change me";  // compile-time fold → SCP
        System.out.println(s3 == s5);             // true

        String s6 = "you cannot";                 // normal variable
        String s7 = s6 + " change me";            // runtime concat → heap
        System.out.println(s3 == s7);             // false

        final String s8 = "you cannot";
        String s9 = s8 + " change me";            // final → compile-time fold
        System.out.println(s3 == s9);             // true
    }
}
```

### 5) StringBuffer capacity — default 16 and `String` constructor rule

```java
class Test {
    public static void main(String[] args) {
        StringBuffer sb1 = new StringBuffer();
        System.out.println(sb1.capacity());       // 16

        StringBuffer sb2 = new StringBuffer("Durga");
        System.out.println(sb2.length());         // 5
        System.out.println(sb2.capacity());         // 21 → length + 16
    }
}
```

### 6) StringBuffer growth formula

```java
class Test {
    public static void main(String[] args) {
        StringBuffer sb = new StringBuffer();
        sb.append("abcdefghijklmnop");   // 16 chars — capacity still 16
        System.out.println(sb.capacity()); // 16

        sb.append("q");                    // 17th char triggers resize
        System.out.println(sb.capacity()); // 34 → (16 + 1) * 2
    }
}
```

### 7) String vs StringBuffer vs StringBuilder

```java
class Test {
    public static void main(String[] args) {
        // Fixed content, no frequent changes → String
        String city = "Hyderabad";

        // Content changes, thread safety needed → StringBuffer (synchronized)
        StringBuffer sb = new StringBuffer("Durga");
        sb.append("soft");

        // Content changes, single-threaded → StringBuilder (faster, not synchronized)
        StringBuilder sbd = new StringBuilder("Durga");
        sbd.append("soft");

        System.out.println(city);
        System.out.println(sb);    // Durgasoft
        System.out.println(sbd);   // Durgasoft
    }
}
```

### 8) Wrapper Boolean String constructor trap

```java
class Test {
    public static void main(String[] args) {
        Boolean x = new Boolean("yes");
        Boolean y = new Boolean("no");
        System.out.println(x);              // false
        System.out.println(y);              // false
        System.out.println(x.equals(y));    // true — both stored as false internally
        // String-arg rule: only case-insensitive "true" → true; everything else → false
    }
}
```

### 9) Autoboxing cache — `==` on Integer (in range vs out of range)

```java
class Test {
    public static void main(String[] args) {
        Integer a = 127;
        Integer b = 127;
        System.out.println(a == b);         // true — cache -128..127

        Integer c = 128;
        Integer d = 128;
        System.out.println(c == d);         // false — outside cache, two objects

        Integer e = new Integer(10);
        Integer f = 10;
        System.out.println(e == f);         // false — new bypasses cache
        System.out.println(e.equals(f));    // true — use equals for value
    }
}
```

### 10) `==` vs `equals()` — String vs StringBuffer type rules

```java
class Test {
    public static void main(String[] args) {
        String s1 = new String("durga");
        String s2 = new String("durga");
        StringBuffer sb1 = new StringBuffer("durga");
        StringBuffer sb2 = new StringBuffer("durga");

        System.out.print(s1 == s2);         // false
        System.out.print(s1.equals(s2));    // true — String overrides equals
        System.out.print(sb1 == sb2);        // false
        System.out.print(sb1.equals(sb2));  // false — StringBuffer does NOT override equals
        // System.out.print(s1 == sb1);     // CE: incomparable types String and StringBuffer
        System.out.print(s1.equals(sb1));    // false — no error, unrelated types
    }
}
```

### 11) `equals()`–`hashCode()` contract — override together

```java
import java.util.*;

class Person {
    String name;
    int age;

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj instanceof Person p) {
            return name.equals(p.name) && age == p.age;
        }
        return false;
    }

    @Override
    public int hashCode() {
        return name.hashCode() + age;  // same fields as equals()
    }
}

class Test {
    public static void main(String[] args) {
        Person p1 = new Person("Shiva", 30);
        Person p2 = new Person("Shiva", 30);
        System.out.println(p1.equals(p2));           // true
        System.out.println(p1.hashCode() == p2.hashCode()); // true — contract satisfied
        Set<Person> set = new HashSet<>();
        set.add(p1);
        System.out.println(set.contains(p2));        // true — hash bucket works
    }
}
```

### 12) `intern()` — move from heap reference to SCP

```java
class Test {
    public static void main(String[] args) {
        String s1 = new String("durga");   // s1 → heap; "durga" also in SCP
        String s2 = s1.intern();           // s2 → SCP reference for "durga"
        String s3 = "durga";               // s3 → SCP

        System.out.println(s1 == s2);        // false — heap vs SCP
        System.out.println(s2 == s3);      // true — both SCP

        String s4 = new String("durga").concat("soft"); // runtime heap only
        String s5 = s4.intern();           // creates "durgasoft" in SCP if missing
        String s6 = "durgasoft";
        System.out.println(s4 == s5);      // false — heap vs SCP
        System.out.println(s5 == s6);        // true
    }
}
```

## How to use this file

1. Prefer videos **105–111** and **113–119** (and their note files) for board-level study.
1. Use this file when you landed on the mega upload at position **112** and need a map + OCJP checklist.
1. Do not expect a minute-by-minute transcript here — captions for `P5tFJ9umhvk` are not usable for that purpose.
