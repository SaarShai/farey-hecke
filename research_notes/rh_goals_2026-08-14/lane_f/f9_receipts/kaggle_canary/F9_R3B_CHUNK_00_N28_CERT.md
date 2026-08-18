# F9 R3b closed-contour certificate

q=9, N=28, sign=1, FULL BOX

```json
{
  "smoke_test": false,
  "q": 9,
  "N": 28,
  "sign": 1,
  "winding_ball": [
    0.9999999999730801,
    1.0000000000269198
  ],
  "winding_mid": 1.0,
  "certified_integer": 1,
  "integer_isolated": true,
  "closed_contour_status": "CLOSED_CONTOUR_CERTIFIED",
  "complete_closed_cover": true,
  "chunk_gate_pass": true,
  "det_calls": 16,
  "min_det_abs_lower_on_contour": 3.3786140676735547e-06,
  "max_dim_tail_upper": 3.0176558383945667e-18,
  "max_dim_tail_at": [
    0.37424980913253375,
    4.080138082773367
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
      "delta_arg": 1.5707975084171624,
      "delta_arg_rad_ball": [
        1.570797508374877,
        1.5707975084594477
      ],
      "wall_s": 67.17
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
      "delta_arg": 1.5707922230795706,
      "delta_arg_rad_ball": [
        1.570792223037283,
        1.5707922231218583
      ],
      "wall_s": 53.89
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
      "delta_arg": 1.5707951448282647,
      "delta_arg_rad_ball": [
        1.5707951447859798,
        1.5707951448705495
      ],
      "wall_s": 54.02
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
      "delta_arg": 1.5708004308545889,
      "delta_arg_rad_ball": [
        1.5708004308123062,
        1.5708004308968713
      ],
      "wall_s": 40.46
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
