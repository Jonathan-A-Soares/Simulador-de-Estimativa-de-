#include <iostream>
#include <cmath>
#include <cstdlib>

class PixelArtApp {
public:
    PixelArtApp() {
        Pos_Text_y = 40;
        geracao = 200000; // Coloque o número desejado de gerações aqui
        acertos = 0;
        erros = 0;
        total_gen = erros + acertos;
        aaa = 0;
    }

    void draw_next_pixel() {
        while (geracao > 0) {
            geracao--;

            Ram_x = rand() % 201 + 150; // Random number between 150 and 350
            Ram_y = rand() % 201 + 150; // Random number between 150 and 350

            Acerto_circulo();

            Pos_Text_y += 10;

            total_gen = erros + acertos;
            aaa = 4 * static_cast<double>(acertos) / total_gen;

            std::cout << "Pi calculado: " << aaa << std::endl;
        }
        std::cout << "Total gen: " << total_gen << std::endl;
    }

    void Acerto_circulo() {
        double Dx = Pos_cir_x - Ram_x;
        double Dy = Pos_cir_y - Ram_y;
        double Dab = std::sqrt(std::pow(Dx, 2) + std::pow(Dy, 2));

        if (Dab <= R_cir) {
            acertos++;
        } else {
            erros++;
        }
    }

private:
    int Pos_Text_y;
    int geracao;
    int acertos;
    int erros;
    int total_gen;
    double aaa;
    int Pos_cir_x = 250;
    int Pos_cir_y = 250;
    int R_cir = 100;
    int Ram_x;
    int Ram_y;
};

int main() {
    PixelArtApp app;
    app.draw_next_pixel();

    return 0;
}
