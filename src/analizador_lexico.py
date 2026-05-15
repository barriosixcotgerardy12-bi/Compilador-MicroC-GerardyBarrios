"""
Clase: AnalizadorLexico
Uso: Define las propiedades y funcionalidades del analizador léxico
para el compilador MicroC
Curso: Autómatas y Lenguajes - Universidad Mesoamericana 2026
"""

from unidades_lexicas import UnidadesLexicas


class AnalizadorLexico:

    def __init__(self):
        self.Lista = []   # Lista de tokens encontrados
        self.cont  = 0    # Contador de posición en el archivo
        self.Linea = 1    # Contador de líneas

    # ──────────────────────────────────────────────────────────
    #  _formato
    #  Genera una línea con columnas alineadas
    # ──────────────────────────────────────────────────────────
    def _formato(self, linea: int, lexema: str, token) -> str:
        col_linea  = f"Linea: {linea}".ljust(12)
        col_lexema = f"Lexema: {lexema}".ljust(22)
        col_token  = f"Token: {token}"
        return f"{col_linea}  {col_lexema}  {col_token}"

    # ──────────────────────────────────────────────────────────
    #  GetAlfabetoAlfanumerico
    #  Retorna 1 si el carácter es letra o guion bajo, 0 si no
    # ──────────────────────────────────────────────────────────
    def GetAlfabetoAlfanumerico(self, c: str) -> int:
        if c.isalpha() or c == '_':
            return 1
        return 0

    # ──────────────────────────────────────────────────────────
    #  GetAlfabetoNumero
    #  Retorna 1 si el carácter es dígito, punto, +, -, 0 si no
    # ──────────────────────────────────────────────────────────
    def GetAlfabetoNumero(self, c: str) -> int:
        if c.isdigit() or c in '.+-':
            return 1
        return 0

    # ──────────────────────────────────────────────────────────
    #  GetAlfabetoSimbolo
    #  Retorna 1 si el carácter es un símbolo válido, 0 si no
    # ──────────────────────────────────────────────────────────
    def GetAlfabetoSimbolo(self, c: str) -> int:
        simbolos = '(){}[];,.<>!&|=+-*/%^~#"\':'
        if c in simbolos:
            return 1
        return 0

    # ──────────────────────────────────────────────────────────
    #  IdentificadorPalabraReservada
    #  Lee letras/guiones seguidos y forma un lexema
    #  Luego busca si es palabra reservada o identificador
    # ──────────────────────────────────────────────────────────
    def IdentificadorPalabraReservada(self, Archivo: str):
        UL = UnidadesLexicas()
        Lexema = ""

        while self.cont < len(Archivo):
            c = Archivo[self.cont]
            if c.isalpha() or c.isdigit() or c == '_':
                Lexema += c
                self.cont += 1
            else:
                break

        token = UL.GetTokenPalabra(Lexema)
        self.Lista.append(self._formato(self.Linea, Lexema, token))

    # ──────────────────────────────────────────────────────────
    #  EnteroReal
    #  Lee dígitos y puntos para formar números enteros o reales
    # ──────────────────────────────────────────────────────────
    def EnteroReal(self, Archivo: str):
        Lexema = ""
        tiene_punto = False

        while self.cont < len(Archivo):
            c = Archivo[self.cont]
            if c.isdigit():
                Lexema += c
                self.cont += 1
            elif c == '.' and not tiene_punto:
                Lexema += c
                tiene_punto = True
                self.cont += 1
            else:
                break

        if Lexema:
            if tiene_punto:
                token = 201  # Token para número real
            else:
                token = 200  # Token para número entero
            self.Lista.append(self._formato(self.Linea, Lexema, token))

    # ──────────────────────────────────────────────────────────
    #  AutomataComentario
    #  Maneja comentarios de una línea (//) y multilínea (/* */)
    # ──────────────────────────────────────────────────────────
    def AutomataComentario(self, Archivo: str):
        # Verificar si es // o /*
        if self.cont + 1 < len(Archivo):
            siguiente = Archivo[self.cont + 1]

            if siguiente == '/':
                # Comentario de una línea — ignorar hasta fin de línea
                while self.cont < len(Archivo) and Archivo[self.cont] != '\n':
                    self.cont += 1

            elif siguiente == '*':
                # Comentario multilínea — ignorar hasta */
                self.cont += 2  # Saltar /*
                while self.cont < len(Archivo) - 1:
                    if Archivo[self.cont] == '*' and Archivo[self.cont + 1] == '/':
                        self.cont += 2  # Saltar */
                        break
                    if Archivo[self.cont] == '\n':
                        self.Linea += 1
                    self.cont += 1
            else:
                # Es solo el símbolo /
                UL = UnidadesLexicas()
                token = UL.GetTokenSimbolo('/')
                self.Lista.append(self._formato(self.Linea, '/', token))
                self.cont += 1
        else:
            self.cont += 1

    # ──────────────────────────────────────────────────────────
    #  AnalisisLexico
    #  Función principal — recorre el archivo carácter por carácter
    #  y genera la lista completa de tokens
    # ──────────────────────────────────────────────────────────
    def AnalisisLexico(self, Archivo: str) -> list:
        UL     = UnidadesLexicas()
        self.Lista  = []
        self.cont   = 0
        self.Linea  = 1

        while self.cont < len(Archivo):
            c = Archivo[self.cont]

            # ── Salto de línea ─────────────────────────────────
            if c == '\n':
                self.Linea += 1
                self.cont  += 1

            # ── Espacios, tabuladores, caracteres nulos ────────
            elif c in ' \t\r\x00':
                self.cont += 1

            # ── Letra o guion bajo → palabra reservada/identificador
            elif self.GetAlfabetoAlfanumerico(c):
                self.IdentificadorPalabraReservada(Archivo)

            # ── Dígito → número entero o real ─────────────────
            elif c.isdigit():
                self.EnteroReal(Archivo)

            # ── Diagonal → puede ser comentario o división ─────
            elif c == '/':
                self.AutomataComentario(Archivo)

            # ── Símbolo ────────────────────────────────────────
            elif self.GetAlfabetoSimbolo(c):
                Lexema = c
                self.cont += 1

                # Verificar símbolo doble (==, !=, <=, >=, ++, --, &&, ||, <<, >>)
                if self.cont < len(Archivo):
                    doble = Lexema + Archivo[self.cont]
                    token_doble = UL.GetTokenSimbolo(doble)
                    if token_doble != -1:
                        Lexema = doble
                        self.cont += 1
                        self.Lista.append(self._formato(self.Linea, Lexema, token_doble))
                        continue

                # Símbolo simple
                token = UL.GetTokenSimbolo(Lexema)
                if token != -1:
                    self.Lista.append(self._formato(self.Linea, Lexema, token))
                else:
                    self.Lista.append(self._formato(self.Linea, Lexema, "Símbolo no encontrado"))

            # ── Carácter no reconocido ─────────────────────────
            else:
                self.cont += 1

        return self.Lista