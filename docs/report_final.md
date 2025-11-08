# Informe Técnico: Compilador Completo MiniLang

**Autor:** Proyecto de Compiladores  
**Fecha:** Octubre/Noviembre 2025  
**Versión:** 1.0 (Completo)

---

## 1. Introducción y Descripción del Lenguaje

MiniLang es un lenguaje de programación simple diseñado para demostrar todas las etapas clásicas del proceso de compilación. El lenguaje soporta:

- **Tipos de datos:** Enteros (implícitos, sin declaración explícita).
- **Operaciones aritméticas:** `+`, `-`, `*`, `/` con precedencia estándar.
- **Operadores relacionales:** `<`, `>`, `<=`, `>=`, `==`, `!=`.
- **Estructuras de control:** `if`/`else` (condicionales) y `while` (ciclos).
- **Entrada/Salida:** `read id;` (lectura de variable) y `print expr;` (impresión de expresión).
- **Delimitadores:** Llaves `{}` para bloques, punto y coma `;` para fin de sentencia, palabra clave `end` para fin de programa.

### Ejemplo de Programa MiniLang
```minilang
read a;
read b;
c = a + b * 2;
if c >= 10 {
    print c;
} else {
    print 0;
}
i = 0;
while i < c {
    print i;
    i = i + 1;
}
end
```

---

## 2. Gramática Formal (EBNF)

```
program        ::= { statement } 'end'

statement      ::= 'read' IDENT ';'
               |   'print' expression ';'
               |   IDENT '=' expression ';'
               |   'if' expression '{' { statement } '}' [ 'else' '{' { statement } '}' ]
               |   'while' expression '{' { statement } '}'

expression     ::= relation { ('==' | '!=') relation }
               |   relation

relation       ::= additive { ('<' | '>' | '<=' | '>=') additive }
               |   additive

additive       ::= multiplicative { ('+' | '-') multiplicative }

multiplicative ::= factor { ('*' | '/') factor }

factor         ::= NUMBER
               |   IDENT
               |   '(' expression ')'

IDENT          ::= [a-zA-Z_][a-zA-Z0-9_]*
NUMBER         ::= [0-9]+
```

**Notas sobre la gramática:**
- Los operadores tienen precedencia estándar: multiplicación/división antes que suma/resta.
- Las operaciones relacionales (`<`, `>`, `<=`, `>=`) tienen precedencia sobre igualdad (`==`, `!=`).
- Las estructuras de control (`if`, `while`) permiten bloques multisencencia delimitados por `{}`.

---

## 3. Diseño Modular y Arquitectura del Compilador

El compilador está dividido en los siguientes módulos:

### 3.1 Analizador Léxico (`lexer.py`, `tokens.py`)
- Lee el código fuente carácter por carácter.
- Reconoce palabras reservadas (`read`, `print`, `if`, `else`, `while`, `end`), identificadores, números, operadores y separadores.
- Maneja comentarios de línea (`//`) y bloque (`/* ... */`).
- Genera una lista de tokens con información de línea y columna para reportes de error.

### 3.2 Analizador Sintáctico (`parser.py`)
- Implementa un parser recursivo descendente.
- Verifica la estructura gramatical según la gramática EBNF.
- Construye un Árbol Sintáctico Abstracto (AST) representado mediante clases dataclass en `ast_nodes.py`.
- Emite errores de sintaxis detallados con línea y columna.

### 3.3 Analizador Semántico (`semantic.py`)
- Recorre el AST y construye una tabla de símbolos para rastrear variables.
- Verifica que toda variable se inicialice antes de ser usada.
- Valida la consistencia básica del programa (solo enteros, sin conversión de tipos).
- Emite errores semánticos cuando detecta uso de variables no inicializadas.

### 3.4 Generador de Código Intermedio (`ir.py`)
- Traduce el AST a Código Intermedio en formato TAC (Three-Address Code).
- Genera instrucciones: `label`, `goto`, `ifgoto`, `assign`, `binop`, `read`, `print`.
- Usa temporales `t1`, `t2`, ... para almacenar resultados intermedios.
- Usa etiquetas `L1`, `L2`, ... para destinos de salto.

### 3.5 Optimizador (`optimizer.py`)
- Implementa "constant folding": reemplaza operaciones aritméticas con operandos constantes por el resultado constante.
- Reducible en futuras versiones a dead code elimination y copy propagation.

### 3.6 Generador de Ensamblador (`codegen_asm.py`)
- Traduce TAC a ensamblador simbólico para una máquina virtual de pila.
- Instrucciones soportadas: `PUSH`, `LOAD`, `STORE`, `ADD`, `SUB`, `MUL`, `DIV`, `LT`, `GT`, `LE`, `GE`, `EQ`, `NE`, `JMP`, `JNZ`, `JZ`, `IN`, `OUT`.
- Etiquetas se representan como strings (`L1:`, `L2:`, ...) para permitir resolución de direcciones.

### 3.7 Ensamblador (`codegen_machine.py`)
- Convierte líneas de ensamblador simbólico a tuplas `(mnemonic, args)`.
- Resuelve etiquetas y construye una tabla de saltos.
- La salida es una lista de instrucciones legibles por la VM.

### 3.8 Máquina Virtual (`runtime_vm.py`)
- Máquina virtual basada en pila con una memoria local (`vars` dict).
- Ejecuta instrucciones: carga/almacena variables, aritmética, comparaciones, saltos condicionales, entrada/salida.
- Soporta entrada interactiva (`input()`) y salida a consola (`print`).

### 3.9 Orquestador Principal (`compiler.py`)
- Script que ejecuta todo el pipeline: lexer → parser → semantic → IR → optimizer → ASM → assemble → VM (opcional).
- Parámetro `--run` ejecuta la máquina virtual tras la compilación.
- Imprime cada etapa intermedia (tokens, TAC, ASM, máquina) para debugging.

---

## 4. Ejemplo Completo de Compilación

### Programa Fuente (archivo: `tests/simple_noio.minilang`)
```minilang
i = 2;
j = 3;
sum = i + j * 4;
print sum;
end
```

### Paso 1: Tokens (Salida del Lexer)
```
Token(IDENT, 'i', 1:1)
Token(ASSIGN, '=', 1:3)
Token(NUMBER, '2', 1:5)
Token(SEMI, ';', 1:6)
Token(IDENT, 'j', 2:1)
Token(ASSIGN, '=', 2:3)
Token(NUMBER, '3', 2:5)
Token(SEMI, ';', 2:6)
Token(IDENT, 'sum', 3:1)
Token(ASSIGN, '=', 3:5)
Token(IDENT, 'i', 3:7)
Token(PLUS, '+', 3:9)
Token(IDENT, 'j', 3:11)
Token(MUL, '*', 3:13)
Token(NUMBER, '4', 3:15)
Token(SEMI, ';', 3:16)
Token(PRINT, 'print', 4:1)
Token(IDENT, 'sum', 4:7)
Token(SEMI, ';', 4:10)
Token(END, 'end', 5:1)
Token(EOF, None, 6:1)
```

### Paso 2: Árbol Sintáctico Abstracto (AST)
```
Program(statements=[
  Assign(target='i', expr=Literal(value=2)),
  Assign(target='j', expr=Literal(value=3)),
  Assign(target='sum', expr=BinaryOp(op='+', 
    left=Var(name='i'),
    right=BinaryOp(op='*', left=Var(name='j'), right=Literal(value=4))
  )),
  Print(expr=Var(name='sum'))
])
```

### Paso 3: Código Intermedio (TAC)
```
TAC(assign, i, 2, None)           // i = 2
TAC(assign, j, 3, None)           // j = 3
TAC(binop, t1, *, ('j', '4'))     // t1 = j * 4
TAC(binop, t2, +, ('i', 't1'))    // t2 = i + t1
TAC(assign, sum, t2, None)        // sum = t2
TAC(print, sum, None, None)       // print sum
```

### Paso 4: TAC Optimizado (Constant Folding)
```
TAC(assign, i, 2, None)
TAC(assign, j, 3, None)
TAC(binop, t1, *, ('j', '4'))     // no optimizable (j es variable)
TAC(binop, t2, +, ('i', 't1'))    // no optimizable
TAC(assign, sum, t2, None)
TAC(print, sum, None, None)
```

### Paso 5: Ensamblador Simbólico
```asm
PUSH 2
STORE i
PUSH 3
STORE j
LOAD j
PUSH 4
MUL
STORE t1
LOAD i
LOAD t1
ADD
STORE t2
LOAD t2
STORE sum
LOAD sum
OUT
```

### Paso 6: Código Máquina (Ensamblado)
```
('PUSH', ['2'])
('STORE', ['i'])
('PUSH', ['3'])
('STORE', ['j'])
('LOAD', ['j'])
('PUSH', ['4'])
('MUL', [])
('STORE', ['t1'])
('LOAD', ['i'])
('LOAD', ['t1'])
('ADD', [])
('STORE', ['t2'])
('LOAD', ['t2'])
('STORE', ['sum'])
('LOAD', ['sum'])
('OUT', [])
```

### Paso 7: Ejecución en la Máquina Virtual
```
Entrada: (ninguna)
Salida: 14
```

**Explicación del resultado:**
- `i = 2, j = 3`
- `sum = i + j * 4 = 2 + 3 * 4 = 2 + 12 = 14`
- `print sum` imprime `14`.

---

## 5. Pruebas y Validación

El proyecto incluye pruebas unitarias para cada etapa:

1. **test_lexer.py:** Verifica que el lexer tokenice correctamente el programa de ejemplo.
2. **test_parser.py:** Verifica que el parser construye un AST válido con estructuras `If` y `While`.
3. **test_semantic.py:** Prueba análisis semántico: acepta programa válido y rechaza uso de variable no inicializada.
4. **test_full_pipeline.py:** Prueba end-to-end: compila y ejecuta un programa simple, verificando la salida de la VM.

**Ejecución de pruebas:**
```bash
python .\tests\test_lexer.py
python .\tests\test_parser.py
python .\tests\test_semantic.py
python .\tests\test_full_pipeline.py
```

Todas las pruebas deben pasar satisfactoriamente, confirmando que el compilador funciona de extremo a extremo.

---

## 6. Conclusión

Se ha desarrollado un compilador funcional completo para el lenguaje MiniLang que implementa todas las etapas clásicas:
- Análisis léxico, sintáctico y semántico.
- Generación de código intermedio (TAC) con optimización básica.
- Generación de ensamblador para una máquina virtual de pila.
- Una máquina virtual ejecutable.

El compilador está bien estructurado en módulos independientes, documenta cada etapa con ejemplos claros y permite extensiones futuras como dead code elimination, copy propagation y otras optimizaciones de compiladores avanzados.
