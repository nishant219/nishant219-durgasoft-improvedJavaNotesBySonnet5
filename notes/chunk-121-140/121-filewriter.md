# Video 121

## Video info

Title: Core Java With OCJP/SCJP: File I/O Part-2 || FileWriter || important methods

ASR decode key: file letter → File; file WR / wrer → FileWriter; upend → append; happing → appending; backs sln / back sln → \n; Bufford → Buffered; CE → checked exception (IOException); wi → void.

### 00:07 — Bridge from File/Directory API to read/write

After Part-1 (creating files, directories, navigation methods), the next mandatory step is writing and reading data. A file with no I/O is useless.

Agenda for writers (3 total in this File I/O block):

- FileWriter ← this video
- BufferedWriter
- PrintWriter
### 00:43 — FileWriter: purpose

Class name: FileWriter — one word, no space (not “file writer” as two words on the exam).

Purpose: Write character / text data to a file.

```java
// Conceptual usage (not a full program)
FileWriter fw = new FileWriter("abc.txt");
// use fw to write character/text data to the file
```

Any textual content (letters, digits as text, \n, etc.) goes through FileWriter.

### 02:07 — Constructors: four total (override vs append)

Rule: Create a FileWriter object — that is the entry point for writing.

#### Override constructors (default — **overwrite** existing file content)

Constructor 1 — file name as `String`:

```java
FileWriter fw = new FileWriter("abc.txt");
// or
FileWriter fw = new FileWriter("demo.txt");
```

Constructor 2 — existing `File` reference:

```java
File f = new File("abc.txt");
FileWriter fw = new FileWriter(f);
```

Override behavior: If abc.txt already contains data and you open FileWriter with constructors 1 or 2, new writes replace (override) old content — old data is gone by default. Override is not recommended in most real scenarios unless you explicitly want to replace the whole file.

#### Append constructors (preserve + add at end)

Constructor 3 — `String` file name + `boolean append`:

FileWriter fw = new FileWriter("abc.txt", true);   // append
FileWriter fw = new FileWriter("abc.txt", false);  // override (same as ctor 1)

Constructor 4 — `File` + `boolean append`:

File f = new File("abc.txt");
FileWriter fw = new FileWriter(f, true);   // append
FileWriter fw = new FileWriter(f, false);  // override

Summary: 4 constructors total — first two = override; next two = append when true.

### 10:18 — Common point for ALL four constructors: auto-create file

Exam / interview loophole: If the named file does not exist, do you get FileNotFoundException?

Answer: NO — all four FileWriter constructors create the file if missing, then write.

Analogy (Durga Sir):

- Student 1: Notice board exists but white paper is missing → comes back saying “I can’t write.” (FileNotFoundException mindset — wrong for FileWriter.)
- Student 2: Pastes white paper on board, writes the message → job done. (FileWriter behavior.)
Note for notes:

If the specified file is not already available, all four constructors will create that file. You do not need to check file.exists() before constructing FileWriter.

### 15:54 — Methods in FileWriter (5 methods)

Writers are like a pipe from program → file (abc.txt).

#### Three `write` overloads

1. `write(int ch)` — single character

fw.write('a');
fw.write(97);   // also writes 'a' (Unicode code point)

- Parameter is int (Unicode value), not char in signature — but you pass 'a' or 97.
- 97 → 'a', 98 → 'b', 99 → 'c', `100` → `'d'`.
2. `write(char[] c)` — array of characters

char[] arr = {'H', 'i'};
fw.write(arr);

3. `write(String s)` — string

fw.write("Durga");
fw.write("\n");           // manual newline — see problems later
fw.write("Software Solutions");

Same 3 write methods exist in FileWriter, BufferedWriter, and PrintWriter — memorize once, applies to all writers.

#### 4. `flush()`

Pipe analogy: Like transferring rice from a heavy bag to a drum in small scoops — some rice may remain stuck in the pipe until you force it through.

fw.flush();

Purpose: Guarantee all buffered data, including the last character, is pushed to the file.

Scope: flush() applies to writers only, not readers.

#### 5. `close()`

fw.close();

Highly recommended after read/write work — releases resources.

Total FileWriter methods covered: 3 × write + flush + close = 5.

### 26:47 — Demo: FileWriterDemo2.java

Board program:

```java
import java.io.*;

class FileWriterDemo2 {
    public static void main(String[] args) throws Exception {  // CE: IOException (checked)
        FileWriter fw = new FileWriter("abc.txt");
        // No need to check if abc.txt exists — constructor creates if missing

        fw.write(100);                        // writes 'd'  (Unicode 100)
        fw.write("Urga");                     // ASR: "Ur G" → Durga (Sir writes "Durga" on board)
        fw.write("\n");                       // newline
        fw.write("Software Solutions");
        fw.write("\n");
        fw.write("ABC");

        fw.flush();   // recommended
        fw.close();   // recommended
    }
}
```

Compile & run (board):

> javac FileWriterDemo2.java    // compiles fine
> java FileWriterDemo2          // no console output — data goes to file

Expected `abc.txt` content after first run:

dUrga
Software Solutions
ABC

*(ASR heard "Ur G" / "DGA" — on screen the demo shows D from write(100) plus Urga or full Durga line; executed file showed DGA Software Solutions followed by ABC.)*

Console output: none (unless you print separately).

### 30:29 — IO exception handling note

Whenever performing I/O read/write, `IOException` is possible → it is a checked exception → must handle (try-catch) or declare (throws).

Writers/readers = text files. For binary data (images, video, audio) → use Streams (separate topic).

### 33:52 — Override demo: run program multiple times

Using constructor 1 (no append flag):

FileWriter fw = new FileWriter("abc.txt");  // override mode

- Run once → one copy of content in file.
- Run 1000 times → still one copy — each run overwrites previous content.
### 34:55 — Append demo: `true` flag

FileWriter fw = new FileWriter("abc.txt", true);  // append mode

- File already had 1 block → run once → 2 blocks.
- Run 10 times → content repeated 10 times (Sir ran many times → 57 lines in abc.txt on screen).
Board note:

In the above program, FileWriter performs overriding of existing data (constructors 1–2).

For append, use: new FileWriter("abc.txt", true).

### 38:35 — Why BufferedWriter & PrintWriter exist (FileWriter limitations)

Student question: Simple FileWriter exists — why next-level writers?

#### Problem 1: Manual line separator

Programmers care about data, not \n syntax. Manually inserting \n is a burden.

#### Problem 2: `\n` is NOT portable (real classroom bug)

A student reported: program compiles and runs, but opening abc.txt shows literal text:

d\nSoftware Solutions\nABC

…instead of line breaks.

Durga Sir’s debugging session:

- Verified backslash \ not forward /
- Verified not double backslash
- Ran on student laptop — same issue
- Changed file name — same
- Changed content — same
- Google: “backslash n problem with file writer”
- Root cause: On some OS / systems, \n in a String passed to `write()` is not treated as newline — it is normal text. The actual line separator symbol varies system to system.
Main problem with FileWriter (board note):

We must insert line separator manually — e.g. "\n" — which varies from system to system → difficulty for the programmer.

Solution (next videos): BufferedWriter and PrintWriter — they handle platform line separators (especially via newLine() in BufferedWriter).

### 45:52 — Session wrap-up

Covered today:

- What FileWriter is
- 4 constructors (override vs append; auto-create file)
- 5 methods (3 writes + flush + close)
- Live demo with override vs append
- Limitation: manual \n → use BufferedWriter / PrintWriter next
## Quick reference tables

### FileWriter constructors

### FileWriter methods

Java code block count: 13

## Tables (placement lost -- re-place these in context)

| Field | Value |
|---|---|
| Playlist | Java tutorial by Durga Sir |
| Position | 121 of 203 |
| Series | Core Java With OCJP/SCJP |
| Topic | File I/O — FileWriter (character/text writing) |
| Instructor | Durga Sir |
| Duration | 46m 10s (from transcript) |
| Video ID | QT8DCW5ZFxI |
| Watch | https://www.youtube.com/watch?v=QT8DCW5ZFxI |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

| Constructors | append arg | Behavior |
|---|---|---|
| 1, 2 | (none) | Override only |
| 3, 4 | true | Append |
| 3, 4 | false | Override (redundant with 1/2) |

| # | Signature | Mode |
|---|---|---|
| 1 | FileWriter(String fileName) | Override |
| 2 | FileWriter(File file) | Override |
| 3 | FileWriter(String fileName, boolean append) | append flag |
| 4 | FileWriter(File file, boolean append) | append flag |

| Method | Purpose |
|---|---|
| write(int ch) | Single character (Unicode int) |
| write(char[] c) | Char array |
| write(String s) | String |
| flush() | Force all buffered chars to file |
| close() | Close writer |
