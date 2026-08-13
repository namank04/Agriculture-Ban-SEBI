export const meta = {
  name: 'ban-methodology-research',
  description: 'Deep research: ban-period literature sweep + C1/C2 methodology menu + novel-method design with correctness audit',
  phases: [
    { title: 'Sweep', detail: '5 parallel lanes: India-2021, India-2007, global bans, causal methods, vol/basis methods' },
    { title: 'Verify', detail: 'per-lane citation verification (existence, metadata, pdf urls)', model: 'opus' },
    { title: 'Fetch', detail: 'archive accessible PDFs to 01_literature/papers/', model: 'opus' },
    { title: 'Critic', detail: 'completeness check; one supplementary round if gaps' },
    { title: 'Novel', detail: '3 independent publication-grade method designs' },
    { title: 'Audit', detail: '3-lens correctness panel per design (identification / inference / prior-art)' },
    { title: 'Synthesize', detail: 'bibliography + methodology menu + references ledger' },
  ],
}

const ROOT = '/Users/narayan/Desktop/agri_ban_project'

const CONTEXT = `PROJECT CONTEXT (be precise, this constrains everything):
Journal-grade empirical evaluation of India's 19/20-Dec-2021 SEBI suspension of futures trading
in 7 agri commodities (wheat, chana/chickpea, mustard complex, soybean complex, crude palm oil,
paddy non-basmati, moong), extended yearly through at least 2027. Research questions under
verification: C1 = causal effect of the suspension on SPOT price volatility (claimed +8-10% by a
prior lost analysis); C2 = volatility dynamics via GARCH(1,1) with ban dummy + behaviour of the
futures-spot BASIS (pre-ban trend only — banned commodities have NO futures post-Dec-2021).
DATA IN HAND: daily mandi (district & national) spot prices 2017-2025 for all 7 banned + 5
control candidates (castor, jeera/cumin, turmeric, guar seed, cotton; kapas ruled out - illiquid);
monthly district-level realized-vol panel (131k commodity-district-month cells, 11 commodities,
up to 384 districts each); pre-ban futures for CPO (full contract-level w/ volume+OI) and soon
chana+wheat (vendor daily c1-c3); controls' futures c1-c3 2017-2026; CBOT wheat; FCPO pending.
KEY EMPIRICAL FACTS ALREADY ESTABLISHED: two-way-FE DiD on log realized vol gives -16.4%
(p=.029, 11 commodity clusters) — but a placebo ban at Dec-2019 on pre-ban-only data gives
-13.6% (p=.046) and the binned joint lead test rejects (p=.033): naive DiD is DEAD by
pre-registered rules. Reason: POLICY ENDOGENEITY — the ban was imposed BECAUSE food-price
volatility/inflation was elevated in 2021 (treatment timing selected on the outcome; banned
commodities ran hotter than controls for ~12 months pre-ban, then mean-reverted).
Identification challenges: single treatment date (no staggering), only 7 treated / ~4 usable
control commodities (few clusters), volatile agricultural prices with seasonality, MSP (minimum
support price) and other policy confounders, controls partially contaminated (MCX cotton had
its own anti-speculation halt Aug-2022..Jan-2023).`

const PAPERS_SCHEMA = {
  type: 'object', required: ['papers'],
  properties: {
    papers: { type: 'array', items: { type: 'object',
      required: ['title', 'authors', 'year', 'venue', 'url', 'method', 'findings', 'relevance', 'ban_event'],
      properties: {
        title: { type: 'string' }, authors: { type: 'string' }, year: { type: 'string' },
        venue: { type: 'string', description: 'journal / WP series / report / thesis' },
        kind: { type: 'string', description: 'journal|working_paper|govt_report|thesis|book_chapter' },
        url: { type: 'string' }, pdf_url: { type: 'string', description: 'direct pdf link if found, else empty' },
        data_used: { type: 'string' }, method: { type: 'string' },
        findings: { type: 'string' }, relevance: { type: 'string', description: 'what we adopt or avoid for C1/C2' },
        ban_event: { type: 'string', description: 'which ban/episode or "methodology"' },
      } } },
    lane_notes: { type: 'string' },
  },
}

const VERIFY_SCHEMA = {
  type: 'object', required: ['papers'],
  properties: { papers: { type: 'array', items: { type: 'object',
    required: ['title', 'status', 'cite', 'url'],
    properties: {
      title: { type: 'string' },
      status: { type: 'string', description: 'verified|corrected|unverifiable' },
      cite: { type: 'string', description: 'full corrected citation: authors (year) title, venue' },
      url: { type: 'string' }, pdf_url: { type: 'string' },
      note: { type: 'string' },
    } } } },
}

const FETCH_SCHEMA = {
  type: 'object', required: ['files'],
  properties: { files: { type: 'array', items: { type: 'object',
    required: ['title', 'ok'],
    properties: { title: { type: 'string' }, ok: { type: 'boolean' },
      file: { type: 'string', description: 'filename saved under 01_literature/papers/' },
      note: { type: 'string' } } } } },
}

const CRITIC_SCHEMA = {
  type: 'object', required: ['gaps', 'extra_leads'],
  properties: {
    gaps: { type: 'array', items: { type: 'string' } },
    extra_leads: { type: 'array', items: { type: 'string' },
      description: 'specific papers or precise search queries still missing; empty if coverage is adequate' },
  },
}

const DESIGN_SCHEMA = {
  type: 'object',
  required: ['name', 'target', 'summary', 'assumptions', 'estimator', 'identification_argument',
             'inference_procedure', 'data_requirements', 'feasibility', 'failure_modes', 'why_publishable'],
  properties: {
    name: { type: 'string' }, target: { type: 'string', description: 'C1|C2|both' },
    summary: { type: 'string' },
    assumptions: { type: 'array', items: { type: 'string' } },
    estimator: { type: 'string', description: 'precise estimator incl. math sketch in plain LaTeX' },
    identification_argument: { type: 'string' },
    inference_procedure: { type: 'string' },
    data_requirements: { type: 'string' },
    feasibility: { type: 'string', description: 'effort grade + what exists in our data already' },
    failure_modes: { type: 'array', items: { type: 'string' } },
    why_publishable: { type: 'string' },
  },
}

const AUDIT_SCHEMA = {
  type: 'object', required: ['verdict', 'issues', 'fixes', 'confidence'],
  properties: {
    verdict: { type: 'string', description: 'sound|fixable|unsound' },
    issues: { type: 'array', items: { type: 'string' } },
    fixes: { type: 'array', items: { type: 'string' } },
    prior_art: { type: 'array', items: { type: 'string' } },
    confidence: { type: 'string', description: 'high|medium|low' },
  },
}

const LANES = [
  { key: 'india2021', prompt: `Find EVERY paper/report/thesis/working paper analysing India's Dec-2021 SEBI
agri-derivatives suspension (the 7-commodity futures ban). Known leads to verify and expand on: Gaurav & Pandey
(IIT Bombay / BIMTECH); Aggarwal, Chatterjee & Sehgal; Dey & Gairola (EPW 2024); ICRIER working paper(s)
(incl. WP 383 which we already hold); any NCDEX/MCX-commissioned or SEBI-internal studies; IIM working papers;
agricultural economics journals (Agricultural Economics Research Review, Indian Journal of Agricultural
Economics); SSRN; RBI/NITI Aayog commentary with empirical content. Search English sources, multiple phrasings:
"futures suspension India 2021", "SEBI ban agricultural derivatives", "commodity derivatives suspension chana
mustard", "NCDEX suspension impact volatility". For each: data, method, findings, what we can adopt/avoid.` },
  { key: 'india2007', prompt: `Find EVERY paper/report analysing India's EARLIER futures bans/delistings:
2007 delisting of tur & urad & wheat & rice futures; 2008 additions (chana, potato, soy oil, rubber);
the Abhijit Sen Committee report (2008) and its empirical annexes; guar gum/seed suspension 2012; any
relisting studies (wheat 2009, chana 2016). Known leads: Nath & Lingareddy (tur/urad, EPW); Sahadevan
(several studies); Bose (money & finance); Kolamkar; IIMA / IGIDR work; UNCTAD or FAO assessments;
Sen Committee minority note. Also any study of MCX cotton's own Aug-2022 halt. For each: data, method,
findings, what transfers to the 2021 episode.` },
  { key: 'global', prompt: `Find EVERY paper analysing futures-market bans/suspensions OUTSIDE India, plus
transferable-method papers from adjacent ban literatures. Core: US onion futures ban 1958 (Holbrook Working
1960; Aaron Johnson 1973; modern re-examinations e.g. onion price volatility post-ban studies); China's 2015
stock-index-futures restrictions (volatility/liquidity papers) and Chinese commodity-exchange cooling measures
(Dalian/Zhengzhou margin & position-limit episodes); any other country delisting agricultural futures.
Adjacent-with-transferable-methods: equity short-sale ban literature (Beber & Pagano 2013 JF design —
cross-sectional variation in ban exposure), futures speculation limits (CFTC position-limit studies,
Brunetti-Buyuksahin), Masters-hypothesis / financialization-of-commodities empirical designs (Irwin-Sanders).
For each: data, method, findings, and explicitly HOW the identification strategy maps to a single-date
all-treated ban like ours.` },
  { key: 'causal_methods', prompt: `Survey the econometric methods frontier for OUR exact causal problem:
single adoption date, 7 treated units vs ~4 clean controls, monthly panel 2017-2025, treatment timing
ENDOGENOUS to the outcome (ban triggered by high volatility), naive TWFE DiD already failed placebo +
pre-trend tests. Cover, with the canonical paper(s) for each: synthetic control (Abadie-Diamond-Hainmueller;
Abadie 2021 JEL conditions), augmented SCM (Ben-Michael-Feller-Rothstein), synthetic DiD
(Arkhangelsky et al 2021 AER), generalized synthetic control / interactive FE (Xu 2017; Bai 2009),
matrix completion (Athey et al), penalized/pooled SCM for MULTIPLE treated units (Abadie-L'Hour;
Cattaneo et al scpi), inference for few treated units (Conley-Taber; Ferman-Pinto; Chernozhukov-Wuthrich-Zhu
conformal; Firpo-Possebom placebo sensitivity), wild-cluster bootstrap with few clusters (MacKinnon-Webb),
honest pre-trends & sensitivity (Rambachan-Roth 2023; Roth 2022 pretest), Ashenfelter-dip / selection-on-
pre-trends corrections, changes-in-changes (Athey-Imbens 2006), BSTS/CausalImpact (Brodersen et al),
event studies with endogenous policy timing in finance/macro. For each: 1-line method, key assumption,
whether it survives policy endogeneity + mean-reverting outcomes, software availability (R/Python),
and verdict on fit for C1.` },
  { key: 'vol_basis_methods', prompt: `Survey methodology for C2 (volatility dynamics + futures-spot basis)
beyond plain GARCH(1,1)-with-ban-dummy, with canonical papers: structural breaks in variance (Inclan-Tiao
ICSS; Hillebrand 2005 on neglected breaks biasing GARCH persistence — directly relevant since our pre/post
persistence comparison is the test), Markov-switching GARCH (Haas-Mittnik-Paolella), GJR/EGARCH asymmetry,
realized volatility & HAR (Corsi 2009) on daily mandi data feasibility, jump-robust measures (bipower
variation), seasonality handling in ag vol (harvest cycles), volatility spillover/connectedness
(Diebold-Yilmaz) banned vs control vs international (CBOT/FCPO), price discovery shares for pre-ban period
(Hasbrouck information share; Gonzalo-Granger; Garbade-Silber) incl. application to Indian agri futures,
hedging effectiveness (Ederington), basis behaviour theory for storables (Working curve; Fama-French 1987),
futures trading & spot vol theory (Bessembinder-Seguin 1992; Danthine; Turnovsky), and the right way to
characterize a PRE-BAN basis trend when post-ban basis cannot exist (our C2 internal-inconsistency catch).
For each: 1-line method, what it would show, data adequacy with daily mandi medians (composition noise!),
verdict on fit for C2.` },
]

phase('Sweep')
log('Launching 5 literature/method lanes + 3 novel-method designers concurrently')

// ---- Novel-method branch (runs concurrently with the literature branch) ----
const DESIGN_ANGLES = [
  { key: 'design:endogeneity-robust-causal', angle: `a causal-identification innovation for C1 that DIRECTLY
confronts policy endogeneity of the ban date (treatment selected on lagged outcome). Think: combining synthetic
control on PRE-2021 (pre-run-up) fit windows with explicit modelling of the selection rule (the regulator's
reaction function), or a mean-reversion-adjusted comparative case design, or conformal/permutation inference
exploiting the 36 placebo commodities available on NCDEX/MCX that were NOT banned. The design must produce an
interpretable causal estimand for "effect of suspending futures on spot volatility".` },
  { key: 'design:vol-process', angle: `a volatility-process innovation for C2: a formally specified model of
how removing the futures market changes the spot variance process — e.g. GARCH with endogenous-break testing
where the break date is ESTIMATED not imposed (testing whether it coincides with the ban), or a two-regime
model where futures-market state enters the variance equation via observable proxies (basis, futures volume on
controls, international vol as exogenous driver), with likelihood-ratio machinery whose null distribution is
valid under the known break-selection issues (Hillebrand critique).` },
  { key: 'design:cross-market-info', angle: `an information/price-discovery design exploiting markets the ban
did NOT close: international futures for the same commodities (CBOT wheat, Bursa FCPO vs domestic spot),
controls' domestic futures, and the cross-section of districts (spatial price dispersion as an information-
friction outcome — law-of-one-price convergence speed pre/post ban). The estimand: did the ban slow information
incorporation / raise spatial dispersion, mechanisms BEHIND any vol effect. Must be feasible with our district
panel + international dailies.` },
]

const designBranch = parallel(DESIGN_ANGLES.map(d => () =>
  agent(`${CONTEXT}

You are designing ONE novel, publication-grade empirical method for this project: ${d.angle}

Requirements (the user demands mathematical soundness — be rigorous, not hand-wavy):
- State the estimand formally. State EVERY identifying assumption explicitly and assess its plausibility
  in THIS setting (7 treated commodities, ~4 controls, single ban date, policy endogeneity, seasonal
  mean-reverting outcomes).
- Specify the estimator precisely (plain-LaTeX math sketch ok), the inference procedure VALID for the
  actual sample sizes (do NOT assert asymptotics in N when N=11), and a falsification/diagnostic battery.
- Search the literature (WebSearch) enough to ground the design in existing theory and to know what is
  genuinely novel vs incremental; cite the shoulders you stand on.
- Be honest about failure modes. Novelty must not come at the price of correctness.
Return via StructuredOutput.`, { label: d.key, phase: 'Novel', schema: DESIGN_SCHEMA })
)).then(designs => {
  const kept = designs.filter(Boolean)
  log(`Novel designs drafted: ${kept.map(k => k.name).join(' | ')}`)
  // 3-lens correctness audit per design — the user's "very very important" check
  return parallel(kept.map(des => () =>
    parallel([
      ['identification', `Audit ONLY the identification logic: is the estimand well-defined? Does each stated
assumption actually deliver it? Does policy endogeneity (ban triggered by past volatility) or mean reversion
break it? Hunt for hidden assumptions the author did not state. Try hard to REFUTE.`],
      ['inference', `Audit ONLY the statistical inference: is the proposed inference valid at the ACTUAL sample
sizes (7 treated, ~4 control commodities, ~100 months, hundreds of districts but commodity-level shocks)?
Check: few-cluster problems, pre-testing distortions, break-search multiplicity (sup-type critical values),
permutation validity (exchangeability), conformal assumptions. Try hard to REFUTE.`],
      ['prior-art', `Audit ONLY novelty and correctness against the literature (use WebSearch aggressively):
does this design already exist under another name? Is any step known to be flawed/superseded? Name the closest
prior work. If it is essentially known, say so plainly — incremental is a verdict, not an insult.`],
    ].map(([lens, charge]) => () =>
      agent(`${CONTEXT}

PROPOSED NOVEL DESIGN (audit target):
${JSON.stringify(des, null, 1)}

You are a hostile referee. ${charge}
Verdict 'sound' only if you genuinely failed to break it; 'fixable' if specific repairs exist (list them);
'unsound' if fatally flawed. Return via StructuredOutput.`,
        { label: `audit:${lens}:${des.name.slice(0, 30)}`, phase: 'Audit', schema: AUDIT_SCHEMA })
    )).then(audits => ({ design: des, audits: audits.filter(Boolean) }))
  ))
})

// ---- Literature branch: find -> verify (pipeline, no barrier between lanes) ----
const lit = await pipeline(LANES,
  lane => agent(`${CONTEXT}

LANE: ${lane.key}. ${lane.prompt}

Rules: WebSearch/WebFetch extensively, multiple query phrasings. Only report papers you have actually seen
evidence of (a result page, abstract page, repository entry) — NO recalled-from-memory citations without a
live URL. Aim for completeness over brevity; include grey literature (committee reports, working papers,
theses). We already hold: ICRIER WP383, NCDEX AGRIDEX methodology note, Jha MSP paper. Return via
StructuredOutput.`, { label: `find:${lane.key}`, phase: 'Sweep', schema: PAPERS_SCHEMA }),
  (found, lane) => {
    if (!found || !found.papers.length) return { papers: [] }
    return agent(`You are a citation verifier. For EACH paper below, verify it EXISTS and the metadata is right:
search the exact title (quoted) + authors; confirm year/venue; find the best stable URL and a direct PDF link
if one is openly accessible (SSRN/RePEc/journal OA/instituional repository). Correct any wrong metadata
(status='corrected'), mark hallucinated/unfindable entries status='unverifiable'. Do not drop entries —
mark them. Papers:
${JSON.stringify(found.papers.map(p => ({ title: p.title, authors: p.authors, year: p.year, venue: p.venue, url: p.url })), null, 1)}
Return via StructuredOutput.`, { label: `verify:${lane.key}`, phase: 'Verify', schema: VERIFY_SCHEMA, model: 'opus' })
      .then(v => ({ lane: lane.key, raw: found.papers, verified: v ? v.papers : [] }))
  })

// barrier here is genuine: dedup needs ALL lanes before fetching (no double-downloads)
const laneResults = lit.filter(Boolean).filter(r => r.verified && r.verified.length)
const byTitle = new Map()
for (const r of laneResults) {
  for (const v of r.verified) {
    if (v.status === 'unverifiable') continue
    const raw = (r.raw || []).find(p => p.title.toLowerCase().slice(0, 40) === v.title.toLowerCase().slice(0, 40)) || {}
    const key = v.title.toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 60)
    if (!byTitle.has(key)) byTitle.set(key, { ...raw, ...v, lane: r.lane })
  }
}
let bib = [...byTitle.values()]
const unverifiable = laneResults.flatMap(r => r.verified.filter(v => v.status === 'unverifiable').map(v => v.title))
log(`Verified bibliography: ${bib.length} unique papers (${unverifiable.length} unverifiable dropped: ${unverifiable.slice(0, 5).join('; ')}${unverifiable.length > 5 ? '…' : ''})`)

// ---- Fetch PDFs in chunks ----
phase('Fetch')
const fetchable = bib.filter(p => p.pdf_url || p.url)
const chunks = []
for (let i = 0; i < fetchable.length; i += 8) chunks.push(fetchable.slice(i, i + 8))
const manifests = await parallel(chunks.map((chunk, ci) => () =>
  agent(`Archive papers as PDFs into ${ROOT}/01_literature/papers/ (create nothing else; NEVER touch 02_data/).
First run: ls "${ROOT}/01_literature/papers/" and skip any paper already present (match loosely on author/title).
For each paper below: try pdf_url then url with curl -L --max-time 90 -A "Mozilla/5.0 (Macintosh)" -o <dest>;
if the landing page is HTML, look for a pdf link in it (SSRN delivery, RePEc, journal OA) and WebFetch/curl that.
Name files <FirstAuthorSurname><Year>_<3-5word-slug>.pdf. After each download verify it IS a pdf
(head -c 4 == %PDF), else delete the file and mark ok=false with a note (paywalled/login-walled is a fine reason).
Papers: ${JSON.stringify(chunk.map(p => ({ title: p.title, cite: p.cite, url: p.url, pdf_url: p.pdf_url || '' })), null, 1)}
Return the manifest via StructuredOutput.`,
    { label: `fetch:${ci + 1}/${chunks.length}`, phase: 'Fetch', schema: FETCH_SCHEMA, model: 'opus' })
))
const fileIndex = new Map()
for (const m of manifests.filter(Boolean)) for (const f of m.files) if (f.ok && f.file) fileIndex.set(f.title.toLowerCase().slice(0, 40), f.file)
bib = bib.map(p => ({ ...p, saved_file: fileIndex.get(p.title.toLowerCase().slice(0, 40)) || '' }))
log(`Archived ${fileIndex.size}/${fetchable.length} PDFs to 01_literature/papers/`)

// ---- Completeness critic, one supplementary round max ----
phase('Critic')
const critic = await agent(`${CONTEXT}

A literature sweep on ban-period analysis + C1/C2 methodology just returned the bibliography below.
You are the completeness critic: what is MISSING? Think by source-type (SSRN, RePEc/IDEAS, EPW archive,
Indian agri-econ journals, SEBI/CCI/government committee reports, PhD theses via Shodhganga, UNCTAD/FAO/IFPRI,
CFTC studies) and by episode (2021 India, 2007-08 India, guar 2012, onion 1958, China 2015, position-limit
debates). Also check the methods lanes cover: SCM family, few-treated inference, honest pre-trends, GARCH
breaks, price discovery. List concrete extra_leads (specific papers or precise queries) ONLY where a real gap
exists; empty list if coverage is adequate.
Bibliography (title | venue | year | lane): 
${bib.map(p => `${p.title} | ${p.venue || ''} | ${p.year || ''} | ${p.lane}`).join('\n')}
Return via StructuredOutput.`, { label: 'completeness-critic', phase: 'Critic', schema: CRITIC_SCHEMA })

if (critic && critic.extra_leads && critic.extra_leads.length) {
  log(`Critic found gaps: ${critic.gaps.join('; ').slice(0, 300)} — running supplementary round (${critic.extra_leads.length} leads)`)
  const supp = await agent(`${CONTEXT}

Supplementary literature round. Chase EXACTLY these leads (papers or queries), nothing else:
${critic.extra_leads.map((l, i) => `${i + 1}. ${l}`).join('\n')}
Same rules: only report entries you can evidence with a live URL. Return via StructuredOutput.`,
    { label: 'find:supplementary', phase: 'Critic', schema: PAPERS_SCHEMA })
  if (supp && supp.papers.length) {
    const v = await agent(`Citation verifier (same charge as before): verify each, correct metadata, find pdf
links, mark unverifiable. Papers: ${JSON.stringify(supp.papers.map(p => ({ title: p.title, authors: p.authors, year: p.year, venue: p.venue, url: p.url })), null, 1)}
Return via StructuredOutput.`, { label: 'verify:supplementary', phase: 'Critic', schema: VERIFY_SCHEMA, model: 'opus' })
    const ok = (v ? v.papers : []).filter(x => x.status !== 'unverifiable')
    const fetched = ok.length ? await agent(`Archive these into ${ROOT}/01_literature/papers/ — identical rules
to the earlier fetch agents (ls first to avoid duplicates, curl with browser UA, %PDF check, ok=false when
paywalled). Papers: ${JSON.stringify(ok.map(x => ({ title: x.title, cite: x.cite, url: x.url, pdf_url: x.pdf_url || '' })), null, 1)}
Return via StructuredOutput.`, { label: 'fetch:supplementary', phase: 'Critic', schema: FETCH_SCHEMA, model: 'opus' }) : null
    const sf = new Map()
    if (fetched) for (const f of fetched.files) if (f.ok && f.file) sf.set(f.title.toLowerCase().slice(0, 40), f.file)
    for (const x of ok) {
      const raw = supp.papers.find(p => p.title.toLowerCase().slice(0, 40) === x.title.toLowerCase().slice(0, 40)) || {}
      bib.push({ ...raw, ...x, lane: 'supplementary', saved_file: sf.get(x.title.toLowerCase().slice(0, 40)) || '' })
    }
    log(`Supplementary round added ${ok.length} verified papers`)
  }
}

// ---- Join the novel branch ----
const auditedDesigns = await designBranch
const survivors = auditedDesigns.filter(Boolean).map(({ design, audits }) => {
  const verdicts = audits.map(a => a.verdict)
  const unsound = verdicts.filter(v => v === 'unsound').length
  return { design, audits, keep: unsound === 0, verdicts }
})
log(`Novel designs after audit: ${survivors.map(s => `${s.design.name} [${s.verdicts.join(',')}] -> ${s.keep ? 'KEPT' : 'KILLED'}`).join(' | ')}`)

// ---- Synthesis ----
phase('Synthesize')
const synth = await agent(`${CONTEXT}

You are the synthesis writer. Inputs below: (A) verified deduplicated bibliography with archived-PDF filenames,
(B) three novel-method designs with full 3-lens hostile audits and keep/kill verdicts.

Write THREE artifacts (Read existing files first where noted; match the repo's documentation style — terse,
dense, no fluff):

1. ${ROOT}/01_literature/ban_literature_review.md — the annotated bibliography of ban-period analysis,
   organised by episode (India 2021 / India 2007-08 & guar 2012 / global / methods-causal / methods-vol-basis).
   Per entry: full citation, [saved: filename] or [url only], 1-2 lines data+method+finding, 1 line
   "for us: adopt/avoid/beware". End with a "coverage notes" section listing known-paywalled items and the
   unverifiable-claims we dropped. No redundancy with 01_literature/references.md — cross-reference it.

2. ${ROOT}/01_literature/methodology_menu_c1_c2.md — the decision menu for the researcher. Three parts:
   (i) C1 estimator menu: each candidate method, key assumption, does-it-survive-policy-endogeneity verdict,
   difficulty, software, our-data adequacy, and a RANKED recommendation (synthetic-control family expected on
   top — justify with the placebo/pre-trend facts). (ii) C2 menu: same treatment for vol/basis methods
   (flag the Hillebrand break-bias point against our current pre/post GARCH persistence comparison).
   (iii) NOVEL DESIGNS: for each surviving design — full specification, the audit verdicts with the issues
   and required fixes verbatim-summarised, honest novelty assessment, and what would make it publishable.
   Mark every choice "DECISION NEEDED (researcher)". Include killed designs in one short post-mortem paragraph
   each (why killed) so work is not silently lost.

3. Update ${ROOT}/01_literature/references.md (Read it FIRST, preserve its format exactly) — append the new
   verified entries with their archived filenames.

(A) BIBLIOGRAPHY: ${JSON.stringify(bib.map(p => ({ cite: p.cite, lane: p.lane, kind: p.kind, url: p.url, saved_file: p.saved_file, data_used: p.data_used, method: p.method, findings: p.findings, relevance: p.relevance, ban_event: p.ban_event, status: p.status })), null, 1)}

(B) NOVEL DESIGNS + AUDITS: ${JSON.stringify(survivors, null, 1)}

Return via StructuredOutput a summary: files written, counts, the ranked C1 recommendation in one line,
surviving novel designs in one line each, and the DECISION NEEDED list.`,
  { label: 'synthesis', phase: 'Synthesize', schema: {
    type: 'object', required: ['files_written', 'summary', 'decision_needed'],
    properties: { files_written: { type: 'array', items: { type: 'string' } },
      summary: { type: 'string' }, c1_recommendation: { type: 'string' },
      novel_kept: { type: 'array', items: { type: 'string' } },
      decision_needed: { type: 'array', items: { type: 'string' } } } } })

return { bibliography_count: bib.length, pdfs_archived: fileIndex.size,
  novel: survivors.map(s => ({ name: s.design.name, verdicts: s.verdicts, kept: s.keep })),
  synthesis: synth }