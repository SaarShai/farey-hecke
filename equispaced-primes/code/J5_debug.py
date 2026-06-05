"""Debug J_5 carefully."""
import mpmath as mp

mp.mp.dps = 40
mpf = mp.mpf

k_int = 5
k = mpf(k_int)

# Strip
u_lb_strip = max(mpf(2)/3, (k-1)/(k+1))  # = 2/3
u_ub_strip = (-9 + mp.sqrt(81 + 72*(k_int+1))) / 18  # k=5: (-9+sqrt(513))/18
print(f"Strip u-range: ({u_lb_strip}, {u_ub_strip}) = ({float(u_lb_strip):.10f}, {float(u_ub_strip):.10f})")

# Breakpoints
bp = set()
bp.add(u_lb_strip)
bp.add(u_ub_strip)
bp.add(k/(k+2))  # v_lo crossover: k/(k+2) = 5/7
bp.add((-9 + mp.sqrt(81+72*k_int))/18)  # v_hi crossover; for k=5: (-9+21)/18 = 2/3
bp.add((2*k_int - 9)/mpf(9))  # v_root vs (1+u)/k: (10-9)/9 = 1/9 (out of range)
bp.add(mp.sqrt(k)/3)  # v_root vs 2/(9u): sqrt(5)/3 ≈ 0.7454

bp = sorted([b for b in bp if u_lb_strip <= b <= u_ub_strip])
print(f"Breakpoints: {[float(b) for b in bp]}")

def vlo(u):
    return max((1+u)/(k+1), 1-u)
def vhi_nocap(u):
    return min((1+u)/k, mpf(2)/(9*u))
def vroot(u):
    return (u + mp.sqrt(u*u + mpf(8)*k/9)) / (2*k)
def integrand(u):
    vL = vlo(u)
    vH = min(vhi_nocap(u), vroot(u))
    if vH <= vL:
        return mpf(0)
    return 2*(vH - vL)

for i in range(len(bp)-1):
    a, b = bp[i], bp[i+1]
    if b - a < mpf(10)**-15: continue
    mid = (a+b)/2
    vL_m, vR_m, vH_m = vlo(mid), vroot(mid), vhi_nocap(mid)
    print(f"\n[{float(a):.6f}, {float(b):.6f}]: mid={float(mid):.6f}")
    print(f"  vlo={float(vL_m):.6f}, vhi_nocap={float(vH_m):.6f}, vroot={float(vR_m):.6f}")
    print(f"  integrand(mid) = 2*(min(vH,vR) - vL) = {float(2*(min(vH_m, vR_m) - vL_m)):.6e}")
    val = mp.quad(integrand, [a, b])
    print(f"  segment = {mp.nstr(val, 15)}")

total = mp.quad(integrand, bp)
print(f"\nTotal J_5 = {mp.nstr(total, 20)}")
