certified rho* = [1.97395587760749810993628 +/- 3.69e-25] (upper-bound object; WORSE THAN 0.70: true Arb result reported; blocks over threshold: 1→3, +3, tail, 1→3, −2, tail, 2→3, +2, tail, 2→3, −2, tail, 3→3, +2, tail, 3→3, −2, tail)

## 2. Certified block bounds

| block | certified sup |θ_n(z)−c_j| upper bound | ratio to a_j·h_j |
|---|---:|---:|
| 1→2, +2, head | [0.145692331321380769343769 +/- 4.69e-25] | [0.543755611698494007472267 +/- 2.26e-25] |
| 1→3, +3, tail | [0.451349961469227562964439 +/- 4.33e-26] | [1.39017592934987433740050 +/- 1.22e-24] |
| 1→2, −1, head | [0.119978981227791315370640 +/- 3.29e-25] | [0.447787771235326160426074 +/- 3.34e-25] |
| 1→3, −2, tail | [0.640886445010421289476541 +/- 3.31e-26] | [1.97395587760749810993628 +/- 3.69e-25] |
| 2→3, +2, tail | [0.596147914496981854861437 +/- 1.67e-25] | [1.83615941467701725799497 +/- 4.42e-24] |
| 2→2, −1, head | [0.0808981696386693732958100 +/- 2.86e-26] | [0.301929643916046753086174 +/- 4.19e-25] |
| 2→3, −2, tail | [0.596147914496981854861437 +/- 1.67e-25] | [1.83615941467701725799497 +/- 4.42e-24] |
| 3→1, +1, head | [0.193815196049383778201456 +/- 3.42e-25] | [0.646388243049058694023515 +/- 4.57e-26] |
| 3→3, +2, tail | [0.558574133524274131781765 +/- 1.71e-25] | [1.72043066682714325306358 +/- 2.93e-24] |
| 3→2, −1, head | [0.173721543517871723077573 +/- 1.12e-25] | [0.648366755504751163715637 +/- 5.00e-25] |
| 3→3, −2, tail | [0.558574133524274131781765 +/- 1.71e-25] | [1.72043066682714325306358 +/- 2.93e-24] |

Tail rows use the requested all-n dominating inequality; the `arc_n0_sup` field in the receipt is the independent M=512 contour check at n0.
The centered-at-zero tail image-ball inclusion check is recorded with its certified margin in the receipt; it is not silently replaced by the tighter pointwise contour value.

## 3. Pole clearance

The pole margin is the certified distance from the pole to the closed source disc: `|pole−c_i|−R_i`. For a tail row, the displayed n0 pole is the closest pole and the same positive margin holds for every n≥n0.

| block | used branch | pole location | margin to closed source disc | verdict |
|---|---|---:|---:|---|
| 1→2, +2, head | theta_2 | [-3.23606797749978969640917 +/- 3.67e-24] | [2.22269916710603601609633 +/- 4.21e-24] | PASS |
| 1→3, +3, tail | theta_3 (n≥3) | [-4.85410196624968454461376 +/- 5.04e-25] | [3.84073315585593086430092 +/- 1.05e-24] | PASS |
| 1→2, −1, head | theta_-1 | [1.61803398874989484820459 +/- 3.17e-24] | [2.03171616148098344019863 +/- 2.38e-24] | PASS |
| 1→3, −2, tail | theta_-2 (n≥2) | [3.23606797749978969640917 +/- 3.67e-24] | [3.64975015023087828840321 +/- 4.46e-24] | PASS |
| 2→3, +2, tail | theta_2 (n≥2) | [-3.23606797749978969640917 +/- 3.67e-24] | [2.46813082303752839098476 +/- 1.56e-24] | PASS |
| 2→2, −1, head | theta_-1 | [1.61803398874989484820459 +/- 3.17e-24] | [1.85009683428763354278017 +/- 4.73e-24] | PASS |
| 2→3, −2, tail | theta_-2 (n≥2) | [3.23606797749978969640917 +/- 3.67e-24] | [3.46813082303752839098476 +/- 1.56e-24] | PASS |
| 3→1, +1, head | theta_1 | [-1.61803398874989484820459 +/- 3.17e-24] | [1.10237987356225289328078 +/- 9.40e-25] | PASS |
| 3→3, +2, tail | theta_2 (n≥2) | [-3.23606797749978969640917 +/- 3.67e-24] | [2.72041386231214774148537 +/- 4.11e-24] | PASS |
| 3→2, −1, head | theta_-1 | [1.61803398874989484820459 +/- 3.17e-24] | [1.48434588481235804507619 +/- 2.23e-24] | PASS |
| 3→3, −2, tail | theta_-2 (n≥2) | [3.23606797749978969640917 +/- 3.67e-24] | [3.10237987356225289328078 +/- 9.40e-25] | PASS |

## 4. Branch-cut clearance

For positive branches the table gives the lower bound for `Re(z+nλ)`; for negative branches it gives the lower bound for `Re(nλ−z)`. Tail rows use n0, and the expression increases with n.

| block | branch-cut expression | certified lower-bound interval | verdict |
|---|---|---:|---|
| 1→2, +2, head | `Re(z+nλ), n≥2` | [2.22269916710603601609633 +/- 4.21e-24] | PASS |
| 1→3, +3, tail | `Re(z+nλ), n≥3` | [3.84073315585593086430092 +/- 1.05e-24] | PASS |
| 1→2, −1, head | `Re(nλ−z), n≥1` | [2.03171616148098344019863 +/- 2.38e-24] | PASS |
| 1→3, −2, tail | `Re(nλ−z), n≥2` | [3.64975015023087828840321 +/- 4.46e-24] | PASS |
| 2→3, +2, tail | `Re(z+nλ), n≥2` | [2.46813082303752839098476 +/- 1.56e-24] | PASS |
| 2→2, −1, head | `Re(nλ−z), n≥1` | [1.85009683428763354278017 +/- 4.73e-24] | PASS |
| 2→3, −2, tail | `Re(nλ−z), n≥2` | [3.46813082303752839098476 +/- 1.56e-24] | PASS |
| 3→1, +1, head | `Re(z+nλ), n≥1` | [1.10237987356225289328078 +/- 9.40e-25] | PASS |
| 3→3, +2, tail | `Re(z+nλ), n≥2` | [2.72041386231214774148537 +/- 4.11e-24] | PASS |
| 3→2, −1, head | `Re(nλ−z), n≥1` | [1.48434588481235804507619 +/- 2.23e-24] | PASS |
| 3→3, −2, tail | `Re(nλ−z), n≥2` | [3.10237987356225289328078 +/- 9.40e-25] | PASS |

## 5. Receipt JSON

Float reconciliation is diagnostic-only: the input `tb_disc_opt.json` contains an overall reconnaissance value but no per-block result list. No M=512 n0 arc comparison exceeded the configured diagnostic tolerance. 
The final tail-family values are intentionally compared against the tail inequality, not against the pointwise float sample.

Standalone receipt: [TB_BLOCK_CERTIFICATES_RECEIPT.json](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_RECEIPT.json).

```json
{
  "M": 512,
  "all_branch_cut_clearances_pass": true,
  "all_pole_clearances_pass": true,
  "all_tail_image_balls_inside_with_margin": false,
  "backend": "python-flint Arb/Acb ball arithmetic",
  "blocks": [
    {
      "arc_cover": {
        "M": 512,
        "arc_enclosure": "Acb rectangular ball"
      },
      "arc_n0_sup": "[0.145692331321380769343769 +/- 4.69e-25]",
      "block": [
        1,
        2,
        2,
        false,
        false
      ],
      "certified_sup_upper_bound": "[0.145692331321380769343769 +/- 4.69e-25]",
      "label": "1->2, +2 (head)",
      "n0": 2,
      "ratio_less_than_0_70": true,
      "ratio_upper_bound": "[0.543755611698494007472267 +/- 2.26e-25]",
      "tail": false,
      "tail_denominator_at_n0": null,
      "tail_image_ball_inside_with_margin": null,
      "tail_image_ball_margin": null,
      "tail_image_radius": null,
      "tail_target_distance_upper": null
    },
    {
      "arc_cover": {
        "M": 512,
        "arc_enclosure": "Acb rectangular ball"
      },
      "arc_n0_sup": "[0.0693845180812098999266305 +/- 8.52e-27]",
      "block": [
        1,
        3,
        3,
        false,
        true
      ],
      "certified_sup_upper_bound": "[0.451349961469227562964439 +/- 4.33e-26]",
      "label": "1->3, +3 (tail)",
      "n0": 3,
      "ratio_less_than_0_70": false,
      "ratio_upper_bound": "[1.39017592934987433740050 +/- 1.22e-24]",
      "tail": true,
      "tail_denominator_at_n0": "[3.84073315585593086430092 +/- 1.05e-24]",
      "tail_image_ball_inside_with_margin": false,
      "tail_image_ball_margin": "[-0.126678851906638183938338 +/- 1.48e-25]",
      "tail_image_radius": "[0.260366955844174987066732 +/- 4.61e-25]",
      "tail_target_distance_upper": "[0.451349961469227562964439 +/- 4.33e-26]"
    },
    {
      "arc_cover": {
        "M": 512,
        "arc_enclosure": "Acb rectangular ball"
      },
      "arc_n0_sup": "[0.119978981227791315370640 +/- 3.29e-25]",
      "block": [
        1,
        2,
        1,
        true,
        false
      ],
      "certified_sup_upper_bound": "[0.119978981227791315370640 +/- 3.29e-25]",
      "label": "1->2, -1 (head)",
      "n0": 1,
      "ratio_less_than_0_70": true,
      "ratio_upper_bound": "[0.447787771235326160426074 +/- 3.34e-25]",
      "tail": false,
      "tail_denominator_at_n0": null,
      "tail_image_ball_inside_with_margin": null,
      "tail_image_ball_margin": null,
      "tail_image_radius": null,
      "tail_target_distance_upper": null
    },
    {
      "arc_cover": {
        "M": 512,
        "arc_enclosure": "Acb rectangular ball"
      },
      "arc_n0_sup": "[0.0830089512152930273170374 +/- 1.77e-26]",
      "block": [
        1,
        3,
        2,
        true,
        true
      ],
      "certified_sup_upper_bound": "[0.640886445010421289476541 +/- 3.31e-26]",
      "label": "1->3, -2 (tail)",
      "n0": 2,
      "ratio_less_than_0_70": false,
      "ratio_upper_bound": "[1.97395587760749810993628 +/- 3.69e-25]",
      "tail": true,
      "tail_denominator_at_n0": "[2.22269916710603601609633 +/- 4.21e-24]",
      "tail_image_ball_inside_with_margin": false,
      "tail_image_ball_margin": "[-0.316215335447831910450440 +/- 1.58e-25]",
      "tail_image_radius": "[0.449903439385368713578834 +/- 4.51e-25]",
      "tail_target_distance_upper": "[0.640886445010421289476541 +/- 3.31e-26]"
    },
    {
      "arc_cover": {
        "M": 512,
        "arc_enclosure": "Acb rectangular ball"
      },
      "arc_n0_sup": "[0.214182942891143058981568 +/- 1.66e-27]",
      "block": [
        2,
        3,
        2,
        false,
        true
      ],
      "certified_sup_upper_bound": "[0.596147914496981854861437 +/- 1.67e-25]",
      "label": "2->3, +2 (tail)",
      "n0": 2,
      "ratio_less_than_0_70": false,
      "ratio_upper_bound": "[1.83615941467701725799497 +/- 4.42e-24]",
      "tail": true,
      "tail_denominator_at_n0": "[2.46813082303752839098476 +/- 1.56e-24]",
      "tail_image_ball_inside_with_margin": false,
      "tail_image_ball_margin": "[-0.271476804934392475835336 +/- 2.45e-26]",
      "tail_image_radius": "[0.405164908871929278963731 +/- 4.17e-25]",
      "tail_target_distance_upper": "[0.596147914496981854861437 +/- 1.67e-25]"
    },
    {
      "arc_cover": {
        "M": 512,
        "arc_enclosure": "Acb rectangular ball"
      },
      "arc_n0_sup": "[0.0808981696386693732958100 +/- 2.86e-26]",
      "block": [
        2,
        2,
        1,
        true,
        false
      ],
      "certified_sup_upper_bound": "[0.0808981696386693732958100 +/- 2.86e-26]",
      "label": "2->2, -1 (head)",
      "n0": 1,
      "ratio_less_than_0_70": true,
      "ratio_upper_bound": "[0.301929643916046753086174 +/- 4.19e-25]",
      "tail": false,
      "tail_denominator_at_n0": null,
      "tail_image_ball_inside_with_margin": null,
      "tail_image_ball_margin": null,
      "tail_image_radius": null,
      "tail_target_distance_upper": null
    },
    {
      "arc_cover": {
        "M": 512,
        "arc_enclosure": "Acb rectangular ball"
      },
      "arc_n0_sup": "[0.0973572651021819005282857 +/- 1.20e-26]",
      "block": [
        2,
        3,
        2,
        true,
        true
      ],
      "certified_sup_upper_bound": "[0.596147914496981854861437 +/- 1.67e-25]",
      "label": "2->3, -2 (tail)",
      "n0": 2,
      "ratio_less_than_0_70": false,
      "ratio_upper_bound": "[1.83615941467701725799497 +/- 4.42e-24]",
      "tail": true,
      "tail_denominator_at_n0": "[2.46813082303752839098476 +/- 1.56e-24]",
      "tail_image_ball_inside_with_margin": false,
      "tail_image_ball_margin": "[-0.271476804934392475835336 +/- 2.45e-26]",
      "tail_image_radius": "[0.405164908871929278963731 +/- 4.17e-25]",
      "tail_target_distance_upper": "[0.596147914496981854861437 +/- 1.67e-25]"
    },
    {
      "arc_cover": {
        "M": 512,
        "arc_enclosure": "Acb rectangular ball"
      },
      "arc_n0_sup": "[0.193815196049383778201456 +/- 3.42e-25]",
      "block": [
        3,
        1,
        1,
        false,
        false
      ],
      "certified_sup_upper_bound": "[0.193815196049383778201456 +/- 3.42e-25]",
      "label": "3->1, +1 (head)",
      "n0": 1,
      "ratio_less_than_0_70": true,
      "ratio_upper_bound": "[0.646388243049058694023515 +/- 4.57e-26]",
      "tail": false,
      "tail_denominator_at_n0": null,
      "tail_image_ball_inside_with_margin": null,
      "tail_image_ball_margin": null,
      "tail_image_radius": null,
      "tail_target_distance_upper": null
    },
    {
      "arc_cover": {
        "M": 512,
        "arc_enclosure": "Acb rectangular ball"
      },
      "arc_n0_sup": "[0.176609337063826729670103 +/- 1.33e-25]",
      "block": [
        3,
        3,
        2,
        false,
        true
      ],
      "certified_sup_upper_bound": "[0.558574133524274131781765 +/- 1.71e-25]",
      "label": "3->3, +2 (tail)",
      "n0": 2,
      "ratio_less_than_0_70": false,
      "ratio_upper_bound": "[1.72043066682714325306358 +/- 2.93e-24]",
      "tail": true,
      "tail_denominator_at_n0": "[2.72041386231214774148537 +/- 4.11e-24]",
      "tail_image_ball_inside_with_margin": false,
      "tail_image_ball_margin": "[-0.233903023961684752755664 +/- 3.62e-25]",
      "tail_image_radius": "[0.367591127899221555884058 +/- 2.47e-25]",
      "tail_target_distance_upper": "[0.558574133524274131781765 +/- 1.71e-25]"
    },
    {
      "arc_cover": {
        "M": 512,
        "arc_enclosure": "Acb rectangular ball"
      },
      "arc_n0_sup": "[0.173721543517871723077573 +/- 1.12e-25]",
      "block": [
        3,
        2,
        1,
        true,
        false
      ],
      "certified_sup_upper_bound": "[0.173721543517871723077573 +/- 1.12e-25]",
      "label": "3->2, -1 (head)",
      "n0": 1,
      "ratio_less_than_0_70": true,
      "ratio_upper_bound": "[0.648366755504751163715637 +/- 5.00e-25]",
      "tail": false,
      "tail_denominator_at_n0": null,
      "tail_image_ball_inside_with_margin": null,
      "tail_image_ball_margin": null,
      "tail_image_radius": null,
      "tail_target_distance_upper": null
    },
    {
      "arc_cover": {
        "M": 512,
        "arc_enclosure": "Acb rectangular ball"
      },
      "arc_n0_sup": "[0.131351102087849059590351 +/- 4.04e-25]",
      "block": [
        3,
        3,
        2,
        true,
        true
      ],
      "certified_sup_upper_bound": "[0.558574133524274131781765 +/- 1.71e-25]",
      "label": "3->3, -2 (tail)",
      "n0": 2,
      "ratio_less_than_0_70": false,
      "ratio_upper_bound": "[1.72043066682714325306358 +/- 2.93e-24]",
      "tail": true,
      "tail_denominator_at_n0": "[2.72041386231214774148537 +/- 4.11e-24]",
      "tail_image_ball_inside_with_margin": false,
      "tail_image_ball_margin": "[-0.233903023961684752755664 +/- 3.62e-25]",
      "tail_image_radius": "[0.367591127899221555884058 +/- 2.47e-25]",
      "tail_target_distance_upper": "[0.558574133524274131781765 +/- 1.71e-25]"
    }
  ],
  "blocks_source": {
    "assignment_line": 19,
    "blocks": [
      [
        1,
        2,
        2,
        false,
        false
      ],
      [
        1,
        3,
        3,
        false,
        true
      ],
      [
        1,
        2,
        1,
        true,
        false
      ],
      [
        1,
        3,
        2,
        true,
        true
      ],
      [
        2,
        3,
        2,
        false,
        true
      ],
      [
        2,
        2,
        1,
        true,
        false
      ],
      [
        2,
        3,
        2,
        true,
        true
      ],
      [
        3,
        1,
        1,
        false,
        false
      ],
      [
        3,
        3,
        2,
        false,
        true
      ],
      [
        3,
        2,
        1,
        true,
        false
      ],
      [
        3,
        3,
        2,
        true,
        true
      ]
    ],
    "count": 11,
    "exact_count_check": true,
    "expected_count": 11,
    "path": "/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/tb_disc_sweep.py"
  },
  "branch_cut_clearance": [
    {
      "block": [
        1,
        2,
        2,
        false,
        false
      ],
      "expression": "Re(z+n\u03bb), n\u22652",
      "margin": "[2.22269916710603601609633 +/- 4.21e-24]",
      "pass": true
    },
    {
      "block": [
        1,
        3,
        3,
        false,
        true
      ],
      "expression": "Re(z+n\u03bb), n\u22653",
      "margin": "[3.84073315585593086430092 +/- 1.05e-24]",
      "pass": true
    },
    {
      "block": [
        1,
        2,
        1,
        true,
        false
      ],
      "expression": "Re(n\u03bb\u2212z), n\u22651",
      "margin": "[2.03171616148098344019863 +/- 2.38e-24]",
      "pass": true
    },
    {
      "block": [
        1,
        3,
        2,
        true,
        true
      ],
      "expression": "Re(n\u03bb\u2212z), n\u22652",
      "margin": "[3.64975015023087828840321 +/- 4.46e-24]",
      "pass": true
    },
    {
      "block": [
        2,
        3,
        2,
        false,
        true
      ],
      "expression": "Re(z+n\u03bb), n\u22652",
      "margin": "[2.46813082303752839098476 +/- 1.56e-24]",
      "pass": true
    },
    {
      "block": [
        2,
        2,
        1,
        true,
        false
      ],
      "expression": "Re(n\u03bb\u2212z), n\u22651",
      "margin": "[1.85009683428763354278017 +/- 4.73e-24]",
      "pass": true
    },
    {
      "block": [
        2,
        3,
        2,
        true,
        true
      ],
      "expression": "Re(n\u03bb\u2212z), n\u22652",
      "margin": "[3.46813082303752839098476 +/- 1.56e-24]",
      "pass": true
    },
    {
      "block": [
        3,
        1,
        1,
        false,
        false
      ],
      "expression": "Re(z+n\u03bb), n\u22651",
      "margin": "[1.10237987356225289328078 +/- 9.40e-25]",
      "pass": true
    },
    {
      "block": [
        3,
        3,
        2,
        false,
        true
      ],
      "expression": "Re(z+n\u03bb), n\u22652",
      "margin": "[2.72041386231214774148537 +/- 4.11e-24]",
      "pass": true
    },
    {
      "block": [
        3,
        2,
        1,
        true,
        false
      ],
      "expression": "Re(n\u03bb\u2212z), n\u22651",
      "margin": "[1.48434588481235804507619 +/- 2.23e-24]",
      "pass": true
    },
    {
      "block": [
        3,
        3,
        2,
        true,
        true
      ],
      "expression": "Re(n\u03bb\u2212z), n\u22652",
      "margin": "[3.10237987356225289328078 +/- 9.40e-25]",
      "pass": true
    }
  ],
  "centers": [
    "[-0.713525491562421136153440 +/- 1.26e-25]",
    "[-0.500000000000000000000000 +/- 1e-29]",
    "[-0.190983005625052575897707 +/- 4.18e-25]"
  ],
  "certification_verdict": "FAIL_RHO_THRESHOLD_REPORT_TRUE_CERTIFIED_VALUES",
  "float_recon_diagnostic_only": {
    "arc_comparisons": [
      {
        "block": [
          1,
          2,
          2,
          false,
          false
        ],
        "flag": false,
        "status": "WITHIN_DIAGNOSTIC_TOLERANCE"
      },
      {
        "block": [
          1,
          3,
          3,
          false,
          true
        ],
        "flag": false,
        "status": "WITHIN_DIAGNOSTIC_TOLERANCE"
      },
      {
        "block": [
          1,
          2,
          1,
          true,
          false
        ],
        "flag": false,
        "status": "WITHIN_DIAGNOSTIC_TOLERANCE"
      },
      {
        "block": [
          1,
          3,
          2,
          true,
          true
        ],
        "flag": false,
        "status": "WITHIN_DIAGNOSTIC_TOLERANCE"
      },
      {
        "block": [
          2,
          3,
          2,
          false,
          true
        ],
        "flag": false,
        "status": "WITHIN_DIAGNOSTIC_TOLERANCE"
      },
      {
        "block": [
          2,
          2,
          1,
          true,
          false
        ],
        "flag": false,
        "status": "WITHIN_DIAGNOSTIC_TOLERANCE"
      },
      {
        "block": [
          2,
          3,
          2,
          true,
          true
        ],
        "flag": false,
        "status": "WITHIN_DIAGNOSTIC_TOLERANCE"
      },
      {
        "block": [
          3,
          1,
          1,
          false,
          false
        ],
        "flag": false,
        "status": "WITHIN_DIAGNOSTIC_TOLERANCE"
      },
      {
        "block": [
          3,
          3,
          2,
          false,
          true
        ],
        "flag": false,
        "status": "WITHIN_DIAGNOSTIC_TOLERANCE"
      },
      {
        "block": [
          3,
          2,
          1,
          true,
          false
        ],
        "flag": false,
        "status": "WITHIN_DIAGNOSTIC_TOLERANCE"
      },
      {
        "block": [
          3,
          3,
          2,
          true,
          true
        ],
        "flag": false,
        "status": "WITHIN_DIAGNOSTIC_TOLERANCE"
      }
    ],
    "comparison_performed": true,
    "note": "Float samples are not used in any certified value or verdict.",
    "source_opt_json": "/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/tb_disc_opt.json",
    "source_opt_json_has_per_block_results": false
  },
  "half_widths": [
    "[0.0954915028125262879488533 +/- 8.62e-27]",
    "[0.118033988749894848204587 +/- 1.66e-25]",
    "[0.190983005625052575897707 +/- 4.18e-25]"
  ],
  "lambda": "[1.61803398874989484820459 +/- 3.17e-24]",
  "partition_points": [
    "[-0.809016994374947424102293 +/- 4.18e-25]",
    "[-0.618033988749894848204587 +/- 1.66e-25]",
    "[-0.381966011250105151795413 +/- 1.66e-25]",
    "0"
  ],
  "pole_clearance": [
    {
      "block": [
        1,
        2,
        2,
        false,
        false
      ],
      "branch": "theta_2",
      "margin": "[2.22269916710603601609633 +/- 4.21e-24]",
      "pass": true,
      "pole_location": "[-3.23606797749978969640917 +/- 3.67e-24]"
    },
    {
      "block": [
        1,
        3,
        3,
        false,
        true
      ],
      "branch": "theta_3 (n\u22653)",
      "margin": "[3.84073315585593086430092 +/- 1.05e-24]",
      "pass": true,
      "pole_location": "[-4.85410196624968454461376 +/- 5.04e-25]"
    },
    {
      "block": [
        1,
        2,
        1,
        true,
        false
      ],
      "branch": "theta_-1",
      "margin": "[2.03171616148098344019863 +/- 2.38e-24]",
      "pass": true,
      "pole_location": "[1.61803398874989484820459 +/- 3.17e-24]"
    },
    {
      "block": [
        1,
        3,
        2,
        true,
        true
      ],
      "branch": "theta_-2 (n\u22652)",
      "margin": "[3.64975015023087828840321 +/- 4.46e-24]",
      "pass": true,
      "pole_location": "[3.23606797749978969640917 +/- 3.67e-24]"
    },
    {
      "block": [
        2,
        3,
        2,
        false,
        true
      ],
      "branch": "theta_2 (n\u22652)",
      "margin": "[2.46813082303752839098476 +/- 1.56e-24]",
      "pass": true,
      "pole_location": "[-3.23606797749978969640917 +/- 3.67e-24]"
    },
    {
      "block": [
        2,
        2,
        1,
        true,
        false
      ],
      "branch": "theta_-1",
      "margin": "[1.85009683428763354278017 +/- 4.73e-24]",
      "pass": true,
      "pole_location": "[1.61803398874989484820459 +/- 3.17e-24]"
    },
    {
      "block": [
        2,
        3,
        2,
        true,
        true
      ],
      "branch": "theta_-2 (n\u22652)",
      "margin": "[3.46813082303752839098476 +/- 1.56e-24]",
      "pass": true,
      "pole_location": "[3.23606797749978969640917 +/- 3.67e-24]"
    },
    {
      "block": [
        3,
        1,
        1,
        false,
        false
      ],
      "branch": "theta_1",
      "margin": "[1.10237987356225289328078 +/- 9.40e-25]",
      "pass": true,
      "pole_location": "[-1.61803398874989484820459 +/- 3.17e-24]"
    },
    {
      "block": [
        3,
        3,
        2,
        false,
        true
      ],
      "branch": "theta_2 (n\u22652)",
      "margin": "[2.72041386231214774148537 +/- 4.11e-24]",
      "pass": true,
      "pole_location": "[-3.23606797749978969640917 +/- 3.67e-24]"
    },
    {
      "block": [
        3,
        2,
        1,
        true,
        false
      ],
      "branch": "theta_-1",
      "margin": "[1.48434588481235804507619 +/- 2.23e-24]",
      "pass": true,
      "pole_location": "[1.61803398874989484820459 +/- 3.17e-24]"
    },
    {
      "block": [
        3,
        3,
        2,
        true,
        true
      ],
      "branch": "theta_-2 (n\u22652)",
      "margin": "[3.10237987356225289328078 +/- 9.40e-25]",
      "pass": true,
      "pole_location": "[3.23606797749978969640917 +/- 3.67e-24]"
    }
  ],
  "precision_bits": 384,
  "q": 5,
  "radius_multipliers": [
    "[3.14000000000000000000000 +/- 1e-28]",
    "[2.27000000000000000000000 +/- 3e-28]",
    "[1.70000000000000000000000 +/- 1e-28]"
  ],
  "rho_less_than_0_70": false,
  "rho_star": "[1.97395587760749810993628 +/- 3.69e-25]",
  "rho_star_upper_bound": "[1.97395587760749810993628 +/- 3.69e-25]",
  "schema": "tb-block-certificates/v1",
  "source_radii": [
    "[0.299843318831332544159399 +/- 3.36e-25]",
    "[0.267937154462261305424412 +/- 1.15e-25]",
    "[0.324671109562589379026101 +/- 1.91e-25]"
  ],
  "tail_pattern": "|theta_pm_n(z)| <= 1/(n*lambda-|c_i|-R_i), n>=n0; then |w-c_j| <= |w|+|c_j|",
  "tail_pattern_source": "projects/aristotle_dispatch_v17/TailBranchBound.lean:image_in_disc_with_margin",
  "threshold_0_70": "[0.700000000000000000000000 +/- 3e-29]",
  "worst_block": [
    1,
    3,
    2,
    true,
    true
  ]
}
```

## 6. Code listing/reference

The executable Arb certifier is [certify_tb_blocks.py](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tb_certify/certify_tb_blocks.py:1). Its `arc_ball`, `contour_sup`, `tail_dominating_bound`, `pole_margin`, and `branch_cut_margin` functions are the code paths that generated this receipt. The tail inclusion proof pattern is cited at `projects/aristotle_dispatch_v17/TailBranchBound.lean:image_in_disc_with_margin`.

```python
# Exact entry point used to generate this report
# /Users/za/.venvs/farey-rh/bin/python code/tb_certify/certify_tb_blocks.py \
#   --sweep-source /Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/tb_disc_sweep.py \
#   --opt-json /Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/tb_disc_opt.json \
#   --out-dir /Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g
```
