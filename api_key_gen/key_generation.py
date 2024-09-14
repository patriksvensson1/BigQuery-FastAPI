import secrets
import key_database


def generate_key():
    max_retries = 100
    for _ in range(max_retries):
        key = secrets.token_hex(16)
        if not key_database.key_exists(key):
            key_database.add_key(key)
            return f'API key generated: {key}.'
    return f'Failed to generate API key, retried {max_retries} times.'


if __name__ == "__main__":
    generate_key()


