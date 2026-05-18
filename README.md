* Gerardy Maria Fernanda Barrios Ixcot 
* Carnet: 202425513
* Curso Autómatas y Lenguajes
* Proyecto: Compilador MicroC

## Descripción del Proyecto         
El proyecto Pre-compilador MicroC consiste en el desarrollo de una aplicación que simula las primaras etapas de un compilador para un lenguaje en simplificado llamado MicroC hecho en python. El sistema permite cargar archivo de código fuente, analizar su estructura y verificar posibles errores básicos antes del proceso de compilacion. Ademas el objetivo principal es aplicar los conceptos aprendidos en el curso de Autómatas y lenguaje, comprendiendo cómo funcionan los procesos internos de un compilador y fortaleciendo habilidades en programación y organización de proyectos con GitHub.


## Tecnologías Utilizadas       
Lenguaje: Python 3
Editor de código: Visual Studio Code 
Control de versiones: Git y GitHub
Librerías utilizadas
* tkinter 
* filedialog 
* messagebox 
* font
* os
              

## Instruciones de Ejecusión        
* Abrir la carpeta del proyecto en Visual Studio code.
* Verificar que Python esté instalado en el sistema.
* Abrir  la terminal dentro del proyecto.
* ejecutar el programa con el siguiente comando (python src/microc_compiler.py)
* Se abrirá la aplicación del Pre-Compilador MicroC donde se podrá cargar un archivo de código y realizar el análisis correspondiente.


# Commits Realizados


| # | Mensaje | Descripción |
|---|---|---|
| 1 | `init: estructura inicial del repositorio` | Creación del repositorio y README base |
| 2 | `feat: crear interfaz gráfica base con Tkinter` | Diseño de la ventana principal |
| 3 | `feat: implementar funcionalidad Abrir archivo` | Botón Abrir con modo solo lectura |
| 4 | `feat: implementar funcionalidad Guardar archivo` | Guardar nuevo y sobreescribir |
| 5 | `feat: implementar Editar y Salir con confirmación` | Botones Editar y Salir |
| 6 | `feat: agregar numeración de líneas y barra de estado` | Mejoras visuales del editor |
| 7 | `docs: agregar manual de usuario` | Manual de usuario en /docs |
| 8 | `docs: agregar capturas de pantalla` | Imágenes de la interfaz |
| 9 | `fix: resolver conflicto manual de usuario` | Corrección de conflicto Git |
| 10 | `docs: README completo con datos del estudiante` | README finalizado |


<img width="1006" height="636" alt="image" src="https://github.com/user-attachments/assets/2bae9480-f935-4666-a83d-aeb3ed539612" />

# Captura de la interfaz grafica del Pre-Compilador MicroC
<img width="1102" height="723" alt="image" src="https://github.com/user-attachments/assets/826a6182-78e1-4e87-b49c-4e11b43f5d44" />

## Analizador Léxico — Fase I y Fase II

### ¿Qué es el Analizador Léxico?
Es la primera etapa del compilador. Lee el código fuente carácter 
por carácter y clasifica cada elemento en tokens siguiendo el 
diagrama de flujo proporcionado.

### Clases Implementadas

| Clase | Archivo | Descripción |
|---|---|---|
| `frmEditor` | `microc_compiler.py` | Interfaz gráfica del compilador |
| `AnalizadorLexico` | `analizador_lexico.py` | Análisis léxico con autómatas |
| `UnidadesLexicas` | `unidades_lexicas.py` | Diccionario de tokens |

---

### FASE I — Tareas Básicas

| Tarea | Estado |
|---|---|
| Generar lista de tokens | ✅ |
| Eliminar espacios y tabuladores | ✅ |
| Relacionar líneas con el análisis | ✅ |
| Identificar lexemas y tokens | ✅ |

### FASE II — Completar lista de Tokens

| Tarea | Estado |
|---|---|
| Identificar palabras reservadas | ✅ |
| Identificar números enteros y reales | ✅ |
| Identificar comentarios // y /* */ | ✅ |
| Detectar símbolos no reconocidos | ✅ |

---

### Autómatas Implementados
#### 🤖 Autómata 1 — IdentificadorPalabraReservada

q0 --[letra|]--> q1
q1 --[letra|dígito|]--> q1
q1 --[otro]--> q2 (ACEPTAR)
Resultado: Token de palabra reservada o Token 300 (identificador)

#### 🤖 Autómata 2 — EnteroReal

q0 --[dígito]--> q1
q1 --[dígito]--> q1
q1 --[punto]--> q2
q2 --[dígito]--> q3
q3 --[dígito]--> q3
q1|q3 --[otro]--> q4 (ACEPTAR)
Resultado: Token 200 (entero) o Token 201 (real)

#### 🤖 Autómata 3 — AutomataComentario
q0 --[/]--> q1
q1 --[/]--> q2 (línea)
q1 --[]--> q3 (bloque)
q1 --[otro]--> q6 (división)
q2 --[\n]--> q5 (ACEPTAR)
q3 --[]--> q4 --[/]--> q5 (ACEPTAR)

### Capturas de Pantalla — Analizador Léxico

**Compilación normal — palabras reservadas e identificadores:**
<img width="710" height="476" alt="Captura de pantalla 2026-05-17 230156" src="https://github.com/user-attachments/assets/3fcc23ac-d166-4e51-9061-bb9b379782d7" />

**Números enteros y reales:**
<img width="695" height="404" alt="Captura de pantalla 2026-05-17 230212" src="https://github.com/user-attachments/assets/54fdef4e-2a30-4cc4-b0a7-a749c0e7a946" />

**Comentarios ignorados:**
<img width="678" height="409" alt="Captura de pantalla 2026-05-17 230244" src="https://github.com/user-attachments/assets/abbf33b4-9599-4969-9d73-e400a32e5dfc" />

**Detección de errores:**
<img width="870" height="430" alt="Captura de pantalla 2026-05-17 230305" src="https://github.com/user-attachments/assets/ca0177c7-24d1-4030-b1e4-fc63287dcd2f" />

---

# Video Demostrativo 
discule la calidad y disculpe que lo haya grabado en el teléfono ya que ah la hora de grabar no se miraba la interfaz grafica y tuve que tomar otra alternativa. 
(https://youtu.be/e2tFPNO_uIU)

### Video Demostrativo — Analizador Léxico
https://youtu.be/7JCXQHlOgM8


