# LinkedIn Post — "I let one AI grade another AI"

> Ready to copy-paste. Keep the line breaks — they are deliberate and drive LinkedIn's "see more" cut-off.

---

My LLM answered "4".

But how do I *know* the answer is actually good?

That was the question that sent me down the rabbit hole of **LLM evaluation** this week.

Turns out you don't read 100 outputs by hand. You let one model grade another — this is called **LLM-as-a-judge**.

Here's what I built in ~30 lines of Python with DeepEval:

**1. A model under test**
Groq serves the model that answers the question. Groq speaks the OpenAI API, so I pointed the standard OpenAI client at it with one line — just a different `base_url`.

**2. A judge (a completely different provider)**
OpenRouter runs the model that does the scoring.

Why split them? Because a model grading its own homework is a conflict of interest. Two providers = an independent referee.

**3. Metrics that turn "vibes" into numbers**
• **Answer Relevancy** — did it actually answer what was asked?
• **Hallucination** — did it make things up or contradict the context?

Each one returns a score, a pass/fail against my threshold, and — my favorite part — a *plain-English reason* for the score.

**The result:**

```
Answer Relevancy   1.00   ✅ PASSED
Hallucination      1.00   ✅ PASSED

Reason: "The response directly answered the question with only the
requested number and contained no irrelevant statements."
```

That "reason" line is the whole point. It's not just a green checkmark — it's an auditable why.

**The biggest lesson:**
A passing test means nothing if it can't fail. So the real skill isn't writing the test — it's setting the threshold and giving the judge enough context to be honest.

Next up: catching a model that's *confidently wrong*. That's where hallucination scoring earns its keep.

If you're shipping anything with an LLM in it, "it looked fine when I tried it" is not a test.

You need a number. You need a reason. You need a threshold it can fail.

---

Building in public — what's your go-to metric for evaluating LLM output? 👇

#AI #LLM #DeepEval #MachineLearning #Python #AIEngineering #LLMOps #GenerativeAI #Testing #Groq #OpenRouter #BuildInPublic
