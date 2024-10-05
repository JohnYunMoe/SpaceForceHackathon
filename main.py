# from cryptography.fernet import Fernet

# def generate_key():
#     key = Fernet.generate_key()
#     with open("secret.key", "wb") as key_file:
#         key_file.write(key)

# def load_key():
#     return open("secret.key", "rb").read()

# def encrypt_data(data: str) -> str:
#     key = load_key()
#     fernet = Fernet(key)
#     encrypted_data = fernet.encrypt(data.encode())
#     return encrypted_data.decode()

# def decrypt_data(encrypted_data: str) -> str:
#     key = load_key()
#     fernet = Fernet(key)
#     decrypted_data = fernet.decrypt(encrypted_data.encode())
#     return decrypted_data.decode()

response = self.__GETRequest(
                "satellites/private/" + str(norad_cat_id),
                {"live": live},
                auth=(self.username, self.password),
                stream=True,
            )

            if isinstance(response, str):
                print(response)  # Handle errors or text response
            else:
                content_type = response.headers.get('Content-Type')
                if 'image' in content_type:  # Ensure the response is an image
                    image_format = content_type.split("/")[-1]  # Extract the format (e.g., png, jpeg)
                    image_name = f"satellite_{norad_cat_id}_live.{image_format}"
                    image_path = os.path.join(os.getcwd(), image_name)

                    print(f"Saving image as: {image_path} (Content-Type: {content_type})")

                    try:
                        with open(image_path, 'wb') as image_file:
                            for chunk in response.iter_content(chunk_size=1024):
                                if chunk:
                                    image_file.write(chunk)
                        print(f"Image successfully saved as {image_name}")
                    except IOError as e:
                        print(f"Error saving image: {str(e)}")
                else:
                    print(f"Error: Expected an image, but received {content_type}")