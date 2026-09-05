# Video 135 — Regular Expressions Part 4: How to Use Regular Expressions

## Video info

Title: Core Java With OCJP/SCJP: RegularExpresions Part-4 || How to use Regular Expresions

URL: https://www.youtube.com/watch?v=IZt3rF8YAEA

Duration: ~57m 48s

Position: Video 135 of 203 in the Durga Sir OCJP/SCJP playlist

Prerequisite: Videos 132–134 covered Pattern/Matcher basics, character classes, quantifiers, Pattern.split(), and how to write regex for mobile numbers, email IDs, and Java identifiers. This lecture is entirely about how to use those regexes in real Java programs — validation and extraction.

## 00:04 — Recap & today's shift: from writing regex to using regex

Durga Sir opens by recapping the previous session's writing exercises:

- Write a regex to represent all mobile numbers
- Write a regex to represent all mail IDs
- Write a regex to represent all Java language identifiers
That was the "how to write" part. Today's target:

How to use these regular expressions inside Java programs — validation logic, file extraction, and directory filtering.

Real-world connection: whenever you submit a form and see "Please enter your valid mobile number" or "Please enter your valid mail ID", internally this type of Pattern/Matcher logic is running.

## 00:31 — Example 1 (board): Validate mobile number from command line

### Requirement (board wording)

Write a program to check whether the given number is a valid mobile number or not.

- Input: a number passed from the command prompt (args[0])
- Output: print "valid mobile number" or "invalid mobile number"
### Mobile number rules (from Video 134 — Sir repeats here)

A valid mobile number has exactly one of these formats:

Regex (from previous lecture):

(0|91)?[789][0-9]{9}

Breakdown:

In Java source: "(0|91)?[789][0-9]{9}"

### Test cases Sir walks through (before coding)

## 03:03 — RegexDemo / LectureDemo: step-by-step validation program

### Standard two-step Pattern/Matcher workflow

Step 1 — Create a Pattern object representing the mobile-number regex:

Pattern p = Pattern.compile("(0|91)?[789][0-9]{9}");

Step 2 — Create a Matcher object to match that pattern against the command-line argument:

Matcher m = p.matcher(args[0]);

### How many matches in `args[0]`?

Sir emphasizes: for this validation program, at most one match exists in the input string — the entire input is the mobile number. You are not searching a long text for embedded numbers.

- No `while (m.find())` loop needed here — a single if (m.find()) suffices.
- Contrast with the file-extraction example later, where multiple matches per line require a while loop.
### Complete board program — RegexDemo2 (mobile validation)

```java
import java.util.regex.*;

class RegexDemo2 {
    public static void main(String[] args) {
        Pattern p = Pattern.compile("(0|91)?[789][0-9]{9}");
        Matcher m = p.matcher(args[0]);
        if (m.find() && m.group().equals(args[0])) {
            System.out.println("valid mobile number");
        } else {
            System.out.println("invalid mobile number");
        }
    }
}
```

### THE CRITICAL TWIST — `m.find()` alone is NOT enough

Sir spends significant time on this — the most common mistake in validation programs.

#### Problem: partial (substring) match vs full-string match

m.find() searches for the pattern anywhere in the input. It returns true if any substring matches — even when the entire string is not a valid mobile number.

Example that breaks naive code:

Input: 9292929292929292   (16 digits — INVALID)

Trace with regex (0|91)?[789][0-9]{9}:

- m.find() → true — because substring 9292929292 (or similar 10–12 digit chunk starting with 9) matches the pattern internally
- But the full input is NOT a valid mobile number
#### Solution — second condition: `m.group().equals(args[0])`

if (m.find() && m.group().equals(args[0]))

Sir's board wording:

"Which thing got matched? And which thing was provided — both are equal or not?"

- Matched thing = m.group() — what the regex engine actually captured
- Provided thing = args[0] — what the user passed
- Both must be identical for validation to pass
#### Truth table for all four test cases

## 09:31 — Live demo: proving the bug without the second condition

Sir runs RegexDemo2 without the m.group().equals(args[0]) check — only if (m.find()).

### Compile & run commands

javac RegexDemo2.java
java RegexDemo2 9848022338        → valid mobile number   ✅
java RegexDemo2 09804802238       → valid mobile number   ✅
java RegexDemo2 919293949596      → valid mobile number   ✅
java RegexDemo2 9292929292929292  → valid mobile number   ❌ WRONG!

Without the second condition, the last case incorrectly prints "valid mobile number" even though 16 digits is invalid.

With both conditions, the last case correctly prints "invalid mobile number".

Exam trap: OCJP questions often test whether you know that find() alone validates a substring, not the whole string. Always pair find() with group().equals(fullInput) for exact validation.

## 14:01 — Validation framework connection

Sir connects this to web/form validation:

- User enters mobile number in a form field
- On submit, server-side (or client-side) code runs Pattern/Matcher logic
- If validation fails → error message: "Please enter your valid mobile number"
The Java program you write today is the same logic used inside validation frameworks — just without the UI wrapper.

Take the RegexDemo2 program as-is — it is the canonical validation template.

## 17:03 — Example 2: Validate email ID (same program, different regex)

### Requirement

Write a program to check whether the given mail ID is valid or not.

Sir's answer: "The only difference — replace mobile number regular expression with mail ID regular expression."

### Email regex (from Video 134)

[a-zA-Z0-9][a-zA-Z0-9_.]+@[a-zA-Z0-9]+(\.[a-zA-Z]+)+

Breakdown:

In Java: "[a-zA-Z0-9][a-zA-Z0-9_.]+@[a-zA-Z0-9]+(\\.[a-zA-Z]+)+"

### Board program — RegexDemo (email validation)

```java
import java.util.regex.*;

class RegexDemo {
    public static void main(String[] args) {
        Pattern p = Pattern.compile(
            "[a-zA-Z0-9][a-zA-Z0-9_.]+@[a-zA-Z0-9]+(\\.[a-zA-Z]+)+");
        Matcher m = p.matcher(args[0]);
        if (m.find() && m.group().equals(args[0])) {
            System.out.println("valid mail ID");
        } else {
            System.out.println("invalid mail ID");
        }
    }
}
```

### Test cases Sir runs

Sir notes: no need to re-explain how to write the email regex — that was covered in detail in Video 134. Focus here is usage.

## 21:11 — Example 3: Extract all mobile numbers from an input file

### Requirement (board wording)

Write a program to read all mobile numbers present in the given input file, where mobile numbers are mixed with normal text data, and write them to a separate output file.

### Real-world motivation

Suppose input.txt contains:

This is Durga.
This is Durga with mobile number 9848022338.
This is Ravi with mobile number 809696...
... some mail IDs and mobile numbers mixed in ...
9123456781
929292929292

Manually copying each mobile number is tedious. A Java program can extract one lakh mobile numbers in one or two minutes and write them to output.txt — useful for bulk SMS campaigns, contact list building, etc.

### I/O class choices (Sir's recommendations)

Both were covered in the File I/O lectures (Videos 121–124).

### Algorithm (board steps)

- Create PrintWriter for output.txt
- Create Pattern for mobile regex
- Create BufferedReader for input.txt
- Read line by line in a while (line != null) loop
- For each line, create Matcher and loop while (m.find()) — multiple matches per line possible
- For each match, pw.println(m.group()) — write matched mobile number to output
- After all lines, call pw.flush() and pw.close()
### Key difference from validation example

### Complete board program — MobileExtractor1.java

```java
import java.io.*;
import java.util.regex.*;

class MobileExtractor1 {
    public static void main(String[] args) throws IOException {
        PrintWriter out = new PrintWriter("output.txt");
        Pattern p = Pattern.compile("(0|91)?[789][0-9]{9}");
        BufferedReader br = new BufferedReader(
            new FileReader("input.txt"));
        String line = br.readLine();
        while (line != null) {
            Matcher m = p.matcher(line);
            while (m.find()) {
                out.println(m.group());
            }
            line = br.readLine();
        }
        out.flush();
        out.close();
        br.close();
    }
}
```

### Nested loop structure explained

while (line != null) {          // outer: every line in input file
    Matcher m = p.matcher(line);
    while (m.find()) {          // inner: every mobile number in this line
        out.println(m.group());
    }
    line = br.readLine();
}

Sir's wording: "This cycle by default will be repeated for every line present in the input file."

### Live demo results

Sir's input.txt contained 5 mobile numbers scattered across mixed text. After running:

javac MobileExtractor1.java
java MobileExtractor1

Opening output.txt shows all 5 extracted numbers, one per line — including numbers embedded mid-sentence like "mobile number 9848022338".

## 36:33 — Example 4: Extract all mail IDs from input file

### Requirement

Write a program to extract all mail IDs present in the given input file, where mail IDs are mixed with normal text.

### Sir's answer — one-line change

"Program is the same. Only difference — replace mobile number regular expression with mail ID regular expression."

Replace in MobileExtractor1:

```java
// FROM:
Pattern p = Pattern.compile("(0|91)?[789][0-9]{9}");

// TO:
Pattern p = Pattern.compile(
    "[a-zA-Z0-9][a-zA-Z0-9_.]+@[a-zA-Z0-9]+(\\.[a-zA-Z]+)+");
```

Everything else — PrintWriter, BufferedReader, nested while loops, flush(), close() — stays identical.

### Live demo

Sir runs the modified program. output.txt now contains mail IDs like:

- Durga@versi (example from input)
- Ravi.com (partial — depends on input data)
- Nagar.wara_Prasad123 (examples from Sir's sample file)
Same automation benefit: extract all email addresses from a large document in seconds.

## 40:38 — Example 5: Display all `.txt` file names in a directory

### Requirement (board wording)

Write a program to display all `.txt` file names present in `C:\DurgaClasses`.

Sir's working directory is C:\DurgaClasses — it contains:

- Several .java files
- Several .class files
- Several .txt files
- Some subdirectories
Goal: list only `.txt` files (not .java, not .class, not backup files).

### Backup-file trap — why full match matters again

If you only check m.find(), abc.txt.bak would match because `abc.txt` is a substring. Same partial-match bug as mobile validation!

### Regex for `.txt` file names

Allowed characters in file name (before .txt):

- a-z, A-Z, 0-9, _, ., $ — any number of times, at least once
- Must end with literal .txt
[a-zA-Z0-9_.$]+\.txt

Why dot inside `[ ]` or escaped?

Sir asks: "Why am I taking that within square bracket?"

- . outside brackets = any character (dangerous — Video 133)
- \. or [.] = literal dot symbol only
For .txt suffix, use \.txt in the regex (Java string: "\\.txt").

### Complete board program — FileNameExtractor.java

```java
import java.io.*;
import java.util.regex.*;

class FileNameExtractor {
    public static void main(String[] args) {
        int count = 0;
        Pattern p = Pattern.compile("[a-zA-Z0-9_.$]+\\.txt");
        File f = new File("C:\\DurgaClasses");
        String[] s = f.list();
        for (String s1 : s) {
            Matcher m = p.matcher(s1);
            if (m.find() && m.group().equals(s1)) {
                System.out.println(s1);
                count++;
            }
        }
        System.out.println("The total number :" + count);
    }
}
```

### API walkthrough

### Live demo result

javac FileNameExtractor.java
java FileNameExtractor

Output: 116 .txt files listed, ending with:

The total number :116

Examples from output: output.txt, SIT.txt, SanRathi.txt, etc.

## 51:25 — Variations: `.java`, `.class`, and alternation `(java|class)`

Sir demonstrates the same program with small regex changes:

### Variation A — `.java` files only

Change regex suffix:

Pattern p = Pattern.compile("[a-zA-Z0-9_.$]+\\.java");

Result: 360 .java files in C:\DurgaClasses.

### Variation B — `.class` files only

Pattern p = Pattern.compile("[a-zA-Z0-9_.$]+\\.class");

Result: 226 .class files.

Sir notes: "Don't tell for every .java file one .class file — no guarantee." (Inner classes, compilation failures, etc. can cause mismatched counts.)

### Variation C — `.java` OR `.class` (alternation)

Pattern p = Pattern.compile("[a-zA-Z0-9_.$]+\\.(java|class)");

Board wording: "File name ends with either `.java` or `.class`."

- (java|class) — grouping with OR: match either literal java or literal class
- Total: 360 + 226 = 586 files
This introduces regex alternation in a practical context — the | inside (...) means OR.

## 55:09 — Lecture wrap-up & exam guidance

### Application areas of regular expressions (summary)

### Exam expectations

*"For the exams sake minimum two questions you can expect from this area — two bits you can expect from exam purpose."*

Regular expressions is a special area — many candidates lack clarity. Sir urges:

- Have special clarity on Pattern/Matcher workflow
- Know the `find()` vs full-match distinction (validation trap)
- Know when to use `if (find())` vs `while (find())`
- Know `Pattern.split()` vs `String.split()` (Video 134)
- Know practical regexes: mobile, email, filename patterns
This is the last example in the regular expressions series (Parts 1–4).

## Master reference — regex patterns used in this lecture

## Decision guide — `if (find())` vs `while (find())`

## OCJP/SCJP checklist — Video 135

- [ ] Validation template: Pattern.compile → matcher(input) → if (find() && group().equals(input))
- [ ] Know why find() alone gives false positives on long digit strings
- [ ] Extraction template: BufferedReader read lines → while (m.find()) → PrintWriter.println(group())
- [ ] Remember flush() and close() on PrintWriter
- [ ] Directory listing: File → list() → iterate → matcher per name
- [ ] Escape literal dot in regex: \\. or [.]
- [ ] Alternation for multiple extensions: \\.(java|class)
- [ ] Replace regex string to switch between mobile/email/file applications — program structure stays same
## Quick revision card

VALIDATE:  compile → matcher(input) → if(find && group().equals(input))
EXTRACT:   compile → read lines → while(find) → println(group())
FILTER:    compile → File.list() → for each name → if(find && group().equals(name))

Golden rule: When the entire input must match, always add m.group().equals(fullInput).

## Tables (placement lost -- re-place these in context)

| Format | Digits | Rule |
|---|---|---|
| 10-digit | 10 | First digit must be 7, 8, or 9 |
| 11-digit | 11 | First digit must be 0, then 10-digit mobile |
| 12-digit | 12 | First two digits must be 91, then 10-digit mobile |

| Fragment | Meaning |  |
|---|---|---|
| `(0\ | 91)?` | Optional prefix: either 0 or 91, zero or one time |
| [789] | First digit of the 10-digit core must be 7, 8, or 9 |  |
| [0-9]{9} | Remaining 9 digits (any digit 0–9) |  |

| Input | Valid? | Why |
|---|---|---|
| 9804332238 | ✅ Yes | 10 digits, starts with 9 |
| 09804802238 | ✅ Yes | 11 digits, leading 0 |
| 919293949596 | ✅ Yes | 12 digits, leading 91 |
| 9292929292929292 | ❌ No | 16 digits — too long; not 10/11/12 |

| Check | 9292929292929292 |
|---|---|
| m.find() | ✅ true (partial match found) |
| Full string valid? | ❌ No — 16 digits |

| Condition | Meaning |
|---|---|
| m.find() | At least one match exists in the input |
| m.group().equals(args[0]) | The matched substring equals the entire input — total thing matched, not just a part |

| Input | m.find() | m.group().equals(args[0]) | Result |
|---|---|---|---|
| 9804332238 | true | true | valid mobile number |
| 09804802238 | true | true | valid mobile number |
| 919293949596 | true | true | valid mobile number |
| 9292929292929292 | true | false | invalid mobile number |

| Fragment | Meaning |
|---|---|
| [a-zA-Z0-9] | First character must be alphanumeric |
| [a-zA-Z0-9_.]+ | Local part: letters, digits, _, . — one or more |
| @ | Literal at-sign |
| [a-zA-Z0-9]+ | Domain name (gmail, yahoo, etc.) — at least one char |
| (\.[a-zA-Z]+)+ | One or more dot-suffix groups (.com, .co.in, etc.) |

| Input | Valid? | Why |
|---|---|---|
| Durga123.ABC | ❌ No | No @ and no domain |
| cm@gmail | ❌ No | Missing .com (or any TLD) |
| cm@gmail. | ❌ No | Dot at end with no TLD letters |
| cm@gmail.com | ✅ Yes | Complete local@domain.tld |

| Task | Best class | Why |
|---|---|---|
| Read from file | BufferedReader wrapping FileReader | Best reader for line-by-line file reading |
| Write to file | PrintWriter | Best writer for writing data to a file |

| Validation (Example 1) | Extraction (Example 3) |
|---|---|
| Input = single command-line arg | Input = entire file, line by line |
| At most one match | Multiple matches per line possible |
| if (m.find()) once | while (m.find()) loop |
| Must check full-string match | Write each m.group() — partial matches are desired |

| File name | Should match? | Why |
|---|---|---|
| abc.txt | ✅ Yes | Normal text file |
| 123abc.txt | ✅ Yes | Digits allowed in name |
| abc.txt.bak | ❌ No | Backup file — ends with .bak, not .txt |
| abc.txt.backup | ❌ No | Same reason |

| Fragment | Meaning |
|---|---|
| [a-zA-Z0-9_.$]+ | One or more allowed filename characters |
| \.txt | Literal dot + txt (escaped dot — not "any character") |

| Step | Code | Purpose |
|---|---|---|
| Create Pattern | Pattern.compile("[a-zA-Z0-9_.$]+\\.txt") | Regex for .txt filenames |
| Create File object | new File("C:\\DurgaClasses") | Point to target folder |
| List all names | f.list() → String[] | Returns every file and subdirectory name |
| For each name | for (String s1 : s) | Iterate the array |
| Match + validate | m.find() && m.group().equals(s1) | Full filename must match — skip .txt.bak |
| Count | count++ inside the if-block | Track total .txt files |

| # | Application | Key API pattern |
|---|---|---|
| 1 | Validate mobile number | Pattern.compile → matcher(args[0]) → find() + group().equals() |
| 2 | Validate email ID | Same structure, different regex |
| 3 | Extract mobile numbers from file | BufferedReader + while(find()) + PrintWriter |
| 4 | Extract email IDs from file | Same structure, different regex |
| 5 | Filter filenames in directory | File.list() + matcher(name) + find() + group().equals() |

| Purpose | Regex | Java string literal |  |  |
|---|---|---|---|---|
| Indian mobile (10/11/12 digit) | `(0\ | 91)?[789][0-9]{9}` | `"(0 | 91)?[789][0-9]{9}"` |
| Email ID | [a-zA-Z0-9][a-zA-Z0-9_.]+@[a-zA-Z0-9]+(\.[a-zA-Z]+)+ | "[a-zA-Z0-9][a-zA-Z0-9_.]+@[a-zA-Z0-9]+(\\.[a-zA-Z]+)+" |  |  |
| .txt filename | [a-zA-Z0-9_.$]+\.txt | "[a-zA-Z0-9_.$]+\\.txt" |  |  |
| .java filename | [a-zA-Z0-9_.$]+\.java | "[a-zA-Z0-9_.$]+\\.java" |  |  |
| .class filename | [a-zA-Z0-9_.$]+\.class | "[a-zA-Z0-9_.$]+\\.class" |  |  |
| .java or .class | `[a-zA-Z0-9_.$]+\.(java\ | class)` | `"[a-zA-Z0-9_.$]+\\.(java | class)"` |

| Scenario | Loop type | Also need group().equals()? |
|---|---|---|
| Validate entire command-line input | if (m.find()) | Yes — must equal full input |
| Validate entire filename | if (m.find()) | Yes — skip .txt.bak |
| Extract all matches from a line of text | while (m.find()) | No — write each m.group() |
| Search for literal substring in short text | while (m.find()) | No |
