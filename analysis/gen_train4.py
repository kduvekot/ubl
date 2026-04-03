#!/usr/bin/env python3
"""Train track SVG v4: 45° angled connections, tighter layout, no crossings."""
import subprocess, re, math
from collections import Counter

REPO = "/home/user/ubl"

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True, cwd=REPO).strip()

# ─── TRUNK ───
trunk = run("git rev-list --first-parent origin/ubl-2.5").split("\n")
trunk.reverse()
trunk_set = set(trunk)
trunk_idx = {sha: i for i, sha in enumerate(trunk)}

log_data = run(f"git rev-list --first-parent origin/ubl-2.5 --reverse --format='%at %as %s'")
log_lines = [l for l in log_data.split("\n") if not l.startswith("commit ")]
trunk_ts = []
trunk_dates = []
trunk_msgs = []
for line in log_lines:
    parts = line.split(" ", 2)
    trunk_ts.append(int(parts[0]))
    trunk_dates.append(parts[1])
    trunk_msgs.append(parts[2][:50] if len(parts) > 2 else "")

N = len(trunk)
print(f"Trunk commits: {N}")

# ─── MERGES with full branch data ───
merge_branches = []

for i, sha in enumerate(trunk):
    plines = [l for l in run(f"git cat-file -p {sha}").split("\n") if l.startswith("parent ")]
    if len(plines) < 2:
        continue
    p1 = plines[0].split()[1]
    p2 = plines[1].split()[1]
    msg = run(f"git log --format='%s' -1 {sha}")

    pr_match = re.search(r'#(\d+)', msg)
    pr = f"PR#{pr_match.group(1)}" if pr_match else ""
    br_match = re.search(r'from (\S+)', msg)
    source = br_match.group(1) if br_match else ""
    source = source.replace("oasis-tcs/", "").replace("kduvekot/", "")

    try:
        mb = run(f"git merge-base {p1} {p2}")
        fork_idx = trunk_idx.get(mb, i - 1)
    except:
        fork_idx = i - 1

    branch_shas = run(f"git rev-list --reverse {p2} --not {p1}").split("\n")
    commits = []
    for bsha in branch_shas:
        if not bsha:
            continue
        bdate = run(f"git log --format='%as' -1 {bsha}")
        bmsg = run(f"git log --format='%s' -1 {bsha}")[:45]
        commits.append({"sha": bsha[:7], "msg": bmsg, "date": bdate})

    if commits:
        merge_branches.append({
            "merge_idx": i,
            "fork_idx": fork_idx,
            "pr": pr,
            "source": source,
            "commits": commits,
        })

# ─── DEAD-END branches ───
dead_branches = [
    {"name": "ubl-2.3-csd05-copy", "fork_idx": 5, "commits": 1, "release": "★ 2.3 CSD05  12 May 2021"},
    {"name": "ubl-2.3-cs02", "fork_idx": 5, "commits": 2, "release": "★ 2.3 CS02  25 May 2021"},
    {"name": "ubl-2.3-os (+os-iso)", "fork_idx": 9, "commits": 2, "release": "★ 2.3 OS  15 Jun 2021"},
    {"name": "review", "fork_idx": 9, "commits": 5, "release": None},
    {"name": "main", "fork_idx": 9, "commits": 1, "release": None},
    {"name": "ubl-2.4-csd01 tip", "fork_idx": 68, "commits": 1, "release": None},
    {"name": "tsc-ubl-2.5-exp", "fork_idx": 102, "commits": 14, "release": None},
    {"name": "ubl-2.4-cs01 tip", "fork_idx": 106, "commits": 7, "release": None},
    {"name": "ubl-2.4-os", "fork_idx": 106, "commits": 14, "release": "★ 2.4 OS  20 Jun 2024"},
    {"name": "ubl-2.4-os-iso-pub", "fork_idx": 106, "commits": 22, "release": None},
    {"name": "retest", "fork_idx": 125, "commits": 2, "release": None},
    {"name": "ubl-2.5-kenneth", "fork_idx": 138, "commits": 2, "release": None},
    {"name": "kentest", "fork_idx": 307, "commits": 9, "release": None},
    {"name": "server-test", "fork_idx": 307, "commits": 1, "release": None},
    {"name": "ubl-2.5-retry", "fork_idx": 308, "commits": 1, "release": None},
]

# ─── RELEASES on trunk ───
releases = {}
for prefix, label in [
    ("2e3c601", "★ 2.4 CSD01  08 Feb 2023"),
    ("9b42a40", "★ 2.4 CSD02  26 Jul 2023"),
    ("b9df309", "★ 2.4 CS01  17 Oct 2023"),
    ("0b44c38", "★ 2.5 CSD01  20 Aug 2025"),
    ("b122814", "★ 2.5 CSD02  03 Dec 2025"),
    ("3d81e8a", "★ 2.5 CSD03  11 Feb 2026"),
]:
    for sha in trunk:
        if sha.startswith(prefix):
            releases[trunk_idx[sha]] = label

# ─── MILESTONES ───
milestones = {
    0: "Repo created  11 Apr 2018",
    9: "PIVOT  26 May 2021",
    175: "UBL-433-xsd-doc  06 Jul 2025",
    215: "dc1249d (recovered)  06 Aug 2025",
}

# ─── COMPUTE Y POSITIONS ───
MIN_GAP = 6
MAX_GAP = 40
BRANCH_DOT_SP = 12
DIAG = 12  # length of 45° diagonal segment (horizontal & vertical component)

deltas = []
for i in range(1, N):
    dt = trunk_ts[i] - trunk_ts[i-1]
    deltas.append(max(dt, 0))

log_deltas = []
for dt in deltas:
    if dt <= 0:
        log_deltas.append(0)
    else:
        log_deltas.append(math.log1p(dt / 3600))

if log_deltas:
    max_ld = max(log_deltas) if max(log_deltas) > 0 else 1
    base_gaps = [MIN_GAP + (ld / max_ld) * (MAX_GAP - MIN_GAP) for ld in log_deltas]
else:
    base_gaps = []

def required_span(n_dots):
    return (n_dots + 1) * BRANCH_DOT_SP + 2 * DIAG + 10

branch_spans = []
for mb in merge_branches:
    needed = required_span(len(mb["commits"]))
    branch_spans.append((mb["fork_idx"], mb["merge_idx"], needed))

for db in dead_branches:
    end_idx = min(db["fork_idx"] + db["commits"] + 1, N - 1)
    needed = required_span(db["commits"])
    branch_spans.append((db["fork_idx"], end_idx, needed))

gaps = list(base_gaps)
MAX_EXPANDED_GAP = 60

for start, end, needed in sorted(branch_spans, key=lambda x: x[1]-x[0]):
    if start >= end or end > len(gaps):
        continue
    current = sum(gaps[start:end])
    if current < needed:
        deficit = needed - current
        span_len = end - start
        add_per = deficit / span_len
        for j in range(start, min(end, len(gaps))):
            gaps[j] = min(gaps[j] + add_per, MAX_EXPANDED_GAP)

header_h = 55
y_start = header_h + 35
y_pos = [0.0] * N
y_pos[0] = y_start
for i in range(1, N):
    y_pos[i] = y_pos[i-1] + gaps[i-1]

total_h = y_pos[-1] + 80
print(f"Total height: {total_h:.0f}px")
print(f"Gap range: {min(gaps):.1f} - {max(gaps):.1f}px")

# ─── SVG LAYOUT PARAMS ───
DOT_R = 2.5
DOT_R_SIG = 4
DOT_R_REL = 5
TRUNK_X = 300
RIGHT_COL_SP = 55   # tighter column spacing for right side
LEFT_COL_SP = 90     # wide enough for branch-name labels to fit between columns
RIGHT_START = 30     # gap from trunk to first right column
LEFT_START = 30      # gap from trunk to first left column

def yp(idx):
    return y_pos[idx]

# ─── COLUMN ASSIGNMENT: right side ───
# Greedy: for each branch, find the lowest column not in use during its span
right_tracks = []
for mb in merge_branches:
    # Find columns used by overlapping branches
    used_cols = set()
    for existing in right_tracks:
        if not (mb["fork_idx"] >= existing["merge_idx"] or mb["merge_idx"] <= existing["fork_idx"]):
            used_cols.add(existing["col"])
    # Find lowest free column
    col = 0
    while col in used_cols:
        col += 1
    mb["col"] = col
    right_tracks.append(mb)

max_right_col = max((mb["col"] for mb in merge_branches), default=0)

# ─── COLUMN ASSIGNMENT: left side ───
# Crossing-aware: a branch's horizontal line to col C must not cross
# any existing branch's vertical section at columns 0..C-1.
# Sort by fork_idx DESCENDING so later (lower) branches get inner columns first.
# Earlier branches with long verticals go to outer columns where their horizontals
# (at higher y) pass above later branches' verticals.
# Within same fork_idx: shorter branches first (closer to trunk).
dead_sorted = sorted(dead_branches, key=lambda d: (-d["fork_idx"], d["commits"]))
left_tracks = []

for db in dead_sorted:
    # Compute this branch's y-range for its vertical section
    # (with maximum possible fan-out offset added)
    db_y_top = yp(db["fork_idx"]) + DIAG  # where horizontal arrives & vertical starts
    db_y_end = db_y_top + db["commits"] * BRANCH_DOT_SP + 15

    best_col = None
    for col in range(20):
        ok = True
        horiz_y = db_y_top
        for existing in left_tracks:
            same_fork = (existing["fork_idx"] == db["fork_idx"])
            if existing["col"] < col:
                # Would our horizontal cross this branch's vertical?
                # Skip this check for same-fork branches (fan-out handles separation)
                if not same_fork:
                    e_y_top = existing["_y_top"]
                    e_y_end = existing["_y_end"]
                    if e_y_top - 2 <= horiz_y <= e_y_end + 2:
                        ok = False
                        break
            elif existing["col"] == col:
                # Same column: check vertical overlap
                if not (db_y_top > existing["_y_end"] + 2 or db_y_end < existing["_y_top"] - 2):
                    ok = False
                    break
        if ok:
            best_col = col
            break

    if best_col is None:
        best_col = max((ex["col"] for ex in left_tracks), default=-1) + 1

    db["col"] = best_col
    db["_y_top"] = db_y_top
    db["_y_end"] = db_y_end
    left_tracks.append(db)

max_left_col = max((db["col"] for db in dead_branches), default=0)

svg_w = TRUNK_X + RIGHT_START + (max_right_col + 1) * RIGHT_COL_SP + 250
left_margin = LEFT_START + (max_left_col + 1) * LEFT_COL_SP + 170
if TRUNK_X < left_margin:
    TRUNK_X = left_margin  # ensure enough room for left branches + labels
    svg_w = TRUNK_X + RIGHT_START + (max_right_col + 1) * RIGHT_COL_SP + 250

print(f"TRUNK_X={TRUNK_X}, svg_w={svg_w}")
print(f"Right cols: max={max_right_col}, Left cols: max={max_left_col}")

# Year markers
year_first = {}
for i, d in enumerate(trunk_dates):
    y = d[:4]
    if y not in year_first:
        year_first[y] = i

lines = []
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{int(total_h)}" '
             f'style="background-color:#0d1117">')
lines.append('<style>')
lines.append('text { font-family: Helvetica, Arial, sans-serif; paint-order: stroke fill; stroke: #0d1117; stroke-width: 3px; stroke-linejoin: round; }')
lines.append('.dot-trunk { fill: #4a7a5a; }')
lines.append('.dot-release { fill: #7ee787; }')
lines.append('.dot-merge { fill: #58a6ff; }')
lines.append('.dot-recovered { fill: #d2a8ff; }')
lines.append('.dot-branch { fill: #6a8a7a; }')
lines.append('.dot-branch-release { fill: #7ee787; }')
lines.append('.dot-pr { fill: #4a6a8a; }')
lines.append('.line-trunk { stroke: #4a7a5a; stroke-width: 3; }')
lines.append('.line-dead { stroke: #484f58; stroke-width: 1.5; }')
lines.append('.line-dead-rel { stroke: #3a6a3a; stroke-width: 1.5; }')
lines.append('.line-pr { stroke: #2a4a6a; stroke-width: 1.5; }')
lines.append('.lbl { fill: #8b949e; font-size: 8px; }')
lines.append('.lbl-rel { fill: #7ee787; font-size: 9px; font-weight: bold; }')
lines.append('.lbl-mile { fill: #ffa657; font-size: 9px; }')
lines.append('.lbl-pr { fill: #58a6ff; font-size: 7.5px; }')
lines.append('.lbl-src { fill: #6a8a9e; font-size: 7px; }')
lines.append('.lbl-year { fill: #484f58; font-size: 11px; font-weight: bold; }')
lines.append('.year-line { stroke: #21262d; stroke-width: 1; stroke-dasharray: 2,4; }')
lines.append('.rec-zone { fill: #2a1a3a; opacity: 0.25; }')
lines.append('</style>')

# Title
lines.append(f'<text x="10" y="16" fill="#58a6ff" font-size="13" font-weight="bold">oasis-tcs/ubl — Train Track View</text>')
lines.append(f'<text x="10" y="30" fill="#8b949e" font-size="9">328 trunk commits (dots) · 160 PR branch commits (side tracks) · '
             f'★ = verified release · Blue = merge-back branches · Gray = dead ends</text>')
lines.append(f'<text x="10" y="42" fill="#484f58" font-size="8">Generated 2026-04-02 · Time-proportional spacing</text>')

# Recovered zone
lines.append(f'<rect x="{TRUNK_X-15}" y="{yp(176)-5}" width="30" height="{yp(215)-yp(176)+10}" class="rec-zone" rx="5"/>')

# Year markers
for year, idx in sorted(year_first.items()):
    y = yp(idx)
    lines.append(f'<line x1="10" y1="{y}" x2="{TRUNK_X-30}" y2="{y}" class="year-line"/>')
    lines.append(f'<text x="15" y="{y+4}" class="lbl-year">{year}</text>')

# ─── TRUNK LINE ───
lines.append(f'<line x1="{TRUNK_X}" y1="{yp(0)}" x2="{TRUNK_X}" y2="{yp(N-1)}" class="line-trunk"/>')

# ─── RIGHT SIDE: PR MERGE-BACK BRANCHES with 45° connections ───
# Group by fork/merge idx, assign offsets with furthest column first
OFFSET_STEP = 10

# Pre-compute fork offsets: group branches by fork_idx, sort by col descending
# Furthest column (highest col) gets rank 0 (departs first = smallest y offset)
r_fork_groups = {}
for mb in merge_branches:
    r_fork_groups.setdefault(mb["fork_idx"], []).append(mb)
r_fork_offset = {}
for fidx, group in r_fork_groups.items():
    if len(group) <= 1:
        for mb_id in [id(m) for m in group]:
            r_fork_offset[mb_id] = 0
    else:
        for rank, mb in enumerate(sorted(group, key=lambda m: -m["col"])):
            r_fork_offset[id(mb)] = rank * OFFSET_STEP

# Same for merge points: furthest column arrives first (smallest negative offset from merge dot)
r_merge_groups = {}
for mb in merge_branches:
    r_merge_groups.setdefault(mb["merge_idx"], []).append(mb)
r_merge_offset = {}
for midx, group in r_merge_groups.items():
    if len(group) <= 1:
        for mb_id in [id(m) for m in group]:
            r_merge_offset[mb_id] = 0
    else:
        for rank, mb in enumerate(sorted(group, key=lambda m: -m["col"])):
            r_merge_offset[id(mb)] = rank * OFFSET_STEP

for mb in merge_branches:
    x_branch = TRUNK_X + RIGHT_START + mb["col"] * RIGHT_COL_SP
    y_fork_base = yp(mb["fork_idx"])
    y_merge_base = yp(mb["merge_idx"])
    n = len(mb["commits"])
    d = DIAG

    fork_off = r_fork_offset[id(mb)]
    merge_off = r_merge_offset[id(mb)]

    y_fork = y_fork_base + fork_off
    y_merge = y_merge_base - merge_off

    lines.append(f'<path d="M {TRUNK_X},{y_fork} '
                 f'L {TRUNK_X+d},{y_fork+d} '
                 f'L {x_branch},{y_fork+d} '
                 f'L {x_branch},{y_merge-d} '
                 f'L {TRUNK_X+d},{y_merge-d} '
                 f'L {TRUNK_X},{y_merge}" '
                 f'class="line-pr" fill="none"/>')

    # Dots along vertical portion (between y_fork+d and y_merge-d)
    if n > 0:
        vert_start = y_fork + d
        vert_end = y_merge - d
        vert_len = vert_end - vert_start
        if vert_len > 0:
            step = vert_len / (n + 1)
            for j in range(n):
                dy = vert_start + (j + 1) * step
                lines.append(f'<circle cx="{x_branch}" cy="{dy}" r="{DOT_R}" class="dot-pr"/>')

    # Label at midpoint of vertical section
    label_y = (y_fork + d + y_merge - d) / 2
    pr_label = mb["pr"] if mb["pr"] else "merge"
    lines.append(f'<text x="{x_branch+6}" y="{label_y-4}" class="lbl-pr">{pr_label} ({n})</text>')
    if mb["source"]:
        lines.append(f'<text x="{x_branch+6}" y="{label_y+6}" class="lbl-src">{mb["source"]}</text>')

# ─── LEFT SIDE: DEAD-END BRANCHES with 45° connections ───
# Pre-compute fork offsets: furthest column (highest col) departs first (smallest y offset)
# so its horizontal line passes above inner branches' verticals
l_fork_groups = {}
for db in dead_branches:
    l_fork_groups.setdefault(db["fork_idx"], []).append(db)
l_fork_offset = {}
for fidx, group in l_fork_groups.items():
    if len(group) <= 1:
        for db_id in [id(d) for d in group]:
            l_fork_offset[db_id] = 0
    else:
        for rank, db in enumerate(sorted(group, key=lambda d: -d["col"])):
            l_fork_offset[id(db)] = rank * OFFSET_STEP

left_labels = []  # collected for collision resolution

for db in dead_branches:
    x_branch = TRUNK_X - LEFT_START - db["col"] * LEFT_COL_SP
    y_fork_base = yp(db["fork_idx"])
    n = db["commits"]
    d = DIAG

    fork_off = l_fork_offset[id(db)]
    y_fork = y_fork_base + fork_off

    is_rel = db["release"] is not None
    line_cls = "line-dead-rel" if is_rel else "line-dead"
    dot_cls = "dot-branch-release" if is_rel else "dot-branch"

    # Path: trunk → 45° down-left → horizontal → vertical down
    y_branch_start = y_fork + d
    y_end = y_branch_start + n * BRANCH_DOT_SP

    lines.append(f'<path d="M {TRUNK_X},{y_fork} '
                 f'L {TRUNK_X-d},{y_fork+d} '
                 f'L {x_branch},{y_fork+d} '
                 f'L {x_branch},{y_end}" '
                 f'class="{line_cls}" fill="none"/>')

    for j in range(1, n + 1):
        dy = y_branch_start + j * BRANCH_DOT_SP
        dr = DOT_R_SIG if (j == n and is_rel) else DOT_R
        lines.append(f'<circle cx="{x_branch}" cy="{dy}" r="{dr}" class="{dot_cls}"/>')

    # End cap
    lines.append(f'<line x1="{x_branch-3}" y1="{y_end}" x2="{x_branch+3}" y2="{y_end}" '
                 f'stroke="{"#7ee787" if is_rel else "#484f58"}" stroke-width="2"/>')

    # Label — collected for collision resolution later
    lbl = db.get("release", None) or f'{db["name"]} ({n})'
    lbl_cls = "lbl-rel" if is_rel else "lbl"
    # Store: (x, y, text, css_class, anchor, estimated_width)
    char_w = 5.5 if is_rel else 5  # approx px per char at font size
    lbl_w = len(lbl) * char_w
    left_labels.append({"x": x_branch - 8, "y": y_end + 12, "text": lbl, "cls": lbl_cls, "anchor": "end", "w": lbl_w, "h": 10, "branch_x": x_branch, "endcap_y": y_end, "orig_x": x_branch - 8})
    if is_rel:
        left_labels.append({"x": x_branch - 8, "y": y_end + 22, "text": db["name"], "cls": "lbl", "anchor": "end", "w": len(db["name"]) * 5, "h": 9, "branch_x": x_branch, "endcap_y": y_end, "orig_x": x_branch - 8})

# ─── LEFT LABEL CROSSING CHECK: ensure no label crosses a branch vertical ───
left_vert_segs = []
for db in dead_branches:
    bx = TRUNK_X - LEFT_START - db["col"] * LEFT_COL_SP
    fork_off = l_fork_offset[id(db)]
    y_top = yp(db["fork_idx"]) + fork_off + DIAG
    y_bot = y_top + db["commits"] * BRANCH_DOT_SP
    left_vert_segs.append({"x": bx, "y_top": y_top, "y_bot": y_bot})

def check_left_label_crossings(labels):
    """Push left labels leftward so they don't cross any branch vertical."""
    for lbl in labels:
        own_x = lbl["branch_x"]
        lbl_h = lbl.get("h", 10)
        for _ in range(20):
            lbl_y = lbl["y"]
            lbl_x_right = lbl["x"]
            lbl_x_left = lbl_x_right - lbl["w"]
            crossing_xs = []
            for v in left_vert_segs:
                if abs(v["x"] - own_x) < 1:
                    continue  # skip own branch
                # Label covers [lbl_y - lbl_h, lbl_y]; branch covers [y_top, y_bot]
                # They overlap when lbl_y > y_top AND lbl_y - lbl_h < y_bot
                if v["y_top"] - 3 < lbl_y and lbl_y < v["y_bot"] + lbl_h + 3:
                    if lbl_x_left - 3 < v["x"] < lbl_x_right + 3:
                        crossing_xs.append(v["x"])
            if not crossing_xs:
                break
            lbl["x"] = min(crossing_xs) - 6

def resolve_collisions_2d(labels, min_gap=12, anchor="end"):
    """Nudge overlapping labels apart vertically, only when 2D bboxes overlap."""
    if not labels:
        return
    labels.sort(key=lambda l: l["y"])
    for _iteration in range(8):
        moved = False
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                if labels[j]["y"] - labels[i]["y"] > 50:
                    break
                # Check x overlap
                if anchor == "end":
                    a_left, a_right = labels[i]["x"] - labels[i]["w"], labels[i]["x"]
                    b_left, b_right = labels[j]["x"] - labels[j]["w"], labels[j]["x"]
                else:
                    a_w = labels[i].get("w", len(labels[i]["text"]) * 5)
                    b_w = labels[j].get("w", len(labels[j]["text"]) * 5)
                    a_left, a_right = labels[i]["x"], labels[i]["x"] + a_w
                    b_left, b_right = labels[j]["x"], labels[j]["x"] + b_w
                if a_left >= b_right + 4 or b_left >= a_right + 4:
                    continue  # no x overlap, skip
                # y overlap with min_gap
                if labels[j]["y"] - labels[i]["y"] < min_gap:
                    labels[j]["y"] = labels[i]["y"] + min_gap
                    moved = True
        if not moved:
            break
        labels.sort(key=lambda l: l["y"])

# ─── RIGHT-SIDE VERTICAL SEGMENTS for trunk label crossing checks ───
right_vert_segs = []
right_horiz_segs = []
for mb in merge_branches:
    bx = TRUNK_X + RIGHT_START + mb["col"] * RIGHT_COL_SP
    fork_off = r_fork_offset[id(mb)]
    merge_off = r_merge_offset[id(mb)]
    y_top = yp(mb["fork_idx"]) + fork_off + DIAG
    y_bot = yp(mb["merge_idx"]) - merge_off - DIAG
    right_vert_segs.append({"x": bx, "y_top": y_top, "y_bot": y_bot})
    # Horizontal connectors at fork and merge
    right_horiz_segs.append({"y": y_top, "x_right": bx})
    right_horiz_segs.append({"y": y_bot, "x_right": bx})

# ─── TRUNK DOTS ───
for i in range(N):
    y = yp(i)
    if i in releases:
        r, cls = DOT_R_REL, "dot-release"
    elif any(mb["merge_idx"] == i for mb in merge_branches):
        r, cls = DOT_R_SIG, "dot-merge"
    elif 176 <= i <= 215:
        r, cls = DOT_R, "dot-recovered"
    elif i in milestones or any(mb["fork_idx"] == i for mb in merge_branches):
        r, cls = DOT_R_SIG, "dot-merge"
    else:
        r, cls = DOT_R, "dot-trunk"
    lines.append(f'<circle cx="{TRUNK_X}" cy="{y}" r="{r}" class="{cls}"/>')

# ─── ALL LABELS: collect, resolve collisions, render ───
trunk_labels = []
for idx, label in releases.items():
    trunk_labels.append({"x": TRUNK_X + 8, "y": yp(idx) + 4, "text": label, "cls": "lbl-rel", "anchor": "start", "h": 10, "w": len(label) * 5.5})
for idx, label in milestones.items():
    trunk_labels.append({"x": TRUNK_X + 8, "y": yp(idx) + 4, "text": label, "cls": "lbl-mile", "anchor": "start", "h": 10, "w": len(label) * 5.0})
for mb in merge_branches:
    i = mb["merge_idx"]
    if i not in releases and i not in milestones:
        pr_label = mb["pr"] if mb["pr"] else "merge"
        txt = f"← {pr_label}"
        trunk_labels.append({"x": TRUNK_X + 8, "y": yp(i) + 3, "text": txt, "cls": "lbl-pr", "anchor": "start", "h": 8, "w": len(txt) * 4.5})

# ─── ITERATIVE LABEL POSITIONING ───
# Run crossing check + collision resolution in multiple rounds so that
# labels pushed down by collision resolution get re-checked for crossings.
for _round in range(3):
    check_left_label_crossings(left_labels)
    resolve_collisions_2d(left_labels, min_gap=12, anchor="end")

# Trunk label crossing check
for lbl in trunk_labels:
    lbl_y = lbl["y"]
    lbl_w = lbl["w"]
    max_cross_x = 0
    for v in right_vert_segs:
        if v["y_top"] - 10 <= lbl_y <= v["y_bot"] + 3:
            if lbl["x"] - 2 < v["x"] < lbl["x"] + lbl_w + 2:
                max_cross_x = max(max_cross_x, v["x"])
    for h in right_horiz_segs:
        if abs(h["y"] - lbl_y) < 8:
            if lbl["x"] < h["x_right"] + 2:
                max_cross_x = max(max_cross_x, h["x_right"])
    if max_cross_x > 0:
        lbl["x"] = max_cross_x + 8

resolve_collisions_2d(trunk_labels, min_gap=11, anchor="start")

# Build leader lines for displaced left labels
leader_lines = []
for lbl in left_labels:
    if lbl["x"] < lbl["orig_x"] - 15:
        leader_lines.append((lbl["branch_x"], lbl["endcap_y"] + 4, lbl["x"] + 3, lbl["y"] - 3))

# Render leader lines for displaced left labels
for x1, y1, x2, y2 in leader_lines:
    lines.append(f'<line x1="{x1}" y1="{y1:.1f}" x2="{x2}" y2="{y2:.1f}" stroke="#484f58" stroke-width="0.5" stroke-dasharray="2,2"/>')

# Render all labels
for lbl in left_labels:
    lines.append(f'<text x="{lbl["x"]}" y="{lbl["y"]:.1f}" class="{lbl["cls"]}" text-anchor="{lbl["anchor"]}">{lbl["text"]}</text>')
for lbl in trunk_labels:
    lines.append(f'<text x="{lbl["x"]}" y="{lbl["y"]:.1f}" class="{lbl["cls"]}" text-anchor="{lbl["anchor"]}">{lbl["text"]}</text>')

lines.append('</svg>')

svg = "\n".join(lines)
outpath = "/home/user/ubl/analysis/trunk-train.svg"
with open(outpath, "w") as f:
    f.write(svg)

print(f"\nGenerated: {N} trunk dots, {sum(len(mb['commits']) for mb in merge_branches)} PR branch dots")
print(f"Right-side tracks: {len(merge_branches)} (max col {max_right_col})")
print(f"Left-side tracks: {len(dead_branches)} (max col {max_left_col})")
print(f"SVG: {svg_w}x{int(total_h)}")
