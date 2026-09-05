# Video 001 — Foundation of Spring Boot

## Video info

| Field | Detail |
|---|---|
| Playlist | Chai aur Spring Boot |
| Position | Video 1 of 4 |
| Topic | Why backend frameworks exist, Spring Boot project setup, Spring Core (IoC/DI/beans), Spring Boot's internal startup pipeline, Spring MVC request flow |
| Instructor | Aniket (Chai aur Code) |
| Duration | 1h 56m 47s |
| Watch | https://www.youtube.com/watch?v=16X0rONMaWQ |
| Playlist | https://www.youtube.com/playlist?list=PLAtsKd9vhf5M |

> **How to read these notes.** Sections follow the lecture's own timestamps and
> are cleaned up from a raw auto-caption transcript, not a literal transcript.
> **📌 Beyond the lecture** boxes add context the video doesn't cover but you'll
> want as you start real Spring Boot work. **⚠️ Nuance** boxes flag a spot
> where the lecture simplifies something worth knowing precisely. **🟨 Coming
> from JS?** boxes map the concept onto Node.js/Express (and NestJS, where
> relevant) since that's the background this reader is coming from.

## What this lecture covers

This is the first of a 4-video series. The whole series:

1. Foundation of Spring Boot ← *this video*
2. Building REST APIs and database connectivity (Spring Data JPA)
3. Security in Spring Boot
4. Production concerns — Redis, microservices, Kafka

This video itself covers, in order:

1. What Spring Boot is and why backend frameworks exist at all
2. Why Spring was created, and what it fixed
3. Why Spring Boot was created on top of Spring, and what *it* fixed
4. Prerequisites (Java, OOP, collections, exceptions)
5. Installing IntelliJ IDEA
6. Generating a project with Spring Initializr and understanding every field
7. Project structure, running the app, and a first `@RestController` endpoint
8. Spring Core: IoC, the IoC container, beans, dependency injection
9. Choosing between multiple bean implementations (`@Qualifier`, `@Primary`, `@Profile`, `@ConditionalOnProperty`)
10. Bean scopes and the bean lifecycle
11. Externalizing configuration (`@Value`, `@ConfigurationProperties`)
12. What actually happens inside `SpringApplication.run()` — auto-configuration internals
13. How an HTTP request flows through Spring MVC, end to end

---

## Coming from JavaScript/Node.js? Quick orientation

| Node.js / Express concept | Spring Boot equivalent | Notes |
|---|---|---|
| `npm` / `package.json` | Maven (`pom.xml`) or Gradle (`build.gradle`) | Both declare dependencies and build/run commands |
| `npm install <pkg>` | Add a dependency line to `pom.xml` (or pick a starter in Spring Initializr) | No manual install step — Maven resolves and downloads on build |
| `node_modules/` (per project) | Local Maven repo `~/.m2/repository` (shared across all your projects) | Different caching model, same idea |
| `express()` + `app.listen(3000)` | `@SpringBootApplication` + `SpringApplication.run(...)` | Both boot an HTTP server; Spring Boot's default port is **8080**, not 3000 |
| `app.get('/hello', (req, res) => ...)` | `@GetMapping("/hello")` inside a `@RestController` | Express: one function per route. Spring: an annotated method, discovered automatically |
| Express middleware (`app.use`, `next()`) | `DispatcherServlet` + filters/interceptors | Same chain-of-responsibility idea, different names |
| `req.body`, `req.params`, `req.query` | `@RequestBody`, `@PathVariable`, `@RequestParam` | Spring binds these as method parameters instead of one `req` object |
| `res.json(data)` | `return data;` from a `@RestController` method | Spring auto-converts the return value to JSON via Jackson |
| `.env` + `dotenv` | `application.properties` / `application.yml` | Same idea: environment config kept outside the code |
| `process.env.NODE_ENV` | Spring **profiles** (`spring.profiles.active`) | Both select environment-specific behavior |
| You `require()`/`import` and wire dependencies by hand | Spring's IoC container auto-wires dependencies for you | The single biggest conceptual difference — see the Spring Core section below |
| `module.exports = new Thing()` (singleton via `require` caching) | A `@Service`/`@Component` bean, default (singleton) scope | Similar end result, very different mechanism |
| Jest + Supertest | JUnit 5 + Mockito (unit), `@SpringBootTest` (integration) | Spring Boot ships test dependencies by default |
| Single-threaded event loop, non-blocking I/O | Thread-per-request, blocking I/O by default | The other big conceptual difference — its own section further down |
| TypeScript interfaces (compile-time only, erased at runtime) | Java interfaces (`interface Database { ... }`) | Java's interfaces exist at runtime and drive how Spring picks implementations |
| NestJS (`@Injectable()`, `@Controller()`, modules) | Spring Boot (`@Service`, `@RestController`, auto-configuration) | If you've touched NestJS, you've already seen Spring's ideas — Nest was explicitly modeled on Spring |

The single biggest mindset shift: **Express hands you a blank canvas and you
wire everything by hand; Spring Boot hands you a fully-wired application and
you customize pieces of it.** Where Express is minimal by design, Spring Boot
is deliberately "batteries included" — most of what looks like magic in this
video (auto-configuration, component scanning, dependency injection) exists
specifically to remove the manual wiring code you'd write in Express.

If you've used **NestJS**, most of Spring Core below will feel instantly
familiar — its decorators (`@Injectable()`, `@Controller()`, `@Module()`) and
its dependency-injection container are a deliberate, close copy of Spring's
model, brought to Node/TypeScript.

---

## 05:16 — What is Spring Boot?

> Spring Boot is an extension to the Spring Framework that makes backend
> development fast, easy, and low on configuration.

Spring Boot is **not** a replacement for Spring — it uses Spring internally.
The pitch: build a complete, production-ready backend in minutes instead of
hours.

## 05:57 — Life before backend frameworks

Before frameworks like Spring existed, Java backend development meant:

- **Servlets** and **JSP** (Java Server Pages) for handling web requests
- **JDBC** (raw `java.sql`) for database connectivity
- Application servers like **Tomcat** or **WebLogic** to run it all

Flow: browser → servlet → JDBC → database.

### 06:37 — What made this painful

| Problem | What it meant in practice |
|---|---|
| Heavy boilerplate | Every JDBC call meant open connection → create statement → execute query → handle result → close connection → handle exceptions, by hand, in every project |
| Tight coupling | `Database db = new MySQLDatabase();` scattered through the code — switching databases meant hunting down and editing every usage |
| No enforced structure | No standard for where request-handling logic vs. business logic vs. data access lived — every developer organized it differently |
| Manual configuration | Server behavior, servlet mappings, etc. lived in hand-edited XML (`web.xml`) — one typo and the server wouldn't start |
| Resource leaks | Forgetting to close a JDBC connection leaked memory |

Net effect: slow to build, hard to maintain, error-prone, and it didn't scale
across a team.

## 10:02 — Why Spring came, and what it fixed

Spring's core idea: simplify Java backend development by making it clean and
**loosely coupled**.

- **Dependency Injection (DI) / Inversion of Control (IoC)** — instead of your
  code doing `new MySQLDatabase()`, Spring hands the object to you already
  built. Easier to swap implementations, easier to test.
- **Spring JDBC / ORM support** — less boilerplate around JDBC, cleaner
  exception handling, good Hibernate/JPA integration.
- **Spring MVC** — introduced a clean split into **Controller → Service →
  Repository**, giving every team a structure to follow.

Result: Spring solved the boilerplate problem, the coupling problem, and the
structure problem, and became the standard for enterprise Java.

> ⚠️ **Nuance — "Spring fixed everything" undersells the JSR/servlet-spec side.**
> The video frames this purely as Spring vs. hand-rolled Servlets+JDBC. In
> reality Java EE (now **Jakarta EE**) also evolved its own answers in
> parallel — JPA, CDI, JAX-RS. Spring won the popularity contest for typical
> web/microservice backends, but Jakarta EE app servers are still very much
> alive in some enterprises (especially banking/insurance). Worth knowing the
> name exists if you ever inherit a Java EE codebase.

## 12:04 — Why Spring itself wasn't enough

Spring was powerful but not *easy*:

| Problem | Detail |
|---|---|
| Heavy configuration | Old-style Spring projects were full of XML: bean definitions, web configs, dispatcher-servlet setup |
| Hard setup | Manually download JARs, configure the server, hand-write `web.xml` |
| Version compatibility | Getting a working combination of library versions ("dependency hell") was its own project |
| Slow developer experience | Not friendly for beginners, and too slow for the rapid-setup expectations of startups/microservices |

## 13:43 — Why Spring Boot was created

Spring Boot's goal: make Spring itself easy. Zero or minimal configuration,
auto-configure everything possible, ship with sane production-ready defaults.

| Innovation | What it gives you |
|---|---|
| **Auto-configuration** | Spring Boot configures things (DB, web server, security, JSON handling) automatically based on which dependencies are on the classpath |
| **Starters** | A "starter" is a bundle of dependencies for one purpose — e.g. `spring-boot-starter-web` pulls in Spring MVC, embedded Tomcat, and Jackson (JSON) as one dependency instead of ten |
| **Embedded server** | No external Tomcat install needed — run `java -jar app.jar` and the server is inside the jar |
| **Production-ready features (Actuator)** | Health checks, metrics, and logs out of the box |

> 📌 **Beyond the lecture — what a "starter" actually is.**
> A starter has no code of its own; it's a Maven/Gradle POM whose only job is
> to declare a curated set of compatible dependency versions. `spring-boot-starter-web`
> transitively pulls in `spring-webmvc`, `spring-boot-starter-tomcat`,
> `spring-boot-starter-json` (Jackson), and `spring-boot-starter-logging`
> (Logback via SLF4J). This is also *how* Spring Boot solves the "version
> compatibility" pain point from the previous section — the Spring Boot
> **BOM** (Bill of Materials) pins one tested, mutually-compatible version for
> every library in the ecosystem, so you generally never specify a version
> number yourself; you just pick a Spring Boot version and starters inherit
> compatible versions.

## 16:01 — Why learn Spring Boot

Widely used in enterprise and cloud-native applications, across product
companies, service companies, and startups alike. A reasonable default choice
for backend Java work and a strong signal on a resume/interview.

## 16:35 — Prerequisites

Java is **non-negotiable** — the video is explicit that you should know it
before starting Spring Boot, or at minimum be comfortable with:

- OOP: classes, objects, inheritance, encapsulation, polymorphism, abstraction, interfaces
- Basic syntax: variables, methods, loops, conditionals
- Packages and access modifiers (`public`, `private`, `protected`)
- Exception handling: `try`/`catch`, custom exceptions
- The Collections framework: `List`, `Map`, `Set`

Reasons given: Spring uses interfaces heavily (you'll implement them
constantly), collections back most API request/response payloads, and
exception handling underlies how Spring reports errors.

## 18:24 — Installing IntelliJ IDEA

The IDE used throughout the series. Community Edition is free and sufficient
for this series; Ultimate adds paid extras (some companies provide Ultimate
licenses). As of the current download page, IntelliJ ships as a single
unified installer rather than two separate downloads — you install the same
product and Ultimate features unlock via trial or license.

> 📌 **Beyond the lecture — Community vs. Ultimate for Spring Boot, precisely.**
> Community Edition can run any Spring Boot app you build with Maven/Gradle —
> you lose nothing functionally. Ultimate adds IDE-level conveniences specific
> to Spring: a Spring-aware project view, endpoint navigation gutter icons for
> `@GetMapping`/`@PostMapping`, a "Beans" diagram, and database tooling. Nice
> to have, not required to follow this series or work productively.

---

## 20:26 — Generating a project with Spring Initializr

Spring Initializr (`start.spring.io`) is the standard way real Spring Boot
projects get bootstrapped — used directly on the website, or the same wizard
built into IntelliJ.

### Fields explained

| Field | What it means | What was chosen |
|---|---|---|
| **Project** | Build tool — Maven or Gradle | **Maven** — older, still the more common/widely-supported choice industry-wide; Gradle is newer and also good |
| **Language** | Java, Kotlin, or Groovy | **Java** — most Spring Boot work is Java; Kotlin is popular for Android, less so for typical Spring Boot shops |
| **Spring Boot version** | Pick a **stable** release, not one with `SNAPSHOT` or a milestone tag like `M1` | Latest stable |
| **Group** | Reverse-domain style organization identifier, e.g. `com.example` | `com.lets` (example org) |
| **Artifact** | The project's name — becomes the built jar's filename, e.g. `demo` → `demo.jar` | `demo` |
| **Name** / **Description** | Human-readable project name and a free-text description | — |
| **Package name** | Java package for your code — usually `group` + `artifact` combined | — |
| **Packaging** | `Jar` or `War` | **Jar** — the modern default; `War` was needed only when deploying to an external application server, which Spring Boot's embedded server makes largely unnecessary |
| **Java version** | Target JDK | **17** — Spring Boot 3.x requires Java 17 as a floor; 21 is also common |
| **Dependencies** | Starters to include | **Spring Web** (`spring-boot-starter-web`) |

> ⚠️ **Nuance — "Java version for Spring Boot 3 is 17 or 21" needs a floor, not a menu.**
> The video presents 17/21 as two options to pick between. More precisely:
> **Spring Boot 3.x requires Java 17 or newer** — 17 is the *minimum*, not an
> alternative to 21. You can run Spring Boot 3 on 17, 21, 23, 24, or 25; you
> cannot run it on Java 8 or 11 (that's Spring Boot 2.x territory, which is
> now out of OSS support). For a brand-new project in 2026, defaulting to the
> current LTS (21, with 25 also LTS and gaining adoption) rather than 17 is
> reasonable unless a company-mandated JDK says otherwise.

> 🟨 **Coming from JS?** `pom.xml` plays the role of `package.json`, but there's
> no `npm install` step you run yourself — Maven (or your IDE) resolves and
> downloads dependencies automatically on build, into a shared local cache
> (`~/.m2/repository`) rather than a per-project `node_modules/`. There's also
> no `npm run dev` with hot reload by default; the closer equivalent is the
> optional **Spring Boot DevTools** dependency, which restarts the app
> automatically on file changes.

Clicking **Generate** downloads a `.zip`; extract it, then open the extracted
folder in IntelliJ (rather than opening the zip directly, which can be
unreliable).

## 27:38 — Project structure

| Path | Purpose |
|---|---|
| `pom.xml` | Maven's build file — project metadata, Java version, and the dependency list (this is where `spring-boot-starter-web` and `spring-boot-starter-test` show up after generation) |
| `src/main/java/.../DemoApplication.java` | The main class, annotated `@SpringBootApplication` — where the app starts. **Must** stay in (or above) the root package, because Spring's component scanning starts here |
| `src/main/resources/application.properties` | Application configuration — port, app name, DB settings, etc. |
| `src/main/resources/static/` | Static frontend assets (HTML/CSS/JS/images) if you're serving them directly |
| `src/main/resources/templates/` | Server-side view templates (e.g. Thymeleaf) — noted as less common for modern API-first apps |
| `src/test/` | Unit/integration tests |
| External Libraries (IDE panel) | The actual jars resolved by Maven for your declared dependencies — e.g. `spring-webmvc`, `jackson-databind`, `mockito` |

Setting up the SDK: if IntelliJ shows no "Run" option, the **Project SDK**
isn't set. Fix via *Project Structure → SDK → Download JDK* (pick 17, any
vendor — Amazon Corretto, Temurin, etc. are all fine, since OpenJDK is open
source and multiple vendors build it).

> 🟨 **Coming from JS?** Map this onto a typical Express project:
> `DemoApplication.java` is your `server.js`/`app.js` entry point; a
> `controller/` package is your `routes/`; `application.properties` is your
> `.env`; `src/test/` is your `__tests__/`/`test/` folder. The biggest
> difference: Java requires the folder structure to exactly mirror the
> `package` declaration at the top of each file — you can't put a file
> anywhere and just `require()` it by relative path the way you can in Node.

## 31:45 — Running the app

Running the main class starts the embedded **Tomcat** server, by default on
**port 8080**. Hitting `http://localhost:8080/` with no mapping defined
returns Spring Boot's default "No mapping" error page — expected, since no
endpoint has been written yet.

## 34:38 — First endpoint

```java
package com.lets.demo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Hi this is Aniket";
    }
}
```

- `@RestController` marks the class as one that handles web requests and
  returns data directly (not a view name).
- `@GetMapping("/hello")` maps HTTP `GET /hello` to this method.

Hitting `http://localhost:8080/hello` in the browser now returns the string.
The video defers the deeper mechanics of `@GetMapping`/`@PostMapping`/etc. to
later in this same video (see the request-flow section) and to video 2 for
full REST API building.

> 🟨 **Coming from JS?** The Express equivalent of the whole snippet above:
> ```javascript
> const express = require('express');
> const app = express();
>
> app.get('/hello', (req, res) => {
>   res.send('Hi this is Aniket');
> });
>
> app.listen(8080);
> ```
> `@RestController` + `@GetMapping` together do what `app.get(path, handler)`
> does in one line in Express. The difference: Spring finds this method by
> **scanning annotations** across your whole codebase at startup, rather than
> you explicitly registering it yourself by calling `app.get(...)`.

---

## 38:09 — Spring Core: the goal is loose coupling

A second demo project (`spring-core-concepts`, Maven, Java 17, Spring Web
dependency) is used purely to teach Spring's core concepts, separate from the
REST-API demo above.

### 40:46 — The tight-coupling problem

```java
class UserService {
    void saveUser(String user) {
        MySQLDatabase db = new MySQLDatabase();
        db.saveToDb(user);
    }
}

class MySQLDatabase {
    void saveToDb(String user) {
        System.out.println("MySQL: saving user " + user);
    }
}
```

Calling `saveUser` works, but `UserService` is now hard-wired to
`MySQLDatabase`. Switching to Postgres or MongoDB means editing every place
`new MySQLDatabase()` appears. Consequences: hard to test (can't substitute a
fake database), hard to scale/maintain as the codebase grows.

### 45:29 — Introducing an interface

```java
interface Database {
    void save(String user);
}

class MySQLDatabase implements Database {
    @Override
    public void save(String user) {
        System.out.println("MySQL: saving user " + user);
    }
}

class PostgresDatabase implements Database {
    @Override
    public void save(String user) {
        System.out.println("Postgres: saving user " + user);
    }
}
```

`UserService` now depends on the `Database` **interface**, not a specific
class, and receives its dependency through the constructor instead of
creating it:

```java
class UserService {
    private final Database database;

    UserService(Database database) {
        this.database = database;
    }

    void saveUser(String user) {
        database.save(user);
    }
}
```

This *is* loose coupling — `UserService` no longer cares which database
implementation it's given. But one problem remains: **something still has to
call `new MySQLDatabase()`** and pass it in. In a real project with hundreds
of classes and thousands of dependencies, wiring all of that by hand becomes
its own mess.

### 51:19 — Inversion of Control (IoC)

> Spring says: give the responsibility of creating and connecting objects to
> me.

Before: your code controlled object creation (`new X()` everywhere). After:
Spring controls it, and hands objects to your code. The control has been
*inverted* — hence Inversion of Control.

### 52:22 — IoC Container / ApplicationContext

Also called the **Spring Container**, and closely tied to
`ApplicationContext`. It:

- Creates objects
- Stores them
- Injects them wherever needed
- Manages their lifecycle

Described as "a big box of ready-made objects" that hands you what you need.

> 🟨 **Coming from JS?** There's no equivalent to an IoC container in plain
> Node/Express — you `require()`/`import` a module and use it directly, and
> if module A needs module B, A imports B itself. Spring flips this: your
> class *declares* what it needs (as a constructor parameter) and never
> imports or constructs its dependency directly — the container looks at
> every class's declared needs and wires the whole dependency graph together
> at startup. If you've used **NestJS**, this is exactly its `@Injectable()` +
> constructor-injection model, borrowed directly from Spring.

### 52:57 — Beans

A **bean** is an object that Spring creates and manages. Not every object in
your app is a bean — only the ones Spring is told to manage.

### 53:52 — How Spring knows what to make into a bean: stereotype annotations

Spring scans your project for specific annotations:

| Annotation | Typical use | Functionally |
|---|---|---|
| `@Component` | Generic — any Spring-managed object | Base annotation |
| `@Service` | Business-logic layer | Meta-annotated with `@Component`; same mechanism, clearer semantics |
| `@Repository` | Data-access layer | Same mechanism as `@Component`; also enables Spring's automatic exception translation for persistence-layer exceptions |

The video is explicit: these are "almost the same" mechanically — they exist
for semantic clarity so a reader of the code immediately knows a class's
role. Modern best practice is to use the most specific one (`@Service` for
business logic, `@Repository` for data access) rather than defaulting
everything to `@Component`.

> 📌 **Beyond the lecture — `@Repository`'s exception translation is not just semantics.**
> The video says the three annotations are "functionally the same," which is
> true for component scanning, but `@Repository` does one extra thing:
> Spring wraps methods on `@Repository`-annotated beans so that
> database-specific exceptions (JDBC `SQLException` subclasses, JPA
> exceptions, etc.) get translated into Spring's own unchecked
> `DataAccessException` hierarchy. That means your service layer can catch
> one consistent exception type regardless of which database driver threw
> the original error.

> 🟨 **Coming from JS?** In an Express app you'd express these same roles
> just by folder convention — `services/userService.js`,
> `repositories/userRepository.js` — with no annotation and no registration
> step; you'd `require()` them directly wherever needed. Spring's
> `@Component`/`@Service`/`@Repository` replace that manual `require()`
> wiring: annotate the class, and the container finds it and makes it
> injectable everywhere, with no file needing to explicitly import another.

### 58:19 — Dependency Injection

> Dependency Injection: Spring automatically provides whatever object a class
> needs — you never write `new` for a managed dependency.

Two ways shown:

**1. Field injection** — works, but Spring itself warns against it:

```java
@Service
class UserService {
    @Autowired
    private Database database;
}
```

Problems: the field can't be `final` (so it's mutable after construction),
and IDEs warn "field injection not recommended."

**2. Constructor injection** — the recommended approach, and needs **no
annotation at all** once there's exactly one constructor:

```java
@Service
class UserService {
    private final Database database;

    UserService(Database database) {
        this.database = database;
    }
}
```

Why constructor injection is preferred (from the video, plus why):

- The dependency is a required constructor parameter — missing it is a
  compile-time/startup-time error, not a silent `null`
- The field can be `final` → the bean becomes **immutable** after
  construction, which the video notes is safe because Spring beans generally
  aren't swapped out after creation
- Works better with testing frameworks (you can pass a mock/fake straight
  into the constructor without needing Spring or reflection at all)

Removing the object assignment and running the app demonstrates the failure
mode directly: a `NullPointerException` because Spring never got a chance to
inject anything if the wiring point doesn't exist.

> ⚠️ **Nuance — the "startup-time error" for missing constructor dependencies
> isn't a plain NPE in a working project.**
> The video's NPE only shows up because the object was being built manually
> (`new UserService()`), bypassing Spring entirely. When Spring itself can't
> satisfy a constructor dependency, it fails **application startup** with a
> `NoSuchBeanDefinitionException` (wrapped in `UnsatisfiedDependencyException`)
> and a clear message naming the missing bean — which is actually a big part
> of why constructor injection is considered safer: you find out immediately
> when the app boots, not later when some code path finally touches a null
> field.

> 🟨 **Coming from JS? — manual DI vs Spring's DI, side by side.**
> The "loose coupling" version from earlier (`UserService(Database database)`)
> is something you can write in plain JavaScript too — it's just called
> **manual dependency injection** (a factory-pattern style):
> ```javascript
> // database.js
> class MySQLDatabase {
>   save(user) { console.log(`MySQL: saving ${user}`); }
> }
>
> // userService.js
> class UserService {
>   constructor(database) {
>     this.database = database; // dependency passed in, not created here
>   }
>   saveUser(user) { this.database.save(user); }
> }
>
> // app.js — YOU wire it together by hand
> const db = new MySQLDatabase();
> const userService = new UserService(db);
> userService.saveUser('Aniket');
> ```
> That last block — manually `new`-ing everything and passing it down — is
> exactly the wiring problem Spring's IoC container eliminates. In a 5-file
> app it's a non-issue; in a real app with 200 classes and deeply nested
> dependencies, hand-wiring becomes its own maintenance burden. Spring (and
> NestJS, if you've used it) automates precisely that last block — Spring
> Boot's component scan finds `MySQLDatabase` and `UserService`, sees that
> `UserService` needs a `Database`, and does the `new` + wiring for you.

## 1:04:23 — Multiple implementations of the same interface

Adding a second `Database` implementation (`PostgresDatabase implements
Database`) alongside `MySQLDatabase` breaks autowiring immediately:

```text
Parameter 0 of constructor in UserService required a single bean, but 2 were found:
- mySQLDatabase
- postgresDatabase
```

Spring has no way to know which one to inject. Four ways to resolve it, in
the order the video builds them up:

### `@Qualifier` — explicit but hardcoded

```java
UserService(@Qualifier("mySQLDatabase") Database database) { ... }
```

Works, but **not recommended** as a long-term pattern — switching databases
means editing and redeploying application code.

### `@Primary` — pick a default

```java
@Service
@Primary
class PostgresDatabase implements Database { ... }
```

Tells Spring "use this one by default" when no other qualifier is given.
Simple for small projects with one clear default, but still hardcodes the
choice into source code — can't change environments without a redeploy.

### `@Profile` — environment-based switching

```java
@Service
@Profile("dev")
class MySQLDatabase implements Database { ... }

@Service
@Profile("prod")
class PostgresDatabase implements Database { ... }
```

Activated via `application.properties`:

```properties
spring.profiles.active=dev
```

...or an environment variable, which is how it'd typically be set per
deployment target (dev/stage/prod). Benefit: **no code change** between
environments, just configuration. Good for "this whole set of beans differs
by environment."

### `@ConditionalOnProperty` — the recommended default

```java
@Service
@ConditionalOnProperty(name = "db.type", havingValue = "mysql")
class MySQLDatabase implements Database { ... }

@Service
@ConditionalOnProperty(name = "db.type", havingValue = "postgres")
class PostgresDatabase implements Database { ... }
```

```properties
db.type=mysql
```

The video calls this the **modern, preferred** approach: fine-grained,
property-value-driven bean selection with zero `if`/`else` in application
code, and it composes naturally with feature-flag-style toggling (not just
whole-environment switching like `@Profile`).

> 📌 **Beyond the lecture — where this leads in real projects.**
> This whole progression (`@Qualifier` → `@Primary` → `@Profile` →
> `@ConditionalOnProperty`) is really a build-up to a broader Spring Boot
> idea: **externalized, environment-specific configuration** using
> `application-{profile}.properties` files (e.g. `application-dev.properties`,
> `application-prod.properties`), which Spring Boot loads automatically based
> on `spring.profiles.active`. In a real multi-database setup you'd rarely
> switch the *implementation class* by property at all — you'd instead keep
> one `DataSource`/JPA setup and just change its connection URL per
> environment. The pattern shown here is a genuinely useful *general*
> Spring technique (pick between competing bean implementations), independent
> of the database example used to teach it.

## 1:17:26 — Bean scopes

| Scope | Behavior | Notes |
|---|---|---|
| **Singleton** (default) | One shared instance for the entire application context | Memory efficient, fast, and safe to share — *if* the bean is stateless |
| **Prototype** | A new instance every time the bean is requested | Rarely needed |
| **Request** | One instance per HTTP request | Web apps only |
| **Session** | One instance per user session | Web apps only |

> ⚠️ **Nuance — "singleton is thread-safe usually" needs a qualifier.**
> A singleton bean is safe to share across concurrent requests only if it
> holds **no mutable instance state** (or only immutable/thread-safe state).
> `UserService` with a `final Database database` field is safe. A singleton
> bean with a plain mutable field being read and written across requests is a
> classic concurrency bug — Spring gives you one shared instance regardless of
> whether your code is safe to share. This is exactly why constructor
> injection + `final` fields (immutability) matters beyond just "cleaner
> code" — it's what makes the default singleton scope safe in practice.

> 🟨 **Coming from JS?** Default singleton scope is similar in spirit to how
> `require()`/`import` caches modules in Node — `module.exports = new
> UserService()` gives you one shared instance everywhere it's imported, same
> end result as a Spring singleton bean. The difference: Node's "singleton" is
> just a side effect of module caching (and easy to accidentally break by
> exporting the *class* instead of an instance); Spring's is an explicit,
> container-managed scope you can change per bean (`@Scope("prototype")`,
> etc.) without touching how the bean is imported or used elsewhere.

## 1:18:12 — Bean lifecycle

Rough flow: Spring creates the object → injects its dependencies → calls an
init hook → the bean is ready for use → (eventually) a shutdown hook fires
before the bean is destroyed.

```java
@Service
class SomeService {

    @PostConstruct
    void init() {
        // runs once, right after dependencies are injected
    }

    @PreDestroy
    void cleanup() {
        // runs once, right before the bean is destroyed (e.g. app shutdown)
    }
}
```

Typical uses: opening a connection pool or warming a cache in `@PostConstruct`,
releasing resources in `@PreDestroy`.

---

## 1:19:19 — Externalizing configuration

Goal: never hardcode values like DB URLs, ports, or credentials — put them in
`application.properties` (or `.yml`) instead.

### `@Value` — inject a single property

```java
@Service
class SomeService {

    @Value("${db.type}")
    private String property;
}
```

Works well for one-off values.

### `@ConfigurationProperties` — the modern way for grouped properties

```properties
db.type=mysql
```

```java
@Configuration
@ConfigurationProperties(prefix = "db")
class DbConfigurations {
    private String type;

    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
}
```

```java
@Service
class SomeService {
    private final DbConfigurations configurations;

    SomeService(DbConfigurations configurations) {
        this.configurations = configurations;
    }

    void printType() {
        System.out.println(configurations.getType());
    }
}
```

Cleaner than a pile of individual `@Value` injections once you have more than
one related property under a shared prefix (e.g. `db.type`, `db.timeout`,
`db.poolSize` all landing on one `DbConfigurations` class).

> 📌 **Beyond the lecture — `@ConfigurationProperties` needs to be enabled.**
> The video mentions "we'll need `@ConfigurationPropertiesScan`" in passing
> but doesn't show it wired up. In practice you need one of:
> `@EnableConfigurationProperties(DbConfigurations.class)` on a
> `@Configuration` class, or `@ConfigurationPropertiesScan` on the main
> `@SpringBootApplication` class (scans the whole app for
> `@ConfigurationProperties`-annotated classes), or — as done in this
> video — simply also annotating the properties class itself with
> `@Configuration`/`@Component`, which registers it as a bean directly.
> Without one of these, Spring won't bind the properties file to the class at
> all and every field will stay `null`.

> 🟨 **Coming from JS?** `application.properties`/`.yml` is doing the job of a
> `.env` file read through `dotenv`. `@ConfigurationProperties` is the typed,
> structured version of what libraries like `envalid` or a `zod`/`joi` schema
> do for `process.env` in a Node app — instead of scattering
> `process.env.DB_TYPE` string lookups through your code (the direct
> equivalent of the `@Value` approach above), you validate and bind a whole
> group of related config values once into a typed object, then inject *that*
> object wherever it's needed.

## 1:24:01 — Java-based configuration

```java
@Configuration
class AppConfig {
    // @Bean methods go here for objects you want to
    // hand-build yourself but still let Spring manage
}
```

Used when you need to create a custom bean yourself (e.g. a third-party
object you don't own the source of, so you can't just slap `@Component` on
it). The video flags this as an "also exists" concept without going deep —
covered further as the series builds real features.

## 1:25:46 — Component scanning, recap

Spring starts scanning from the package containing the `@SpringBootApplication`
class and walks downward through subpackages. Classes in packages **outside**
that root won't be picked up unless you explicitly widen the scan (there's an
annotation for that, but it's rarely needed in practice since nearly all your
code naturally lives under the root package).

---

## 1:26:07 — What `SpringApplication.run()` actually does

```java
@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

That one line is not magic — it's a deterministic pipeline with four main
phases.

### Phase 1 — Create the `SpringApplication`

Detects the **application type** by inspecting the classpath: if Spring MVC
and the Servlet API are present, it assumes a **Servlet-based web
application**; other possibilities are **reactive** (WebFlux) or
**none** (a plain non-web app). This is why adding/removing a dependency like
`spring-boot-starter-web` changes Spring Boot's runtime behavior — it's
literally checking what's on the classpath.

### Phase 2 — Prepare the environment

Builds an `Environment` object that merges every configuration source, in a
strict **priority order** (highest wins when the same property is set in more
than one place):

1. Command-line arguments *(highest priority)*
2. JVM system properties
3. OS environment variables
4. `application.properties` / `application.yml`
5. Default values *(lowest priority)*

This is exactly why setting `DB_TYPE` as an environment variable overrode
what was written in `application.properties` in the `@ConditionalOnProperty`
demo earlier — environment variables outrank the properties file. This
ordering is also *how* production deployments override config without
touching code or files: pass a command-line flag or set an env var, and it
wins.

### Phase 3 — Create the `ApplicationContext`

Spring Boot picks the right context implementation based on the detected
application type — e.g.
`AnnotationConfigServletWebServerApplicationContext` for a standard web app.
This is the object responsible for managing beans, dependency injection,
lifecycle, and eventing (the IoC container from earlier, now concretely
instantiated).

### Auto-configuration mechanism

This is the "magic" behind zero-config setup, broken into concrete steps:

```text
@SpringBootApplication
  └── @EnableAutoConfiguration
        └── AutoConfigurationImportSelector
              └── reads: META-INF/spring/
                    org.springframework.boot.autoconfigure.AutoConfiguration.imports
                    (a file listing every possible auto-configuration class)
              └── applies conditional filtering
              └── registers the classes that pass
```

Conditional filtering uses annotations on each candidate auto-configuration
class:

| Annotation | Meaning |
|---|---|
| `@ConditionalOnClass` | Only apply if a given class exists on the classpath (e.g. only configure a `DataSource` if a JDBC driver class is present) |
| `@ConditionalOnMissingBean` | Only apply if you haven't already defined this bean yourself |
| `@ConditionalOnProperty` | Only apply if a config property has a specific value (the exact mechanism from the `db.type` example earlier) |
| `@ConditionalOnWebApplication` | Only apply for web applications |

**"Override strategy":** your own configuration always wins over
auto-configuration, enforced via `@ConditionalOnMissingBean` — if you define
your own `DataSource` bean, Spring Boot's default auto-configured one simply
won't be created.

> 📌 **Beyond the lecture — the exact filename, and why it matters if you're
> reading older tutorials.**
> `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`
> is the **Spring Boot 2.7+** mechanism. Anything written before that (a lot
> of blog posts and Stack Overflow answers still are) will reference
> `META-INF/spring.factories` instead — the older mechanism for the same
> purpose. If you go spelunking in a Spring Boot 3.x jar looking for
> `spring.factories` and can't find it, this is why: it moved.

> 🟨 **Coming from JS?** Express has nothing like this by design — it's
> intentionally minimal and does zero auto-configuration; you `app.use()`
> every single piece of middleware yourself. The closer analogy is a more
> opinionated, convention-driven framework: think of how **Next.js** wires up
> a route just because a file exists in `pages/api/`, or how **NestJS**
> auto-wires a whole module from its `@Module({...})` decorator. Spring
> Boot's auto-configuration takes that idea further — it inspects your
> *dependencies* (not just your files) and configures accordingly.

### Phase 4 — `context.refresh()`

The final step: registers every selected configuration/bean definition in
the Spring container, resolves dependencies, instantiates all singleton
beans, and the application becomes fully operational — ready to accept
requests (for a web app).

**Recap of the four phases:** create `SpringApplication` (detect app type) →
prepare environment (merge config sources by priority) → create
`ApplicationContext` → load and filter auto-configuration → `context.refresh()`
→ application ready.

---

## 1:44:47 — How a request flows through Spring MVC

High-level path for an incoming request, and the reverse path for the
response:

```text
Client
  → Tomcat (embedded server, default port 8080)
    → DispatcherServlet   ("front controller" — Spring MVC's entry point)
      → HandlerMapping    (decides which controller method handles this URL)
        → HandlerAdapter  (knows how to invoke that specific method)
          → Controller    (delegates immediately — no business logic here)
            → Service     (business logic, validation)
              → Repository  (talks to the database)
                → Database
              ← (data comes back up)
            ← Controller returns a Java object
          ← HttpMessageConverter (Jackson) converts the object to JSON
        ←
      ←
    ← Tomcat
  ← Client receives the JSON response
```

### Front controller pattern

Every HTTP request hits one central component first, before any of your
controllers — in Spring MVC that component is the **`DispatcherServlet`**,
described as "the heart of Spring MVC." It doesn't handle business logic
itself; it **delegates** each concern to a specialized collaborator.

### `HandlerMapping`

Answers: *which controller method should handle this URL?* Maps a request
URL to a specific controller method by reading annotations like
`@GetMapping`, `@PostMapping`, `@RequestMapping`. The most common
implementation is `RequestMappingHandlerMapping`.

### `HandlerAdapter`

Once the right method is identified, the adapter knows *how* to actually
invoke it — necessary because different controller methods can have very
different signatures (different parameter types, return types, path
variables), and Spring needs a uniform way to call any of them. The most
common one: `RequestMappingHandlerAdapter`.

### Three-layer architecture

| Layer | Responsibility |
|---|---|
| **Controller** | Receives the HTTP request; contains **no business logic** — immediately delegates to a service |
| **Service** | Business logic — validation, business rules (e.g. "is this email address valid?") |
| **Repository** | Talks to the database — CRUD operations, database queries. Commonly built on **Spring Data JPA**, covered in video 2 |

### Response path

The controller returns a plain Java object (e.g. a `List<User>`). Spring MVC
converts it to JSON via an `HttpMessageConverter` — by default, **Jackson**
(also mentioned earlier as part of what `spring-boot-starter-web` pulls in).
The JSON then flows back through the same chain in reverse to the client.

### Where auto-configuration fits into this whole flow

All of `DispatcherServlet`, `HandlerMapping`, `HandlerAdapter`, and the
Jackson `HttpMessageConverter` are configured **automatically** the moment
`spring-boot-starter-web` is on the classpath — none of this is code you
write. As a developer, you only write the parts that vary per feature:
`@RestController` classes and `@GetMapping`/`@PostMapping` methods. Spring
Boot configures all the surrounding infrastructure.

> 🟨 **Coming from JS?** Map the whole request-flow diagram onto Express:
>
> | Spring MVC | Express |
> |---|---|
> | `DispatcherServlet` (front controller) | The `express()` app instance itself, routing every request |
> | `HandlerMapping` | Express's internal route matching (`app.get`, `app.post`, etc.) |
> | `HandlerAdapter` | Not really separate in Express — it calls your handler function directly |
> | Controller (delegates, no logic) | Your route handler — in a well-structured Express app it should *also* just delegate to a service, not hold business logic |
> | Service | A plain module/class you `require()` into the route handler |
> | Repository | Your DB-access module (e.g. wrapping `pg`/`mongoose`/Prisma calls) |
> | `HttpMessageConverter` (Jackson) | `res.json(data)` (uses `JSON.stringify` under the hood) |
> | Filters / interceptors | Express middleware (`app.use((req, res, next) => ...)`) |
>
> The three-layer split (Controller/Service/Repository) isn't unique to
> Spring — it's good practice in Express too, just not enforced by the
> framework the way Spring's conventions push you toward it.

---

## The threading model: the biggest mental shift from Node.js

Not covered in the video, but it's the single most consequential difference
for anyone moving from Node.js to Java/Spring, and it directly drives how you
design for scale.

**Node.js / Express:** single-threaded, event-loop based. One thread handles
*all* requests by interleaving them — as long as your code doesn't block that
one thread (no synchronous heavy CPU work, no `fs.readFileSync` in a hot
path), thousands of concurrent requests can be in flight, each waiting on
non-blocking I/O (DB calls, HTTP calls) without tying up a thread.

**Spring MVC (the "servlet stack" used throughout this video):**
thread-per-request, blocking I/O by default. Every incoming HTTP request is
handed a thread from a pool, backed by the embedded Tomcat server (default
max ~200 threads). That thread stays genuinely blocked for the entire request
— including while waiting on a slow database query or an external API call.
If every pool thread is busy, new requests queue up.

| | Node.js / Express | Spring MVC (servlet stack) |
|---|---|---|
| Concurrency model | Single thread, event loop, non-blocking I/O | Thread pool, one thread per in-flight request, blocking I/O |
| A slow DB call... | ...frees the thread to serve other requests while it waits | ...holds its thread hostage until the query returns |
| Scaling more concurrent requests | Mostly free, as long as you avoid blocking the loop | Costs a thread (and its memory) per concurrent request — tunable, but finite |
| Classic foot-gun | Blocking the event loop with sync/CPU-heavy code | Under-sizing the thread pool or DB connection pool for real concurrent load |

**Why this matters for "scalable, robust":** the Tomcat thread pool and the
database connection pool (Spring Boot defaults to **HikariCP**, default pool
size 10) have to be sized together, for your actual concurrent load.
Undersize either and requests queue or time out under load; oversize the DB
pool and you can exhaust the database's own connection limit instead. This is
a tuning conversation you'll have in Java-land that mostly doesn't exist the
same way in Node.

**If you eventually need Node-like non-blocking concurrency in Spring:**
that's what **Spring WebFlux** (Spring's reactive stack, built on Project
Reactor) is for — a genuinely different, non-blocking programming model,
closer conceptually to Node's event loop, using `Mono`/`Flux` types instead
of returning plain objects directly. It's a deliberate architectural choice
made per-project (you'd pick `spring-boot-starter-webflux` instead of
`spring-boot-starter-web` at project-creation time), not a runtime toggle —
and it isn't used anywhere in this series, which sticks to the traditional
servlet/MVC stack throughout. Good to know it exists for later; not something
to reach for by default.

---

## 📌 Beyond the lecture — getting your Spring Boot journey started

A few things not in this video that will help immediately, since you're
starting a new role with this stack:

- **Reference the docs directly.** [spring.io/projects/spring-boot](https://spring.io/projects/spring-boot)
  and the [Spring Boot reference documentation](https://docs.spring.io/spring-boot/) are
  genuinely well written and worth bookmarking now — this course will not
  replace them for edge cases.
- **`start.spring.io` has an API**, not just a web form — `curl
  https://start.spring.io/starter.zip -d dependencies=web,data-jpa -d
  javaVersion=21 -o demo.zip` generates the same project from a terminal or
  script.
- **Testing wasn't covered here but comes bundled by default.** Every
  Initializr project includes `spring-boot-starter-test` (JUnit 5, Mockito,
  AssertJ) automatically — worth opening `src/test/...ApplicationTests.java`
  in your own project now just to see the generated `@SpringBootTest` smoke
  test.
- **Common annotation cheat sheet**, gathering everything from this video in
  one place:

  | Annotation | Layer/purpose |
  |---|---|
  | `@SpringBootApplication` | Marks the main class; combines `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan` |
  | `@RestController` | Web layer — handles requests, returns data (not view names) |
  | `@Service` | Business logic layer |
  | `@Repository` | Data access layer |
  | `@Component` | Generic Spring-managed bean |
  | `@Configuration` | A class that declares beans manually via `@Bean` methods |
  | `@Autowired` | Field/setter injection (works, but constructor injection needs no annotation and is preferred) |
  | `@Qualifier` | Disambiguate between multiple beans of the same type |
  | `@Primary` | Default bean when multiple candidates exist |
  | `@Profile` | Activate a bean only for a given environment |
  | `@ConditionalOnProperty` | Activate a bean only if a config property matches a value |
  | `@Value` | Inject a single external property |
  | `@ConfigurationProperties` | Bind a group of properties (by prefix) onto a POJO |
  | `@PostConstruct` / `@PreDestroy` | Bean lifecycle hooks |
  | `@GetMapping` / `@PostMapping` / `@PutMapping` / `@DeleteMapping` | HTTP-verb-specific request mappings (shorthand for `@RequestMapping(method = ...)`) |

- **HTTP verbs you'll meet immediately in video 2**, since only `@GetMapping`
  appeared here: `POST` (create), `PUT`/`PATCH` (update — full vs. partial),
  `DELETE` (remove), each with a matching `@...Mapping` annotation.
- **Maven quick orientation**, since the video picks Maven without explaining
  its mechanics: `pom.xml` declares `<dependencies>`; `mvn spring-boot:run`
  runs the app from the terminal without needing an IDE; `mvn clean package`
  builds the deployable jar Spring Boot then runs via `java -jar`.

---

## Building this into a scalable, robust backend — a roadmap

This video is foundations only. Here's the fuller map of what "production
grade" actually requires, so it's in one place even before the later videos
in this series get there — each mapped to its Node/Express equivalent, and
to where in the series (or beyond it) it gets covered.

| Concern | Spring Boot tool | Node/Express equivalent | Covered |
|---|---|---|---|
| Request validation | Bean Validation (`@Valid`, `@NotNull`, `@Size` on a DTO) | `Joi`, `Zod`, `express-validator` | Expected in video 2, alongside REST APIs |
| Centralized error handling | `@RestControllerAdvice` + `@ExceptionHandler` | Express error-handling middleware `(err, req, res, next) => ...` | Not in the series yet — example below |
| Keeping API shape separate from DB shape | DTOs (plain request/response classes) mapped to/from JPA entities | A response-shaping layer, or just not returning your Mongoose/Prisma model directly | Video 2 |
| Persistence | Spring Data JPA + Hibernate | Prisma / Sequelize / Mongoose / raw `pg` | Video 2 |
| Structured logging | SLF4J + Logback (bundled by default) | `winston`, `pino` | Not in the series yet |
| Testing | JUnit 5 + Mockito (unit), `@SpringBootTest` (integration) | Jest/Mocha + Supertest | Bundled by default, not walked through yet |
| Health checks / metrics | Spring Boot **Actuator** (`/actuator/health`, `/actuator/metrics`) | A hand-rolled `/health` route, or `prom-client` | Named in video 1, not demoed |
| Authentication/authorization | Spring Security | `passport.js`, hand-rolled JWT middleware | **Video 3** |
| Caching | Spring Cache abstraction + Redis | `ioredis`, `node-cache` | **Video 4** |
| Microservices / async messaging | Spring Cloud, Kafka | Message queues (`bullmq`, `kafkajs`), REST/gRPC between services | **Video 4** |
| API documentation | springdoc-openapi (Swagger UI) | `swagger-jsdoc`, `swagger-ui-express` | Not in the series yet |
| Resilience (retries, circuit breakers, timeouts) | Resilience4j | `opossum`, `p-retry` | Not in the series yet — worth it once you call external services |
| Packaging & running in prod | `mvn clean package` → `java -jar app.jar`, usually inside Docker | `npm run build` → `node dist/server.js`, usually inside Docker | Not in the series yet |

A minimal centralized error handler is worth having from day one — it's a
gap in this video, and it's the direct Spring equivalent of Express's
`app.use((err, req, res, next) => ...)` at the bottom of the middleware
chain:

```java
@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(UserNotFoundException ex) {
        return ResponseEntity
            .status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse(ex.getMessage()));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneric(Exception ex) {
        return ResponseEntity
            .status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(new ErrorResponse("Something went wrong"));
    }
}

record ErrorResponse(String message) {}
```

`@RestControllerAdvice` applies across **every** controller in the app — one
place to catch exceptions instead of a `try`/`catch` in every method, exactly
the same motivation as Express's single error-handling middleware.

## Interview and practical takeaways

1. **Spring Boot is not a Spring replacement** — it's an opinionated,
   auto-configuring layer on top of Spring that eliminates most manual setup.
2. **IoC/DI in one line:** your code declares what it needs (via constructor
   parameters); Spring decides what object to hand over and manages its
   lifecycle. You never write `new` for a managed dependency.
3. **Constructor injection over field injection** — immutable (`final`
   fields), fails fast and loudly if a dependency is missing, and is the
   easiest to unit test without a Spring context at all.
4. **Know the difference between `@Qualifier`/`@Primary` (hardcoded in code)
   and `@Profile`/`@ConditionalOnProperty` (driven by external config)** —
   a very common "how would you handle multiple database implementations"
   interview question maps directly onto this progression.
5. **`@SpringBootApplication` = `@Configuration` + `@EnableAutoConfiguration`
   + `@ComponentScan`** — knowing this decomposition signals you understand
   what's actually happening under the one annotation everyone copy-pastes.
6. **The request flow — Tomcat → DispatcherServlet → HandlerMapping →
   HandlerAdapter → Controller → Service → Repository → DB, then back through
   an `HttpMessageConverter`** — is a very standard "walk me through what
   happens when a request hits your API" interview answer.
7. **Auto-configuration is conditional, not unconditional** — `@ConditionalOnClass`,
   `@ConditionalOnMissingBean`, `@ConditionalOnProperty`, and
   `@ConditionalOnWebApplication` are the levers; your own explicit bean
   definitions always win over Spring Boot's defaults.

---

**Next:** Video 002 — Building REST APIs and database connectivity (Spring Data JPA).
