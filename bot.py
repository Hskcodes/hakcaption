port random
from pyrogram import Client, filters
from pyrogram.types import Message

# Bot credentials
api_id = 25649636  # Replace with your API ID
api_hash = "43af470d1c625e603733268b3c2f7b8f"  # Replace with your API hash
bot_token = "7175839469:AAGZAd1HHRr77yOJK8tdExxjkziKiCA2SKM"  # Replace with your bot token

# List of allowed channel IDs
allowed_channels = [-1001802798611]  # Replace with your channel IDs

# Initialize the bot
app = Client("caption_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Load captions from the file
with open("captions.txt", "r") as file:
    captions = [line.strip() for line in file if line.strip()]

# Dictionary to store processed media_group_id
processed_albums = set()

@app.on_message(filters.channel & filters.media)
async def add_caption(client, message: Message):
    # Check if the message is from an allowed channel
    if message.chat.id not in allowed_channels:
        return
    
    # Check if the post is part of an album (multiple media)
    if message.media_group_id:
        # Skip if the album has already been processed
        if message.media_group_id in processed_albums:
            return
        
        # Mark the album as processed
        processed_albums.add(message.media_group_id)
    
    # Get the existing caption
    original_caption = message.caption or ""
    
    # Check if the caption starts with "nahi"
    if original_caption.lower().startswith("nahi"):
        # Remove "nahi" and update the message
        new_caption = original_caption[4:].strip()  # Remove "nahi" and any extra space
        await message.edit_caption(new_caption)
        return  # Skip adding a random caption
    
    # Choose a random caption
    random_caption = random.choice(captions)
    
    # Split the original caption to separate links if any
    split_caption = original_caption.split("http", 1)
    
    # Add "Here is your link" and "How to open"
    if len(split_caption) > 1:
        link = "http" + split_caption[1]
        main_caption = split_caption[0].strip()
        new_caption = (
            f"{random_caption}\n\n"
            f"Here is your link:\n{link}\n\n"
            f"[How to open](t.me/howtopenlink)\n\n"
        )
        await message.edit_caption(new_caption)
    else:
        # Add only the random caption if no link is present
        new_caption = random_caption
        await message.edit_caption(new_caption)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
