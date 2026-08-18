# F12 R3b closed-contour certificate

q=12, N=32, sign=1, FULL BOX

```json
{
  "smoke_test": false,
  "q": 12,
  "N": 32,
  "kappa": 5,
  "sign": 1,
  "winding_ball": [
    0.9999999630471621,
    1.0000000369528377
  ],
  "winding_mid": 0.9999999999999999,
  "certified_integer": 1,
  "integer_isolated": true,
  "closed_contour_status": "CLOSED_CONTOUR_CERTIFIED",
  "complete_closed_cover": true,
  "chunk_gate_pass": true,
  "det_calls": 16,
  "min_det_abs_lower_on_contour": 3.7752891907009067e-06,
  "max_dim_tail_upper": 1.3142682889996904e-14,
  "max_dim_tail_at": [
    0.2873253025928323,
    3.4924065186049105
  ],
  "N_escalated_points": [],
  "tail_safety": 4,
  "edges": [
    {
      "edge": "bottom",
      "from": [
        0.2873248025928323,
        3.4924065186049105
      ],
      "to": [
        0.2873268025928322,
        3.4924065186049105
      ],
      "initial_samples": 5,
      "certified_segments": 4,
      "bisections": 0,
      "max_bisection_depth": 0,
      "delta_arg": 1.5707957527536005,
      "delta_arg_rad_ball": [
        1.570795667121058,
        1.570795838386143
      ],
      "wall_s": 19.53
    },
    {
      "edge": "right",
      "from": [
        0.2873268025928322,
        3.4924065186049105
      ],
      "to": [
        0.2873268025928322,
        3.4924085186049107
      ],
      "initial_samples": 5,
      "certified_segments": 4,
      "bisections": 0,
      "max_bisection_depth": 0,
      "delta_arg": 1.5707923710898224,
      "delta_arg_rad_ball": [
        1.5707923303377234,
        1.5707924118419216
      ],
      "wall_s": 15.61
    },
    {
      "edge": "top",
      "from": [
        0.2873268025928322,
        3.4924085186049107
      ],
      "to": [
        0.2873248025928323,
        3.4924085186049107
      ],
      "initial_samples": 5,
      "certified_segments": 4,
      "bisections": 0,
      "max_bisection_depth": 0,
      "delta_arg": 1.57079690049814,
      "delta_arg_rad_ball": [
        1.570796860779555,
        1.5707969402167248
      ],
      "wall_s": 15.69
    },
    {
      "edge": "left",
      "from": [
        0.2873248025928323,
        3.4924085186049107
      ],
      "to": [
        0.2873248025928323,
        3.4924065186049105
      ],
      "initial_samples": 5,
      "certified_segments": 4,
      "bisections": 0,
      "max_bisection_depth": 0,
      "delta_arg": 1.570800282838023,
      "delta_arg_rad_ball": [
        1.570800216763267,
        1.5708003489127789
      ],
      "wall_s": 11.74
    }
  ],
  "pin_name": "g12_pin_1",
  "pin_source": "f9f12_pin_finder.py -> f12_receipts/F12_PIN_SCAN.json (pins[0])",
  "s_box": {
    "re": "0.28732580259283225",
    "im": "3.4924075186049106",
    "half_width": "1e-6"
  },
  "engine": {
    "path": "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py",
    "sha256": "693d2a88fd525e94c8ab6a63486e82fe0670d9dce142effbd5be5e324597212a",
    "module": "zeta_cert_rosen_even",
    "parity": "even"
  },
  "arcs_total": 16,
  "arcs_per_edge": 4,
  "N_head": 4,
  "prec_bits": 300
}
```
