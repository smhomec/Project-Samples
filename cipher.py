# Create a function that will encode a message using a Caesar cipher that can 
# use the 15th letter after the one provided as the key.
def caesar_cipher(message):
    '''
    Encode a message using a Caesar cipher with a shift based on the 
    15th letter after the provided key.
    '''
    encoded_message = ""
    shift = 15 # Fixed shift value for the cipher
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - base + shift) % 26 + base)
            encoded_message += new_char
        else:
            encoded_message += char
    return encoded_message

# Ask the user to type a message
user_message = input("Enter a message to encode: ")
print(caesar_cipher(user_message))