# Plan

Junction is built in sessions, each with a clear success test. Later sessions build on
earlier ones.

| # | Session | Success |
|---|---|---|
| 1 | Road network model and file format: nodes, links, lanes, turning movements, signal groups and plans | A sample city loads and validates; a bad file lists every error with its location; connectivity problems (unreachable links, lanes with no exit) are reported |
| 2 | Vehicle simulation on links: car-following (Intelligent Driver Model) and lane changing, with seeded arrivals | Speed, flow and density on a single road match the model's fundamental diagram; no vehicle overlaps or reverses; runs replay exactly |
| 3 | Signalised junctions: fixed-time plans, queues, spillback and blocking back | At low and moderate demand, average delay at an isolated junction matches Webster's formula within a stated tolerance; queues clear when demand drops |
| 4 | Routing: origin-destination demand, shortest paths by travel time, and re-routing when a road closes | Traffic assignment converges; a closure moves traffic onto alternative routes and every trip still finishes or is reported as stranded |
| 5 | Adaptive signal control from detector counts, compared with fixed-time plans on the same seeds | Across seeds, adaptive control cuts average delay against the Webster baseline without starving any approach |
| 6 | Live engine and web UI: clock, map, vehicles, signal states, incidents and replay | Playwright covers a road closure being routed around and a signal plan being changed |
| 7 | Scale: a synthetic city with thousands of links and tens of thousands of vehicles, profiling and benchmarks | A peak hour of the large city runs within a set budget; benchmarks fail the build on regression |

## Rules

- The reference is SUMO, run in a separate tool environment, plus closed-form formulas
  (Webster, the fundamental diagram). The project's own simulator never calls SUMO.
- All randomness comes from named, seeded streams. Every run replays exactly.
- No learned models. Demand comes from origin-destination matrices and fixed profiles.
