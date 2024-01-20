import threading
import random
import math
import gc
import time

Pos_cir_x = 250
Pos_cir_y = 250
R_cir = 100

class PixelArtApp:
    def __init__(self):
        self.Pos_Text_y = 40
        self.geracao = 10000
        self.acertos = 0
        self.erros = 0
        self.total_gen = 0
        self.aaa = 0
        self.lock = threading.Lock()

    def draw_next_pixel(self):
        while self.geracao > 0:
            self.geracao -= 1

            self.Ram_x = random.randint(150, 350)
            self.Ram_y = random.randint(150, 350)

            self.Acerto_circulo()

            with self.lock:
                self.Pos_Text_y += 10

            gc.collect()
            self.total_gen = self.erros + self.acertos
            self.aaa = 4 * (self.acertos / self.total_gen) if self.total_gen > 0 else 0

    def Acerto_circulo(self):
        Dx = Pos_cir_x - self.Ram_x
        Dy = Pos_cir_y - self.Ram_y
        Dab = math.sqrt(math.pow(Dx, 2) + math.pow(Dy, 2))

        if Dab <= R_cir:
            with self.lock:
                self.acertos += 1
        else:
            with self.lock:
                self.erros += 1

def run_app(thread_id, results):
    app = PixelArtApp()
    start_time = time.time()
    app.draw_next_pixel()
    elapsed_time = time.time() - start_time

    results[thread_id] = {'acertos': app.acertos, 'erros': app.erros, 'tempo': elapsed_time}

if __name__ == "__main__":
    threads = []
    results = {}

    start_time_total = time.time()

    for i in range(20):
        thread = threading.Thread(target=run_app, args=(i, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_acertos = sum(result['acertos'] for result in results.values())
    total_erros = sum(result['erros'] for result in results.values())
    total_tempo = sum(result['tempo'] for result in results.values())

    total_gen = total_acertos + total_erros
    pi_calculado = 4 * (total_acertos / total_gen) if total_gen > 0 else 0

    elapsed_time_total = time.time() - start_time_total

    print(f"Total de acertos: {total_acertos}")
    print(f"Total de erros: {total_erros}")
    print(f"Pi calculado global: {pi_calculado}")
    print(f"Tempo total: {elapsed_time_total} segundos")
