# 0001: SUMO and closed-form formulas are the reference, not dependencies

## Status

Accepted

## Context

A traffic simulator is easy to make look plausible and hard to make right. Two kinds of check
are available. Closed-form results (Webster's delay formula, the fundamental diagram of the
car-following model) hold exactly in simple cases. SUMO, the open-source microsimulator,
gives a second opinion on whole networks. Building on SUMO would be quicker, but then
Junction could not be checked independently and the adaptive controller would be limited to
what SUMO exposes.

## Decision

- Junction implements its own network model, vehicle simulation, routing and signal control.
- SUMO is used only to produce reference results. It runs in a separate, pinned tool
  environment and writes fixtures that the tests compare against.
- Closed-form checks live in the main test suite.
- `make check` never needs SUMO installed.

## Consequences

- Simple cases are checked exactly; whole networks are checked statistically against SUMO with
  a stated tolerance, because the two simulators use different car-following details.
- Reference fixtures must be regenerated deliberately when SUMO's version changes.
