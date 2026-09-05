# Video 122

## Video info

Title: Core Java With OCJP/SCJP: File I/O Part-3 || FileReader || important methods || BufferedWriter

ASR decode key: file radar / file Rader / file leer → FileReader; Bufford / buffard / Prof → Buffered; typ casting → type casting; CE → checked exception; wi / qu → void; sop → System.out.println; compil → compile error; 10 lakh → 1,000,000 (Indian numbering); 1 CR → 10 million read ops in analogy.

## Part A — FileReader

### 00:05 — Introduction: reading after writing

Previous session: FileWriter — how to write character data to a file.

This session: FileReader — how to read character/text data from a file.

Name rule: FileReader — one word, no space.

Purpose: Read character data (text) from a file — e.g. "ABC", "Durga", any textual content.

```java
// Conceptual
FileReader fr = new FileReader("abc.txt");
// read character/text data from file
```

### 01:25 — FileReader constructors (only 2)

No append/override concept for reading — only two constructors.

Constructor 1 — file name:

```java
FileReader fr = new FileReader("abc.txt");
```

Constructor 2 — `File` reference:

```java
File f = new File("abc.txt");
FileReader fr = new FileReader(f);
```

Either pass String file name or existing `File` reference.

### 04:13 — FileReader methods overview

For reading → `read` methods.

Total methods in FileReader class covered: 3 (2 read + 1 close).

### 04:45 — `read()` — no-arg, returns `int` (Unicode value)

Sample file content (`abc.txt`): Durga + Software Solutions (ASR garbled as “u r g d software Solutions”).

Behavior:

- Each call reads next single character from file.
- 1st call → 'D' (Unicode 100)
- 2nd call → next char, etc.
- When no next character → returns `-1`
Return type is `int`, not `char` — returns Unicode numeric value of the character.

int i = fr.read();
// 1st call: i == 100  ('D')
// at EOF:     i == -1

Loop until `-1`:

```java
int i = fr.read();
while (i != -1) {
    System.out.print((char) i);   // type casting mandatory for readable output
    i = fr.read();
}
```

Without type casting: prints 100 117 114 ... (Unicode values) — not human-readable.

Board summary — `int read()`:

Attempts to read next character from the file and returns its Unicode value (int).

If next character not available → returns `-1`.

At printing time → type casting to `char` is compulsory.

### 07:34 — Demo approach 1: character-by-character loop

Target: Read all data in abc.txt.

```java
FileReader fr = new FileReader("abc.txt");
int i = fr.read();
while (i != -1) {
    System.out.print((char) i);
    i = fr.read();
}
fr.close();
```

Cycle stops when `i == -1` (end of file).

### 12:46 — `read(char[] c)` — read into char array

Signature: returns int (count of characters copied, not Unicode of one char).

Example A — array smaller than file:

char[] ch = new char[10];      // array size 10
// file has 1000 characters
int count = fr.read(ch);       // count == 10 (only 10 copied)

Example B — array larger than file:

char[] ch = new char[10000];   // array size 10000
// file has 1000 characters
int count = fr.read(ch);       // count == 1000

Board summary — `int read(char[] c)`:

Attempts to read enough characters from file into `c`.

Returns number of characters copied from file into the array.

Only 2 read methods in FileReader — no third overload.

### 17:32 — Problem: fixed array size (10 vs 10,000)

Good practice: Find file length first, then create array of exact size.

### 18:40 — `File.length()` and array sizing

```java
File f = new File("abc.txt");
char[] ch = new char[(int) f.length()];   // type cast long → int
FileReader fr = new FileReader(f);
fr.read(ch);

for (char ch1 : ch) {
    System.out.println(ch1);
}
```

Compile issue without cast:

char[] ch = new char[f.length()];  // ERROR

Compiler message (board):

possible loss of precision
found: long
required: int

Reason: Array size must be int; File.length() returns `long`.

Limitation: This approach works only if character count ≤ `Integer.MAX_VALUE`. If file exceeds int range → use character-by-character read() loop (approach 1).

### 23:29 — Third method: `close()`

After read or write → close is highly recommended.

fr.close();

FileReader method count: 2 × read + close = 3.

### 24:07 — FileReaderDemo.java (both approaches in one program)

Sample `abc.txt` content (board):

Durga
Software Solutions
Hyderabad 38

Approach 2 — array + enhanced for:

```java
File f = new File("abc.txt");
char[] ch = new char[(int) f.length()];
FileReader fr = new FileReader(f);
fr.read(ch);
for (char ch1 : ch) {
    System.out.println(ch1);
}
```

Separator on console: *** (Sir uses stars between approaches)

Approach 1 — while loop:

```java
FileReader fr1 = new FileReader("abc.txt");
int i = fr1.read();
while (i != -1) {
    System.out.print((char) i);
    i = fr1.read();
}
```

Compile & run (board):

> javac FileReaderDemo.java
> java FileReaderDemo

Console output (observed):

Durga
Software Solutions
Hyderabad 38
***
Durga
Software Solutions
Hyderabad 38

Type casting reminders:

- (int) f.length() for array size
- (char) i when printing from read()
### 31:40 — Recap: one writer + one reader so far

### 31:51 — Main problem with FileReader

Can read only character-by-character, not line-by-line.

Performance analogy:

- File has 10 lakh (1,000,000) mobile numbers, each 10 digits.
- To check if one number exists → compare digit by digit → 10 `read()` calls per number.
- For 10 lakh numbers → 10 lakh × 10 = 1 crore (10 million) read operations for one lookup.
Worst programming practice for real tasks that think in lines.

Need: Read line by line (1st line, 2nd line, …) → `BufferedReader` (later in this video).

Board note:

By using FileReader, we can read data character by character, which is not convenient to the programmer.

### 35:28 — FileWriter vs FileReader problems → use Buffered classes

Conclusion (underline for exam):

Usage of FileWriter and FileReader is NOT recommended in production-style code.

Use BufferedWriter and BufferedReader instead.

## Part B — BufferedWriter

### 39:44 — BufferedWriter purpose

Purpose: Write character data to file — same job as FileWriter.

Advantage: No manual `\n` for line breaks — call `newLine()` instead. Platform-specific line separator handled internally.

(Minor performance buffering exists internally, but Sir emphasizes convenience of `newLine()` over raw performance in this lecture.)

```java
// Conceptual
BufferedWriter bw = new BufferedWriter(/* Writer argument */);
```

### 41:07 — BufferedWriter constructors (2) — CRITICAL EXAM POINT

BufferedWriter CANNOT talk directly to a file.

Unlike FileWriter, you cannot pass file name or File object.

Must wrap another `Writer` (typically FileWriter).

Constructor 1:

```java
Writer w = new FileWriter("abc.txt");
BufferedWriter bw = new BufferedWriter(w);
```

Constructor 2 — with buffer size:

BufferedWriter bw = new BufferedWriter(w, bufferSize);  // int bufferSize

Usually don’t customize buffer size — use 1-arg form.

Pipeline diagram (board):

Program → BufferedWriter → FileWriter → abc.txt (file)

Invalid (compile error):

BufferedWriter bw = new BufferedWriter("abc.txt");           // INVALID
BufferedWriter bw = new BufferedWriter(new File("abc.txt")); // INVALID — File is not Writer

Valid:

BufferedWriter bw = new BufferedWriter(new FileWriter("abc.txt"));  // VALID

Valid (two-level buffering — optional performance):

BufferedWriter bw2 = new BufferedWriter(
    new BufferedWriter(new FileWriter("abc.txt")));  // VALID — nested buffers

Board note:

BufferedWriter can't communicate directly with the file.

It communicates via some Writer object only.

### 51:55 — BufferedWriter methods (6 total)

Same 5 as FileWriter:

6th — EXTRA method (exam favorite):

bw.newLine();   // inserts platform-specific line separator

Exam bit question: *Which capability is available extra in BufferedWriter compared to FileWriter?*

Answer: Inserting a new line character (newLine() method).

### 57:01 — BufferedWriterDemo.java

```java
import java.io.*;

class BufferedWriterDemo {
    public static void main(String[] args) throws Exception {
        FileWriter fw = new FileWriter("abc.txt");
        BufferedWriter bw = new BufferedWriter(fw);

        bw.write(100);              // 'd'
        bw.newLine();
        bw.write("ABCD");           // char[] or string — board uses char[] {'A','B','C','D'}
        bw.newLine();
        bw.write("Durga");
        bw.newLine();
        bw.write("Software Solutions");

        bw.flush();
        bw.close();                 // only bw.close() in demo — see closing rules below
    }
}
```

Expected `abc.txt`:

d
ABCD
Durga
Software Solutions

Compile & run:

> javac BufferedWriterDemo.java
> java BufferedWriterDemo

Console: no output. File contains formatted lines (actual newlines, not literal \n text).

### 1:03:23 — Closing order: FileWriter + BufferedWriter

Open order: FileWriter first → then BufferedWriter on top.

Close options:

Rule:

When closing BufferedWriter, the underlying FileWriter is closed automatically.

No need to close `fw` explicitly.

Same pattern applies to BufferedReader + FileReader later.

## Part C — BufferedReader

### 1:07:55 — BufferedReader purpose & advantage

Purpose: Read character data from file (like FileReader).

Main advantage over FileReader:

Can read line by line in addition to character-by-character.

“Most enhanced reader” (Sir’s phrase) for text files — prefer BufferedReader for reading.

### 1:09:51 — Main advantage (board)

The main advantage of BufferedReader when compared with FileReader is:

we can read data line by line, in addition to character by character.

### 1:11:02 — BufferedReader constructors (2)

Same rule as BufferedWriter: Cannot connect directly to file — needs a `Reader`.

```java
Reader r = new FileReader("abc.txt");
BufferedReader br = new BufferedReader(r);

// with buffer size:
BufferedReader br = new BufferedReader(r, bufferSize);
```

Board note:

BufferedReader can't communicate directly with the file.

It communicates via some Reader object.

### 1:14:14 — BufferedReader methods (4 total)

Same 3 as FileReader:

4th — SPECIAL (line reading):

```java
String line = br.readLine();
```

Behavior:

- Each call → next line as String (without line terminator chars).
- 1st call → line 1, 2nd → line 2, etc.
- When no next line → returns `null` (not -1).
Loop until `null`:

```java
String line = br.readLine();
while (line != null) {
    System.out.println(line);
    line = br.readLine();
}
```

Board summary — `String readLine()`:

Attempts to read next line from file and returns it.

If next line not available → returns `null`.

### 1:17:46 — BufferedReaderDemo.java

Sample file:

Durga
Software Solutions
Sr nagar
Hyderabad 38

Program:

```java
import java.io.*;

class BufferedReaderDemo {
    public static void main(String[] args) throws Exception {
        FileReader fr = new FileReader("abc.txt");
        BufferedReader br = new BufferedReader(fr);

        String line = br.readLine();
        while (line != null) {
            System.out.println(line);
            line = br.readLine();
        }

        br.close();    // closes underlying FileReader too
    }
}
```

Compile & run:

> javac BufferedReaderDemo.java
> java BufferedReaderDemo

Console output (observed):

Durga
Software Solutions
Sr nagar
Hyderabad 38

Best/simple approach to read text files line-by-line.

### 1:23:31 — Closing BufferedReader

Same as writer side:

When closing BufferedReader, underlying FileReader is closed automatically — no explicit fr.close() required.

### 1:25:07 — Session wrap-up

Most enhanced reader for character data: BufferedReader

Pipeline patterns:

Write:  BufferedWriter → FileWriter → file
Read:   BufferedReader → FileReader → file

## Exam quick-reference bits

### Valid / invalid BufferedWriter creation

new BufferedWriter("abc.txt");                              // INVALID
new BufferedWriter(new File("abc.txt"));                    // INVALID
new BufferedWriter(new FileWriter("abc.txt"));              // VALID
new BufferedWriter(new BufferedWriter(new FileWriter("abc.txt"))); // VALID

### EOF sentinels

### Type casting required

Java code block count: 26

## Tables (placement lost -- re-place these in context)

| Field | Value |
|---|---|
| Playlist | Java tutorial by Durga Sir |
| Position | 122 of 203 |
| Series | Core Java With OCJP/SCJP |
| Topic | File I/O — FileReader, BufferedWriter, BufferedReader |
| Instructor | Durga Sir |
| Duration | 1h 26m 19s (from transcript) |
| Video ID | Zw71nmiWkJ0 |
| Watch | https://www.youtube.com/watch?v=Zw71nmiWkJ0 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

| Array size | Problem |
|---|---|
| 10 | File may have more chars → incomplete read |
| 10,000 | File may have fewer → memory waste (e.g. 9000 slots unused) |

| Role | Class covered |
|---|---|
| Writer | FileWriter (prev video) |
| Reader | FileReader (this video) |

| Class | Problem |
|---|---|
| FileWriter | Must insert line separator manually ("\n"), varies system to system |
| FileReader | Only character-by-character read |

| # | Method | Purpose |
|---|---|---|
| 1 | write(int ch) | Single character |
| 2 | write(char[] c) | Char array |
| 3 | write(String s) | String |
| 4 | flush() | Flush buffer |
| 5 | close() | Close |

| Option | Code | Recommended? |
|---|---|---|
| 1 | bw.close() only | YES — highly recommended |
| 2 | fw.close() only | NO — BufferedWriter still open; may get “stream already closed” if writing later |
| 3 | bw.close(); fw.close(); | Redundant — not wrong but unnecessary |

| Method | Purpose |
|---|---|
| int read() | Next char as Unicode int; -1 at EOF |
| int read(char[] c) | Read into array; returns count |
| close() | Close reader |

| Class | Role | Direct to file? | Key extra method |
|---|---|---|---|
| FileReader | Basic read | Yes | — |
| BufferedReader | Enhanced read | No (via Reader) | readLine() |
| FileWriter | Basic write | Yes | — |
| BufferedWriter | Enhanced write | No (via Writer) | newLine() |

| API | End signal |
|---|---|
| FileReader.read() | -1 |
| BufferedReader.readLine() | null |

| Situation | Cast |
|---|---|
| Print read() result | (char) i |
| Array size from f.length() | (int) f.length() |
