# Video 132

## Video info

Title: Core Java With OCJP/SCJP: RegularExpresions Part-1 || Introduction

### 00:03 — Topic introduction: Regular Expressions

- Next topic in the series: Regular Expressions (ASR: "regular expressions", "regular expression").
- Part 1 = basic introduction: what is a regex, where it is used, first Java demo.
### 00:23 — Informal vs real definition

Student joke answer: "The expression which is regular is called regular expression."

Real definition (board):

If you want to represent a group of strings according to a particular pattern, then we should go for Regular Expression.

- Not one string — a group of strings sharing structure.
- Pattern = rules all members must follow.
### 01:23 — Example 1: Valid mobile numbers

Pattern rules (Indian mobile, as stated in class):

- Exactly 10 digits.
- First digit: 7, 8, or 9.
- Remaining 9 digits: 0–9 (any digit).
All valid mobile numbers follow this pattern → one regex can represent the whole set.

### 02:14 — Example 2: Valid email IDs

- Every email ID follows a pattern (user@domain structure, etc.).
- We can write a regex to represent all valid mail IDs.
Board (decoded ASR *"male ladies"* → mail IDs):

We can write a regular expression to represent all valid mobile numbers.

We can write a regular expression to represent all mail IDs.

Syntax of how to write regex → covered in later sessions (Part 2+).

### 03:19 — Board definition (formal notes)

If you want to represent a group of strings
according to a particular pattern,
then we should go for Regular Expression.

Example 1: regex for all valid mobile numbers.

Example 2: regex for all mail IDs.

### 05:14 — Where can we use Regular Expressions?

Three main application areas (plus two academic extras).

### 05:47 — Application area 1: Form validation / validation frameworks

Real-life scenario — online inquiry/registration form:

Fields: Name, Mobile number, Mail ID, … → Submit.

Student experience Durga Sir narrates:

- Enter name Durga, mobile 9848022338, email durga → submit.
- Error: "Please enter a valid mail ID".
- Change to durga@gmail → still invalid format.
- Enter complete durga@gmail.com → "Request submitted".
- Later tries fake email aaa@bbbccc → accepted by form (format OK) but mail bounces — no such mailbox.
Key insight:

- Form checks format / pattern, not whether mailbox physically exists.
- These validations = validation frameworks built internally on Regular Expressions.
Use cases:

- Pre-check: is given mail ID format-valid?
- Pre-check: is given mobile number format-valid?
- Pattern-wise / format-wise checking → Regular Expressions.
### 09:34 — Application area 2: Pattern matching applications

Anecdote (humor — Ctrl+C / Ctrl+V / Ctrl+F "mantras"):

- Student asks how to become best software engineer.
- Durga Sir's answer: master Copy (Ctrl+C), Paste (Ctrl+V), Find (Ctrl+F) — ~90% of industry work.
- Ctrl+F = search/find in document → classic pattern matching.
Ctrl+F behavior:

- Prompt: "Which thing you want to search?"
- Enter e.g. SCJP → Find / Find All / Next / Previous.
- Shows count (e.g. 23 matches) and locations.
Pattern matching application:

- Given a pattern, check if present in target text.
- If present → how many times? Where (indices)?
Implementation: internally uses Regular Expressions.

### 15:54 — Main purpose summary (two classroom focus areas)

- Develop validation frameworks (form validation).
- Implement pattern matching applications (Find, grep, etc.).
Third area mentioned but out of deep classroom scope: translators.

### 16:17 — Application area 3: Translators (lexical analysis)

Compiler phases (board):

- Lexical analysis (also: tokenization, scanning)
- Syntax analysis (also: parsing)
- Semantic analysis
- Intermediate code generation & optimization
- Target code generation
Lexical analysis internally implemented using Regular Expressions.

Related academic subjects (not Java exam focus):

- Compiler Design / Language Processors (LP)
- Theory of Computation (TOC)
- Automata Theory & Formal Languages (AFL)
Designing a full compiler/assembler = ~6-month academic project — not in this course scope, but lexical phase uses regex.

### 19:11 — Classroom scope vs full list

Will discuss in classroom:

- Form validation
- Pattern matching applications
Additional areas (awareness only, not programmer day-to-day):

### 22:23 — Extra application areas 4 & 5

4. Digital circuits

- Regular expression → can create Finite Automaton (FA).
- Special FA with output → Moore machine, Mealy machine.
- Used in digital circuit design (binary adder, multiplier, etc.).
- Not required for Java programmers.
5. Communication protocols

- TCP/IP, UDP, etc. — protocol design may use regex internally.
- Not in programmer scope for this course.
Board extras:

- To develop digital circuits
- To develop communication protocols (TCP/IP, UDP, etc.)
### 25:49 — Recap before Java program

What is regex? Represent group of strings by pattern.

Where used? Validation, pattern matching, translators (+ digital circuits, protocols academically).

### 26:03 — First Java program: pattern matching demo

Requirement:

- Target string: "abababa" (board: a b a b a b a)
- Pattern to search: "ab"
- Answer needed:
- Is "ab" available? Yes
- How many times? 2
- Where? index 0 and index 3 (0-based)
Expected program output:

0
3
The total number of occurrences is 2

### 28:15 — `RegExDemo` class (board)

```java
import java.util.regex.*;

class RegExDemo {
    public static void main(String[] args) {
        String target = "abababa";
        String patternStr = "ab";

        // Step 1: create Pattern object
        Pattern p = Pattern.compile("ab");

        // Step 2: create Matcher for target
        Matcher m = p.matcher(target);

        int count = 0;
        while (m.find()) {
            System.out.println(m.start());  // start index of each match
            count++;
        }
        System.out.println("The total number of occurrences is " + count);
    }
}
```

Two-step process (board):

Package:

Pattern and Matcher are in `java.util.regex` (sub-package of java.util).

```java
import java.util.regex.*;
```

NOT java.util alone — specifically `java.util.regex`.

### 31:41 — `while (m.find())` loop explained

- `find()` → attempts to locate next match in target.
- Returns `true` if next match exists → enter loop body.
- Returns `false` when no more matches → exit loop.
- For each match, print `m.start()` (start index).
- Increment `count` for total occurrences.
Live run output:

0
3
The total number of occurrences is 2

- Match 1: "ab" at index 0 (a at 0, b at 1).
- Match 2: "ab" at index 3.
### 37:09 — Extended output: start, end, group

Add to loop body:

```java
while (m.find()) {
    System.out.println(
        m.start() + " " + m.end() + " " + m.group());
    count++;
}
```

`end()` behavior (important exam detail):

- Returns `endIndex + 1` of the match (exclusive end index in the API sense).
- First match "ab" at 0–1 → start()=0, end()=2.
- Second match at 3–4 → start()=3, end()=5.
Expected output:

0 2 ab
3 5 ab
The total number of occurrences is 2

`group()` method:

- Returns the matched substring (what actually matched).
- Useful when pattern matches any digit, any letter, mobile number, etc. — you need to know which substring matched.
### 40:48 — Change pattern: different search strings

Search for `"ba"` in "abababa":

- Matches at indices where b followed by a.
- 2 matches (Durga Sir counts on board).
Search for `"bb"`:

- 1 match (only one bb substring in target).
Search for `"bbbb"` (four B's):

- No match → loop never prints indices.
Output:

The total number of occurrences is 0

### 45:36 — Theory: Pattern class

Definition (board):

A Pattern object is a compiled version of regular expression.

It is the Java equivalent object of the regex pattern string.

How to create:

Pattern p = Pattern.compile("ab");
// static method on Pattern class
// argument: String regularExpression

API signature (from screen):

```java
public static Pattern compile(String regularExpression)
```

Example:

Pattern p = Pattern.compile("ab");

### 49:22 — Theory: Matcher class

Definition (board):

A Matcher object can be used to match the pattern in the given target string.

How to create:

Matcher m = p.matcher("abababa");
// instance method on Pattern
// argument: target String
// returns Matcher

API signature (from screen):

```java
public Matcher matcher(String target)
```

Example:

Matcher m = p.matcher("abababa");

### 52:44 — Important methods of Matcher class (board)

Usage pattern:

```java
Pattern p = Pattern.compile("ab");
Matcher m = p.matcher("abababa");
while (m.find()) {
    System.out.println("start=" + m.start()
        + ", end=" + m.end()
        + ", matched=" + m.group());
}
```

### 55:50 — Package and Java version

Board note:

Pattern and Matcher classes
present in java.util.regex package
introduced in Java 1.4 version

- `regex` = regular expression (package name abbreviation).
- Not in Java 1.0 — came in 1.4.
### 57:34 — Session wrap-up; preview Part 2

Completed in Part 1:

- Definition of regular expression
- Application areas (validation, pattern matching, translators + extras)
- `Pattern` / `Matcher` classes
- Demo: find pattern in string, count, indices, group()
- `import java.util.regex.*`
Next session (Part 2) will cover:

- Instead of literal "ab", match any digit, any alphabet, mobile number pattern, etc.
- Regex syntax/meta-characters — what to write inside Pattern.compile(...).
Assignment-style closing:

Can you write a simple pattern matching application using regular expressions? Target/pattern may change; process stays the same.

## Complete demo (consolidated for notes)

```java
import java.util.regex.*;

class RegExDemo {
    public static void main(String[] args) {
        String target = "abababa";
        Pattern p = Pattern.compile("ab");
        Matcher m = p.matcher(target);

        int count = 0;
        while (m.find()) {
            System.out.println(
                m.start() + " " + m.end() + " " + m.group());
            count++;
        }
        System.out.println("The total number of occurrences is " + count);
    }
}
```

Print:

0 2 ab
3 5 ab
The total number of occurrences is 2

## Application areas summary table

## Key API cheat sheet

```java
import java.util.regex.*;          // Java 1.4+

Pattern p = Pattern.compile(regex); // compiled regex
Matcher m = p.matcher(target);      // bind to target string

m.find();    // boolean — next match?
m.start();   // int — start index
m.end();     // int — end+1 index
m.group();   // String — matched text
```

Java code block count: 12

## Tables (placement lost -- re-place these in context)

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP |
| Position | 132 of 203 |
| Series | Core Java With OCJP/SCJP |
| Topic | Regular Expressions — Part 1: Introduction |
| Instructor | Durga Sir |
| Duration | 58m 18s |
| Video ID | vftR8LilgMw |
| Watch | https://www.youtube.com/watch?v=vftR8LilgMw |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

| Platform | Pattern matching tool |
|---|---|
| Windows | Ctrl+F (Find) |
| Unix/Linux | `grep` command (also egrep, fgrep, variations) |

| Step | Action | API |
|---|---|---|
| 1 | Create Pattern object for regex | Pattern.compile("ab") |
| 2 | Create Matcher on target string | p.matcher(target) |

| Method | Return | Purpose |
|---|---|---|
| `find()` | boolean | Attempts to find next match; returns true if available, else false |
| `start()` | int | Returns start index of the current match |
| `end()` | int | Returns `end + 1` index of the match (exclusive end position) |
| `group()` | String | Returns the matched pattern / matched substring |

| # | Area | Examples | Classroom focus |
|---|---|---|---|
| 1 | Validation frameworks | Email/mobile format check on forms | Yes |
| 2 | Pattern matching | Ctrl+F (Windows), grep (Unix) | Yes |
| 3 | Translators | Lexical analysis in compilers | Mentioned |
| 4 | Digital circuits | Moore/Mealy machines | Awareness only |
| 5 | Communication protocols | TCP/IP, UDP design | Awareness only |
