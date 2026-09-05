# Video 149 — Collections Part-14: Hashtable & Properties

## Video info

## Session overview

This lecture completes the Map half of the Collections Framework by covering the two remaining legacy (Java 1.0) map-related classes:

- Hashtable — full property sheet, four constructors, and a memory-level demo proving how hash codes determine bucket placement and print order
- Properties — real-time importance of externalizing configuration, the Properties class API (load/store), and JDBC-style usage patterns
Sir explicitly states that most Hashtable terminology is already familiar from HashMap/HashSet sessions — the minor differences (default capacity 11, full synchronization, null rejection) are the exam focus.

After this video, the entire Map concept is completed. The next Collections topic is Queue.

## 00:05 — Recap: Map classes already covered

Before starting legacy classes, Sir recaps everything covered in prior Map sessions (no re-explanation needed):

Remaining legacy Map-related classes (this session):

Note: Dictionary is an abstract legacy class — Sir skips it because abstract classes are not used directly (same decision as in Video 146 agenda).

## 01:00 — Hashtable introduction

### Underlying data structure

Hashtable (Java class) is implemented based on Hashtable (data structure).

Same naming convention as HashMap → hash table, HashSet → hash table. The Java class name matches the standard CS data structure name.

### Hashtable — complete property sheet (board conclusions)

Copy these exactly — they mirror HashMap with critical differences highlighted:

Board wording (exact phrases Sir repeats):

- "Null — such a type of story — not applicable for the key, not applicable for the value."
- "Otherwise we will get runtime exception saying NullPointerException."
- "Every method present in Hashtable is synchronized, and hence Hashtable object is thread-safe."
- "Hashtable is the best choice if our frequent operation is search operation."
### Why these points feel familiar

Sir acknowledges: "More or less all points are our known points only… most of the times we covered already with respect to some other [class]. Small minor differences only."

You are near the end of Collections — Hashtable is essentially HashMap + synchronization + stricter null rules + different default capacity.

## 09:35 — Hashtable constructors (VERY IMPORTANT)

Hashtable has four constructors — same pattern as HashMap and HashSet:

Hashtable h = new Hashtable();
Hashtable h = new Hashtable(int initialCapacity);
Hashtable h = new Hashtable(int initialCapacity, float fillRatio);
Hashtable h = new Hashtable(Map m);   // conversion from another Map

### Constructor details table

### ⚠️ EXAM TRAP: Default initial capacity is 11, NOT 16

All three use default fill ratio 0.75.

Sir emphasizes: "If it is HashSet — 16. If it is HashMap — 16. But if it is Hashtable — 11 only. Remember."

## 15:13 — Memory-level demo: How hash code determines storage

Sir goes deeper than theory — a programmatic proof showing exactly where each entry lands in buckets and what System.out.println(h) prints.

"Being programmer, not required to talk this much — but having the basic idea is always essential."

### Step 1: Custom `Temp` class (controlled hash codes)

Sir deliberately overrides `hashCode()` so hash codes are predictable (not relying on Object.hashCode()):

```java
class Temp {
    int i;
    Temp(int i) { this.i = i; }

    public int hashCode() {
        return i;   // hash code = the int value passed to constructor
    }

    public String toString() {
        return i + "";   // prints the int value (i + "" converts int to String)
    }
}
```

Why `i + ""` instead of returning `i` directly?

- toString() return type must be String
- i is int — compiler error if you return i;
- i + "" concatenates int with empty string → String result
Example: Temp t1 = new Temp(10); → hash code of t1 is 10.

### Step 2: Insert key–value pairs into Hashtable

```java
Hashtable h = new Hashtable();

h.put(new Temp(5),  "A");
h.put(new Temp(2),  "B");
h.put(new Temp(6),  "C");
h.put(new Temp(15), "D");
h.put(new Temp(23), "E");
h.put(new Temp(16), "F");
// h.put(null, "X");  // commented — would throw NullPointerException

System.out.println(h);
```

### Step 3: Bucket model (default capacity = 11)

Default constructor → 11 buckets, indexed 0 through 10.

Technical term: Sir uses "bucket" — this is the official hashing terminology, not casual language.

Placement rule: For each key, compute hashCode, then determine bucket index. When hash code ≥ capacity, use modulo:

Collision handling: Multiple entries can exist in the same bucket — linked within the bucket. Bucket 5 holds both 5=A and 16=F.

### Bucket diagram (default demo)

Bucket index:  0    1       2       3    4        5              6       7   8   9   10
               .   23=E    2=B     .   15=D    5=A → 16=F       6=C     .   .   .   .

### Step 4: Print order formula (CRITICAL for exam)

When you print a Hashtable (System.out.println(h)), iteration order follows:

From top to bottom (higher bucket index → lower bucket index)

Within a bucket: from right to left (most recently added entry first)

Sir's exact words: "From top to bottom… within a bucket, multiple entries — from right to left."

Applying the formula to buckets 10 → 0:

### Expected program output (Demo 1)

```java
{6=C, 16=F, 5=A, 15=D, 2=B, 23=E}
```

Sir runs the program live — output matches exactly.

### Key takeaways from Demo 1

- Entries are stored based on hash code of keys (not values).
- When hash code ≥ initial capacity, bucket = hashCode % capacity.
- Collisions place multiple entries in one bucket.
- Print order ≠ insertion order — follows top-to-bottom, right-to-left rule.
- If you know all hash codes and capacity, you can predict exact output.
## 27:29 — Null value demo → NullPointerException

Sir tests null rules:

h.put(new Temp(5), null);   // null VALUE — compiles fine

Runtime result:

Exception in thread "main" java.lang.NullPointerException

"Null — such a type of story — not applicable for Hashtable."

Both null key and null value are rejected at runtime with NullPointerException.

## 34:13 — Demo 2: Changing hashCode formula (`return i % 9`)

Sir modifies only the hashCode() method:

```java
public int hashCode() {
    return i % 9;
}
```

Same entries, same default capacity (11), new hash codes:

Print order (top → bottom, right → left):

```java
{16=F, 15=D, 6=C, 23=E, 5=A, 2=B}
```

Board conclusion:

If we change hashCode method of key class → automatically there is a change in output.

Live execution confirms: 16=F, 15=D, 6=C, 23=E, 5=A, 2=B ✓

## 41:04 — Demo 3: Changing initial capacity to 25

Sir keeps return i but changes constructor:

Hashtable h = new Hashtable(25);   // 25 buckets: indices 0–24

Placement (hash codes fit directly into buckets 0–24):

No collisions — each entry gets its own bucket.

Print order (buckets 24 → 0):

```java
{23=E, 16=F, 15=D, 6=C, 5=A, 2=B}
```

Live execution confirms ✓

Board conclusion:

If we configure initial capacity as 25 → corresponding change in output (because number of buckets changed, so bucket assignment changes).

### Summary of three demo variations

## 48:19 — Hashtable concept complete → transition to Properties

Sir closes Hashtable with:

"Based on hash code of the keys, the entries will be saved in Hashtable. Practical proof for you people."

Next topic: Properties — described as "the most valuable concept, especially for real-time coding and day-to-day programming."

## 48:28 — Properties: Why externalize configuration?

### The hardcoding problem

Suppose you write a Java program and hardcode database credentials:

```java
String username = "Scott";
String password = "tiger";
```

Client requirement: Every 3 months, database username/password must change (security constraint).

To change tiger → tiger123 in the Java source file, you must:

Total downtime: 2–3 hours minimum per change.

Business impact: Application down for 3 hours = significant financial loss for the client.

Sir's examples of hardcoded values that change frequently:

- Database username / password
- Mail IDs
- Mobile numbers
- Even punctuation (comma → semicolon, dot → comma)
"For every small change we have to do this — minimum 2 to 3 hours time must be required."

### The properties file solution

Rule: If anything changes frequently → never hardcode in Java program.

Instead, configure in a properties file:

# db.properties
username=Scott
password=tiger
db.url=jdbc:oracle:thin:@localhost:1521:xe
driver.class.name=oracle.jdbc.driver.OracleDriver

Workflow:

- Configure variable data in .properties file
- From Java program → read values from properties file
- Use read values in application logic
When properties file changes (e.g., password tiger → tiger123):

"Just redeployment is enough — which won't create big business impact to the client."

Real-world truth: "In real time, any application without having properties file — there is no chance of expecting any Java-based application." Not only Java — every programming language uses config files.

## 55:00 — Properties class: Role in the architecture

┌─────────────────────┐         load()          ┌──────────────────────┐
│  abc.properties     │  ───────────────────►   │  Java Properties     │
│  (on disk)          │                         │  object (in memory)  │
│                     │  ◄───────────────────   │                      │
└─────────────────────┘         store()          └──────────────────────┘
                                                          │
                                                          │ getProperty()
                                                          ▼
                                                   Java application code

Purpose of Properties object:

"We can use Java Properties object to hold properties which are coming from properties file."

- Load all properties from file → into Properties object (load)
- Read individual values from Properties object (getProperty)
- Optionally write changes back to file (store)
Package: java.util.Properties

## 01:04:03 — Properties vs normal Map: String-only restriction

Properties is a Map (key–value pairs), but with one critical restriction:

Board wording:

"In normal map — key and value can be any type. But in the case of Properties — key and value should be string type only."

Property name = key (String). Property value = value (String).

Both are compulsory and both must be String.

## 01:06:47 — Properties constructor

Only one constructor discussed:

```java
Properties p = new Properties();
```

Creates an empty Properties object (empty Map with String–String restriction).

## 01:07:20 — Properties methods

### Method 1: `String getProperty(String propertyName)`

- Purpose: Given a property name (key), return the corresponding property value.
- Return type: String
- If property not available: returns `null`
String user = p.getProperty("username");    // e.g., "Scott"
String pass = p.getProperty("password");    // e.g., "tiger"
String missing = p.getProperty("unknown");  // null

Most commonly used method in real projects.

### Method 2: `String setProperty(String propertyName, String propertyValue)`

- Purpose: Add a new property (or update existing).
- Behavior: Like Map.put() — if key already exists, old value replaced with new value, and old value is returned.
- Return type: String (the old value, or null if key was new)
```java
String old = p.setProperty("nag", "8888");
```

Sir notes: Usually Properties object is used to read, not write — but setProperty exists for rare cases.

### Method 3: `Enumeration propertyNames()`

- Purpose: Returns all property names present in the Properties object.
- Return type: Enumeration (legacy — old naming convention, not getPropertyNames())
- Usage pattern: Iterate property names → call getProperty(name) for each value
```java
Enumeration e = p.propertyNames();
while (e.hasMoreElements()) {
    String name = (String) e.nextElement();
    String value = p.getProperty(name);
    System.out.println(name + " = " + value);
}
```

### Method 4: `void load(InputStream is)` ⭐ VERY IMPORTANT

- Purpose: Load all properties from a properties file (via InputStream) into the Java Properties object.
- Direction: File → Properties object
FileInputStream fis = new FileInputStream("abc.properties");
p.load(fis);
// After this line, Properties object contains ALL entries from the file

### Method 5: `void store(OutputStream os, String comment)` ⭐ VERY IMPORTANT

- Purpose: Store properties from Java Properties object back into a properties file.
- Direction: Properties object → File
- Comment parameter: Written as a header comment in the output file (e.g., "updated by durga for OCJP demo class")
- File also gets a timestamp of when it was updated
```java
FileOutputStream fos = new FileOutputStream("abc.properties");
p.store(fos, "updated by durga for OCJP demo class");
```

### Properties methods summary table

## 01:19:07 — Properties file naming convention

- Convention: abc.properties, db.properties, log4j.properties
- Extension .properties is convention only — not enforced by Java
- Java file concept follows Unix: extension is not important
- Acceptable alternatives: abc.xml, abc.txt, abc.dat — anything works
- Convention exists for readability only
## 01:20:27 — Demo 1: PropertiesDemo (full program)

### abc.properties (input file)

user=Scott
winky=9999
password=tiger

### PropertiesDemo.java

```java
import java.util.*;
import java.io.*;

public class PropertiesDemo {
    public static void main(String[] args) throws Exception {
        Properties p = new Properties();

        FileInputStream fis = new FileInputStream("abc.properties");
        p.load(fis);   // load all properties from file into p

        System.out.println(p);                              // all key-value pairs
        System.out.println(p.getProperty("winky"));       // 9999

        p.setProperty("nag", "8888");   // add new property

        FileOutputStream fos = new FileOutputStream("abc.properties");
        p.store(fos, "updated by durga for OCJP demo class");
    }
}
```

### Program output

```java
{user=Scott, winky=9999, password=tiger}
9999
```

### abc.properties AFTER store()

The file now contains:

#updated by durga for OCJP demo class
#Sun Sep 21 ... (timestamp)
user=Scott
winky=9999
password=tiger
nag=8888

Observations:

- Comment from store() second parameter appears in file
- Timestamp of update is automatically added
- New property nag=8888 is persisted to file
- Order in file/output is not insertion order — based on hash code of keys (because Properties extends Hashtable internally)
### Live proof: Change properties file WITHOUT recompiling

Sir manually edits abc.properties:

password=tiger123

Then runs the already compiled program again (no recompile):

9999                    // winky still 9999
password → tiger123     // updated value picked up automatically

"Can I require to recompile? No. Automatically it should be reflected."

This is the power of properties files.

## 01:26:44 — JDBC anti-pattern vs best practice

Sir warns against hardcoding in JDBC programs:

```java
// ❌ BAD — hardcoded (common beginner mistake)
Connection con = DriverManager.getConnection(
    "jdbc:oracle:thin:@localhost:1521:xe", "Scott", "tiger");
```

Recommended approach:

```java
// ✅ GOOD — read from db.properties
Properties p = new Properties();
FileInputStream fis = new FileInputStream("db.properties");
p.load(fis);

String url  = p.getProperty("url");
String user = p.getProperty("username");
String pass = p.getProperty("password");

Connection con = DriverManager.getConnection(url, user, pass);
```

### db.properties example

username=Scott
password=tiger
url=jdbc:oracle:thin:@localhost:1521:xe
driver.class.name=oracle.jdbc.driver.OracleDriver

Flexibility: Change properties file to MySQL values → same Java program works with MySQL without code changes.

## 01:31:41 — Demo 2: PropertiesDemo2 (JDBC pseudo-code)

Sir shows the real-world pattern (pseudo-code for enterprise applications):

```java
import java.util.*;
import java.io.*;
import java.sql.*;

public class PropertiesDemo2 {
    public static void main(String[] args) throws Exception {
        Properties p = new Properties();
        FileInputStream fis = new FileInputStream("db.properties");
        p.load(fis);

        String url  = p.getProperty("url");
        String user = p.getProperty("username");
        String pass = p.getProperty("password");

        Connection con = DriverManager.getConnection(url, user, pass);
        // ... use connection ...
    }
}
```

Typical JDBC properties required:

"Don't hardcode anything in the Java program. This type of approach is always recommended."

## 01:36:08 — Session wrap-up

### Map module status: COMPLETED ✓

All Map-related topics from the syllabus are now done:

### Next topic

"Next what we have to discuss — Queue. In Collections, one more remaining part — Queue. That part we will discuss."

## Hashtable vs HashMap — complete comparison (exam table)

Interview one-liner: "Hashtable is legacy, synchronized, null-hostile, default capacity 11. HashMap is modern, unsynchronized, null-tolerant, default capacity 16. For thread-safe HashMap, use `Collections.synchronizedMap()` — don't default to Hashtable."

## OCJP / SCJP exam rapid-fire Q&A

## What's next (Video 150+)

Per session closing:

- Queue — remaining part of Collections Framework
- Collections utility classes (if not yet covered)
- Arrays class (Video 153 per playlist)
## Board diagrams to reproduce

### Diagram 1: Hashtable bucket layout (Demo 1, capacity 11)

Index:  0     1      2     3     4       5            6      7-10
        empty 23=E   2=B   empty 15=D   5=A←→16=F     6=C    empty

Print order: 6=C → 16=F → 5=A → 15=D → 2=B → 23=E
Rule: top→bottom buckets, right→left within bucket

### Diagram 2: Properties architecture

.properties file  ──load()──►  Properties object  ──getProperty()──►  Application
                               ◄──store()──

### Diagram 3: Hardcode vs Properties file workflow

Hardcoded in .java:
  Change → Recompile → Rebuild → Redeploy → Restart server (2-3 hours)

Properties file:
  Change → Redeploy only (2-3 minutes)

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Title | Core Java With OCJP/SCJP: Collections Part-14 \ | \ | hashtable |
| URL | https://www.youtube.com/watch?v=rfpvtTwWFK0 |  |  |
| Video ID | rfpvtTwWFK0 |  |  |
| Duration | 1h 36m 34s |  |  |
| Position | Video 149 of 203 in the Durga Sir OCJP/SCJP playlist |  |  |
| Source | YouTube auto-generated captions (yt-dlp + node PO token) |  |  |
| Prerequisite | Videos 146–148 (HashMap, LinkedHashMap, IdentityHashMap, WeakHashMap, SortedMap, TreeMap) |  |  |

| # | Class / Interface | Status |
|---|---|---|
| 1 | HashMap | ✓ Completed |
| 2 | LinkedHashMap | ✓ Completed |
| 3 | IdentityHashMap | ✓ Completed |
| 4 | WeakHashMap | ✓ Completed |
| 5 | SortedMap (interface) | ✓ Completed |
| 6 | TreeMap (implementation) | ✓ Completed |

| # | Class | Java version |
|---|---|---|
| 1 | Hashtable | 1.0 (legacy) |
| 2 | Properties | 1.0 (legacy, extends Hashtable) |

| # | Property | Hashtable value | HashMap comparison |
|---|---|---|---|
| 1 | Underlying data structure | Hash table | Same |
| 2 | Insertion order | Not preserved — based on hash code of keys | Same rule |
| 3 | Duplicate keys | Not allowed | Same |
| 4 | Duplicate values | Allowed | Same |
| 5 | Heterogeneous objects | Allowed for both keys and values | Same |
| 6 | Null key / null value | NOT allowed for key OR value → NullPointerException | HashMap: null key once, null values unlimited |
| 7 | Implements | Serializable and Cloneable | Same |
| 8 | RandomAccess | No | Same |
| 9 | Synchronization | Every method is synchronized → object is thread-safe | HashMap: not synchronized |
| 10 | Best choice when | Frequent operation is search / retrieval | Same recommendation |

| # | Signature | Creates | Default initial capacity | Default fill ratio |
|---|---|---|---|---|
| 1 | new Hashtable() | Empty Hashtable | 11 | 0.75 |
| 2 | new Hashtable(int initialCapacity) | Empty Hashtable | user-specified | 0.75 |
| 3 | new Hashtable(int initialCapacity, float fillRatio) | Empty Hashtable | user-specified | user-specified |
| 4 | new Hashtable(Map m) | Hashtable from existing Map entries | depends on m | 0.75 |

| Class | Default initial capacity |
|---|---|
| HashMap | 16 |
| HashSet | 16 |
| Hashtable | 11 |

| Key object | hashCode | Bucket index | Entry stored |
|---|---|---|---|
| new Temp(5) | 5 | 5 (5 < 11) | 5 = A |
| new Temp(2) | 2 | 2 | 2 = B |
| new Temp(6) | 6 | 6 | 6 = C |
| new Temp(15) | 15 | 15 % 11 = 4 | 15 = D |
| new Temp(23) | 23 | 23 % 11 = 1 | 23 = E |
| new Temp(16) | 16 | 16 % 11 = 5 | 16 = F (collision with 5=A) |

| Bucket | Entries (right → left) | Printed |
|---|---|---|
| 6 | 6=C | 6=C |
| 5 | 16=F, 5=A | 16=F, then 5=A |
| 4 | 15=D | 15=D |
| 2 | 2=B | 2=B |
| 1 | 23=E | 23=E |

| Key | hashCode (i % 9) | Bucket |
|---|---|---|
| Temp(5) | 5 | 5 |
| Temp(2) | 2 | 2 |
| Temp(6) | 6 | 6 |
| Temp(15) | 15 % 9 = 6 | 6 (collision with 6=C) |
| Temp(23) | 23 % 9 = 5 | 5 (collision with 5=A) |
| Temp(16) | 16 % 9 = 7 | 7 |

| Key | hashCode | Bucket |
|---|---|---|
| Temp(5) | 5 | 5 |
| Temp(2) | 2 | 2 |
| Temp(6) | 6 | 6 |
| Temp(15) | 15 | 15 |
| Temp(23) | 23 | 23 |
| Temp(16) | 16 | 16 |

| Demo | hashCode() | Initial capacity | Output |
|---|---|---|---|
| 1 (default) | return i | 11 (default) | {6=C, 16=F, 5=A, 15=D, 2=B, 23=E} |
| 2 (formula change) | return i % 9 | 11 (default) | {16=F, 15=D, 6=C, 23=E, 5=A, 2=B} |
| 3 (capacity change) | return i | 25 | {23=E, 16=F, 15=D, 6=C, 5=A, 2=B} |

| Step | Activity | Time impact |
|---|---|---|
| 1 | Edit .java source file | — |
| 2 | Recompile | Required |
| 3 | Rebuild application (EAR / WAR / JAR) | Required |
| 4 | Redeploy new EAR/WAR to server | Required |
| 5 | Restart server (often required for web/enterprise apps) | Required |

| Activity | Required? |
|---|---|
| Recompile | ❌ No |
| Rebuild | ❌ No |
| Restart server | ❌ No (usually) |
| Redeploy only | ✅ Yes — ~2–3 minutes |

| Map type | Key type | Value type |
|---|---|---|
| HashMap, Hashtable, TreeMap, etc. | Any type | Any type |
| Properties | String only | String only |

| Method | Return type | Purpose |
|---|---|---|
| getProperty(String name) | String | Get value for property name; returns null if missing |
| setProperty(String name, String value) | String | Set/add property; returns old value |
| propertyNames() | Enumeration | All property names in the object |
| load(InputStream is) | void | Load from properties file → object |
| store(OutputStream os, String comment) | void | Store from object → properties file |

| Property | Example value |
|---|---|
| url | jdbc:oracle:thin:@localhost:1521:xe |
| username | Scott |
| password | tiger |
| driver.class.name | oracle.jdbc.driver.OracleDriver |

| Topic | Status |
|---|---|
| HashMap, LinkedHashMap, IdentityHashMap, WeakHashMap | ✓ |
| SortedMap, TreeMap | ✓ |
| Hashtable | ✓ (this session) |
| Properties | ✓ (this session) |

| # | Point | HashMap | Hashtable |
|---|---|---|---|
| 1 | Introduced in | Java 1.2 | Java 1.0 (legacy) |
| 2 | Underlying DS | Hash table | Hash table |
| 3 | Insertion order | Not preserved (hash code of keys) | Not preserved (hash code of keys) |
| 4 | Duplicate keys | Not allowed | Not allowed |
| 5 | Null key | Allowed (once) | Not allowed → NPE |
| 6 | Null value | Allowed (multiple) | Not allowed → NPE |
| 7 | Synchronization | Not synchronized | All methods synchronized |
| 8 | Thread-safe? | No (use Collections.synchronizedMap()) | Yes |
| 9 | Performance | Faster (no sync overhead) | Slower (sync overhead) |
| 10 | Default initial capacity | 16 | 11 |
| 11 | Default fill ratio | 0.75 | 0.75 |
| 12 | Constructors | 4 | 4 (same pattern) |
| 13 | Implements | Serializable, Cloneable | Serializable, Cloneable |
| 14 | RandomAccess | No | No |
| 15 | Best for | Frequent search | Frequent search |

| # | Question | Answer |
|---|---|---|
| 1 | Underlying data structure of Hashtable? | Hash table |
| 2 | Default initial capacity of Hashtable? | 11 (not 16) |
| 3 | Default fill ratio? | 0.75 |
| 4 | Is Hashtable thread-safe? | Yes — every method synchronized |
| 5 | Null key allowed in Hashtable? | No → NullPointerException |
| 6 | Null value allowed in Hashtable? | No → NullPointerException |
| 7 | How many constructors in Hashtable? | Four |
| 8 | Hashtable print order rule? | Top to bottom (buckets), right to left (within bucket) |
| 9 | Properties extends which class? | Hashtable |
| 10 | Properties key/value type restriction? | Both must be String |
| 11 | How to load properties file into object? | p.load(InputStream) |
| 12 | How to save Properties object to file? | p.store(OutputStream, comment) |
| 13 | getProperty() returns what if key missing? | null |
| 14 | propertyNames() return type? | Enumeration |
| 15 | Why use properties file over hardcoding? | Avoid recompile/rebuild/redeploy/restart cycle |
