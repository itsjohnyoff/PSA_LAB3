import numpy as np
import matplotlib.pyplot as plt

def simulate_waiting_times(lambda_rate, target_time, num_trials):
    # estimate maximum arrivals needed
    max_arrivals = 450
    
    # sample interarrival times
    interarrivals = np.random.exponential(1.0 / lambda_rate, size=(num_trials, max_arrivals))
    
    # calculate arrival times
    arrival_times = np.cumsum(interarrivals, axis=1)
    
    # verify that all trials crossed the target time
    assert np.all(arrival_times[:, -1] > target_time), "Increase max_arrivals"
    
    # locate first arrival after target time
    first_arrival_idx = np.argmax(arrival_times > target_time, axis=1)
    
    # estimate waiting time
    waiting_times = arrival_times[np.arange(num_trials), first_arrival_idx] - target_time
    return waiting_times

def plot_results(waiting_times, lambda_rate, target_time):
    # set visual style
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(10, 6))

    # plot empirical histogram
    ax.hist(waiting_times, bins=100, density=True, alpha=0.6, color='#2b5c8f', 
            edgecolor='#1a3a60', linewidth=0.5, label='Simulated Waiting Time')

    # compute theoretical PDF
    w_vals = np.linspace(0, max(waiting_times), 1000)
    pdf_vals = lambda_rate * np.exp(-lambda_rate * w_vals)

    # plot theoretical PDF line
    ax.plot(w_vals, pdf_vals, color='#d95f02', linewidth=2.5, 
            label=f'Theoretical PDF: f(w) = {lambda_rate}e^(-{lambda_rate}w)')

    # format plot details
    ax.set_title('Waiting Time Distribution at T = 50 (Memoryless Property)', 
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Waiting Time (hours)', fontsize=12)
    ax.set_ylabel('Probability Density', fontsize=12)
    ax.set_xlim(0, max(waiting_times))
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.5)

    # compare theory and experiment
    sim_mean = np.mean(waiting_times)
    sim_mean_mins = sim_mean * 60
    theo_mean = 1.0 / lambda_rate
    theo_mean_mins = theo_mean * 60

    # display results on plot
    info_text = (f"Rate (\u03bb): {lambda_rate} customers/hr\n"
                 f"Target Time (T): {target_time} hr\n\n"
                 f"Theoretical expected wait:\n"
                 f"  {theo_mean:.4f} hr ({theo_mean_mins:.1f} mins)\n\n"
                 f"Monte Carlo estimate:\n"
                 f"  {sim_mean:.4f} hr ({sim_mean_mins:.2f} mins)\n\n"
                 f"Absolute difference:\n"
                 f"  {abs(sim_mean - theo_mean):.5f} hr")
    
    box_style = dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#bdc3c7', alpha=0.9)
    ax.text(0.55, 0.75, info_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=box_style, fontfamily='monospace')

    plt.tight_layout()
    # save plot
    plt.savefig('waiting_time_distribution.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    lambda_rate = 6
    target_time = 50
    num_trials = 100_000

    print(f"Running Monte Carlo simulation ({num_trials} trials)...")
    waiting_times = simulate_waiting_times(lambda_rate, target_time, num_trials)

    sim_mean = np.mean(waiting_times)
    theo_mean = 1.0 / lambda_rate

    print(f"Simulated mean waiting time: {sim_mean:.5f} hours ({sim_mean * 60:.2f} minutes)")
    print(f"Theoretical mean waiting time: {theo_mean:.5f} hours ({theo_mean * 60:.2f} minutes)")
    print(f"Difference: {abs(sim_mean - theo_mean):.5f} hours")

    # plot results
    plot_results(waiting_times, lambda_rate, target_time)
    print("Graph saved to waiting_time_distribution.png")
