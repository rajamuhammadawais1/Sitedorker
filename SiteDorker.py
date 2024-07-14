import sys
import os
import subprocess
import logging
import configparser
import shutil
from multiprocessing import Pool
from logging.handlers import RotatingFileHandler
import pyfiglet

def setup_ascii_art():
    ascii_art = pyfiglet.figlet_format("Turkzada", font="slant")
    print(ascii_art)

def create_directories():
    sample_dorks_file_path = os.path.expanduser('~/myapp/config/sample_dorks.txt')
    log_file_path = '/var/log/myapp/app.log'
    os.makedirs(os.path.dirname(sample_dorks_file_path), exist_ok=True)
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    return sample_dorks_file_path, log_file_path

def create_config_file(sample_dorks_file_path, log_file_path):
    config_content = f"""
    [Paths]
    sample_dorks_file = {sample_dorks_file_path}

    [Logging]
    log_file = {log_file_path}
    """
    config_file_path = os.path.expanduser('~/myapp/config/config.ini')
    os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
    with open(config_file_path, 'w') as config_file:
        config_file.write(config_content)
    print(f"Configuration file '{config_file_path}' created with specified paths.")
    return config_file_path

def setup_logging(config_file_path):
    config = configparser.ConfigParser()
    config.read(config_file_path)
    log_file = config.get('Logging', 'log_file', fallback='/var/log/myapp/app.log')
    log_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    logging.basicConfig(handlers=[log_handler], level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def check_dependencies():
    dependencies = ['nmap', 'curl']
    for dep in dependencies:
        if not shutil.which(dep):
            print(f"{dep} is not installed. Please install it to proceed.")
            sys.exit(1)

def generate_sites_from_dork():
    try:
        print("Generating sites from dork...")
        subprocess.run(['echo', 'Dorking sites generation logic goes here'])
    except Exception as e:
        logging.error(f"Error generating sites from dork: {e}")
        print("An error occurred. Please check the log file for details.")

def scan_for_vulnerable_sites(site):
    try:
        print(f"Scanning {site} for vulnerabilities...")
        result = subprocess.run(['nmap', '-p80', site], capture_output=True, text=True)
        print(result.stdout)
        return result.stdout
    except Exception as e:
        logging.error(f"Error scanning site {site}: {e}")
        return f"Error scanning {site}: {e}"

def scan_sites_parallel(sites):
    with Pool(processes=4) as pool:
        results = pool.map(scan_for_vulnerable_sites, sites)
        for result in results:
            print(result)

def view_sample_dorks(config):
    try:
        print("Viewing sample dorks...")
        sample_dorks_path = config.get('Paths', 'sample_dorks_file', fallback='~/myapp/config/sample_dorks.txt')
        with open(sample_dorks_path, 'r') as file:
            dorks = file.readlines()
            for dork in dorks:
                print(dork.strip())
    except FileNotFoundError:
        print("Sample dorks file not found.")
    except Exception as e:
        logging.error(f"Error viewing sample dorks: {e}")
        print("An error occurred. Please check the log file for details.")

def show_instructions():
    print("For instructions, please refer to the user manual or help section.")

def exit_program():
    print("Exiting the program.")
    sys.exit()

def main():
    setup_ascii_art()
    sample_dorks_file_path, log_file_path = create_directories()
    config_file_path = create_config_file(sample_dorks_file_path, log_file_path)
    setup_logging(config_file_path)

    config = configparser.ConfigParser()
    config.read(config_file_path)

    check_dependencies()

    while True:
        print("\nSelect an Option:")
        print("1. Generate Sites From Dork")
        print("2. Scan For Vulnerable Sites")
        print("3. View Sample Dorks")
        print("4. For Instructions")
        print("5. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            generate_sites_from_dork()
        elif choice == '2':
            sites = ['example.com', 'test.com']
            scan_sites_parallel(sites)
        elif choice == '3':
            view_sample_dorks(config)
        elif choice == '4':
            show_instructions()
        elif choice == '5':
            exit_program()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
