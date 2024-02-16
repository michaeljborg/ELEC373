import numpy as np
import matplotlib.pyplot as plt       

# Constants
service_rate = 0.75
packet_arrival_rates =  [0.2, 0.4, 0.5, 0.6, 0.65, 0.7, 0.72, 0.74, 0.745]
time_slots = 10**6

# Single Servere Queue simulation function
def single_server_queue(packet_arrival_rate):
    # Initialization
    time = 0
    packets_in_queue = 0
    total_time_in_system = 0
    total_packets_serviced = 0
    packet_arrival_times = []
    total_queue_length = 0

    # Begin with intial arrival service
    next_arrival_time = np.random.geometric(p=packet_arrival_rate)
    next_service_completion_time = float('inf')  # Initialize to 'infinity'

    while time < time_slots:
        # Packet Service
        if packets_in_queue > 0 and time == next_service_completion_time:
            # Update queue and serviced count
            packets_in_queue -= 1
            total_packets_serviced += 1

            # Pop out packet entry time into queue and add its total time spent in the system to the total
            arrival_time = packet_arrival_times.pop(0)
            total_time_in_system += time - arrival_time

            # Schedule next service time if queue has packets, if not set to infinity so next event is an arrival
            if packets_in_queue > 0:
                next_service_completion_time = time + np.random.geometric(p=service_rate)
            else:
                next_service_completion_time = float('inf')

        # Packet arrival
        if time == next_arrival_time:
            # Update queue and queue length
            packets_in_queue += 1
            total_queue_length += packets_in_queue

            # Store time of packet entry into queue
            packet_arrival_times.append(time)

            # Schedule next arrival time
            next_arrival_time = time + np.random.geometric(p=packet_arrival_rate)

            # Now that an arrival happened the queue is no longer empty and service scheduling can resume
            if next_service_completion_time == float('inf'):
                next_service_completion_time = time + np.random.geometric(p=service_rate)

        # Take minimum to advance to the next event
        time = min(next_arrival_time, next_service_completion_time)
    
    # Final Calculations and return
    avg_queue_length = total_queue_length / time_slots
    avg_queue_delay = total_time_in_system / total_packets_serviced
    return avg_queue_delay, avg_queue_length

# Store simulation reuslts for plotting
avg_lengths = []
avg_delays = []
theoretical_delays = []

# Simulate each packet arrival rate
for packet_arrival_rate in packet_arrival_rates:
    delay, length = single_server_queue(packet_arrival_rate)
    avg_delays.append(delay)
    avg_lengths.append(length)

# Theoretical queueing delay for each arrival rate
for packet_arrival_rate in packet_arrival_rates:
    theoretical_delays.append(1 / (service_rate - packet_arrival_rate)) 

# print theoretical delays
for lambda_example in packet_arrival_rates:
        theoretical_delay_example = 1 / (service_rate - lambda_example)
        print(f"Theoretical delay for Packet Arrival Rate = {lambda_example}: {theoretical_delay_example: .4f}")

# print simulation delays
print("\nSimulation Results")
for rate, delay, length in zip(packet_arrival_rates, avg_delays, avg_lengths):
    print(f"Packet Arrival Rate: {rate}, Average Queueing Delay: {delay: .4f}, Average Queue Length: {length: .4f}")

# Plotting
plotting_rates =  [0.2, 0.4, 0.5, 0.6, 0.65, 0.7, 0.745]
plt.figure(figsize=(12, 6))
plt.plot(packet_arrival_rates, avg_delays, marker='o', linestyle='-', color='b', label='Average Queueing Delay')
plt.plot(packet_arrival_rates, theoretical_delays, label='Theoretical Queueing Delay', linestyle='--', color='red')
plt.title('Average Queueing Delay vs. Packet Arrival Rate')
plt.xlabel('Packet Arrival Rate')
plt.ylabel('Average Queueing Delay')
plt.xticks(plotting_rates, labels=[str(rate) for rate in plotting_rates])
plt.grid(True)
plt.legend()
plt.show()