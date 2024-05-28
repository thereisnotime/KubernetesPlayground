import concurrent.futures
import requests
import time
import statistics
import argparse
import subprocess
import re
from prettytable import PrettyTable
from colorama import Fore, Style, init

def get_ports():
    # Command to get the output from ps aux filtering for kubectl port-forward in the servernetes namespace
    command = "ps aux | grep 'kubectl port-forward' | grep 'servernetes'"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    # Regex to find the port numbers
    port_regex = r'\b(\d+):7777\b'
    ports = re.findall(port_regex, result.stdout)
    
    # Convert ports to integers
    ports = [int(port) for port in ports if port.isdigit()]
    return ports

# Function to perform POST request and measure response time
def post_request(port):
    url = f"http://localhost:{port}"
    start_time = time.time()
    try:
        response = requests.post(url, json=payload)
        response_time = time.time() - start_time
        if 200 <= response.status_code < 300:
            last_word = response.text.split()[-1] if response.text else ''
            return port, response_time, response.status_code, last_word
        else:
            return port, None, response.status_code, None
    except requests.RequestException:
        return port, None, None, None

# Function to benchmark the endpoints
def benchmark(endpoints, total_requests):
    response_times = {port: [] for port in endpoints}
    total_failed_requests = {port: 0 for port in endpoints}
    last_words = {port: None for port in endpoints}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(total_requests):
            for port in endpoints:
                futures.append(executor.submit(post_request, port))
        
        for future in concurrent.futures.as_completed(futures):
            port, response_time, status_code, last_word = future.result()
            if response_time is not None:
                response_times[port].append(response_time)
                last_words[port] = last_word
            else:
                total_failed_requests[port] += 1
    
    return response_times, total_failed_requests, last_words

# Function to print benchmark results in a table
def print_results(response_times, total_failed_requests, last_words):
    table = PrettyTable()
    table.field_names = ["Port", "Language", "Max Response Time (s)", "Min Response Time (s)", "Avg Response Time (s)", "Total Time (ms)", "Total Requests Sent", "Total Failed Requests"]
    
    for port, times in response_times.items():
        last_word = last_words[port] if last_words[port] is not None else 'N/A'
        if times:
            max_time = max(times)
            min_time = min(times)
            avg_time = statistics.mean(times)
            total_time_ms = sum(times) * 1000  # Convert seconds to milliseconds
            table.add_row([
                port,
                f"{Fore.YELLOW}{last_word}{Style.RESET_ALL}",
                f"{Fore.GREEN}{max_time:.4f}{Style.RESET_ALL}",
                f"{Fore.GREEN}{min_time:.4f}{Style.RESET_ALL}",
                f"{Fore.GREEN}{avg_time:.4f}{Style.RESET_ALL}",
                f"{Fore.GREEN}{total_time_ms:.2f}{Style.RESET_ALL}",
                f"{Fore.CYAN}{len(times) + total_failed_requests[port]}{Style.RESET_ALL}",
                f"{Fore.RED}{total_failed_requests[port]}{Style.RESET_ALL}"
            ])
        else:
            table.add_row([
                port,
                f"{Fore.RED}No successful requests{Style.RESET_ALL}",
                f"{Fore.RED}No successful requests{Style.RESET_ALL}",
                f"{Fore.RED}No successful requests{Style.RESET_ALL}",
                f"{Fore.RED}No successful requests{Style.RESET_ALL}",
                f"{Fore.RED}No successful requests{Style.RESET_ALL}",
                f"{Fore.CYAN}{total_failed_requests[port]}{Style.RESET_ALL}",
                f"{Fore.RED}{total_failed_requests[port]}{Style.RESET_ALL}"
            ])
    
    print(table)

if __name__ == "__main__":
    # Initialize colorama
    init()

    # Get all 
    ports = get_ports()

    # Example JSON payload
    payload = {"example_key": "example_value"}

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Benchmark API endpoints")
    parser.add_argument("total_requests", type=int, help="Total number of requests to send")
    args = parser.parse_args()

    response_times, total_failed_requests, last_words = benchmark(ports, args.total_requests)
    print_results(response_times, total_failed_requests, last_words)
