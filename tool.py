from PIL import Image

def hide_text_in_image(input_image_path, output_image_path, secret_text):
    image = Image.open(input_image_path)
    encoded_image = image.copy()

    binary_secret_text = ''.join(format(ord(char), '08b') for char in secret_text)
    text_length = len(binary_secret_text)

    # Ensure the text length can be represented using 16 bits
    if text_length > 65535:
        raise ValueError("Text is too long to be hidden in the image.")

    # Convert the text length to a 16-bit binary string
    text_length_binary = format(text_length, '016b')

    pixel_index = 0
    for char in text_length_binary + binary_secret_text:
        pixel = list(image.getpixel((pixel_index % image.width, pixel_index // image.width)))
        pixel[-1] = int(char)
        encoded_image.putpixel((pixel_index % image.width, pixel_index // image.width), tuple(pixel))
        pixel_index += 1

    # Save the encoded image
    encoded_image.save(output_image_path)

def extract_text_from_image(encoded_image_path):
    encoded_image = Image.open(encoded_image_path)
    binary_secret_text = ""

    pixel_index = 0
    text_length_binary = ""
    for _ in range(16):  # Read the 16 bits of text length
        pixel = encoded_image.getpixel((pixel_index % encoded_image.width, pixel_index // encoded_image.width))
        text_length_binary += str(pixel[-1])
        pixel_index += 1

    text_length = int(text_length_binary, 2)

    for _ in range(text_length):
        pixel = encoded_image.getpixel((pixel_index % encoded_image.width, pixel_index // encoded_image.width))
        binary_secret_text += str(pixel[-1])
        pixel_index += 1

    text = ""
    for i in range(0, len(binary_secret_text), 8):
        byte = binary_secret_text[i:i + 8]
        text += chr(int(byte, 2))

    return text

print("DOCTOR ENILNOS IMAGE STUFF HIDER OR SMTHNG LIKE THAT")


while 1:
    print("Choose Mode: 1=Write to Image | 2=Read from Image")
    mode = int(input(">> "))
    if mode == 1:
        input_image_path = input("Original Image: ")
        output_image_path = input("Where do you want to save the image: ")
        secret_text = input("What Message do you want to store in your image: ")
        hide_text_in_image(input_image_path, output_image_path, secret_text)
    elif mode == 2:
        output_image_path = input("What image do you want to Read: ")
        extracted_text = extract_text_from_image(output_image_path)
        print("Extracted Text:", extracted_text)
    else:
        print("Error, please choose between 1 and 2")