# DAHN Launch Experience Design Specification

## Status and authority

Draft normative specification for the bounded application-shell launch
experience. It owns narrative, imagery/provenance, readiness/handoff, and
accessibility. The MAP Application Launcher owns startup and home-Dancer
selection; this presentation does not select the Dancer or make Space Navigator
a Launcher dependency. References to Space Navigator describe the initial
handoff experience.

## Purpose


Before the initial Space Navigator becomes visible, DAHN SHOULD present a
brief, evocative launch experience. It is an entry ritual into DAHN, not a
splash screen, cinematic sequence, or substitute for the Navigator. The
sequence frames the person as a locally situated participant in nested wholes
and frames this first Navigator as an early visual expression that future
Visualizer Commons contributors may deepen.

## Narrative and scenes

The MVP scene order is:

1. **Cosmos** — observational imagery of NGC 346 begins somewhat unresolved
   and comes into focus.
2. **Stellar transition** — the view moves toward a luminous point in the
   nebula; increasing brightness may bridge the scene into Earth's solar
   context without representing that star as literally the Sun.
3. **Living Earth** — a whole-Earth NASA DSCOVR / EPIC observation becomes the
   visual center.
4. **Living place** — Earth yields to observational imagery of the Okavango
   Delta, selected for its visibly nested relationships among water, land,
   vegetation, species, and changing conditions.
5. **I-Space** — the terrestrial scene recedes as the initialized Space
   Navigator emerges, so the handoff reads as arrival rather than screen
   replacement.

The sequence MUST suggest semantic continuity across scales rather than
simulate astrophysically literal travel. It SHOULD use restrained full-screen
still-image treatment—zoom, focal translation, blur/focus, opacity,
brightness, crossfade, and easing—rather than video, 3D simulation, or text
that competes with the imagery. Any textual framing is optional, sparse, and
provisional.

## Application-shell boundary

The MVP launch experience is an **application-shell concern**. It is not a MAP
Visualizer, MAP media ValueType, media Holon, or Visualizer Commons feature.
Its imagery may be bundled as ordinary application assets. It MUST NOT put MAP
media infrastructure, dynamic visualizer acquisition, generalized animation
grammar, WebGL/Three.js, GIS, geolocation, personalized locality, or external
media streaming on the critical path.

A future experience may descend from Earth into the user's actual locality or
bioregion. That possibility makes local-first participation visually literal,
but it is explicitly deferred and creates no MVP requirement for location
services, map tiles, or geospatial data.

## Readiness, handoff, and control

DAHN initialization and the narrative sequence are independent timelines.
Initialization begins immediately beneath the launch experience. If readiness
arrives early, the sequence completes normally. If it arrives late, the final
terrestrial scene enters a subtle holding state until the initial Space
Navigator can render; the experience MUST NOT expose incomplete UI.

A Skip control MUST become available after a short initial interval. Skipping
before readiness advances to that holding state; skipping after readiness
hands off promptly. The final handoff SHOULD retain subtle local movement while
the Navigator canvas emerges through or beneath the terrestrial scene.

The launch MUST provide a reduced-motion treatment that substantially removes
travel motion while preserving the semantic progression where practical, or
transitions directly to the final state. It MUST avoid flashing or rapid
luminosity changes, keep controls keyboard-accessible, fail gracefully when an
asset cannot load, and never prevent eventual access to the application.

## Observational imagery and provenance

The launch uses authentic **observational imagery of the actual universe and
Earth**, not AI-generated or invented artwork. “Observational” deliberately
includes instrumentally captured and scientifically processed imagery,
including assigned-color processing; it does not imply ordinary visible-light
photography.

Provenance is part of the experience, not legal boilerplate. An unobtrusive,
keyboard-accessible **Image credits** affordance MUST expose each incorporated
asset's title/subject, mission or instrument, complete supplied credit line,
authoritative source URL, applicable usage information, and optional short
explanation that it derives from scientific observation rather than AI
artwork. The full source credit MUST NOT be reduced to merely “NASA.”

The preferred starting set is JWST NGC 346 imagery (NASA / ESA / CSA, retaining
the complete supplied credit), NASA DSCOVR / EPIC whole-Earth imagery, and
NASA Earth Observatory or other verified NASA observational imagery of the
Okavango Delta. Exact asset, crop, and source-provided attribution remain
implementation-time selections.

Bundled derivatives MUST be appropriately sized and efficiently encoded for
startup, require no network connection, and avoid expensive runtime image
processing. Original source references and provenance metadata remain retained
alongside the optimized derivatives.
