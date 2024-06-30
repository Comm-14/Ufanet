import asyncio
import aiomqtt

# async def run(topic):
#     async def main(topic):
#         try:
#             # Cancel the listener task after 5 seconds
#             async with asyncio.timeout(10):
#                 async with aiomqtt.Client("localhost")as client:
#                     await client.subscribe(topic)
#                     async for message in client.messages:
#                         print(message.payload)
#         # Ignore the resulting TimeoutError
#         except asyncio.TimeoutError:
#             pass
#     # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     # asyncio.run(main(topic))  

async def listen(topic):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    async with aiomqtt.Client("localhost")as client:
        await client.subscribe(topic)
        async for message in client.messages:
            return(message.payload)


async def main(topic):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        # Cancel the listener task after 5 seconds
        async with asyncio.timeout(15):
            msg = await listen(topic)
            return msg
        

    # Ignore the resulting TimeoutError
    
    except asyncio.TimeoutError:
        
        pass
    # return False

topic = "mac1"
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main(topic))
