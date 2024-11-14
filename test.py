import zlib
import base64
from cryptography.fernet import Fernet

# Function to generate a new key for encryption (you should save this key securely)
def generate_key():
    return Fernet.generate_key()

# Function to encrypt and compress a list of strings
def compress_and_encrypt(data_list, encryption_key):
    # Convert list to a string and encode it to bytes
    data_string = "\n".join(data_list)
    data_bytes = data_string.encode('utf-8')
    
    # Compress the data using zlib
    compressed_data = zlib.compress(data_bytes)
    
    # Encrypt the compressed data using Fernet encryption
    fernet = Fernet(encryption_key)
    encrypted_data = fernet.encrypt(compressed_data)
    
    # Return the encrypted and compressed data as a base64 encoded string
    return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

# Function to decrypt and decompress the encoded data
def decrypt_and_decompress(encoded_data, encryption_key):
    # Decode the base64 encoded string
    encrypted_data = base64.urlsafe_b64decode(encoded_data)
    
    # Decrypt the data using Fernet decryption
    fernet = Fernet(encryption_key)
    decrypted_data = fernet.decrypt(encrypted_data)
    
    # Decompress the data using zlib
    decompressed_data = zlib.decompress(decrypted_data)
    
    # Convert bytes back to string and split into a list
    data_string = decompressed_data.decode('utf-8')
    return data_string.split("\n")

# Example usage:
if __name__ == "__main__":
    # Generate encryption key (save it securely!)
    key = generate_key()
    
    # Example list of strings
    data = ["mod1", "mod2", "mod3", "mod4"]
    
    # Compress and encrypt the list
    encoded_data = compress_and_encrypt(data, key)
    print(f"Encoded Data: {encoded_data}")
    
    # Decrypt and decompress the list
    decoded_data = decrypt_and_decompress(encoded_data, key)
    print(f"Decoded Data: {decoded_data}")
