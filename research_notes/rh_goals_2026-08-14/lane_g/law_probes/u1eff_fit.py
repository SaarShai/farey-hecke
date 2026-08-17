"""u1eff_fit.py -- fit q-exponents from u1eff_entries.json / u1eff_det.json.

For each tracked entry E(q) we form the SUCCESSIVE difference
    D(q) = |E(2q+dq) - E(q)|      (proxy-free; QS is a doubling ladder)
and the PROXY difference to the largest q,
    P(q) = |E(q) - E(q_max)|,
then fit  log P ~ -alpha log q  by least squares over the available q.

Read-only; prints a table and writes u1eff_fit.json.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def fit(qs, vals):
    pts = [(math.log(q), math.log(v)) for q, v in zip(qs, vals) if v > 0]
    if len(pts) < 2:
        return None
    n = len(pts)
    sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0] ** 2 for p in pts); sxy = sum(p[0] * p[1] for p in pts)
    d = n * sxx - sx * sx
    if abs(d) < 1e-14:
        return None
    slope = (n * sxy - sx * sy) / d
    return -slope


def analyse(fn="u1eff_entries.json"):
    with open(os.path.join(HERE, fn)) as f:
        D = json.load(f)
    res = {}
    for pt, rows in D["points"].items():
        qs = sorted(int(q) for q in rows)
        qmax = qs[-1]
        res[pt] = {}
        for group in ("right_entries", "left_entries", "block_sup"):
            keys = rows[str(qs[0])][group].keys()
            g = {}
            for k in keys:
                def val(q):
                    v = rows[str(q)][group][k]
                    return complex(v[0], v[1]) if isinstance(v, list) else complex(v, 0)
                ref = val(qmax)
                pq, pv = [], []
                for q in qs[:-1]:
                    pq.append(q); pv.append(abs(val(q) - ref))
                a = fit(pq, pv)
                succ = []
                for i in range(len(qs) - 1):
                    succ.append((qs[i], abs(val(qs[i + 1]) - val(qs[i]))))
                asucc = fit([x[0] for x in succ[:-1]], [x[1] for x in succ[:-1]])
                g[k] = {"val_qmax": [ref.real, ref.imag], "abs_qmax": abs(ref),
                        "diff_to_qmax": pv, "alpha_proxy": a,
                        "succ_diff": [x[1] for x in succ], "alpha_succ": asucc}
            res[pt][group] = g
    return D, res


def main():
    D, res = analyse()
    for pt in res:
        print("=" * 78)
        print("POINT", pt, " qs =", D["qs"])
        for group in ("right_entries", "left_entries", "block_sup"):
            print("-- ", group)
            for k, v in sorted(res[pt][group].items()):
                if v["abs_qmax"] == 0 and max(v["succ_diff"]) == 0:
                    continue
                a = v["alpha_proxy"]; asu = v["alpha_succ"]
                print(f"   {k:22s} |val|={v['abs_qmax']:.6g}  "
                      f"alpha_proxy={'--' if a is None else f'{a:6.3f}'}  "
                      f"alpha_succ={'--' if asu is None else f'{asu:6.3f}'}  "
                      f"succdiff={[f'{x:.3g}' for x in v['succ_diff']]}")
    with open(os.path.join(HERE, "u1eff_fit.json"), "w") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
