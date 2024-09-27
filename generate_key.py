import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()


def generate_encryption_key():
    if 'ENCRYPTION_KEY' in os.environ:
        print("Encryption key already exists.")
        return os.environ['ENCRYPTION_KEY']

    new_key = Fernet.generate_key().decode()

    with open('.env', 'a') as f:
        f.write(f"ENCRYPTION_KEY='{new_key}'\n")

    print(f"Generated new encryption key: {new_key}")
    return new_key


if __name__ == "__main__":
    generate_encryption_key()
