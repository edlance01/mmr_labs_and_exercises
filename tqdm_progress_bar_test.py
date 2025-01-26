from tqdm import tqdm
import time


def long_running_method(steps):
    """Simulates a method that takes time to execute in steps."""
    for _ in range(steps):
        time.sleep(0.1)  # Simulate work with a delay


# Wrap the method execution with a progress bar
def execute_with_progress_bar(method, steps):
    with tqdm(total=steps, desc="Processing", unit="step") as pbar:
        for _ in range(steps):
            method(1)  # Execute one step at a time
            pbar.update(1)


# Example usage
if __name__ == "__main__":
    total_steps = 50
    execute_with_progress_bar(long_running_method, total_steps)
