# PSA Laboratory 3

## Overview

This laboratory explores the modeling of a customer arrival process using a Poisson process. Specifically, we investigate the interarrival time distribution, the memoryless property of the exponential distribution, and verify the expected waiting time both theoretically and using a Monte Carlo simulation in Python.

## Problem 1 – Interesting Sequence Occurrences

### Problem Statement

Suppose customers arrive at a store according to a Poisson process with an average arrival rate of:
* $\lambda = 6$ customers per hour

The time between arrivals is exponentially distributed. You arrive at the store at time:
* $T = 50$ hours

and wait for the next customer to arrive. We determine:
1. The expected waiting time.
2. The exact theoretical result.
3. A simulation-based estimate.

### Mathematical Background

* **Poisson Process**: A counting process $\{N(t), t \ge 0\}$ is a homogeneous Poisson process with rate $\lambda > 0$ if events occur independently, and the number of events in any interval of length $t$ follows a Poisson distribution with mean $\lambda t$.
* **Exponential Distribution**: The interarrival times $X_1, X_2, \dots$ are independent and identically distributed (i.i.d.) random variables following an exponential distribution with rate parameter $\lambda$. The probability density function (PDF) is:
  $$f(x) = \lambda e^{-\lambda x}, \quad x \ge 0$$
  The mean time between arrivals is $E[X] = \frac{1}{\lambda}$.
* **Memoryless Property**: The exponential distribution is uniquely characterized by the memoryless property. For any $s, t \ge 0$:
  $$P(X > s + t \mid X > s) = P(X > t)$$
  This implies that the probability of waiting an additional time $t$ for an arrival, given that $s$ time has already elapsed since the last arrival, is independent of $s$.
* **Expected Waiting Time**: Let $W$ be the waiting time from $T = 50$ until the next customer arrives. By the memoryless property, the elapsed time since the last arrival does not affect the time until the next arrival. Thus, the remaining waiting time $W$ is also exponentially distributed with rate $\lambda = 6$:
  $$W \sim \text{Exp}(\lambda = 6)$$
  The expected waiting time is:
  $$E[W] = \frac{1}{\lambda} = \frac{1}{6} \text{ hours} \approx 0.1667 \text{ hours} \quad (10 \text{ minutes})$$

### Methodology

* **Theoretical Computation**: The expected waiting time is computed directly using the expectation formula of the exponential distribution:
  $$E[W] = \int_{0}^{\infty} w \cdot \lambda e^{-\lambda w} \, dw = \frac{1}{\lambda}$$
* **Monte Carlo Simulation**: 
  - For $N = 100,000$ independent trials, customer arrivals are generated starting from $t = 0$.
  - Interarrival times are sampled from $\text{Exp}(\lambda = 6)$.
  - The arrival times are accumulated until they exceed $T = 50$.
  - The waiting time for trial $j$ is calculated as $W_j = t_{\text{next}} - T$.
  - The Monte Carlo estimate is the sample mean of these waiting times:
    $$\bar{W} = \frac{1}{N} \sum_{j=1}^{N} W_j$$

### Output

* **Theoretical Waiting Time**: $0.1667$ hours ($10.0$ minutes).
* **Simulated Waiting Time**: $\approx 0.1670$ hours ($\approx 10.02$ minutes) (varies slightly per run).

![Waiting Time Distribution](waiting_time_distribution.png)

### Interpretation

The simulated expected waiting time closely matches the theoretical value of $10$ minutes. Despite arriving at a late hour ($T = 50$), the time we wait for the next customer does not depend on when the last customer arrived or how long the store has been open. The simulation results converge to the theoretical expectation as $N \to \infty$ by the Law of Large Numbers, verifying the memoryless property of the Poisson process.

## Problem 2 – Continuous Conditional Probability

### Problem Statement

A dart is thrown uniformly at random onto a circular target of radius 10 inches centered at the origin. Given that the dart lands in the upper half of the target ($y > 0$), we determine the following conditional probabilities:
1. The dart lands in the right half of the target ($x > 0$).
2. The distance from the center is less than 5 inches.
3. The distance from the center is greater than 5 inches.
4. The dart lands within 5 inches of the point $(0, 5)$.

### Mathematical Background

* **Geometric Probability**: For a uniform distribution over a region $C \subset \mathbb{R}^2$, the probability of the dart landing in a subregion $A \subseteq C$ is proportional to its area:
  $$P(A) = \frac{\text{Area}(A)}{\text{Area}(C)}$$
* **Conditional Probability**: The probability of event $E$ given the conditioning event $U$ is:
  $$P(E \mid U) = \frac{P(E \cap U)}{P(U)} = \frac{\text{Area}(E \cap U)}{\text{Area}(U)}$$
  For a circular target of radius $R = 10$, the upper half $U$ is a semicircle with area $\text{Area}(U) = \frac{1}{2} \pi R^2 = 50\pi$ square inches.
* **Area-Based Calculations**:
  - **Part A (Right Half)**: The region $R_h \cap U$ is the upper-right quadrant of the circle.
    $$\text{Area}(R_h \cap U) = \frac{1}{4} \pi R^2 = 25\pi \implies P(R_h \mid U) = \frac{25\pi}{50\pi} = 0.5000$$
  - **Part B (Distance < 5)**: The region $D_{<5} \cap U$ is a semicircle of radius $r = 5$.
    $$\text{Area}(D_{<5} \cap U) = \frac{1}{2} \pi r^2 = 12.5\pi \implies P(D_{<5} \mid U) = \frac{12.5\pi}{50\pi} = 0.2500$$
  - **Part C (Distance > 5)**: This is the complement of Part B:
    $$P(D_{>5} \mid U) = 1 - P(D_{<5} \mid U) = 1 - 0.2500 = 0.7500$$
  - **Part D (Within 5 of (0,5))**: The shifted circle $C_P$ of radius $r = 5$ centered at $P = (0, 5)$ lies entirely in the upper half-plane ($y \ge 0$) and inside the target disk. Thus, the intersection region is the entire disk $C_P$.
    $$\text{Area}(C_P \cap U) = \pi r^2 = 25\pi \implies P(\text{within 5 of } (0,5) \mid U) = \frac{25\pi}{50\pi} = 0.5000$$

### Methodology

* **Theoretical Derivation**: Derived using geometric area ratios as shown in the Mathematical Background section.
* **Monte Carlo Simulation**: 
  - $N = 1,000,000$ points are sampled uniformly in the bounding box $[-10, 10] \times [-10, 10]$.
  - Points outside the circular target (distance $> 10$) are rejected.
  - Darts landing in the upper half ($y > 0$) are selected to form the conditioning set $U$.
  - The conditional probabilities are estimated as the fraction of conditioning darts that satisfy each respective subregion criteria.

### Output

* **Theoretical Probabilities**:
  - Part A (Right half): $0.5000$
  - Part B (Distance < 5): $0.2500$
  - Part C (Distance > 5): $0.7500$
  - Part D (Within 5 of (0,5)): $0.5000$
* **Simulated Probabilities**:
  - Part A (Right half): $\approx 0.5004$
  - Part B (Distance < 5): $\approx 0.2498$
  - Part C (Distance > 5): $\approx 0.7502$
  - Part D (Within 5 of (0,5)): $\approx 0.4989$

![Dart Board Simulation Regions](dart_simulation_regions.png)

### Interpretation

As the number of simulated trials increases, the relative frequency of darts landing within each subregion approaches the ratio of the subregion's area to the semicircle's area. This empirical convergence to the theoretical probability is guaranteed by the Law of Large Numbers, verifying that the physical simulation correctly models the geometric probability space.

## Installation

Ensure you have Python 3 and the required libraries installed:

```bash
pip install numpy matplotlib
```

## Usage

To run the simulations and view the results/plots:

```bash
# Problem 1
python problem1.py

# Problem 2
python problem2.py
```

## Repository Structure

```
├── .gitignore                      # Git ignore patterns
├── README.md                       # Laboratory documentation
├── problem1.py                     # Problem 1 simulation script
├── problem2.py                     # Problem 2 simulation script
├── waiting_time_distribution.png   # Problem 1 visualization plot
└── dart_simulation_regions.png     # Problem 2 visualization plot
```

## Technologies Used

* Python 3
* NumPy
* Matplotlib

## Key Concepts

* Poisson Process
* Exponential Distribution
* Memoryless Property
* Geometric Probability
* Continuous Conditional Probability
* Monte Carlo Simulation