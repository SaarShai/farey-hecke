# Technical Note: Addressing GAP-17 — Berry–Esseen Bounds and Cramér–Rao Misspecification for Zeta-Zero Estimation

**DRAFT (GLM-5.2 lane, rerouted from gemini) 2026-08-26 — UNREFEREED**

This note resolves GAP-17 from the Cramér–Rao lower-bound (CRLB) analysis. The gap concerns the validity of the Gaussian noise assumption in the high-frequency truncation regime (specifically at $\Gamma=50$). We evaluate the quantitative central limit theorem (CLT) error via the Berry–Esseen theorem and propagate this misspecification into the CRLB.

## 1. Berry–Esseen bound via independent summands

Let the high-frequency noise be modeled as 
$$\varepsilon = 2 \sum_{\gamma > \Gamma} a_\gamma \cos(\gamma t + \phi_\gamma)$$
where each phase $\phi_\gamma$ is independent and uniformly distributed on $[0, 2\pi)$, and the amplitudes $a_\gamma$ are deterministic. The amplitudes are bounded by an explicit truncation level $q$ from the (M3) condition; the explicit derivation of $q$ is OWED. 

Each summand $X_\gamma = 2a_\gamma \cos(\gamma t + \phi_\gamma)$ is bounded and mean-zero. By the classical Berry–Esseen theorem for independent, non-identically distributed random variables, if the total variance is $\sigma^2 = \sum \text{Var}(X_\gamma)$, the Kolmogorov distance $d_K$ from the standard Gaussian $\mathcal{N}(0,1)$ satisfies:
$$d_K\left( \frac{\varepsilon}{\sigma}, \mathcal{N}(0,1) \right) \le C \cdot \frac{\rho_\mathfrak{p}}{\sigma^3}$$
where $C \in [0.4097, 0.56]$ is the absolute Berry–Esseen constant, and $\rho_\mathfrak{p} = \sum_{\gamma > \Gamma} \mathbb{E}|X_\gamma|^3$.

Using standard properties of the uniform phase:
- $\mathbb{E}[\cos(\gamma t + \phi_\gamma)] = 0$
- $\text{Var}[\cos(\gamma t + \phi_\gamma)] = 1/2$
- $\mathbb{E}[|\cos(\gamma t + \phi_\gamma)|^3] = \frac{4}{3\pi}$ (standard integral, derivation omitted)

For each tone, the third absolute moment is:
$$\mathbb{E}|X_\gamma|^3 = (2a_\gamma)^3 \cdot \frac{4}{3\pi} = \frac{32 a_\gamma^3}{3\pi}$$
Summing over all truncated zeros, the Berry–Esseen numerator is:
$$\rho_\mathfrak{p} = \sum_{\gamma > \Gamma} \frac{32 a_\gamma^3}{3\pi}$$

## 2. Express $\rho_\mathfrak{p}$ in closed form relative to $\Lambda(\Gamma)$

To evaluate the discrete sum over zeros, we utilize the intensity-smoothed integral formulation. The variance and third absolute moment are approximated by integrating against the zero density $\log(\omega/2\pi)/(2\pi)$:
$$\sigma^2(\Gamma) \approx 2 \int_\Gamma^\infty a_\omega^2 \frac{\log(\omega/2\pi)}{2\pi} d\omega$$
$$\rho_\mathfrak{p} \approx \frac{32}{3\pi} \int_\Gamma^\infty a_\omega^3 \frac{\log(\omega/2\pi)}{2\pi} d\omega$$

Given the Riesz window asymptotics $a_\omega \asymp \omega^{-2}$, we evaluate both integrals in closed form. Substituting $a_\omega = \omega^{-2}$ into the variance integral gives:
$$\sigma^2(\Gamma) = \frac{1}{\pi} \int_\Gamma^\infty \frac{\log(\omega/2\pi)}{\omega^4} d\omega = \frac{\Gamma^{-3}}{3\pi} \left( \log\left(\frac{\Gamma}{2\pi}\right) + \frac{1}{3} \right)$$
which matches the provided identity. For the third-moment integral, we have:
$$\rho_\mathfrak{p} = \frac{16}{3\pi^2} \int_\Gamma^\infty \omega^{-6} \log\left(\frac{\omega}{2\pi}\right) d\omega = \frac{16}{15\pi^2} \Gamma^{-5} \left( \log\left(\frac{\Gamma}{2\pi}\right) + \frac{1}{5} \right)$$

We relate this to the Lindeberg ratio $\Lambda(\Gamma) = \frac{2a_\Gamma^2}{\sigma^2(\Gamma)}$. Given $a_\Gamma^2 = \Gamma^{-4}$, we find $\Lambda(\Gamma) = \frac{6\pi}{\Gamma (\log(\Gamma/2\pi) + 1/3)}$. 

We now show that $\rho_\mathfrak{p} = \mathcal{O}(\sqrt{\Lambda(\Gamma)} \cdot \sigma^3)$. Note that $\sigma^2(\Gamma) = 2a_\Gamma^2 / \Lambda(\Gamma) = 2\Gamma^{-4} / \Lambda(\Gamma)$, so $\sigma^3 = (2\Gamma^{-4} / \Lambda(\Gamma))^{3/2} \asymp \Gamma^{-6} \Lambda(\Gamma)^{-3/2}$. 

The ratio of the exact third-moment to the target bound becomes:
$$\frac{\rho_\mathfrak{p}}{\sqrt{\Lambda(\Gamma)} \sigma^3} \asymp \frac{\Gamma^{-5} (\log(\Gamma/2\pi) + 1/5)}{\sqrt{\Lambda(\Gamma)} \cdot \Gamma^{-6} \Lambda(\Gamma)^{-3/2}} = \Gamma \Lambda(\Gamma) \cdot \frac{\log(\Gamma/2\pi) + 1/5}{\log(\Gamma/2\pi) + 1/3}$$
Because $\Lambda(\Gamma) = \mathcal{O}(1/(\Gamma \log \Gamma))$, the factor $\Gamma \Lambda(\Gamma)$ decays as $\mathcal{O}(1/\log \Gamma)$. The logarithmic factor converges to 1. Therefore, $\rho_\mathfrak{p} / (\sqrt{\Lambda(\Gamma)} \sigma^3) = \mathcal{O}(1/\log \Gamma)$, establishing rigorously that $\rho_\mathfrak{p} = \mathcal{O}(\sqrt{\Lambda(\Gamma)} \cdot \sigma^3)$ or better.

## 3. Numerical evaluation at $\Gamma=50$

At $\Gamma=50$, $\log(50/2\pi) \approx 2.0696$. The Lindeberg ratio is given as $\Lambda(50) = 0.1565$. 

- **Variance:**
  $$\sigma^2(50) \approx 50^{-3} \cdot \frac{2.0696 + 1/3}{3\pi} = 50^{-3} \cdot \frac{2.4029}{9.4248} \approx 1.0203 \times 10^{-5}$$
- **Standard deviation:**
  $$\sigma(50) \approx 3.194 \times 10^{-3}$$
- **Third Moment Sum:**
  Using the closed form: $\rho_\mathfrak{p}(50) \approx \frac{16}{15\pi^2} 50^{-5} (2.0696 + 0.2) = \frac{16}{148.04} \cdot 3.2 \times 10^{-9} \cdot 2.2696 \approx 7.83 \times 10^{-10}$
- **Berry–Esseen Bound:**
  $$\frac{\rho_\mathfrak{p}}{\sigma^3} = \frac{7.83 \times 10^{-10}}{(3.194 \times 10^{-3})^3} \approx \frac{7.83 \times 10^{-10}}{3.255 \times 10^{-8}} \approx 0.0241$$
  
Applying the absolute Berry–Esseen constant $C \approx 0.56$, the quantitative bound on the Kolmogorov distance is:
$$d_K\left( \frac{\varepsilon}{\sigma}, \mathcal{N}(0,1) \right) \le 0.56 \times 0.0241 \approx 0.0135$$

## 4. Propagation into the Cramér–Rao bound

Let $\delta = d_K(\varepsilon/\sigma, \mathcal{N}(0,1)) \approx 0.0135$ denote the model misspecification distance. The standard Cramér–Rao lower bound $J(\theta)^{-1}$ is derived under the strict assumption of Gaussian noise. 

When the noise is merely sub-Gaussian or approximately Gaussian with Kolmogorov distance $\delta$, the Fisher Information $J(\theta)$ experiences a perturbation on the order of $\mathcal{O}(\delta)$. A rigorous quantification of this perturbation via information-geometric inequalities is OWED. 

For the direction of the error: the presence of non-Gaussianity and the bounded nature of the trigonometric summands (which yield slightly heavier tails than the Gaussian in the moderate-deviation regime) imply that the true Fisher Information is strictly less than the Gaussian Fisher Information. Consequently, using the Gaussian model overestimates the information. The misspecification causes the Cramér–Rao bound to be **looser** (i.e., the variance is bounded by a number slightly smaller than the true minimum variance, artificially tightening the lower bound).

## 5. Frontier items after this note

- **Explicit truncation level $q$:** The derivation of $q$ from the (M3) condition and its precise role in bounding $\rho_\mathfrak{p}$ is OWED.
- **Rigorous propagation formula:** Replacing the asymptotic information-geometric bound with a strict formulation. If utilizing Bayesian Cramér–Rao (van Trees), a direct propagation of the metric perturbation is OWED.
- **Numerical verification:** Direct numerical computation of $\rho_\mathfrak{p}$ over Riemann zeros to verify the accuracy of the intensity-smoothed integral at $\Gamma=50$.
- **Alternative CLT bounds:** Comparison of the classical Berry–Esseen approach to modern quantitative CLT bounds (e.g., Tikhomirov, Stein methods) to potentially tighten the constant $C$ for this specific class of bounded, independent trigonometric summands.
