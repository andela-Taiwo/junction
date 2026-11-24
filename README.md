# Junction

Simulate a city's traffic: vehicles following each other along roads, queues building at
signals, drivers choosing routes, and whether adaptive signal control beats fixed timings.

> **Status: foundation only.** The project layout, tooling, traffic units, Webster's
> fixed-time signal formulas and seeded random streams exist and are tested. The road network,
> vehicle simulation, routing, adaptive control and web UI are not built yet. See
> [the plan](docs/PLAN.md).

## What it will do

- **Road network**: links, lanes, junctions, turning movements and signal plans, read from a
  file and validated.
- **Vehicles**: car-following and lane-changing, so queues form, spill back and clear.
- **Signals**: fixed-time plans by Webster's method, then an adaptive controller that reacts to
  detector counts.
- **Routes**: drivers choose routes from an origin-destination matrix, and re-route when a road
  closes.
- **Live view**: a map with vehicles, queues and signal states, incidents you can inject, and a
  timeline you can replay.

All randomness comes from a seed, so every run replays exactly.

## What exists today

| Module | What it does |
|---|---|
| `junction.units` | Speeds, flows, headways, densities and passenger car units |
| `junction.signals` | Webster's optimum cycle, green splits and average delay for an isolated junction |
| `junction.rng` | Named, independent random streams from one run seed |

## Quickstart

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12.

```bash
make setup   # install locked dependencies
make check   # lint, format check, type check and tests
make help    # list every target
```

## Layout

```
src/junction/  # the simulator package
tests/         # unit and property tests
docs/PLAN.md   # what is being built, in order
docs/adr/      # architecture decision records
```

## Licence

MIT. See [LICENSE](LICENSE).
