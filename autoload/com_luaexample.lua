
local function com_luaexample(message, com)
    asyncio.create_task(message.channel:send("Lua example runs successfully!"))
end

register_command("luaexample", com_luaexample)
