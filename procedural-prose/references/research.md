# Research notes

These sources support the design of the skill. They do not establish that
any single punctuation mark proves model authorship.

## Instruction-tuned prose

A PNAS study compared human writing with output from GPT-4o and several
Llama 3 variants. The instruction-tuned models used more nominalizations,
present participial clauses, and phrasal coordination. The authors describe
the result as an informationally dense, noun-heavy style that does not
always match the genre.

- Russell et al., "Do LLMs write like humans? Variation in grammatical and
  rhetorical styles": https://pmc.ncbi.nlm.nih.gov/articles/PMC11874169/

This supports reviewing sentence structure and information density instead
of treating punctuation as the underlying problem.

## Recurring surface patterns

Wikipedia's community guide records negative parallelisms, repeated
rhetorical structures, rule-of-three constructions, and formulaic dash use
as recurring signs in model-generated writing. It states that these are
indicators to consider together. They are not proof of authorship.

- Wikipedia, "Signs of AI writing":
  https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing

## Prompting for style

Anthropic recommends telling the model what to produce instead of relying
only on prohibitions. It describes examples as one of the most reliable
ways to control output format, tone, and structure. It also recommends
matching the prompt's style to the desired output.

- Anthropic, "Prompting best practices":
  https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices

A 2024 style-transfer study found that concrete style properties applied in
steps generally produced more consistent control than a broad style request
alone. Results varied by model and style.

- Reif et al., "Step-by-Step: Controlling Arbitrary Style in Text with
  Large Language Models":
  http://www.lrec-conf.org/proceedings/lrec-coling-2024/pdf/2024.main-1.1328.pdf

## Procedural-writing rules

Google recommends one idea per sentence and splitting long or branching
sentences. Microsoft recommends a separate step for each instruction.
ASD-STE100 uses controlled rules such as one instruction per sentence and
placing conditions before actions.

- Google Technical Writing, "Short sentences":
  https://developers.google.com/tech-writing/one/short-sentences
- Microsoft Writing Style Guide, "Writing step-by-step instructions":
  https://learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions
- ASD-STE100 Issue 9:
  https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf

These sources support atomic instructions, concrete positive rules,
approved examples, and a final structural review. They do not support a
blanket ban on semicolons, dashes, contrast, or emphasis.
