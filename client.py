import asyncio
import random
import math

#functie care calculeaza valorile conform formulei
def calculate_value(x):
    return abs(math.sin(x)) * math.exp(-math.sin(x))
    
async def tcp_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    #determinam pasul de crestere pentru x pentru a acoperi intervalul
    x = -math.pi 
    step = (8 * math.pi - (-math.pi)) / 50

    for i in range(50):
        value = calculate_value(x)

        #introducem anomaliile la iteratiile 15,30 si 45 cu o valoare aleatorie intre 1 si 3
        if i in [15, 30, 45]:
            value += random.uniform(1, 3)

        print (f"Sending value: {value }")
        writer.write(f"{value}\n".encode())
        await writer.drain()

        #asteptam o secunda inainte de a calcula urmatoarea valoare 
        await asyncio.sleep(1)
        x += step

    print("Closing the connection")
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_client())

