export const meta = {
  name: 'improve-java-notes',
  description: 'Correctness + modern-Java pass over Durga Sir Core Java lecture notes',
  phases: [{ title: 'Rewrite', detail: 'one agent per note: verify, correct, modernise' }],
}

const TEMPLATE = 'notes/chunk-001-020/001-identifiers-reserved-words.md'

const SCHEMA = {
  type: 'object',
  required: ['note', 'corrections', 'modernBoxes', 'summary'],
  properties: {
    note: { type: 'string', description: 'note number, e.g. "042"' },
    corrections: { type: 'integer', description: 'count of factual errors fixed' },
    modernBoxes: { type: 'integer', description: 'count of Modern Java callouts added' },
    compilerChecked: { type: 'boolean', description: 'were any claims run through javac' },
    summary: { type: 'string', description: 'one line: the most significant fix made' },
  },
}

function prompt(it) {
  return `You are improving one lecture note from a Core Java (Durga Sir, OCJP/SCJP) study set.
The recording is from the Java 6/7 era. Your job is to make the note **correct, current, and well written** without destroying the lecture.

## Files
- Note to rewrite (edit in place): \`${it.md}\`
- Transcript of what Sir actually said: ${it.tx ? `\`${it.tx}\`` : '**none available** — improve from the note text alone, and do NOT invent lecture content that is not already there'}
- Template to match exactly: \`${TEMPLATE}\` — READ THIS FIRST. It is the agreed house style.
${it.orphan ? '- ⚠️ This note ends with a `## Tables (placement lost)` section. Those tables were orphaned by a bad converter. Move each one back to the section that discusses it and DELETE that trailing heading.' : ''}

## A JDK is installed — use it
\`export PATH=/opt/homebrew/opt/openjdk/bin:$PATH\` gives you javac/java 26.
Use \`--release N\` to check version-specific behaviour.
**Actually compile any claim you are unsure about** rather than trusting memory. Work in a temp dir under /private/tmp/claude-501/-Users-macbookprom1-test/d2522eaf-e931-41f9-9147-ef8e9d87df98/scratchpad/. Do not leave .java/.class files in the repo.

## What to do

1. **Read the transcript** (if present) and the current note. The note was built from auto-captions, so ASR noise may have been mis-decoded into wrong technical claims. Fix those against the transcript.
2. **Delete the ASR decode key** paragraph near the top ("ASR noise is decoded in place — ..."). It is scaffolding, not study material. Keep the video-info table.
3. **Verify every technical claim.** Where Sir (or the transcription) is simply wrong, keep the teaching flow but add:
   \`> ❗ **Correction — <short claim>.**\` followed by what is actually true and why.
4. **Add \`> ⚠️ **Modern Java**\` callouts** wherever the language has moved since the recording. Keep what Sir taught (it is still the OCJP answer and still true of legacy code), then state what changed and in which release. Be specific about versions. High-value areas across this playlist:
   - collections/concurrency: ConcurrentHashMap stopped using segment locking in Java 8 (CAS + per-bin locking now); sequenced collections in 21; \`List.of\`/\`Map.of\`
   - threads: \`stop()\`/\`suspend()\`/\`resume()\` removed for real in 20+; virtual threads (21); structured concurrency
   - exceptions: try-with-resources effectively-final form (9); helpful NPEs (14)
   - strings: text blocks (15), \`isBlank\`/\`strip\`/\`repeat\`/\`formatted\`, compact strings (9)
   - classes: records (16), sealed (17), pattern matching for switch (21), \`var\` (10)
   - GC/finalization: \`finalize()\` deprecated (9) and disabled by default (18); SecurityManager deprecated (17)
   - obsolete-but-taught: \`strictfp\` no-op since 17; \`new Integer(...)\` deprecated; \`Vector\`/\`Hashtable\`/\`Stack\` legacy
   Only add a box where something genuinely changed. Do not pad. A note on a topic Java never changed (e.g. operator precedence) may legitimately need zero boxes.
5. **Rewrite the prose.** Keep Sir's analogies and stories — they are the memory hooks — but tighten them to a couple of sentences. Cut pure classroom filler ("are you getting", roll-call, repetition). Keep the \`### MM:SS — heading\` timestamps.
6. **Make every code block real Java** that would compile (or that carries a comment saying exactly why it does not, e.g. \`// CE: ...\`).
7. **Keep tables inline** next to the text that explains them, never at the end.
8. End with an **## Exam and interview points** numbered list, then \`**Next:** Video NNN — <title>\`.

## Hard rules
- Write the improved Markdown back to \`${it.md}\` with the Write tool. Do not create new files in the repo.
- Do NOT touch the .doc/.docx files — those are regenerated afterwards.
- Do not shorten the note overall. This is a study set; depth is the point. Corrections and modern context should make it longer, not shorter.
- Never invent a timestamp, a quote, or a lecture moment that is not in the transcript or the existing note.
- Preserve the video-info table verbatim (title, duration, URL, position).

Return the JSON summary.`
}

const items = args
log(`improving ${items.length} notes`)

const results = await pipeline(items, (it) =>
  agent(prompt(it), {
    label: `note ${it.n}`,
    phase: 'Rewrite',
    schema: SCHEMA,
  })
)

const ok = results.filter(Boolean)
const corrections = ok.reduce((a, r) => a + (r.corrections || 0), 0)
const boxes = ok.reduce((a, r) => a + (r.modernBoxes || 0), 0)
log(`done: ${ok.length}/${items.length} notes, ${corrections} corrections, ${boxes} modern-Java boxes`)

return {
  completed: ok.length,
  failed: items.length - ok.length,
  corrections,
  modernBoxes: boxes,
  compilerChecked: ok.filter((r) => r.compilerChecked).length,
  notes: ok.map((r) => ({ n: r.note, c: r.corrections, m: r.modernBoxes, s: r.summary })),
}
