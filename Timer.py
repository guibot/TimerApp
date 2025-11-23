import time
import playsound

def tocar_som():
    """Reproduz um arquivo WAV usando playsound."""
    playsound.playsound('/Users/g/Documents/G/_PROJECTS/PYTHON/Timer/timer2.wav', True)

def definir_timer(tempo_em_minutos):
    """
    Cria um timer que, ao atingir o tempo especificado, toca um som.
    """
    try:
        tempo_em_segundos = float(tempo_em_minutos) * 60  # Convertendo minutos para segundos
        if tempo_em_segundos <= 0:
            print("O tempo deve ser maior que 0.")
            return

        print(f"Timer definido para {tempo_em_minutos} minutos ({tempo_em_segundos} segundos)...")
        time.sleep(tempo_em_segundos)
        tocar_som()

    except ValueError:
        print("Entrada inválida. Por favor, insira um número inteiro para o tempo.")

if __name__ == "__main__":
    while True:
        try:
            tempo = input("Digite o tempo em minutos (ou 'sair' para encerrar): ")
            if tempo.lower() == 'sair':
                break
            definir_timer(tempo)
        except KeyboardInterrupt:
            print("\nTimer interrompido.")
            break
