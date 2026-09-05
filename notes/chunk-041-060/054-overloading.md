# Video 054 — Overloading

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming)Part-4 ||overloading

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 54 of 203 |
| Series | OOPs · Part 4 |
| Topic | overloading |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 07m 40s |
| Video ID | tSv-XlP_1JA |
| Watch | https://www.youtube.com/watch?v=tSv-XlP_1JA |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Video 053 already gave the definition of overloading (same name, different
argument types) and the headline rule that resolution is compiler-driven,
based on reference type. This video assumes that and spends the whole hour on
**six loophole cases** — the ones OCJP and interviews actually probe:

1. `m1(int)` vs `m1(float)` — automatic promotion (`char`→`int`, `long`→`float`, …)
2. `m1(String)` vs `m1(Object)` — child type beats parent type
3. `m1(String)` vs `m1(StringBuffer)` — same-level siblings, `null` is ambiguous
4. `m1(int,float)` vs `m1(float,int)` — argument order counts; both-match vs neither-match
5. `m1(int)` vs `m1(int...)` — var-arg is always the last resort
6. `m1(Animal)` vs `m1(Monkey)` — reference type decides, runtime object never does

---

## 00:05 — This video is loopholes, not the definition

Last session covered the basics of overloading. This one drills five or six
internal-resolution cases — all important for the exam and for the interview
room.

---

## 00:45 — Case 1: `int` version vs `float` version

Class `Test`, two instance methods, same name, different argument types:

```java
class Test {
    public void m1(int i) {
        System.out.println("int-arg method");
    }

    public void m1(float f) {
        System.out.println("float-arg method");
    }
}
```

Two methods, and they're overloaded — same name, different argument types.

### 02:06 — `main`, `t.m1(10)`, `t.m1(10.5f)`

```java
class Test {
    public void m1(int i) {
        System.out.println("int-arg method");
    }

    public void m1(float f) {
        System.out.println("float-arg method");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1(10);     // exact match: int -> prints int-arg method
        t.m1(10.5f);  // exact match: float -> prints float-arg method
    }
}
```

Exact match always gets top priority. `10` is `int`, so the int-arg method
runs; `10.5f` is `float`, so the float-arg method runs.

### 03:11 — The reception-chair story (why `char` → `int` matters)

Sir tells a story from years back: a four-year Java veteran wanting to skip
straight into the SCJP batch complained that "stupid" people fail interviews
on basic questions. His last interview had asked exactly one thing: *a method
takes `int`; you pass `char` — does it run?* He said no, was told he was
wrong three times, and was shown the door. Rather than just asserting the
answer to his own class, Sir ran the program live and let the output settle
it: for a `char` argument, the int-arg method *does* get the chance.

### 09:32 — `t.m1('a')` and the generalized promotion rule

```java
class Test {
    public void m1(int i) {
        System.out.println("int-arg method");
    }

    public void m1(float f) {
        System.out.println("float-arg method");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1('a'); // prints int-arg method
    }
}
```

If a method takes `int` and you pass `char`, that method runs. The general
rule: while resolving an overloaded call, the compiler first looks for an
**exact match**. If there isn't one, it does **not** immediately raise a
compile-time error — it **promotes** the argument to the next level and
checks again. `char` promotes to `int` automatically; match found.

If that still didn't match, it would promote again — `long`, then `float`,
then `double` — the same idea applies down the `byte`→`short`→`int` chain.
Promotion is automatic; you never write the cast yourself.

**Board dictation:** While resolving overloaded methods, if the exact matched
method is not available, the compiler will not raise a compile-time error
immediately. It promotes the argument to the next level and checks again; if
a match is available it is considered; if not, it promotes once more. This
continues until all possible promotions are exhausted — only then, if still
no match, does the compiler raise a compile-time error.

### 12:11 — `t.m1(10L)` vs `t.m1(10.5)`

```java
class Test {
    public void m1(int i) {
        System.out.println("int-arg method");
    }

    public void m1(float f) {
        System.out.println("float-arg method");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1(10L); // long has no matching method; promote long -> float -> matches
                   // prints float-arg method
    }
}
```

```java
class Test {
    public void m1(int i) {
        System.out.println("int-arg method");
    }

    public void m1(float f) {
        System.out.println("float-arg method");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1(10.5); // CE: no suitable method found for m1(double)
                    //   method Test.m1(int) is not applicable
                    //     (argument mismatch; possible lossy conversion from double to int)
                    //   method Test.m1(float) is not applicable
                    //     (argument mismatch; possible lossy conversion from double to float)
    }
}
```

`10.5` is `double` by default. There's no double-arg method, and `double`
cannot be promoted any further — it's the widest primitive type. Match not
found, no promotion possible → compile-time error.

> ⚠️ **Modern Java — the wording of this error has changed; the outcome hasn't.**
> Sir dictates this error on the board (and it is what OCJP-era javac showed)
> as a flat:
> ```text
> cannot find symbol
> symbol: method m1(double)
> location: class Test
> ```
> Compiled just now on current javac (26), the same call instead produces the
> "no suitable method found" block shown above, listing *why* each existing
> `m1` overload was rejected. javac's diagnostics for exactly this
> situation — a method name that exists, just with no applicable overload —
> were substantially rewritten starting around **JDK 7**, replacing the old
> blanket message with per-candidate reasons. (The bare "cannot find symbol"
> still appears today, but only when the method name itself doesn't exist at
> all — not when it exists with the wrong argument types.) The same rewrite
> also added the "both method X and method Y match" explanation line you'll
> see under Case 3 and Case 4's **ambiguous** errors below — the headline
> sentence there, "reference to m1 is ambiguous," is unchanged. Know the
> concept either way; don't be thrown by the extra detail on a real machine.

### 18:14 — All possible promotions (board diagram)

```text
byte -> short -> int -> long -> float -> double
                  ^
                 char
```

- `byte` to `short`
- `short` to `int`
- `int` to `long`
- `long` to `float`
- `float` to `double`
- `char` to `int`

This chain is called **automatic promotion in overloading**.

### 19:54 — Recopy Case 1 (full board program)

```java
class Test {
    public void m1(int i) {
        System.out.println("int-arg method");
    }

    public void m1(float f) {
        System.out.println("float-arg method");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1(10);     // prints int-arg method
        t.m1(10.5f);  // prints float-arg method
        t.m1('a');    // prints int-arg method  (char -> int)
        t.m1(10L);    // prints float-arg method (long -> float)
        // t.m1(10.5); // CE: no suitable method found for m1(double)
    }
}
```

Case one done. Next: case two.

---

## 22:15 — Case 2: `String` version vs `Object` version

Same `m1` name, now with reference types instead of primitives:

```java
class Test {
    public void m1(String s) {
        System.out.println("String version");
    }

    public void m1(Object o) {
        System.out.println("Object version");
    }
}
```

Overloaded? Yes — same name, different argument types.

### 24:01 — Exact match: `new Object()` and `"durga"`

```java
class Test {
    public void m1(String s) {
        System.out.println("String version");
    }

    public void m1(Object o) {
        System.out.println("Object version");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1(new Object()); // exact match -> prints Object version
        t.m1("durga");      // exact match -> prints String version
    }
}
```

### 25:08 — `t.m1(null)`: child vs parent

```java
class Test {
    public void m1(String s) {
        System.out.println("String version");
    }

    public void m1(Object o) {
        System.out.println("Object version");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1(null); // prints String version
    }
}
```

`null` is a valid value for `String` *and* for `Object`. `Object` is the
parent; `String` is the child. Which gets the chance?

### 26:05 — Collector-office analogy

Sir's story, compressed: you go to the collector's office (parent) for a
two-minute signature; you don't waste the collector's time asking about
nearby movie theatres — that question goes to the attender (child) outside.
If the work can complete at the attender's level, there's no need to escalate
to the collector.

Same idea here: `null` is valid for both `String` (child) and `Object`
(parent). If the call can be satisfied at the **child** level, there's no
need to go to the **parent**.

### 28:54 — Child type gets more priority; recopy Case 2

```java
class Test {
    public void m1(String s) {
        System.out.println("String version");
    }

    public void m1(Object o) {
        System.out.println("Object version");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1(new Object()); // prints Object version
        t.m1("durga");      // prints String version
        t.m1(null);         // prints String version
    }
}
```

### 31:48 — Board note (Case 2 rule)

While resolving overloaded methods, the compiler always gives precedence to
the **child type** argument over the **parent type** argument, when both
match.

---

## 32:50 — Case 3: `String` vs `StringBuffer` (same level)

```java
class Test {
    public void m1(String s) {
        System.out.println("String version");
    }

    public void m1(StringBuffer sb) {
        System.out.println("StringBuffer version");
    }
}
```

`Object` is the parent of both; `String` and `StringBuffer` are two
*different* children, sitting at the **same level** — neither is a subtype of
the other.

### 33:58 — Exact matches still win

```java
class Test {
    public void m1(String s) {
        System.out.println("String version");
    }

    public void m1(StringBuffer sb) {
        System.out.println("StringBuffer version");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1("durga");                    // prints String version
        t.m1(new StringBuffer("durga"));  // prints StringBuffer version
    }
}
```

### 34:55 — `t.m1(null)` is ambiguous

```java
class Test {
    public void m1(String s) {
        System.out.println("String version");
    }

    public void m1(StringBuffer sb) {
        System.out.println("StringBuffer version");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1(null);
        // CE: reference to m1 is ambiguous
        //   both method m1(String) in Test and method m1(StringBuffer) in Test match
    }
}
```

`null` is valid for both `String` and `StringBuffer`, and they are siblings —
neither one is more specific than the other. Case 2's child-beats-parent rule
doesn't apply because there's no parent/child relationship to break the tie.
Both methods match, both sit at the same level → immediate compile-time
error: **reference to m1 is ambiguous**.

### 36:29 — Recopy Case 3

```java
class Test {
    public void m1(String s) {
        System.out.println("String version");
    }

    public void m1(StringBuffer sb) {
        System.out.println("StringBuffer version");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1("durga");                    // prints String version
        t.m1(new StringBuffer("durga"));  // prints StringBuffer version
        // t.m1(null);                    // CE: reference to m1 is ambiguous
    }
}
```

Case three done.

---

## 39:18 — Case 4: order of arguments (`int,float` vs `float,int`)

```java
class Test {
    public void m1(int i, float f) {
        System.out.println("int-float version");
    }

    public void m1(float f, int i) {
        System.out.println("float-int version");
    }
}
```

Two methods: **overloaded** — a change in the *order* of arguments is
sufficient on its own.

### 40:41 — Exact-match two-arg calls

```java
class Test {
    public void m1(int i, float f) {
        System.out.println("int-float version");
    }

    public void m1(float f, int i) {
        System.out.println("float-int version");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1(10, 10.5f);  // prints int-float version
        t.m1(10.5f, 10);  // prints float-int version
    }
}
```

### 41:41 — `t.m1(10, 10)`: both match

```java
class Test {
    public void m1(int i, float f) {
        System.out.println("int-float version");
    }

    public void m1(float f, int i) {
        System.out.println("float-int version");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1(10, 10);
        // CE: reference to m1 is ambiguous
        //   both method m1(int,float) in Test and method m1(float,int) in Test match
    }
}
```

Both arguments are `int`. The first method's first parameter is an exact
`int` match, and its second `int` promotes to `float` — matches. The second
method's second parameter is an exact `int` match, and its first `int`
promotes to `float` — also matches. Sir's joke: is the answer "read
left-to-right" in India and "read right-to-left" in Pakistan? No — Java isn't
country-dependent. Both overloads genuinely match, the compiler has no way to
prefer one, so it's an immediate **ambiguous** error regardless of reading
direction.

### 43:40 — `t.m1(10.5f, 10.5f)`: neither matches

```java
class Test {
    public void m1(int i, float f) {
        System.out.println("int-float version");
    }

    public void m1(float f, int i) {
        System.out.println("float-int version");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1(10.5f, 10.5f);
        // CE: no suitable method found for m1(float,float)
        //   method Test.m1(int,float) is not applicable
        //     (argument mismatch; possible lossy conversion from float to int)
        //   method Test.m1(float,int) is not applicable
        //     (argument mismatch; possible lossy conversion from float to int)
    }
}
```

Both arguments are `float`. Neither method's `int` parameter can accept a
`float` — that's a *narrowing* conversion (`float` → `int` is not a widening
promotion; only `int` → `float` is). No method matches at all →
**cannot find symbol** territory (see the Modern Java note in Case 1 for how
javac phrases this today).

Rule of thumb Sir gives: **both match → ambiguous; none match → cannot find
symbol / no suitable method.**

### 45:21 — Recopy Case 4

```java
class Test {
    public void m1(int i, float f) {
        System.out.println("int-float version");
    }

    public void m1(float f, int i) {
        System.out.println("float-int version");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1(10, 10.5f);     // prints int-float version
        t.m1(10.5f, 10);     // prints float-int version
        // t.m1(10, 10);      // CE: reference to m1 is ambiguous
        // t.m1(10.5f, 10.5f); // CE: no suitable method found for m1(float,float)
    }
}
```

Case four done.

---

## 48:43 — Case 5: general method vs var-arg

```java
class Test {
    public void m1(int i) {
        System.out.println("general method");
    }

    public void m1(int... x) {
        System.out.println("var-arg method");
    }
}
```

Overloaded — same name, different argument types. One takes a single `int`;
the var-arg one can be called with **any number** of `int` values, including
zero.

### 49:48 — Zero args, two args, one arg

```java
class Test {
    public void m1(int i) {
        System.out.println("general method");
    }

    public void m1(int... x) {
        System.out.println("var-arg method");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1();       // no method matches int-arg; var-arg accepts zero -> var-arg method
        t.m1(10, 20); // no method matches int-arg; var-arg accepts two  -> var-arg method
        t.m1(10);     // BOTH match -> see below
    }
}
```

For `t.m1(10)`, **both** `m1(int)` and `m1(int...)` match. Which wins?

### 51:08 — "Old version beats new version"

Sir's memory hook: `m1(int)` is the "senior" method — the plain, fixed-arity
method concept has been in Java since **1.0**; var-arg arrived in **1.5**. In
a fight between old and new, the old one wins, to preserve compatibility with
code that predates var-args. Output: **general method**.

> ❗ **Correction — it isn't really about which version is older.**
> The actual mechanism is the compiler's three-phase overload resolution
> (JLS §15.12.2), unchanged since var-args and autoboxing both arrived in
> Java 5: **Phase 1** tries every applicable method using only exact matches
> and widening/promotion, with var-arg methods excluded entirely. **Phase 2**
> allows boxing/unboxing, still no var-arg. Only if *nothing* matched in
> either phase does **Phase 3** bring var-arg methods into consideration.
> `m1(10)` matches `m1(int)` in Phase 1, so the algorithm never even reaches
> the phase where `m1(int...)` would be considered — it isn't "1.0 beats
> 1.5," it's "fixed-arity is tried first, period." Sir's mnemonic correctly
> predicts every outcome in this lecture; just don't repeat "older code wins"
> in an interview as if the compiler tracks release history.

### 52:04 — Recopy Case 5

```java
class Test {
    public void m1(int i) {
        System.out.println("general method");
    }

    public void m1(int... x) {
        System.out.println("var-arg method");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1();       // prints var-arg method
        t.m1(10, 20); // prints var-arg method
        t.m1(10);     // prints general method
    }
}
```

### 53:51 — Conclusion: var-arg has least priority (like `default` in `switch`)

**In general, a var-arg method gets the least priority.** It only gets the
chance if no other (fixed-arity) method matched — exactly like `default`
inside a `switch`, which only runs if no `case` matched:

```java
class SwitchDefaultAnalogy {
    public static void main(String[] args) {
        int x = 10;
        switch (x) {
            case 1:
                System.out.println("case 1");
                break;
            case 2:
                System.out.println("case 2");
                break;
            default:
                System.out.println("default"); // only if no other case matched
        }
    }
}
```

That's case five. Last one, and an important one: case six.

---

## 56:37 — Case 6: `Animal` vs `Monkey`

```java
class Animal {
}

class Monkey extends Animal {
}
```

Sir's running joke for the child class name: he calls it `Monkey` rather than
`Dog` or `Tiger`, with a wink at the "job-hopping" stereotype about Indian
software engineers — a one-line aside, not the technical point.

### 59:34 — `Test`: Animal version and Monkey version

```java
class Animal {
}

class Monkey extends Animal {
}

class Test {
    public void m1(Animal a) {
        System.out.println("Animal version");
    }

    public void m1(Monkey m) {
        System.out.println("Monkey version");
    }
}
```

Overloaded — same name, different argument types (`Animal` vs `Monkey`).

### 1:01:04 — Three calls: exact parent, exact child, parent-ref + child-obj

```java
class Animal {
}

class Monkey extends Animal {
}

class Test {
    public void m1(Animal a) {
        System.out.println("Animal version");
    }

    public void m1(Monkey m) {
        System.out.println("Monkey version");
    }

    public static void main(String[] args) {
        Test t = new Test();

        Animal a = new Animal();
        t.m1(a); // exact match on reference type -> prints Animal version

        Monkey m = new Monkey();
        t.m1(m); // exact match on reference type -> prints Monkey version

        Animal a1 = new Monkey(); // parent reference, child object
        t.m1(a1); // prints Animal version  (reference type is Animal)
    }
}
```

| Call | Reference type | Object type | Output |
|---|---|---|---|
| `t.m1(a)` | `Animal` | `Animal` | Animal version |
| `t.m1(m)` | `Monkey` | `Monkey` | Monkey version |
| `t.m1(a1)` | `Animal` | `Monkey` | Animal version |

The third row is the one that trips people up. Remember the rule from last
session: **in overloading, the compiler resolves methods based on reference
type; the runtime object never plays any role.** `a1` is declared as
`Animal`, so `m1(Animal)` runs — even though the object underneath is
actually a `Monkey`.

### 1:04:27 — Recopy Case 6

```java
class Animal {
}

class Monkey extends Animal {
}

class Test {
    public void m1(Animal a) {
        System.out.println("Animal version");
    }

    public void m1(Monkey m) {
        System.out.println("Monkey version");
    }

    public static void main(String[] args) {
        Test t = new Test();

        Animal a = new Animal();
        t.m1(a); // prints Animal version

        Monkey m = new Monkey();
        t.m1(m); // prints Monkey version

        Animal a1 = new Monkey();
        t.m1(a1); // prints Animal version  (reference type Animal)
    }
}
```

### 1:05:52 — Board note (same point as last session)

**In overloading, method resolution always takes care by compiler based on
reference type. In overloading, runtime object won't play any role.**

---

## 1:07:19 — Wrap-up

These six cases are the loopholes of overloading. Next session: **overriding**
— where, in direct contrast to everything above, the runtime object *does*
decide which method runs.

---

## Exam and interview points

1. **Exact match always wins first.** Only when there is no exact match does
   the compiler try automatic promotion: `byte`→`short`→`int`→`long`→`float`→`double`,
   with `char` feeding into `int`.
2. **`double` is the ceiling.** It's the widest primitive, so an unmatched
   `double` argument (no further promotion possible) is a compile-time error,
   not a silent pick of some other overload.
3. **Child beats parent when both match.** `m1(String)` vs `m1(Object)`:
   `null` resolves to `String` — the more specific (child) type — every time.
4. **Two unrelated sibling types matching the same value is ambiguous, not a
   coin flip.** `m1(String)` vs `m1(StringBuffer)` with `null`: neither is a
   subtype of the other, so both matching is a compile-time error
   (`reference to m1 is ambiguous`), decided at compile time, never at
   runtime.
5. **Argument order is part of the signature.** `m1(int,float)` and
   `m1(float,int)` are legitimately overloaded. If a call can only reach both
   overloads via promotion (`m1(10,10)`), that's ambiguous; if it can reach
   neither even with promotion (`m1(10.5f,10.5f)`, since `float`→`int` is
   narrowing), that's cannot-find-symbol / no-suitable-method.
6. **Var-arg is always the last resort**, exactly like `default` in a
   `switch`: it only gets the call if no fixed-arity overload matches. The
   real mechanism is the compiler's three-phase resolution (strict match,
   then boxing, then var-arg) — not "older code always wins," even though
   that mnemonic predicts the right answer.
7. **Overloading is resolved entirely from the reference type, at compile
   time — the runtime object is irrelevant.** `Animal a1 = new Monkey();
   t.m1(a1);` calls the `Animal` overload. This is exactly why overloading is
   called compile-time / static polymorphism / early binding, and it's the
   opposite of what overriding does (next video).
8. **Modern javac's error *wording* has moved, the underlying rules haven't.**
   Since roughly JDK 7, a call that matches no overload of an existing method
   name reports "no suitable method found for m1(...)" with a per-candidate
   reason, instead of the flat "cannot find symbol" from the board — know
   both phrasings.

---

**Next:** Video 055 — Overriding
