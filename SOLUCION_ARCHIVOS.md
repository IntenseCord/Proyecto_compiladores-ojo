# ❓ ¿Por Qué No Funciona? - Solución

## El Problema

```powershell
python .\minilang_compiler\compiler.py .\tu_programa.minilang --run
# Error: Source file not found: tu_programa.minilang
```

**Razón:** `tu_programa.minilang` es solo un **placeholder (ejemplo ficticio)**. El archivo **no existe**.

---

## ✅ La Solución

### **Opción 1: Usa uno de los archivos .minilang existentes**

El compilador incluye 3 programas de prueba listos para usar:

#### 1️⃣ **simple_noio.minilang** (El más simple - SIN entrada)
```minilang
i = 2;
j = 3;
sum = i + j * 4;
print sum;
end
```

**Ejecutar:**
```powershell
python .\minilang_compiler\compiler.py .\tests\simple_noio.minilang --run
```

**Resultado:** `14` ✅

---

#### 2️⃣ **sample.minilang** (Programa completo - CON entrada)
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

**Ejecutar:**
```powershell
python .\minilang_compiler\compiler.py .\tests\sample.minilang --run
```

**Interactivo:** Te pedirá que ingreses `a` y `b` ✅

---

#### 3️⃣ **ejemplo_usuario.minilang** (Ejemplo de suma - CON entrada)
```minilang
// Suma dos números
read num1;
read num2;
resultado = num1 + num2;
print resultado;
end
```

**Ejecutar:**
```powershell
python .\minilang_compiler\compiler.py .\tests\ejemplo_usuario.minilang --run
```

**Ejemplo de ejecución:**
```
IN num1: 5
IN num2: 10
15
```

---

### **Opción 2: Crea tu propio archivo .minilang**

Puedes crear archivos nuevos siguiendo la sintaxis de MiniLang.

#### **Paso 1: Crear el archivo**

Crea un archivo llamado `mi_programa.minilang` en la carpeta `tests/`:

```minilang
// Mi primer programa
read x;
y = x * 2;
print y;
end
```

#### **Paso 2: Ejecutarlo**

```powershell
python .\minilang_compiler\compiler.py .\tests\mi_programa.minilang --run
```

**Entrada y salida:**
```
IN x: 7
14
```

---

## 📋 Sintaxis de Archivos .minilang

### **Instrucciones Básicas**

```minilang
// Comentario de línea

/* Comentario
   de múltiples líneas */

// Lectura de entrada
read variable;

// Asignación
variable = expresion;

// Impresión
print variable;

// Condicional
if condicion {
    instrucciones;
} else {
    instrucciones;
}

// Bucle
while condicion {
    instrucciones;
}

// Fin del programa
end
```

### **Operadores Disponibles**

- **Aritméticos:** `+`, `-`, `*`, `/`
- **Relacionales:** `<`, `>`, `<=`, `>=`, `==`, `!=`
- **Precedencia:** Multiplicación/División > Adición/Sustracción

### **Ejemplo Completo**

```minilang
// Calcular factorial
read n;
factorial = 1;
i = 2;
while i <= n {
    factorial = factorial * i;
    i = i + 1;
}
print factorial;
end
```

---

## 🎯 Resumen: Qué Hacer

| Situación | Comando |
|---|---|
| **Quiero probar el compilador rápido** | `python .\minilang_compiler\compiler.py .\tests\simple_noio.minilang --run` |
| **Quiero ver un programa completo** | `python .\minilang_compiler\compiler.py .\tests\sample.minilang --run` |
| **Quiero ver un ejemplo de suma** | `python .\minilang_compiler\compiler.py .\tests\ejemplo_usuario.minilang --run` |
| **Quiero crear mi propio programa** | Crea `mi_archivo.minilang` en `tests/` y ejecuta como arriba |

---

## ⚠️ Errores Comunes

### ❌ Error: "Source file not found"
```powershell
python .\minilang_compiler\compiler.py .\archivo_inexistente.minilang --run
```

**Solución:** Asegúrate de que el archivo existe en la carpeta `tests/`

### ❌ Error: "Syntax error"
Si tu programa tiene error de sintaxis:

```minilang
read x
y = x + 1;  // Falta ; en la línea anterior
end
```

**Solución:** Revisa la sintaxis de MiniLang

### ❌ Error: "Use of uninitialized variable"
Si usas una variable antes de inicializarla:

```minilang
y = x + 1;  // x nunca fue inicializado
end
```

**Solución:** Primero asigna un valor: `x = 5;`

---

## 📂 Estructura de Archivos

```
ProyectiniCompiladores/
├── tests/
│   ├── simple_noio.minilang       ✅ Usa este
│   ├── sample.minilang            ✅ O este
│   ├── ejemplo_usuario.minilang   ✅ O este
│   ├── bad.minilang               (Tiene error semántico)
│   └── mi_archivo.minilang        👈 Crea aquí tus programas
├── minilang_compiler/
│   └── compiler.py
└── ...
```

---

## 🚀 Próximos Pasos

1. ✅ Entiende la sintaxis de MiniLang
2. ✅ Ejecuta los programas de prueba
3. ✅ Crea tu propio programa
4. ✅ Revisa el informe en `docs/report_final.pdf`

---

*Problema resuelto: Los archivos que uses deben existir en la carpeta `tests/` o especificar la ruta correcta.*
