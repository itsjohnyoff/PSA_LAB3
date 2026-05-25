import random
import numpy as np
import matplotlib.pyplot as plt

def simulate_theater_seating(num_seats=100):
    # track occupied seats
    available_seats = list(range(num_seats))
    
    # choose a random free seat for first passenger
    first_choice = random.choice(available_seats)
    available_seats.remove(first_choice)
    
    # simulate remaining passengers boarding
    for person in range(1, num_seats - 1):
        if person in available_seats:
            available_seats.remove(person)
        else:
            random_choice = random.choice(available_seats)
            available_seats.remove(random_choice)
            
    # check if last passenger gets their assigned seat
    last_person_seat = num_seats - 1
    return available_seats[0] == last_person_seat

def run_simulation(num_seats=100, num_trials=100_000):
    print(f"Running Monte Carlo simulation ({num_trials} trials)...")
    
    results = np.zeros(num_trials)
    for i in range(num_trials):
        # simulate one boarding process
        results[i] = 1 if simulate_theater_seating(num_seats) else 0
        
    # estimate probability
    success_count = np.sum(results)
    sim_prob = success_count / num_trials
    theo_prob = 0.5000
    
    print("\n--- Theater Seating Simulation Results ---")
    print(f"Total seats: {num_seats}")
    print(f"Total trials: {num_trials:,}")
    print(f"Successes (last person in correct seat): {int(success_count):,}\n")
    print(f"{'Metric':<25} | {'Value':<10}")
    print("-" * 38)
    print(f"{'Simulated Probability':<25} | {sim_prob:.4f}")
    print(f"{'Theoretical Probability':<25} | {theo_prob:.4f}")
    print(f"{'Absolute Difference':<25} | {abs(sim_prob - theo_prob):.5f}")
    
    # plot convergence behavior
    plot_convergence(results, theo_prob)

def plot_convergence(results, theo_prob):
    # set visual style
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # compute running probability
    num_trials = len(results)
    # subsample points to avoid heavy plotting
    step = 100
    indices = np.arange(step, num_trials + 1, step)
    running_successes = np.cumsum(results)
    running_prob = running_successes[indices - 1] / indices
    
    # plot running probability line
    ax.plot(indices, running_prob, color='#2b5c8f', linewidth=1.5, label='Running Monte Carlo Estimate')
    
    # plot theoretical expectation line
    ax.axhline(theo_prob, color='#d95f02', linestyle='--', linewidth=2, label=f'Theoretical Value ({theo_prob:.1f})')
    
    # format plot details
    ax.set_title('Monte Carlo Seating Probability Convergence', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Number of Trials', fontsize=12)
    ax.set_ylabel('Estimated Probability', fontsize=12)
    ax.set_ylim(0.4, 0.6)
    ax.set_xlim(0, num_trials)
    ax.legend(fontsize=10, loc='upper right', frameon=True, facecolor='white', edgecolor='#bdc3c7')
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # display results text box
    final_prob = running_successes[-1] / num_trials
    info_text = (f"Final Estimate: {final_prob:.4f}\n"
                 f"Theoretical:    {theo_prob:.4f}\n"
                 f"Difference:     {abs(final_prob - theo_prob):.5f}")
    box_style = dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#bdc3c7', alpha=0.9)
    ax.text(0.60, 0.20, info_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=box_style, fontfamily='monospace')
            
    plt.tight_layout()
    # save plot
    plt.savefig('theater_seating_convergence.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    run_simulation(100, 100_000)
