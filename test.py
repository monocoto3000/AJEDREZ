from maquina_ajedrez import MaquinaTuring

def main():
    maquina = MaquinaTuring('MT.xml')

    while True:
        cadena = input("Introduce la cadena (o 'exit' para terminar): ")
        if cadena.lower() == 'exit':
            break
        resultado = maquina.validarCadena(cadena)
        print("Resultado:", resultado)

if __name__ == "__main__":
    main()
