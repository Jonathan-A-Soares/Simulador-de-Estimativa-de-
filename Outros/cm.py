import threading
import random
import math
import gc
import time
import json

Pos_cir_x = 250
Pos_cir_y = 250
R_cir = 0.00005  # Reduzindo o raio do círculo em 3x
pi_real = 3.14159265358979323846  # Valor conhecido de pi

class PixelArtApp:
    def __init__(self):
        self.Pos_Text_y = 40
        self.geracao = 5000
        self.acertos = 0
        self.erros = 0
        self.total_gen = 0
        self.aaa = 0
        self.points = []  # Lista para armazenar os pontos gerados
        self.lock = threading.Lock()

    def draw_next_pixel(self):
        while self.geracao > 0:
            self.geracao -= 1

            # Ajustando o intervalo para o quadrado reduzido
            self.Ram_x = random.uniform(Pos_cir_x - R_cir, Pos_cir_x + R_cir)
            self.Ram_y = random.uniform(Pos_cir_y - R_cir, Pos_cir_y + R_cir)

            self.Acerto_circulo()

            with self.lock:
                self.Pos_Text_y += 10

            gc.collect()
            self.total_gen = self.erros + self.acertos
            self.aaa = 4 * (self.acertos / self.total_gen) if self.total_gen > 0 else 0

            # Verificar se o valor calculado de pi é próximo ao valor real
            #if round(self.aaa, 8) == round(pi_real, 8):
              #  break

    def Acerto_circulo(self):
        Dx = Pos_cir_x - self.Ram_x
        Dy = Pos_cir_y - self.Ram_y
        Dab = math.sqrt(math.pow(Dx, 2) + math.pow(Dy, 2))

        status = 'acerto' if Dab <= R_cir else 'erro'

        with self.lock:
            ponto = {'x': self.Ram_x, 'y': self.Ram_y, 'status': status}
            self.points.append(ponto)

            if status == 'acerto':
                self.acertos += 1
            else:
                self.erros += 1

# Função para executar a aplicação em uma thread
def run_app(thread_id, results):
    app = PixelArtApp()
    start_time = time.time()
    app.draw_next_pixel()
    elapsed_time = time.time() - start_time

    results[thread_id] = {'acertos': app.acertos, 'erros': app.erros, 'tempo': elapsed_time, 'points': app.points}

if __name__ == "__main__":
    threads = []
    results = {}

    start_time_total = time.time()

    for i in range(10):
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

    # Exporta os resultados para um arquivo JSON
    with open('resultados.json', 'w') as json_file:
        json.dump(results, json_file, indent=2)

    print("Resultados exportados para 'resultados.json'")
