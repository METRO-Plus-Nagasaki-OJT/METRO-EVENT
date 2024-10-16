from cryptography.fernet import Fernet

def load_key(file_path):
    with open(file_path, 'r') as key_file:
        key = key_file.read()
    return key

def generate_key(file_path):
    with open(file_path, 'w') as key_file:
        key_file.write(r"nDjgKXPfLCRuQ3fvYSg-rJ0kg-tUTPx_GJvHYgsr2Rg=")