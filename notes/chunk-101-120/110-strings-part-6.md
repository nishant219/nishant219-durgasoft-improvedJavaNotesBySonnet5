# Video 110

## Video info

**Title:** Core Java With OCJP/SCJP: java.lang.package Part-6 ||  Strings class

**Position:** 110 of 203 · Series `java.lang` · Part 6

**Duration:** 1h 43m 17s (from transcript)

**ID:** 7zeOxAl19bg

**Watch:** https://www.youtube.com/watch?v=7zeOxAl19bg

**Playlist:** https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0

### 00:07 — Session opening: String APIs (constructors + methods)

Durga Sir resumes after prior videos on String terminology — immutability, advantages/disadvantages, internal SCP (String Constant Pool) behavior. **Remaining syllabus for this video:** String class **constructors** and **important methods**.

### 00:43 — Constructors of `String` class (overview)

Board heading: **Constructors of String class.**

Durga Sir covers the main constructors one by one. Additional constructors exist but are deferred; focus first on the foundational ones.

### 01:06 — Constructor 1: `new String()` — empty String object

Creates an **empty String object** on the heap — zero-length, **not null**.

```java
String s = new String();
// Creates empty String object; length = 0
// s.length() → 5? No → 0
```

**Critical distinction (exam favourite):**

| Code | Meaning |
|---|---|
| String s = ""; | String object exists, length 0 |
| String s = null; | No String object; reference is null |

Both are **not the same**. `new String()` is equivalent to `""` in content (zero-length object), but **not** equivalent to `null`.

```java
String s1 = new String();   // empty object, length 0
String s2 = "";             // same idea — zero-length object (often pooled)
String s3 = null;           // no object at all
```

### 02:36 — Constructor 2: `new String(String literal)`

For a given **String literal**, creates an **equivalent String object in the heap**. The literal still lives in **SCP**; `new` forces a **separate heap object**.

```java
String s = new String("Durga");
// Literal "Durga" → SCP
// new String(...) → separate object in heap
// s refers to heap copy, not SCP literal reference
```

### 03:24 — Constructor 3: `new String(StringBuffer sb)`

**Conversion / “dancing” between StringBuffer and String** — for a given `StringBuffer`, create equivalent `String`.

```java
StringBuffer sb = new StringBuffer("Durga");
String s = new String(sb);
// Equivalent String object for contents of sb
```

Same pattern works the other way (`StringBuffer` constructor from `String`) — bidirectional conversion is possible.

### 04:31 — Recap: first three constructors on board

```java
// 1. Empty
String s1 = new String();

// 2. From literal (heap copy)
String s2 = new String("Durga");

// 3. From StringBuffer
StringBuffer sb = new StringBuffer("Durga");
String s3 = new String(sb);
```

### 07:08 — Constructor 4: `new String(char[] chars)`

For given **char array**, create equivalent String.

```java
char[] ch = {'a', 'b', 'c', 'd'};
String s = new String(ch);
System.out.println(s);
// Prints: abcd
```

By default the **entire array** becomes the String content.

### 08:22 — Constructor 5: `new String(char[] chars, int offset, int count)`

Subset of char array — from `offset`, for `count` characters.

```java
char[] ch = {'a', 'b', 'c', 'd'};
String s = new String(ch, 0, 4);
System.out.println(s);
// Prints: abcd
```

Same example array; constructor can take portion of array (offset + count).

### 10:06 — Constructor 6: `new String(byte[] bytes)`

For given **byte array**, create String using **default charset** (platform default). Bytes treated as **character codes** (Unicode code units in example).

```java
byte[] b = {100, 101, 102};  // ASCII/Unicode: d=100, e=101, f=102
String s = new String(b);
System.out.println(s);
// Prints: def
```

**Board decoding (ASR “uncoded values” → Unicode values):**

| Byte value | Character |
|---|---|
| 97 | a |
| 98 | b |
| 99 | c |
| 100 | d |

Constructor interprets bytes per default charset; in lecture example, values map directly to characters.

```java
byte[] b = {97, 98, 99, 100};
String s = new String(b);
System.out.println(s);
// Prints: abcd
```

### 13:41 — Transition: important methods of String class

Constructors related to `byte[]` and `char[]` are important for OCJP. Now shift to **important methods** — several are compulsory for exam and daily use.

### 14:27 — Method 1: `char charAt(int index)`

Returns the **character at specified index** (zero-based).

```java
String s = "Durga";
System.out.println(s.charAt(3));
// Prints: g
// Index: D=0, u=1, r=2, g=3, a=4
```

**Invalid index → runtime exception:**

```java
String s = "Durga";
System.out.println(s.charAt(30));
// Runtime: StringIndexOutOfBoundsException
```

Signature on board:

```java
public char charAt(int index)
// Returns character at specified index
```

### 17:38 — Method 2: `concat(String str)` (+ and `+=` overload)

**Concatenation** — join this String with argument.

```java
String s = "Durga";
s = s.concat(" Software");
System.out.println(s);
// Prints: Durga Software
```

**`+` and `+=` are overloaded for String — also concatenation only:**

```java
String s = "Durga";
s = s + " Software";      // valid
s += " Solutions";         // valid — same purpose as concat
System.out.println(s);
// Prints: Durga Software Solutions
```

No difference in purpose: `concat`, `+`, `+=` all concatenate.

### 21:19 — Method 3: `equals(Object)` vs `equalsIgnoreCase(String)`

**`equals`** — **content comparison**, **case-sensitive** (overriding `Object.equals`).

```java
String s = "Java";
System.out.println(s.equals("java"));
// Prints: false   (case matters)
```

**Real-world use case:**

| Scenario | Method |
|---|---|
| Password validation | equals — case important |
| Email / username validation | equalsIgnoreCase — case not important |

```java
String email = "User@Mail.com";
System.out.println(email.equalsIgnoreCase("user@mail.com"));
// Prints: true
```

**`equalsIgnoreCase`** — content comparison where **case is NOT important**; String-specific method (not on `Object`).

```java
public boolean equals(Object obj)           // case important
public boolean equalsIgnoreCase(String s)   // case NOT important
```

**Board example:**

```java
String s = "Java";
System.out.println(s.equals("java"));              // false
System.out.println(s.equalsIgnoreCase("java"));    // true
```

**Exam note:** Use `equalsIgnoreCase` to validate **usernames**; use `equals` to validate **passwords** where case matters.

### 28:50 — Method 4: `substring` — introduction via ABCDEFG example

String for substring demo (ASR: movie tagline joke — “A Boy Can Do Everything For Girl”):

```java
String s = "a b c d e f g";
// Or compact: "abcdefg" depending on board — lecture uses spaced form
```

**`substring(6)`** — from begin index **6** to **end of string**:

```java
String s = "a b c d e f g";
System.out.println(s.substring(6));
// Prints from index 6 to end → "g" (in spaced string) or "g" portion
```

**Two-argument form:**

```java
String s = "a b c d e f g";
System.out.println(s.substring(2, 6));
// From index 2 inclusive to index 6 EXCLUSIVE
// Indices 2,3,4,5 → "c d e" (with spaces) or "cdef" in compact form
// Lecture: begin=2, end=6 → characters at 2,3,4,5 only (end-1 rule)
```

**Common mistake (compile error):** wrong casing — `subString` with capital **S** is invalid. Must be **`substring`** (lowercase **s** after “sub”).

```java
// CE — cannot find symbol
// s.subString(2);   // WRONG

s.substring(2);        // CORRECT
```

### 33:56 — `substring` method signatures

```java
public String substring(int beginIndex)
// Returns substring from beginIndex to end of string

public String substring(int beginIndex, int endIndex)
// Returns substring from beginIndex to endIndex-1 (endIndex exclusive)
```

**Board example:**

```java
String s = "abcdefg";
System.out.println(s.substring(3));
// Prints: defg

System.out.println(s.substring(2, 6));
// Prints: cdef   (indices 2,3,4,5)
```

### 36:35 — Method 5: `length()` vs `length` variable

**Common confusion — arrays vs String:**

```java
String s = "Durga";
System.out.println(s.length);
// CE: cannot find symbol — length variable NOT for String

System.out.println(s.length());
// Prints: 5
```

| Feature | Applies to |
|---|---|
| `length` variable | Arrays only |
| `length()` method | String objects only |

```java
int[] a = {10, 20, 30};
System.out.println(a.length);    // 3 — variable

String s = "Durga";
System.out.println(s.length());  // 5 — method
```

Signature:

```java
public int length()
// Returns number of characters in the String
```

### 41:21 — Method 6: `replace(char oldChar, char newChar)`

Replace **every occurrence** of old character with new character; returns **new String** (immutability).

```java
String s = "abababa";
System.out.println(s.replace('a', 'b'));
// Prints: bbbbbbb
// Every 'a' replaced with 'b'
```

```java
public String replace(char oldChar, char newChar)
```

### 43:27 — Methods 7 & 8: `toLowerCase()` and `toUpperCase()`

Self-explanatory — convert case of all characters.

```java
public String toLowerCase()
// Every uppercase → lowercase

public String toUpperCase()
// Every lowercase → uppercase
```

No extra examples required on board — method names indicate purpose.

### 44:17 — Method 9: `trim()`

**Problem scenario:** User enters city name with leading/trailing spaces; database has `"Hyderabad"` but input is `"   Hyderabad"`. Comparison fails unless trimmed.

**Purpose:** Remove **blank spaces at beginning AND end** — **NOT** middle spaces.

```java
String city = "   Hyderabad   ";
System.out.println(city.trim());
// Prints: Hyderabad
// Leading and trailing spaces removed; middle spaces kept if any
```

**MCQ trap (exam):**

| Option | Correct? |
|---|---|
| Remove spaces only at beginning | ❌ |
| Remove spaces only at end | ❌ |
| Remove spaces at beginning and end | ✅ |
| Remove all spaces in string | ❌ |

Middle spaces **not** removed by `trim()`.

```java
public String trim()
// Remove blank spaces at beginning and end, NOT middle
```

### 48:36 — Methods 10 & 11: `indexOf(char)` and `lastIndexOf(char)`

**Reverse of `charAt`:** given character, find **index**.

- `charAt(index)` → character
- `indexOf(char)` → **first** occurrence index
- `lastIndexOf(char)` → **last** occurrence index
Only **first** and **last** have ready-made methods — for 2nd, 3rd occurrence you must write explicit code.

```java
String s = "ababa";
System.out.println(s.indexOf('a'));
// Prints: 0   (first 'a')

System.out.println(s.lastIndexOf('a'));
// Prints: 4   (last 'a')
```

Signatures:

```java
public int indexOf(char ch)
// Returns index of first occurrence of specified character

public int lastIndexOf(char ch)
// Returns index of last occurrence of specified character
```

### 52:57 — ★ MOST IMPORTANT: runtime String methods & object creation

**Exam trap:** People assume `==` on results of `toUpperCase()` / `toLowerCase()` always gives `false false` — **wrong** in some cases.

**Case A — literal references (SCP), no `new`:**

```java
String s1 = "durga";
String s2 = s1.toUpperCase();   // "DURGA" — content CHANGED → new heap object
String s3 = s1.toLowerCase();   // "durga" — no content change → SAME object

System.out.println(s1 == s2);   // false
System.out.println(s1 == s3);   // true  ← surprise for many students
```

**Case B — `new String()` → heap object:**

```java
String s1 = new String("Durga");   // heap object (literal "Durga" also in SCP)
String s2 = s1.toUpperCase();      // "DURGA" — change → NEW heap object
String s3 = s1.toLowerCase();      // "durga" — change → NEW heap object

System.out.println(s1 == s2);   // false
System.out.println(s1 == s3);   // false
```

**★ Golden rule (star note):**

> *Because of ***runtime operation***: if there is ***change in content*** → ***new object*** created in ***heap only*** (NOT SCP). If ***no change in content*** → ***existing object*** returned (reuse).*

Same rule whether object came from heap, SCP, or both.

### 57:16 — Extended `==` examples with heap + SCP diagram

```java
String s1 = new String("Durga");
String s2 = s1.toUpperCase();    // "DURGA" — new object
String s3 = s1.toLowerCase();    // "durga" — new object (content changed from "Durga")

System.out.println(s1 == s2);    // false
System.out.println(s1 == s3);    // false
```

When lowercase `"durga"` already exists in SCP, **`toLowerCase()` still may create new heap object** if called on heap `String` from `new String(...)` — because runtime method does **not** check SCP for reuse when source is heap object; it applies change rule on **current object content**.

### 1:03:00 — `s4 = s2.toLowerCase()` — new object even when SCP has match

```java
String s1 = new String("Durga");
String s2 = s1.toUpperCase();     // "DURGA" on heap
String s4 = s2.toLowerCase();   // "durga" — CHANGE from "DURGA" → NEW object

// Even if "durga" literal exists in SCP,
// runtime call on heap "DURGA" → new heap "durga" object
// Does NOT check "is lowercase already in SCP?"
```

**Key insight:** At runtime method call, JVM creates new object on heap when content changes — **does not** search SCP for existing equal string to reuse (for these transform methods on non-literal-derived references).

### 1:06:31 — `toString()` on String — no content change

```java
String s1 = "Durga";              // SCP
String s2 = s1.toString();        // already String, no change

System.out.println(s1 == s2);     // true — same object
```

```java
String s1 = "Durga";
String s3 = s1.toUpperCase();     // "DURGA" — but if already upper? 
// "Durga".toUpperCase() → "DURGA" — content changed → new object

String s1 = "DURGA";
String s3 = s1.toUpperCase();     // no change → same object
System.out.println(s1 == s3);     // true
```

**Summary table:**

| Operation | Content change? | Result |
|---|---|---|
| toString() on String | No | Same object |
| toUpperCase() when already upper | No | Same object |
| toLowerCase() when already lower | No | Same object |
| toUpperCase() / toLowerCase() / trim() / replace() when content differs | Yes | New heap object |

### 1:11:00 — Immutability definition (formal) + link to String behavior

**Immutability:** Once object created, if you try to “change” it via operation:

- **Content changes** → **new object** created with new content
- **No content change** → **existing object** reused
This **behavior IS immutability** for String. String class implements this pattern.

**Typo in ASR:** “mutable” at opening often means **immutable** in context — String objects are **immutable**.

### 1:11:39 — How to create our own immutable class

**Interview / OCJP question:** “How to create immutable class?” — implement same behavior as String.

**Step 1:** Understand immutability (above).

**Step 2:** Implement `modify`-style methods that return new object on change, same object on no change.

**Step 3:** Declare class **`final`** so nobody overrides your immutability logic.

### 1:18:12 — `Test` class: custom immutable class pattern

```java
public final class Test {
    private int x;

    public Test(int x) {
        this.x = x;
    }

    public Test modify(int x) {
        if (this.x == x) {
            return this;              // no change → reuse current object
        } else {
            return new Test(x);         // change → new object
        }
    }
}
```

**Usage:**

```java
Test t1 = new Test(10);
Test t2 = t1.modify(100);    // 10 != 100 → NEW Test(100) object
Test t3 = t1.modify(10);     // 10 == 10 → return t1 (same object)

System.out.println(t1 == t2);   // false
System.out.println(t1 == t3);   // true
```

**Why `final` class?**

- `String` is **final**
- All **wrapper classes** are **final**
- Prevents subclass from **overriding** methods and breaking immutability contract
### 1:24:14 — Immutability implementation rule (board summary)

Once object created:

- Any attempted change with **different content** → **new object**
- Same content → **return current object** (`return this`)
Immutability achieved through **method implementation**, not keyword alone.

### 1:30:02 — `final` vs `immutable` — DIFFERENT concepts

**Most common student mistake:** treating `final` and immutable as same — **they are NOT**.

| Concept | Applies to | Meaning |
|---|---|---|
| `final` variable | Variable / reference | Re-assignment not allowed |
| Immutability | Object | Object content cannot change; operations return new object |

**Both sound “non-changeable” but different dimensions.**

### 1:31:28 — `final StringBuffer` example — object CAN still change

```java
final StringBuffer sb = new StringBuffer("Durga");
sb.append(" Software");          // VALID — mutating object content
System.out.println(sb);
// Prints: Durga Software

// sb = new StringBuffer("Solutions");  // CE — cannot assign to final variable sb
```

**`final` impact:** only **reassignment** of `sb` forbidden. **Append/modify** object content allowed because `StringBuffer` is **mutable**.

Even if **two references** are `final`, still can mutate object:

```java
final StringBuffer sb = new StringBuffer("Durga");
sb.append(" Software");   // OK
System.out.println(sb);   // Durga Software
```

**Reassignment fails:**

```java
final StringBuffer sb = new StringBuffer("Durga");
sb = new StringBuffer("Solutions");
// CE: cannot assign a value to final variable sb
```

### 1:36:37 — Board notes: final vs immutability

**`final`:**

- Applicable for **variable** (reference)
- **Not** for making object immutable
- Declaring reference `final` → **no immutability** for object
- Even two `final` references → can still change **object content** if type is mutable
**Immutability:**

- Applicable for **object** behavior
- **Not** controlled by `final` keyword on variable alone
- String immutability from **class design** + **final class** + method behavior
**Non-final mutable example:**

```java
StringBuffer sb = new StringBuffer("Durga");
sb.append(" Software");                    // valid
System.out.println(sb);                    // Durga Software

sb = new StringBuffer("Solutions");        // also valid — not final
System.out.println(sb);                    // Solutions
```

### 1:41:18 — Quick review: four “meaningful” combinations (tick-mark exercise)

Durga Sir asks which phrases are meaningful:

| Phrase | Valid? | Reason |
|---|---|---|
| Final variable | ✅ Yes | final applies to variables |
| Null variable | ❌ Invalid phrase | Variables can hold null; “null variable” not standard terminology |
| Final object | ❌ Invalid | Objects aren’t declared final — references are |
| Null object | ✅ Yes | Reference pointing to no object |

**Important for interview + SCJP + day-to-day programming.**

### 1:42:52 — Session wrap-up

Topics completed:

1. String **constructors** (`()`, literal, StringBuffer, char[], char[]+offset+count, byte[])
1. String **methods** (charAt, concat/+/+=, equals/equalsIgnoreCase, substring, length, replace, toLowerCase/toUpperCase, trim, indexOf/lastIndexOf)
1. **Runtime object creation** rule for String methods (★ exam star)
1. **Custom immutable class** pattern (`Test` + `modify`)
1. **`final` vs immutable** distinction
Next session preview: more String topics / related `java.lang` content (Covariant return types mentioned in passing for future).

## Quick reference — String constructors covered

```java
new String()
new String(String original)
new String(StringBuffer sb)
new String(char[] value)
new String(char[] value, int offset, int count)
new String(byte[] bytes)
```

## Quick reference — String methods covered

```java
charAt(int index)
concat(String str)          // + and += equivalent for concatenation
equals(Object o)
equalsIgnoreCase(String s)
substring(int begin)
substring(int begin, int end)
length()
replace(char old, char new)
toLowerCase()
toUpperCase()
trim()
indexOf(char ch)
lastIndexOf(char ch)
toString()                  // on String → same object
```

**Java block count: 48**
