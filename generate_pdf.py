"""
Script para generar un PDF del informe técnico usando reportlab.
Ejecutar: python generate_pdf.py
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from pathlib import Path

def generate_pdf():
    """Generate a professional PDF report from the markdown content."""
    
    output_path = Path(__file__).parent / "docs" / "report_final.pdf"
    
    # Create document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        title="Informe Técnico: Compilador MiniLang"
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        alignment=1  # center
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#003366'),
        spaceAfter=10,
        spaceBefore=10
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=8,
        spaceBefore=8
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=4,  # justify
        spaceAfter=8
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['BodyText'],
        fontSize=9,
        fontName='Courier',
        textColor=colors.HexColor('#333333'),
        backColor=colors.HexColor('#f5f5f5'),
        spaceAfter=8,
        leftIndent=20,
        rightIndent=20
    )
    
    # Build content
    content = []
    
    # Title and metadata
    content.append(Paragraph("Informe Técnico: Compilador Completo MiniLang", title_style))
    content.append(Spacer(1, 0.1*inch))
    content.append(Paragraph("<b>Autor:</b> Proyecto de Compiladores", body_style))
    content.append(Paragraph("<b>Fecha:</b> Octubre/Noviembre 2025", body_style))
    content.append(Paragraph("<b>Versión:</b> 1.0 (Completo)", body_style))
    content.append(Spacer(1, 0.3*inch))
    
    # Section 1
    content.append(Paragraph("1. Introducción y Descripción del Lenguaje", heading1_style))
    content.append(Paragraph(
        "MiniLang es un lenguaje de programación simple diseñado para demostrar todas las etapas clásicas del proceso de compilación. "
        "El lenguaje soporta tipos enteros implícitos, operaciones aritméticas (+, -, *, /), operadores relacionales (&lt;, &gt;, &lt;=, &gt;=, ==, !=), "
        "estructuras de control (if/else, while), entrada/salida (read, print) y bloques delimitados por llaves.",
        body_style
    ))
    content.append(Spacer(1, 0.15*inch))
    
    content.append(Paragraph("<b>Ejemplo de Programa MiniLang:</b>", heading2_style))
    example_code = """read a;
read b;
c = a + b * 2;
if c >= 10 {
    print c;
} else {
    print 0;
}
end"""
    content.append(Preformatted(example_code, code_style))
    content.append(Spacer(1, 0.2*inch))
    
    # Section 2
    content.append(Paragraph("2. Gramática Formal (EBNF)", heading1_style))
    content.append(Paragraph(
        "La gramática del lenguaje define la estructura sintáctica permitida. Los operadores respetan precedencia estándar: "
        "multiplicación/división antes que suma/resta, y operaciones relacionales tienen precedencia sobre igualdad.",
        body_style
    ))
    content.append(Spacer(1, 0.1*inch))
    
    grammar = """program ::= { statement } 'end'
statement ::= 'read' IDENT ';'
           | 'print' expression ';'
           | IDENT '=' expression ';'
           | 'if' expression '{' { statement } '}' ...
           | 'while' expression '{' { statement } '}'
expression ::= relation { ('==' | '!=') relation }
relation ::= additive { ('<' | '>' | '<=' | '>=') additive }
additive ::= multiplicative { ('+' | '-') multiplicative }
multiplicative ::= factor { ('*' | '/') factor }
factor ::= NUMBER | IDENT | '(' expression ')'"""
    
    content.append(Preformatted(grammar, code_style))
    content.append(Spacer(1, 0.2*inch))
    
    # Section 3
    content.append(Paragraph("3. Diseño Modular y Arquitectura", heading1_style))
    
    modules = [
        ("<b>Analizador Léxico</b> (lexer.py, tokens.py): ", 
         "Lee el código fuente y genera tokens. Soporta comentarios (// y /* */) y reporta errores con línea/columna."),
        ("<b>Analizador Sintáctico</b> (parser.py): ", 
         "Parser recursivo descendente que construye el AST (Árbol Sintáctico Abstracto) según la gramática EBNF."),
        ("<b>Analizador Semántico</b> (semantic.py): ", 
         "Construye tabla de símbolos y verifica que variables se inicialicen antes de usarse."),
        ("<b>Generador de IR</b> (ir.py): ", 
         "Traduce el AST a TAC (Three-Address Code) usando temporales y etiquetas para control de flujo."),
        ("<b>Optimizador</b> (optimizer.py): ", 
         "Aplica constant folding: reemplaza operaciones constantes por sus resultados."),
        ("<b>Generador de ASM</b> (codegen_asm.py): ", 
         "Traduce TAC a ensamblador simbólico (PUSH, LOAD, STORE, ADD, SUB, MUL, DIV, JMP, JNZ, etc.)."),
        ("<b>Ensamblador</b> (codegen_machine.py): ", 
         "Convierte líneas de ASM a tuplas (mnemonic, args) y resuelve etiquetas."),
        ("<b>Máquina Virtual</b> (runtime_vm.py): ", 
         "VM basada en pila que ejecuta el código ensamblado con soporte para E/S y saltos condicionales."),
        ("<b>Orquestador</b> (compiler.py): ", 
         "Script principal que ejecuta todo el pipeline: lexer → parser → semántica → IR → opt → ASM → VM."),
    ]
    
    for title, desc in modules:
        content.append(Paragraph(f"{title}{desc}", body_style))
        content.append(Spacer(1, 0.05*inch))
    
    content.append(Spacer(1, 0.15*inch))
    
    # Section 4
    content.append(Paragraph("4. Ejemplo Completo de Compilación", heading1_style))
    content.append(Paragraph(
        "Se compilará el programa 'simple_noio.minilang' mostrando cada etapa del pipeline:",
        body_style
    ))
    content.append(Spacer(1, 0.1*inch))
    
    content.append(Paragraph("<b>Programa Fuente:</b>", heading2_style))
    src_code = """i = 2;
j = 3;
sum = i + j * 4;
print sum;
end"""
    content.append(Preformatted(src_code, code_style))
    content.append(Spacer(1, 0.1*inch))
    
    content.append(Paragraph("<b>Etapa 1 - Tokens (Lexer):</b>", heading2_style))
    content.append(Paragraph(
        "El lexer genera una secuencia de tokens: IDENT(i), ASSIGN, NUMBER(2), SEMI, IDENT(j), ... TOKEN(END), TOKEN(EOF). "
        "Cada token incluye línea y columna para debugging.",
        body_style
    ))
    content.append(Spacer(1, 0.1*inch))
    
    content.append(Paragraph("<b>Etapa 2 - AST (Parser):</b>", heading2_style))
    content.append(Paragraph(
        "El parser construye: Program([Assign('i', Literal(2)), Assign('j', Literal(3)), "
        "Assign('sum', BinaryOp('+', Var('i'), BinaryOp('*', Var('j'), Literal(4)))), Print(Var('sum'))])",
        code_style
    ))
    content.append(Spacer(1, 0.1*inch))
    
    content.append(Paragraph("<b>Etapa 3 - TAC (Code Generator):</b>", heading2_style))
    tac_code = """TAC(assign, i, 2, None)
TAC(assign, j, 3, None)
TAC(binop, t1, *, ('j', '4'))
TAC(binop, t2, +, ('i', 't1'))
TAC(assign, sum, t2, None)
TAC(print, sum, None, None)"""
    content.append(Preformatted(tac_code, code_style))
    content.append(Spacer(1, 0.1*inch))
    
    content.append(Paragraph("<b>Etapa 4 - Ensamblador (Codegen ASM):</b>", heading2_style))
    asm_code = """PUSH 2      # cargar 2
STORE i     # almacenar en i
PUSH 3      # cargar 3
STORE j     # almacenar en j
LOAD j      # cargar j
PUSH 4      # cargar 4
MUL         # multiplicar
STORE t1    # almacenar en t1
LOAD i      # cargar i
LOAD t1     # cargar t1
ADD         # sumar
STORE t2    # almacenar en t2
LOAD t2     # cargar t2
STORE sum   # almacenar en sum
LOAD sum    # cargar sum
OUT         # imprimir"""
    content.append(Preformatted(asm_code, code_style))
    content.append(Spacer(1, 0.1*inch))
    
    content.append(Paragraph("<b>Etapa 5 - Ejecución VM:</b>", heading2_style))
    content.append(Paragraph(
        "<b>Entrada:</b> ninguna<br/><b>Salida:</b> 14",
        body_style
    ))
    content.append(Paragraph(
        "<b>Explicación:</b> i=2, j=3, sum = 2 + 3*4 = 2 + 12 = 14. El programa imprime 14.",
        body_style
    ))
    content.append(Spacer(1, 0.2*inch))
    
    # Section 5
    content.append(Paragraph("5. Pruebas y Validación", heading1_style))
    content.append(Paragraph(
        "Se incluyen 4 pruebas unitarias que validan cada etapa del compilador:",
        body_style
    ))
    content.append(Spacer(1, 0.1*inch))
    
    tests = [
        "<b>test_lexer.py:</b> Verifica tokenización correcta.",
        "<b>test_parser.py:</b> Verifica construcción de AST válido.",
        "<b>test_semantic.py:</b> Prueba análisis semántico (acepta válido, rechaza inválido).",
        "<b>test_full_pipeline.py:</b> Prueba completa: compila y ejecuta, verifica salida.",
    ]
    
    for test in tests:
        content.append(Paragraph(test, body_style))
    
    content.append(Spacer(1, 0.1*inch))
    content.append(Paragraph(
        "<b>Resultado:</b> Todas las pruebas pasan satisfactoriamente, confirmando que el compilador funciona correctamente.",
        body_style
    ))
    content.append(Spacer(1, 0.2*inch))
    
    # Section 6
    content.append(Paragraph("6. Conclusión", heading1_style))
    content.append(Paragraph(
        "Se ha desarrollado un compilador funcional y didáctico que implementa todas las etapas clásicas del proceso de compilación: "
        "análisis léxico, sintáctico y semántico; generación de código intermedio con optimización; y una máquina virtual ejecutable. "
        "El proyecto está bien estructurado en módulos independientes, totalmente documentado, y permite extensiones futuras.",
        body_style
    ))
    
    # Build PDF
    doc.build(content, onFirstPage=add_header, onLaterPages=add_header)
    print(f"✅ PDF generado exitosamente: {output_path}")

def add_header(canvas_obj, doc):
    """Add header and footer to each page."""
    canvas_obj.saveState()
    
    # Footer
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.drawString(0.75*inch, 0.5*inch, 
        f"Compilador MiniLang - Proyecto de Compiladores 2025")
    canvas_obj.drawRightString(A4[0] - 0.75*inch, 0.5*inch, 
        f"Página {doc.page}")
    
    canvas_obj.restoreState()

if __name__ == '__main__':
    generate_pdf()
