# Video 104

## Video info

| Field | Value |  |  |
|---|---|---|---|
| Title: | Core Java With OCJP/SCJP: Innerclass Part- 5 \ | \ | nested classes and interfaces |
| Position | 104 of 203 |  |  |
| Series | Inner Classes · Part 5 |  |  |
| Instructor | Durga Sir |  |  |
| Duration | 1h 00m 29s |  |  |
| Video ID | V3fhKrL8fy8 |  |  |
| Watch | https://www.youtube.com/watch?v=V3fhKrL8fy8 |  |  |
| Playlist | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |  |  |
| Notes source | Local Whisper STT |  |  |

## Session overview

Part 5 closes the **nested classes and interfaces** topic by walking through all **four valid nesting combinations**, giving a real-world justification for each, running compile/execute demos on the board, and ending with **modifier rules** (what is always `public static`, what is only `static`, etc.). This is the capstone of roughly four prior sessions on inner/nested types.

**ASR decoding note:** Whisper often heard *interface* as *entrapage*, *entropy*, *intraface*, *intraphase*; *existing* as *digesting*; *m1/m2* as *Yam/Yaman/human*; *wheels* as *fields*; *an entry* as *Yarn entry*; *valid* as *valley/value*. All such tokens are corrected below.

### 00:04 — Opening recap: can you nest types?

Durga Sir opens with interview-style rapid-fire questions the panel may ask after three or four prior sessions on inner classes:

- Can I declare a **class inside a class**?
- Can I declare a **class inside an interface**?
- Can I declare an **interface inside an interface**?
- Can I declare an **interface inside a class**?
The short interview answer for all four: **yes — anything inside anything is possible** with respect to classes and interfaces.

But the interviewer may follow up: *"Can you explain with an example where that requirement exists?"* — especially for the less obvious cases like **class inside interface**, where everything in an interface is normally abstract. This session supplies those examples and the governing rules.

### 01:02 — Interview follow-up: justify each combination

Panels rarely stop at "yes." They expect **where** and **why**:

- **Class inside interface** — unusual because interface members are usually abstract; you must cite a concrete API-style use (helper parameter class, default impl class).
- **Interface inside interface** — cite `Map.Entry` or similar nested API.
- **Interface inside class** — cite localized multiple implementations scoped to one outer class.
- **Class inside class** — cite domain containment (University/Department).
Durga Sir's board heading for the session: **various combinations of nested classes and interfaces** — four cases, each with theory + example.

### 00:47 — All four combinations are valid

The four nesting patterns (all legal in Java):

| # | Pattern | Status |
|---|---|---|
| 1 | Class inside class | Valid |
| 2 | Interface inside class | Valid |
| 3 | Interface inside interface | Valid |
| 4 | Class inside interface | Valid |

The lecture systematically covers each with theory, a motivating scenario, board code, and (where applicable) execution output.

### 01:58 — Case 1: Class inside a class

**Rule (theory):** Without **existing** one type of object, if there is **no chance of existing** another type of object, then we can declare a **class inside a class**.

**Real-world analogy:** A **department** is always part of a **university**. Without a university, a department cannot exist independently. Therefore the `Department` class should live **inside** the `University` class.

**Interview phrasing:** "Department is always part of university; without existing university there is no chance of existing department — so declare department class inside university class."

By default this pattern is treated as **class inside class** (member / nested class), not a top-level type.

```java
class University {
    // Department cannot meaningfully exist without a University context
    class Department {
        // department-specific members
    }
}
```

**Key takeaway:** Use **class inside class** when the inner type's lifecycle and meaning are **tightly bound** to the outer type — the inner object should not exist as a standalone concept in the domain model.

### 04:06 — Case 1 example on board: University → Department

Board notes repeated the domain story:

- University consists of several departments.
- Without existing university, there is no chance of existing department.
- Hence: declare **department class inside university class**.
```java
class University {
    class Department {
        String name;

        Department(String name) {
            this.name = name;
        }

        void show() {
            System.out.println("Department: " + name + " (under University)");
        }
    }

    void addDepartment(String deptName) {
        Department d = new Department(deptName);
        d.show();
    }
}
```

**CE/prints:** No standalone compile demo in this segment; the emphasis is conceptual. If used from `main`, you would typically need an outer instance (unless `Department` were `static` — not discussed here).

### 05:23 — Case 2: Interface inside a class

**Scenario:** You have **one outer class** and within it you need **multiple implementations of an interface**, and **all those implementations are relevant only to that particular class** — not general-purpose types for the whole application.

**Analogy on board:** "Chest of drawers" — one container (`VehicleTypes`) holding several related vehicle implementations.

**Rule heading (board):** *Interface inside a class — if we require multiple implementations of an interface, and all these implementations are related to your particular class, then we can define interface inside a class.*

```java
class VehicleTypes {

    interface Vehicle {
        int getNumberOfWheels();
    }

    class Bus implements Vehicle {
        public int getNumberOfWheels() {
            return 6;
        }
    }

    class Auto implements Vehicle {
        public int getNumberOfWheels() {
            return 3;
        }
    }

    // ... several more implementation classes possible ...
}
```

**Key points from board walkthrough:**

- `Vehicle` interface declares `getNumberOfWheels()`.
- `Bus implements Vehicle` → returns **6**.
- `Auto implements Vehicle` → returns **3**.
- Dot-dot-dot: many more vehicle classes can follow the same pattern.
**Why nest here?** Bus, Auto, etc. are not generic application-wide types; they exist **only to categorize vehicles within `VehicleTypes`**. Nesting keeps cohesion and hides implementation detail inside the owning class.

### 08:51 — Case 2 conclusion

**Can I declare interface inside a class?** Yes, no problem.

Use when:

1. Multiple interface implementations are needed.
1. All implementations belong to / are scoped to one outer class.
1. You want modular, localized design rather than polluting the package with many small top-level types.
### 10:33 — Board snapshot: VehicleTypes example completed

Durga Sir pauses for students to copy the full **`VehicleTypes`** board diagram from screen/snap. Checklist for the snapshot:

- Outer class: `VehicleTypes`
- Nested interface: `Vehicle` with `getNumberOfWheels()`
- Nested impl classes: `Bus` (6 wheels), `Auto` (3 wheels), plus room for more (`...`)
**Heading on board:** *Interface inside a class — if we require multiple implementations of an interface and all implementations are related to your particular class.*

Technology should be clear before moving to Case 3.

### 11:28 — Case 3: Interface inside interface

**Prior knowledge:** Already touched in earlier sessions (e.g. collections API).

**Canonical example — `java.util.Map` and `Map.Entry`:**

- A **map** is a group of **key–value pairs**.
- Each key–value pair is called **an entry**.
- Without an existing **map object**, there is no chance of an **entry** object existing on its own in the same sense — entry is always associated with a map.
- Therefore **`Entry` interface is defined inside `Map` interface**.
```java
interface Map<K, V> {
    // Each key-value pair is an Entry
    interface Entry<K, V> {
        K getKey();
        V getValue();
        V setValue(V value);
    }

    // map operations...
}
```

**Domain illustration (board):** `{1→3, 2→4, ...}` — each pair is an entry; entries don't stand alone without their map.

**Rule:** We can declare **interface inside interface** when the inner interface models a sub-concept that only makes sense in the context of the outer interface.

Board diagram label: **interface Map → within that → interface Entry**. Students asked to capture the diagram snap as well as code.

### 17:22 — Case 3 extended example: Outer / Inner interfaces

Durga Sir adds a second board example to derive **implementation independence** rules.

**Setup:**

- `Outer` interface → method `m1()`.
- `Inner` interface (nested in `Outer`) → method `m2()`.
**Critical rule (stated repeatedly):** Every interface present inside an interface is **always `public static`**, whether you declare those modifiers or not.

**Consequence 1:** When implementing **`Outer`**, you are **NOT** required to implement **`Inner`**. Inner is a static member of the outer interface — ignorable for outer implementors.

**Consequence 2:** When implementing **`Inner`** (via `Outer.Inner`), you are **NOT** required to implement **`Outer`**.

**Consequence 3:** Outer and inner can be implemented **independently**.

```java
interface Outer {
    void m1();

    interface Inner {
        void m2();
    }
}

class Test1 implements Outer {
    public void m1() {
        System.out.println("outer interface method implementation");
    }
    // No need to implement Inner or provide m2()
}

class Test2 implements Outer.Inner {
    public void m2() {
        System.out.println("inner interface method implementation");
    }
    // No need to implement Outer or provide m1()
}
```

**Calling from main:**

```java
class Test {
    public static void main(String[] args) {
        Test1 t1 = new Test1();
        t1.m1();   // prints outer interface method implementation

        Test2 t2 = new Test2();
        t2.m2();   // prints inner interface method implementation
    }
}
```

**Compile & run (board):** `javac Test.java` then `java Test`

**Prints:**

```java
outer interface method implementation
inner interface method implementation
```

**CE/prints annotated:** Both lines print as shown; no compile error despite each class implementing only one of the two nested interfaces.

### 23:08 — Live re-type on screen: Outer / Inner / Test1 / Test2 / Test

Sir rewrites the same example cleanly on screen before compile (ASR: *interface outer*, *Yaman/Yaman too* → **`m1`/`m2`**):

```java
interface Outer {
    void m1();

    interface Inner {
        void m2();
    }
}

class Test1 implements Outer {
    public void m1() {
        System.out.println("outer interface method implementation");
    }
}

class Test2 implements Outer.Inner {
    public void m2() {
        System.out.println("inner interface method implementation");
    }
}

class Test {
    public static void main(String[] args) {
        Test1 t1 = new Test1();
        t1.m1();

        Test2 t2 = new Test2();
        t2.m2();
    }
}
```

**Commands (board):** `javac Test.java` → `java Test`

**Prints:** `outer interface method implementation` then `inner interface method implementation`.

**First-case vs second-case call flow:**

- `t1.m1()` → outer interface method path.
- `t2.m2()` → inner interface method path (not `Outer` implementation).
### 24:51 — Nested interface modifier rule (formal)

**Board heading repeated many times:**

> *Every interface present inside interface is ***always public and static***, whether we are declaring or not.*

**Hence:**

- We can implement **inner interface directly** (e.g. `implements Outer.Inner`).
- When implementing **outer**, not required to implement **inner**.
- When implementing **inner**, not required to implement **outer**.
- We can implement outer and inner **independently**.
This mirrors the static nested class story: inner interface members are static; they don't require an implementing instance of the outer interface.

### 30:22 — Case 4: Class inside interface

**Last combination:** Class inside interface.

**When?** If the **functionality of a class is closely associated with an interface**, and you use that class **only within that interface's methods** (parameter type, return type, helper data holder), declare the class **inside the interface** for better modularity.

### 31:34 — Case 4 example A: EmailService + EmailDetails

**Scenario:**

- Interface: `EmailService` with method `sendMail(...)`.
- `EmailDetails` is needed **only** for `sendMail` and **only** for `EmailService`.
- Not used anywhere else in the application → declare **`EmailDetails` class inside `EmailService`**.
```java
interface EmailService {
    void sendMail(EmailDetails e);

    class EmailDetails {
        String toList;
        String ccList;
        String subject;
        String body;
        // ... other email fields as needed ...
    }
}
```

**Board theory notes:**

- Email details functionality required only for email service.
- Outside of that, not used anywhere else.
- Highly recommended to declare class inside interface in such cases.
- Common triggers: **method argument is a class**, or **return type is a class** — define that helper class nested in the interface.
**In the above example:** EmailDetails is required **only for EmailService**; not using it elsewhere → nested declaration is the right design.

### 35:38 — EmailService board completion

Full board layout (ASR: *toList*, *CC list*, *subject*, *body*):

```java
interface EmailService {
    void sendMail(EmailDetails e);

    class EmailDetails {
        String toList;
        String ccList;
        String subject;
        String body;
    }
}
```

**Theory lines written:** If functionality of a class is closely associated with the interface → **highly recommended** to declare class inside interface. Modularity improves by keeping helper types colocated with the API that uses them.

No further explanation required once the association rule is understood.

### 38:01 — Case 4 example B: Default implementation class inside interface

**Second motivation for class inside interface:** Provide a **default implementation** of the interface.

- Some clients are happy with defaults → use the nested default class.
- Others want customization → provide their own implementing class.
**Analogy:** Like software asking "Do you want to proceed with **default settings**?" — default vs customized implementation.

```java
interface Vehicle {
    int getNumberOfWheels();

    // Default implementation — most vehicles expected to have 2 wheels (bike, car, cycle)
    class DefaultVehicle implements Vehicle {
        public int getNumberOfWheels() {
            return 2;
        }
    }
}

class Bus implements Vehicle {
    public int getNumberOfWheels() {
        return 6;   // customized — not satisfied with default 2
    }
}
```

**Main demo — using default vs custom:**

```java
class Test {
    public static void main(String[] args) {
        // Satisfied with default implementation
        Vehicle.DefaultVehicle d = new Vehicle.DefaultVehicle();
        System.out.println(d.getNumberOfWheels());   // 2

        // Not satisfied — use customized Bus
        Bus b = new Bus();
        System.out.println(b.getNumberOfWheels());   // 6
    }
}
```

**Compile & run (board):** `javac Test.java` → `java Test`

**Prints:**

```java
2
6
```

**CE/prints annotated:**

- `DefaultVehicle` → **2** (default two-wheeler assumption).
- `Bus` → **6** (custom implementation).
**Theory line:** We can also **define a class inside the interface to provide default implementation** for that interface.

**In the above example:** `DefaultVehicle` is the **default implementation** of the `Vehicle` interface.

### 44:52 — Second board pass: Vehicle / DefaultVehicle / Bus main

Sir rewrites the default-vs-custom example on screen for a final snap. Key instantiation line emphasized:

```java
Vehicle.DefaultVehicle d = new Vehicle.DefaultVehicle();
System.out.println(d.getNumberOfWheels());   // 2

Bus b = new Bus();
System.out.println(b.getNumberOfWheels());     // 6
```

Because nested classes in interfaces are **`public static`**, reference and construction use **`Vehicle.DefaultVehicle`** — no `Vehicle` instance needed.

### 46:04 — Execute Test.java: output 2 then 6

**Run:** `javac Test.java` → `java Test`

**Prints:**

```java
2
6
```

Students must internalize:

- **2** → default vehicle (two-wheeler common expectation: bike, car, cycle).
- **6** → customized `Bus` implementation.
Board theory after run: *Default vehicle is the default implementation of vehicle interface.*

### 50:37 — Class inside interface: always public static

**Extra note (board — take a note):**

> *The class which is declared inside interface is ***always public static***, whether we are declaring or not.*

**Why it matters:** You can create the nested class object **directly** without having an instance of the outer interface:

```java
Vehicle.DefaultVehicle d = new Vehicle.DefaultVehicle();   // valid
```

Same idea as static nested classes: no enclosing interface instance required.

Board phrasing: "Without having outer interface type object, directly we can create this class object" — as demonstrated with `DefaultVehicle d = new Vehicle.DefaultVehicle()`.

### 53:01 — Recap: all four combinations

| Case | Pattern | Example from session |
|---|---|---|
| 1 | Class inside class | University → Department |
| 2 | Interface inside class | VehicleTypes → Vehicle, Bus, Auto |
| 3 | Interface inside interface | Map → Entry; Outer → Inner |
| 4 | Class inside interface | EmailService → EmailDetails; Vehicle → DefaultVehicle |

### 53:33 — Conclusion 1: Anything inside anything

Durga Sir validates all four nesting directions with generic `A` / `B` placeholders:

| Outer | Inner | Valid? |
|---|---|---|
| class A | class B | Yes |
| class A | interface B | Yes |
| interface A | interface B | Yes |
| interface A | class B | Yes |

**Grand rule (board):** Among classes and interfaces, **we can declare anything inside anything** — all combinations are acceptable.

```java
class A {
    class B { }           // valid
    interface B { }        // valid — nested interface in class
}

interface A {
    interface B { }       // valid
    class B { }            // valid
}
```

### 56:09 — Conclusion 2: Modifier rules for nested types

Three formal conclusions to memorize for OCJP/SCJP and interviews:

#### (1) Interface declared inside interface

> *Always ***`public static`***, whether declared or not.*

- Must be accessible to implementation classes that need it.
- Enables direct `implements Outer.Inner`.
#### (2) Class declared inside interface

> *Always ***`public static`***, whether declared or not.*

- Enables direct instantiation: `Outer.NestedClass obj = new Outer.NestedClass();`
- No outer interface instance required.
#### (3) Interface declared inside class

> *Always ***`static`***, but ***need not be `public`***.*

- Can be **`private`** if the interface is needed only within that class.
- Unlike nested interfaces in interfaces, visibility can be restricted.
```java
class Container {
    private interface SecretHandler {
        void handle();
    }

    class Worker implements SecretHandler {
        public void handle() {
            System.out.println("private nested interface — static, scoped to Container");
        }
    }
}
```

**CE/prints:** `SecretHandler` is not API-visible outside `Container`; still **static** by rule. Contrast with `Map.Entry` which must be **`public static`**.

### 58:37 — Third conclusion restated: interface in class visibility

Sir repeats point 3 slowly for notes:

- Interface declared inside **class** → **always static**.
- **Need not be public** — **`private`** allowed when the nested interface is an internal implementation detail of the outer class only.
- Do **not** confuse with interface-in-interface (which is always **public static**).
**Summary table:**

| Nested type | Modifiers (implicit/default) |
|---|---|
| Interface in interface | always public static |
| Class in interface | always public static |
| Interface in class | always static; visibility can be private |

### 59:59 — Session closing

- These conclusions are **extra important** — minimal explanation needed if you already understand the four cases.
- Inner/nested class concept is among the **more difficult** areas in core Java; this session completes the combinations and modifier rules.
- **A-V-R** (be aware) of all points above for exams and interviews.
## Quick reference — when to use which nesting

| Pattern | Use when… |
|---|---|
| Class in class | Inner object cannot exist without outer (Department/University) |
| Interface in class | Several interface impls belong only to one outer class (VehicleTypes) |
| Interface in interface | Sub-concept only meaningful inside outer API (Map.Entry) |
| Class in interface | Helper/default class tied only to that interface (EmailDetails, DefaultVehicle) |

## Interview cheat sheet

1. **Can X go inside Y?** → Yes for all four class/interface pairings.
1. **Interface in interface modifiers?** → Always `public static`.
1. **Class in interface modifiers?** → Always `public static`; instantiate as `Iface.Nested`.
1. **Interface in class modifiers?** → Always `static`; can be `private`.
1. **Implement Outer but not Inner?** → Allowed; inner is static and independent.
1. **Implement Inner but not Outer?** → Allowed; use `implements Outer.Inner`.
1. **Class in interface — two reasons?** → (a) helper/parameter class used only there; (b) default implementation class.
**Java code block count: 15**
