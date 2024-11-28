import discord

# ID của kênh chào mừng (khởi tạo là None, có thể đặt giá trị khi cần)
welcome_channel_id = None

# Hàm thiết lập kênh chào mừng
def set_welcome_channel(channel_id):
    global welcome_channel_id
    welcome_channel_id = channel_id

# Hàm gửi tin nhắn chào mừng
async def send_welcome_message(member):
    if welcome_channel_id is not None:
        channel = member.guild.get_channel(welcome_channel_id)
        if channel:
            embed = discord.Embed(
                title="👋🏻 Welcome To Server !",
                description=f"Xin chào {member.mention}, chào mừng bạn đã tham gia chúng tôi!",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url)
            await channel.send(embed=embed)