# Case Studies

Use these as worked examples when the user needs a concrete model.

## 1) Async Submit Button

**Trigger**
- Primary button press
- Keyboard submit where appropriate

**Rules**
- Validate required fields
- If invalid, do not submit; focus the first issue
- If valid, enter loading immediately
- Prevent duplicate submission
- Preserve input on failure
- Offer retry when helpful

**Feedback**
- Press acknowledgment immediately
- Loading label such as "Submitting..."
- Success confirmation near the button or next step
- Actionable error near the source plus summary if needed

**Loops / Modes**
- Returning users benefit from fewer explanatory hints, not different meaning

## 2) Toggle With Remote Persistence

**Trigger**
- Tap or click on a visible binary control

**Rules**
- Optimistic update only if rollback is safe and understandable
- Otherwise show pending state until confirmed
- On failure, restore prior state and explain what happened

**Feedback**
- State change visible instantly
- Pending state if server confirmation matters
- Failure message tied to the control

**Loops / Modes**
- Repeated use should feel instant and unsurprising

## 3) Pull-To-Refresh

**Trigger**
- Downward pull on scrollable content
- Prefer a visible refresh affordance somewhere in the UI if the action is important

**Rules**
- Do not trigger until threshold is crossed
- Prevent nested scroll confusion
- Ignore repeat attempts during active refresh

**Feedback**
- Stretch or resistance while pulling
- Threshold indication before release
- Clear loading state during refresh
- "Updated just now" or equivalent after completion when useful

**Loops / Modes**
- First-time users may need a one-time hint; experienced users should not

## 4) Delete With Undo

**Trigger**
- Explicit delete action with clear consequence framing

**Rules**
- If the object is recoverable, prefer immediate delete plus undo window
- If irreversible or high-stakes, require stronger confirmation
- Preserve context after delete so users understand what changed

**Feedback**
- Immediate removal or marked-removed state
- Undo affordance in a predictable location
- Specific error if deletion fails

**Loops / Modes**
- Repeated deletes should stay predictable; never make undo harder to find over time
