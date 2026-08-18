# F9 R3b closed-contour certificate

q=9, N=32, sign=1, FULL BOX

```json
{
  "smoke_test": false,
  "q": 9,
  "N": 32,
  "kappa": 7,
  "sign": 1,
  "winding_ball": [
    0.9999999999999665,
    1.0000000000000335
  ],
  "winding_mid": 1.0,
  "certified_integer": 1,
  "integer_isolated": true,
  "closed_contour_status": "CLOSED_CONTOUR_CERTIFIED",
  "complete_closed_cover": true,
  "chunk_gate_pass": true,
  "det_calls": 16,
  "min_det_abs_lower_on_contour": 3.3786140676871098e-06,
  "max_dim_tail_upper": 3.754947331675394e-21,
  "max_dim_tail_at": [
    0.37424980913253375,
    4.080140082773367
  ],
  "N_escalated_points": [],
  "tail_safety": 4,
  "edges": [
    {
      "edge": "bottom",
      "from": [
        0.3742478091325338,
        4.080138082773367
      ],
      "to": [
        0.37424980913253375,
        4.080138082773367
      ],
      "initial_samples": 5,
      "certified_segments": 4,
      "bisections": 0,
      "max_bisection_depth": 0,
      "delta_arg": 1.5707975084163004,
      "delta_arg_rad_ball": [
        1.5707975084162478,
        1.570797508416353
      ],
      "wall_s": 36.31
    },
    {
      "edge": "right",
      "from": [
        0.37424980913253375,
        4.080138082773367
      ],
      "to": [
        0.37424980913253375,
        4.080140082773367
      ],
      "initial_samples": 5,
      "certified_segments": 4,
      "bisections": 0,
      "max_bisection_depth": 0,
      "delta_arg": 1.5707922230796625,
      "delta_arg_rad_ball": [
        1.5707922230796099,
        1.570792223079715
      ],
      "wall_s": 29.13
    },
    {
      "edge": "top",
      "from": [
        0.37424980913253375,
        4.080140082773367
      ],
      "to": [
        0.3742478091325338,
        4.080140082773367
      ],
      "initial_samples": 5,
      "certified_segments": 4,
      "bisections": 0,
      "max_bisection_depth": 0,
      "delta_arg": 1.5707951448291266,
      "delta_arg_rad_ball": [
        1.570795144829074,
        1.5707951448291793
      ],
      "wall_s": 29.26
    },
    {
      "edge": "left",
      "from": [
        0.3742478091325338,
        4.080140082773367
      ],
      "to": [
        0.3742478091325338,
        4.080138082773367
      ],
      "initial_samples": 5,
      "certified_segments": 4,
      "bisections": 0,
      "max_bisection_depth": 0,
      "delta_arg": 1.570800430854497,
      "delta_arg_rad_ball": [
        1.5708004308544443,
        1.5708004308545496
      ],
      "wall_s": 22.0
    }
  ],
  "pin_name": "g9_pin_1",
  "pin_source": "f9f12_pin_finder.py -> f9_receipts/F9_PIN_SCAN.json (pins[0])",
  "s_box": {
    "re": "0.3742488091325338",
    "im": "4.080139082773367",
    "half_width": "1e-6"
  },
  "engine": {
    "path": "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen.py",
    "sha256": "965c2e5f65ae88b458d79bc425375e31589dcbf50703173664ef0e30901dceac",
    "module": "zeta_cert_rosen",
    "parity": "odd"
  },
  "arcs_total": 16,
  "arcs_per_edge": 4,
  "N_head": 4,
  "prec_bits": 300
}
```
