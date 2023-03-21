import cowsay
import asyncio
import datetime


unregister_clients = {}
clients = {}
names = set(cowsay.list_cows())


async def cowsay_chat(reader, writer):
    quit_flag = True
    login = False

    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(f'User {me} in chat')
    unregister_clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(unregister_clients[me].get())
    while (not reader.at_eof()) and quit_flag:
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)

        for q in done:
            if me not in clients.keys():
                client = unregister_clients[me]
            else:
                client = clients[me]

            if q is send:
                send = asyncio.create_task(reader.readline())
                result = q.result().decode().strip().split(' ', maxsplit=1)

                if len(result) == 1:
                    command, message = result[0], None
                else:
                    command, message = result

                if command == 'cows':
                    if message is not None:
                        await client.put('\nError: The "cows" command has no arguments\n')
                    else:
                        await client.put(f'\nAvailable names: {", ".join(names - set(clients.keys()))}\n')
                elif command == 'who':
                    if message is not None:
                        await client.put('\nError: The "who" command has no arguments\n')
                    else:
                        await client.put(f'\nUsers in chat: {", ".join(clients.keys())}\n')
                elif command == 'quit':
                    if message is not None:
                        await client.put('\nError: The "quit" command has no arguments\n')
                    else:
                        await client.put('\nYou quit chat\n')
                        for out in clients.values():
                            if out is not clients[me]:
                                await out.put(f'\n{me} quit chat\n')
                elif command == 'login':
                    if message is not None:
                        if me in clients.keys():
                            await client.put('\nError: You has already registered\n')
                        elif message not in names:
                            await client.put(f'\nError: The name {message} is not allowed\n')
                        elif message in clients.keys():
                            await client.put(f'\nError: The name {message} is occupied\n')
                        elif len(names - set(clients.keys())) == 0:
                            await client.put('\nError: The chat is full. Wait for someone to come out\n')
                        else:
                            print(f'User {me} has registered as {message}')
                            unregister_clients.pop(me)
                            me = message
                            clients[me] = asyncio.Queue()
                            login = True
                            await client.put(f'\nYou logged in under the name {me}\n')
                            for out in clients.values():
                                if out is not clients[me]:
                                    await out.put(f'\n{me} join chat\n')
                    else:
                        await client.put('\nError: The "login" command has one argument\n')
                elif command == 'say':
                    if login:
                        if message is not None:
                            message = message.split(' ', maxsplit=1)

                            if len(message) == 1:
                                await client.put('\nError: The "say" command has two argument\n')
                            else:
                                cow, message = message

                                if cow not in clients.keys():
                                    await client.put(f'\nError: No user with name {cow}\n')
                                else:
                                    if cow == me:
                                        await client.put("\nError: You can't send messages to yourself\n")
                                    else:
                                        await clients[cow].put(f'\n{str(datetime.datetime.now()).split(".")[0]} {me}:\n{cowsay.cowsay(message, cow=me)}\n')
                        else:
                            await client.put('\nError: The "say" command has two argument\n')
                    else:
                        await client.put('\nError: You has not registered yet\n')
                elif command == 'yield':
                    if login:
                        if message is not None:
                            for out in clients.values():
                            	await out.put(f'\n{str(datetime.datetime.now()).split(".")[0]} {me}:\n{cowsay.cowsay(message, cow=me)}\n')
                        else:
                            await client.put('\nError: The "yield" command has one argument\n')
                    else:
                        await client.put('\nError: You has not registered yet\n')
                else:
                    await client.put('\nError: This command is not supported\n')

            elif q is receive:
                receive = asyncio.create_task(client.get())
                if q.result() == '\nYou quit chat\n':
                    quit_flag = False
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    send.cancel()
    receive.cancel()
    print(f'User {me} quit')
    if me not in clients.keys():
        del unregister_clients[me]
    else:
        del clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(cowsay_chat, '0.0.0.0', 8080)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
