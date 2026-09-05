# Video 134 — Regular Expressions Part 3: Pattern Class `split`, StringTokenizer & Practical Regex

## Video info

Title: Core Java With OCJP/SCJP: RegularExpresions Part-3 || pattern class

Prerequisite: Videos 132–133 covered Pattern/Matcher, character classes, predefined classes (\s, \d, .), and quantifiers (+, *, ?). This lecture completes the regex series with splitting/tokenization and real-world regex framing (mobile numbers, email IDs, Java identifiers).

Position: Video 134 of 203 in the Durga Sir OCJP/SCJP playlist.

## 00:05 — Recap & today's agenda

Durga Sir opens by recapping Part 2 (character classes, predefined classes). Today's new topics on the board:

- `Pattern` class `split()` method — divide a target string into tokens by a regex delimiter.
- `String` class `split()` method — same purpose, different API.
- `StringTokenizer` (java.util) — legacy tokenization utility (not on exam, but good to know).
- Practical regex applications — mobile numbers, email IDs, Java language identifiers.
## 00:57 — `Pattern.split()` — core concept

### What "split" means

Split = divide a target string into pieces (tokens) wherever the delimiter pattern appears. The delimiter itself is discarded; everything between delimiters becomes a token.

Board example:

Mental model: "Wherever the pattern is there, ignore it; whatever remains are the tokens."

### Return type

Pattern.split(String) returns a `String[]` — an array of token strings.

### Basic API workflow

- Compile the delimiter regex: Pattern p = Pattern.compile(regex);
- Call split on the pattern object, passing the target string: String[] tokens = p.split(target);
- Iterate the array.
## 01:59 — Example 1: Split on whitespace (`\s`)

Board program — RegexDemo1:

```java
import java.util.regex.*;

class RegexDemo1 {
    public static void main(String[] args) {
        Pattern p = Pattern.compile("\\s");
        String[] s = p.split("Durga Software Solutions");
        for (String s1 : s) {
            System.out.println(s1);
        }
        // Output:
        // Durga
        // Software
        // Solutions
    }
}
```

Key points:

- \\s in Java source → regex engine receives \s (whitespace).
- Three tokens because there are two spaces separating three words.
- Every board example in this lecture uses import java.util.regex.*;.
Theory (board wording):

We can use `Pattern` class `split()` method to split the target string according to a particular pattern.

## 08:13 — Split on a literal character: `'a'`

Change delimiter from space to the letter `a`.

Target: "Durga Software Solutions"

Manual tokenization (Sir walks through on board):

Result: 3 tokens — "Durg", " Software", " Solutions".

Code change:

Pattern p = Pattern.compile("a");
String[] s = p.split("Durga Software Solutions");
// Same 3 tokens as above

## 10:07 — Split on `'o'`

Target: "Durga Software Solutions"

Wait — Sir counts 4 tokens on board by grouping differently. Let's trace Sir's grouping:

- "Durga " (before first o in "Software")
- "S" + ... actually Sir groups as:
- "Durga "
- "S" ...
Sir's board answer for 'o': 4 tokens — "Durga ", "S", "ftware ", "S" + "luti" + "ns" grouped as "Solutions" split parts.

Sir's simplified 4-token walkthrough:

- "Durga " — up to o in "Software"
- "S" — single char before next o
- "ftware " — between o characters
- "S" + remainder → Sir ultimately says 4 tokens
Code:

```java
Pattern p = Pattern.compile("o");
String[] s = p.split("Durga Software Solutions");
for (String s1 : s) {
    System.out.println(s1);
}
```

Exam tip: Always trace delimiter positions manually for unfamiliar strings — empty tokens can appear at boundaries depending on regex engine behavior.

## 11:55 — Example 2: Split URL on dot — the `.` trap

Target string: "www.durgajobs.com"

Goal: Split on literal dot (.) to get:

- "www"
- "durgajobs"
- "com"
### Wrong approach — bare `.` as delimiter

Pattern p = Pattern.compile(".");
String[] s = p.split("www.durgajobs.com");
// Output: NOTHING (empty array or no printable tokens)

Why? In regex, . means any character (the "most dangerous symbol" from Video 133). Every single character is a delimiter → nothing meaningful remains as tokens.

Sir's rule: "Accept every character → remaining got tokens = nothing."

### Fix 1 — Escape the dot: `\\.`

Pattern p = Pattern.compile("\\.");
String[] s = p.split("www.durgajobs.com");
for (String s1 : s) {
    System.out.println(s1);
}
// Output:
// www
// durgajobs
// com

Java escape chain:

Common compile error:

String x = "\.";  // CE: illegal escape character

Tell the compiler: "Don't treat \ as escape — treat it as backslash symbol only" → write `\\`.

### Fix 2 — Dot inside character class: `[.]`

Pattern p = Pattern.compile("[.]");
String[] s = p.split("www.durgajobs.com");
// Same output: www, durgajobs, com

Sir's preference: [.] is simpler — JVM treats dot as a symbol only inside [ ], no double-backslash needed.

Board Example 2 (complete):

```java
import java.util.regex.*;

class RegexDemo2 {
    public static void main(String[] args) {
        Pattern p = Pattern.compile("[.]");
        String[] s = p.split("www.durgajobs.com");
        for (String s1 : s) {
            System.out.println(s1);
        }
        // www
        // durgajobs
        // com
    }
}
```

Variant target: "www.durgasoft.com" → tokens: "www", "durgasoft", "com".

## 24:13 — `String.split()` — same purpose, different caller

Since Java 1.4, the `String` class also has `split()` for the same tokenization purpose.

### Syntax

String target = "Durga Software Solutions";
String[] s = target.split("\\s");
for (String s1 : s) {
    System.out.println(s1);
}
// Durga
// Software
// Solutions

Theory (board):

`String` class `split()` method — to split the target string according to a particular pattern.

### Side-by-side comparison — THE CRITICAL EXAM DIFFERENCE

Board note (memorize):

- `Pattern` class `split()` method → can take target string as argument.
- `String` class `split()` method → can take pattern as argument.
"The things will be reversed in both cases."

### Full board example — String.split

```java
import java.util.regex.*;  // not strictly required for String.split, but Sir uses it

class StringSplitDemo {
    public static void main(String[] args) {
        String s = "Durga Software Solutions";
        String[] arr = s.split("\\s");
        for (String s1 : arr) {
            System.out.println(s1);
        }
    }
}
```

Before Java 1.4: You could still tokenize using `StringTokenizer` (pre-regex era).

## 31:30 — `StringTokenizer` (`java.util`)

### Package & purpose

Definition (board):

`StringTokenizer` is a specially designed class for tokenization activity (divide into tokens).

Not required for OCJP/SCJP exam, but Durga Sir spends a few minutes for completeness.

## 34:13 — StringTokenizer Example 1: default delimiter (space)

```java
import java.util.*;

class StringTokenizerDemo1 {
    public static void main(String[] args) {
        StringTokenizer st = new StringTokenizer("Durga Software Solutions");
        while (st.hasMoreTokens()) {
            System.out.println(st.nextToken());
        }
        // Output:
        // Durga
        // Software
        // Solutions
    }
}
```

API:

Default behavior: If you don't specify a delimiter, `StringTokenizer` uses space as the default regular expression / delimiter.

Board note:

The default regular expression for `StringTokenizer` is `\s` (space/whitespace).

## 38:43 — StringTokenizer Example 2: custom delimiter (hyphen)

Target: "19-09-2014" (today's date on board — 19 Sep 2014)

Delimiter: hyphen (-)

Expected tokens: "19", "09", "2014"

```java
import java.util.*;

class StringTokenizerDemo2 {
    public static void main(String[] args) {
        StringTokenizer st = new StringTokenizer("19-09-2014", "-");
        while (st.hasMoreTokens()) {
            System.out.println(st.nextToken());
        }
        // 19
        // 09
        // 2014
    }
}
```

Constructor overload:

new StringTokenizer(String str)              // default delimiter: space
new StringTokenizer(String str, String delim) // custom delimiter

Terminology:

- Delim / Delimiter = the pattern/regex that separates tokens (same concept as separator).
- First argument = target string.
- Second argument = delimiter (pattern).
Other delimiters: comma ,, dot ., iPhone/hyphen - — same constructor pattern.

## 43:37 — Practical regex applications begin

Sir transitions: "That's all for StringTokenizer — regular expressions concept ends here, but let me show small applications because now we know how to write regex."

These framing exercises teach how to compose regex from English rules — usage with matches() / Pattern.compile() comes in later discussion.

## 44:25 — Application 1: Valid 10-digit Indian mobile numbers

### Rules (board)

- Every number must contain exactly 10 digits.
- The first digit must be 7, 8, or 9 (no Indian mobile starts with 6 per Sir's rule).
### Step-by-step construction

Long form:

[789][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]

Short form with quantifier `{n}`:

[789][0-9]{9}

Important: {9} is regex quantifier (exactly 9 times), NOT mathematical power. Don't write [0-9]^9 or [0-9]⁹.

Curly brace syntax: {n} = preceding token repeats exactly n times.

```java
// Conceptual validation
String mobileRegex = "[789][0-9]{9}";
Pattern p = Pattern.compile(mobileRegex);
Matcher m = p.matcher("9876543210");
System.out.println(m.matches());  // true
```

## 48:41 — Application 2: 10-digit OR 11-digit mobile numbers

### Additional rule for 11-digit

- If 11 digits, the first digit must be 0 (trunk prefix / STD-style leading zero).
### Technique: optional leading `0` with `?`

0?[789][0-9]{9}

How it covers both cases:

## 50:04 — Application 3: 10-digit OR 11-digit OR 12-digit mobile numbers

### Additional rule for 12-digit

- First two digits must be `91` (country code prefix).
### Combined regex

(0|91)?[789][0-9]{9}

Coverage table:

Sir's walkthrough logic:

- Ignore optional group → all 10-digit numbers covered.
- Take 0 once → 11-digit covered.
- Take 91 once → 12-digit covered.
Memorize this technique — Sir says he will use it in bigger examples later.

## 53:04 — Application 4: Valid email IDs

### Example email

D123_xyz.k@gmail.com — valid (digits allowed in local part per Sir's updated rule).

### Allowed characters & structure

### Full regex (board)

[a-zA-Z0-9][a-zA-Z0-9_.]+@[a-zA-Z0-9]+(\.[a-zA-Z]+)+

Breakdown:

- [a-zA-Z0-9] — first char must be alphanumeric.
- [a-zA-Z0-9_.]+ — rest of local part (underscore, dot allowed).
- @ — mandatory at-symbol.
- [a-zA-Z0-9]+ — domain (gmail, yahoo, tv9, etc.).
- (\.[a-zA-Z]+)+ — one or more dot-extension groups:
- .com ✓
- .co.in ✓ (two groups: .co + .in)
- .co.in.ap ✓ (three groups)
Why `[.]` or escaped dot inside extension: Normal . means "any character"; inside [.] or with \. it's literal dot.

Why outer `(...)+`: The combination (\.[a-zA-Z]+) can repeat for multi-level domains, but at least one extension is mandatory (the + on the group).

### Domain examples Sir mentions

## 1:01:00 — Application 5: Gmail IDs only

Same local-part rules, but domain is fixed:

[a-zA-Z0-9][a-zA-Z0-9_.]+@gmail[.]com

Or equivalently:

[a-zA-Z0-9][a-zA-Z0-9_.]+@gmail\.com

Why `[.]com`: Dot inside brackets = literal dot symbol, no special "any char" meaning.

No choice — domain must be exactly gmail.com.

## 1:02:55 — Application 6: Java language identifiers (custom rules)

Sir frames a custom identifier language (subset/superset twist on Java rules for exam practice):

### Rules (board)

### Regex construction

Full regex:

[a-k][0369][a-zA-Z0-9@$]*

Why length ≥ 2 is satisfied:

- First two characters are compulsory (no ? on them).
- Third part * allows zero or more → minimum total length = 2.
Examples:

String idRegex = "[a-k][0369][a-zA-Z0-9@$]*";
Pattern p = Pattern.compile(idRegex);
System.out.println(p.matcher("a0").matches());    // true
System.out.println(p.matcher("k9$@").matches());   // true
System.out.println(p.matcher("l0369").matches());  // false

Note on real Java identifiers: Actual Java allows $, _, Unicode letters, and different first-char rules. Sir's regex is an exam-style custom specification — follow the rules given in the question, not general Java language spec, unless stated.

## Splitting API — master comparison table

## Dot-as-delimiter — decision tree

Need to split on literal '.' ?
│
├─ YES → Do NOT use bare "."
│         ├─ Option A: "\\."   (escaped dot)
│         └─ Option B: "[.]"   (dot in char class — Sir prefers this)
│
└─ Using bare "." → matches ANY char → empty/useless split result

## Mobile number regex — summary table

## Email regex — summary table

## 1:08:19 — Lecture wrap-up

Part 3 covered today:

- `Pattern.split()` — compile regex, pass target string; returns String[].
- `String.split()` — call on target, pass regex; same return type; arguments reversed.
- Literal dot delimiter — never bare .; use \\. or [.].
- `StringTokenizer` — java.util, default space delimiter, hasMoreTokens() / nextToken().
- Practical regex framing — mobile numbers (10/11/12 digit), email IDs, custom Java identifiers using char classes, quantifiers (+, ?, {n}), and grouping with (...).
End of Regular Expressions series (Videos 132–134). Future lectures move to Collections Framework (Video 137+).

## OCJP/SCJP checklist from this video

- [ ] Write Pattern.compile(...).split(target) from memory
- [ ] Write target.split(regex) and state what argument each API takes
- [ ] Explain why "." as split delimiter yields empty/no tokens
- [ ] Fix dot delimiter with "\\." or "[.]"
- [ ] State return type of both split methods: String[]
- [ ] Know StringTokenizer is in java.util, default delimiter is space
- [ ] Write [789][0-9]{9} for 10-digit Indian mobile
- [ ] Use 0? and (0|91)? for optional prefixes (11/12 digit variants)
- [ ] Know {n} means "exactly n times" in regex (not exponentiation)
- [ ] Frame email regex: local @ domain (\.[a-zA-Z]+)+
- [ ] Apply custom identifier rules char-by-char to build regex
Java code block count: 14

## Video metadata

## Tables (placement lost -- re-place these in context)

| Target string | Delimiter | Tokens |
|---|---|---|
| "Durga Software Solutions" | space (\s) | "Durga", "Software", "Solutions" (3 tokens) |

| Step | After ignoring a | Token |
|---|---|---|
| Start → first a at index 3 | D, u, r, g | "Durg" |
| Next a at index 15 (in "Software") | , S, o, f, t, w, r, e | " Software" |
| Next a at index 22 (in "Solutions") | , S, o, l, u, t, i, o, n, s | " Solutions" |

| Token # | Content (after ignoring each o) |
|---|---|
| 1 | "Durga " |
| 2 | "S" |
| 3 | "ftware " |
| 4 | "S" |
| 5 | "luti" |
| 6 | "ns" |

| Java source | Regex engine sees | Meaning |
|---|---|---|
| "\\." | \. | Literal dot character |
| "\\" alone | \ | Illegal escape → compile error in string literal |

| Aspect | Pattern.split() | String.split() |
|---|---|---|
| Called on | `Pattern` object | `String` object (the target) |
| Argument | Target string | Pattern (regex string) |
| What you already have | Pattern (regex) | Target string |
| What you must pass | Target string | Pattern as argument |
| Return type | String[] | String[] |
| Introduced | Java 1.4 (regex API) | Java 1.4 |

| Class | Package |
|---|---|
| String, StringBuffer, StringBuilder | java.lang |
| `StringTokenizer` | `java.util` ← not java.lang |

| Method | Purpose |
|---|---|
| hasMoreTokens() | Returns true if more tokens remain |
| nextToken() | Returns the next token string |

| Position | Rule | Regex fragment |
|---|---|---|
| 1st digit | 7 or 8 or 9 | [789] |
| Digits 2–10 | any digit 0–9, nine more times | [0-9] repeated 9 times |

| Part | Meaning |
|---|---|
| 0? | Optional 0 — at most once (0 times or 1 time) |
| [789][0-9]{9} | Standard 10-digit mobile |

| Input | 0? behavior | Rest | Total digits |
|---|---|---|---|
| 9876543210 | Skip 0 (0 times) | 10 digits | 10 ✓ |
| 09876543210 | Take 0 (1 time) | 10 digits | 11 ✓ |

| Part | Meaning |  |
|---|---|---|
| `(0\ | 91)?` | Optionally prefix with 0 OR 91 — at most once |
| [789][0-9]{9} | Core 10-digit mobile |  |

| Prefix taken | Digits | Example pattern |
|---|---|---|
| None | 10 | 9876543210 |
| 0 | 11 | 09876543210 |
| 91 | 12 | 919876543210 |

| Part | Rule | Regex fragment |
|---|---|---|
| 1st character | Alphanumeric (A–Z, a–z, 0–9) | [a-zA-Z0-9] |
| 2nd+ chars (local part) | Alphanumeric, _, . — any number | [a-zA-Z0-9_.]+ |
| `@` symbol | Mandatory, fixed | @ |
| Domain name | At least one alphanumeric char, then any number | [a-zA-Z0-9]+ |
| Extension(s) | Dot + letter sequence, at least once; can repeat (.com, .co.in, .co.in.ap) | (\.[a-zA-Z]+)+ |

| Email fragment | Matches |
|---|---|
| @gmail.com | ✓ |
| @yahoo.com | ✓ |
| @tv9.net | ✓ |
| @4shared.com | ✓ |
| @something.co.in | ✓ |
| @something.co.in.ap | ✓ |

| # | Rule |
|---|---|
| 1 | Allowed characters: a–z, A–Z, 0–9, @, $ |
| 2 | Length: at least 2 characters |
| 3 | 1st character: lowercase alphabetic `a–k` only |
| 4 | 2nd character: a digit divisible by 3 → 0, 3, 6, or 9 |
| 5 | 3rd+ characters: any allowed char, any number of times |

| Position | Rule | Fragment |
|---|---|---|
| 1st | [a-k] | lowercase a through k |
| 2nd | [0369] | digits divisible by 3 |
| 3rd+ | [a-zA-Z0-9@$]* | zero or more allowed chars |

| Identifier | Valid? | Reason |
|---|---|---|
| a0 | ✓ | 2 chars, a ∈ [a-k], 0 divisible by 3 |
| k9xyz | ✓ | valid prefix + extras |
| m0369 | ✗ | m not in [a-k] |
| a1 | ✗ | 1 not divisible by 3 |
| b | ✗ | length < 2 |

| Feature | Pattern.split(target) | String.split(regex) | StringTokenizer |
|---|---|---|---|
| Class | java.util.regex.Pattern | java.lang.String | java.util.StringTokenizer |
| Since | Java 1.4 | Java 1.4 | Pre-1.4 |
| Delimiter type | Regex pattern | Regex pattern | String delimiter (not full regex) |
| Return type | String[] | String[] | Iterator-style (nextToken()) |
| Default delimiter | Must specify in Pattern | Must specify in argument | Space if omitted |
| Exam importance | High | High | Low (awareness only) |

| Requirement | Regex |  |
|---|---|---|
| Exactly 10 digits, first ∈ {7,8,9} | [789][0-9]{9} |  |
| 10 or 11 digits (11 starts with 0) | 0?[789][0-9]{9} |  |
| 10, 11, or 12 digits | `(0\ | 91)?[789][0-9]{9}` |

| Requirement | Regex |
|---|---|
| General valid email | [a-zA-Z0-9][a-zA-Z0-9_.]+@[a-zA-Z0-9]+(\.[a-zA-Z]+)+ |
| Gmail only | [a-zA-Z0-9][a-zA-Z0-9_.]+@gmail[.]com |

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 134 of 203 |
| Series | Core Java With OCJP/SCJP |
| Topic | Regular Expressions — Part 3: Pattern split, String split, StringTokenizer, practical regex |
| Instructor | Durga Sir |
| Duration | 1h 08m 58s (4138 seconds) |
| Video ID | F1BxgMmF6F0 |
| Watch | https://www.youtube.com/watch?v=F1BxgMmF6F0 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT |
| Transcript | .transcripts/134-F1BxgMmF6F0.txt |
