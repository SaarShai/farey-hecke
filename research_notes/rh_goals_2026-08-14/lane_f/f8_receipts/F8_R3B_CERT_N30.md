# F8 R3b closed-contour certificate

N=30, sign=1, FULL BOX

```json
{
  "smoke_test": false,
  "N": 30,
  "sign": 1,
  "winding_ball": [
    0.9999992484226823,
    1.0000007515773177
  ],
  "winding_mid": 1.0,
  "certified_integer": 1,
  "integer_isolated": true,
  "closed_contour_status": "CLOSED_CONTOUR_CERTIFIED",
  "complete_closed_cover": true,
  "chunk_gate_pass": true,
  "det_calls": 17,
  "min_det_abs_lower_on_contour": 3.001027609746654e-06,
  "max_dim_tail_upper": 2.553040467117226e-13,
  "max_dim_tail_at": [
    0.4252300423737965,
    4.345760288321985
  ],
  "N_escalated_points": [
    [
      0.4252300423737965,
      4.345760788321986,
      34
    ]
  ],
  "tail_safety": 4,
  "edges": [
    {
      "edge": "bottom",
      "from": [
        0.4252300423737965,
        4.345759788321986
      ],
      "to": [
        0.42523204237379647,
        4.345759788321986
      ],
      "initial_samples": 5,
      "certified_segments": 4,
      "bisections": 0,
      "max_bisection_depth": 0,
      "delta_arg": 1.5707957882575863,
      "delta_arg_rad_ball": [
        1.5707947230104655,
        1.570796853504707
      ],
      "wall_s": 5.64
    },
    {
      "edge": "right",
      "from": [
        0.42523204237379647,
        4.345759788321986
      ],
      "to": [
        0.42523204237379647,
        4.345761788321986
      ],
      "initial_samples": 5,
      "certified_segments": 4,
      "bisections": 0,
      "max_bisection_depth": 0,
      "delta_arg": 1.5707930715576883,
      "delta_arg_rad_ball": [
        1.5707921835557648,
        1.5707939595596119
      ],
      "wall_s": 4.5
    },
    {
      "edge": "top",
      "from": [
        0.42523204237379647,
        4.345761788321986
      ],
      "to": [
        0.4252300423737965,
        4.345761788321986
      ],
      "initial_samples": 5,
      "certified_segments": 4,
      "bisections": 0,
      "max_bisection_depth": 0,
      "delta_arg": 1.5707968647087476,
      "delta_arg_rad_ball": [
        1.5707959492224741,
        1.570797780195021
      ],
      "wall_s": 4.51
    },
    {
      "edge": "left",
      "from": [
        0.4252300423737965,
        4.345761788321986
      ],
      "to": [
        0.4252300423737965,
        4.345759788321986
      ],
      "initial_samples": 5,
      "certified_segments": 4,
      "bisections": 0,
      "max_bisection_depth": 0,
      "delta_arg": 1.5707995816224725,
      "delta_arg_rad_ball": [
        1.5707977630774725,
        1.5708014001674724
      ],
      "wall_s": 4.91
    }
  ],
  "q": 8,
  "pin_name": "g8_pin_1",
  "s_box": {
    "re": "0.4252310423737965",
    "im": "4.345760788321986",
    "half_width": "1e-6"
  },
  "engine": {
    "path": "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py",
    "sha256": "693d2a88fd525e94c8ab6a63486e82fe0670d9dce142effbd5be5e324597212a"
  },
  "arcs_total": 16,
  "arcs_per_edge": 4,
  "N_head": 4,
  "prec_bits": 300
}
```
