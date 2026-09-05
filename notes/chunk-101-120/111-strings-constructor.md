# Video 111

## Video info

**Title:** Core Java With OCJP/SCJP: java.lang.package Part-7 || Strings||constructor

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP (java.lang package series) |
| Position | 111 of 203 |
| Series | java.lang.package |
| Topic | String vs StringBuffer; StringBuffer constructors & methods; StringBuilder |
| Instructor | Durga Sir |
| Duration | 1h 42m 01s |
| Video ID | JEaVfaRJiZw |
| Watch | https://www.youtube.com/watch?v=JEaVfaRJiZw |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

*Caption title says “constructors of StringsBuffer”; session follows prior String deep-dive and covers StringBuffer/StringBuilder.*

### 00:06 — Recap: moving from String to StringBuffer / StringBuilder

Last session completed **postmortem on String**. Now: **StringBuffer**, then **StringBuilder**.

### 00:30 — When to use String vs StringBuffer

**String objects are immutable.**

| Content behavior | Recommendation |
|---|---|
| Fixed, won't change frequently | Use `String` |
| Not fixed, keeps changing | Not recommended to use String |

**Problem with String for changing content:**

```java
String s = "Durga";
// want "soft" → new object "Durgasoft"
// want "software" → new object "Durgasoftware"
// want "Durga Software Solutions" → yet another new object
```

For **every small change** (even comma → semicolon), a **new object** is created → **memory / performance** issues at scale.

**Solution for changing content:** **`StringBuffer`**

**Main advantage of StringBuffer over String:** all required changes happen in the **existing object only** (mutable).

### 10:44 — String: length = size = capacity (no separate capacity)

For `String s = "Durga"` (length **5**):

- **length** = **size** = **capacity** = **5**
- Cannot add/remove after creation → only talk about **length** for String
For **StringBuffer** with `"Durga"` (length 5):

- **length** = characters already inserted
- **capacity** = total characters the buffer **can** hold (can grow)
- Must distinguish **length** vs **capacity**
**Analogy:**

- **Array** ≈ String (fixed size, no capacity talk)
- **Collection / ArrayList** ≈ StringBuffer (size vs capacity)
- Default ArrayList capacity: **10**; default StringBuffer capacity: **16**
### 13:12 — StringBuffer Constructor 1: no-arg (default capacity 16)

```java
StringBuffer sb = new StringBuffer();
// Creates empty StringBuffer with default initial capacity = 16
```

**When 17th character is appended:** internal resize (like ArrayList):

1. New StringBuffer object created
1. Existing 16 chars copied
1. 17th char added
1. Reference repointed; old object eligible for GC
**Growth formula (StringBuffer):**

```java
newCapacity = (currentCapacity + 1) * 2
```

**ArrayList formula (contrast):**

```java
newCapacity = currentCapacity * 3 / 2 + 1
```

**Demo:**

```java
class Test {
    public static void main(String[] args) {
        StringBuffer sb = new StringBuffer();
        System.out.println(sb.capacity()); // 16

        sb.append("abcdefghijklmnop");     // 16 chars
        System.out.println(sb.capacity()); // still 16

        sb.append("q");                    // 17th char triggers resize
        System.out.println(sb.capacity()); // 34  → (16+1)*2
    }
}
```

Further growth example on board: after filling 34 chars, next append → capacity **70** → `(34+1)*2`.

### 27:51 — StringBuffer Constructor 2: `int initialCapacity`

If you know you'll add ~1000 characters, don't grow 16→34→70→142→… wastefully:

```java
StringBuffer sb = new StringBuffer(1000);
// Empty buffer, initial capacity = 1000 → better performance
```

### 30:27 — StringBuffer Constructor 3: `String str`

Create equivalent StringBuffer for a given String:

```java
String s = "Durga";
StringBuffer sb = new StringBuffer(s);
```

**Interview twist — capacity is NOT 16 or 5:**

```java
capacity = s.length() + 16
```

For `"Durga"` (length 5): capacity = **5 + 16 = 21**

```java
class Test {
    public static void main(String[] args) {
        StringBuffer sb = new StringBuffer("Durga");
        System.out.println(sb.capacity()); // 21
    }
}
```

**Three constructors summary:**

1. `new StringBuffer()` → empty, capacity **16**
1. `new StringBuffer(int initialCapacity)` → empty, specified capacity
1. `new StringBuffer(String s)` → content from string, capacity **s.length() + 16**
### 36:38 — Important StringBuffer methods (part 1)

| Method | Purpose |
|---|---|
| public int length() | Number of characters already present |
| public int capacity() | Total characters buffer can accommodate |
| public char charAt(int index) | Character at index (zero-based) |
| public void setCharAt(int index, char ch) | Replace char at index |

**`charAt` example:**

```java
StringBuffer sb = new StringBuffer("Durga");
System.out.println(sb.charAt(3));  // 'g' — index 3
System.out.println(sb.charAt(30)); // StringIndexOutOfBoundsException
```

**Note:** Even for StringBuffer, exception name is **`StringIndexOutOfBoundsException`** (no separate StringBufferIndexOutOfBoundsException).

**`setCharAt`:** replace character at specified index with new character.

### 42:18 — `append()` — overloaded, not String-only

```java
public StringBuffer append(/* many types */)
```

Return type: **`StringBuffer`** (enables chaining).

Overloads exist for: `String`, `int`, `long`, `char`, `double`, `boolean`, etc.

```java
class Test {
    public static void main(String[] args) {
        StringBuffer sb = new StringBuffer();
        sb.append("pi value is ");
        sb.append(3.14);      // double
        sb.append(" it is exactly ");
        sb.append(true);      // boolean
        System.out.println(sb);
    }
}
```

**Output:**

```java
pi value is 3.14 it is exactly true
```

### 48:18 — `insert(int index, …)` vs `append`

- **`append`:** always adds at **end**
- **`insert`:** inserts at **specified index** (also overloaded)
```java
StringBuffer sb = new StringBuffer("abcdefgh");
sb.insert(2, "XYZ");
System.out.println(sb);
```

**Output:** `abXYZcdefgh` — `XYZ` inserted at index 2.

### 53:53 — `delete()` methods

1. `public StringBuffer delete(int begin, int end)` — deletes from `begin` to **`end - 1`** (same half-open interval idea as `substring`)
1. `public StringBuffer deleteCharAt(int index)` — delete single char at index
### 56:30 — `reverse()`

No `reverse()` in **String**; exists in **StringBuffer**.

```java
StringBuffer sb = new StringBuffer("Durga");
System.out.println(sb.reverse());
```

**Output:** `agruD`

- Reverses **order of characters**, not each character's internal spelling
- `'a'` stays `'a'`, order flips
### 59:26 — `setLength(int newLength)`

```java
StringBuffer sb = new StringBuffer("iswarabi");
sb.setLength(8);
System.out.println(sb);
```

**Output:** `iswarabi` truncated to first **8** characters → `iswarabi` → board example keeps first 8 chars (`iswarabi` → `iswarabi` trimmed conceptually to length 8).

If length set **shorter**, trailing characters removed.

### 1:02:29 — `ensureCapacity(int minimumCapacity)`

Increase capacity **on the fly** after object already created:

```java
StringBuffer sb = new StringBuffer();  // capacity 16
sb.ensureCapacity(1000);
System.out.println(sb.capacity());     // 1000
```

Opposite of constructor-with-capacity when you discover size requirement later.

### 1:06:46 — `trimToSize()`

Reverse of `ensureCapacity` — release unused capacity:

```java
StringBuffer sb = new StringBuffer(1000);  // capacity 1000
sb.append("abc");                          // length 3 only
sb.trimToSize();
System.out.println(sb.capacity());         // 3 — deallocate extra
```

### 1:09:46 — ~12 important StringBuffer methods covered

Length, capacity, charAt, setCharAt, append, insert, delete, deleteCharAt, reverse, setLength, ensureCapacity, trimToSize.

### 1:10:08 — Critical: every StringBuffer method is **synchronized**

- All StringBuffer methods → **synchronized**
- At a time, **only one thread** can operate on a given StringBuffer (even reads)
- **Thread-safe** but **performance** may suffer (threads wait)
**Java 1.5 response:** **`StringBuilder`** — same API idea, **non-synchronized**.

### 1:14:48 — StringBuilder origin story (Durga Sir’s explanation)

Legend (teaching mnemonic): Sun took `StringBuffer.java`, replaced **buffer → builder**, removed **`synchronized`** keyword → `StringBuilder.java`.

**Top-level definition:** **Non-synchronized version of StringBuffer**.

|  | StringBuffer | StringBuilder |
|---|---|---|
| Methods synchronized? | Yes | No |
| Threads at a time | One | Multiple |
| Thread-safe? | Yes | No |
| Performance | Relatively lower (waiting) | Relatively higher |
| Introduced in | 1.0 | 1.5 |

**Everything else same** (methods, constructors) except above differences.

### 1:27:17 — When String vs StringBuffer vs StringBuilder

| Scenario | Choice |
|---|---|
| Content fixed, won't change often (city name, college name) | String |
| Content changes + thread safety required | StringBuffer |
| Content changes + thread safety NOT required | StringBuilder |

### 1:33:22 — Method chaining

Most StringBuffer/StringBuilder mutating methods return **`StringBuffer` / `StringBuilder`** (same type) → chain calls:

```java
StringBuffer sb = new StringBuffer()
    .append("Durga")
    .append("software")
    .append("solutions")
    .insert(2, "XYZ")
    .reverse()
    .delete(2, 10);
System.out.println(sb);
```

**Rules:**

- **Method chaining:** after one method, call another on the result
- Execution order: **left to right** (`M1` then `M2` then `M3` …)
Board full example:

```java
StringBuffer sb = new StringBuffer()
    .append("Durga")
    .append("software")
    .append("solutions")
    .insert(2, "XYZ")
    .reverse()
    .delete(2, 10);
System.out.println(sb);
// Output depends on intermediate steps after live demo
```

### 1:41:40 — Session end

StringBuffer constructors, methods, StringBuilder comparison, selection criteria, and method chaining complete.

## ASR decode notes

| Heard | Intended |
|---|---|
| sing / single buffer | StringBuffer |
| sting buffer / singer | StringBuffer |
| upend / P | append |
| Kat / karat / car get | charAt |
| set car get | setCharAt |
| Prim to size | trimToSize |
| insure capacity | ensureCapacity |
| threat / thre | thread |
| build / Builder | StringBuilder |

**Java code block count:** 16
