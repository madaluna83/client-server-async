import asyncio 

#clasa pentru generarea serverului si detectarea anomaliilor
class AnomalyServer:
    def __init__(self):
        #in base_values vom stoca primele 10valori pentru a calcula media de referinta
        self.base_values = []
        #pragul pentru a detecta o anomalie conform chatGPT =))
        self.threshold = 0.5  

    async def handle_client(self, reader, writer):
        print("Client connected")
        while True:
            #citim datele primite d ela client 
            data = await reader.read(100)
            if not data:
                break
            try:
                value = float(data.decode())
            except ValueError:
                print("Invalid data received")
                continue

            print(f"Received value: {value}")

            #stocam primele 10 valori in vector 
            if len(self.base_values) < 10:
                self.base_values.append(value)
                print("Base values: ", self.base_values)
            else:
                #calculam media celor 10 val si verificam anomaliile pentru urmatoarele valori 
                mean_base = sum(self.base_values) / len(self.base_values)
                deviation = abs(value - mean_base)

                #daca valoarea depaseste pragul este considerata anomalie
                if deviation > self.threshold:
                    print(f"Anomally detected: {value} (deviation: {deviation})")
                else:
                    print(f"Value within normal range")   

        writer.close()
        await writer.wait_closed()
        print("Client disconnected")

    async def main(self):
        server = await asyncio.start_server(self.handle_client, '127.0.0.1', 8888)
        async with server: 
            await server.serve_forever()

anomaly_server = AnomalyServer()
asyncio.run(anomaly_server.main())