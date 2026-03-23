# Reviewer Prompt Template

Each reviewer gets a single prompt containing:

1. The stated intent (from Step 2)
2. Their assigned lens (full text from references/reviewer-lenses.md)
3. The principles relevant to their lens (file contents, not summaries)
4. The code or diff to review
5. Instructions: "You are an adversarial reviewer. Your job is to find real problems, not
   validate the work. Be specific — cite files, lines, and concrete failure scenarios.
   Rate each finding: high (blocks ship), medium (should fix), low (worth noting).
   Write findings as a numbered markdown list to your output file."

When Claude Code CLI native repo access is available, keep the review prompt
small and let Claude inspect the repo with `Read/Grep/Glob` instead of pasting
large file excerpts by default. Include the scope, intent, starting files or
diff targets, and the reviewer instructions; let the CLI do the reading.

Spawn all reviewers in parallel.
