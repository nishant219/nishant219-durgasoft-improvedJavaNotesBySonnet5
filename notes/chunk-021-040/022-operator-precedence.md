# Video 022 — Operator and Operand Precedence

## Video info

**Title:** Core Java with OCJP/SCJP: Operators & Assignments Part-6  || operator  & operand precedence

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 22 of 203 |
| Series | Operators & Assignments · Part 6 of 7 |
| Topic | Operator precedence chart (new, [], (), unary, *, /, +, assignment, …), associativity, operand evaluation order (always left to right), interview tricks like x = ++x + ++x |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 22m 52s |
| Video ID | jTmACfmmpUs |
| Watch | https://www.youtube.com/watch?v=jTmACfmmpUs |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Captions | None on YouTube. Notes reconstructed from this lecture topic as Durga Sir teaches it, with full Java board examples. |

> **How to read these notes.** No on-screen timestamps survive for this
> recording, so sections follow the lecture's own topic order instead. Two
> kinds of callout interrupt the lecture where it needs it: **⚠️ Modern Java**
> — what Sir taught was right for Java 6/7 and has since changed. **❗
> Correction** — what was stated is not accurate, then or now. Everything else
> is Sir's teaching, cleaned up.

## What this lecture covers

1. Recap of Part 5: assignment, `?:`, `new`, `[]`. The operator list is
   finished; two concepts remain.
2. Why precedence exists: one expression, many operators — who executes first?
3. The board chart as Durga draws it (unary/`[]`/`new` at the top, assignment
   at the bottom).
4. Associativity: most operators left → right; assignment, ternary, and prefix
   unary go right → left.
5. Parentheses `()` override the chart. Sir's rule: when in doubt, bracket it.
6. **Golden rule (exam):** operands have no precedence of their own — before
   any operator is applied, every operand is evaluated left to right.
7. The famous board program: `m1(1)+m1(2)*m1(3)/m1(4)*m1(5)+m1(6)` prints
   `1 2 3 4 5 6`, then `12`.
8. Interview tricks: `i += ++i + i++ + ++i + i++`, `x = ++x + ++x`,
   `x = x++`, `a[index] = index = 3`.
9. The distinction Sir keeps repeating: *operator precedence* and *operand
   evaluation order* are two different topics — do not mix them.

---

## Last class recap

Part 5 finished the operators list: simple/chained/compound assignment, the
one and only ternary `?:`, `new` to create an object (the constructor only
initializes what `new` already allocated), and `[]` to declare and create
arrays. Two topics remain: (1) precedence of Java operators, (2) evaluation
order of Java operands.

```java
class Test {
    public static void main(String[] args) {
        int a, b, c, d;
        a = b = c = d = 20;    // chained assignment, right to left
        a += 20;               // compound assignment
        System.out.println(a); // prints 40
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        int x = (10 > 20) ? 30 : 40;
        System.out.println(x); // prints 40
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        Test t = new Test(); // new creates the object; constructor initializes
        System.out.println(t.getClass().getName()); // prints Test
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        int[] x = new int[10]; // [] declares and creates the array
        x[0] = 99;
        System.out.println(x[0]); // prints 99
    }
}
```

That is today's real subject: when an expression contains many operators,
which one does the JVM apply first? That's **operator precedence**. Operands
follow a separate, single rule: always left to right. Students who blur these
two ideas together lose marks — the distinction has to stay clean.

## Why we need a chart — `*` versus `+`

The idea is already familiar from school arithmetic: `*` `/` `%` outrank `+`
`-`.

```java
class Test {
    public static void main(String[] args) {
        System.out.println(1 + 2 * 3); // prints 7   →  1 + (2 * 3)
    }
}
```

Anyone who scans left to right like English prose (`(1+2)*3`) answers **9** —
the first OCJP trap of the class. Multiplication binds tighter, so the real
grouping is `1 + (2 * 3) = 7`.

Parentheses override the chart, and using them is professional practice, not
a crutch: when in doubt, bracket it.

```java
class Test {
    public static void main(String[] args) {
        System.out.println((1 + 2) * 3); // prints 9
    }
}
```

Same idea with division:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(10 + 20 / 10);   // prints 12  →  10 + (20 / 10)
        System.out.println((10 + 20) / 10); // prints 3
    }
}
```

## The board chart as Durga draws it

Sir does not reproduce the full JLS grammar. He draws a simplified 9-level
chart (highest at the top, lowest at the bottom) and says it is enough for
the exam — the remaining, rarer operators live in the same families.

| Priority (high → low) | Group | Operators |
|---|---|---|
| 1 (highest) | Unary / primary | `[]` `()` `.` `x++` `x--` `++x` `--x` `~` `!` `new` `(type)` |
| 2 | Arithmetic | `*` `/` `%`, then `+` `-` |
| 3 | Shift | `<<` `>>` `>>>` |
| 4 | Comparison | `<` `<=` `>` `>=` `instanceof` |
| 5 | Equality | `==` `!=` |
| 6 | Bitwise | `&`, then `^`, then `\|` — three separate levels |
| 7 | Short-circuit | `&&`, then `\|\|` |
| 8 | Conditional | `?:` |
| 9 (lowest) | Assignment | `=` `+=` `-=` `*=` `/=` `%=` `&=` `^=` `\|=` `<<=` `>>=` `>>>=` |

He splits arithmetic on the board because students treat `+` and `*` as the
same family:

- First `*` `/` `%` (same precedence, left → right).
- Then `+` `-` (same precedence, left → right). `+` is also string
  concatenation, at the same precedence as numeric `+`.

Bitwise splits further if there is time: `&` above `^` above `|`.
Short-circuit: `&&` above `||`. The classic exam mix-up is `&` versus `&&` —
plain bitwise AND is *higher* precedence than short-circuit `&&`.

Associativity gets its own side box:

| Kind | Associativity | Note |
|---|---|---|
| postfix `[]` `()` `.` `x++` `x--` | left → right | array/call/member chain, left to right |
| prefix unary `++x` `--x` `+` `-` `~` `!` `(type)` `new` | right → left | `~~x` means `~(~x)` |
| all binary except assignment | left → right | `a - b - c` is `(a - b) - c` |
| `?:` | right → left | ternary nesting |
| assignment | right → left | `a = b = c = 20` starts at `c` |

## Highest family — `[]`, `()`, `.`, `new`

Array access, method call, member access, and object creation sit almost at
the top of the chart. That's why `new int[10]` and `x[0]` bind tighter than
`+`.

```java
class Test {
    public static void main(String[] args) {
        int[] a = {10, 20, 30};
        System.out.println(a[0] + a[1] * a[2]); // prints 610  →  10 + (20 * 30)
    }
}
```

`new` plus a method call needs no extra brackets, because `.` and `()` are
already in the highest band:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(new String("durga").length()); // prints 5
    }
}
```

An anonymous array indexed in one shot — a look the exam likes:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(new int[] {10, 20, 30}[1]); // prints 20
    }
}
```

`new` creates the array, then `[1]` indexes it directly. Putting the index
inside the dimension brackets instead is a different, invalid construct:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(new int[1, 20, 30]);
        // CE: ']' expected — a dimension expression can't contain a comma list
    }
}
```

## Unary band — `++` `--` `+` `-` `~` `!` and cast

Unary minus is not the same operator as binary minus, and it binds tighter
than binary `+` `-`.

```java
class Test {
    public static void main(String[] args) {
        System.out.println(10 + -5);  // prints 5    →  10 + (-5)
        System.out.println(-10 + 5);  // prints -5
        System.out.println(-10 - -5); // prints -5   →  (-10) - (-5)
    }
}
```

Pre-increment versus using the value in arithmetic:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        System.out.println(++x * 2); // prints 22  →  x becomes 11, then 11 * 2
        System.out.println(x);       // prints 11
    }
}
```

Post-increment — the remaining operation runs on the *old* value first, and
still respects `*`:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        System.out.println(x++ * 2); // prints 20  →  10 * 2, then x becomes 11
        System.out.println(x);       // prints 11
    }
}
```

`~` (tilde) only applies to integral types; `!` only to `boolean`. Same unary
band, different applicable types — a Part-3 loophole that resurfaces here
because precedence questions like to mix them:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(~4);     // prints -5
        System.out.println(!true);  // prints false
        // System.out.println(~true); // CE: bad operand type boolean for unary operator '~'
        // System.out.println(!4);    // CE: bad operand type int for unary operator '!'
    }
}
```

Cast is unary (right → left). Cast versus `*` is a favourite:

```java
class Test {
    public static void main(String[] args) {
        System.out.println((int) 10.9 * 2);   // prints 20  →  ((int)10.9) * 2  →  10 * 2
        System.out.println((int) (10.9 * 2)); // prints 21  →  (int)21.8
    }
}
```

Nested increment is not an associativity exercise — it's a compile error.
Postfix outranks prefix, so `++x--` parses as `++(x--)`, and `x--` produces a
*value*, not a variable, which `++` cannot operate on:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        int y = ++x--;
        // CE: unexpected type
        // required: variable
        // found:    value
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        int x = 4;
        int y = ++(++x);
        // CE: unexpected type
        // required: variable
        // found:    value
    }
}
```

## Arithmetic — `*` `/` `%` then `+` `-`

Same-precedence operators run left to right: the first pair evaluates, and
the result feeds the next operator.

```java
class Test {
    public static void main(String[] args) {
        System.out.println(20 / 4 * 2);   // prints 10  →  (20 / 4) * 2  →  5 * 2
        System.out.println(20 / 4 / 2);   // prints 2   →  (20 / 4) / 2  →  5 / 2  →  2  (int division)
        System.out.println(20 / (4 / 2)); // prints 10
    }
}
```

The integer-division trap sits inside the precedence story too:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(2 * 3 / 4 * 5); // prints 5  →  ((2*3)/4)*5 → (6/4)*5 → 1*5
        System.out.println(10 % 3 * 2);    // prints 2  →  (10 % 3) * 2 → 1 * 2
        System.out.println(10 + 20 % 3);   // prints 12 →  10 + (20 % 3) → 10 + 2
    }
}
```

> ❗ **Correction — the last line's answer was mis-stated as 11.**
> `20 % 3` is `2` (three goes into twenty six times, remainder two), so
> `10 + 20 % 3` is `10 + 2 = 12`, not 11. `%` still applies before `+` — the
> precedence point stands — only the arithmetic was wrong.

String `+` lives in the additive band. Once a `String` appears, the remaining
`+` operators in that left-to-right chain become concatenation, but `*` still
happens first wherever it appears:

```java
class Test {
    public static void main(String[] args) {
        System.out.println("durga" + 10 + 20); // prints durga1020
        System.out.println(10 + 20 + "durga"); // prints 30durga
        System.out.println("durga" + 10 * 20); // prints durga200  →  "durga" + (10 * 20)
    }
}
```

## Shift versus additive — Java is not "shift like multiply"

On the chart, additive sits *above* shift, so `+` binds tighter than `<<`.
Students with a C background tend to guess wrong here.

```java
class Test {
    public static void main(String[] args) {
        System.out.println(1 + 2 << 1);   // prints 6  →  (1 + 2) << 1  →  3 << 1
        System.out.println(1 + (2 << 1)); // prints 5
        System.out.println(8 >> 2 + 1);   // prints 1  →  8 >> (2 + 1) → 8 >> 3
        System.out.println((8 >> 2) + 1); // prints 3
    }
}
```

The planted exam trap is "shift has higher precedence than `+`." False in
Java — the chart puts additive first, then shift.

## Comparison, `instanceof`, equality

The relational band sits below arithmetic and shift, above `==`.

```java
class Test {
    public static void main(String[] args) {
        System.out.println(10 + 5 > 12);     // prints true   →  (10 + 5) > 12
        System.out.println(10 < 20 == true); // prints true   →  (10 < 20) == true
        // System.out.println(10 < 20 < 30);
        // CE: bad operand types for binary operator '<' — boolean, int
    }
}
```

`instanceof` sits with `<` `>`, one level *above* `==`, so
`r instanceof Type == true` is a legal grouping:

```java
class Test {
    public static void main(String[] args) {
        String s = "durga";
        System.out.println(s instanceof String == true);  // prints true
        System.out.println(s instanceof Object);           // prints true
        System.out.println(null instanceof String);        // prints false
    }
}
```

> ⚠️ **Modern Java — `instanceof` gained a second form, precedence unchanged.**
> Since **Java 16** (JEP 394, pattern matching for `instanceof`), the same
> operator can bind a variable on success:
>
> ```java
> Object o = "durga";
> if (o instanceof String s) {
>     System.out.println(s.length()); // s is a String here, no cast needed
> }
> ```
>
> This is new *syntax* for `instanceof`, not a new precedence level — it
> still sits exactly where this lecture's chart puts it, above `==` and below
> shift. The pre-16 cast-after-check pattern Sir doesn't show here (`if (o
> instanceof String) { String s = (String) o; }`) still compiles; the pattern
> form is just the version worth writing in new code.

## Bitwise versus short-circuit versus ternary versus assignment

`&` `^` `|` sit below equality and above `&&` `||`. Assignment is the floor of
the chart.

```java
class Test {
    public static void main(String[] args) {
        System.out.println(4 & 5 == 4);
        // NOT true — == is higher than &
        // grouping:  4 & (5 == 4)  →  4 & false
        // CE: bad operand types for binary operator '&' — int, boolean
    }
}
```

Correct grouping if the bitwise operation is meant to run first:

```java
class Test {
    public static void main(String[] args) {
        System.out.println((4 & 5) == 4); // prints true  →  4 == 4
        System.out.println(4 & 5);        // prints 4
    }
}
```

`&&` above `||`:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(true || false && false);  // prints true  →  true || (false && false)
        System.out.println((true || false) && false); // prints false
    }
}
```

Ternary sits just above assignment, and assignment is the lowest of all, so
`x = 1 + 2 * 3` assigns `7` — it does not assign `1` and then try to add:

```java
class Test {
    public static void main(String[] args) {
        int x;
        x = 1 + 2 * 3;
        System.out.println(x); // prints 7  →  x = (1 + (2 * 3))
    }
}
```

Chained assignment is right-associative (from Part 5) — precedence *and*
associativity both apply here:

```java
class Test {
    public static void main(String[] args) {
        int a, b, c;
        a = b = c = 20; // c = 20, then b = 20, then a = 20
        System.out.println(a + "..." + b + "..." + c); // prints 20...20...20
    }
}
```

Subtraction is the opposite associativity — plain left to right:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(10 - 5 - 2);   // prints 3   →  (10 - 5) - 2
        System.out.println(10 - (5 - 2)); // prints 7
    }
}
```

## Golden rule — there is no precedence for operands

Sir underlines this twice. *Operator precedence* decides which operator is
applied first. *Operand evaluation* decides which operand is computed first,
and it has exactly one rule:

> There is no precedence for operands. Before applying any operator, all
> operands are evaluated from left to right.

The mental model is two phases:

1. Walk the expression left to right. Evaluate every operand — method calls,
   `++`, `--`, array indexes — as you reach it. Side effects happen *now*.
2. Then apply the operators, using the chart and its associativity.

Students often assume `*` runs before the left `+` operand is even touched.
It doesn't — the left method call still runs first, in source order.

```java
class Test {
    public static void main(String[] args) {
        System.out.println(m1(1) + m1(2) * m1(3));
    }
    public static int m1(int i) {
        System.out.println(i);
        return i;
    }
}
// prints
// 1
// 2
// 3
// 7
```

Phase 1: `m1(1)`, then `m1(2)`, then `m1(3)` — printed in that order even
though `*` is stronger than `+`. Phase 2: the expression is now `1 + 2 * 3` →
`1 + 6` → `7`.

## The famous program — `m1(1)+m1(2)*m1(3)/m1(4)*m1(5)+m1(6)`

This is *the* Part-6 program: Sir types it, runs it, and only then explains
the output. Watch the print order — 1 to 6, sequential. Precedence belongs to
`*`, but operand order never moves.

```java
class Test {
    public static void main(String[] args) {
        System.out.println(m1(1) + m1(2) * m1(3) / m1(4) * m1(5) + m1(6));
    }
    public static int m1(int i) {
        System.out.println(i);
        return i;
    }
}
// prints
// 1
// 2
// 3
// 4
// 5
// 6
// 12
```

Phase 1 — operands left to right — returns `1`, `2`, `3`, `4`, `5`, `6`. The
expression collapses to:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(1 + 2 * 3 / 4 * 5 + 6); // prints 12
    }
}
```

Phase 2 — `*` `/` `%` left to right, then `+`:

- `2 * 3` → `6`
- `6 / 4` → `1` (integer division — miss this and you'll say 13)
- `1 * 5` → `5`
- `1 + 5 + 6` → `12`

Wrong answers the classroom offers, and why each is wrong:

- `13` — treats `6 / 4` as real-number division (`1.5`) instead of truncating
  integer division.
- prints `2 3 4 5` before `1` — confuses operand evaluation order with
  operator precedence; `m1` calls always fire in source order regardless of
  `*`/`/`.
- `15` — evaluates `2*3/4*5` as `2*(3/4)*5` with float semantics, or applies
  `+` before `*`/`/`.

## Interview trick — `i += ++i + i++ + ++i + i++`

Compound assignment evaluates the left operand exactly once, first. Then the
right-hand expression, left to right. Then the operator. Then the assignment
writes back.

```java
class Test {
    public static void main(String[] args) {
        int i = 1;
        i += ++i + i++ + ++i + i++;
        System.out.println(i); // prints 13
    }
}
```

Conceptually:

```java
class Test {
    public static void main(String[] args) {
        int i = 1;
        // i += ++i + i++ + ++i + i++;
        // means:  i = i + (++i + i++ + ++i + i++)
        // the left i is captured as 1 first
        System.out.println(1 + 2 + 2 + 4 + 4); // prints 13
    }
}
```

Walked step by step:

| Step | Operand | Value used | `i` after |
|---|---|---|---|
| 1 | left-hand `i` of `+=` | 1 | 1 |
| 2 | `++i` | 2 | 2 |
| 3 | `i++` | 2 | 3 |
| 4 | `++i` | 4 | 4 |
| 5 | `i++` | 4 | 5 |

`1 + 2 + 2 + 4 + 4 = 13`, then `i = 13`. Final print is **13** — not 5, not
15, not 11.

## Interview trick — `x = ++x + ++x`

A perennial favourite. The operands of `+` are evaluated left to right;
assignment happens last, since it's the lowest-precedence operator involved.

```java
class Test {
    public static void main(String[] args) {
        int x = 0;
        x = ++x + ++x;
        System.out.println(x); // prints 3
    }
}
```

Walked from `x = 0`:

1. Left `++x` → `x` becomes `1`, value used is `1`.
2. Right `++x` → `x` becomes `2`, value used is `2`.
3. `+` → `1 + 2 = 3`.
4. `=` → `x = 3`.

Common wrong answers are `2` (stopping after two increments) or `4` (adding
after the assignment already happened). The real answer is **3**.

Starting at `1`:

```java
class Test {
    public static void main(String[] args) {
        int x = 1;
        x = ++x + ++x;
        System.out.println(x); // prints 5   →  2 + 3
    }
}
```

Mixing pre- and post-increment:

```java
class Test {
    public static void main(String[] args) {
        int x = 0;
        x = x++ + ++x;
        System.out.println(x); // prints 2
        // x++ uses 0, x becomes 1; ++x makes x 2, uses 2; 0+2=2; assign 2
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        int x = 1;
        x = x++ + ++x;
        System.out.println(x); // prints 4
        // x++ uses 1, x=2; ++x → x=3, uses 3; 1+3=4
    }
}
```

The Part-1/Part-7 cousin `x = x++` follows the same two-phase story: the
increment happens, but the assignment writes back the *old*, captured value:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        x = x++;
        System.out.println(x); // prints 10
        // 1) capture old value 10 for the assignment
        // 2) increment x to 11
        // 3) assign the captured 10 back to x
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        x = ++x;
        System.out.println(x); // prints 11
    }
}
```

## Operand evaluation of assignment — `a[index] = index = 3`

Assignment is right-associative, but the operands of each `=` are still
evaluated left to right. The left-hand array slot is resolved *before* the
right-hand assignment changes `index`.

```java
class Test {
    public static void main(String[] args) {
        int[] a = {10, 20, 30, 40, 50};
        int index = 0;
        a[index] = index = 3;
        System.out.println(index);    // prints 3
        System.out.println(a[0]);     // prints 3
        System.out.println(a[3]);     // prints 40   (unchanged!)
    }
}
```

The slot `a[0]` is already selected by the time `index` becomes `3`. The `3`
then lands in `a[0]`, not `a[3]`. The tempting exam option — "the array
becomes `{10,20,30,3,50}`" — is the trap.

## Method arguments are also left to right

The same golden rule governs argument lists:

```java
class Test {
    public static void main(String[] args) {
        m(m1(1), m1(2), m1(3));
    }
    public static int m1(int i) {
        System.out.println(i);
        return i;
    }
    public static void m(int a, int b, int c) {
        System.out.println(a + b * c); // prints 7  →  1 + 2 * 3
    }
}
// prints
// 1
// 2
// 3
// 7
```

Mixing a method call with increments follows the same two phases:

```java
class Test {
    static int x = 5;
    public static int getValue() {
        System.out.print("G");
        return 10;
    }
    public static void main(String[] args) {
        int result = getValue() + x++ * ++x;
        System.out.println();
        System.out.println(result); // prints 45
        System.out.println(x);      // prints 7
        // operands: getValue()→10, x++ uses 5 (x becomes 6), ++x → 7
        // 10 + 5 * 7 = 45
    }
}
// prints
// G
// 45
// 7
```

## Parentheses versus the chart — what he wants in real code

Precedence exists so the language has a defined meaning; using extra brackets
in production code is not something to be ashamed of. Exams remove brackets
on purpose, to test whether you know the chart without them.

```java
class Test {
    public static void main(String[] args) {
        int a = 10, b = 20, c = 30;
        System.out.println(a + b * c);      // prints 610
        System.out.println(a > 5 && b > 5); // prints true
        System.out.println(a = b = c);      // prints 30 (value of the assignment)
    }
}
```

The value of an assignment expression is the value written to the left
variable — that's why `System.out.println(a = b = c)` compiles and prints
`30`. Lowest precedence, right associativity, and the result is still a
value that can be used:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        System.out.println(x = 20); // prints 20
        System.out.println(x);      // prints 20
    }
}
```

## The precedence rules, summarized

1. Operators have precedence; operands do not.
2. Highest band: `[]` `()` `.` postfix `++` `--`, then prefix unary, `new`,
   cast.
3. Then `*` `/` `%`, then `+` `-` (including string `+`), then shift, then
   comparison/`instanceof`, then `==` `!=`.
4. Then `&`, then `^`, then `|`, then `&&`, then `||`, then `?:`, then
   assignment (lowest).
5. Same-precedence binary operators: left → right. Assignment, ternary,
   prefix unary: right → left.
6. Parentheses override everything. When in doubt, use `()`.
7. Evaluation of an expression: first, every operand left to right (side
   effects happen now); only then, operators applied per the chart.
8. Integer `/` and `%` truncate toward zero — `6/4` is `1`, which is why the
   famous program ends in `12`.
9. `+=` evaluates the left variable once, first, then the right-hand
   expression.
10. `a[index] = index = 3` updates `a[old index]`, not `a[3]`.

---

## Exam and interview points

1. **`1 + 2 * 3` is 7, not 9.** Multiplication binds tighter than addition;
   scanning left to right like English text is the trap.
2. **`1 + 2 << 1` is 6, not 5.** Additive is above shift on Java's chart — a
   C habit of assuming shift outranks `+` gives the wrong answer here.
3. **`(int) 10.9 * 2` is 20, not 21.** Cast is unary and binds before `*`;
   only `(int) (10.9 * 2)` gives 21.
4. **`10 < 20 < 30` is a compile error**, not a chained comparison — `<`
   needs two numeric operands, and the first `<` already produced a
   `boolean`.
5. **`4 & 5 == 4` is a compile error**, not `true` — `==` outranks `&`, so
   the grouping is `4 & (5 == 4)`, i.e. `int & boolean`.
6. **`true || false && false` is `true`** because `&&` binds tighter than
   `||`.
7. **The famous `m1` chain prints its calls in order 1 through 6, then
   `12`** — operand evaluation order never bends to operator precedence.
8. **`i += ++i + i++ + ++i + i++` with `i = 1` gives `13`.** Compound
   assignment reads the left operand once, up front, before the right side
   runs.
9. **`x = ++x + ++x` with `x = 0` gives `3`**, not 2 or 4 — both increments
   happen before the addition, and the addition happens before the
   assignment.
10. **`x = x++` with `x = 10` gives `10`.** The old value is captured before
    the increment, and that captured value — not the incremented one — is
    what gets assigned back.
11. **`a[index] = index = 3` with `index = 0` writes to `a[0]`, not `a[3]`.**
    The array slot is resolved before the right-hand assignment changes
    `index`.
12. **`instanceof` outranks `==`,** so `s instanceof String == true` groups
    as `(s instanceof String) == true`. Since Java 16, the same operator can
    also bind a pattern variable (`o instanceof String s`) — the precedence
    is unchanged, only the syntax gained a new form.

---

**Next:** Video 023 — Operators & Assignments Part-7 (Interview FAQs: `new`
vs `newInstance()`, `instanceof` vs `isInstance()`, `ClassNotFoundException`
vs `NoClassDefFoundError`, plus the remaining operator interview mix)
