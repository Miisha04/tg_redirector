import asyncio
from telethon.sync import TelegramClient
import pyperclip


class TelegramForwarder:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient(
            f'session_{self.phone_number}',
            self.api_id,
            self.api_hash,
            device_model="Desktop",
            system_version="Windows 11",
            app_version="1.0",
            lang_code="en",
            system_lang_code="en"
        )

    async def send_clipboard_to_target(self, target):
        await self.client.connect()

        # Ensure you're authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        last_clipboard_content = None

        print("Starting to monitor clipboard...")
        while True:
            # Получаем текущий текст из буфера обмена
            clipboard_content = pyperclip.paste()

            # Проверяем, изменилось ли содержимое буфера обмена
            if clipboard_content and clipboard_content != last_clipboard_content:
                print(f"New clipboard content detected: {clipboard_content}")

                try:
                    # Отправляем текст указанной цели
                    await self.client.send_message(target, clipboard_content)
                    print("Message sent!")
                except ValueError as e:
                    print(f"Failed to send message: {e}")

                # Обновляем последнее содержимое буфера
                last_clipboard_content = clipboard_content

            # Задержка между проверками (0.5 секунды)
            await asyncio.sleep(0.5)


# Function to read credentials from file
def read_credentials():
    try:
        with open("credentials.txt", "r") as file:
            lines = file.readlines()
            api_id = lines[0].strip()
            api_hash = lines[1].strip()
            phone_number = lines[2].strip()
            return api_id, api_hash, phone_number
    except FileNotFoundError:
        print("Credentials file not found.")
        return None, None, None


# Function to write credentials to file
def write_credentials(api_id, api_hash, phone_number):
    with open("credentials.txt", "w") as file:
        file.write(api_id + "\n")
        file.write(api_hash + "\n")
        file.write(phone_number + "\n")


async def main():
    # Attempt to read credentials from file
    api_id, api_hash, phone_number = read_credentials()

    # If credentials not found in file, prompt the user to input them
    if api_id is None or api_hash is None or phone_number is None:
        api_id = input("Enter your API ID: ")
        api_hash = input("Enter your API Hash: ")
        phone_number = input("Enter your phone number: ")
        # Write credentials to file for future use
        write_credentials(api_id, api_hash, phone_number)

    forwarder = TelegramForwarder(api_id, api_hash, phone_number)

    print("Choose target type:")
    print("1. User ID")
    print("2. Username")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        target = int(input("Enter the User ID: "))
    elif choice == "2":
        target = input("Enter the Username (e.g., @username): ")
    else:
        print("Invalid choice")
        return

    await forwarder.send_clipboard_to_target(target)


# Start the event loop and run the main function
if __name__ == "__main__":
    asyncio.run(main())
