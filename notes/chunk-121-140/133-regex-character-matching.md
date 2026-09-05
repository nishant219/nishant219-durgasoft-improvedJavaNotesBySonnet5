# Video 133 — Regular Expressions Part 2: Character Matching & Quantifiers

## Video info

Title: Core Java With OCJP/SCJP: RegularExpresions Part-2 || character matching

Prerequisite: Video 132 covered Pattern/Matcher basics. This lecture deepens character matching (custom + predefined character classes) and introduces quantifiers (+, *, ?).

### 00:04 — Recap: Pattern and Matcher workflow

Durga Sir briefly reviews Video 132 before new material.

Standard regex program structure:

- Create a Pattern with Pattern.compile(regex).
- Create a Matcher with pattern.matcher(targetString).
- Loop with while (m.find()) and read m.start(), m.end(), m.group().
- m.start() — starting index of the match (inclusive).
- m.end() — ending index (exclusive); value is last matched index + 1.
- m.group() — the substring that matched.
Board recap — search for literal `AB`:

```java
import java.util.regex.*;

class RegexRecapAB {
    public static void main(String[] args) {
        Pattern p = Pattern.compile("AB");
        Matcher m = p.matcher("ABBBBBBBBBBBBBBBBBBBBBBBBBBBBBAB");
        while (m.find()) {
            System.out.println(m.start() + "..." + m.end() + "..." + m.group());
        }
        // prints 0...2...AB
        // prints 29...31...AB
    }
}
```

Terminology reminder: pattern = regex string; target = input searched; each find() call locates the next match left-to-right.

### 02:44 — Custom character classes: `[ABC]` (OR inside brackets)

Requirement: Match A or B or C — any one of them counts as a valid match (not the sequence ABC).

```java
import java.util.regex.*;

class CharClassABC {
    public static void main(String[] args) {
        Pattern p = Pattern.compile("[ABC]");
        Matcher m = p.matcher("ABBBBBBBBBBBBBBBBBBBBBBBBBBBBBAB");
        while (m.find()) {
            System.out.println(m.start() + "..." + m.group());
        }
        // prints many lines — every A and every B is a separate match
    }
}
```

Key point: Characters inside [ ] form a character class — a set of allowed single characters.

### 04:09 — Negation with caret: `[^ABC]`

Requirement: Match any character except A, B, and C.

- ^ inside [ ] at the first position = negation / "except".
- Do not confuse with ^ outside brackets (anchor for start of line — covered later in the series).
Example: in "x3@y", pattern [^ABC] matches x, 3, @, y.

### 05:13 — Range notation in character classes

Ranges use hyphen - between two endpoints inside [ ].

"Special character" in Durga Sir's terminology = anything that is not a letter or digit (e.g. #, @, space in some contexts, punctuation).

Durga Sir's board summary — custom character classes:

All of the above are custom character classes (you define the set explicitly).

### 12:21 — Hands-on demo: custom character classes

Target string (board): "AA3B#K@9J" — covers lowercase/uppercase letters, digits, and special symbols (#, @).

Master demo program (run each regex against the same target):

```java
import java.util.regex.*;

class CustomCharClassDemo {
    static void findAll(String regex, String target) {
        System.out.println("--- regex = "" + regex + "" ---");
        Matcher m = Pattern.compile(regex).matcher(target);
        while (m.find()) {
            System.out.println(m.start() + "..." + m.group());
        }
    }
    public static void main(String[] args) {
        String s = "AA3B#K@9J";
        findAll("[ABC]", s);
        findAll("[^ABC]", s);
        findAll("[a-z]", s);
        findAll("[0-9]", s);
        findAll("[0-9a-zA-Z]", s);
        findAll("[^0-9a-zA-Z]", s);
    }
}
```

Expected output (Durga Sir's board answers):

Note on case: In Java regex, [a-z] matches only lowercase unless Pattern.CASE_INSENSITIVE is used. The board uses A, B, K, J as matched by [a-z] because Durga Sir treats the demo as conceptual; in strict Java, use [a-zA-Z] or (?i)[a-z] for letters regardless of case.

Why skip `m.end()` in print loop: end() returns index after the last matched character (n+1 style). For a single-character match at index i, end() = i + 1. Sir prints start...group for clarity.

### 18:07 — Live run: verify custom class output

Durga Sir runs the same demo in the IDE against target "A3B#K@9J" (slightly shorter variant) and confirms:

- [ABC] → positions 0 (A), 1 is 3 (skip), 2 (B) — two matches.
- [^ABC] → 1 (3), 3 (#), 4 (K), 5 (@), 6 (9), 7 (J).
- [a-z] → A, B, K, J positions.
- [0-9] → 3 and 9.
- [0-9a-zA-Z] → all alphanumerics.
- [^0-9a-zA-Z] → only # and @.
Minimal board program (what students must copy):

```java
import java.util.regex.*;

class RegexCustomClasses {
    public static void main(String[] args) {
        String x = "[ABC]";   // change x for each experiment
        Pattern p = Pattern.compile(x);
        Matcher m = p.matcher("A3B#K@9J");
        while (m.find()) {
            System.out.println(m.start() + "..." + m.group());
        }
    }
}
```

Conclusion (23:08): You must know how to write regex for alphabetic only, digits only, alphanumeric, or special characters — using custom character classes.

### 24:35 — Finding a space character

Requirement: Match the space character specifically.

Two approaches:

For custom-class approach:

```java
import java.util.regex.*;

class SpaceCharDemo {
    public static void main(String[] args) {
        Pattern p = Pattern.compile("[ ]");  // or " "
        Matcher m = p.matcher("hello world");
        while (m.find()) {
            System.out.println(m.start() + "..." + m.group());
        }
        // prints 5...  (space between hello and world)
    }
}
```

### 25:49 — Predefined `\s` vs `\S` (and chat etiquette aside)

`\s` (lowercase) = whitespace character (space, tab, etc.).

`\S` (uppercase) = negation of `\s` = any character except whitespace.

Durga Sir's anecdote: in chat/messaging, an answer in ALL CAPS can signal disinterest or aggression (like forced agreement). Similarly, lowercase \s vs uppercase \S are opposites — a pattern seen throughout Java regex predefined classes (d/D, w/W, s/S).

Critical Java rule: \ is an escape in Java string literals. You must write `"\\s"` so the regex engine receives \s.

String X = "\s";  // CE: illegal escape character at end of line

String X = "\s"; // OK — regex \s

### 27:53 — All predefined character classes

Predefined classes are shorthand — the regex engine already knows them (unlike custom [0-9] ranges you write yourself).

Durga Sir emphasis on `.` (dot/period):

- Matches any single character — alphabet, digit, space, special symbol.
- "Most dangerous" because it is so broad; easy to over-match unintentionally.
`\w` vs alphanumeric: Sir states \w = any word character ≈ alphanumeric. In Java, \w also includes underscore _.

Board list — predefined character classes:

- \s → space/whitespace
- \S → except whitespace
- \d → digit
- \D → except digit
- \w → word/alphanumeric character
- \W → except word character (special chars)
- . → any character
### 32:29 — Hands-on demo: predefined character classes

Target string (board): "A7B K@9Z" — includes letters, digits, space at index 3, and @ special char.

```java
import java.util.regex.*;

class PredefinedClassDemo {
    static void findAll(String regex, String target) {
        System.out.println("--- \"" + regex + "\" ---");
        Matcher m = Pattern.compile(regex).matcher(target);
        while (m.find()) {
            System.out.println(m.start() + "..." + m.group());
        }
    }
    public static void main(String[] args) {
        String s = "A7B K@9Z";
        findAll("\s", s);
        findAll("\S", s);
        findAll("\d", s);
        findAll("\D", s);
        findAll("\w", s);
        findAll("\W", s);
        findAll(".", s);
    }
}
```

Expected matches:

### 33:07 — Java compile error: illegal escape character

Problem: Writing "\s" wrong as "\s" in a Java string.

```java
class BadEscape {
    public static void main(String[] args) {
        String x = "\s";  // CE: illegal escape character
        Pattern p = Pattern.compile(x);
    }
}
```

Why: Java treats \ as escape in string literals (`

, 	,

exist — but \s` is not a valid Java escape).

Fix — double the backslash:

String x = "\s";  // Java string → regex engine sees \s

Rule: Wherever regex needs \, Java source needs \.

```java
class GoodEscape {
    public static void main(String[] args) {
        String x = "\s";
        Pattern p = Pattern.compile(x);
        Matcher m = p.matcher("A7B K@9Z");
        while (m.find()) {
            System.out.println(m.start() + "..." + m.group());
        }
        // prints 3...  (space at index 3)
    }
}
```

Sir also mentions error text "illegal control character" when compiler mis-parses the escape sequence.

### 35:47 — Live IDE demo: predefined classes verified

Durga Sir compiles and runs each pattern against "A7B K@9Z":

- "\s" → index 3 (space) only.
- "\S" → all characters except the space.
- "\d" → 7 at index 1, 9 at index 6.
- "\D" → everything except those two digits.
- "\w" → alphanumeric word chars: A, 7, B, K, 9, Z.
- "\W" → space (index 3) and @ (index 5).
- "." → matches every character (all eight positions).
Board template to memorize:

```java
import java.util.regex.*;

class RegexPredefinedTemplate {
    public static void main(String[] args) {
        String x = "\\s";  // change: \S, \d, \D, \w, \W, .
        Pattern p = Pattern.compile(x);
        Matcher m = p.matcher("A7B K@9Z");
        while (m.find()) {
            System.out.println(m.start() + "..." + m.group());
        }
    }
}
```

### 43:44 — Quantifiers: controlling **how many** times

New terminology — Quantifier: specifies quantity — how many occurrences of the preceding element to match.

Three default quantifier symbols (more in advanced lectures):

Quantifiers apply to the immediately preceding token (single char, class, or group).

Summary table (board):

Difference `a+` vs `a*`:

- a+ requires minimum 1 a.
- a* allows zero a — still a valid match at positions where no a appears.
### 45:07 — Quantifier demo target string

Target string (board): "abaabaab" (length 8, indices 0–7)

Characters at indices 0, 2, 3, 5, 6, 7 are a — six positions for pattern a (exactly one).

Pattern `a` — exactly one a:

```java
import java.util.regex.*;

class QuantifierExactA {
    public static void main(String[] args) {
        Matcher m = Pattern.compile("a").matcher("abaabaab");
        while (m.find()) {
            System.out.println(m.start() + "..." + m.group());
        }
        // prints 0...a
        // prints 2...a
        // prints 3...a
        // prints 5...a
        // prints 6...a
        // prints 7...a
    }
}
```

Six separate matches — each single a counts individually.

### 46:14 — Pattern `a+` (at least one a as one match)

Requirement: Treat a sequence of one or more `a` as a single match (not six separate single-a matches).

```java
import java.util.regex.*;

class QuantifierPlusA {
    public static void main(String[] args) {
        Matcher m = Pattern.compile("a+").matcher("abaabaab");
        while (m.find()) {
            System.out.println(m.start() + "..." + m.group());
        }
        // prints 0...a
        // prints 2...aa
        // prints 5...aaa
    }
}
```

Three matches total:

- Index 0 — one a
- Index 2 — aa (indices 2–3)
- Index 5 — aaa (indices 5–6–7)
+ = at least one; engine consumes the longest consecutive run (greedy).

### 47:30 — Pattern `a*` (zero or more)

Meaning: Any number of a, including zero.

Critical exam point: At a position where the next char is b (not a), a* still matches successfully with zero `a` characters. The match has empty group but valid start index.

```java
import java.util.regex.*;

class QuantifierStarA {
    public static void main(String[] args) {
        Matcher m = Pattern.compile("a*").matcher("abaabaab");
        while (m.find()) {
            System.out.println(m.start() + "..." + m.group());
        }
        // matches at EVERY index including b positions (zero-count match)
        // plus stretches of a's at 0, 2-3, 5-7
        // ALSO index 8 (end+1) — zero count after last char
    }
}
```

Sir's walkthrough on `"abaabaab"`:

- Index 0: one a
- Index 1 (b): zero a's — valid a* match
- Index 2–3: run of a's
- Index 4 (b): zero a's
- Index 5–7: run of a's
- Index 8 (after end of string): zero a's — valid because regex can touch index n+1 (end index + 1 / past last character)
Remember: For a*, "zero count" at non-a positions and at end-of-input is a deliberate behavior — frequent OCJP/SCJP trap.

### 49:01 — Pattern `a?` (at most one)

Meaning: Either zero or one a — not two or more.

```java
import java.util.regex.*;

class QuantifierQuestionA {
    public static void main(String[] args) {
        Matcher m = Pattern.compile("a?").matcher("abaabaab");
        while (m.find()) {
            System.out.println(m.start() + "..." + m.group());
        }
        // index 0: one a
        // index 1 (b): zero a
        // index 2,3: one a each at start of each position scan
        // index 4 (b): zero
        // index 5,6,7: one a each
        // index 8: zero (past end)
    }
}
```

Quick comparison:

### 52:00 — Side-by-side quantifier run on board

Sir re-runs all four against "abaabaab":

Full board program:

```java
import java.util.regex.*;

class QuantifierBoard {
    public static void main(String[] args) {
        String target = "abaabaab";
        String[] patterns = {"a", "a+", "a*", "a?"};
        for (String x : patterns) {
            System.out.println("=== " + x + " ===");
            Matcher m = Pattern.compile(x).matcher(target);
            while (m.find()) {
                System.out.println(m.start() + "..." + m.group());
            }
        }
    }
}
```

Quantifiers definition (exam wording): Quantifiers specify the number of occurrences to match — at least one (+), any including zero (*), or at most one (?).

### 57:04 — Quantifiers are default regex building blocks

Durga Sir writes the same Pattern/Matcher skeleton using target "ababaaBaabaab" variant on board (mixed case in transcript ASR); the pedagogical string for lowercase demos is `"abaabaab"`.

```java
import java.util.regex.*;

class QuantifierTemplate {
    public static void main(String[] args) {
        String x = "a+";  // try: a, a+, a*, a?
        Pattern p = Pattern.compile(x);
        Matcher m = p.matcher("abaabaab");
        while (m.find()) {
            System.out.println(m.start() + "..." + m.group());
        }
    }
}
```

These symbols (+, *, ?) are quantifiers by default in regular expressions.

### 1:00:13 — Lecture wrap-up

Part 2 covered today:

- Custom character classes — [abc], [^abc], ranges [a-z], [0-9], combined alphanumeric and negated special-char patterns.
- Predefined character classes — \s, \S, \d, \D, \w, \W, and . (any char); Java requires \ in source strings.
- Quantifiers — + (≥1), * (≥0), ? (≤1); a* zero-match at non-matching chars and index n+1 after input end.
Next (future videos): More regex applications, anchors, groups, and advanced quantifier forms.

OCJP/SCJP checklist from this video:

- [ ] Write Pattern/Matcher loop from memory
- [ ] Distinguish [ABC] (OR) from ABC (sequence)
- [ ] Use ^ inside [ ] for negation
- [ ] Map custom vs predefined classes ([0-9] ≡ \d)
- [ ] Double backslashes in Java string literals for regex
- [ ] Know . matches any character
- [ ] Explain a+ vs a* vs a? with "abaabaab" example
- [ ] Explain zero-length a* match at b positions and after string end
Java code block count: 18

## Tables (placement lost -- re-place these in context)

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 133 of 203 |
| Series | Core Java With OCJP/SCJP |
| Topic | Regular Expressions — Part 2: Character classes, predefined classes, quantifiers |
| Instructor | Durga Sir |
| Duration | 1h 0m 27s (3627 seconds) |
| Video ID | Wo3wMiDt3a4 |
| Watch | https://www.youtube.com/watch?v=Wo3wMiDt3a4 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | YouTube auto-captions |

| Pattern | Meaning |
|---|---|
| AB | Literal sequence A followed by B |
| [ABC] | Exactly one character that is A, B, or C |

| Pattern | Meaning |
|---|---|
| [ABC] | A or B or C |
| [^ABC] | Any single character other than A, B, C |

| Pattern | Matches |
|---|---|
| [a-z] | Any lowercase letter a–z |
| [A-Z] | Any uppercase letter A–Z |
| [a-zA-Z] | Any letter (both cases) — no space between the two ranges |
| [0-9] | Any digit 0–9 |
| [0-9a-zA-Z] | Any alphanumeric character |
| [^0-9a-zA-Z] | Any non-alphanumeric character (= special character) |

| Syntax | Meaning |
|---|---|
| [ABC] | A or B or C |
| [^ABC] | Except A, B, C |
| [a-z] | Lowercase a–z |
| [A-Z] | Uppercase A–Z |
| [a-zA-Z] | Any alphabetic character |
| [0-9] | Any digit |
| [0-9a-zA-Z] | Any alphanumeric |
| [^0-9a-zA-Z] | Special (non-alphanumeric) characters |

| Index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Char | A | 3 | B | # | K | @ | 9 | J |

| Pattern | Matches (index...char) |
|---|---|
| [ABC] | 0...A, 2...B |
| [^ABC] | 1...3, 3...#, 4...K, 5...@, 6...9, 7...J |
| [a-z] | 0...A, 2...B, 4...K, 7...J |
| [0-9] | 1...3, 6...9 |
| [0-9a-zA-Z] | 0...A, 1...3, 2...B, 4...K, 6...9, 7...J |
| [^0-9a-zA-Z] | 3...#, 5...@ |

| Approach | Pattern | Notes |
|---|---|---|
| Literal space inside class | [ ] | Space directly in brackets |
| Predefined class (next section) | \s in Java source | Whitespace character |

| Pattern (regex) | Meaning |
|---|---|
| \s | Whitespace |
| \S | Non-whitespace (everything except space/tab/etc.) |

| Pattern (regex) | Meaning | Custom equivalent |
|---|---|---|
| \s | Whitespace | [ ] or broader whitespace sets |
| \S | Except whitespace | negation of above |
| \d | Digit 0–9 | [0-9] |
| \D | Non-digit | [^0-9] |
| \w | Word character (alphanumeric + _) | roughly [0-9a-zA-Z_] |
| \W | Non-word character | special characters + space |
| . | Any character (the "most dangerous") | matches letter, digit, space, symbol |

| Index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Char | A | 7 | B | (space) | K | @ | 9 | Z |

| Pattern | Matches |
|---|---|
| \s | 3...  (space only) |
| \S | 0...A, 1...7, 2...B, 4...K, 5...@, 6...9, 7...Z |
| \d | 1...7, 6...9 |
| \D | all except indices 1 and 6 |
| \w | 0...A, 1...7, 2...B, 4...K, 6...9, 7...Z (skips space and @) |
| \W | 3... , 5...@ |
| . | every index 0 through 7 |

| Symbol | Name | Meaning |
|---|---|---|
| (none) | — | Exactly one occurrence |
| + | Plus | At least one (one or more) |
| * | Aster/star | Zero or more (any number including zero) |
| ? | Question mark | At most one (zero or one) |

| Pattern | Meaning |
|---|---|
| a | Exactly one a |
| a+ | At least one a (greedy sequence of a's) |
| a* | Any number of a including zero |
| a? | At most one a |

| Index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Char | a | b | a | a | b | a | a | a |

| At position with b | a+ | a* | a? |
|---|---|---|---|
| Match? | No (needs ≥1 a) | Yes (0 a's) | Yes (0 a's) |

| At position with aaa | a+ | a* | a? |
|---|---|---|---|
| Consumes | all three | all three | only one (at most one) |

| Pattern | # of find() hits (conceptually) | Notes |
|---|---|---|
| a | 6 | each a separately |
| a+ | 3 | grouped sequences |
| a* | many (every index + end) | zero-length matches at b and after end |
| a? | many | zero or one at each position |
