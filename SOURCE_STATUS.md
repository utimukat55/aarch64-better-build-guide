# Source input status

The project contains seven tracked GCC AArch64 source inputs. They are treated as replaceable upstream inputs; the generator does not modify them.

- `aarch64-cores.def`: CPU/GCC definitions and core `FLAGS`.
- `aarch64-arches.def`: architecture names, architecture revisions, and recursive architecture `FLAGS`. This is now the authoritative source for the `-march` baseline and for the architecture that first introduced each omitted modifier.
- `aarch64-option-extensions.def`: `AARCH64_OPT_EXTENSION`, aliases, FMV records, `REQUIRES`, and Linux `FEATURE_STRING` data.
- `aarch64-feature-deps.h`: tracked source input; the standalone generator reconstructs its relevant `get_enable()` closure from the extension/architecture definitions.
- `cpuinfo.h`: authoritative `FEAT_*` enumeration.
- `cpuinfo.c`: runtime feature detection logic compiled into the tool.
- `aarch64.cc`: tracked GCC backend source used for source-version auditing, including GCC-side feature aliases such as `MEMTAG`/`FEAT_MEMTAG2` and `SSBS`/`FEAT_SSBS2`.

## Architecture baseline generation

`tools/generate_tables.py` parses `aarch64-arches.def` and recursively resolves its architecture identifiers and extension identifiers. Extension `REQUIRES` are expanded in the same direction as `aarch64-feature-deps.h`'s `get_enable()`. The generated architecture table records:

- GCC `-march` spelling (`armv9.2-a`, etc.)
- recursive baseline GCC option set
- the first architecture that introduced each option
- extension dependency edges used to suppress redundant `+no...` modifiers

This replaces the v7 hand-written architecture baseline table. In particular, `FRINTTS` is no longer missing from the omission reference: `V8_5A` directly contains `FRINTTS`, so later architectures that inherit it report `frintts (omitted by including in armv8.5-a)`.

## Generated files

The build generates `architecture_table.inc` in addition to the core, feature, and flag tables. The generated file is build output and is not an upstream source input.

## util-linux ARM CPU database

`upstream/util-linux/sys-utils/lscpu-arm.c` is tracked as the source of the `hw_implementer[]` and `id_part[]` CPU-name database used by the GCC-unmatched fallback. The generated `lscpu_table.inc` preserves the implementer -> part-array relationship and the product names from that source.

The fallback does not use a separate Qualcomm-only table. It first follows `hw_implementer[]`, then the selected `id_part[]` array, exactly as the source structure specifies.

The upstream tree used for this build was replaced wholesale from the attached `upstream.tar.gz`.

The verbose source attribution uses the commit identifiers supplied for this project, including the requested `gcc/config/aarch64/aarch64-c.cc at commit b610d8c` label. The attached tree itself contains `gcc/config/aarch64/aarch64.cc`; it is retained unchanged as supplied.
