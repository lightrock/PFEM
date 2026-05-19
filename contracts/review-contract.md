# Review Contract

A PFEM review record should identify:

- `review_id`
- `review_gate`
- `decision`
- `reviewer_role`
- `created_time`
- `subject_refs`

A federation message that crosses a topology link with a review gate should have
an approved review record covering the message or a referenced rollup/package.
