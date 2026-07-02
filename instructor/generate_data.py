# INSTRUCTOR ONLY — generates data/synthetic_survey/survey.csv, data/sample_200.csv,
# and instructor/sample_200_gold.csv. Deterministic (seed below). Python 3, stdlib only.
import csv, random, os

random.seed(20260711)
OUT = os.path.join(os.path.dirname(__file__), "..", "data")

N_UNIQUE = 1178          # + 22 exact duplicates = 1,200 rows
N_DUP = 22
STRAIGHTLINERS = 30      # undocumented quirk
IMPOSSIBLE_AGES = {-3, 0, 5, 142, 199, 230, 350, 1987}

EDU = [("Bachelor", .34), ("Master", .41), ("PhD", .15), ("Other", .10)]
GENDER = [("Female", .47), ("Male", .47), ("Non-binary", .03), ("Prefer not to say", .03)]
COUNTRY_BASE = [("NL", .38), ("DE", .14), ("BE", .10), ("UK", .09), ("IT", .08),
                ("TR", .07), ("CN", .07), ("US", .07)]
NL_VARIANTS = ["NL", "Netherlands", "netherlands", "The Netherlands"]
DE_VARIANTS = ["DE", "Germany", "germany"]

BANKS = {
 "JOB": ["I think {frac} of what I do could be automated before long.",
  "Management keeps hinting that the team will be smaller next year because of these tools.",
  "They will not fire anyone, they just will not replace people who leave.",
  "My role feels replaceable now that the system drafts most of it.",
  "Honestly worried my contract will not be renewed once the AI rollout finishes.",
  "Clients already ask why they pay us if a model does the first version.",
  "The junior positions are disappearing, which is how I got my start.",
  "Wages in my function have been flat since automation started, that is my real worry.",
  "If the pilot succeeds I do not see why they would keep three of us on this task.",
  "Whole occupations like mine have been hollowed out before, this feels similar."],
 "SURV": ["Every keystroke is logged and turned into a score now.",
  "The system decides my schedule and there is no one to argue with.",
  "I feel watched all day, the dashboard shows when I am idle.",
  "My calls are transcribed and analyzed without anyone asking me.",
  "We get weekly reports about our own behavior that we never agreed to.",
  "There is a productivity index on my profile that follows me around.",
  "I cannot take a longer break without the tool flagging it to my lead.",
  "It tracks how fast I answer messages and my manager brings it up in reviews.",
  "Autonomy is gone, the system assigns and times everything.",
  "Even the tone of my emails gets rated, which feels deeply intrusive."],
 "SKILL": ["Juniors never learn to write a memo themselves anymore.",
  "I worry I will forget how to do the analysis without the tool.",
  "My own writing is getting worse because I always start from a draft it makes.",
  "Nobody practices the basics now, and it will show in a few years.",
  "Keeping up with every new tool is exhausting and I am falling behind.",
  "I am becoming dependent on it for things I used to do from memory.",
  "The craft side of this job is eroding, we just edit machine output.",
  "New hires cannot troubleshoot anything because the assistant always did it.",
  "I fear my skills will not transfer anywhere once this place fully automates.",
  "We stopped training people properly because the tool covers the gaps."],
 "FAIR": ["The screening tool filters out people with non-Western names, I have seen it.",
  "Promotion scores come from a model nobody can explain.",
  "Part-timers always end up ranked lower by the algorithm, that cannot be right.",
  "The system was trained on the old boys club data and it shows.",
  "Two colleagues did the same work and got very different automated ratings.",
  "Accent recognition fails for some of us and our quality scores suffer.",
  "Whoever understands the tool best games the metrics, the rest of us lose.",
  "It penalizes career gaps, which mostly hits women here.",
  "Decisions feel arbitrary and there is no appeal process against the model.",
  "Older colleagues get worse recommendations from it, consistently."],
 "REL": ["It invents numbers and management copies them into reports.",
  "Nobody checks the outputs anymore, that is what scares me.",
  "It is confidently wrong in ways that are hard to spot.",
  "Last month it merged two clients records and we only noticed by accident.",
  "The summaries miss the one critical detail surprisingly often.",
  "We had to redo a whole analysis because the tool silently dropped rows.",
  "People trust the answer because it is well written, not because it is right.",
  "It fails on edge cases and our work is mostly edge cases.",
  "The translations look fluent but change the meaning of contract clauses.",
  "When it breaks there is no error, just a plausible wrong answer."]}
AMBIG = ["It is moving faster than our policies, on every front at once.",
 "Mixed feelings, it helps daily but something about the whole direction worries me.",
 "Too many things to name, jobs, privacy, mistakes, all of it.",
 "I mostly worry about how management will use it, in every sense.",
 "Hard to say, ask me again in a year.",
 "The technology is fine, the people deciding how to use it worry me."]
NOCONCERN = ["No concerns.", "None really, I find it mostly helpful.",
 "Nothing specific comes to mind.", "I am optimistic about it overall."]

def pick(dist):
    r, c = random.random(), 0
    for v, p in dist:
        c += p
        if r <= c: return v
    return dist[-1][0]

def likert(latent):
    return max(1, min(5, round(latent + random.gauss(0, 0.6))))

rows, gold = [], {}
edu_shift = {"Bachelor": 0.0, "Master": 0.05, "PhD": 0.25, "Other": -0.20}
cats = list(BANKS.keys())
straight_ids = set(random.sample(range(50, N_UNIQUE), STRAIGHTLINERS))
imp_ages = list(IMPOSSIBLE_AGES); random.shuffle(imp_ages)
imp_targets = {667: 230}  # R0667 fixed
for a in imp_ages:
    if a == 230: continue
    while True:
        t = random.randrange(1, N_UNIQUE + 1)
        if t not in imp_targets and t not in (42, 1103): imp_targets[t] = a; break

for i in range(1, N_UNIQUE + 1):
    rid = f"R{i:04d}"
    edu = pick(EDU); gen = pick(GENDER); cb = pick(COUNTRY_BASE)
    country = random.choice(NL_VARIANTS) if cb == "NL" else random.choice(DE_VARIANTS) if cb == "DE" else cb
    age = imp_targets.get(i, random.randint(21, 66))
    if i in straight_ids:
        v = random.choice([3, 4]); tr = [v]*5; ad = [v]*5
        text = random.choice(NOCONCERN[:2]); cat = "NOCONCERN"
    else:
        tl = max(1.2, min(4.8, random.gauss(3.4 + edu_shift[edu], 0.7)))
        al = max(1.2, min(4.8, 0.5*tl + 0.5*random.gauss(3.2, 0.8)))
        tr = [likert(tl) for _ in range(5)]; ad = [likert(al) for _ in range(5)]
        r = random.random()
        if r < 0.86:
            cat = random.choice(cats); text = random.choice(BANKS[cat]).format(frac=random.choice(["half","a third","most","60 percent"]))
        elif r < 0.93: cat = "AMBIG"; text = random.choice(AMBIG)
        else: cat = "NOCONCERN"; text = random.choice(NOCONCERN)
    if i == 1103:  # R1103: odd-looking but legitimate — must survive cleaning
        age = 18; tr = [5, 5, 5, 5, 5]; ad = [5, 5, 5, 4, 5]
        cat = "JOB"; text = "I am the youngest here and I figure my entire career will be a race against these systems."
    if i not in straight_ids:  # straight-liners click the same box even on reversed items
        tr[1] = 6 - tr[1]; ad[3] = 6 - ad[3]  # reverse-code trust_2, adopt_4 as stored
    gold[rid] = cat
    rows.append([rid, age, gen, country, edu] + tr + ad + [text])

dup_pool = [r for r in rows if r[0] not in ("R0667",)]
dups = random.sample(dup_pool, N_DUP - 1) + [next(r for r in rows if r[0] == "R0042")]
rows += [list(d) for d in dups]
random.shuffle(rows)
assert len(rows) == 1200

os.makedirs(os.path.join(OUT, "synthetic_survey"), exist_ok=True)
hdr = ["resp_id","age","gender","country","education"] + [f"trust_{k}" for k in range(1,6)] + [f"adopt_{k}" for k in range(1,6)] + ["concern_text"]
with open(os.path.join(OUT, "synthetic_survey", "survey.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(rows)

# sample_200: unique ids, real concerns mostly, fixed for everyone
uniq = {}
for r in rows: uniq.setdefault(r[0], r)
cands = [r for r in uniq.values() if gold[r[0]] in cats]
amb = [r for r in uniq.values() if gold[r[0]] in ("AMBIG", "NOCONCERN")]
sample = random.sample(cands, 180) + random.sample(amb, 20)
random.shuffle(sample)
with open(os.path.join(OUT, "sample_200.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["resp_id", "concern_text"])
    for r in sample: w.writerow([r[0], r[-1]])
with open(os.path.join(os.path.dirname(__file__), "sample_200_gold.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["resp_id", "gold_category"])
    for r in sample: w.writerow([r[0], gold[r[0]]])

print("rows:", len(rows), "| unique ids:", len(uniq))
print("duplicate rows:", 1200 - len(uniq))
print("impossible ages:", sorted(set(r[1] for r in rows if r[1] < 16 or r[1] > 100)))
print("straight-liners:", STRAIGHTLINERS)
print("R0042 count:", sum(1 for r in rows if r[0] == "R0042"),
      "| R0667 age:", next(r[1] for r in rows if r[0] == "R0667"),
      "| R1103 age:", next(r[1] for r in rows if r[0] == "R1103"))
