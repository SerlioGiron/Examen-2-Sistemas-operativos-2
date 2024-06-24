import random
import threading

class CacheSimulator:
    def __init__(self, memory_size, cache_capacity):
        self.primary_memory = {i: random.randint(1, 100) for i in range(memory_size)}
        self.cache_storage = {}
        self.cache_capacity = cache_capacity
        self.cache_keys_order = []
        self.cache_position = 0
        self.lock = threading.Lock()


    def fetch_from_memory(self, address):
        with self.lock:
            if address in self.cache_storage:
                print(f"Cache hit: {self.cache_storage[address]} at address {address}")
                return self.cache_storage[address]
            else:
                data = self.primary_memory[address]
                self._refresh_cache(address, data)
                return data

    def _refresh_cache(self, address, data):
        if len(self.cache_keys_order) < self.cache_capacity:
            self.cache_keys_order.append(address)
        else:
            oldest_address = self.cache_keys_order[self.cache_position]
            del self.cache_storage[oldest_address]
            self.cache_keys_order[self.cache_position] = address
            self.cache_position = (self.cache_position + 1) % self.cache_capacity
        
        self.cache_storage[address] = data

    def simulate_memory_accesses(self, access_count):
        addresses = list(self.primary_memory.keys())
        for _ in range(access_count):
            address = random.choice(addresses)
            self.fetch_from_memory(address)
  

def execute_simulation(simulator, access_count):
    simulator.simulate_memory_accesses(access_count)

if __name__ == "__main__":
    memory_size = 1000
    cache_capacity = memory_size // 8
    accesses_per_thread = 100

    simulator = CacheSimulator(memory_size, cache_capacity)
    
    # Crear dos hilos para simular dos procesos consumidores
    thread1 = threading.Thread(target=execute_simulation, args=(simulator, accesses_per_thread))
    thread2 = threading.Thread(target=execute_simulation, args=(simulator, accesses_per_thread))

    # Iniciar los hilos
    thread1.start()
    thread2.start()

    # Esperar a que los hilos terminen
    thread1.join()
    thread2.join()
