# Video 128

## Video info

Title: Core Java With OCJP/SCJP: Serialization Part- 4||Customized serialization - 2

### 00:06 — Recap: one transient vs multiple transient fields

In Video 127 (Part 1), the Account class had only one transient variable — password. Customized serialization recovered that single secured field after default serialization wrote null to the file.

New requirement in this video: Assume more than one transient (secured) field exists — e.g., password and ATM card pinNumber. Both must remain transient (never written to the file in plain form), yet the receiver must get the original values back after deserialization.

Core question Durga Sir poses: If more than one transient variable is present, how do we handle customized serialization for all of them?

This video uses almost the same example as Part 1 — the only extra piece is the additional secured field (pinNumber). Focus on understanding the flow, not memorizing variable names.

### 01:11 — Problem setup: Account with username, password, and pin

```java
class Account implements Serializable {
    String username = "Durga";
    transient String password = "Anushka";   // secured — must not appear in file as-is
    transient int pinNumber = 1234;          // secured — must not appear in file as-is
}
```

Field count: 3 fields total — username, password, pinNumber.

Secured fields: password and pinNumber — you should not write these anywhere in plain text during serialization.

Normal field: username — serialized by default (no transient).

Create and print before serialization:

Account a1 = new Account();
System.out.println(a1.username + "..." + a1.password + "..." + a1.pinNumber);
// Output: Durga...Anushka...1234

### 04:11 — Default serialization behavior (without customized methods)

```java
FileOutputStream fos = new FileOutputStream("abc.ser");
ObjectOutputStream oos = new ObjectOutputStream(fos);
oos.writeObject(a1);
```

What goes into the file with default serialization only:

Requirement: The receiver should get original values (Anushka, 1234) even though both secured fields are transient. That is exactly what customized serialization achieves.

### 04:52 — JVM checks for `writeObject` in Account class

When oos.writeObject(a1) is called:

- JVM checks: does Account class contain a writeObject method?
- Yes → JVM is happy — programmer is doing customized serialization.
- JVM automatically executes writeObject on the Account object (never called by programmer directly).
The ObjectOutputStream (oos) passed as the argument to writeObject is the same stream pointing to the file — so anything written inside writeObject goes to the same .ser file.

### 05:05 — Full `writeObject` implementation (serialization side)

```java
private void writeObject(ObjectOutputStream oos) throws Exception {
    // Step 1: default serialization
    oos.defaultWriteObject();

    // Step 2: extra work — encrypt and write password manually
    String ePassword = "123" + password;   // "123" + "Anushka" = "123Anushka"
    oos.writeObject(ePassword);            // String is an object → writeObject

    // Step 3: extra work — encrypt and write pin manually
    int ePin = 4444 + pinNumber;           // 4444 + 1234 = 5678
    oos.writeInt(ePin);                    // int is primitive → writeInt
}
```

Step-by-step breakdown:

#### Step 1 — `oos.defaultWriteObject()`

Performs default serialization for all non-transient fields and writes default values for transient fields.

After this line, the file contains:

- username = Durga
- password = null (transient default)
- pinNumber = 0 (transient default)
Highlight this line: oos.defaultWriteObject(); — default serialization inside the custom hook.

#### Step 2 — Encrypt and write password

String ePassword = "123" + password;   // prepend "123" as simple encryption
oos.writeObject(ePassword);            // writes "123Anushka" as a separate object in stream

Encryption rule (same as Video 127): prepend "123" to the original password.

#### Step 3 — Encrypt and write pin number

int ePin = 4444 + pinNumber;   // add 4444 to original pin as simple encryption
oos.writeInt(ePin);            // writes 5678 (4444 + 1234) to stream

Encryption rule for pin: add 4444 to the original pin value.

Important: Password uses writeObject (String is an object). Pin uses writeInt (int is a primitive). This distinction is critical — covered again at end of video.

File contents after complete `writeObject`:

- Default-serialized Account state (username=Durga, password=null, pinNumber=0 in default part)
- Encrypted password object: "123Anushka"
- Encrypted pin primitive: 5678
### 09:55 — Serialization complete; move to deserialization

After writeObject finishes, serialization is done. Deserialization side uses readObject.

### 10:06 — Deserialization setup

```java
FileInputStream fis = new FileInputStream("abc.ser");
ObjectInputStream ois = new ObjectInputStream(fis);
Account a2 = (Account) ois.readObject();
```

When ois.readObject() is called for Account:

- JVM checks: does Account class contain a readObject method?
- Yes → JVM automatically executes readObject.
- Programmer never calls readObject directly — JVM invokes it as a callback.
### 10:55 — Full `readObject` implementation (deserialization side)

```java
private void readObject(ObjectInputStream ois) throws Exception {
    // Step 1: default deserialization
    ois.defaultReadObject();

    // Step 2: read encrypted password (must match write order — password was written FIRST)
    String ePassword = (String) ois.readObject();

    // Step 3: decrypt password and assign to original field
    password = ePassword.substring(3);   // remove "123" prefix → "Anushka"

    // Step 4: read encrypted pin (written SECOND — read SECOND)
    int ePin = ois.readInt();

    // Step 5: decrypt pin and assign to original field
    pinNumber = ePin - 4444;             // 5678 - 4444 = 1234
}
```

Step-by-step breakdown:

#### Step 1 — `ois.defaultReadObject()`

Performs default deserialization.

After this line, a2 object state:

- username = Durga
- password = null
- pinNumber = 0
Highlight this line: ois.defaultReadObject(); — default deserialization inside the custom hook.

#### Step 2 & 3 — Read and decrypt password

String ePassword = (String) ois.readObject();   // reads "123Anushka"
password = ePassword.substring(3);               // index 3 to end → "Anushka"

substring(3) removes characters at index 0, 1, 2 ("123") and returns from index 3 onward.

#### Step 4 & 5 — Read and decrypt pin

int ePin = ois.readInt();       // reads 5678
pinNumber = ePin - 4444;        // 5678 - 4444 = 1234

Reverse the encryption: subtract the same 4444 that was added during serialization.

### 12:45 — CRITICAL RULE: Read order must match write order

During serialization (writeObject), extra data was written in this order:

- Encrypted password (oos.writeObject(ePassword)) — first
- Encrypted pin (oos.writeInt(ePin)) — second
During deserialization (readObject), you must read in the exact same order:

- Read encrypted password — first
- Read encrypted pin — second
If you swap the read order, the program will fail or produce wrong values. Durga Sir emphasizes: "In which order we have to read it, make sure this one is very important."

### 15:35 — Final output after customized serialization

System.out.println(a2.username + "..." + a2.password + "..." + a2.pinNumber);
// Output: Durga...Anushka...1234

Comparison:

No loss of information. Before serialization and after deserialization, the account object provides the same complete information.

This is the entire purpose of customized serialization — recover data that would otherwise be lost because of the transient keyword.

### 16:18 — Live demo: `CustSerializeDemo2.java`

Durga Sir executes the program on screen.

Complete program:

```java
import java.io.*;

class Account implements Serializable {
    String username = "Durga";
    transient String password = "Anushka";
    transient int pinNumber = 1234;

    private void writeObject(ObjectOutputStream oos) throws Exception {
        oos.defaultWriteObject();              // default serialization
        String ePassword = "123" + password;   // prepare encrypted password
        int ePin = 4444 + pinNumber;           // prepare encrypted pin
        oos.writeObject(ePassword);            // write encrypted password
        oos.writeInt(ePin);                    // write encrypted pin
    }

    private void readObject(ObjectInputStream ois) throws Exception {
        ois.defaultReadObject();               // default deserialization
        String ePassword = (String) ois.readObject();  // read encrypted password
        password = ePassword.substring(3);     // assign decrypted password
        int ePin = ois.readInt();              // read encrypted pin
        pinNumber = ePin - 4444;               // assign decrypted pin
    }
}

class CustSerializeDemo2 {
    public static void main(String[] args) throws Exception {
        Account a1 = new Account();
        System.out.println(a1.username + "..." + a1.password + "..." + a1.pinNumber);
        // 1st print: Durga...Anushka...1234

        FileOutputStream fos = new FileOutputStream("abc.ser");
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(a1);

        FileInputStream fis = new FileInputStream("abc.ser");
        ObjectInputStream ois = new ObjectInputStream(fis);
        Account a2 = (Account) ois.readObject();
        System.out.println(a2.username + "..." + a2.password + "..." + a2.pinNumber);
        // 2nd print (with customized methods): Durga...Anushka...1234
    }
}
```

### 17:15 — Experiment: comment out both customized methods

If writeObject and readObject are commented out, behavior reverts to default serialization:

```java
// private void writeObject(ObjectOutputStream oos) throws Exception { ... }
// private void readObject(ObjectInputStream ois) throws Exception { ... }
```

Output:

Durga...Anushka...1234    ← 1st print (before serialization — in-memory object)
Durga...null...0          ← 2nd print (after deserialization — password=null, pin=0)

Both secured fields are lost: password becomes null, pinNumber becomes 0.

When comments are removed (customized methods active):

Durga...Anushka...1234    ← 1st print
Durga...Anushka...1234    ← 2nd print — no loss of information

Durga Sir confirms on screen: first run without methods → Durga null 0; with methods restored → Durga Anushka 1234 both times.

### 18:16 — Purpose recap: why customized serialization?

How this works is not magic — it is customized serialization.

What customized serialization lets you do:

- Declare sensitive fields as transient (so default serialization does not expose real values in the file).
- Still recover the original values at deserialization time by doing extra work on both sender and receiver sides.
Part 1 (Video 127): One transient field (password).

Part 2 (this video): Multiple transient fields (password + pinNumber) — same pattern, repeated for each secured field, with correct read/write order.

### 20:53 — Second example on board (reinforcement)

Durga Sir writes a second Account example on the board with the same structure:

- String username = "Durga"
- transient String password (any name/value — e.g., Anushka)
- transient int pinNumber
Same writeObject / readObject logic. The concept does not change — only the number of secured fields increases.

### 21:01 — How JVM invokes `writeObject`: argument and target object

When oos.writeObject(a1) is called from main:

- The ObjectOutputStream (oos) passed to writeObject is the same stream that points to the file.
- JVM automatically calls writeObject on the Account object (a1) — because writeObject is defined in the Account class.
- The stream argument (oos) is forwarded by JVM as the method parameter.
Rule: writeObject and readObject must be defined in the corresponding class — the class of the object being serialized (Account), not in the demo/main class.

Access modifier: Methods should be `private`. JVM can invoke private methods from outside the class; the programmer cannot. This is required for the callback mechanism to work.

### 21:56 — Order of operations inside `writeObject`

Recommended order:

- First perform default serialization (defaultWriteObject).
- Then do extra manual work (encrypt and write secured fields).
Durga Sir notes: changing this order may or may not cause issues — safest and standard approach is default first, extra work second. Always follow the pattern shown.

### 23:55 — Wrapper / stream usage note

When writing encrypted data manually, use the same ObjectOutputStream instance (oos) that was passed into writeObject. Do not create a new stream. Whatever you write via oos.writeObject(...) or oos.writeInt(...) appends to the same serialized file stream.

### 26:18 — Most difficult concept in serialization

Durga Sir states clearly:

The most difficult concept in the entire serialization unit is customized serialization only.

By this point (Videos 127 + 128), students should feel that this topic demands the most careful attention in the whole serialization chapter.

### 27:23 — String vs int: `writeObject` vs `writeInt`

Critical distinction for OCJP:

Rule: For every primitive type, ObjectOutputStream / ObjectInputStream provide dedicated writeXxx / readXxx methods. For objects (like String), use writeObject / readObject.

That is why encrypted password uses writeObject (String is an object) and encrypted pin uses writeInt (int is a primitive).

### 28:01 — Video conclusion (Part 2 of customized serialization)

Topics covered in this video:

- Handling more than one transient (secured) field in customized serialization.
- Extended Account example: username + transient password + transient pinNumber.
- writeObject: defaultWriteObject() → encrypt password → writeObject(ePassword) → encrypt pin → writeInt(ePin).
- readObject: defaultReadObject() → read password → decrypt → read pin → decrypt.
- Read order must match write order — compulsory rule.
- String (object) vs int (primitive) — different stream methods.
- Live demo confirms: without customized methods → Durga...null...0; with methods → Durga...Anushka...1234.
- Customized serialization is the hardest topic in the serialization unit.
Connection to Video 127: Part 1 introduced the concept with one transient field. Part 2 extends the same pattern to multiple transient fields — the mechanism is identical, just repeated for each secured field with strict ordering.

## Summary tables

### Default vs customized serialization (multiple transient fields)

### File contents during customized serialization

### Encryption / decryption mapping

### Part 1 vs Part 2 comparison

## Metadata

## Tables (placement lost -- re-place these in context)

| Field | Value |
|---|---|
| username | Durga |
| password | Anushka |
| pinNumber | 1234 |

| Field | Value in file | Reason |
|---|---|---|
| username | Durga | Normal field — serialized as-is |
| password | null | transient → JVM ignores original value, writes default (null for String) |
| pinNumber | 0 | transient → JVM ignores original value, writes default (0 for int) |

| Write order (serialization) | Read order (deserialization) |
|---|---|
| 1. oos.writeObject(ePassword) | 1. (String) ois.readObject() |
| 2. oos.writeInt(ePin) | 2. ois.readInt() |

| Phase | username | password | pinNumber |
|---|---|---|---|
| Before serialization (a1) | Durga | Anushka | 1234 |
| After deserialization (a2) — with customized methods | Durga | Anushka | 1234 |

| Type | Category | Write method | Read method |
|---|---|---|---|
| String | Object (reference type) | oos.writeObject(str) | (String) ois.readObject() |
| int | Primitive | oos.writeInt(n) | ois.readInt() |
| float | Primitive | oos.writeFloat(f) | ois.readFloat() |
| double | Primitive | oos.writeDouble(d) | ois.readDouble() |
| boolean | Primitive | oos.writeBoolean(b) | ois.readBoolean() |
| long | Primitive | oos.writeLong(l) | ois.readLong() |

| Scenario | 1st print (before) | 2nd print (after deserialize) |
|---|---|---|
| Default serialization (no custom methods) | Durga...Anushka...1234 | Durga...null...0 |
| Customized serialization (with custom methods) | Durga...Anushka...1234 | Durga...Anushka...1234 |

| Data in stream | Value | How written |
|---|---|---|
| Default Account state | username=Durga, password=null, pin=0 | oos.defaultWriteObject() |
| Encrypted password | "123Anushka" | oos.writeObject(ePassword) |
| Encrypted pin | 5678 | oos.writeInt(ePin) |

| Field | Encryption (write) | Decryption (read) |
|---|---|---|
| password (String) | "123" + password | ePassword.substring(3) |
| pinNumber (int) | 4444 + pinNumber | ePin - 4444 |

| Aspect | Video 127 (Part 1) | Video 128 (Part 2) |
|---|---|---|
| Transient fields | 1 (password) | 2 (password, pinNumber) |
| Extra writes in writeObject | 1 (writeObject for password) | 2 (writeObject + writeInt) |
| Extra reads in readObject | 1 (readObject for password) | 2 (readObject + readInt) |
| Read order rule | N/A (only one) | Critical — must match write order |
| Core mechanism | Same | Same — extended |

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP |
| Position | 128 of 203 |
| Series | Serialization |
| Topic | Customized serialization — Part 2 (multiple transient fields, writeInt/readInt, read order) |
| Instructor | Durga Sir |
| Duration | 28m 27s |
| Video ID | lVIl3wx67ds |
| Watch | https://www.youtube.com/watch?v=lVIl3wx67ds |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Prerequisites | Video 127 — Customized serialization Part 1 |
| Java code block count | 8 |
