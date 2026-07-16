# Compensation, time, and workflow evidence register

Date retrieved: 2026-07-16. These are planning inputs, not observed customer
costs. May-2025 national median wages are combined with March-2026 BLS
occupation-group total-compensation/wage ratios; the result is a derived mixed-
date loaded-rate scenario, not an occupation-specific employer-cost estimate.

| Review proxy | Wage | Load ratio | Derived loaded rate |
|---|---:|---:|---:|
| Data Entry Keyer | $19.88/h | 1.4568 | $28.96/h |
| Inspectors/testers/sorters/samplers/weighers (simple-QA proxy) | $23.35/h | 1.4873 | $34.73/h |
| Biological Technician | $27.65/h | 1.4445 | $39.94/h |
| Clinical laboratory reviewer (May 2024 annual $61,890 divided by 2,080 hours) | $29.75/h | 1.4445 | $42.98/h |
| Compliance Officer | $38.81/h | 1.4848 | $57.62/h |
| Financial Examiner | $45.27/h | 1.4848 | $67.22/h |

Derived loaded 10th/median/90th planning bands are: data entry
`$21.85/$28.96/$41.17`; simple QA `$25.39/$34.73/$55.69`; biological
technician `$28.01/$39.94/$58.99`; clinical lab `$26.40/$42.98/$68.05`;
compliance `$34.42/$57.62/$95.46`; financial examiner
`$40.15/$67.22/$124.35`; software-QA proxy `$42.67/$72.43/$115.98`; and
medical-scientist proxy `$45.00/$71.82/$123.46`; and biochemist/biophysicist
proxy `$51.58/$88.49/$139.67` per hour.

Primary sources: [BLS/O*NET Data Entry](https://www.onetonline.org/link/localwages/43-9021.00),
[Quality Control](https://www.onetonline.org/link/localwages/51-9061.00),
[Biological Technician](https://www.onetonline.org/link/localwages/19-4021.00),
[Compliance Officer](https://www.onetonline.org/link/localwages/13-1041.00),
[Financial Examiner](https://www.onetonline.org/link/localwages/13-2061.00),
[Clinical Laboratory](https://www.bls.gov/ooh/healthcare/clinical-laboratory-technologists-and-technicians.htm),
[Software QA](https://www.onetonline.org/link/localwages/15-1253.00),
[Medical Scientists](https://www.onetonline.org/link/localwages/19-1042.00),
[Biochemists/Biophysicists](https://www.onetonline.org/link/localwages/19-1021.00),
and [BLS employer compensation table 4](https://www.bls.gov/news.release/ecec.t04.htm).

Published platform prices are not wages: Prolific's $8–$12/h participant range
is about $11.42–$17.14/h corporate or $10.66–$16.00/h academic/nonprofit before
VAT. CloudResearch's $7.50–$10/h participant range is about $10.50–$14.00/h for
other buyers or $9.38–$12.50/h academic/nonprofit, before an optional 3% card
fee. MTurk charges reward ×1.20 normally or ×1.40 for HITs with 10+ assignments,
has no wage floor, and says it closes to new customers July 30, 2026. Managed
expert services are generally custom quotes. Sources:
[Prolific](https://researcher-help.prolific.com/en/articles/445239-what-is-your-pricing),
[CloudResearch](https://connect-researcher-help.cloudresearch.com/hc/en-us/articles/5046181555732-Project-Cost),
[CloudResearch funding fee](https://connect-researcher-help.cloudresearch.com/hc/en-us/articles/21117760032276-How-do-I-Fund-my-Connect-Account),
[MTurk](https://www.mturk.com/pricing), and
[AWS Ground Truth FAQ](https://aws.amazon.com/sagemaker/ai/groundtruth/faqs/).
Payment-card charges, taxes, and custom managed-service fees are excluded; these
published fragments are not all-in customer-price estimates.

## What is actually measurable

Software can measure order construction, confidence updates, API/browser
latency, import/export, digest verification, reviews-to-stop, and coverage.
Actual active review time, elapsed time, mistakes, corrections, skips,
adjudication, training, interruptions, and integration labor require real people
and a real workflow. AWS Ground Truth's output fields—acceptance time,
submission time, and active `timeSpentInSeconds`—provide an authoritative model
for the event schema: [AWS output data](https://docs.aws.amazon.com/sagemaker/latest/dg/sms-data-output.html).

Required pilot events: session/item shown, response, correction, skip,
visibility/pause, adjudication, stop evaluation, import/mapping/export, with
monotonic timestamps and a hash-chained manifest/order digest. Cost is:

```text
loaded reviewer rate * (active review + adjudication)/3600
+ loaded operator rate * recurring overhead/3600
+ compute + rework + amortized integration + license
```

No operational marketing claim is permitted until a preregistered participant
study shows a positive paired time/cost effect, noninferior error/adjudication,
and conservative value after all overhead on at least three frozen workloads
and one professional workflow.
