import tkinter as tk
from queue import Queue
import random
import math
import threading
import signal
import sys

Pos_cir_x = 250
Pos_cir_y = 250
R_cir = 100
pi_real = 3.14159265358979323846  # Valor conhecido de pi

class PixelArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pi ?")
        self.root.geometry("750x540+1500+50")
        self.canvas = tk.Canvas(root, width=750, height=540, bg="white")
        self.canvas.pack(expand=tk.NO, fill=tk.BOTH)
        self.canvas.create_rectangle(50, 50, 450, 450, outline="black")

        self.draw_circle(Pos_cir_x, Pos_cir_y, R_cir, "black")
        self.draw_circle(Pos_cir_x, Pos_cir_y, R_cir - 2, "white")
        self.Pos_Text_y = 40
        self.geracao = 00  # Ajuste o número de gerações conforme necessário
        self.acertos = 0
        self.erros = 0
        self.total_gen = self.erros + self.acertos
        self.aaa = 0
        self.draw_text(640, 50, "Acertos: " + str(self.acertos), font_size=10, color="black", tag="acert")
        self.draw_text(640, 70, "Erros: " + str(self.erros), font_size=10, color="black", tag="err")
        self.draw_text(640, 90, "Total gen: " + str(self.total_gen), font_size=10, color="black", tag="total")
        self.draw_text(150, 400, "Pi calculado: " + str(self.aaa), font_size=10, color="black", tag="pi_calc")
        self.draw_text(150, 500, "Pi ≈ 4 * (pontos acertos no círculo / quantidade pontos no quadrado)", font_size=10, color="black")
        self.draw_text(150, 480, "Pi = 3.14159265358979323846", font_size=10, color="black")  # 3,14159265358979323846
        self.entry = tk.Entry(root, width=10, bd=2)
        self.entry.pack(pady=10)
        self.entry.insert(0, str(self.geracao))
        self.entry.place(x=640, y=220)

        btn_clear = tk.Button(root, text="Zerar", command=lambda: self.clear_result())
        btn_clear.place(x=640, y=150)
        btn_Gerar = tk.Button(root, text="Gerar Novo", command=lambda: self.regen())
        btn_Gerar.place(x=640, y=180)

        self.pixel_queue = Queue()
        self.exit_flag = False
        self.num_threads = 4  # Ajuste o número de threads conforme necessário
        self.pixel_threads = []

        # Configurar sinal SIGINT para interrupção com Ctrl+C
        signal.signal(signal.SIGINT, self.handle_signal)

        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.generate_pixels)
            thread.start()
            self.pixel_threads.append(thread)

        self.root.after(0, self.draw_next_pixel)

    def handle_signal(self, signum, frame):
        # Função para lidar com o sinal SIGINT (Ctrl+C)
        print("Sinal de interrupção recebido. Encerrando o programa.")
        self.exit_flag = True
        self.root.destroy()

    def generate_pixels(self):
        while not self.exit_flag:
            action = self.pixel_queue.get()
            if action == "generate_pixel" and self.geracao > 0:
                self.geracao -= 1

                Ram_x = random.randint(150, 350)
                Ram_y = random.randint(150, 350)

                self.Acerto_circulo(Ram_x, Ram_y)

                self.Pos_Text_y += 10

                self.delete('acert')
                self.delete('err')
                self.delete('total')
                self.delete('pi_calc')

                self.draw_text(640, 50, "Acertos: " + str(self.acertos), font_size=10, color="black", tag="acert")
                self.draw_text(640, 70, "Erros: " + str(self.erros), font_size=10, color="black", tag="err")

                self.total_gen = self.erros + self.acertos
                self.root.after(0, self.draw_next_pixel)
                if round(self.aaa, 4) == round(pi_real, 4):
                    self.geracao -= self.geracao

                # Atualizar total de gerações e valor de pi calculado em tempo real
                self.draw_text(640, 90, "Total gen: " + str(self.total_gen), font_size=10, color="black", tag="total")
                self.aaa = 4 * (self.acertos / self.total_gen)
                self.draw_text(150, 400, "Pi calculado: " + str(self.aaa), font_size=10, color="black", tag="pi_calc")
                print("Pi calculado: " + str(self.aaa))

    def draw_next_pixel(self):
        self.pixel_queue.put("generate_pixel")

    def draw_pixel(self, x, y, color, tag=None):
        pixel_size = 5  # Tamanho do pixel
        x1, y1 = x - pixel_size // 2, y - pixel_size // 2
        x2, y2 = x + pixel_size // 2, y + pixel_size // 2
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color, tags=tag)

    def draw_circle(self, x, y, radius, color):
        x1, y1 = x - radius, y - radius
        x2, y2 = x + radius, y + radius
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    def draw_text(self, x, y, text, font_size=12, color="black", tag=None):
        text_item = self.canvas.create_text(x, y, text=text, font=("Helvetica", font_size), fill=color, tags=tag,
                                            anchor="nw")
        return text_item

    def delete(self, a):
        self.canvas.delete(a)

    def Acerto_circulo(self, Ram_x, Ram_y):
        Dx = Pos_cir_x - Ram_x
        Dy = Pos_cir_y - Ram_y
        Dab = math.sqrt(math.pow(Dx, 2) + math.pow(Dy, 2))

        if Dab <= R_cir:
            self.acertos += 1
            self.draw_pixel(Ram_x, Ram_y, "green", tag="ponto")
            self.draw_text(560, self.Pos_Text_y, "X: " + str(Ram_x) + " " + " Y: " + str(Ram_y),
                           font_size=8, color="green", tag="pos")
        else:
            self.draw_pixel(Ram_x, Ram_y, "red", tag="ponto")
            self.draw_text(560, self.Pos_Text_y, "X: " + str(Ram_x) + " " + " Y: " + str(Ram_y),
                           font_size=8, color="red", tag="pos")
            self.erros += 1

    def clear_result(self):
        self.delete('ponto')
        self.delete('pos')
        self.delete('err')
        self.delete('acert')
        self.delete('total')
        self.acertos = 0
        self.erros = 0
        self.Pos_Text_y = 40
        self.geracao = 1000  # Ajuste o número de gerações conforme necessário
        self.draw_text(640, 50, "Acertos: " + str(self.acertos), font_size=10, color="black", tag="acert")
        self.draw_text(640, 70, "Erros: " + str(self.erros), font_size=10, color="black", tag="err")
        self.draw_text(640, 90, "Total gen: " + str(self.total_gen), font_size=10, color="black", tag="total")

    def regen(self):
        self.geracao = int(self.entry.get())
        self.root.after(0, self.draw_next_pixel)

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelArtApp(root)
    root.mainloop()
