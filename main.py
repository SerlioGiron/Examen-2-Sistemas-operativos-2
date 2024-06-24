import random
import string
import threading

memoria = 800
capacidad_cache = memoria // 8
cache = []

class MyClass:
    def __init__(self, id, contenido):
        self.id = id
        self.contenido = contenido

def print_cache():
    for objeto in cache:
        print(f"[{objeto.id} {objeto.contenido}]", end="")
    print("")
        

def buscar_o_cargar_en_cache(cont, identificacion):
    for _ in range(cont):
        id_aleatorio = random.randint(0, memoria - 1)  # Genera un número aleatorio en el rango deseado
        for objeto in cache:
            if objeto.id == id_aleatorio:
                print(f"Thread {identificacion} match de caché: {objeto.contenido}")
                # print_cache()
                break
        # Si no se encuentra en cache, buscar en el archivo
        with open("disco.txt", "r") as file:
            for line in file:
                id_archivo, contenido_archivo = line.split(maxsplit=1)
                if int(id_archivo) == id_aleatorio:
                    # Crear un nuevo objeto MyClass y añadirlo al cache
                    nuevo_objeto = MyClass(id_aleatorio, contenido_archivo.strip())
                    if len(cache) >= capacidad_cache:
                        cache.pop(0)  # Elimina el primer elemento si el cache está lleno
                    cache.append(nuevo_objeto)
                    break
        # print_cache()

def fill_file():
    with open("disco.txt", "w") as file:
        for i in range(memoria):
            line = f"{i} {generate_string()}\n"
            file.write(line)

def generate_string():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(3))

fill_file()

def main():
    # print("Hello, world!")
    fill_file()
    consumir = input("paginas a consumir: ")
    print("cache capacity: ", capacidad_cache, end="\n\n")
    
    thread1 = threading.Thread(target=buscar_o_cargar_en_cache, args=(int(consumir),1))
    thread2 = threading.Thread(target=buscar_o_cargar_en_cache, args=(int(consumir),2))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()