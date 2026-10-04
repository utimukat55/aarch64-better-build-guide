#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path


def num(s):
    s = s.strip().lower()
    if s.startswith('0x'):
        return int(s, 16)
    return int(s, 0)


def split_top_level_args(s):
    args, start, depth = [], 0, 0
    in_string = False
    esc = False
    for i, ch in enumerate(s):
        if in_string:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        elif ch == ',' and depth == 0:
            args.append(s[start:i].strip())
            start = i + 1
    args.append(s[start:].strip())
    return args


def extract_invocations(text, macro):
    marker = macro + '('
    pos = 0
    while True:
        i = text.find(marker, pos)
        if i < 0:
            return
        j = i + len(marker)
        depth = 1
        in_string = False
        esc = False
        while j < len(text) and depth:
            ch = text[j]
            if in_string:
                if esc:
                    esc = False
                elif ch == '\\':
                    esc = True
                elif ch == '"':
                    in_string = False
            else:
                if ch == '"':
                    in_string = True
                elif ch == '(':
                    depth += 1
                elif ch == ')':
                    depth -= 1
            j += 1
        if depth == 0:
            yield text[i + len(marker):j - 1]
        pos = j


def parse_cores(text):
    out = []
    for body in extract_invocations(text, 'AARCH64_CORE'):
        args = split_top_level_args(body)
        if len(args) != 9:
            continue
        name, ident, sched, arch, flags, costs, imp, part, variant = [x.strip() for x in args]
        if not (name.startswith('"') and name.endswith('"')):
            continue
        name = name[1:-1]
        if flags.startswith('(') and flags.endswith(')'):
            flags = flags[1:-1]
        impv = None if 'INVALID_IMP' in imp else num(imp)
        parts = []
        bm = re.fullmatch(r'AARCH64_BIG_LITTLE\s*\(\s*([^,]+)\s*,\s*([^\)]+)\s*\)', part)
        if bm:
            parts = [num(bm.group(1)), num(bm.group(2))]
        elif 'INVALID_CORE' not in part:
            try:
                parts = [num(part)]
            except ValueError:
                parts = []
        vv = None if variant.strip() == '-1' else num(variant)
        out.append((name, ident, arch, flags, impv, parts, vv))
    return out


def parse_arches(text):
    out = []
    for body in extract_invocations(text, 'AARCH64_ARCH'):
        args = split_top_level_args(body)
        if len(args) != 5:
            continue
        name, core, ident, revision, flags = [x.strip() for x in args]
        if not (name.startswith('"') and name.endswith('"')):
            continue
        name = unquote(name)
        if flags.startswith('(') and flags.endswith(')'):
            flags = flags[1:-1]
        out.append({
            'name': name,
            'core': core,
            'ident': ident,
            'revision': int(revision, 0),
            'flags': parse_flag_expr('(' + flags + ')'),
        })
    return out


def parse_enum(text):
    m = re.search(r'enum\s+CPUFeatures\s*\{(.*?)\n\s*\};', text, re.S)
    if not m:
        raise SystemExit('CPUFeatures enum not found')
    names = []
    for line in m.group(1).splitlines():
        line = line.split('/*', 1)[0].strip().rstrip(',')
        if not line or '=' in line:
            continue
        if re.fullmatch(r'FEAT_[A-Za-z0-9_]+', line):
            names.append(line)
    return names


def unquote(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return bytes(s[1:-1], 'utf-8').decode('unicode_escape')
    return s


def parse_option_extensions(text):
    extensions = {}
    fmv = {}

    # We parse the raw macro definitions, not the helper macro
    # AARCH64_OPT_FMV_EXTENSION, so the source's actual FMV relation is visible.
    for body in extract_invocations(text, 'AARCH64_OPT_EXTENSION'):
        args = split_top_level_args(body)
        if len(args) != 6:
            continue
        name, ident, requires, explicit_on, explicit_off, feature_string = args
        ident = ident.strip()
        extensions[ident] = {
            'name': unquote(name),
            'ident': ident,
            'requires': requires.strip(),
            'feature_string': unquote(feature_string),
        }

    for body in extract_invocations(text, 'AARCH64_OPT_EXTENSION_ALIAS'):
        args = split_top_level_args(body)
        if len(args) != 7:
            continue
        name, ident, requires, explicit_on, explicit_off, prefer, feature_string = args
        ident = ident.strip()
        extensions[ident] = {
            'name': unquote(name),
            'ident': ident,
            'requires': requires.strip(),
            'feature_string': unquote(feature_string),
            'alias': True,
        }

    # AARCH64_OPT_FMV_EXTENSION is a helper macro in the upstream file:
    # it creates both an OPT_EXTENSION and an FMV_FEATURE with OPT_FLAGS=(IDENT).
    for body in extract_invocations(text, 'AARCH64_OPT_FMV_EXTENSION'):
        args = split_top_level_args(body)
        if len(args) != 6:
            continue
        name, ident, requires, explicit_on, explicit_off, feature_string = args
        ident = ident.strip()
        extensions[ident] = {
            'name': unquote(name), 'ident': ident, 'requires': requires.strip(),
            'feature_string': unquote(feature_string)
        }
        fmv[ident] = {'name': unquote(name), 'feat_name': ident, 'opt_flags': '(' + ident + ')'}

    for body in extract_invocations(text, 'AARCH64_FMV_FEATURE'):
        args = split_top_level_args(body)
        if len(args) != 3:
            continue
        name, feat_name, opt_flags = args
        feat_name = feat_name.strip()
        fmv[feat_name] = {
            'name': unquote(name),
            'feat_name': feat_name,
            'opt_flags': opt_flags.strip(),
        }

    return extensions, fmv


def parse_flag_expr(expr):
    expr = expr.strip()
    if expr in ('()', ''):
        return []
    if expr.startswith('(') and expr.endswith(')'):
        expr = expr[1:-1]
    return [x.strip() for x in expr.split(',') if x.strip()]


def parse_or_expr(s):
    # For FEATURE_STRING: spaces mean AND; | means OR between alternatives.
    s = s.strip()
    if not s:
        return []
    return [[x for x in alt.strip().split() if x] for alt in s.split('|') if alt.strip()]


def expr_to_text(expr):
    if not expr:
        return ''
    return ' OR '.join(' AND '.join(a) for a in expr)


def transitive_requires(ident, extensions, memo=None, visiting=None):
    memo = {} if memo is None else memo
    visiting = set() if visiting is None else visiting
    if ident in memo:
        return memo[ident]
    if ident in visiting:
        raise SystemExit('cyclic extension dependency involving ' + ident)
    visiting.add(ident)
    e = extensions.get(ident)
    if not e:
        result = []
    else:
        result = []
        for dep in parse_flag_expr(e['requires']):
            for x in transitive_requires(dep, extensions, memo, visiting):
                if x not in result:
                    result.append(x)
            if dep not in result:
                result.append(dep)
    visiting.remove(ident)
    memo[ident] = result
    return result


def feature_records(feats, extensions, fmv):
    records = []
    aliases = {
        'RDMA': 'RDM',
        'MEMTAG': 'MEMTAG2',
        'SSBS': 'SSBS2',
    }
    # AARCH64_FMV_FEATURE uses unprefixed FEAT names, so the enum is the
    # authoritative list.  If an enum feature has no FMV record, report it.
    for feat in feats:
        suffix = feat[5:]
        key = aliases.get(suffix, suffix)
        rec = fmv.get(key)
        if rec is None:
            records.append({
                'feat': feat, 'fmv_name': '', 'opt_flags': [],
                'direct_flags': [], 'requires': [], 'runtime': [],
                'runtime_text': '', 'note': 'no AARCH64_FMV_FEATURE record in aarch64-option-extensions.def'
            })
            continue
        opt_flags = parse_flag_expr(rec['opt_flags'])
        # Resolve direct FMV OPT_FLAGS and the extension definitions they point to.
        closure = []
        for fl in opt_flags:
            if fl not in closure:
                closure.append(fl)
            for dep in transitive_requires(fl, extensions):
                if dep not in closure:
                    closure.append(dep)
        runtime_parts = []
        for fl in opt_flags:
            e = extensions.get(fl)
            if e and e.get('feature_string'):
                parts = parse_or_expr(e['feature_string'])
                if len(parts) == 1:
                    runtime_parts.append(' AND '.join(parts[0]))
                elif parts:
                    runtime_parts.append('(' + ' OR '.join(' AND '.join(x) for x in parts) + ')')
        if not runtime_parts:
            e = extensions.get(key)
            if e and e.get('feature_string'):
                runtime_parts.append(expr_to_text(parse_or_expr(e['feature_string'])))
        # For aliases such as RDM, the FMV name is an alias but runtime data lives on RDMA.
        if not runtime_parts and key in ('RDM', 'MEMTAG2', 'SSBS2'):
            base = {'RDM': 'RDMA', 'MEMTAG2': 'MEMTAG', 'SSBS2': 'SSBS'}[key]
            e = extensions.get(base)
            if e and e.get('feature_string'):
                runtime_parts.append(expr_to_text(parse_or_expr(e['feature_string'])))
        records.append({
            'feat': feat,
            'fmv_name': rec['name'],
            'opt_flags': opt_flags,
            'direct_flags': opt_flags,
            'requires': closure,
            'runtime': parse_or_expr(' | '.join(runtime_parts)),
            'runtime_text': ' AND '.join(runtime_parts),
            'note': ''
        })
    return records


def feature_for_extension_ident(ident, fmv):
    aliases = {'RDMA': 'RDM', 'MEMTAG': 'MEMTAG2', 'SSBS': 'SSBS2'}
    # Prefer an FMV record whose OPT_FLAGS directly names this extension.
    for suffix, rec in fmv.items():
        if ident in parse_flag_expr(rec['opt_flags']):
            return 'FEAT_' + aliases.get(suffix, suffix)
    # Otherwise the extension itself may be a dependency of a composite
    # option; its runtime feature has the same spelling when an FMV record
    # exists, including the usual GCC aliases above.
    if ident in fmv:
        return 'FEAT_' + aliases.get(ident, ident)
    return None


def core_flag_enable_candidate(core_flag, extensions, fmv):
    """Return (option, required FEAT_* names) for a positive core modifier."""
    ext = extensions.get(core_flag)
    if ext is None:
        return None
    option = ext.get('name', '')
    if not option:
        return None
    req = []
    # A direct FMV feature is the most precise runtime test.
    direct = feature_for_extension_ident(core_flag, fmv)
    if direct:
        req.append(direct)
    # Composite/alias options require all runtime features corresponding to
    # their transitive extension dependencies. This covers e.g.
    # SVE2_BITPERM -> SVE2 + SVE_BITPERM.
    for dep in transitive_requires(core_flag, extensions):
        feat = feature_for_extension_ident(dep, fmv)
        if feat and feat not in req:
            req.append(feat)
    # An option with no runtime FEAT representation (PROFILE, LS64, etc.)
    # cannot safely be emitted as a positive modifier.
    if not req:
        return None
    return option, req

def core_flag_disable_candidates(core_flag, extensions, fmv):
    """Return runtime-detectable GCC negative options for one core flag.

    The exact core flag is the root.  Only that option and its transitive
    REQUIRES dependencies are considered; unrelated FMV extensions that merely
    share a prerequisite (for example SVE2-AES and SVE2-BITPERM both requiring
    SVE2) must not be emitted.
    """
    closure = [core_flag] + transitive_requires(core_flag, extensions)
    items = []
    seen = set()

    # Preserve dependency order while mapping each extension IDENT to its GCC
    # option spelling and runtime FEAT_* representation.
    for ident in closure:
        ext = extensions.get(ident)
        option = ext.get('name', '') if ext else ''
        if not option:
            continue

        feat = None
        if ident in fmv:
            suffix = ident
            feat_suffix = {'MEMTAG': 'MEMTAG2', 'SSBS': 'SSBS2'}.get(suffix, suffix)
            feat = 'FEAT_' + feat_suffix
        else:
            # Aliased GCC options can have the runtime feature under a distinct
            # FEAT name, as with MEMTAG/SSBS/RDMA.
            for suffix, rec in fmv.items():
                if ident in parse_flag_expr(rec['opt_flags']):
                    feat_suffix = {'MEMTAG': 'MEMTAG2', 'SSBS': 'SSBS2', 'RDMA': 'RDM'}.get(suffix, suffix)
                    feat = 'FEAT_' + feat_suffix
                    break
        if not feat:
            continue

        prereq = []
        for dep in transitive_requires(ident, extensions):
            dep_ext = extensions.get(dep)
            dep_option = dep_ext.get('name', '') if dep_ext else ''
            if dep_option and dep_option not in prereq:
                prereq.append(dep_option)
        key = (option, feat)
        if key in seen:
            continue
        seen.add(key)
        items.append((option, feat, ','.join(prereq)))

    return items

def parse_lscpu_arm(text):
    """Parse util-linux lscpu-arm.c's hw_implementer -> id_part database."""
    arrays = {}
    # The supplied source uses simple static const struct id_part arrays.
    for m in re.finditer(r'static\s+const\s+struct\s+id_part\s+(\w+)\[\]\s*=\s*\{(.*?)\};', text, re.S):
        name, body = m.group(1), m.group(2)
        rows = []
        for e in re.finditer(r'\{\s*([^,}]+)\s*,\s*"([^"]*)"\s*(?:,\s*[^}]*)?\}', body):
            try:
                ident = int(e.group(1).strip(), 0)
            except ValueError:
                continue
            if ident == -1:
                continue
            rows.append((ident, e.group(2)))
        arrays[name] = rows

    impls = []
    m = re.search(r'static\s+const\s+struct\s+hw_impl\s+hw_implementer\[\]\s*=\s*\{(.*?)\};', text, re.S)
    if not m:
        raise SystemExit('hw_implementer[] not found in lscpu-arm.c')
    for e in re.finditer(r'\{\s*([^,}]+)\s*,\s*(\w+)\s*,\s*"([^"]*)"', m.group(1)):
        try:
            ident = int(e.group(1).strip(), 0)
        except ValueError:
            continue
        if ident == -1:
            continue
        parts = e.group(2)
        if parts not in arrays:
            raise SystemExit('part array %s referenced by hw_implementer is missing' % parts)
        impls.append((ident, parts, e.group(3)))
    return arrays, impls

def cppstr(s):
    return json.dumps(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cores', required=True)
    ap.add_argument('--arches', required=True)
    ap.add_argument('--cpuinfo-h', required=True)
    ap.add_argument('--option-extensions', required=True)
    ap.add_argument('--feature-deps-h', required=True)
    ap.add_argument('--lscpu-arm', required=True)
    ap.add_argument('--out-dir', required=True)
    a = ap.parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    core_text = Path(a.cores).read_text()
    cpuinfo_text = Path(a.cpuinfo_h).read_text()
    ext_text = Path(a.option_extensions).read_text()
    # Read to make the dependency input an explicit, tracked source. The
    # actual dependency semantics are reconstructed from option-extensions.def.
    Path(a.feature_deps_h).read_text()
    lscpu_text = Path(a.lscpu_arm).read_text()

    arches_text = Path(a.arches).read_text()
    arches = parse_arches(arches_text)
    cores = parse_cores(core_text)
    feats = parse_enum(cpuinfo_text)
    extensions, fmv = parse_option_extensions(ext_text)
    records = feature_records(feats, extensions, fmv)

    arch_by_ident = {x['ident']: x for x in arches}
    ext_by_ident = extensions
    arch_memo = {}
    ext_memo = {}

    def resolve_ext(ident, visiting=None):
        if ident in ext_memo:
            return list(ext_memo[ident])
        visiting = set() if visiting is None else visiting
        if ident in visiting:
            raise SystemExit('cyclic extension/architecture dependency involving ' + ident)
        visiting.add(ident)
        e = ext_by_ident.get(ident)
        result = []
        if e is not None:
            for dep in parse_flag_expr(e['requires']):
                for x in resolve_ident(dep, visiting):
                    if x not in result:
                        result.append(x)
            if ident not in result:
                result.append(ident)
        visiting.remove(ident)
        ext_memo[ident] = result
        return list(result)

    def resolve_arch(ident, visiting=None):
        if ident in arch_memo:
            return list(arch_memo[ident])
        visiting = set() if visiting is None else visiting
        if ident in visiting:
            raise SystemExit('cyclic architecture dependency involving ' + ident)
        visiting.add(ident)
        adef = arch_by_ident.get(ident)
        result = []
        if adef is not None:
            for dep in adef['flags']:
                for x in resolve_ident(dep, visiting):
                    if x not in result:
                        result.append(x)
        visiting.remove(ident)
        arch_memo[ident] = result
        return list(result)

    def resolve_ident(ident, visiting=None):
        if ident in arch_by_ident:
            return resolve_arch(ident, visiting)
        if ident in ext_by_ident:
            return resolve_ext(ident, visiting)
        # Unknown identifiers are retained so a source update cannot silently
        # disappear from the generated architecture report.
        return [ident]

    # The source file is ordered from older to newer architecture levels.
    # The first architecture in that order whose recursive enable closure adds
    # an option is therefore the architecture that introduced it.
    introduced = {}
    arch_rows = []
    # Keep the complete extension dependency graph, not only options that happen
    # to occur in an architecture baseline.  Core FLAGS can reference composite
    # extensions such as SVE2_BITPERM whose child options must also participate
    # in redundant +no... suppression.
    arch_option_rows = {}
    for ident, ext in ext_by_ident.items():
        option = ext['name']
        req_options = []
        for dep in parse_flag_expr(ext['requires']):
            dep_ext = ext_by_ident.get(dep)
            dep_option = dep_ext['name'] if dep_ext is not None else dep.lower()
            if dep_option not in req_options:
                req_options.append(dep_option)
        arch_option_rows[option] = req_options
    for adef in arches:
        opts = resolve_arch(adef['ident'])
        for ident in opts:
            ext = ext_by_ident.get(ident)
            option = ext['name'] if ext is not None else ident.lower()
            if option not in introduced:
                introduced[option] = adef['name']
            if ext is not None and option not in arch_option_rows:
                req_options = []
                for dep in parse_flag_expr(ext['requires']):
                    dep_ext = ext_by_ident.get(dep)
                    dep_option = dep_ext['name'] if dep_ext is not None else dep.lower()
                    if dep_option not in req_options:
                        req_options.append(dep_option)
                arch_option_rows[option] = req_options
        # Keep options unique while preserving the recursive GCC dependency order.
        unique_opts = []
        unique_reasons = []
        for ident in opts:
            option = ext_by_ident[ident]['name'] if ident in ext_by_ident else ident.lower()
            if option in unique_opts:
                continue
            unique_opts.append(option)
            unique_reasons.append(introduced[option])
        arch_rows.append((adef, unique_opts, unique_reasons))

    with (out / 'architecture_table.inc').open('w') as f:
        f.write('// Generated from upstream gcc/config/aarch64/aarch64-arches.def + aarch64-option-extensions.def dependency semantics.\n')
        f.write('struct ArchOptionRecord { const char *option,*requires; };\n')
        f.write('static const ArchOptionRecord arch_option_table[] = {\n')
        for option, reqs in arch_option_rows.items():
            f.write('{%s,%s},\n' % (cppstr(option), cppstr(','.join(reqs))))
        f.write('};\n')
        f.write('static const unsigned arch_option_table_count = sizeof(arch_option_table)/sizeof(arch_option_table[0]);\n')
        f.write('struct ArchRecord { const char *name,*core,*ident; unsigned revision; const char *options,*introduced; };\n')
        f.write('static const ArchRecord arch_table[] = {\n')
        for adef, opts, reasons in arch_rows:
            f.write('{%s,%s,%s,%d,%s,%s},\n' % (
                cppstr(adef['name']), cppstr(adef['core']), cppstr(adef['ident']),
                adef['revision'], cppstr(','.join(opts)), cppstr(','.join(reasons))))
        f.write('};\n')
        f.write('static const unsigned arch_table_count = sizeof(arch_table)/sizeof(arch_table[0]);\n')

    lscpu_arrays, lscpu_impls = parse_lscpu_arm(lscpu_text)
    with (out / 'lscpu_table.inc').open('w') as f:
        f.write('// Generated from upstream/util-linux/sys-utils/lscpu-arm.c.\n')
        f.write('struct LscpuPartRecord { unsigned id; const char *name; };\n')
        for name, rows in lscpu_arrays.items():
            f.write('static const LscpuPartRecord lscpu_parts_%s[] = {\n' % name)
            for ident, pname in rows:
                f.write('{%s,%s},\n' % (hex(ident), cppstr(pname)))
            f.write('};\n')
        f.write('struct LscpuImplementerRecord { unsigned id; const LscpuPartRecord *parts; unsigned part_count; const char *name; };\n')
        f.write('static const LscpuImplementerRecord lscpu_implementer_table[] = {\n')
        for ident, parts, name in lscpu_impls:
            f.write('{%s,lscpu_parts_%s,sizeof(lscpu_parts_%s)/sizeof(lscpu_parts_%s[0]),%s},\n' % (hex(ident), parts, parts, parts, cppstr(name)))
        f.write('};\n')
        f.write('static const unsigned lscpu_implementer_count = sizeof(lscpu_implementer_table)/sizeof(lscpu_implementer_table[0]);\n')
        for name, rows in lscpu_arrays.items():
            f.write('static const unsigned lscpu_parts_%s_count = sizeof(lscpu_parts_%s)/sizeof(lscpu_parts_%s[0]);\n' % (name, name, name))

    with (out / 'core_table.inc').open('w') as f:
        f.write('// Generated from upstream gcc/config/aarch64/aarch64-cores.def.\n')
        f.write('struct CoreRecord { const char *name,*ident,*arch; const char *flags; unsigned implementer; const unsigned *parts; unsigned part_count; int variant; };\n')
        for i, (_, _, _, _, _, parts, _) in enumerate(cores):
            f.write('static const unsigned core_parts_%d[] = {%s};\n' % (i, ','.join(hex(x) for x in parts)))
        f.write('static const CoreRecord core_table[] = {\n')
        for i, (name, ident, arch, flags, imp, parts, var) in enumerate(cores):
            fs = ','.join(x.strip() for x in flags.split(',') if x.strip())
            imp_s = '0' if imp is None else hex(imp)
            var_s = '-1' if var is None else str(var)
            f.write('{%s,%s,%s,%s,%s,core_parts_%d,%d,%s},\n' %
                    (cppstr(name), cppstr(ident), cppstr(arch), cppstr(fs), imp_s, i, len(parts), var_s))
        f.write('};\n')
        f.write('static const unsigned core_table_count = sizeof(core_table)/sizeof(core_table[0]);\n')

    with (out / 'feature_table.inc').open('w') as f:
        f.write('// Generated from cpuinfo.h + aarch64-option-extensions.def + aarch64-feature-deps.h semantics.\n')
        f.write('struct FeatureRecord { const char *name,*fmv_name,*direct_flags,*direct_options,*closure_flags,*runtime_condition,*note; };\n')
        f.write('static const FeatureRecord feature_table[] = {\n')
        for r in records:
            direct = ' AND '.join(r['direct_flags'])
            direct_options = []
            for fl in r['direct_flags']:
                ext = extensions.get(fl)
                if ext and ext.get('name') and ext['name'] not in direct_options:
                    direct_options.append(ext['name'])
            direct_options_text = ','.join(direct_options)
            closure = ' AND '.join(r['requires'])
            f.write('{%s,%s,%s,%s,%s,%s,%s},\n' % (
                cppstr(r['feat']), cppstr(r['fmv_name']), cppstr(direct), cppstr(direct_options_text), cppstr(closure),
                cppstr(r['runtime_text']), cppstr(r['note'])))
        f.write('};\n')
        f.write('static const unsigned feature_table_count = sizeof(feature_table)/sizeof(feature_table[0]);\n')
        f.write('static const char *const cpu_feature_names[] = {\n')
        for n in feats:
            f.write(cppstr(n) + ',\n')
        f.write('};\nstatic const unsigned cpu_feature_count = sizeof(cpu_feature_names)/sizeof(cpu_feature_names[0]);\n')

    with (out / 'flag_table.inc').open('w') as f:
        f.write('// Generated mapping from GCC core FLAGS to CPUFeatures.\n')
        all_flags = []
        for _, _, _, flags, *_ in cores:
            for fl in parse_flag_expr('(' + flags + ')'):
                if fl not in all_flags:
                    all_flags.append(fl)
        by_direct = {}
        for r in records:
            for fl in r['direct_flags']:
                by_direct.setdefault(fl, []).append(r['feat'])
        f.write('struct DisableCandidate { const char *option,*feature,*prereq_features; };\n')
        disable_rows = []
        f.write('struct FlagRecord { const char *flag,*features,*status,*positive_option,*positive_features; unsigned disable_first,disable_count; };\n')
        f.write('static const DisableCandidate disable_candidates[] = {\n')
        for fl in all_flags:
            for option, feat, prereqs in core_flag_disable_candidates(fl, extensions, fmv):
                f.write('{%s,%s,%s},\n' % (cppstr(option), cppstr(feat), cppstr(' AND '.join(prereqs))))
                disable_rows.append(fl)
        f.write('};\n')
        # Reconstruct ranges in the same order as disable_candidates.
        cursor=0
        f.write('static const FlagRecord flag_table[] = {\n')
        for fl in all_flags:
            fs = by_direct.get(fl, [])
            status = 'direct FMV mapping' if fs else 'no direct FEAT_* FMV mapping in supplied sources'
            features = ' OR '.join(fs) if fs else ''
            rows = core_flag_disable_candidates(fl, extensions, fmv)
            pos = core_flag_enable_candidate(fl, extensions, fmv)
            pos_opt = pos[0] if pos else ''
            pos_feats = ' AND '.join(pos[1]) if pos else ''
            f.write('{%s,%s,%s,%s,%s,%d,%d},\n' % (cppstr(fl), cppstr(features), cppstr(status), cppstr(pos_opt), cppstr(pos_feats), cursor, len(rows)))
            cursor += len(rows)
        f.write('};\nstatic const unsigned flag_table_count = sizeof(flag_table)/sizeof(flag_table[0]);\n')

    print(f'generated {len(arches)} architecture records, {len(cores)} CPU records, {len(feats)} FEAT records, {len(all_flags)} core FLAGS')

if __name__ == '__main__':
    main()
