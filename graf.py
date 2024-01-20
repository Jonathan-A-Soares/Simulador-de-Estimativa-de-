import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ler os resultados do arquivo JSON
with open('resultados.json', 'r') as json_file:
    results = json.load(json_file)

# Extrair pontos e resultados globais
all_points = []
total_acertos = 0
total_erros = 0

for result in results.values():
    all_points.extend(result['points'])
    total_acertos += result['acertos']
    total_erros += result['erros']

# Extrair estatísticas globais
total_gen = total_acertos + total_erros
pi_calculado = 4 * (total_acertos / total_gen) if total_gen > 0 else 0

# Criar gráfico
fig, ax = plt.subplots()
ax.set_aspect('equal', 'box')
ax.set_xlim(100, 300)  # Ajuste para o quadrado reduzido
ax.set_ylim(100, 300)  # Ajuste para o quadrado reduzido

# Adicionar quadrado
square = patches.Rectangle((166.6, 166.6), 66.6, 66.6, linewidth=1, edgecolor='blue', facecolor='none')  # Ajuste para o quadrado reduzido
ax.add_patch(square)

# Adicionar círculo
circle = plt.Circle((200, 200), 100 / 3, color='blue', fill=False)  # Ajuste para o círculo reduzido
ax.add_patch(circle)

# Adicionar pontos centralizados
acertos_x = [point['x'] for point in all_points if point['status'] == 'acerto']
acertos_y = [point['y'] for point in all_points if point['status'] == 'acerto']
erros_x = [point['x'] for point in all_points if point['status'] == 'erro']
erros_y = [point['y'] for point in all_points if point['status'] == 'erro']

# Ajuste para centralizar os pontos
acertos_x_centered = [x - 50 for x in acertos_x]
acertos_y_centered = [y - 50 for y in acertos_y]
erros_x_centered = [x - 50 for x in erros_x]
erros_y_centered = [y - 50 for y in erros_y]

ax.scatter(acertos_x_centered, acertos_y_centered, color='green', marker='o', label='Acertos')
ax.scatter(erros_x_centered, erros_y_centered, color='red', marker='o', label='Erros')

# Adicionar estatísticas
stats_text = f"Pi Calculado ≈ {pi_calculado:.10f}\nAcertos: {total_acertos}\nErros: {total_erros}\nTotal: {total_gen}"
ax.text(310, 200, stats_text, fontsize=12, verticalalignment='center')

# Adicionar legenda
ax.legend()

plt.title("Pi = 4 * Quantidade de Pontos no circulo / Quantidade de Pontos no quadrado")

plt.xlabel("Coordenada X")
plt.ylabel("Coordenada Y")

plt.show()
