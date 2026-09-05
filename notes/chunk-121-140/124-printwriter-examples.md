# Video 124

## Video info

Title: Core Java With OCJP/SCJP: File I/O Part- 5||Printwriter-Examples

### 00:04 — Recap of File I/O classes covered so far

Durga Sir opens by recapping prior sessions: File, FileWriter, FileReader, BufferedWriter, BufferedReader, and related small applications — how to perform I/O line by line or file by file.

Two more real-world programs remain in this File I/O block before the topic closes.

### 00:48 — Real business problem: bulk SMS before new batches

Context (Durga Soft training institute): Before every new SCJP/Java batch, SMS alerts were sent to inquiry database numbers — historically 10 lakh to 20 lakh mobile numbers per campaign.

Economics of bulk SMS (ASR decoded):

- Earlier: 1 lakh SMS ≈ ₹1,750
- After government intervention: 1 lakh SMS ≈ ₹50,000
Why prices spiked: A rumor spread via bulk SMS (North–South tension in Bangalore/Manipal/Assam context). Government response:

- 15-day bulk SMS ban
- Daily cap on personal SMS (100–150 messages/day)
- Instead of permanent ban, massive price hike so misuse becomes costly
Impact on businesses: ICICI Bank-style transactional SMS, Google SMS Channel (9848098480-style subscription service) — all paused because cost became prohibitive.

### 05:28 — Wrong-number calls after SMS blast

After sending batch-start SMS, reception got mixed calls:

Reception staff faced abusive/vulgar calls; one employee resigned because threatening calls kept coming even after promising "we won't send again."

### 09:14 — Solution: `delete.txt` opt-out list

Process agreed with admin/reception:

- On complaint call → note mobile number in `delete.txt`
- Send delete.txt to the person managing SMS
- Before next blast → remove those numbers from master list
- SMS only to remaining numbers
Requirement stated on board:

Write a Java program to perform file extraction operation.

Formula (board):

output = input − delete

Remove every number present in delete.txt from input.txt; write survivors to output.txt.

### 10:18 — Sample files on board

`input.txt` (master list — example numbers):

tri2
tri3
tri4
tri5
tri6
tri7
tri8
tri9

(ASR garbles as "Tri2 Tri3…6789" — board intent is one mobile number per line.)

After first round of complaints, `delete.txt`:

tri5
tri8
tri2

Expected `output.txt`:

tri3
tri4
tri6
tri7
tri9

Logic (line-by-line trace):

- Read one line from input.txt
- Compare against every line in delete.txt
- If match found → do not write (skip SMS)
- If no match after scanning entire delete file → PrintWriter.println(line) to output.txt
- Repeat for all input lines
### 13:29 — Student pause: "write your program"

Sir repeats the assignment several times so students attempt it before the solution:

Write a program to perform file extraction operation.

### 16:01 — Algorithm before coding

Outer loop: read each line from input.txt via BufferedReader (br1).

Inner loop: for that line, scan delete.txt via second BufferedReader (br2 / br1 in transcript).

Boolean flag:

```java
boolean available = false;
```

- If line.equals(target) → available = true; break;
- Else read next delete line: target = br2.readLine();
After inner loop:

- If available == false → number not in delete list → write to output
- If available == true → skip
I/O class choice (Durga Sir convention):

- Reading → BufferedReader (wraps FileReader)
- Writing → PrintWriter
### 17:20 — Board code: `FileExtractor`

```java
// Board skeleton — class FileExtractor
PrintWriter pw = new PrintWriter("output.txt");
BufferedReader br1 = new BufferedReader(new FileReader("input.txt"));
String line = br1.readLine();
while (line != null) {
    boolean available = false;
    BufferedReader br2 = new BufferedReader(new FileReader("delete.txt"));
    String target = br2.readLine();
    while (target != null) {
        if (line.equals(target)) {
            available = true;
            break;
        }
        target = br2.readLine();
    }
    if (available == false) {
        pw.println(line);
    }
    line = br1.readLine();
}
pw.flush();
```

CE: Needs import java.io.*;, public class FileExtractor, and main — Sir writes executable version on screen.

### 25:31 — Live execution demo

Compile & run:

```java
// Terminal commands (not Java — shown on screen)
// javac FileExtractor.java
// java FileExtractor
```

Demo files:

- input.txt: tri2, tri3, tri4, tri5, tri6, tri7, tri8, tri9
- delete.txt: tri5, tri8, tri2
- `output.txt` result: tri3, tri4, tri6, tri7, tri9 ✓
Dynamic update demo: Add tri7 to delete.txt, re-run → tri7 disappears from output; only four numbers remain for SMS.

### 28:41 — Production use at Durga Soft

Sir gave this program to admin staff workflow:

- Put all target numbers in `input.txt`
- Put opt-out numbers in `delete.txt`
- Run Java program
- Use `output.txt` numbers for actual SMS send
This eliminated wrong-number harassment at scale.

### 29:18 — Full board program copied (FileExtractor complete)

```java
import java.io.*;

class FileExtractor {
    public static void main(String[] args) throws Exception {
        PrintWriter pw = new PrintWriter("output.txt");
        BufferedReader br1 = new BufferedReader(new FileReader("input.txt"));
        String line = br1.readLine();
        while (line != null) {
            boolean available = false;
            BufferedReader br2 = new BufferedReader(new FileReader("delete.txt"));
            String target = br2.readLine();
            while (target != null) {
                if (line.equals(target)) {
                    available = true;
                    break;
                }
                target = br2.readLine();
            }
            if (available == false) {
                pw.println(line);
            }
            line = br1.readLine();
        }
        pw.flush();
    }
}
```

Print/CE notes:

- throws Exception — Sir avoids try/catch in classroom demos
- pw.flush() — ensures buffered output reaches disk before program ends
- Inner BufferedReader on delete.txt reopened per input line (simple but O(n×m); acceptable for teaching)
### 32:44 — Second real problem: duplicate numbers in database

Story: Same student number stored multiple times:

- Inquiry → demo → registration for Core Java = 3 entries
- Repeat for Advanced Java and Struts = 9 entries for one person
Meeting-room embarrassment: Ex-employee in serious company meeting (40 people) receives 9 identical "Durga Soft new SCJP batch" SMS within minutes — ringtone in hot meeting → account manager humiliation → employee calls to remove number.

Two problems identified:

- Reputation / goodwill damage
- Financial waste — 9 SMS charges for one person; that cost could reach 9 others
Requirement:

Write a Java program to remove duplicates from the given input file.

Output: `output.txt` with unique numbers only (first occurrence kept).

### 40:18 — Sample duplicate input

`input.txt` (board example):

tri2
tri3
tri2
tri4
tri2
tri4
tri3
tri5
tri2
tri4
tri5
tri6

Expected unique `output.txt`:

tri2
tri3
tri4
tri5
tri6

Logic: Same structure as FileExtractor, but compare current line against `output.txt` so far (not a separate delete file):

- If already written to output → ignore (duplicate)
- If not found in output → write + flush immediately so next comparison sees it
### 42:18 — Board code: `DuplicateEliminator`

```java
PrintWriter pw = new PrintWriter("output.txt");
BufferedReader br1 = new BufferedReader(new FileReader("input.txt"));
String line = br1.readLine();
while (line != null) {
    boolean available = false;
    BufferedReader br2 = new BufferedReader(new FileReader("output.txt"));
    String target = br2.readLine();
    while (target != null) {
        if (line.equals(target)) {
            available = true;
            break;
        }
        target = br2.readLine();
    }
    if (available == false) {
        pw.println(line);
        pw.flush();   // critical — next read must see newly written line
    }
    line = br1.readLine();
}
```

### 47:41 — "Empty output file" doubt resolved

Student doubt: At start output.txt is empty — how does comparison work?

Trace for first line `tri2`:

- Open output.txt → readLine() returns `null`
- Inner while (target != null) never runs
- available stays `false`
- Write tri2 → program works from first line onward
Sir: "100% it is going to work — valid program."

### 48:49 — Large-scale demo: 3,186 → 6 unique numbers

Sir copy-pastes repeated numbers into input.txt:

- 3,186 / 3,187 numbers in input (ASR varies)
- After run, `output.txt`: tri2, tri3, tri4, tri5, tri6, tri7 — only 6 unique lines
Compile & run:

```java
// javac DuplicateEliminator.java
// java DuplicateEliminator
```

### 49:44 — Complete DuplicateEliminator program

```java
import java.io.*;

class DuplicateEliminator {
    public static void main(String[] args) throws Exception {
        PrintWriter pw = new PrintWriter("output.txt");
        BufferedReader br1 = new BufferedReader(new FileReader("input.txt"));
        String line = br1.readLine();
        while (line != null) {
            boolean available = false;
            BufferedReader br2 = new BufferedReader(new FileReader("output.txt"));
            String target = br2.readLine();
            while (target != null) {
                if (line.equals(target)) {
                    available = true;
                    break;
                }
                target = br2.readLine();
            }
            if (available == false) {
                pw.println(line);
                pw.flush();
            }
            line = br1.readLine();
        }
    }
}
```

Key difference from FileExtractor:

### 56:20 — File I/O topic closure & SCJP exam note

- File I/O concept ends here for this playlist block
- For SCJP/OCJP: expect 2–3 questions on File I/O — not the most heavily weighted topic, but not ignorable
- Both programs reinforce `PrintWriter` + `BufferedReader` pattern from prior PrintWriter sessions
## Summary table

Java code block count: 7

## Tables (placement lost -- re-place these in context)

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP |
| Position | 124 of 203 |
| Series | Core Java With OCJP/SCJP |
| Topic | File I/O — Part 5 (PrintWriter Examples / File Extraction & Duplicate Removal) |
| Instructor | Durga Sir |
| Duration | 56m 51s |
| Video ID | l8ONfuJo7wg |
| Watch | https://www.youtube.com/watch?v=l8ONfuJo7wg |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

| Caller type | Example reaction |
|---|---|
| Valid inquiry | "When is SCJP batch? Who is faculty? Fee? Demo date?" |
| Wrong number | Auto driver: "What is SCJP? Why SMS me?" (number reused from former student) |
| Professional | Orthopedic surgeon at IM Hospital: "What is Java?" |
| Threat | SI from Nagar police station: "Tell your address — I will shoot each person" |

| Program | Compare against | flush? |
|---|---|---|
| FileExtractor | delete.txt | end only |
| DuplicateEliminator | output.txt (self) | after each write |

| Program | Input | Second file | Output formula | Use case |
|---|---|---|---|---|
| FileExtractor | input.txt | delete.txt | input − delete | SMS opt-out / blacklist |
| DuplicateEliminator | input.txt | (reads own output.txt) | unique lines | SMS deduplication |
