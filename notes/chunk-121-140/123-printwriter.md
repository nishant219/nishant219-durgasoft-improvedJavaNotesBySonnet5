# Video 123

## Video info

Title: Core Java With OCJP/SCJP: File I/O Part-4 || PrintWriter

Position: 123 of 203

Duration: 1h 08m 13s

Video ID: JN7-L3ZEnTw

Watch: https://www.youtube.com/watch?v=JN7-L3ZEnTw

Playlist: Java tutorial by Durga Sir — https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0

Transcript source: Local Whisper STT (.transcripts/123-JN7-L3ZEnTw.txt)

ASR decode key: file letter / FW → FileWriter; buffer writer / bufford writer / BW → BufferedWriter; print writer / PW → PrintWriter; print off / print of → print(); print line / print ln / printelen → println(); new line → newLine(); athima / atima → automatically; CE → compile-time error; five / 5 → file; redder / radar → reader; file niche / file midge / file netch → file merge; Tribulier / 3-Bull → sample line labels on board (a, b, c / 312, 313…).

## Session overview

This video completes the writer side of File I/O by introducing PrintWriter — the third and most enhanced writer after FileWriter and BufferedWriter. Durga Sir also:

- Recaps why FileWriter/BufferedWriter are insufficient for everyday programming
- Covers PrintWriter constructors, inherited methods, and the powerful print() / println() overloads
- Runs PrintWriterDemo1 with a critical print() vs println() vs write() exam trap
- Revisits character data vs binary data and the Reader/Writer vs Stream split
- Draws the full java.io hierarchy (Object → Writer/Reader → concrete classes)
- Implements two file merge applications (sequential merge + alternating line-by-line merge with null-checking)
Exam one-liner: Wherever writing character/text data is required → use PrintWriter. Wherever reading character/text data is required → use BufferedReader.

### 00:04 — Why PrintWriter when Writer already exists?

Student question: FileWriter and BufferedWriter already exist — why one more writer?

Two unresolved problems even after BufferedWriter:

#### Problem 1 — Line separator is still awkward

BufferedWriter solved the portable-newline problem with newLine(), but:

- Programmer must still call a separate method for every line break
- Manually writing \ + n in a string is still possible but platform-dependent and error-prone
- Calling newLine() per line is better than `\n`, but still extra work on every line
#### Problem 2 — Cannot write primitive values directly (FileWriter & BufferedWriter)

FileWriter (and BufferedWriter, which inherits Writer API) exposes only three `write` overloads:

There is no write(int i), write(double d), write(boolean b), etc.

Consequence — numeric trap (exam favorite):

FileWriter fw = new FileWriter("abc.txt");
fw.write(100);        // writes 'd' (Unicode 100), NOT the number 100
fw.write(10.5);       // CE — no write(double)
fw.write(true);       // CE — no write(boolean)

To write the numeric value 100, 10.5, or true as text, you must convert to String first:

fw.write(String.valueOf(100));   // works but creates String object
fw.write("10.5");                // works
fw.write("true");                // works

Problems with String conversion:

- Extra String object creation → performance hit
- Extra memory usage
- Programmer's intent was "write 100", not "create a String and write it"
PrintWriter solves both problems — next level / most enhanced writer for character output.

### 03:50 — PrintWriter introduction

Class: java.io.PrintWriter

Main advantage over FileWriter and BufferedWriter:

We can write any type of primitive data (and String, char, Object via print/println) directly to the file — no mandatory String conversion.

The magic method: print(...)

PrintWriter pw = new PrintWriter("abc.txt");
pw.print(100);       // writes 100 (not 'd')
pw.print(10.5);      // writes 10.5
pw.print(true);      // writes true
pw.print('c');       // writes c
pw.print("Durga");   // writes Durga

Why the name "PrintWriter"? Because of the `print()` method family — formatted, convenient output (similar spirit to System.out.print).

Second problem solved — automatic line separator with `println()`:

pw.println(100);     // writes 100 AND appends platform line separator
pw.println("Durga"); // writes Durga AND newline — no separate newLine() or "\n"

No need to call newLine() or embed \n manually when using println().

### 06:17 — Three levels of Writers (recommendation)

Durga Sir's rule:

- Writing character data → PrintWriter (hands should go here)
- Reading character data → BufferedReader (only two reader levels: FileReader, BufferedReader — BufferedReader is the top reader)
Readers have two levels; writers have three levels.

### 08:25 — PrintWriter constructors (3 total)

Key difference from BufferedWriter: BufferedWriter cannot communicate directly with a file — it must wrap another Writer. PrintWriter offers both direct file access and wrapping.

Board notes:

```java
// Constructor 1 — String file name
PrintWriter pw = new PrintWriter("abc.txt");

// Constructor 2 — File reference
File f = new File("abc.txt");
PrintWriter pw = new PrintWriter(f);

// Constructor 3 — via another Writer (e.g. FileWriter)
FileWriter fw = new FileWriter("abc.txt");
PrintWriter pw = new PrintWriter(fw);
```

PrintWriter can communicate directly with a file AND can communicate via some Writer object also.

Because PrintWriter can open a file directly, you do not always need an intermediate FileWriter — unlike BufferedWriter.

### 12:22 — Methods in PrintWriter

#### Inherited from Writer hierarchy (same as FileWriter / BufferedWriter)

All FileWriter/BufferedWriter write/flush/close methods are available on PrintWriter too.

#### PrintWriter-specific power methods

`print(...)` overloads — write data without trailing line separator:

`println(...)` overloads — same set as print, but after writing the value, automatically appends the platform-specific line separator:

Legend on board: For every print(X) there is a matching println(X).

### 16:22 — Demo 1: PrintWriterDemo1.java

Purpose: Show write() vs print() vs println() behavior and expected file content.

```java
import java.io.*;

class PrintWriterDemo1 {
    public static void main(String[] args) throws Exception {
        FileWriter fw = new FileWriter("abc.txt");
        PrintWriter out = new PrintWriter(fw);

        out.write(100);           // writes 'd' (Unicode 100)
        out.print(100);             // writes literal 100 — SAME LINE continues
        out.print(true);            // writes true — SAME LINE continues
        out.println('c');           // writes c + line separator
        out.println("Durga");       // writes Durga + line separator

        out.flush();
        out.close();
    }
}
```

Alternative (PrintWriter direct to file — also valid):

```java
PrintWriter out = new PrintWriter("abc.txt");
```

Trace — what lands in `abc.txt`:

Expected file content:

d100truec
Durga

Critical exam clarification — `print()` vs `println()`:

- `print()` → writes data; cursor stays on same line
- `println()` → writes data; then inserts line separator (moves to next line)
- `println()` is NOT the same as `print()` alone — the `ln` part adds the newline
Common wrong answer: "After print(100), the 100 goes to the next line." → False. Only println adds the separator.

Compile & run:

> javac PrintWriterDemo1.java
> java PrintWriterDemo1

No console output — data goes to abc.txt. Open abc.txt to verify.

### 22:53 — Exam question: `write(100)` vs `print(100)`

Question (board): What is the difference between write(100) and print(100)?

out.write(100);   // 'd'
out.print(100);   // "100"

Must-have exam clarity — this distinction has appeared repeatedly across FileWriter and PrintWriter sessions.

### 25:22 — Best reader vs best writer (summary note)

Do not confuse PrintWriter (writing) with a non-existent "PrintReader" — readers top out at BufferedReader.

### 27:17 — Character data vs Binary data (revision)

All Java data falls into two categories for I/O:

#### 1. Character / Text data

Examples: "Durga", 10.5 as text, true as text, normal .txt content.

Handle with: Readers and Writers

#### 2. Binary data

Examples: images, PDF, JAR, audio, video — any non-text file.

Handle with: Streams (InputStream / OutputStream)

Board summary:

In general, we can use Readers & Writers to handle character data (text data).

We can use Streams to handle binary data (images, video files, audio files, etc.).

More specifically:

Streams topic comes later; this video mentions it so students know why Readers/Writers exist and when not to use them.

### 32:40 — java.io class hierarchy (Object → Writer/Reader tree)

Root: Object class — parent of all Java classes.

Object
├── Writer (abstract)
│   └── OutputStreamWriter
│       └── FileWriter
│           ├── BufferedWriter
│           └── PrintWriter   ← most enhanced writer
│
└── Reader (abstract)
    └── InputStreamReader
        └── FileReader
            └── BufferedReader   ← most enhanced reader

Writer side (3 concrete levels under FileWriter path):

- FileWriter
- BufferedWriter
- PrintWriter
Reader side (2 concrete levels):

- FileReader
- BufferedReader — no PrintReader
Exam tip: Know parent/child relationships — PrintWriter extends Writer (via PrintWriter → Writer chain; internally may wrap FileWriter but IS-A Writer).

### 36:26 — File I/O exam content complete; applications begin

Core File I/O syllabus for certification is done after this hierarchy. Remaining time converts concepts into small applications showing effective read/write patterns.

## Application 1 — Merge data from two files into a third file

### 36:50 — Problem statement

Write a program to merge data from two files into a third file.

Sample input files:

file1.txt:

aaa
bbb
ccc

file2.txt:

312
313
314
315

Expected `file3.txt` (all of file1, then all of file2):

aaa
bbb
ccc
312
313
314
315

(ASR heard "3 billier / 3-Bull" — board used aaa, bbb, ccc and numeric lines.)

### 38:33 — Design: BufferedReader to read, PrintWriter to write

Pattern: BufferedReader to read, PrintWriter to write.

### 39:09 — Solution: FileMerger.java (sequential merge)

```java
import java.io.*;

class FileMerger {
    public static void main(String[] args) throws Exception {
        PrintWriter pw = new PrintWriter("file3.txt");

        // --- Merge file1.txt ---
        BufferedReader br = new BufferedReader(new FileReader("file1.txt"));
        String line = br.readLine();
        while (line != null) {
            pw.println(line);
            line = br.readLine();
        }

        // --- Merge file2.txt (reuse same BufferedReader variable) ---
        br = new BufferedReader(new FileReader("file2.txt"));
        line = br.readLine();
        while (line != null) {
            pw.println(line);
            line = br.readLine();
        }

        pw.flush();
        pw.close();
    }
}
```

Logic walkthrough:

- Open one PrintWriter on file3.txt
- Read file1.txt line-by-line with BufferedReader; each non-null line → pw.println(line)
- When readLine() returns null, file1 is exhausted
- Reuse br — open new BufferedReader on file2.txt; repeat read/write loop
- flush() and close() PrintWriter
Run:

> javac FileMerger.java
> java FileMerger

Open file3.txt — file1 content followed by file2 content.

### 50:21 — Why append happened without `append` mode?

Student doubt: Data from file2 is appended after file1 in file3, but we never passed append true anywhere.

Answer:

- Only one PrintWriter object was used for the entire operation
- First loop writes file1 data
- Second loop continues writing with the same PrintWriter → natural continuation (append behavior)
- If you opened a new PrintWriter on the same file for file2, it would overwrite file3 by default
One PrintWriter → continuation. New PrintWriter on same file → overwrite (unless append constructor).

## Application 2 — Merge line-by-line alternatively

### 51:24 — Problem statement

Write a program to perform file merge where merging is done line-by-line alternatively.

Take one line from file1, one from file2, alternate until one or both files end.

Same file1 / file2 as before. Expected `file3.txt`:

aaa
312
bbb
313
ccc
314
315

(if file2 has an extra line 316, it appears after file1 exhausted — see trace below)

With file2 having lines through `315` and an extra `316`:

aaa
312
bbb
313
ccc
314
315
316

### 53:25 — Design: two BufferedReaders + one PrintWriter

Must read both files simultaneously — open both readers at the start.

### 53:33 — First attempt (WRONG — prints literal "null")

```java
// BUGGY VERSION — DO NOT USE AS-IS
PrintWriter pw = new PrintWriter("file3.txt");
BufferedReader br1 = new BufferedReader(new FileReader("file1.txt"));
BufferedReader br2 = new BufferedReader(new FileReader("file2.txt"));

String line1 = br1.readLine();
String line2 = br2.readLine();

while (line1 != null || line2 != null) {
    pw.println(line1);          // BUG: prints "null" when line1 is null
    line1 = br1.readLine();
    pw.println(line2);          // BUG: prints "null" when line2 is null
    line2 = br2.readLine();
}
pw.flush();
pw.close();
```

What goes wrong:

When file1 finishes first, line1 becomes null but file2 still has data.

pw.println(null) writes the string `"null"` to the file — not what we want.

Observed bad output (example):

aaa
312
bbb
313
ccc
314
null
315
null
316

### 59:54 — Correct solution: null-check before each write

```java
import java.io.*;

class FileMerger2 {
    public static void main(String[] args) throws Exception {
        PrintWriter pw = new PrintWriter("file3.txt");
        BufferedReader br1 = new BufferedReader(new FileReader("file1.txt"));
        BufferedReader br2 = new BufferedReader(new FileReader("file2.txt"));

        String line1 = br1.readLine();
        String line2 = br2.readLine();

        while (line1 != null || line2 != null) {
            if (line1 != null) {
                pw.println(line1);
                line1 = br1.readLine();
            }
            if (line2 != null) {
                pw.println(line2);
                line2 = br2.readLine();
            }
        }

        pw.flush();
        pw.close();
    }
}
```

Loop condition: line1 != null || line2 != null — continue while at least one file still has data.

Write rules:

- If line1 != null → write line1, advance br1
- If line2 != null → write line2, advance br2
- If line1 == null → skip write for file1 (don't print "null")
- When both null → stop
Manual trace (aaa/bbb/ccc vs 312/313/314/315/316):

Final file3.txt:

aaa
312
bbb
313
ccc
314
315
316

Compile & run:

> javac FileMerger2.java
> java FileMerger2

### 1:07:30 — Session wrap-up

Covered in Video 123:

- Limitations of FileWriter/BufferedWriter (primitives + line separators)
- PrintWriter advantages — print / println overloads
- Three PrintWriter constructors (direct file OR via Writer)
- Inherited write/flush/close + print method family
- PrintWriterDemo1 — write(100) vs print(100) vs println
- Character vs binary data; Readers/Writers vs Streams
- Full I/O hierarchy diagram
- File merge app (sequential) — one PrintWriter, reuse BufferedReader
- Alternate merge app — two BufferedReaders, null-check before println
Next video (124): More PrintWriter examples (file extraction, duplicate removal, business scenarios).

## Quick reference tables

### PrintWriter vs FileWriter / BufferedWriter

### PrintWriter constructors

### Key methods summary

### Exam traps checklist

### Video metadata

Java code block count: 12

## Tables (placement lost -- re-place these in context)

| Method | Argument type |
|---|---|
| write(int ch) | single character (Unicode int) |
| write(char[] c) | char array |
| write(String s) | String |

| Level | Class | Role |
|---|---|---|
| 1 | FileWriter | Basic character writing to file |
| 2 | BufferedWriter | Buffering + newLine() for portable line breaks |
| 3 | PrintWriter | Most enhanced — print/println for all primitive types + auto newline |

| # | Constructor | Meaning |
|---|---|---|
| 1 | PrintWriter(String fileName) | Direct communication with file by name |
| 2 | PrintWriter(File f) | Direct communication via File reference (like FileWriter) |
| 3 | PrintWriter(Writer w) | Communication via some Writer object (like BufferedWriter pattern) |

| Method | Purpose |
|---|---|
| write(int ch) | Single character (Unicode int) — still writes char, not int value |
| write(char[] c) | Char array |
| write(String s) | String |
| flush() | Push buffered data to destination |
| close() | Close writer, release resources |

| Overload | Example |
|---|---|
| print(char ch) | pw.print('a'); |
| print(int i) | pw.print(100); |
| print(double d) | pw.print(10.5); |
| print(boolean b) | pw.print(true); |
| print(String s) | pw.print("Durga"); |
| … | (and more: long, float, char[], Object, etc.) |

| Overload | Example |
|---|---|
| println(char ch) | pw.println('c'); |
| println(int i) | pw.println(100); |
| println(double d) | pw.println(10.5); |
| println(boolean b) | pw.println(true); |
| println(String s) | pw.println("Durga"); |
| println() | blank line (separator only) |

| Statement | Effect on file |
|---|---|
| out.write(100) | Writes character `d` (not number 100) |
| out.print(100) | Appends `100` on same line as d → so far: d100 |
| out.print(true) | Appends `true` on same line → d100true |
| out.println('c') | Appends `c` then newline → line 1: d100truec |
| out.println("Durga") | New line: `Durga` then newline |

| Call | What gets written to file |
|---|---|
| write(100) | Corresponding character 'd' (Unicode value 100) |
| print(100) | Integer value `100` as text (not a single char) |

| Operation | Most enhanced class |
|---|---|
| Write character/text data to file | PrintWriter |
| Read character/text data from file | BufferedReader |

| Task | API |
|---|---|
| Write binary data to file | OutputStream |
| Read binary data from file | InputStream |

| Role | Class |
|---|---|
| Write merged output to file3.txt | PrintWriter |
| Read lines from file1.txt, file2.txt | BufferedReader |

| Component | Count | Target |
|---|---|---|
| PrintWriter | 1 | file3.txt |
| BufferedReader br1 | 1 | file1.txt |
| BufferedReader br2 | 1 | file2.txt |

| Iteration | line1 | line2 | Written |
|---|---|---|---|
| Start | aaa | 312 | aaa, 312 |
|  | bbb | 313 | bbb, 313 |
|  | ccc | 314 | ccc, 314 |
|  | null | 315 | 315 only |
|  | null | 316 | 316 only |
| End | null | null | stop |

| Feature | FileWriter / BufferedWriter | PrintWriter |
|---|---|---|
| Write int 100 as number | No — write(100) → 'd' | Yes — print(100) → 100 |
| Write double/boolean directly | No (CE or String only) | Yes — print(10.5), print(true) |
| Line separator | Manual \n or newLine() | println() auto-adds separator |
| Talk to file directly | FileWriter yes; BufferedWriter no | Yes (constructors 1 & 2) |
| Via another Writer | BufferedWriter only | Constructor 3 |

| # | Signature | Direct to file? |
|---|---|---|
| 1 | PrintWriter(String fileName) | Yes |
| 2 | PrintWriter(File f) | Yes |
| 3 | PrintWriter(Writer w) | Via wrapped Writer |

| Category | Methods |
|---|---|
| From Writer | write(int), write(char[]), write(String), flush(), close() |
| PrintWriter-specific | print(...) overloads, println(...) overloads |

| Trap | Correct understanding |
|---|---|
| write(100) on any Writer | Writes char 'd', not integer 100 |
| print(100) on PrintWriter | Writes text 100 |
| print vs println | Only println adds line separator |
| println(null) | Writes literal "null" string |
| Alternate merge without null check | "null" appears in output file |
| Two PrintWriters same file | Second opens in overwrite mode |
| BufferedWriter constructor | Cannot take filename alone — needs Writer |
| PrintWriter constructor | Can take filename directly |

| Field | Value |
|---|---|
| Playlist | Java tutorial by Durga Sir |
| Position | 123 of 203 |
| Series | Core Java With OCJP/SCJP |
| Topic | File I/O — Part 4 (PrintWriter) |
| Instructor | Durga Sir |
| Duration | 1h 08m 13s |
| Video ID | JN7-L3ZEnTw |
| Watch | https://www.youtube.com/watch?v=JN7-L3ZEnTw |
