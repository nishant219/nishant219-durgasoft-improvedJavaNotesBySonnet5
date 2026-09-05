# Video 127

## Video info

Title: Core Java With OCJP/SCJP: Serialization Part- 3||Customized serialization - 1

### 00:05 — Introduction: Customized Serialization

Next topic: Customized Serialization — Durga Sir calls this the most difficult topic in the entire serialization unit. Students must pay very careful attention.

Flow of this lecture:

- What is the need/purpose of customized serialization?
- How to implement it (covered in this video — Part 1).
### 00:32 — Problem setup: Account class with sensitive password

```java
class Account implements Serializable {
    String username = "Durga";
    transient String password = "Anushka";   // secured field — must be transient
}
```

Fields:

- username — normal String, serialized by default.
- password — secured field; must be declared `transient` so JVM does not write the real value to the file.
Account object created:

Account a1 = new Account();
System.out.println(a1.username + "..." + a1.password);
// CE/print (before serialization): Durga...Anushka

### 03:49 — Default serialization of Account

```java
FileOutputStream fos = new FileOutputStream("abc.ser");
ObjectOutputStream oos = new ObjectOutputStream(fos);
oos.writeObject(a1);
```

What goes into file `abc.ser`:

Transient rule (repeated): At serialization time, JVM ignores the original value of a transient variable and saves the default value (null for String) to the file.

### 05:07 — Default deserialization: password lost

FileInputStream fis = new FileInputStream("abc.ser");
ObjectInputStream ois = new ObjectInputStream(fis);
Account a2 = (Account) ois.readObject();

System.out.println(a2.username + "..." + a2.password);
// CE/print (after deserialization): Durga...null

Before serialization: username = Durga, password = Anushka ✓

After deserialization: username = Durga, password = null ✗

Why null instead of Anushka? Because password was declared `transient`.

### 06:37 — Core problem: loss of information

During default serialization, there may be a chance of loss of information because of the `transient` keyword.

- Before serialization: account object provides proper username and password.
- After deserialization: account object provides only username, not password.
Practical concern: Without the password, how can the receiver use the account information? The data is incomplete.

Solution: Customized serialization — to recover loss of information caused by the transient keyword.

### 08:47 — Purpose of customized serialization (summary)

Purpose of customized serialization: To recover loss of information which happened because of the transient keyword.

Password is transient → file contains null only → but receiver must get "Anushka" back. Some extra work/magic is required — that magic is customized serialization.

### 08:59 — Live demo: `CustSerializeDemo.java` (problem only)

Durga Sir runs the program without customized methods:

```java
// CustSerializeDemo.java — default serialization only
class Account implements Serializable {
    String username = "Durga";
    transient String password = "Anushka";
}

class CustSerializeDemo {
    public static void main(String[] args) throws Exception {
        Account a1 = new Account();
        System.out.println(a1.username + "..." + a1.password);
        // 1st print: Durga...Anushka

        FileOutputStream fos = new FileOutputStream("abc.ser");
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(a1);

        FileInputStream fis = new FileInputStream("abc.ser");
        ObjectInputStream ois = new ObjectInputStream(fis);
        Account a2 = (Account) ois.readObject();
        System.out.println(a2.username + "..." + a2.password);
        // 2nd print: Durga...null
    }
}
```

CE/print output:

Durga...Anushka    ← before serialization
Durga...null       ← after deserialization (password lost)

### 11:30 — Board theory (default serialization loss)

During default serialization, there may be a chance of loss of information because of transient keyword.

To recover this loss of information, we should go for customized serialization.

Diagram to copy:

Account object (before)  → username: Durga, password: Anushka
         ↓ serialize
File abc.ser             → username: Durga, password: null
         ↓ deserialize
Account object (after)   → username: Durga, password: null

### 17:42 — Extended board notes (before/after)

In the above example, before serialization account object can provide proper username and password. But after deserialization account object can provide only username but not password. This is due to declaring password variable as transient.

Hence during default serialization there may be a chance of loss of information because of transient keyword. To recover this loss of information we should go for customized serialization.

### 21:41 — Analogy: mango box and money (sender/receiver extra work)

Durga Sir explains customized serialization through a real-life story (copy-paste legend):

Problem: Need to send money (3 lakhs, later 7 lakhs) to native place via cousin Srinu (Shuu) who travels every weekend. Srinu refuses to carry money/gold directly — security risk; if money is misplaced during overnight bus travel, he would be responsible.

First attempt (3 lakhs): Srinu rejected carrying money outright. Father had to come personally to collect.

Second attempt (7 lakhs) — customized approach:

- Sender side (Durga Sir): Put 7 lakhs in a pot cover (polythene sheet) at the bottom of a box of mangoes. Pack mangoes neatly on top. Tell Srinu it is a box of mangoes for mother — he can verify by opening (shows real mangoes), then repack carefully.
- Transit: Srinu carries box (thinks mangoes only) — no security objection.
- Receiver side (father): At bus stop, receives box. Opens it, throws mangoes aside, unwraps polythene layers, gets the money.
Mapping to customized serialization:

At sender side and receiver side, if we do some extra work, then we can recover loss of information. The extra work itself is customized serialization.

Key idea: Don't send sensitive data directly; do extra work on both sides to hide/recover it.

### 34:53 — Mapping analogy to Account serialization logic

Missing data during default serialization: password (because transient).

Extra work at serialization (sender side):

- Read the password manually.
- Prepare encrypted password — e.g., "123" + originalPassword → "123Anushka".
- Write encrypted password manually to the file (as a separate object).
Extra work at deserialization (receiver side):

- Read the encrypted password from file.
- Perform decryption — reverse the modification (remove "123" prefix via substring(3)).
- Assign decrypted value to the original password field.
### 38:18 — Two methods for customized serialization

Customized serialization is implemented using two methods (exact signatures are critical):

Method 1 — serialization hook:

```java
private void writeObject(ObjectOutputStream oos) throws Exception {
    // extra work at serialization time
}
```

Method 2 — deserialization hook:

```java
private void readObject(ObjectInputStream ois) throws Exception {
    // extra work at deserialization time
}
```

Execution rules:

- writeObject → executed automatically by JVM at serialization time.
- readObject → executed automatically by JVM at deserialization time.
- Programmer writes these methods but never calls them directly — JVM invokes them.
Board note:

We can implement customized serialization by using the following two methods:

1. private void writeObject(ObjectOutputStream oos) throws Exception

2. private void readObject(ObjectInputStream ois) throws Exception

`writeObject` — executed automatically at the time of serialization. Hence if we want to perform any activity at serialization time, define it in this method only.

`readObject` — executed automatically at the time of deserialization. Hence if we want to perform any activity at deserialization time, define it in this method only.

### 47:09 — Callback methods

Because JVM executes these methods automatically (programmer does not call them), they are callback methods.

Other callback method examples:

- main method — JVM calls it.
- Servlet lifecycle methods (init, service, destroy) — container calls them automatically.
Note: The above methods are callback methods because these are executed automatically by the JVM.

### 48:57 — Where to define these methods: corresponding class

Two classes in the example:

- Account — the data class being serialized.
- CustSerializeDemo — demo/main class.
Question: Where must writeObject and readObject be placed?

Answer: In the corresponding class — the class of the object being serialized.

While performing which object serialization we have to do extra work, in the corresponding class we have to define above methods.

For Account object serialization → define methods inside `Account` class, NOT in CustSerializeDemo.

Example rule: For Dog object customized serialization → methods go in Dog class.

### 52:47 — Extra work recap before coding

### 53:17 — Full implementation: Account with customized serialization

```java
import java.io.*;

class Account implements Serializable {
    String username = "Durga";
    transient String password = "Anushka";

    // Callback — JVM calls automatically during serialization
    private void writeObject(ObjectOutputStream oos) throws Exception {
        // Step 1: default serialization (username → file; transient password → null in file)
        oos.defaultWriteObject();

        // Step 2: extra work — encrypt and write password manually
        String ePassword = "123" + password;   // "123Anushka"
        oos.writeObject(ePassword);              // write encrypted password as separate object
    }

    // Callback — JVM calls automatically during deserialization
    private void readObject(ObjectInputStream ois) throws Exception {
        // Step 1: default deserialization (username restored; password → null)
        ois.defaultReadObject();

        // Step 2: extra work — read, decrypt, assign
        String ePassword = (String) ois.readObject();   // read "123Anushka"
        password = ePassword.substring(3);               // decrypt → "Anushka"
    }
}
```

Demo class:

```java
class CustSerializeDemo1 {
    public static void main(String[] args) throws Exception {
        Account a1 = new Account();
        System.out.println(a1.username + "..." + a1.password);
        // CE/print: Durga...Anushka

        FileOutputStream fos = new FileOutputStream("abc.ser");
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(a1);

        FileInputStream fis = new FileInputStream("abc.ser");
        ObjectInputStream ois = new ObjectInputStream(fis);
        Account a2 = (Account) ois.readObject();
        System.out.println(a2.username + "..." + a2.password);
        // CE/print (with customized methods): Durga...Anushka
    }
}
```

### 57:19 — JVM flow during serialization of Account

When oos.writeObject(a1) is called:

- JVM checks: does Account class contain writeObject method?
- Yes → JVM is happy; programmer takes responsibility. JVM executes writeObject automatically.
- Inside writeObject:
- oos.defaultWriteObject() → performs default serialization (username written; transient password → null in stream).
- Then manual extra work: encrypt password, oos.writeObject(ePassword).
Critical line — default serialization inside custom hook:

oos.defaultWriteObject();   // default serialization

Without this line, even username would not be serialized by default mechanism.

### 1:00:50 — Encryption step detail

String ePassword = "123" + password;   // "123" + "Anushka" = "123Anushka"
oos.writeObject(ePassword);             // manually write encrypted form to file

File now contains: default-serialized Account state (username=Durga, password=null in default part) plus separate encrypted password object "123Anushka".

### 1:02:48 — JVM flow during deserialization

When ois.readObject() is called for Account:

- JVM checks: does Account class contain readObject method?
- Yes → JVM executes readObject automatically.
- Inside readObject:
- ois.defaultReadObject() → default deserialization (username=Durga, password=null).
- Read encrypted password: (String) ois.readObject() → "123Anushka".
- Decrypt: ePassword.substring(3) → removes first 3 chars "123" → "Anushka".
- Assign: password = "Anushka".
Critical line — default deserialization inside custom hook:

ois.defaultReadObject();   // default deserialization

After default step: a2.username = "Durga", a2.password = null.

After extra work: a2.password = "Anushka".

CE/print (final): Durga...Anushka — both before and after serialization.

### 1:05:47 — Decryption with substring

String ePassword = (String) ois.readObject();   // "123Anushka"
password = ePassword.substring(3);               // index 3 to end → "Anushka"

substring(3) removes characters at index 0, 1, 2 ("123") and returns from index 3 onward.

### 1:08:56 — Experiment: comment out both methods → back to default

If writeObject and readObject are commented out:

```java
// private void writeObject(...) { ... }
// private void readObject(...) { ... }
```

→ Behavior reverts to default serialization.

CE/print: Durga...Anushka then Durga...null.

If comments removed (customized methods active):

CE/print: Durga...Anushka then Durga...Anushka.

### 1:09:39 — Live execution: `CustSerializeDemo1.java`

Durga Sir runs on screen:

With methods commented:

Durga...Anushka
Durga...null

With methods active:

Durga...Anushka
Durga...Anushka

Confirms customized serialization recovers the transient password.

### 1:13:09 — account.class must exist at both sender and receiver

Both writeObject (encryption at sender) and readObject (decryption at receiver) live in Account class. Therefore `Account.class` must be available at both sender side and receiver side from the beginning. Encryption and decryption cannot be written separately in different classes — they are paired inside the same serializable class.

### 1:14:04 — Private methods: programmer vs JVM

- Programmer cannot call private methods from outside the class.
- JVM can call private methods from outside the class — this special ability is required for customized serialization to work.
Programmer can't call private methods directly from outside of the class, but JVM can call private methods directly from outside of the class.

If JVM could not call private methods, customized serialization would be impossible.

### 1:23:16 — Access modifier must be exactly `private`

Critical rule: Methods must be `private`. If you mistakenly use public or protected instead of private, the program will not work — JVM only recognizes the specific private signature form.

```java
// CORRECT — JVM recognizes this
private void writeObject(ObjectOutputStream oos) throws Exception { ... }
private void readObject(ObjectInputStream ois) throws Exception { ... }

// WRONG — no guarantee JVM will invoke these
public void writeObject(ObjectOutputStream oos) throws Exception { ... }
```

### 1:17:41 — Local variable naming note

ePassword is just a local variable name inside the methods — any name works (ePassword1, x, etc.). It has no special JVM meaning; Durga Sir uses it as a meaningful name for "encrypted password."

### 1:19:14 — Highlight key lines in notes

Students should highlight these two lines in their notes:

oos.defaultWriteObject();   // ← default serialization (inside writeObject)
ois.defaultReadObject();    // ← default deserialization (inside readObject)

These perform the normal/default part; the surrounding code is the extra/custom part.

### 1:20:01 — Output comparison diagram

### 1:22:01 — Final theory note (with customized serialization)

In the above program, before serialization and after serialization (with customized methods active), account object can provide proper username and password.

### 1:24:39 — Video conclusion (Part 1 of customized serialization)

Topics covered:

- Need: recover information lost due to transient keyword during default serialization.
- Analogy: sender/receiver extra work (mango box / money).
- Implementation: two callback methods — writeObject and readObject — defined as `private` in the corresponding class.
- Default hooks: defaultWriteObject() and defaultReadObject() preserve normal serialization behavior alongside custom extra work.
- Example: encrypt password as "123" + password on write; read and substring(3) on read.
- JVM invokes private methods automatically; programmer never calls them directly.
(Part 2 of customized serialization — if any — would be in the next video in the playlist.)

Java code block count: 16

## Tables (placement lost -- re-place these in context)

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP |
| Position | 127 of 203 |
| Series | Serialization |
| Topic | Customized serialization — Part 1 (need, writeObject / readObject, transient recovery) |
| Instructor | Durga Sir |
| Duration | 1h 24m 57s |
| Video ID | XmC4bzCDSHc |
| Watch | https://www.youtube.com/watch?v=XmC4bzCDSHc |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

| Field | Value in file |
|---|---|
| username | "Durga" |
| password | null (default value — transient field ignored) |

| Real life | Serialization |
|---|---|
| Money (sensitive) | transient password (not sent directly) |
| Box of mangoes (cover) | Encrypted password written manually to file |
| Sender extra work (hide money in mangoes) | Extra work at serialization time |
| Receiver extra work (unwrap to get money) | Extra work at deserialization time |
| Recover lost information | Recover password despite transient |

| Phase | Extra work |
|---|---|
| Serialization | Prepare encrypted password ("123" + password); write encrypted password to file |
| Deserialization | Read encrypted password; perform decryption (substring(3)); assign to password field |

| Scenario | 1st print (before) | 2nd print (after deserialize) |
|---|---|---|
| Default serialization | Durga...Anushka | Durga...null |
| Customized serialization | Durga...Anushka | Durga...Anushka |
