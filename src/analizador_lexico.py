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
    #  IdentificadorPalabraReservada — AUTÓMATA
    #
    #  Estados:
    #  q0 → INICIO: espera letra o guion bajo
    #  q1 → LEYENDO: acumula letras, dígitos o guion bajo
    #  q2 → ACEPTAR: carácter no válido → fin del lexema
    #
    #  q0 --[letra|_]--> q1
    #  q1 --[letra|dígito|_]--> q1
    #  q1 --[otro]--> q2 (ACEPTAR)
    # ──────────────────────────────────────────────────────────
    def IdentificadorPalabraReservada(self, Archivo: str):
        UL     = UnidadesLexicas()
        Lexema = ""
        estado = 0  # q0 — Estado inicial

        while self.cont < len(Archivo):
            c = Archivo[self.cont]

            if estado == 0:
                # q0: solo acepta letra o guion bajo para iniciar
                if c.isalpha() or c == '_':
                    Lexema += c
                    self.cont += 1
                    estado = 1  # transición → q1
                else:
                    estado = 2  # transición → q2

            elif estado == 1:
                # q1: sigue leyendo letras, dígitos o guion bajo
                if c.isalpha() or c.isdigit() or c == '_':
                    Lexema += c
                    self.cont += 1
                    estado = 1  # se mantiene en q1
                else:
                    estado = 2  # transición → q2

            elif estado == 2:
                # q2: estado de aceptación — lexema completo
                break

        if Lexema:
            token = UL.GetTokenPalabra(Lexema)
            self.Lista.append(self._formato(self.Linea, Lexema, token))

    # ──────────────────────────────────────────────────────────
    #  EnteroReal — AUTÓMATA
    #
    #  Estados:
    #  q0 → INICIO: espera un dígito
    #  q1 → ENTERO: leyendo dígitos enteros
    #  q2 → PUNTO: encontró un punto decimal
    #  q3 → REAL: leyendo dígitos decimales
    #  q4 → ACEPTAR: carácter no válido → fin del lexema
    #
    #  q0 --[dígito]--> q1
    #  q1 --[dígito]--> q1
    #  q1 --[punto]--> q2
    #  q1 --[otro]--> q4 (ACEPTAR como entero)
    #  q2 --[dígito]--> q3
    #  q3 --[dígito]--> q3
    #  q3 --[otro]--> q4 (ACEPTAR como real)
    # ──────────────────────────────────────────────────────────
    def EnteroReal(self, Archivo: str):
        Lexema = ""
        estado = 0  # q0 — Estado inicial

        while self.cont < len(Archivo):
            c = Archivo[self.cont]

            if estado == 0:
                # q0: espera el primer dígito
                if c.isdigit():
                    Lexema += c
                    self.cont += 1
                    estado = 1  # transición → q1 Entero
                else:
                    estado = 4  # transición → q4 Aceptar

            elif estado == 1:
                # q1: leyendo entero
                if c.isdigit():
                    Lexema += c
                    self.cont += 1
                    estado = 1  # se mantiene en q1
                elif c == '.':
                    Lexema += c
                    self.cont += 1
                    estado = 2  # transición → q2 Punto
                else:
                    estado = 4  # transición → q4 Aceptar como entero

            elif estado == 2:
                # q2: encontró punto, espera dígito decimal
                if c.isdigit():
                    Lexema += c
                    self.cont += 1
                    estado = 3  # transición → q3 Real
                else:
                    estado = 4  # transición → q4 Aceptar

            elif estado == 3:
                # q3: leyendo parte decimal
                if c.isdigit():
                    Lexema += c
                    self.cont += 1
                    estado = 3  # se mantiene en q3
                else:
                    estado = 4  # transición → q4 Aceptar como real

            elif estado == 4:
                # q4: estado de aceptación — número completo
                break

        if Lexema:
            # q1 o q2 → entero | q3 → real
            if estado == 4 and '.' in Lexema:
                token = 201  # Número real
            else:
                token = 200  # Número entero
            self.Lista.append(self._formato(self.Linea, Lexema, token))

    # ──────────────────────────────────────────────────────────
    #  AutomataComentario — AUTÓMATA
    #
    #  Estados:
    #  q0 → INICIO: lee la primera diagonal /
    #  q1 → DIAGONAL: encontró /, decide qué tipo es
    #  q2 → LINEA: comentario de una línea (//)
    #  q3 → BLOQUE: comentario de bloque (/*)
    #  q4 → CIERRE: encontró * dentro de bloque
    #  q5 → ACEPTAR: comentario terminado
    #  q6 → DIVISION: era solo el símbolo /
    #
    #  q0 --[/]--> q1
    #  q1 --[/]--> q2 (comentario línea)
    #  q1 --[*]--> q3 (comentario bloque)
    #  q1 --[otro]--> q6 (es división)
    #  q2 --[\n]--> q5 (ACEPTAR)
    #  q2 --[otro]--> q2
    #  q3 --[*]--> q4
    #  q3 --[otro]--> q3
    #  q4 --[/]--> q5 (ACEPTAR)
    #  q4 --[otro]--> q3
    # ──────────────────────────────────────────────────────────
    def AutomataComentario(self, Archivo: str):
        UL     = UnidadesLexicas()
        estado = 0  # q0 — Estado inicial

        while self.cont < len(Archivo):
            c = Archivo[self.cont]

            if estado == 0:
                # q0: lee la primera diagonal
                if c == '/':
                    self.cont += 1
                    estado = 1  # transición → q1
                else:
                    estado = 6  # transición → q6

            elif estado == 1:
                # q1: decide qué tipo de comentario es
                if c == '/':
                    self.cont += 1
                    estado = 2  # transición → q2 Comentario línea
                elif c == '*':
                    self.cont += 1
                    estado = 3  # transición → q3 Comentario bloque
                else:
                    estado = 6  # transición → q6 Es división

            elif estado == 2:
                # q2: comentario de línea — ignora hasta \n
                if c == '\n':
                    estado = 5  # transición → q5 Aceptar
                else:
                    self.cont += 1
                    estado = 2  # se mantiene en q2

            elif estado == 3:
                # q3: dentro de comentario bloque
                if c == '*':
                    self.cont += 1
                    estado = 4  # transición → q4 posible cierre
                elif c == '\n':
                    self.Linea += 1
                    self.cont += 1
                    estado = 3  # se mantiene en q3
                else:
                    self.cont += 1
                    estado = 3  # se mantiene en q3

            elif estado == 4:
                # q4: encontró *, espera /
                if c == '/':
                    self.cont += 1
                    estado = 5  # transición → q5 Aceptar
                else:
                    estado = 3  # transición → q3 no era cierre

            elif estado == 5:
                # q5: estado de aceptación — comentario terminado
                break

            elif estado == 6:
                # q6: era solo el símbolo de división
                token = UL.GetTokenSimbolo('/')
                self.Lista.append(self._formato(self.Linea, '/', token))
                break

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