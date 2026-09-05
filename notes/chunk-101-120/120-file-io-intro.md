# Video 120 — File I/O Part 1: Introduction & `File` class

## Video info

Import for all demos in this video:

```java
import java.io.*;
// or
import java.io.File;
```

## 00:04 — Why File I/O matters (historical SCJP / OCJP context)

File I/O is one of the foundational Java topics for persistent storage — moving data out of RAM and onto disk (or reading it back).

### Exam weight across Java versions

### Why it was removed in Java 1.4

- Java 1.0 released in 1995 — database concepts were not yet mainstream.
- The most common storage area for data was the file system.
- By 2003–2004 (Java 1.4 era), database storage (JDBC, enterprise apps) became the default.
- Certification dropped File I/O because enterprise Java developers were expected to use databases, not raw files.
### Why it came back in Java 1.5 / 1.6

- Not every program needs a full database server.
- Example: storing one `count` variable — installing a separate DB server and table for that is overkill (wasteful).
- Rule of thumb (Durga Sir):
- Small amount of data → prefer file
- Huge amount of data → prefer database
- Being a certified Java programmer still requires basic file literacy — hence File I/O returned with reduced weight (2–3 questions).
Exam takeaway: File I/O is not the heaviest topic anymore, but the File class traps (especially new File() vs createNewFile()) appear regularly.

## 04:31 — File I/O series agenda (six classes)

This multi-part lecture series covers these `java.io` classes:

This video (120) covers only `File` — constructors and important methods. Reading/writing data comes in later videos.

## 05:54 — ★ Critical twist: `new File()` does NOT create a physical file

### The most common beginner mistake

```java
File f = new File("ABC.txt");
```

Wrong assumption: "This line creates a new physical file named ABC.txt on disk, and `f` is the reference variable for that file."

Correct understanding: This line creates a Java `File` object in memory that represents the name ABC.txt. No physical file is created on disk.

### Internal behavior of `new File(String name)`

- JVM checks: does a physical file/directory with this name already exist?
- If yes → f simply refers to (points to) that existing entity.
- If no → still only creates a Java object representing the name — does not create anything on disk.
### Board diagram (conceptual)

Line 1:  File f = new File("ABC.txt");
         → Creates Java File OBJECT in heap (represents name "ABC.txt")
         → Disk: (nothing created)

Line 3:  f.createNewFile();
         → NOW physical file ABC.txt appears on disk

### Proof program — board demo #1

```java
import java.io.*;

class Test {
    public static void main(String[] args) throws Exception {
        File f = new File("ABC.txt");
        System.out.println(f.exists());   // false — no physical file yet

        f.createNewFile();                  // NOW physical file is created
        System.out.println(f.exists());     // true
    }
}
```

First run output:

false
true

Second run output (file already exists from first run):

true
true

### Live execution demo — board demo #2

Durga Sir uses a unique filename so it definitely does not exist on the system:

```java
import java.io.*;

class Test {
    public static void main(String[] args) throws Exception {
        File f = new File("ABC01092014.txt");
        System.out.println(f.exists());   // false
        // f.createNewFile();             // uncomment to create
    }
}
```

Compile & run:

> javac Test.java
> java Test
false

OS verification (Windows `dir`):

> dir ABC01092014.txt
File Not Found

Physical file is not there — confirming new File() alone does nothing on disk.

After adding `createNewFile()`:

```java
import java.io.*;

class Test {
    public static void main(String[] args) throws Exception {
        File f = new File("ABC01092014.txt");
        System.out.println(f.exists());   // false
        f.createNewFile();
        System.out.println(f.exists());   // true
    }
}
```

Output: false then true. Running dir now shows the file with a fresh timestamp (created "just now").

100% exam trap: new File("x.txt") → never creates a physical file. Only createNewFile() (or writing via streams in later lectures) creates the actual file.

## 17:06 — Unix philosophy: `File` object represents files AND directories

### Key concept

In Unix, everything is a file — even directories are treated as files.

Java's File I/O model is implemented based on the Unix operating system. Therefore a File object can represent:

- A regular file
- A directory
### Directory demo — board demo #3

```java
import java.io.*;

class Test {
    public static void main(String[] args) throws Exception {
        File f = new File("Durga123");       // represents directory name
        System.out.println(f.exists());      // false if not present

        f.mkdir();                           // create physical directory
        System.out.println(f.exists());      // true
    }
}
```

Note: mkdir() creates only the final directory in the path (parent must already exist). For nested paths, mkdirs() exists (covered in later lectures).

### Board notes (copy verbatim)

In Unix, everything is treated as a file.

Java File I/O concept is implemented based on Unix operating system.

Hence, Java File object can be used to represent both files and directories.

### Full directory flow demo — board demo #4

```java
import java.io.*;

class Test {
    public static void main(String[] args) throws Exception {
        File f = new File("Durga123");
        System.out.println(f.exists());   // false
        f.mkdir();
        System.out.println(f.exists());   // true
    }
}
```

## 23:03 — `File` class constructors (three)

All three constructors create a Java `File` object to represent a file or directory name — they do not by themselves create physical files/directories (unless followed by createNewFile() / mkdir()).

```java
// Constructor 1 — name in CURRENT WORKING DIRECTORY
File(String pathname)

// Constructor 2 — name in SPECIFIED subdirectory / path
File(String parent, String child)

// Constructor 3 — child relative to existing File reference
File(File parent, String child)
```

### Constructor selection guide

## 30:04 — Example 1: Create file in current working directory

Requirement: Create file ABC.txt in the current working directory.

### Board demo #5

```java
import java.io.*;

class Test {
    public static void main(String[] args) throws Exception {
        File f = new File("ABC.txt");   // Constructor 1
        f.createNewFile();              // physical file created HERE
    }
}
```

- new File("ABC.txt") → Java object only (no disk file).
- createNewFile() → physical ABC.txt appears in CWD.
## 33:02 — Example 2: Directory + file inside (all 3 constructors)

Requirement: In current working directory:

- Create directory `Durga123`
- Inside it, create file `demodata.txt`
### Step 1 — create directory (Constructor 1) — board demo #6

```java
File f = new File("Durga123");
f.mkdir();
```

### Step 2a — create file inside (Constructor 2) — board demo #7

```java
File f1 = new File("Durga123", "demodata.txt");
f1.createNewFile();
```

### Step 2b — alternative using Constructor 3 — board demo #8

```java
File f  = new File("Durga123");
f.mkdir();

File f1 = new File(f, "demodata.txt");   // parent already pointed by f
f1.createNewFile();
```

### Resulting directory structure

(current working directory)/
    Durga123/
        demodata.txt

### Complete combined program — board demo #9

```java
import java.io.*;

class Test {
    public static void main(String[] args) throws Exception {
        // Step 1: create directory
        File f = new File("Durga123");
        f.mkdir();

        // Step 2: create file inside (Constructor 2)
        File f1 = new File("Durga123", "demodata.txt");
        f1.createNewFile();

        // Alternative (Constructor 3):
        // File f1 = new File(f, "demodata.txt");
        // f1.createNewFile();
    }
}
```

After this example you should know how to use all three constructors.

## 37:45 — Example 3: Create file in another drive/folder

Requirement: Create ABC.txt inside `E:\xyz\` (Windows path).

### Board demo #10

```java
import java.io.*;

class Test {
    public static void main(String[] args) throws Exception {
        File f = new File("E:\\xyz", "ABC.txt");   // Constructor 2
        f.createNewFile();
    }
}
```

### Prerequisites for success

- Drive `E:` must exist on the system.
- Folder `E:\xyz` must already exist (mkdir() only creates the final directory; parent chain must be present).
### Real student error (Durga Sir anecdote)

A student reported FileNotFoundException with this code. Root cause: his machine had only C: and D: drives — no E: drive. Without the drive and folder, creation fails.

Rule: Assume E:\xyz folder is already available before running the example.

## 42:16 — Important methods in `File` class

Methods already used in earlier examples: exists(), createNewFile(), mkdir().

Full method reference for this session:

## 47:36 — `exists()` detailed behavior

boolean exists()

- Returns `true` if the specified file or directory is available on the filesystem.
- Returns `false` otherwise.
- Works for both files and directories.
## 48:30 — `createNewFile()` detailed behavior (intelligent method)

boolean createNewFile()

Algorithm:

- Check: is the specified file already available?
- If already there → return `false` without creating anything.
- If not there → create new physical file → return `true`.
### Demo

File f = new File("demo.txt");
System.out.println(f.createNewFile());   // true — created
System.out.println(f.createNewFile());   // false — already exists, nothing created

Same logic applies to `mkdir()` for directories (returns false if directory already exists).

### Method return-value traps (exam)

## 52:03 — `isFile()` and `isDirectory()`

A File reference may point to either a file or a directory. To distinguish:

f.isFile()        // true if physical file
f.isDirectory()   // true if physical directory

Because File can represent both (Unix model), you cannot tell from the reference alone — you must call these methods after the entity exists on disk.

## 53:12 — `list()` method

String[] list()

- Applicable when File object represents a directory.
- Returns `String[]` — names of all files and subdirectories inside that directory.
- Returns `null` if File is not a directory or an I/O error occurs.
- Return type is `String[]`, not List<String> (legacy API).
## 54:16 — `length()` method

long length()

- Returns number of bytes in the specified file.
- Return type is `long`, not `int`, because large files can exceed Integer.MAX_VALUE.
long len = f.length();

## 55:08 — `delete()` method

boolean delete()

- Deletes the specified file or directory.
- Returns true if deletion succeeded.
Caution: delete() on a non-empty directory may fail (platform-dependent). It does not recurse — typically works on empty directories only.

## 55:44 — Demo: List all files and directories in a folder

Requirement: Display names of all files and directories in C:\DurgaClasses.

### Board demo #11 — list everything

```java
import java.io.*;

class Test {
    public static void main(String[] args) {
        File f = new File("C:\\DurgaClasses");
        String[] names = f.list();

        int count = 0;
        for (String s : names) {
            count++;
            System.out.println(s);
        }
        System.out.println("Total number: " + count);
    }
}
```

Sample output: 19 names listed → Total number: 19 (mix of files and directories).

Durga Sir's live run showed 819 total entries in his C:\DurgaClasses folder (large teaching directory). The pattern is what matters for the exam.

## 1:02:33 — Filter: display ONLY file names (not directories)

### Wrong approach — compile error — board demo #12

for (String s1 : s) {
    if (s1.isFile()) {   // CE — isFile() is NOT on String
        count++;
        System.out.println(s1);
    }
}
// CE: cannot find symbol — method isFile() on String

Why it fails: isFile() and isDirectory() are `File` class methods, not `String` methods. The list() array contains names only (String), not File objects.

Key insight: File class methods must be applied on `File` objects, not on String names.

### Correct approach — board demo #13

For each name, create a File object relative to the parent directory (Constructor 3), then call isFile():

```java
import java.io.*;

class Test {
    public static void main(String[] args) {
        int count = 0;
        File f = new File("C:\\DurgaClasses");
        String[] s = f.list();

        for (String s1 : s) {
            File f1 = new File(f, s1);    // Constructor 3 — parent + child name
            if (f1.isFile()) {
                count++;
                System.out.println(s1);
            }
        }
        System.out.println("Total number of files: " + count);
    }
}
```

Result in Durga Sir's demo: 8 files out of 19 total entries — remaining 11 are directories.

## 1:07:49 — Filter: display ONLY directory names

Same program; replace isFile() with isDirectory() — board demo #14:

```java
import java.io.*;

class Test {
    public static void main(String[] args) {
        int count = 0;
        File f = new File("C:\\DurgaClasses");
        String[] s = f.list();

        for (String s1 : s) {
            File f1 = new File(f, s1);
            if (f1.isDirectory()) {
                count++;
                System.out.println(s1);
            }
        }
        System.out.println("Total number of directories: " + count);
    }
}
```

Result: 11 directories (19 total − 8 files = 11 directories). Counts must add up.

## 1:08:43 — Summary code pattern (board copy)

### List only files — board demo #15

```java
int count = 0;
File f = new File("C:\\DurgaClasses");
String[] s = f.list();

for (String s1 : s) {
    File f1 = new File(f, s1);
    if (f1.isFile()) {
        count++;
        System.out.println(s1);
    }
}
System.out.println("Total number of files: " + count);
```

### List only directories

Replace f1.isFile() → f1.isDirectory(). No other changes needed.

## 1:12:08 — Session wrap-up

### Key points from Part 1

- new File(name) → Java object only; no physical file/directory on disk.
- createNewFile() → creates physical file; returns false if already exists.
- mkdir() → creates physical directory; returns false if already exists.
- File represents files and directories (Unix model).
- Three constructors: current dir, parent+child strings, File parent + child.
- Important methods: exists, createNewFile, mkdir, isFile, isDirectory, list, length, delete.
- list() returns String[] of names — must use new File(parent, name) before calling isFile() / isDirectory().
- length() returns `long`, not int.
Next (Part 2, Video 121): FileWriter — writing character data to files.

## Quick reference card

File I/O Part 1 — java.io.File
├── new File(name)           → Java object ONLY (no disk file)
├── createNewFile()          → physical file (false if exists)
├── mkdir()                  → physical directory (false if exists)
├── exists()                 → boolean — on disk?
├── isFile() / isDirectory() → type check (on File object, NOT String)
├── list()                   → String[] names in directory
├── length()                 → long bytes in file
└── delete()                 → remove file or empty directory

Constructors
├── File(String pathname)              → CWD
├── File(String parent, String child)  → other path
└── File(File parent, String child)    → relative to File ref

Storage choice
├── Small data  → file
└── Huge data   → database

Series (6 classes): File → FileWriter → FileReader → BufferedWriter → BufferedReader → PrintWriter

## Interview / exam trap questions

- Does `new File("a.txt")` create a file? → No. Only a Java object representing the name.
- Which line creates the physical file? → createNewFile() (or stream write in later lectures).
- `createNewFile()` returns false — why? → File already existed; nothing created.
- `list()` return type? → String[] (not List).
- Can you call `s1.isFile()` where `s1` is from `list()`? → No — compile error. Wrap: new File(parent, s1).isFile().
- `length()` return type? → long (large files exceed int).
- Can `File` represent a directory? → Yes (Unix model).
- Constructor for `E:\xyz\abc.txt`? → new File("E:\\xyz", "abc.txt").
- First run vs second run `exists()` after `createNewFile()`? → false→true first run; true→true second run.
- Why was File I/O removed then re-added to SCJP? → DB dominance in 1.4; small-data use cases brought it back in 1.5.
## ASR decode notes (Whisper STT corrections)

Java code block count in notes: 16

## Full transcript

Source: Local Whisper STT · Video ID rxo1SZmq9VE · Duration 1h 12m 26s

[00:04] File Ivo, File Ivo, File Ivo, File Ivo.

[00:14] Okay, File Ivo.

[00:15] So related to File Ivo, there are few things I have to talk.

[00:20] File Ivo, related to this File Ivo, there are few conclusions I have to talk just up,

[00:26] In the SCJP point of view even normal general Java side also in the world and days whenever

[00:36] Java 1.0 1.1 version 1.2 1.3 versions file concept is very important concept in Java look

[00:48] that is say for these versions, for these versions, SEJP is there, SEJP is there, SEJP 1.1,

[00:58] SEJP 1.2 version, SEJP is there for these versions also.

[01:02] At that time, file concept is a very important concept, minimum 7 to 8 questions were there

[01:09] in this.

[01:10] But whenever the situation comes to 1.4 and 1.5 versions, 1.4 version especially.

[01:18] Some people remove the file concept from SEJP cell bus.

[01:23] File concept is not there.

[01:25] But Shadan is 1.5 or 1.6 version.

[01:28] Shadan's file concept came into the picture.

[01:31] Okay.

[01:32] What is the reason for that?

[01:34] In the Java 1.0 version release,

[01:37] at what time this was after?

[01:39] 1995.

[01:40] 1995.

[01:41] This was in 1995.

[01:43] In 1995, database concepts are not that much popular.

[01:48] Correct or not database concepts not that much popular.

[01:51] The very common storage area is an nothing but file only for data.

[01:57] I want to store my data. Very common storage area is an nothing but file concept only.

[02:03] That's why you know Erda time file is very important.

[02:06] That's why 728 questions you can expect.

[02:09] So, in this CGP exams from the file, but 1.4 version, almost around 2003, 2004 like

[02:19] look at this, at that time, so database concepts are more popular, more popular.

[02:24] Being some sort of a Java program, not required to have idea on the files because the reason

[02:30] is everyone is going for what database, that's why file I go, not there in the CGP 1.4

[02:37] in the 1.5 version, 1 second some people kept the file level concept, why? Because database

[02:44] is a very common storage area, but I want to store only one count variable. Sir, only

[02:53] one count variable I want to store. If I want to store one count variable, going for

[03:00] separate database, install separate database server, store this count value in the database

[03:05] server in the table is it recommend? No right? So for small amount of data, going for

[03:11] databases is nothing but a vast. If the huge data is there, going for databases is okay

[03:16] well, but small amount of data, going for databases is the vast. That's why what are some people

[03:21] did is nothing but, you know, being some certified Java programmer, compulsory basic idea

[03:27] in the file concept must be required.

[03:30] regarding like they felt that shadow with the introduced file concept in the 1.5

[03:35] or jump but the importance got reduced just 2 to 3 questions only there in the 1.5 or

[03:42] 1.6 version of Java related to the files.

[03:45] I'll get in the point right ok this is what you people should weigh what is what is

[03:51] what is the why file a concept came so importance is not there but we have to

[03:57] in detail not required to worry.

[03:59] So file either 2 to 3 questions we can able to get.

[04:03] Database file. Small amount of data.

[04:06] Better to go for file concept.

[04:08] Huge amount of data. Better to go for water.

[04:11] Database concept. That's why small amount of data

[04:14] sometimes we may require. Sometimes we may require to store.

[04:17] That's why. So being some certified Java programmer,

[04:20] our varical certified Java programmer,

[04:22] compulsory basic idea in the file,

[04:24] that's why some people introduced once again file logo concept in the higher versions

[04:29] right clear for all of you.

[04:31] Next up, yaza part of file, file live, which things we are going to discuss.

[04:36] The first, first let me talk about file concept, first first file is a Java class file concept

[04:44] then file writer, file writer, next file writer, file writer, file writer, file writer,

[04:57] file writer, fourth one, bufford, bufford writer, bufford writer, bufford, bufford writer,

[05:10] Next, bufford reader, next one print writer, print writer like we have, print writer like

[05:27] that is all this is the agenda related to the file.

[05:30] I am getting file I have related to this for the agenda.

[05:33] These are six classes we require to discuss.

[05:36] now keeps operating file, let me start the system with a small twist, okay, file anywhere

[05:54] right, let me start with a small twist, the people who attend the dollar, they be silent

[05:59] just observe.

[06:00] So, I am taking file F is equal to, file F is equal to new file A, B, C, A dot, T,

[06:16] X, T. Final F is equal to F, F is B, C dot, T, X, T. Can you tell because of this line,

[06:24] what we are doing? Because of this line what we are doing? File F is called new file of

[06:30] ABC.exe what we are doing? We are creating a new file named with ABC.exe and F is reference

[06:41] variable for that. So, here just observe this is ABC.exe a new file we are creating

[06:50] or feel the reference variable for that.

[06:52] Correct or not?

[06:53] Oh, correct or not?

[06:55] Any explanation is required up to this.

[06:57] No, make sure this one is 100% per car wrong.

[07:02] Ok, remember it is another thing which is going to be happened.

[07:06] Sir, this line, this line won't create any physical file.

[07:12] Simple remember, Saram creating Java file object.

[07:16] object. Sir, I am creating a Java file object, not a physical file. We are just creating

[07:23] a Java file object to represent the name ABC.exe. This line won't create any physical

[07:31] file. Are you getting that? Look at this. First it will check. Sir, either physical file

[07:36] ABC.exe already there or not. If it is already there, you have to simply point into that.

[07:42] If it is not already there, it won't create physical file.

[07:46] Just we are creating Java file object to represent ABC.xt in name.

[07:52] Is it clear for all of you?

[07:53] Just we are creating Java file object to represent ABC.xt in name that's all,

[07:59] physical file won't be created.

[08:01] Clear for all of you.

[08:02] Okay. Now, survey the proof.

[08:04] Can you please show like?

[08:05] Sir, I'm taking system.out.println.

[08:09] F dot exists, I can't take it. F dot exists, sir. Is that physical file already there?

[08:24] Arna. Sir, this is positive I'm keeping. That's why word answer by default we are going

[08:29] to get. False is the answer. There is no such type of file. False is the answer. Is it clear?

[08:35] So if this is there, then automatically true I have to get it.

[08:40] Are you getting it?

[08:41] Because this line won't create any physical file.

[08:44] That's why SOPFF.exe is nothing but false.

[08:47] Next up, sir, I want that physical file.

[08:51] Sir, I want that physical file.

[08:53] Then what we have to do?

[08:54] Now, for data create a new file.

[08:59] For data create a new file.

[09:03] Now my question is, physical file will be created.

[09:08] That line number one or line number three.

[09:11] That line number one or three.

[09:13] Physical file will be created at line number three.

[09:17] Not at line number one.

[09:19] Now the physical file got created.

[09:21] Ya Fitha reference variable for that. Now ask the same question. Yes, hope ya F, F

[09:28] for that exists. Ya F for that exists. And I cannot tell, what the answer by the if or

[09:35] if we are going to get? Ya, what the answer? True itself is the answer. I am getting

[09:40] true because, there is physical failure created already. That is why true is the answer

[09:44] So, if I run this program, if I run run this program, first time, sir, if I run this program,

[09:53] first time, first run, first time, first run, first time, first run, first time, false

[10:00] rule, true is the answer, false follow-up, two is answer. If I run the program second time,

[10:07] second run, word answer, word answer, because physical file already created, already there,

[10:16] a swap law of that exists, word answer true, and the second I am word answer true right,

[10:22] are you able to get, so clear indication, this line won't create any physical file, just

[10:28] we are creating Java file objects, are very proof, let me execute this code, here see,

[10:37] just 1 minute 1 minute here see this one just have a look once Saram Taikang class test

[10:51] okay here see this one class test file of is equal to new file of all these things are

[10:58] not there can I can I spell out any any name any name which should not be which is not

[11:03] there in my system. A, B, C, today is a word that is 01092014.T, stick. Okay, like,

[11:15] sir, I am sure today date is not there. A, B, C is not like I am, F, dot, X, J. Can you

[11:21] tell, is that physical file? Is it there or not there? Not there. This line won't create any

[11:29] any physical file. I am sure one create any physical file. Let me compile under let me run this code.

[11:35] Let me compile under let me run Java C Java C test dot Java. The code compiles find next

[11:45] and after that Java test. For the answer false Java test or the answer false is the answer because

[11:51] there is no such type of file. Let me run one second one second one second false only even physically if

[11:56] If you want to check, DIR, ABC, 01092014.TXT is it there or not there?

[12:07] Not there, you know, file not found.

[12:10] Is it nothing but like?

[12:11] File not found.

[12:12] Is a physical is also not there.

[12:14] So, now, can I use the term, this line will create a physical file or not?

[12:20] No, this line won't create any physical files.

[12:23] Sir, I want that physical file.

[12:25] Can you finish by the code?

[12:27] Create

[12:29] Create a new file

[12:31] Now the physical file got created

[12:33] If you want you can

[12:35] CRAG Check

[12:37] What is the answer we are going to get?

[12:39] If you can you can CRAG Check

[12:41] Here see

[12:43] This one

[12:45] Compile is fine

[12:47] Answer false true

[12:49] If I run second time

[12:51] If I run second I more than 2 true okay this is

[12:55] Sir when this file got created if you want to know

[12:59] DIR like can you please catch it when this file got created

[13:03] 0109 2014 year 2033 is another

[13:08] but 833 is another much now just now file got created right

[13:12] I hope you people can have a clear so cinema starts with the twist only

[13:17] okay this is first it keeps a wedding file

[13:20] under then only this line, do not take any other, only first line. File F is equal to,

[13:27] file F is equal to, new file of ABC dot A, stick. File F is equal to, new file of ABC dot

[13:37] at A, stick. ABC dot at T, stick. File F is equal to new file of ABC dot at T, stick.

[14:15] There is no physical file. First it will check is there any physical file? Name it with

[14:22] them. Is there any physical file? Name it with them. A, B, C, dot, T, X, T. Is there any

[14:29] physical file? Name it with A, B, C, dot, T, X, T. Is available or not? Is available

[14:37] not, is available or not or not. If it is available, if it is available, if it is available,

[14:52] if it is available, then then F, then F simply refers to that file, F simply refers to

[14:59] If simply refers to that file, then you have to file that file.

[15:14] If it is not available, then we are just creating.

[15:27] creating, then we are just creating, then we are just creating, and we are just creating

[15:36] Java file object.

[15:38] We are just creating Java file object, Java file object, file object to represent the name,

[15:49] to represent the name ABC dot at EXT.

[15:56] To represent the name ABC dot at EXT, to represent the name ABC ABC dot at EXT, EXT, that's all.

[16:02] Are you able to understand?

[16:03] Okay.

[16:04] Now take this complete example once again.

[16:07] Take this one.

[16:09] Take this complete example.

[16:11] In the current working director.

[16:30] Completed right?

[16:36] So, first run, second run.

[16:38] Even I hope you people took this diagram also.

[16:40] Compulsory you have to take.

[16:42] So, file will be created at line number 1 or line number 3.

[16:50] Line number 3.

[16:52] Okay, we have just creating Java file object, but not physical file.

[16:58] Here we are creating physical file.

[17:00] Now, observe.

[17:03] Are you getting the point right clearly?

[17:05] Next up.

[17:06] You know, in Unix, I hope you people may have unique operating system.

[17:13] In Unix, everything is your file.

[17:17] Everything is considered as a file, correct Aataan, even directory also is treated as a file

[17:23] only.

[17:24] Directory also treated as a file.

[17:25] So Java file aivo concept is implemented based on Unix operating system.

[17:31] That's why Java file object.

[17:34] F. Java file object can be used to represent a directory also. Is it clear right now?

[17:41] Let's take example. Let me take one more one more example here.

[17:46] object. File F is equal to, so I am taking, File F is equal to new file of new file of

[17:59] Sir Durga 1 to 3, Sir Durga 1 to 3, Durga 1 to 3 is File name or Director name, Director

[18:08] name, so it is a Durga 1 to 3, that director. Now I am taking, system dot out that print

[18:14] So, if you want to create a file which you matter we use create new file.

[18:43] If you want to create a directory, which method will you add?

[18:46] Create a new directory.

[18:50] You have for data MKDAR.

[18:54] Oh, not create a new directory.

[18:56] But we have method name MKDAR.

[18:59] So even it's a command I hope.

[19:01] It's a command to make a directory.

[19:06] You have for that MKDAR.

[19:08] Automatically, there is a directory named with the

[19:12] Now, system dot out that print on f dot x is a, yes hope you have got x is a, but

[19:26] cannot tell what the answer we are going to get now, f dot x is a true itself is the answer.

[19:31] Hope any explanation is required about this a terminal jana, so we can use a Java file

[19:38] object, two represent by rectory also, territory also, because Java file is a concept is implemented

[19:45] based on Unix operating system right, we can use Java file object, we can use Java file

[19:57] object, to represent, we can use Java file object to represent, to represent by rectory also

[20:07] So we can use Java file object to represent a directory, to represent a directory also,

[20:14] a directory also, take a wish one.

[20:19] File F is equal to, new file of, file F is equal to new file of Durga123, Sopya of F.XJ,

[20:32] next time falls, can you please make that a directory, f dot m k d a r, f dot m k m k

[20:41] d a r, next I hope you have that x j is nothing but true true itself we are going to get,

[20:51] f dot m k d a r, and I hope you have that x j is, but the answer by the following you are

[20:58] going to get a true itself with the answer. Any explanation is required about this one

[21:05] like terminology is that clear for you people. Better to take diagram also. Take this diagram

[21:13] Next, note, note, note, note.

[21:22] In Unix, in Unix, in Unix, in Unix, everything is in Unix, everything, everything is treated as a file.

[21:38] In Unix everything is treated as a file.

[21:42] In Unix everything is treated as a file.

[21:45] As a file, file.

[21:47] Java fileivo concept, Java fileivo concept, Java fileivo concept is implemented.

[21:57] Java fileivo concept is implemented based on Unix operating system.

[22:03] Java file.ivo concept is implemented based on unique operating system based on unique

[22:09] operating system.

[22:11] Inx operating system.

[22:14] Inx operating system.

[22:16] Inx operating system.

[22:18] Hence, hence, hence, Java file object.

[22:23] Java file object can be user.

[22:27] Yawa file object can be used to represent both files under directories.

[22:48] to represent both the files and the directories.

[22:53] Okay, that's all.

[22:55] So this is the way how to create a file,

[22:59] how to create a directorie, I hope you people have here.

[23:03] Now in the file class, what are various constructors are there?

[23:08] In the file, we use already one constructor,

[23:11] but what are various constructors?

[23:13] Keep somebody.

[23:14] File class constructors, file class constructors, file class constructors, file class constructors,

[23:31] okay.

[23:32] Now observe this point, here the first one file F is equal to, new file of analysis

[24:13] in current work in directory then this constructor we have to use but sometimes my requirement is

[24:19] that can you please create a file name it with a bc.exe in E colon some other location

[24:28] any E colon or E colon x magic folder like you may so in some other location how we can

[24:35] create is an ATM which can set up a how to use a file F is equal to new file of

[24:45] a physical new file of string string sub d a y r name string sub d a r name pass what

[24:54] is that in which a sub director you want to create a file comma string name is an ATM

[25:02] like. Sir, in this sub directorate, I want to create a file named with ABC.exchange

[25:09] is nothing but like. So, if you want to create or if you want to represent a file or directory

[25:16] in current working directory, use this constructor. In some other location, use this constructor,

[25:22] regarding that look at this. Third one, file F is equal to new file of, sir, if this

[25:32] is subdirectory already pointed by some file reference, sir inside Durga123, sir

[25:39] Durga123 already pointed by, so some file reference, then not required to spell out subdirectory

[25:47] the name, if you want you can pass the corresponding reference also.

[25:51] File, sub-di-ar, file sub-di-ar, reference, file reference, comma string name is an

[26:02] nothing but like.

[26:03] But how to use these constructors, I will explain with the example, so that then you will

[26:07] get much clarity.

[26:08] But just observe, sir, I want to create a file-ar directory, in current working directory,

[26:15] then we should go for pass one.

[26:17] So I want to create a filer directory in the specified location, in the specified sub

[26:22] location then we should go for second and third constructors write any explanation is required

[26:27] about this at an all janna at this point.

[26:30] I will explain with the example then we will get much clarity at first constructors only

[27:06] Create a Java File object to represent the object to represent the name of the file.

[27:16] Create a Java File object to represent the name of the file or directory.

[27:22] Name of the file or directory.

[27:26] In current working directory, in current working directory, in current working directory,

[27:35] in current working directory, directory.

[27:38] Next up, second one, File is equal to, File is equal to.

[27:46] New file of.

[27:48] File a physical to new file of.

[27:53] String sub d.I.R name.

[27:55] String sub d.I.R name.

[27:58] Subdirector name.

[28:00] Cama string name.

[28:02] File a physical name.

[28:04] File a string sub d.I.R name.

[28:06] Cama string name name.

[28:08] Got the theory.

[28:11] Creates.

[28:12] a Java file object creates, a Java file object creates a Java file object to

[28:21] represent creates a Java file object to represent to represent name of the name of the

[28:32] name of the file or directory, name of the file or directory, name of the file or directory

[28:40] present in, present in, present in, present in some other, present in specified sub directory

[28:51] present in specified sub directory, present in specified sub directory, specified sub directory

[29:00] is the second extra taba file F is equal to new file of file F is equal to new file of file

[29:14] sub DAIR file F is equal to new file of file sub DAIR comma string the name file sub DAIR

[29:24] name.

[29:25] File a physical to new file file sub to you are comma string the name name.

[29:32] Creates creates one minute one minute.

[29:38] Not required to give.

[29:39] Same thing right.

[29:40] Okay this is not required to give any explanation that's all.

[29:43] But once if you see the example then you will come to no much clarity.

[29:48] But remember if you want to create a filer directory,

[29:52] in current working directory, better to go for first one.

[29:55] In the specified sub directory, better to go for next one.

[29:59] Three or four of it is a little bit different.

[30:01] Now, better to take example one.

[30:04] How to use these I will explain.

[30:06] Example one.

[30:08] Write code, write code, write code, write code,

[30:14] to create a file to create a file to create a file named with the right code to create a file named with the ABC dot TXT in current

[30:33] current working director.

[30:35] I am going to be with ABC.exe.

[30:37] In current working director.

[30:40] In current working director.

[30:43] In current working director.

[30:45] Director.

[30:46] Can you spell out?

[30:48] In current working director.

[30:50] I want to create a file.

[30:51] I am going to be with ABC.exe.

[30:53] What is that option?

[30:54] Can you carry out?

[30:55] What is the code?

[30:56] File F is equal to

[31:00] New file of ABC dot txt.

[31:09] Regarding f dot, create a new file.

[31:17] Automatically, in the current working director,

[31:21] ABC dot txt file by default will be created.

[33:02] DEMO.DOT.TXT.

[33:07] DEMO.DOT.TXT.

[33:11] DEMO.DOT.TXT.

[33:14] DEMO.DOT.TXT.

[33:17] DEMO.DOT.TXT.

[33:20] DEMO.DOT.TXT.

[33:23] So, this current director, we have to create water.

[33:29] to 3 folder, in the we have to create a file name with what demo data takes to it.

[33:35] Is it not in my life?

[33:36] Now observe, observe the file.

[33:39] Sir, first what is our requirement?

[33:42] Create a directory, directory Durga 1 to 3, in current work in directory.

[33:48] file okay you are safe file F is equal to new file of file F is equal to new file of

[34:00] what is the code of the Durga 123 okay Durga 123 F for dot mkdi r you have that mkdi r

[34:13] is nothing but like. Now do you know, yeah Durga 1, 2, 3 direct array got created, name

[34:22] with Durga 1, 2, 3 created, Fieda reference variable for that. Up to this which concept

[34:30] are we use first concept like. Now in this Durga 1, 2, 3 I want to create a file name

[34:38] with the a, b, a, d, m, dot at e, x, d. This is my requirement right. So, in this,

[34:45] name it with the d, m, dot, e, x, d, m, dot, e, x, d, I have to create f1 is the reference

[34:52] variable. I want to create this, that's my job. Then what I have to do, which code I have

[34:57] to write? File f1 is equal to new file of, file f1 is equal to new file of, what is the

[35:08] name demodata txt sorry sorry.

[35:12] Hey, file of fun is equal to you file of in Durga 1 to 3 we have to create a demodata

[35:19] txt that is why Durga 1 to 3 comma demodata txt like I am taking.

[35:31] Indurga 1 to 3 demodata txt.

[35:33] Can you tell which concept are we using?

[35:36] Now, instead of second constructor, can you tell any other, what is the other way?

[35:48] File F is equal to, file F1 is equal to, instead of this one, file F1 is equal to, new file

[35:57] of, Sir Durga 1 to 3 already pointed by F. That's why F, Kama, Demo, Data, Txt, F, Kama,

[36:11] Demo, Data, Txt. Now here F means water, this one only. In that Demo, Data, Txt is nothing

[36:17] like. Sir, which constructor I am using? Thar constructor. Now you know, how to use all the

[36:23] three constructors right. If one dot create new file, if one dot create new file is an

[36:32] nothing but like any explanation is required. Okay, this is take this part completed right.

[36:47] Now, from this example, you can aware how to use all the three constructors. File,

[36:58] file, F is equal to new file of vrg123, F dot mkdi, F1 is equal to new file of like this

[37:14] is compulsory or to take diagram also, this is vrg123 within that demo that TXT is there

[37:27] This is how to use all the three constructors.

[37:40] Next example 3.

[37:45] Example 3.

[37:46] Completed right?

[37:51] Example 3.

[37:53] Yeah, no.

[37:54] Write code.

[37:58] Write code.

[38:01] Create a.

[38:02] Write code to create a.

[38:04] To create a.

[38:06] To create a file.

[38:08] To create a file.

[38:10] Name it with ABC.exe.

[38:12] write code to create a file name it with a, b, c dot, x, d in, in, in, e colon, in e colon,

[38:26] in e colon x, y, z, folder, in e colon x, y, z, folder, e colon x, y, z, folder, folder,

[38:37] okay, in e colon x, y, z, folder write a code. What is the possibility, write, and all this

[38:43] is fine. So, very very simple, file F is equal to, new file of Sir in this location we

[38:55] have to create a file. So, which constructor we have to use? Second constructor, E colon

[39:02] x, y, z, kama, a, b, c, dot, t, x, t. Okay. And then f for dot, f for dot, what is the

[39:12] method? Create, create new file. Automatically, in this location, a, b, c, dot, t, x, t,

[39:23] file got created right. Are you able to understand? Okay, this is it. So in some other location

[39:29] how to create a file at this one.

[39:33] File app is equal to file of equal on x file j comma a b c dot x t. You have for dot

[39:45] create new file. You have dot create create new file. You have dot create new file.

[39:54] So, completed I hope now take this diagram anyway this one also take you know so sometime

[40:11] in the last batch somewhere I covered this example but after one or two days some one

[40:18] one student can sir in my system this last example not working properly like he told

[40:26] Then I ask, maybe based on problem I can tell the solution, then I ask, Sir what problem

[40:33] you are facing? Sir, file not found exception, I am getting like. Then, Uche example like

[40:39] I ask, E colon XYJ, can you please create ABC.exe that code not working sir, like. Then

[40:46] immediate I ask, in your system, E colon is there, I am not. Then immediate rate that

[40:52] person told, oh no sir I have only C 100 D drive sir. E drive is not there.

[40:57] Hey without having E drive how this one is going to work? That's why.

[41:02] Asium compels are in our system equal and should be there. In that X Y Y Y Y should be there.

[41:08] Then only this program is going to work. Are getting, if E column is there, X Y Y Y is not there.

[41:13] Are E column not there then we are going to get final form exception on there.

[41:17] for Allah for the Dukadis, tomorrow you may ask the same question, better to get the

[41:21] point.

[41:22] Assume that, assume that, assume that, equal and xyz folder, assume that equal and xyz folder,

[41:32] equal and xyz folder is already available.

[41:36] Assume that, equal and xyz folder is already available, already available in our system.

[41:44] is already available in our system.

[41:47] In our system, that's all.

[41:50] Are you getting?

[41:51] So this is the basic idea how to create a file, how to create a directory and the

[41:56] Vatar various constructors and so on.

[41:59] I took a this.

[42:00] Listen, in the last session, so just we covered how to create a file, how to create a

[42:07] directory.

[42:08] Next also in the current work in the directory to create and even in some other location

[42:14] how to create a file these things.

[42:16] Now in the file class what are various important methods present in the file.

[42:22] In the last session some methods we covered already.

[42:25] Can I can spell out the methods what we covered some methods we covered already.

[42:30] Which methods we covered already.

[42:33] So it says have you ever remembered it says this method we covered.

[42:38] can you please crochet? Whether the physical file available or not? Whether the physical

[42:44] file available, physical directory available or not? Okay, this is your dot adjacent.

[42:50] Next, sorry, if the file is not available, can you please create new file? What is the method

[42:56] we use at f of dot? Create new file. Okay, we cover this one. Next, f of dot, mkdo,

[43:06] Now I have one file reference is there.

[43:13] Can you tell, is this a file reference pointing to a file R point into the director?

[43:24] Because it can point into a file R it can point into a director.

[43:28] Whether I want to check, whether it is representing a file or whether it is representing a director.

[43:34] I am saying this is the directory. If you want to know, simple, F for data is a file.

[43:41] F for data is a directory. Are you getting F for data is a file? F for data is a directory.

[43:49] These methods can check whether F for 0.20 or whether F for 0.20 is a directory or not.

[43:56] Is it clear? I have to say similar line. You are just make sure.

[44:00] So, my F pointing to a director, assume F is pointing to the director, can you tell within

[44:09] the director which things will be there?

[44:11] Within the director which things will be there?

[44:14] There are some files there, there are some sub directories also there.

[44:18] I want to check how many files are there?

[44:21] How many sub directories are there?

[44:23] Can you please list all files and sub directories?

[44:28] present all files and subdirectories present in the specified directory can you please list

[44:33] out then f dot list method.

[44:37] Okay, it is written the names of all files, the names of subdirectories present in this

[44:45] directory.

[44:46] Are you getting?

[44:47] Can you finish me?

[44:48] What is the return type of this method?

[44:49] The return type, e string, here.

[44:53] Look at, different name is one file.

[44:56] This group of file names, or this group of director in name is a

[45:00] present in this director.

[45:02] Isanati Maa, string a array.

[45:05] Arigatang, this is also one method we have.

[45:08] Now, asium, f, point into the file.

[45:12] Sir, f point into the file.

[45:14] In the file, how many amani characters are there?

[45:17] Huge number of characters are there.

[45:19] There may be a chance of several several characters present in the file.

[45:23] I want to know how many number of characters present in the file?

[45:27] Or what is the length of this file?

[45:29] How many number of characters present in the file?

[45:32] F dot the length of method you can.

[45:35] So, do you know, can you tell what is the return type of length method?

[45:39] What is the return type of length method?

[45:42] The return type of length method is not the input.

[45:45] Because the number of characters may exceed the inter-inches.

[45:49] if it is a big file the number of characters may exceed interchange that's why the return

[45:54] type of this method is long.

[45:57] Long L is equal to f dot length, long L is equal to f dot length of method right now.

[46:02] Next step terminology, sir can you please delete this file?

[46:06] Sir, or can you please delete this directory then we should go for f dot deleted.

[46:43] Can you tell how many characters are there in the file?

[46:45] The fact that length of method, so can you please delete this file?

[46:49] Or can you please delete this directly?

[46:51] Then we should go for what?

[46:52] F.delete method, right?

[46:54] Are you able to understand?

[46:55] Important methods present in file class is nothing but like.

[47:00] Now, keep sabiting.

[47:01] Important methods.

[47:03] Important methods.

[47:06] Important methods present in important methods.

[47:12] present in file file class important methods present in file file class file class just

[47:22] better to take from the screen better to take from the from the screen anyway take only

[47:28] first method don't take any other only first method Boolean Boolean exists Boolean exists

[47:36] x axis, Boolean x axis, so can you can you spell out when this method returns true and

[47:46] when this method returns false, this method returns true and when this method returns

[47:51] true if the specified file or directory is available then this method returns true otherwise

[47:59] returns a true true returns a true redness.

[48:06] If this specify return a true if the specified if the specified file or directory returns stronger

[48:21] the term set root has specified a file at directory, available, available, available,

[48:28] available, okay, is the first one.

[48:30] Next, second one, Boolean create a new file, Boolean create a new file, create new file,

[48:42] Boolean create new file.

[48:44] Sir, can you explain on Boolean create new file, just observe, you bit careful it.

[48:49] Can you tell when this method returns true when this method returns false?

[48:56] William create U file when this method returns true when this method returns false.

[49:01] If the file is already available then this method returns false because I didn't create

[49:10] any file because it's already there that's why it returns false without creating any file

[49:15] because it's already there.

[49:16] So, if the specified file not there, then this method creates a new file under return

[49:22] subtrugu.

[49:23] Are you getting?

[49:24] This method will work a bit intelligent way.

[49:26] First, it will check, is it already there or not?

[49:28] If it is already there, if the file is already there, then returns false without creating

[49:34] any file.

[49:35] So, if the file is not there, create any file under return subtrugu.

[49:39] Is it clear for all of you?

[49:41] Okay, at this point.

[49:43] First this method will check, first this method will check,

[49:50] whether the specified file, whether the specified file is already available or not,

[50:01] whether the specified file is already available or not,

[50:10] If it is already available, then this method returns, can I call it as my law, then this

[50:28] method returns false, then this method returns false, without creating, then this method returns

[50:38] without creating, without creating any physical file. Then this method returns false without

[50:46] creating any physical file. Any physical file, any any physical file.

[50:51] Next up, if the file is not already available, if the file is not already available, if

[51:01] the file is not already available, not already available, then this method will create, then

[51:09] this method will create a new file, then this method will create a new file, then this method

[51:16] creates a new file under returns a true, then this method creates a new file under returns

[51:22] a true, under returns a true true, under returns a true that is all.

[51:28] So this is what is the second method that Boolean create new file.

[51:34] And the CN story applicable for Boolean MKDR.

[51:38] So I can tell what is the difference between second method and third method?

[51:41] Everything is the same but instead of file, we'll have to talk in terms of what is directly

[51:46] the, that's why no explanation is required.

[51:48] Boolean, Boolean, Yum K D I R, Boolean, Yum K D I R, Boolean Yum K D I R, okay.

[52:00] Not required to keep any expolension, but next method.

[52:03] Boolean, Boolean, E sub file, Boolean E sub file, Boolean E is file, okay add.

[52:14] に nEIyin is a file and if that is specified is the file object point

[52:40] physical file, point into physical file, physical file, next up.

[52:47] Boolean is a directory. Boolean is a directory. Boolean is a directory. Boolean is a directory.

[52:59] Okay, not required to keep any explanation. Returns a true, don't write it. Returns a true

[53:04] So, if you have a pointing to director, is not required.

[53:08] So, next stringer list.

[53:12] stringer, erer list.

[53:14] Now, can you tell stringer list?

[53:17] What is matter returns?

[53:18] List of matter returns.

[53:19] stringer, what it means?

[53:21] This matter returns.

[53:24] The names of, if this matter returns, the names of all files of the director is.

[53:33] Files and subdirectories present in the space field directory, this method returns, this

[53:39] method returns, the names of all files and subdirectories, all files and subdirectories,

[53:54] is present in specific directory, present in specific directory, present in specific

[54:06] directory, present in specific directory, directory.

[54:10] Okay, is an atrimat like this method, next one, next step.

[54:16] So, long length, long length, not required to keep any explanation what this long length

[54:28] returns, returns, returns number of characters present in, returns number of characters present

[54:37] in, present in specified file, returns number of characters present in the specified file

[54:45] the terms number of characters present in the specified file, next up Boolean, delete,

[54:56] Boolean, delete, delete, delete, delete, delete, to delete, to delete, to delete, specified

[55:08] file to delete specified file or directory to delete specified file or directory or

[55:17] directory specified file or directory.

[55:22] Like if you if you observe here if you if you see the point sir here almost all the methods

[55:29] exist method we covered.

[55:31] Create new file already we use in the last examples.

[55:34] MKDAER we use it. The remaining methods also just to use the remaining, just let me go for

[55:40] one or two examples, I took a add, add one example.

[55:44] Write a program, write a program, write a program to display, write a program to display,

[55:53] to display the names of, write a program to display the names of, the names of all files and

[56:01] directories, radio program to display the names of all files and directories, the names

[56:07] of all files and directories, present in, present in C colon, C colon Durga classes, present

[56:19] in C colon Durga classes, present in C colon Durga classes, Durga classes. Is it clear

[56:30] for all of the doggat this. What is the option or what is the possibility that C colon

[56:35] Durga classes? So in C colon Durga classes, visually my current work in directoria now,

[56:41] yeah, there are several files are there. Sir, there are several directories also there.

[56:48] There are several files are there, several directories are there. Can you please list out the

[56:53] The names of all file summary directories present in C column Durga classes.

[57:00] Correct or not?

[57:01] This is my requirement right.

[57:02] C column Durga classes, in this, what are various file summary directories are there can

[57:07] if we just out is my requirement right.

[57:09] Very simple, let me go for, okay let me let me have write the code further very very simple.

[57:15] are seen. First file F is equal to, file F is equal to new file of, file F is equal

[57:25] to new file of C colon slash Durga classes. Is that nothing but like, file F is equal

[57:32] to new file of C colon slash Durga classes. Now just I created a file difference for this

[57:38] director. Sir in this director, how many files are there? How many directories are there?

[57:44] Please list out the names all. Can you tell which method you have to use?

[57:48] Oh, which method? Yafada. List method. Now the return type of this method is string

[57:57] array. Yes. Now that list string array. Yes. Now I got. Sir, for, for each string,

[58:06] s1 in yesa for every system. So it may be file name or it may be directory name for

[58:13] every name for every system guess 1 in yesa system dot out dot print ln of yesa 1.

[58:21] So I want count also total amani amani files are there are amani directories are there

[58:29] in the count is equal to 0 for every filing count plus plus, count plus plus, no. So,

[58:40] if you have that out there print, count plus plus, I suppose you have the total number,

[58:46] the total number is an estimate lying plus a count. That's all. So, in this total cinema,

[58:54] Okay, which method is the central?

[58:56] Is it not this one?

[58:58] Correct or not?

[58:59] You have to at least, can you please list all the names of all five subdirectories present

[59:05] in this directory?

[59:06] Is it not like we have?

[59:08] Now let me, so go for let me execute this code on a, here see.

[59:13] See this point well, one minute, one minute.

[59:17] Let me go for a simple example.

[59:25] Let me take a simple example.

[59:29] Class test like import java.io.star class test.

[59:34] Intercount is equal to 0.

[59:36] File app is equal to you file app is equal to you.

[59:39] Go through the classes string.

[59:41] Go to the same code.

[59:43] For each string is 1 in yesa.

[59:46] count to plus plus S for P of S 1. The total number is an Atima plus account. Let me say

[59:53] this code has a test dot java. Let me say this code has a test dot java. Now let me compile.

[1:00:02] So, C is my current working director. There are huge number of functions of directories are there.

[1:00:10] Okay, Javasis A test dot Java.

[1:00:14] The code compiles fine.

[1:00:15] Now Java test.

[1:00:17] Java test, ERC.

[1:00:19] Regating there are several several files and subdirectories are there in my system.

[1:00:26] Okay, this is total.

[1:00:27] How many files and directories are there?

[1:00:31] Eight, 19.

[1:00:32] Is it clear for all of you to look at this?

[1:00:34] Total eight, 19, 8 file are directories.

[1:00:38] total number in SQL and Durga class is 8, 19 number is there. Is it clear for all of

[1:00:44] the Durga, take this example, take take clearly. So, this is the simple demo program, how

[1:00:56] to use, so list, list method. So, in a particular folder, how many files are there, how many

[1:01:05] And directories are there like, how many files and how many directories are there, this

[1:01:12] is the way, not required to keep much explanation about this one, completed right.

[1:01:51] So I hope you people so completed, so take take clear like, the total number is an

[1:02:01] that total number number itself is plus count. I hope it is clear for all of you write plus

[1:02:11] count anywhere. Now here okay well you want to take the output right 19 lines are there

[1:02:22] Now, here that E19 number, it may be a file or it may be both. Suppose my programmer

[1:02:33] required, I want to display only filenames, I want to display only filenames but not directories.

[1:02:40] this is keep sub adding to display to display to display only file names only file names

[1:02:55] so to display only file names only only file names okay so can you can you spell out

[1:03:04] where we have to change the code and only one new file names can I spell out where we have to change in this program

[1:03:11] we got all names for every string S1 in yes for the next

[1:03:18] good can you spell out the code?

[1:03:22] what is the code?

[1:03:24] quote. Can you spell out? If, which one is the E's file? Yes, one dot the E's of file.

[1:03:36] If S1 dot is a file, now if S1 dot is a file, count the plus plus, count the plus plus.

[1:03:45] Can you please print the SOP of S1 and of this and then end of the for loop? I am getting

[1:03:54] So now, system dot out that print and the total number of files, the total number of files

[1:04:04] is an atima plus account, correct or not total number of files is plus account.

[1:04:10] If I can take like this, compiler will give you the left hand right.

[1:04:13] Look at this, compiler number will give you are going to get.

[1:04:16] If I can take like, I am doing a silly mistake, small mistake, what that mistake is,

[1:04:22] What is the object? Can I spell out what mistake I am doing?

[1:04:28] Yes, we are doing a small mistake in this code, what mistake we are doing?

[1:04:33] Because we are calling ease of file method on S1.

[1:04:39] We are calling ease file method on S1.

[1:04:42] S1 is what type?

[1:04:44] It is thing type. Sir, ease of file method present in which class?

[1:04:48] File class. File class method, how you can apply on the string object.

[1:04:54] Are you getting file class method we have to apply on file object. File class method we

[1:05:00] have to apply on file object. But not on string object. Immodiacal compound another cannot

[1:05:05] find symbol which is symbol symbol is a file method. In mutual location Java dot lambda string

[1:05:11] are getting in the string class is file method is not there like compound method which you

[1:05:16] So, all the file objects will have to call.

[1:05:20] Now, with this name whatever the name,

[1:05:24] so what is this name? This name can be a file name or can be directory name.

[1:05:31] Either file or directory, present in this directory.

[1:05:36] So, you call them drug classes.

[1:05:38] In this EF, correct or not?

[1:05:40] Vitteth is a name, create a file, I'm getting Vitteth is a name, create a file object.

[1:05:46] What is the way, no? File, file, F1 is equal to, new file of, F1 is equal to new file

[1:05:55] of, make sure this S1 is available in some other location, in sub directory.

[1:06:01] That's why, what is the code? F1, comma, S1.

[1:06:06] F1 means what? C column of the classes.

[1:06:11] In the S1 is an ATM of this file name.

[1:06:13] Are you getting how to create a file object to represent a file, present in some other location.

[1:06:18] Is an ATM like this is a concept.

[1:06:21] Now, if what is the code will have to take?

[1:06:24] F1 dot is file.

[1:06:26] The very man is still wise the same.

[1:06:28] If it is a file, increment count print value.

[1:06:31] If it is not file, that's all.

[1:06:33] I will show anyway right just observe have a look once yeah see total how many number

[1:06:44] is there?

[1:06:46] 819 819 now see can you please guide and up here we have to change the code for within

[1:06:54] of a loop, can not tell what the file F1 is equal to new file of F comma S1, F comma S1

[1:07:04] 1 minute term, F comma S1 and then if F1 dot is a file, so if it is a file, is it a

[1:07:14] Can you please increment count value under then system dot output print like this.

[1:07:21] Are you getting a spoopy?

[1:07:22] The total number of files or the total number no problem at all.

[1:07:27] Now do you know what is the output by default you are going to get?

[1:07:30] I am sure the answer should not be 819 because there are some directories also there right.

[1:07:36] Yes are you getting can you please cut what is the number?

[1:07:42] 800 exactly.

[1:07:43] Oh 8 on it.

[1:07:45] Then how many directories are there?

[1:07:47] Ninety and directories are there, are you getting?

[1:07:49] Suppose my requirement is to display only directories.

[1:07:54] To display only directories.

[1:07:56] Sir this is the code to display only files.

[1:07:58] To display only directories.

[1:08:00] Where we have to change?

[1:08:02] Where we have to change?

[1:08:03] Use of file method, replace with water.

[1:08:06] Use a directorie method.

[1:08:08] Let me do that.

[1:08:09] How many directories are there?

[1:08:11] Ninety.

[1:08:12] Because total number is 19.

[1:08:14] in the t-100 files then the remaining characters,

[1:08:17] how many characters are there?

[1:08:18] 19 characters are there, isn't that much like

[1:08:21] now here see file F is equal to you file.

[1:08:24] If E is what is the method?

[1:08:27] Directary, E is a directory like this.

[1:08:31] Now have you looked?

[1:08:33] What is the output by default here going to get?

[1:08:35] Isn't that much?

[1:08:36] How many number are not 19?

[1:08:38] Is it match or not?

[1:08:40] That's what you have to remember, will.

[1:08:42] Okay, this is it.

[1:08:43] What what? Heading you took Keneke Nishpala to display only file names. Okay. Better to take this code.

[1:08:50] Not required to complete program. Take this one. In the count is equal to 0.

[1:08:56] File F is equal to new file of C colon slash slash Durga classes.

[1:09:07] string array, s is equal to f dot least method, string array s is equal to f dot least

[1:09:19] least method next time. For each string to s1 in s, for each string s1 in s, in s, file

[1:09:31] In yes, file of one is equal to file of F, S, 1 like better to use.

[1:09:38] This is the demo program to demonstrate how to use ease of file method.

[1:09:45] Number of files is nothing but plus count.

[1:10:04] The total number of files is plus count like completed right?

[1:10:16] That's all.

[1:10:20] This is what what you people should aware clearly write.

[1:10:23] in count is equal to 0, file your physical to new file of like, is it clear for all of

[1:10:35] you that look at this is, now the next one, okay this is keep sabading, can I complete

[1:10:42] that right, next up, to display, to display, to display only, only directory names, to

[1:10:58] to display only directory names.

[1:11:05] Okay, not required to take this total code.

[1:11:08] Can you tell what change we have to do?

[1:11:11] Yes, a file method, can you replace with water?

[1:11:15] Yes, a directory method.

[1:11:18] Beyond that, there is nothing.

[1:11:20] Okay, add.

[1:11:21] In the above program, in the above program,

[1:11:26] We have to replace and by above program we have to replace and by above program we have

[1:11:33] to replace replace.

[1:11:35] E is a file, we have to replace E is a file, E is file method, E is file method with the

[1:11:45] with the E is a directory method, E is file method with the E is a directory method, E is

[1:11:54] a directory method, method like, so that's all. I hope you people can aware now what

[1:12:02] is the purpose, I mean E is file method out to use E is a directory list method like that's

[1:12:08] all this is above what are various important methods present in file class and how to use

[1:12:14] that's right.

[1:12:15] Okay.

End of Video 120 notes — File I/O Part 1: Introduction & File class

## Tables (placement lost -- re-place these in context)

| Field | Detail |  |  |  |  |
|---|---|---|---|---|---|
| Title | Core Java With OCJP/SCJP: File I/O Part-1 \ | \ | Introduction \ | \ | File |
| Playlist | Core Java With OCJP/SCJP (Durga Sir) |  |  |  |  |
| Position | 120 of 203 |  |  |  |  |
| Series | File I/O · Part 1 |  |  |  |  |
| Topic | Introduction to File I/O; java.io.File class — constructors & important methods |  |  |  |  |
| Instructor | Durga Sir (Durga Software Solutions) |  |  |  |  |
| Duration | 1h 12m 26s |  |  |  |  |
| Video ID | rxo1SZmq9VE |  |  |  |  |
| Watch | https://www.youtube.com/watch?v=rxo1SZmq9VE |  |  |  |  |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |  |  |  |  |
| Notes source | Local Whisper STT (no YouTube auto-captions) |  |  |  |  |

| Era | SCJP version | File I/O on exam? | Typical questions |
|---|---|---|---|
| Java 1.0–1.3 (1995+) | SCJP 1.1, 1.2 | Very important | 7–8 questions |
| Java 1.4 (~2003–2004) | SCJP 1.4 | Removed | Databases became dominant |
| Java 1.5–1.6 | SCJP 1.5/1.6 | Reintroduced | 2–3 questions |

| # | Class | Purpose (preview) |
|---|---|---|
| 1 | `File` | Represent file/directory path; metadata & filesystem operations |
| 2 | `FileWriter` | Character output to file |
| 3 | `FileReader` | Character input from file |
| 4 | `BufferedWriter` | Buffered character output |
| 5 | `BufferedReader` | Buffered character input |
| 6 | `PrintWriter` | Formatted character output |

| Line | Action | Physical file on disk? |
|---|---|---|
| File f = new File("ABC.txt"); | Create Java object representing name | NO |
| f.createNewFile(); | Create actual file if absent | YES (if didn't exist) |

| Goal | Method |
|---|---|
| Create file | createNewFile() |
| Create directory | mkdir() |

| Constructor | Use when |
|---|---|
| File(String name) | File/directory in current working directory |
| File(String parent, String child) | File/directory in another location (e.g. E:\\xyz\\ABC.txt) |
| File(File parent, String child) | Parent directory already referenced by another File object |

| Scenario | Constructor |
|---|---|
| demo.txt in current folder | new File("demo.txt") |
| demo.txt in Durga123/ | new File("Durga123", "demo.txt") |
| demo.txt when File dir already points to Durga123 | new File(dir, "demo.txt") |
| ABC.txt in E:\\xyz\\ | new File("E:\\xyz", "ABC.txt") |

| Code | Creates physical entity? |
|---|---|
| new File("x.txt") | No — object only |
| new File("x.txt").createNewFile() | Yes — file (if absent) |
| new File("dir").mkdir() | Yes — directory (if absent) |
| new File("E:\\xyz", "a.txt").createNewFile() | Yes — if E:\xyz exists |

| Method | Return type | Purpose |
|---|---|---|
| exists() | boolean | true if specified file or directory exists on disk |
| createNewFile() | boolean | Create new file if absent |
| mkdir() | boolean | Create new directory if absent |
| isFile() | boolean | true if this File object points to a file |
| isDirectory() | boolean | true if this File object points to a directory |
| list() | String[] | Names of all files and subdirectories in this directory |
| length() | long | Number of bytes in file (not int — large files exceed int range) |
| delete() | boolean | Delete specified file or directory |

| Method | Returns false when |
|---|---|
| createNewFile() | File already exists (no new file created) |
| mkdir() | Directory already exists |
| exists() | File/directory not on disk |
| delete() | Deletion failed |

| Heard (Whisper) | Intended |
|---|---|
| File Ivo / file aivo / file logo | File I/O |
| SEJP / CGP / shadow | SCJP / certification exam |
| ABC.exe / ABC.xt / at EXT | ABC.txt |
| mkdi r / MKDAR / mkdo | mkdir |
| sub d.I.R / sub DAIR | subdirectory (String parent param) |
| ease of file / E sub file | isFile() |
| E's a directory / ease a directorie | isDirectory() |
| stringer list / erer list | String[] list() |
| Durga 1 to 3 / vrg123 | Durga123 |
| compound method / compultimate | compile error |
| unique operating system | Unix operating system |
| amani characters | how many characters |
| C column Durga classes | C:\\DurgaClasses |
| demodata txt / demo data takes | demodata.txt |
