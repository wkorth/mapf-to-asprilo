# Examples

Two maps, "icecrown.map" from Warcraft 3, and "arena.map" from Dragon Age: Origins,
both pre- and post-conversion.

In this example, icecrown was converted from .map to .lp using

```bash
map-to-lp -i icecrown.map -o icecrown.lp
```

Alternatively, the same result could be reached by using

```bash
cat icecrown.map | map-to-lp > icecrown.lp_
```

or a mix between the two.
