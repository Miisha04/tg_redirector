import asyncio
from telethon.sync import TelegramClient

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

    async def monitor_and_forward(self, source, target):
        await self.client.connect()

        # Ensure you're authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        print(f"Listening for new messages from {source}...")

        # Получаем ID последнего сообщения, чтобы начинать с новых
        last_message_id = (await self.client.get_messages(source, limit=1))[0].id if await self.client.get_messages(source, limit=1) else 0

        while True:
            # Получаем новые сообщения
            messages = await self.client.get_messages(source, min_id=last_message_id)

            for message in reversed(messages):
                try:
                    # Отправляем текст указанной цели
                    if message.text:
                        await self.client.send_message(target, message.text)
                        print(f"Forwarded message: {message.text}")
                    else:
                        print("Skipped non-text message")

                    # Обновляем последний ID сообщения
                    last_message_id = max(last_message_id, message.id)

                except ValueError as e:
                    print(f"Failed to send message: {e}")

            # Задержка перед следующим опросом
            await asyncio.sleep(2)

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

    print("Choose source type:")
    print("1. User ID")
    print("2. Username")

    source_choice = input("Enter your choice for source (1 or 2): ")

    if source_choice == "1":
        source = int(input("Enter the Source Chat/User ID: "))
    elif source_choice == "2":
        source = input("Enter the Source Username (e.g., @username): ")
    else:
        print("Invalid choice")
        return

    print("Choose target type:")
    print("1. User ID")
    print("2. Username")

    target_choice = input("Enter your choice for target (1 or 2): ")

    if target_choice == "1":
        target = int(input("Enter the Target Chat/User ID: "))
    elif target_choice == "2":
        target = input("Enter the Target Username (e.g., @username): ")
    else:
        print("Invalid choice")
        return

    await forwarder.monitor_and_forward(source, target)

# Start the event loop and run the main function
if __name__ == "__main__":
    asyncio.run(main())
