
function com_jsexample(message, com) {
    asyncio.create_task(message.channel.send("Javascript example runs successfully!"))
}

register_command("jsexample", com_jsexample)