"""
Clase: UnidadesLexicas
Uso: Define las propiedades y funcionalidades de los objetos 
para el uso de la tabla de símbolos del lenguaje MicroC
Curso: Autómatas y Lenguajes - Universidad Mesoamericana 2026
"""
 
 
class UnidadesLexicas:
 
    def __init__(self):
        # Diccionario de palabras reservadas y sus tokens
        self.Palabra = {}
 
        # ── Palabras Reservadas del lenguaje C ─────────────────
        self.Palabra["auto"]     = 1
        self.Palabra["break"]    = 2
        self.Palabra["case"]     = 3
        self.Palabra["char"]     = 4
        self.Palabra["const"]    = 5
        self.Palabra["continue"] = 6
        self.Palabra["default"]  = 7
        self.Palabra["do"]       = 8
        self.Palabra["double"]   = 9
        self.Palabra["else"]     = 10
        self.Palabra["enum"]     = 11
        self.Palabra["extern"]   = 12
        self.Palabra["float"]    = 13
        self.Palabra["for"]      = 14
        self.Palabra["goto"]     = 15
        self.Palabra["if"]       = 16
        self.Palabra["int"]      = 17
        self.Palabra["long"]     = 18
        self.Palabra["register"] = 19
        self.Palabra["return"]   = 20
        self.Palabra["short"]    = 21
        self.Palabra["signed"]   = 22
        self.Palabra["sizeof"]   = 23
        self.Palabra["static"]   = 24
        self.Palabra["struct"]   = 25
        self.Palabra["switch"]   = 26
        self.Palabra["typedef"]  = 27
        self.Palabra["union"]    = 28
        self.Palabra["unsigned"] = 29
        self.Palabra["void"]     = 30
        self.Palabra["volatile"] = 31
        self.Palabra["while"]    = 32
 
        # ── Directivas del procesador ──────────────────────────
        self.Palabra["#include"] = 40
        self.Palabra["#define"]  = 41
        self.Palabra["#ifdef"]   = 42
        self.Palabra["#ifndef"]  = 43
        self.Palabra["#endif"]   = 44
        self.Palabra["#pragma"]  = 45
 
        # ── Funciones stdio.h ──────────────────────────────────
        self.Palabra["printf"]   = 50
        self.Palabra["scanf"]    = 51
        self.Palabra["fprintf"]  = 52
        self.Palabra["fscanf"]   = 53
        self.Palabra["fopen"]    = 54
        self.Palabra["fclose"]   = 55
        self.Palabra["fgets"]    = 56
        self.Palabra["fputs"]    = 57
        self.Palabra["feof"]     = 58
        self.Palabra["puts"]     = 59
        self.Palabra["gets"]     = 60
 
        # ── Funciones stdlib.h ─────────────────────────────────
        self.Palabra["malloc"]   = 61
        self.Palabra["free"]     = 62
        self.Palabra["exit"]     = 63
        self.Palabra["atoi"]     = 64
        self.Palabra["atof"]     = 65
        self.Palabra["rand"]     = 66
        self.Palabra["srand"]    = 67
 
        # ── Funciones string.h ─────────────────────────────────
        self.Palabra["strlen"]   = 68
        self.Palabra["strcpy"]   = 69
        self.Palabra["strcat"]   = 70
        self.Palabra["strcmp"]   = 71
        self.Palabra["strchr"]   = 72
 
        # ── Funciones math.h ───────────────────────────────────
        self.Palabra["sqrt"]     = 73
        self.Palabra["pow"]      = 74
        self.Palabra["abs"]      = 75
        self.Palabra["ceil"]     = 76
        self.Palabra["floor"]    = 77
 
        # ── Símbolos ───────────────────────────────────────────
        self.Simbolo = {}
 
        # Operadores Aritméticos
        self.Simbolo["+"]  = 80
        self.Simbolo["-"]  = 81
        self.Simbolo["*"]  = 82
        self.Simbolo["/"]  = 83
        self.Simbolo["%"]  = 84
 
        # Asignación, incremental, decremental
        self.Simbolo["="]  = 85
        self.Simbolo["+="] = 86
        self.Simbolo["-="] = 87
        self.Simbolo["*="] = 88
        self.Simbolo["/="] = 89
        self.Simbolo["++"] = 90
        self.Simbolo["--"] = 91
 
        # Operadores Relacionales
        self.Simbolo["=="] = 92
        self.Simbolo["!="] = 93
        self.Simbolo["<"]  = 94
        self.Simbolo[">"]  = 95
        self.Simbolo["<="] = 96
        self.Simbolo[">="] = 97
 
        # Operadores Lógicos
        self.Simbolo["&&"] = 98
        self.Simbolo["||"] = 99
        self.Simbolo["!"]  = 100
 
        # Operadores de Agrupación
        self.Simbolo["("]  = 75
        self.Simbolo[")"]  = 76
        self.Simbolo["{"]  = 101
        self.Simbolo["}"]  = 102
        self.Simbolo["["]  = 103
        self.Simbolo["]"]  = 104
 
        # Misceláneos
        self.Simbolo[";"]  = 92
        self.Simbolo[","]  = 105
        self.Simbolo["."]  = 106
        self.Simbolo[":"]  = 107
        self.Simbolo["#"]  = 108
        self.Simbolo["\""] = 109
        self.Simbolo["'"]  = 110
        self.Simbolo["&"]  = 111
        self.Simbolo["|"]  = 112
        self.Simbolo["^"]  = 113
        self.Simbolo["~"]  = 114
        self.Simbolo["<<"] = 115
        self.Simbolo[">>"] = 116
 
    # ──────────────────────────────────────────────────────────
    #  GetTokenPalabra
    #  Busca el token de una palabra reservada o identificador
    #  Retorna el token si existe, 300 si es identificador
    # ──────────────────────────────────────────────────────────
    def GetTokenPalabra(self, Lexema: str) -> int:
        if Lexema in self.Palabra:
            return self.Palabra[Lexema]
        else:
            return 300  # Es un identificador
 
    # ──────────────────────────────────────────────────────────
    #  GetTokenSimbolo
    #  Busca el token de un símbolo
    #  Retorna el token si existe, -1 si no se encontró
    # ──────────────────────────────────────────────────────────
    def GetTokenSimbolo(self, Lexema: str) -> int:
        if Lexema in self.Simbolo:
            return self.Simbolo[Lexema]
        else:
            return -1  # Símbolo no encontrado