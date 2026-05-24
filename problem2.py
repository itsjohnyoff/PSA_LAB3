import numpy as np
import matplotlib.pyplot as plt

def run_dart_simulation(num_darts=1_000_000):
    # sample random coordinates in bounding box
    x = np.random.uniform(-10, 10, num_darts)
    y = np.random.uniform(-10, 10, num_darts)
    
    # filter points inside disk and in upper half
    in_disk = (x**2 + y**2 <= 100)
    in_upper_half = in_disk & (y > 0)
    upper_half_count = np.sum(in_upper_half)
    
    x_upper = x[in_upper_half]
    y_upper = y[in_upper_half]
    
    # count favorable outcomes
    right_half = np.sum(x_upper > 0)
    dist_less_5 = np.sum(x_upper**2 + y_upper**2 < 25)
    dist_greater_5 = np.sum(x_upper**2 + y_upper**2 > 25)
    near_point = np.sum(x_upper**2 + (y_upper - 5)**2 <= 25)
    
    # compare theory and experiment
    results = [
        ("a) Right half", right_half / upper_half_count, 0.5000),
        ("b) Distance < 5", dist_less_5 / upper_half_count, 0.2500),
        ("c) Distance > 5", dist_greater_5 / upper_half_count, 0.7500),
        ("d) Distance to (0,5) <= 5", near_point / upper_half_count, 0.5000)
    ]
    
    print("--- Conditional Probability Simulation Results ---")
    print(f"Total darts thrown: {num_darts:,}")
    print(f"Darts in upper half (conditioning event): {upper_half_count:,}\n")
    print(f"{'Condition':<28} | {'Simulated':<10} | {'Theoretical':<12} | {'Difference':<10}")
    print("-" * 69)
    for desc, sim, theo in results:
        diff = abs(sim - theo)
        print(f"{desc:<28} | {sim:.4f}     | {theo:.4f}      | {diff:.5f}")
        
    # plot simulation zones
    plot_results(x_upper[:10_000], y_upper[:10_000])

def plot_results(x_sample, y_sample):
    # set visual style
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # draw target boundaries
    target_circle = plt.Circle((0, 0), 10, color='#2c3e50', fill=False, linewidth=2, label='Target boundary (R=10)')
    inner_circle = plt.Circle((0, 0), 5, color='#2b5c8f', fill=True, alpha=0.1, linewidth=1.5, linestyle='--', label='Distance < 5')
    shifted_circle = plt.Circle((0, 5), 5, color='#d95f02', fill=True, alpha=0.15, linewidth=1.5, linestyle='-.', label='Within 5 of (0,5)')
    
    ax.add_patch(target_circle)
    ax.add_patch(inner_circle)
    ax.add_patch(shifted_circle)
    
    # draw division lines
    ax.axhline(0, color='#7f8c8d', linestyle='-', linewidth=1.5, label='y = 0 (Upper half boundary)')
    ax.axvline(0, color='#bdc3c7', linestyle=':', linewidth=1)
    
    # scatter sample darts in the upper half
    ax.scatter(x_sample, y_sample, s=2, color='#2c3e50', alpha=0.4, label='Simulated Darts (Upper Half)')
    
    # format plot details
    ax.set_title('Dart Board Simulation Regions & Subsets', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('X (inches)', fontsize=12)
    ax.set_ylabel('Y (inches)', fontsize=12)
    ax.set_xlim(-11, 11)
    ax.set_ylim(-1, 11)
    ax.set_aspect('equal')
    ax.legend(fontsize=9, loc='upper right', frameon=True, facecolor='white', edgecolor='#bdc3c7')
    ax.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    # save plot
    plt.savefig('dart_simulation_regions.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    run_dart_simulation(1_000_000)
