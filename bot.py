import discord
from discord.ext import commands, tasks
import random
from status2 import statuses  # Import danh sách trạng thái từ status2.py
from autorole import set_auto_role, assign_auto_role  # Import hàm từ autorole.py
from welcome import set_welcome_channel, send_welcome_message  # Import hàm từ welcome.py


# Tạo đối tượng intents và bật các intent cần thiết
intents = discord.Intents.default()
intents.message_content = True  # Cần bật nếu bạn muốn bot đọc nội dung tin nhắn

# Khởi tạo bot với intents
client = commands.Bot(command_prefix='.', intents=intents)

status_task_started = False  # Thêm biến kiểm tra

@client.event
async def on_ready():
    global status_task_started
    if not status_task_started:  # Kiểm tra nếu task chưa khởi động
        change_status.start()
        status_task_started = True
    print(f'{client.user} đã đăng nhập!')

@client.command()
async def hello(ctx):
    await ctx.send('Xin chào bạn nhé!')

@client.command()
async def ping(ctx):
    latency = round(client.latency * 1000)  # Chuyển đổi độ trễ từ giây sang mili giây
    embed = discord.Embed(
        title="🏓 Ping Pong Ping Pong!",
        description=f"Độ Trễ Là: {latency}ms",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)
    
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    deleted = await ctx.channel.purge(limit=amount)
    
    embed = discord.Embed(
        title="🧹 Dọn dẹp tin nhắn",
        description=f"Đã xóa {len(deleted)} tin nhắn!",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Yêu cầu bởi {ctx.author}", icon_url=ctx.author.avatar.url)

    await ctx.send(embed=embed, delete_after=5)
    
@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    # Thay đổi quyền gửi tin nhắn của mọi người trong kênh
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    
    # Tạo embed thông báo khóa kênh
    embed = discord.Embed(
        title="🔒 Kênh đã bị khóa",
        description="Kênh này hiện đã bị khóa. Chỉ quản trị viên mới có thể gửi tin nhắn.",
        color=discord.Color.red()
    )
    embed.set_footer(text=f"Được yêu cầu bởi {ctx.author}", icon_url=ctx.author.avatar.url)
    
    # Gửi embed vào kênh
    await ctx.send(embed=embed)
    
import discord
from discord.ext import commands

@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    
    embed = discord.Embed(
        title="🔓 Kênh đã được mở khóa",
        description="Kênh này hiện đã được mở khóa. Mọi người có thể gửi tin nhắn.",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Được yêu cầu bởi {ctx.author}", icon_url=ctx.author.avatar.url)
    
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    
    embed = discord.Embed(
        title="🚫 Thành viên đã bị cấm",
        description=f"{member.mention} đã bị cấm khỏi máy chủ.",
        color=discord.Color.red()
    )
    embed.add_field(name="Lý do", value=reason if reason else "Không có lý do cụ thể")
    embed.set_footer(text=f"Được yêu cầu bởi {ctx.author}", icon_url=ctx.author.avatar.url)
    
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member_name:
            await ctx.guild.unban(user)
            
            embed = discord.Embed(
                title="✅ Thành viên đã được gỡ cấm",
                description=f"{user.mention} đã được gỡ cấm khỏi máy chủ.",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Được yêu cầu bởi {ctx.author}", icon_url=ctx.author.avatar.url)
            
            await ctx.send(embed=embed)
            return
    
    await ctx.send("Không tìm thấy thành viên với tên đó trong danh sách bị cấm.")

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    
    embed = discord.Embed(
        title="👢 Thành viên đã bị Kick",
        description=f"{member.mention} đã bị đá khỏi máy chủ.",
        color=discord.Color.orange()
    )
    embed.add_field(name="Lý do", value=reason if reason else "Không có lý do cụ thể")
    embed.set_footer(text=f"Được yêu cầu bởi {ctx.author}", icon_url=ctx.author.avatar.url)
    
    await ctx.send(embed=embed)
    
@client.command()
async def avatar(ctx, member: discord.Member = None):
    # Nếu không chỉ định người dùng, lấy avatar của người sử dụng lệnh
    if member is None:
        member = ctx.author

    # Lấy URL của avatar
    avatar_url = member.avatar.url

    # Tạo embed hiển thị avatar
    embed = discord.Embed(
        title=f"Avatar của {member.display_name}",
        color=discord.Color.blue()
    )
    embed.set_image(url=avatar_url)
    embed.set_footer(text=f"Yêu cầu bởi {ctx.author}", icon_url=ctx.author.avatar.url)
    
    # Gửi embed
    await ctx.send(embed=embed)
    
@client.command()
async def status(ctx):
    try:
        # Đọc nội dung từ file status.txt
        with open("status.txt", "r", encoding="utf-8") as file:
            status_content = file.read()
        
        # Tạo embed để hiển thị trạng thái
        embed = discord.Embed(
            title="Trạng thái hiện tại",
            description=status_content,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Yêu cầu bởi {ctx.author}", icon_url=ctx.author.avatar.url)
        
        # Gửi embed
        await ctx.send(embed=embed)

    except FileNotFoundError:
        await ctx.send("Không tìm thấy file trạng thái!")

@client.command()
@commands.has_permissions(administrator=True)
async def setstatus(ctx, *, new_status: str):
    # Ghi nội dung mới vào file status.txt
    with open("status.txt", "w", encoding="utf-8") as file:
        file.write(new_status)
    
    # Phản hồi khi đã cập nhật trạng thái
    await ctx.send(f"Trạng thái đã được cập nhật thành công!")

@client.command()
async def trogiup(ctx):
    embed = discord.Embed(
        title="Danh sách lệnh của bot",
        description="Dưới đây là tất cả các lệnh hiện có:",
        color=discord.Color.blue()
    )
    
    # Duyệt qua tất cả các lệnh của bot và thêm tên vào embed
    for command in client.commands:
        embed.add_field(
            name=f".{command.name}",
            value="\u200b",  # Giá trị trống để không hiển thị mô tả
            inline=False
        )
    
    # Gửi embed với danh sách lệnh
    await ctx.send(embed=embed)
    
@tasks.loop(minutes=1)  # Thay đổi trạng thái mỗi 1 phút
async def change_status():
    # Chọn ngẫu nhiên một trạng thái từ danh sách
    current_status = random.choice(statuses)
    await client.change_presence(
        activity=discord.Game(name=current_status), 
        status=discord.Status.dnd
    )
    
# Lệnh thiết lập vai trò tự động
@client.command()
@commands.has_permissions(administrator=True)
async def setautorole(ctx, role: discord.Role):
    set_auto_role(role.id)  # Gọi hàm thiết lập auto role trong autorole.py
    await ctx.send(f"🪪 Đã thiết lập role tự động: {role.name}")

@client.event
async def on_member_join(member):
    await assign_auto_role(member)  # Gọi hàm cấp vai trò tự động từ autorole.py

# Lệnh thiết lập kênh chào mừng
@client.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, channel: discord.TextChannel):
    set_welcome_channel(channel.id)  # Gọi hàm thiết lập kênh chào mừng trong welcome.py
    await ctx.send(f"✅ Đã thiết lập kênh chào mừng: {channel.mention}")

# Sự kiện khi thành viên mới tham gia
@client.event
async def on_member_join(member):
    await send_welcome_message(member)  # Gọi hàm gửi tin nhắn chào mừng từ welcome.py

# token bot
client.run('MTMwMDIzNjMzMTI4ODM2NzE4NQ.GhiHFD.R6_EJm1xhOF3WG9Fjhx7HkLhN8xXoLStVzLZJQ')