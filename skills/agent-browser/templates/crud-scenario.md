# CRUD Scenario Template

## Baseline

- record starting URL
- record current visible state
- note what must be restored before exit

## Create

- clear network requests
- perform the create action
- verify the request fired
- capture screenshot

## Update

- re-snapshot after the create result renders
- perform the edit
- verify request and final state

## Toggle or Pause

- verify the control state before toggling
- toggle once
- capture the changed state
- restore it if baseline requires that

## Delete or Restore

- delete only disposable entities created by the scenario
- if touching persistent data, restore exact baseline instead

## Evidence

- final URL
- title
- errors
- screenshot path
- network request summary
