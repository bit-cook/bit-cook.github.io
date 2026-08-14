# Changelog

All notable visual and interaction changes to osome.work are documented here.

## Workshop v2.2 - 2026-08-14

### Fixed

- Kept the hero signal and ticker moving when a device reports reduced-motion,
  because these are essential requested features rather than decorative entry
  transitions.
- Increased orbit and ticker speeds and added a second visible orbit marker so
  movement is immediately apparent.
- Versioned workshop CSS and JavaScript URLs to bypass stale browser caches.

## Workshop v2.1 - 2026-08-14

### Changed

- Made the optimistic warm-light palette the daytime default.
- Added automatic local-time theming: light from 07:00 through 18:59 and dark
  from 19:00 through 06:59 in the visitor's device timezone.
- Kept manual theme switching available for the current visit without storing
  a permanent override.
- Kept the signal banner dark in both themes and preserved its continuous
  motion alongside the animated hero orbits.

## Workshop v2 - 2026-08-14

### Changed

- Rebuilt the hero signal mark with three visibly asymmetric rotating orbits,
  an animated primary ring, system labels, and a restrained ambient glow.
- Restored a continuous signal banner between the hero and manifesto sections.
- Added entrance motion, signal pulses, scanning details, and richer hover
  feedback while preserving reduced-motion behavior.
- Changed the workshop navigation to a compact translucent fixed header after
  scrolling.
- Refined project-card motion, keyboard focus states, desktop proportions, and
  mobile signal-art scaling.
- Applied the same structure and behavior to the Chinese and English workshop
  pages.

### Validation

- HTML validated with `html-validate`.
- Patch whitespace validated with `git diff --check`.
- Chinese workshop page and shared CSS/JavaScript assets loaded from a local
  HTTP preview.
- Desktop and mobile renders were generated at 1440 x 1100 and 390 x 844.

## Workshop v1 static archive - 2026-08-14

The version deployed before the Workshop v2 motion redesign is preserved by
the annotated Git tag `workshop-v1-static` at commit `52bdcca`.

To inspect the archived version without changing the working branch:

```bash
git worktree add ../osome-workshop-v1 workshop-v1-static
```

To restore that version as a new commit on `master` if a production rollback
is required:

```bash
git revert --no-commit workshop-v1-static..master
git commit -m "Roll back to workshop v1 static"
git push origin master
```
