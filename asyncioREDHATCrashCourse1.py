import asyncio
import random


async def say(word):
    wait_time = random.randint(0, 5)/2.0
    print('{} to sleep for{}'.format(word, wait_time))
    await asyncio.sleep(wait_time) #await aqui faz com que o python execute uma proxima tarefa enquanto "aguarda"
    print (word)

async def main():
    tasks = [say(word) for word in ("Let's", 'make', 'it', 'asynchronous')]

    await asyncio.gather(*tasks)

asyncio.run(main())