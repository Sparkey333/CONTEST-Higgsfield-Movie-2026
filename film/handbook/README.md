# The Aperture Method

**[the-aperture-method.pdf](the-aperture-method.pdf)** — 27 pages. Print double-sided
and write on it.

Eighteen sheets in the order you work them. Part I is nine stops for a 3–5 minute
generated short; Part II is the Long Aperture, a feature planner and script builder.

## Why it is not the Snowflake

The Snowflake Method expands — one sentence becomes a paragraph, becomes a synopsis,
becomes a draft. That works because prose revises at zero marginal cost.

Generated film does not behave that way. You cannot revise a shot; you can only re-roll
it, paying credits each time, with no guarantee the new roll matches the take you
already cut around. The expensive failure mode is not bad writing. It is **drift** — the
face that changes between shots, the palette that wanders, the light from nowhere.

So this method inverts the shape. It **narrows**. Each sheet removes freedom, ordered by
cost-of-change: whatever is most expensive to fix after generation begins gets locked
first. By the time you spend a credit, every decision the model could get wrong has
already been made by you.

Every sheet ends in a gate. Clear it before stopping down further — skipping one does
not save time, it moves the cost to the most expensive possible moment.

## Regenerating

```bash
python3 scripts/build-handbook.py
```

Content lives in the `SHEETS_SHORT` and `SHEETS_FEATURE` tables in
[`scripts/build-handbook.py`](../../scripts/build-handbook.py). Edit those, re-run,
commit both the script and the PDF. Requires `reportlab`.
