/* aarch64 better build guide
   Copyright (C) 2026 utimukat55

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <string>
#include <vector>
#include <cctype>
#include <algorithm>
#include <cstdlib>

extern "C" uint64_t native_cpu_feature_mask(void);
#include "core_table.inc"
#include "feature_table.inc"
#include "flag_table.inc"
#include "architecture_table.inc"
#include "lscpu_table.inc"

struct CpuId { unsigned implementer=0, part=0, variant=0, count=0; bool have_imp=false, have_part=false, have_variant=false; };

static std::vector<CpuId> read_cpuinfo() {
  const char *override_path = std::getenv("AARCH64_NATIVE_MCPU_CPUINFO");
  std::ifstream f(override_path && *override_path ? override_path : "/proc/cpuinfo");
  std::vector<CpuId> v; CpuId c; std::string line;
  auto finish=[&](){ if(c.have_imp || c.have_part) v.push_back(c); c=CpuId{}; };
  while(std::getline(f,line)) {
    if(line.empty()) { finish(); continue; }
    auto p=line.find(':'); if(p==std::string::npos) continue;
    std::string k=line.substr(0,p), x=line.substr(p+1);
    while(!x.empty() && std::isspace((unsigned char)x.front())) x.erase(x.begin());
    unsigned long val=0; try { val=std::stoul(x,nullptr,0); } catch(...) { continue; }
    if(k.find("CPU implementer")!=std::string::npos) { c.implementer=val; c.have_imp=true; }
    else if(k.find("CPU part")!=std::string::npos) { c.part=val; c.have_part=true; }
    else if(k.find("CPU variant")!=std::string::npos) { c.variant=val; c.have_variant=true; }
  }
  finish();
  std::vector<CpuId> u;
  for(auto x:v) {
    bool seen=false;
    for(auto &y:u) if(y.implementer==x.implementer && y.part==x.part &&
                       (!x.have_variant || !y.have_variant || y.variant==x.variant)) {
      ++y.count;
      seen=true;
      break;
    }
    if(!seen) { x.count=1; u.push_back(x); }
  }
  return u;
}

static bool id_matches_core(const CoreRecord &c, const CpuId &id) {
  if(c.part_count==0 || !id.have_imp || !id.have_part) return false;
  if(id.implementer != c.implementer) return false;
  bool ok=false;
  for(unsigned i=0;i<c.part_count;i++) if(c.parts[i]==id.part) { ok=true; break; }
  if(!ok) return false;
  if(c.variant>=0 && id.have_variant && (unsigned)c.variant!=id.variant) return false;
  return true;
}

static bool part_match(const CoreRecord &c, const std::vector<CpuId>& ids) {
  if(ids.empty() || c.part_count==0) return false;
  // A single-part record matches if any observed CPU has that part.
  // A BIG.LITTLE record matches only when every declared part is observed.
  if(c.part_count==1) {
    for(const auto &id: ids) if(id_matches_core(c,id)) return true;
    return false;
  }
  for(unsigned p=0;p<c.part_count;p++) {
    bool found=false;
    for(const auto &id: ids) {
      if(!id.have_imp || !id.have_part || id.implementer!=c.implementer) continue;
      if(id.part!=c.parts[p]) continue;
      if(c.variant>=0 && id.have_variant && (unsigned)c.variant!=id.variant) continue;
      found=true; break;
    }
    if(!found) return false;
  }
  return true;
}

static std::vector<const CoreRecord*> matches_for_id(const CpuId &id) {
  std::vector<const CoreRecord*> r;
  for(unsigned i=0;i<core_table_count;i++)
    if(id_matches_core(core_table[i], id) && core_table[i].part_count==1) r.push_back(&core_table[i]);
  return r;
}

static std::vector<std::string> split_csv(const char *s) {
  std::vector<std::string> r; std::string x(s?s:""); std::stringstream ss(x); std::string t;
  while(std::getline(ss,t,',')) if(!t.empty()) r.push_back(t);
  return r;
}
static std::string hexv(unsigned x) { std::ostringstream o; o<<"0x"<<std::hex<<x; return o.str(); }
static bool runtime_feature_present(uint64_t mask,const std::string& name) {
  for(unsigned i=0;i<cpu_feature_count && i<64;i++) if(name==cpu_feature_names[i]) return (mask&(1ULL<<i))!=0;
  return false;
}
static bool hidden(const std::string& n) { return n.rfind("FEAT_unused",0)==0 || n=="FEAT_MAX" || n=="FEAT_EXT" || n=="FEAT_INIT"; }


static std::vector<std::string> architecture_baseline_options(const std::string& arch);

struct LscpuIdentification {
  bool implementer_found = false;
  bool part_found = false;
  std::string implementer_name;
  std::string product_name;
};

static const LscpuImplementerRecord* find_lscpu_implementer(unsigned implementer) {
  for (unsigned i = 0; i < lscpu_implementer_count; ++i)
    if (lscpu_implementer_table[i].id == implementer)
      return &lscpu_implementer_table[i];
  return nullptr;
}

static LscpuIdentification lscpu_identify(const CpuId &id) {
  LscpuIdentification out;
  const auto *impl = find_lscpu_implementer(id.implementer);
  if (!impl) return out;
  out.implementer_found = true;
  out.implementer_name = impl->name;
  if (!id.have_part) return out;
  for (unsigned i = 0; i < impl->part_count; ++i) {
    if (impl->parts[i].id == id.part) {
      out.part_found = true;
      out.product_name = impl->parts[i].name;
      return out;
    }
  }
  return out;
}

static std::string fallback_armv8_cpu_flags(uint64_t mask) {
  std::vector<std::string> out;
  const auto baseline = architecture_baseline_options("V8A");
  for (unsigned i = 0; i < feature_table_count; ++i) {
    const auto &r = feature_table[i];
    if (hidden(r.name) || !r.direct_options[0]) continue;
    if (!runtime_feature_present(mask, r.name)) continue;
    std::istringstream ss(r.direct_options);
    std::string option;
    while (std::getline(ss, option, ',')) {
      if (option.empty()) continue;
      if (std::find(baseline.begin(), baseline.end(), option) != baseline.end()) continue;
      if (std::find(out.begin(), out.end(), option) == out.end()) out.push_back(option);
    }
  }
  std::string result;
  for (const auto &x : out) result += "+" + x;
  return result;
}

static std::string fallback_report_text(const std::vector<CpuId>& ids, uint64_t mask) {
  // This path is entered only when GCC did not identify any CPU. FP and SIMD
  // are the two required runtime checks before armv8-a is selected.
  if (ids.empty() || !runtime_feature_present(mask, "FEAT_FP") ||
      !runtime_feature_present(mask, "FEAT_SIMD")) return "";

  std::ostringstream out;
  out << "\nGCC-unmatched CPU fallback:\n";
  out << "  GCC definition: not found\n";
  out << "  FEAT_FP: present\n";
  out << "  FEAT_SIMD: present\n";
  out << "  fallback -march per observed CPU ID:\n";
  for (const auto &id : ids) {
    const auto decoded = lscpu_identify(id);
    out << "    implementer=" << hexv(id.implementer)
        << " part=" << hexv(id.part);
    if (id.have_variant) out << " variant=" << hexv(id.variant);
    out << " : -march=armv8-a" << fallback_armv8_cpu_flags(mask);
    if (decoded.implementer_found)
      out << " (" << decoded.implementer_name;
    if (decoded.part_found)
      out << " / " << decoded.product_name;
    if (decoded.implementer_found)
      out << ")";
    out << "\n";
  }
  return out.str();
}

static std::string feature_mapping_text() {
  std::ostringstream out;
  out << "\nFEAT_* -> GCC FLAGS / GCC dependency closure / Linux runtime condition:\n";
  for(unsigned i=0;i<feature_table_count;i++) {
    const auto&r=feature_table[i]; if(hidden(r.name)) continue;
    out << "  " << r.name;
    if(r.direct_flags[0]) out << " (" << r.direct_flags << ")"; else out << " (no direct FMV FLAG)";
    if(r.closure_flags[0]) {
      std::string requires = r.closure_flags;
      size_t pos = 0;
      while ((pos = requires.find(" AND ", pos)) != std::string::npos) { requires.replace(pos, 5, " and "); pos += 5; }
      while ((pos = requires.find(" OR ", pos)) != std::string::npos) { requires.replace(pos, 4, " or "); pos += 4; }
      out << "\n    GCC requires: " << requires;
    }
    if(r.runtime_condition[0]) out << "\n    runtime condition: " << r.runtime_condition;
    if(r.note[0]) out << "\n    note: " << r.note;
    out << "\n";
  }
  return out.str();
}

static std::string flag_mapping_text() {
  std::ostringstream out;
  out << "\nGCC aarch64-cores.def FLAGS -> FEAT_* mapping:\n";
  for(unsigned i=0;i<flag_table_count;i++) {
    const auto&r=flag_table[i]; out << "  " << r.flag;
    if(r.features[0]) out << " -> " << r.features; else out << " -> (no direct FEAT_* FMV mapping)";
    out << "\n";
  }
  return out.str();
}


static const ArchRecord* find_arch_record(const std::string& ident) {
  for (unsigned i=0; i<arch_table_count; ++i)
    if (ident == arch_table[i].ident) return &arch_table[i];
  return nullptr;
}

static std::string arch_option_name(const char *arch) {
  if (const auto *r = find_arch_record(arch ? arch : "")) return r->name;
  return arch ? arch : "unknown";
}

static std::vector<std::string> split_delimited(const char *s, char delimiter) {
  std::vector<std::string> out;
  std::string text = s ? s : "";
  std::string item;
  std::stringstream ss(text);
  while (std::getline(ss, item, delimiter))
    if (!item.empty()) out.push_back(item);
  return out;
}

static std::vector<std::string> architecture_baseline_options(const std::string& arch) {
  if (const auto *r = find_arch_record(arch))
    return split_delimited(r->options, ',');
  return {};
}

static std::string architecture_option_introduction(const std::string& arch,
                                                    const std::string& option) {
  const auto *r = find_arch_record(arch);
  if (!r) return "";
  const auto options = split_delimited(r->options, ',');
  const auto introductions = split_delimited(r->introduced, ',');
  for (size_t i=0; i<options.size() && i<introductions.size(); ++i)
    if (options[i] == option) return introductions[i];
  return "";
}

static bool architecture_implies_option(const std::string& arch, const std::string& option) {
  const auto base = architecture_baseline_options(arch);
  return std::find(base.begin(), base.end(), option) != base.end();
}

static std::vector<std::string> architecture_option_requires(const std::string& option) {
  for (unsigned i=0; i<arch_option_table_count; ++i)
    if (option == arch_option_table[i].option)
      return split_delimited(arch_option_table[i].requires, ',');
  return {};
}

static bool all_runtime_features_present(const char *feature_text, uint64_t mask) {
  std::istringstream ss(feature_text ? feature_text : "");
  std::string feat;
  bool any=false;
  while(ss >> feat) {
    if(feat=="AND") continue;
    any=true;
    if(!runtime_feature_present(mask, feat)) return false;
  }
  return any;
}

static std::string runtime_requirement_for_option(const std::string& option) {
  for (unsigned i=0; i<flag_table_count; ++i)
    if (option == flag_table[i].positive_option && flag_table[i].positive_features[0])
      return flag_table[i].positive_features;

  if (option == "crypto")
    return "FEAT_PMULL AND FEAT_SHA2";

  for (unsigned i=0; i<feature_table_count; ++i) {
    const auto &r = feature_table[i];
    if (option == r.fmv_name) {
      std::string feat = r.name;
      if (feat.rfind("FEAT_", 0) == 0)
        return feat;
    }
  }

  if (option == "f16fml") return "FEAT_FP16FML";
  if (option == "rdma") return "FEAT_RDM";
  if (option == "memtag") return "FEAT_MEMTAG2";
  if (option == "ssbs") return "FEAT_SSBS2";
  return "";
}

static bool runtime_requirement_present(const std::string& requirement, uint64_t mask) {
  if (requirement.empty()) return false;
  std::istringstream ss(requirement);
  std::string feat;
  bool any = false;
  while (ss >> feat) {
    if (feat == "AND") continue;
    any = true;
    if (!runtime_feature_present(mask, feat)) return false;
  }
  return any;
}

struct ModifierCandidate {
  std::string option;
  std::string feature;
  std::string prerequisites;
};

static bool option_depends_on(const std::string& option, const std::string& ancestor,
                               std::set<std::string>& visiting) {
  if (option == ancestor) return true;
  if (!visiting.insert(option).second) return false;
  for (const auto &dep : architecture_option_requires(option)) {
    if (dep == ancestor || option_depends_on(dep, ancestor, visiting)) {
      visiting.erase(option);
      return true;
    }
  }
  visiting.erase(option);
  return false;
}

static bool option_depends_on(const std::string& option, const std::string& ancestor) {
  std::set<std::string> visiting;
  return option_depends_on(option, ancestor, visiting);
}

static std::vector<ModifierCandidate> architecture_disable_candidates(const CoreRecord& c, uint64_t mask) {
  std::vector<ModifierCandidate> out;
  for (const auto &option : architecture_baseline_options(c.arch)) {
    const std::string req = runtime_requirement_for_option(option);
    if (req.empty() || runtime_requirement_present(req, mask)) continue;

    std::string feature;
    if (option == "crypto") feature = "FEAT_CRYPTO";
    else feature = req;
    out.push_back({option, feature, ""});
  }

  return out;
}

static std::vector<ModifierCandidate> reduce_architecture_missing(
    const std::vector<ModifierCandidate>& in) {
  std::vector<ModifierCandidate> work = in;
  std::vector<ModifierCandidate> roots;

  // Apply GCC's prerequisite hierarchy from the bottom upward.  A missing
  // prerequisite is enough to disable every architecture option that depends
  // on it.  This gives the desired single root modifier: +nofp, +nosimd,
  // +nofp16, +nofcma, or +nosve as applicable.
  static const char *const priority[] = {
    "fp", "simd", "fp16", "fcma", "sve"
  };
  for (const char *name : priority) {
    auto it = std::find_if(work.begin(), work.end(),
                           [&](const ModifierCandidate& x) { return x.option == name; });
    if (it == work.end()) continue;

    roots.push_back(*it);
    std::vector<ModifierCandidate> filtered;
    for (const auto &x : work) {
      if (x.option == name) continue;
      if (option_depends_on(x.option, name)) continue;
      filtered.push_back(x);
    }
    work.swap(filtered);
  }

  // For everything outside the fundamental FP/SIMD/SVE chain, retain a
  // higher-level missing option when its direct dependencies are also missing.
  for (size_t i=0; i<work.size(); ++i) {
    bool redundant = false;
    for (size_t j=0; j<work.size(); ++j) {
      if (i == j) continue;
      if (option_depends_on(work[j].option, work[i].option)) {
        redundant = true;
        break;
      }
    }
    if (!redundant) roots.push_back(work[i]);
  }
  return roots;
}

static std::string runtime_disable_modifiers(const CoreRecord &c, uint64_t mask) {
  std::vector<ModifierCandidate> arch_cs = architecture_disable_candidates(c, mask);
  std::vector<ModifierCandidate> roots = reduce_architecture_missing(arch_cs);

  // Core FLAGS are additional to the architecture baseline.  If an
  // architecture root such as +nosve already disables a core child, do not
  // emit that child's separate +no modifier.
  std::vector<ModifierCandidate> core_cs;
  for(const auto &fl: split_csv(c.flags)) {
    for(unsigned i=0;i<flag_table_count;i++) {
      if(fl != flag_table[i].flag) continue;
      for(unsigned j=0;j<flag_table[i].disable_count;j++) {
        const auto &d = disable_candidates[flag_table[i].disable_first + j];
        if(!runtime_feature_present(mask, d.feature))
          core_cs.push_back({d.option, d.feature, d.prereq_features});
      }
      break;
    }
  }

  std::vector<std::string> candidates;
  for (const auto &x : roots) candidates.push_back(x.option);
  for (const auto &x : core_cs) {
    bool covered = false;
    for (const auto &a : roots) {
      if (option_depends_on(x.option, a.option)
          || option_depends_on(a.option, x.option)
          || (a.option == "sve" && x.option.rfind("sve", 0) == 0)) {
        covered = true;
        break;
      }
    }
    if (!covered && std::find(candidates.begin(), candidates.end(), x.option) == candidates.end())
      candidates.push_back(x.option);
  }

  std::string out;
  for(const auto &x: candidates) out += "+no" + x;
  return out;
}

static std::string runtime_enable_modifiers_for_arch(const CoreRecord &c, uint64_t mask) {
  std::vector<std::string> out;
  for (const auto &fl : split_csv(c.flags)) {
    for (unsigned i=0;i<flag_table_count;i++) {
      if (fl != flag_table[i].flag) continue;
      const auto &fr=flag_table[i];
      std::string option=fr.positive_option;
      if(option.empty() || !all_runtime_features_present(fr.positive_features, mask)) break;
      if(architecture_implies_option(c.arch, option)) break;
      if(std::find(out.begin(),out.end(),option)==out.end()) out.push_back(option);
      break;
    }
  }
  std::string s;
  for(const auto &x:out) s += "+"+x;
  return s;
}

static std::string combined_modifiers(const CoreRecord &c, uint64_t mask) {
  return runtime_enable_modifiers_for_arch(c, mask) + runtime_disable_modifiers(c, mask);
}

static std::vector<std::string> omitted_modifier_notes(const CoreRecord& c, uint64_t mask) {
  std::vector<std::string> notes;
  std::set<std::string> seen;
  const std::string arch_name = arch_option_name(c.arch);
  const std::string emitted_no = runtime_disable_modifiers(c, mask);

  for (const auto &option : architecture_baseline_options(c.arch)) {
    if (!seen.insert(option).second) continue;
    const std::string req = runtime_requirement_for_option(option);
    if (!req.empty() && !runtime_requirement_present(req, mask)) {
      std::string actual;
      const std::string needle = "+no" + option;
      if (emitted_no.find(needle) != std::string::npos) actual = needle;
      if (actual.empty()) {
        for (const auto &root : architecture_baseline_options(c.arch)) {
          const std::string root_needle = "+no" + root;
          if (emitted_no.find(root_needle) == std::string::npos) continue;
          if (option_depends_on(option, root) || option_depends_on(root, option)) {
            actual = root_needle;
            break;
          }
        }
      }
      if (actual.empty()) actual = "+no...";
      const std::string introduced = architecture_option_introduction(c.arch, option);
      notes.push_back(option + " (omitted by including in " + (introduced.empty() ? arch_name : introduced)
                      + "; runtime feature is unavailable, so " + actual + " is emitted)");
    }
    else {
      const std::string introduced = architecture_option_introduction(c.arch, option);
      notes.push_back(option + " (omitted by including in " + (introduced.empty() ? arch_name : introduced) + ")");
    }
  }

  for (const auto &fl : split_csv(c.flags)) {
    const FlagRecord *fr=nullptr;
    for(unsigned i=0;i<flag_table_count;i++)
      if(fl==flag_table[i].flag) { fr=&flag_table[i]; break; }

    if(!fr) {
      notes.push_back(fl + " (omitted because no GCC flag mapping was generated)");
      continue;
    }

    const std::string option = fr->positive_option;
    if(option.empty()) {
      std::string lower = fl;
      std::transform(lower.begin(), lower.end(), lower.begin(),
                     [](unsigned char ch){ return (char)std::tolower(ch); });
      if (architecture_implies_option(c.arch, lower)) {
        if (seen.insert(lower).second) {
          const std::string introduced = architecture_option_introduction(c.arch, lower);
          notes.push_back(lower + " (omitted by including in "
                          + (introduced.empty() ? arch_name : introduced) + ")");
        }
      } else {
        notes.push_back(fl + " (omitted because no runtime FEAT_* mapping is available)");
      }
      continue;
    }

    if (architecture_implies_option(c.arch, option))
      continue;

    if (!all_runtime_features_present(fr->positive_features, mask))
      notes.push_back(option + " (omitted because runtime feature is unavailable; a +no... modifier is emitted instead)");
  }
  return notes;
}

static std::string option_report_text(const std::vector<CpuId>& ids,
                                      const std::vector<const CoreRecord*>& matches,
                                      uint64_t mask) {
  std::ostringstream out;
  std::set<std::string> names;
  for(const auto &id: ids) for(auto*c:matches_for_id(id)) names.insert(c->name);
  if(names.empty()) {
    out << "\nNo GCC definition matched any observed implementer/part ID.\n";
    return out.str();
  }
  out << "\nCPU-matched GCC options with runtime-derived modifiers:\n";
  for(const auto &id: ids) {
    auto im=matches_for_id(id);
    for(auto*c:im) {
      std::string mods = combined_modifiers(*c, mask);
      std::string arch = arch_option_name(c->arch);
      out << "  implementer=" << hexv(id.implementer) << " part=" << hexv(id.part);
      if(id.have_variant) out << " variant=" << hexv(id.variant);
      out << " -> -mcpu=" << c->name << mods << "\n"
          << "     -march=" << arch << mods << "\n"
          << "     -mtune=" << c->name << "\n";
      auto omitted=omitted_modifier_notes(*c,mask);
      if(!omitted.empty()) {
        out << "     omitted feature modifiers (reference; architecture baseline and core-specific omissions):\n";
        for(const auto &n: omitted) out << "       " << n << "\n";
      }
    }
  }
  return out.str();
}
static void print_cpu_ids(std::ostringstream &out, const std::vector<CpuId> &ids) {
  for (const auto &id : ids) {
    out << "  implementer=" << hexv(id.implementer)
        << " part=" << hexv(id.part);
    if (id.have_variant) out << " variant=" << hexv(id.variant);
    out << " : " << id.count << " core(s)\n";
  }
}

static void print_fallback_options_concise(std::ostringstream &out,
                                           const std::vector<CpuId> &ids,
                                           uint64_t mask) {
  if (ids.empty() || !runtime_feature_present(mask, "FEAT_FP") ||
      !runtime_feature_present(mask, "FEAT_SIMD")) return;
  for (const auto &id : ids) {
    out << "  implementer=" << hexv(id.implementer)
        << " part=" << hexv(id.part);
    if (id.have_variant) out << " variant=" << hexv(id.variant);
    out << " -> -march=armv8-a" << fallback_armv8_cpu_flags(mask) << "\n";
  }
}

static void print_matched_options(std::ostringstream &out,
                                  const std::vector<CpuId> &ids,
                                  const std::vector<const CoreRecord*> &matches,
                                  uint64_t mask) {
  out << "CPU matched GCC options with runtime derived modifiers:\n";
  bool any = false;
  for (const auto &id : ids) {
    auto im = matches_for_id(id);
    for (auto *c : im) {
      any = true;
      std::string mods = combined_modifiers(*c, mask);
      std::string arch = arch_option_name(c->arch);
      out << "  implementer=" << hexv(id.implementer)
          << " part=" << hexv(id.part);
      if (id.have_variant) out << " variant=" << hexv(id.variant);
      out << "\n    -mcpu=" << c->name << mods << "\n"
          << "    -march=" << arch << mods << "\n"
          << "    -mtune=" << c->name << "\n";
    }
  }
  if (!any && matches.empty()) {
    if (runtime_feature_present(mask, "FEAT_FP") &&
        runtime_feature_present(mask, "FEAT_SIMD")) {
      out << "  (GCC definition not found; see fallback -march below)\n";
    } else {
      out << "  (GCC definition not found)\n";
    }
  }
}

static std::string upstream_source_attribution() {
  std::ostringstream out;
  out << "\nupstream files derived from https://github.com/gcc-mirror/gcc\n"
      << "  gcc/common/config/aarch64/cpuinfo.h at commit 790e293\n"
      << "  gcc/config/aarch64/aarch64-arches.def at commit 254a858\n"
      << "  gcc/config/aarch64/aarch64-cores.def at commit 2f7613d\n"
      << "  gcc/config/aarch64/aarch64-feature-deps.h at commit 254a858\n"
      << "  gcc/config/aarch64/aarch64-option-extensions.def at commit 37dcc82\n"
      << "  gcc/config/aarch64/aarch64-c.cc at commit b610d8c\n"
      << "  libgcc/config/aarch64/cpuinfo.c at commit e3d2277\n"
      << "upstream files derived from https://github.com/util-linux/util-linux\n"
      << "  sys-utils/lscpu-arm.c at commit 4b53cfd\n";
  return out.str();
}

int main(int argc,char**argv) {
  bool json = false;
  bool verbose = false;
  for (int i = 1; i < argc; ++i) {
    const std::string arg = argv[i];
    if (arg == "--json") json = true;
    else if (arg == "-v" || arg == "--verbose") verbose = true;
    else {
      std::cerr << "unknown argument: " << arg << "\n"
                << "usage: " << argv[0] << " [-v|--verbose] [--json]\n";
      return 2;
    }
  }

  auto ids=read_cpuinfo(); std::vector<const CoreRecord*> matches;
  for(unsigned i=0;i<core_table_count;i++) if(part_match(core_table[i],ids)) matches.push_back(&core_table[i]);
  uint64_t mask=native_cpu_feature_mask();

  if(json) {
    std::ostringstream out;
    out << "{\n  \"cpu_ids\": [\n";
    for(size_t i=0;i<ids.size();i++) {
      out << "    {\"implementer\":\""<<hexv(ids[i].implementer)
          <<"\",\"part\":\""<<hexv(ids[i].part)
          <<"\",\"variant\":\""<<hexv(ids[i].variant)
          <<"\",\"count\":"<<ids[i].count<<"}"<<(i+1<ids.size()?",":"")<<"\n";
    }
    out << "  ],\n  \"matched_cores\": [\n";
    for(size_t i=0;i<matches.size();i++) {
      auto*c=matches[i]; out << "    {\"name\":\""<<c->name<<"\",\"arch\":\""<<c->arch<<"\",\"flags\":[";
      auto fs=split_csv(c->flags);
      for(size_t j=0;j<fs.size();j++) out << "\""<<fs[j]<<"\""<<(j+1<fs.size()?",":"");
      out << "]}"<<(i+1<matches.size()?",":"")<<"\n";
    }
    out << "  ],\n  \"features\": [\n";
    bool first=true;
    for(unsigned i=0;i<feature_table_count;i++) {
      const auto&r=feature_table[i]; if(hidden(r.name)) continue;
      if(!first) out<<",\n"; first=false;
      out<<"    {\"name\":\""<<r.name<<"\",\"flags\":\""<<r.direct_flags
         <<"\",\"closure\":\""<<r.closure_flags<<"\",\"runtime_condition\":\""<<r.runtime_condition<<"\"}";
    }
    out << "\n  ],\n  \"fallback_armv8\": " << ((matches.empty() && runtime_feature_present(mask, "FEAT_FP") && runtime_feature_present(mask, "FEAT_SIMD")) ? "true" : "false") << "\n}\n";
    std::cout << out.str();
    return 0;
  }

  std::ostringstream report;
  if (!verbose) {
    print_cpu_ids(report, ids);
    if (!matches.empty()) {
      print_matched_options(report, ids, matches, mask);
    } else {
      report << "CPU matched GCC options with runtime derived modifiers:\n";
      print_fallback_options_concise(report, ids, mask);
    }
    report << "\nFor more detailed information, add -v/--verbose.\n";
    std::cout << report.str();
    return 0;
  }

  report << "GCC AArch64 native CPU report\n"
         << "sources: aarch64-cores.def + aarch64-arches.def + cpuinfo.h + cpuinfo.c + aarch64-option-extensions.def + aarch64-feature-deps.h\n\n";

  report << "CPU IDs from /proc/cpuinfo:\n";
  print_cpu_ids(report, ids);

  report << "\nMatched GCC definitions (per observed CPU ID):\n";
  bool any_per_id=false;
  for(const auto &id: ids) {
    auto im=matches_for_id(id);
    if(im.empty()) continue;
    any_per_id=true;
    report << "  " << hexv(id.implementer) << "/" << hexv(id.part) << " ->";
    for(auto*c:im) report << " -mcpu=" << c->name;
    report << "\n";
  }
  if(!any_per_id) report << "  (none)\n";
  for(auto*c:matches) {
    report<<"  GCC definition: -mcpu="<<c->name<<"  arch="<<c->arch
          <<(c->part_count>1 ? "  [BIG.LITTLE]" : "")<<"\n    FLAGS: ";
    auto fs=split_csv(c->flags);
    for(size_t i=0;i<fs.size();i++) report<<(i?", ":"")<<fs[i];
    report<<"\n";
  }

  report << "\nRuntime CPU features detected by upstream cpuinfo.c:\n";
  for(unsigned i=0;i<cpu_feature_count && i<64;i++) {
    std::string n=cpu_feature_names[i];
    if(!hidden(n)&&runtime_feature_present(mask,n)) report<<"  + "<<n<<"\n";
  }
  report << "\nRuntime CPU features NOT detected by upstream cpuinfo.c:\n";
  for(unsigned i=0;i<cpu_feature_count && i<64;i++) {
    std::string n=cpu_feature_names[i];
    if(!hidden(n)&&!runtime_feature_present(mask,n)) report<<"  - "<<n<<"\n";
  }

  report << feature_mapping_text();
  report << flag_mapping_text();
  report << option_report_text(ids,matches,mask);
  if (matches.empty()) report << fallback_report_text(ids, mask);
  report << upstream_source_attribution();

  // One final output operation for the normal report. All sections above are
  // assembled first so output ordering is explicit and formatting is not
  // interleaved with computation.
  std::cout << report.str();
  return 0;
}
