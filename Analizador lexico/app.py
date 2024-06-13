import re  # Librería para trabajar con expresiones regulares

ELEMENTOS = {
    # {clave, valor}     {key, value}
    "H": "Hidrógeno", "He": "Helio", "Li": "Litio", "Be": "Berilio", "B": "Boro", "C": "Carbono",
    "N": "Nitrógeno", "O": "Oxígeno", "F": "Flúor", "Ne": "Neón", "Na": "Sodio", "Mg": "Magnesio",
    "Al": "Aluminio", "Si": "Silicio", "P": "Fósforo", "S": "Azufre", "Cl": "Cloro", "Ar": "Argón",
    "K": "Potasio", "Ca": "Calcio", "Sc": "Escandio", "Ti": "Titanio", "V": "Vanadio", "Cr": "Cromo",
    "Mn": "Manganeso", "Fe": "Hierro", "Co": "Cobalto", "Ni": "Níquel", "Cu": "Cobre", "Zn": "Zinc",
    "Ga": "Galio", "Ge": "Germanio", "As": "Arsénico", "Se": "Selenio", "Br": "Bromo", "Kr": "Kriptón",
    "Rb": "Rubidio", "Sr": "Estroncio", "Y": "Itrio", "Zr": "Circonio", "Nb": "Niobio", "Mo": "Molibdeno",
    "Tc": "Tecnecio", "Ru": "Rutenio", "Rh": "Rodio", "Pd": "Paladio", "Ag": "Plata", "Cd": "Cadmio",
    "In": "Indio", "Sn": "Estaño", "Sb": "Antimonio", "Te": "Telurio", "I": "Yodo", "Xe": "Xenón",
    "Cs": "Cesio", "Ba": "Bario", "La": "Lantano", "Ce": "Cerio", "Pr": "Praseodimio", "Nd": "Neodimio",
    "Pm": "Prometio", "Sm": "Samario", "Eu": "Europio", "Gd": "Gadolinio", "Tb": "Terbio", "Dy": "Disprosio",
    "Ho": "Holmio", "Er": "Erbio", "Tm": "Tulio", "Yb": "Iterbio", "Lu": "Lutecio", "Hf": "Hafnio",
    "Ta": "Tántalo", "W": "Wolframio", "Re": "Renio", "Os": "Osmio", "Ir": "Iridio", "Pt": "Platino",
    "Au": "Oro", "Hg": "Mercurio", "Tl": "Talio", "Pb": "Plomo", "Bi": "Bismuto", "Po": "Polonio",
    "At": "Astato", "Rn": "Radón", "Fr": "Francio", "Ra": "Radio", "Ac": "Actinio", "Th": "Torio",
    "Pa": "Protactinio", "U": "Uranio", "Np": "Neptunio", "Pu": "Plutonio", "Am": "Americio", "Cm": "Curio",
    "Bk": "Berkelio", "Cf": "Californio", "Es": "Einstenio", "Fm": "Fermio", "Md": "Mendelevio",
    "No": "Nobelio", "Lr": "Lawrencio", "Rf": "Rutherfordio", "Db": "Dubnio", "Sg": "Seaborgio",
    "Bh": "Bohrio", "Hs": "Hassio", "Mt": "Meitnerio", "Ds": "Darmstadtio", "Rg": "Roentgenio",
    "Cn": "Copernicio", "Nh": "Nihonio", "Fl": "Flerovio", "Mc": "Moscovio", "Lv": "Livermorio",
    "Ts": "Tenesino", "Og": "Oganesón"
}

# Definimos los tipos de tokens que vamos a reconocer
TOKEN_TYPES = [
    ("ELEMENTOS", r"|".join(ELEMENTOS.keys())),  # Elementos químicos específicos
    ("COEFICIENTES", r"\b\d+\b"),  # Coeficientes estequiométricos
    ("MAS", r"\+"),  # Símbolo de suma
    ("FLECHA", r"->"),  # Flecha de reacción
    ("NUMERO", r"\d+"),  # Números (para subíndices)
    ("ESPACIO", r"\s+"),  # Espacios en blanco
    ("INVALIDO", r"[.,_;:{}\[\]\'\"!#$%&/()¿¡?]")  # Símbolos inválidos
]

def get_element_info(simbolo, atomos=1):
    """
    :param simbolo:
    :param moleculas:
    :return: Diccionario con información del elemento:
                *nombre: Nombre completo (value)
                *atomos: Número de moléculas del elemento (por defecto 1)
                *simbolo: Símbolo del elemento (Key)
    """
    if simbolo in ELEMENTOS:
        return {
            "nombre": ELEMENTOS[simbolo],
            "atomos": atomos,
            "simbolo": simbolo
        }
    else:
        raise ValueError(f"Símbolo de elemento inválido: {simbolo}")  # Manejo de errores

def tokenize(ecuacion):
    """
    Tokeniza la ecuación química en elementos, sus cantidades y coeficientes.

    :param ecuacion: La ecuación química a tokenizar.
    :return: Lista de tuplas (tipo, token) donde tipo es "ELEMENTO", "NUMERO", "COEFICIENTE" o "INVALIDO".
    """
    # Es un patrón que identifica los coeficientes, elementos, sus cantidades y símbolos inválidos
    pattern = re.compile(r'\b\d+\b|[A-Z][a-z]?\d*|[.,_;:{}\[\]\'\"!#$%&/()¿¡?]')
    tokens = []

    # Itera sobre lo que encontró en el patrón
    for match in pattern.finditer(ecuacion):
        token = match.group(0)
        if token.isdigit():
            tokens.append(("COEFICIENTE", int(token)))
        elif re.match(r'[A-Z][a-z]?', token):
            elemento = re.match(r'[A-Z][a-z]?', token).group(0)
            if elemento in ELEMENTOS:
                cantidad = re.findall(r'\d+', token)
                tokens.append(("ELEMENTO", elemento))
                if cantidad:
                    tokens.append(("NUMERO", int(cantidad[0])))
                else:
                    tokens.append(("NUMERO", 1))
            else:
                tokens.append(("ELEMENTO_INVALIDO", token))
        else:
            tokens.append(("INVALIDO", token))

    return tokens

def main():
    ecuacion = input("Ingresa una ecuación química: ")
    try:
        tokens = tokenize(ecuacion)
        i = 0
        while i < len(tokens):
            if tokens[i][0] == "COEFICIENTE":
                print(f"Coeficiente: {tokens[i][1]}")
                i += 1
            elif tokens[i][0] == "ELEMENTO":
                elemento = tokens[i][1]
                cantidad = tokens[i + 1][1] if i + 1 < len(tokens) and tokens[i + 1][0] == "NUMERO" else 1
                element_info = get_element_info(elemento, cantidad)
                print(f"Elemento: {element_info['nombre']}")
                print(f"Cantidad de átomos: {element_info['atomos']}")
                print(f"Símbolo: {element_info['simbolo']}")
                print("-" * 5)
                i += 2
            elif tokens[i][0] == "ELEMENTO_INVALIDO":
                print(f"Error: Elemento no encontrado: {tokens[i][1]}")
                i += 1
            elif tokens[i][0] == "INVALIDO":
                print(f"Error: Símbolo inválido encontrado: {tokens[i][1]}")
                i += 1
            else:
                i += 1
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
