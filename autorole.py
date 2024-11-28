import discord

# Biến để lưu ID role tự động (khởi tạo là None)
auto_role_id = None

# Hàm thiết lập vai trò tự động
def set_auto_role(role_id):
    global auto_role_id
    auto_role_id = role_id

# Hàm xử lý sự kiện khi có thành viên mới
async def assign_auto_role(member):
    if auto_role_id is not None:
        role = member.guild.get_role(auto_role_id)
        if role:
            await member.add_roles(role)