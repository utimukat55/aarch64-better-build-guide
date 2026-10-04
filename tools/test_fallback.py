#!/usr/bin/env python3
import re
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
bin_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / 'build/aarch64-better-build-guide'
gen_feature = Path(sys.argv[2]) if len(sys.argv) > 2 else root / 'build/generated/feature_table.inc'

text = gen_feature.read_text()
part = text.split('static const char *const cpu_feature_names[] = {', 1)[1]
names = re.findall(r'"(FEAT_[A-Za-z0-9_]+)"', part)

def mask_for(*wanted):
    return sum(1 << names.index(x) for x in wanted)

def run(cpuinfo, mask):
    env = dict(__import__('os').environ)
    env['AARCH64_NATIVE_MCPU_CPUINFO'] = str(cpuinfo)
    env['AARCH64_NATIVE_MCPU_FEATURE_MASK'] = hex(mask)
    return subprocess.check_output([str(bin_path)], env=env, text=True)

qcom = root / 'tests/qcom.cpuinfo'
mask = mask_for('FEAT_FP', 'FEAT_SIMD', 'FEAT_LSE', 'FEAT_CRC', 'FEAT_SHA2', 'FEAT_PMULL', 'FEAT_FP16')
out = run(qcom, mask)
assert 'CPU matched GCC options with runtime derived modifiers:' in out
assert 'GCC-unmatched CPU fallback:' in subprocess.check_output([str(bin_path), '-v'], env=dict(__import__('os').environ, AARCH64_NATIVE_MCPU_CPUINFO=str(qcom), AARCH64_NATIVE_MCPU_FEATURE_MASK=hex(mask)), text=True)
assert out.count('-> -march=armv8-a+lse+crc+sha2+aes+fp16') == 2
assert 'Runtime CPU features detected' not in out
assert 'FEAT_* -> GCC FLAGS' not in out
assert 'upstream files derived from' not in out
assert 'GCC-unmatched CPU fallback:' not in out
assert 'For more detailed information, add -v/--verbose.' in out
verbose = subprocess.check_output([str(bin_path), '-v'], env=dict(__import__('os').environ, AARCH64_NATIVE_MCPU_CPUINFO=str(qcom), AARCH64_NATIVE_MCPU_FEATURE_MASK=hex(mask)), text=True)
assert 'Qualcomm / Kryo-3XX-Silver' in verbose
assert 'Qualcomm / Kryo-3XX-Gold' in verbose
assert 'GCC definition: not found' in verbose
assert 'upstream files derived from https://github.com/gcc-mirror/gcc' in verbose
assert 'gcc/common/config/aarch64/cpuinfo.h at commit 790e293' in verbose
assert 'gcc/config/aarch64/aarch64-arches.def at commit 254a858' in verbose
assert 'gcc/config/aarch64/aarch64-cores.def at commit 2f7613d' in verbose
assert 'gcc/config/aarch64/aarch64-feature-deps.h at commit 254a858' in verbose
assert 'gcc/config/aarch64/aarch64-option-extensions.def at commit 37dcc82' in verbose
assert 'gcc/config/aarch64/aarch64-c.cc at commit b610d8c' in verbose
assert 'libgcc/config/aarch64/cpuinfo.c at commit e3d2277' in verbose
assert 'upstream files derived from https://github.com/util-linux/util-linux' in verbose
assert 'sys-utils/lscpu-arm.c at commit 4b53cfd' in verbose
assert 'GCC requires: DOTPROD and FP and SIMD' in verbose
assert 'runtime condition: sm3 AND sm4' in verbose

for missing in ('FEAT_FP', 'FEAT_SIMD'):
    wanted = ['FEAT_FP', 'FEAT_SIMD', 'FEAT_LSE']
    wanted.remove(missing)
    out = run(qcom, mask_for(*wanted))
    assert 'GCC-unmatched CPU fallback:' not in out

matched = root / 'fake-a76'
out = run(matched, mask_for('FEAT_FP', 'FEAT_SIMD'))
assert '-mcpu=cortex-a76' in out
assert 'GCC-unmatched CPU fallback:' not in out
print('fallback tests: OK')
