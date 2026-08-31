# Contributing

Thank you for helping improve Image Prompt Replication Skill.

## What makes a useful contribution

Prefer focused changes supported by an observable failure case, such as:

- a mode being selected incorrectly;
- content leaking into a style-only prompt;
- a correction pass changing constraints that already matched;
- contradictory prompt wording;
- a missing high-impact comparison category;
- documentation or packaging errors.

Avoid adding universal rules for a single unusual image unless the failure reveals a general decision problem.

## Development workflow

1. Fork the repository and create a focused branch.
2. Update the smallest relevant file.
3. Run `python3 scripts/validate_skill.py`.
4. Verify that `SKILL.md` remains concise and detailed mode guidance stays in `references/workflows.md`.
5. Open a pull request describing the input scenario, observed failure, and why the proposed behavior is better.

## Pull-request checklist

- [ ] The change preserves the three-mode boundary.
- [ ] New instructions are supported by a realistic use case.
- [ ] There are no unfinished placeholders or contradictory requirements.
- [ ] Links and package paths are valid.
- [ ] The validator passes locally.
- [ ] User-facing documentation is updated when behavior changes.

By contributing, you agree that your contribution will be licensed under the MIT License.

