

import re  # Libreria para trabajar con expresiones regulares

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
    ("NUMBER", r"\d+"),  # Números (para subíndices)
    ("ESPACIO", r"\s+"),  # Espacios en blanco
    ("INVALIDO", r"[.,_;:{}\[\]\'\"!#$%&/()¿¡?]")
]


# Funcion
def get_element_info(simbolo, atomos=1):
    """
    :param simbolo:
    :param moleculas:
    :return: Diccionario con informacion del elemento:
                *nombre: Nombre completo (value)
                *atomos: Número de moleculas del elemento (por defecto 1)
                *simbolo: Simbolo del elemento (Key)
    """
    if simbolo in ELEMENTOS:
        return {
            "nombre": ELEMENTOS[simbolo],
            "atomos": atomos,
            "simbolo": simbolo
        }
    else:
        raise ValueError(f"Simbolo de elemento inválido: {simbolo}")  # Manejo de errores


def tokenize(ecuacion):
    """
    Tokeniza la ecuación química en elementos y sus cantidades.

    :param ecuacion: La ecuación química a tokenizar.
    :return: Lista de tuplas (tipo, token) donde tipo es "ELEMENTO" o "NUMERO".
    """

    #Es un partron que identifica los elementos y sus cantidades
    pattern = re.compile(r'([A-Z][a-z]?)(\d*)')
    tokens = []

    #Itera sobre lo que encontro en el patron
    for match in pattern.finditer(ecuacion):
        elemento = match.group(1) #Captura el simbolo del elemento
        cantidad = match.group(2) #Captura el numero asociado
        tokens.append(("ELEMENTO", elemento))
        if cantidad:
            tokens.append(("NUMERO", int(cantidad)))
        else:
            tokens.append(("NUMERO", 1))
    return tokens


def main():
    ecuacion = input("Ingresa una ecuación química: ")
    try:
        tokens = tokenize(ecuacion)
        i = 0
        while i < len(tokens):
            if tokens[i][0] == "ELEMENTO":
                elemento = tokens[i][1]
                cantidad = tokens[i + 1][1] if i + 1 < len(tokens) and tokens[i + 1][0] == "NUMERO" else 1
                element_info = get_element_info(elemento, cantidad)
                print(f"Elemento: {element_info['nombre']}")
                print(f"Cantidad de átomos: {element_info['atomos']}")
                print(f"Simbolo: {element_info['simbolo']}")
                print("-" * 5)
                i += 2
            else:
                i += 1
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
    