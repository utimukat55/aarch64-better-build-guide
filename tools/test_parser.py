#!/usr/bin/env python3
import importlib.util
from pathlib import Path

root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gen', root/'tools/generate_tables.py')
gen=importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)
cores=gen.parse_cores((root/'upstream/gcc/config/aarch64/aarch64-cores.def').read_text())
row=next(x for x in cores if x[0]=='cortex-a76.cortex-a55')
assert row[4] == 0x41
assert row[5] == [0xd0b,0xd05]
exts,fmv=gen.parse_option_extensions((root/'upstream/gcc/config/aarch64/aarch64-option-extensions.def').read_text())
assert gen.transitive_requires('DOTPROD',exts) == ['FP','SIMD','DOTPROD'] or gen.transitive_requires('DOTPROD',exts) == ['FP','SIMD']
# Direct mappings explicitly required by the supplied definitions.
assert fmv['DOTPROD']['opt_flags'] == '(DOTPROD)'
assert fmv['PMULL']['opt_flags'] == '(AES)'
assert fmv['SVE_PMULL128']['opt_flags'] == '(SVE2, SVE_AES)'
print('parser tests: OK')


# GCC source-level regression check for Cortex-X4 and its runtime dependencies.
cores = gen.parse_cores((root/'upstream/gcc/config/aarch64/aarch64-cores.def').read_text())
x4 = [c for c in cores if c[0] == 'cortex-x4']
assert len(x4) == 1 and x4[0][4] == 0x41 and x4[0][5] == [0xd82]

ext_text = (root/'upstream/gcc/config/aarch64/aarch64-option-extensions.def').read_text()
extensions, fmv = gen.parse_option_extensions(ext_text)
assert 'SVE' in gen.transitive_requires('SVE2_BITPERM', extensions)
assert any(x[0] == 'memtag' and x[1] == 'FEAT_MEMTAG2' for x in gen.core_flag_disable_candidates('MEMTAG', extensions, fmv))
assert any(x[0] == 'sve' and x[1] == 'FEAT_SVE' for x in gen.core_flag_disable_candidates('SVE2_BITPERM', extensions, fmv))

assert gen.core_flag_enable_candidate('DOTPROD', exts, fmv) == ('dotprod', ['FEAT_DOTPROD', 'FEAT_FP', 'FEAT_SIMD'])
assert gen.core_flag_enable_candidate('F16', exts, fmv) == ('fp16', ['FEAT_FP16', 'FEAT_FP'])
assert gen.core_flag_enable_candidate('MEMTAG', exts, fmv) == ('memtag', ['FEAT_MEMTAG2'])
assert gen.core_flag_enable_candidate('PROFILE', exts, fmv) is None
print('positive modifier tests: OK')

# Architecture-baseline regression checks generated from aarch64-arches.def.
arch_text = (root/'upstream/gcc/config/aarch64/aarch64-arches.def').read_text()
arches = gen.parse_arches(arch_text)
assert len(arches) == 18
assert next(a for a in arches if a['ident'] == 'V8_5A')['name'] == 'armv8.5-a'
assert next(a for a in arches if a['ident'] == 'V9_2A')['flags'] == ['V8_7A', 'V9_1A']

# Reconstruct the same recursive architecture closure used by the generator.
arch_by_ident = {a['ident']: a for a in arches}
arch_memo = {}
ext_memo = {}
def resolve_ext(ident, visiting=None):
    if ident in ext_memo: return list(ext_memo[ident])
    visiting = set() if visiting is None else visiting
    assert ident not in visiting
    visiting.add(ident)
    result=[]
    for dep in gen.parse_flag_expr(exts[ident]['requires']):
        for x in resolve_ident(dep, visiting):
            if x not in result: result.append(x)
    if ident not in result: result.append(ident)
    visiting.remove(ident); ext_memo[ident]=result
    return list(result)
def resolve_arch(ident, visiting=None):
    if ident in arch_memo: return list(arch_memo[ident])
    visiting = set() if visiting is None else visiting
    assert ident not in visiting
    visiting.add(ident)
    result=[]
    for dep in arch_by_ident[ident]['flags']:
        for x in resolve_ident(dep, visiting):
            if x not in result: result.append(x)
    visiting.remove(ident); arch_memo[ident]=result
    return list(result)
def resolve_ident(ident, visiting=None):
    if ident in arch_by_ident: return resolve_arch(ident, visiting)
    return resolve_ext(ident, visiting) if ident in exts else [ident]

def option_names(ident):
    return [exts[x]['name'] if x in exts else x.lower() for x in resolve_arch(ident)]

v85 = option_names('V8_5A')
v92 = option_names('V9_2A')
assert 'frintts' in v85
assert 'frintts' in v92
assert 'sve2' in v92
assert 'mops' not in v92
print('architecture inheritance tests: OK')
