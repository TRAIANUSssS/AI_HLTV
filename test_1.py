import time
from tqdm import tqdm

# Outer loop
outer_iterations = 5
# Inner loop
inner_iterations = 300

# Create the outer progress bar
with tqdm(total=24705) as pbar_outer:
    for i1 in range(outer_iterations):
        # Create the inner progress bar
        with tqdm(total=inner_iterations, desc='Inner Loop', leave=False, miniters=10, mininterval=0.5) as pbar_inner:
            for i2 in range(inner_iterations):
                # Do something, e.g., sleep
                time.sleep(0.01)
                # Update the inner progress bar
                pbar_inner.update(1)
        # Update the outer progress bar
        pbar_outer.update(1)