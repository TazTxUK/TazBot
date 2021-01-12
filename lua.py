import lupa
from lupa import LuaRuntime

runtime = LuaRuntime(unpack_returned_tuples=True)

g = runtime.globals()

async def com_lua(message, com):
    f = message.content[4:]
    g.message = message
    runtime.execute(f)

