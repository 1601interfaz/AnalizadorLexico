from app import tokenize

def parse(tokens):
    """
    Analizador sintáctico para una ecuación química.
    """
    if len(tokens) < 3 or tokens[1][0] != "FLECHA":
        raise SyntaxError("Error de sintaxis: formato de ecuación incorrecto")
    for token in tokens:
        if token[0] == "INVALIDO":
            raise SyntaxError(f"Error de sintaxis: símbolo no válido '{token[1]}'")
        elif token[0] == "ELEMENTO_INVALIDO":
            raise SyntaxError(f"Error de sintaxis: elemento no válido '{token[1]}'")

    def main():
        ecuacion = input("Ingresa una ecuación química: ")
        try:
            tokens = tokenize(ecuacion)
            parse(tokens)
            print("La ecuación es sintácticamente correcta.")
        except ValueError as e:
            print(f"Error: {e}")
        except SyntaxError as e:
            print(f"Error: {e}")

    if __name__ == "__main__":
        main()

