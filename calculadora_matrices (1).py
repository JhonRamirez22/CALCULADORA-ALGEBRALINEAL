# ============================================================================
# CALCULADORA DE MATRICES, SISTEMAS LINEALES Y VECTORES
# Proyecto: Ecuaciones Diferenciales - Álgebra Lineal
# Descripción: Programa con interfaz gráfica para operaciones matriciales,
#              sistemas lineales y vectoriales
# ============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import math
from fractions import Fraction
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class CalculadoraMatricesVectores:
    """Clase principal para la calculadora"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Matrices, Sistemas Lineales y Vectores")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Estilos
        style = ttk.Style()
        style.theme_use('clam')
        
        # Variables para almacenar matrices
        self.matriz1 = None
        self.matriz2 = None
        self.sistema_A = None
        self.sistema_b = None
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.frame_matrices = ttk.Frame(self.notebook)
        self.frame_sistemas = ttk.Frame(self.notebook)
        self.frame_vectores = ttk.Frame(self.notebook)
        
        self.notebook.add(self.frame_matrices, text="Matrices")
        self.notebook.add(self.frame_sistemas, text="Sistemas Lineales")
        self.notebook.add(self.frame_vectores, text="Vectores")
        
        # Inicializar contenidos
        self.crear_interfaz_matrices()
        self.crear_interfaz_sistemas()
        self.crear_interfaz_vectores()
    
    # ========================================================================
    # SECCIÓN 1: MATRICES
    # ========================================================================
    
    def crear_interfaz_matrices(self):
        """Crea la interfaz para operaciones con matrices"""
        
        # Frame principal
        main_frame = ttk.Frame(self.frame_matrices)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sección de entrada
        entrada_frame = ttk.LabelFrame(main_frame, text="Entrada de Dimensiones", padding=10)
        entrada_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(entrada_frame, text="Matriz 1:").grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Label(entrada_frame, text="Filas:").grid(row=0, column=1, sticky=tk.W, padx=5)
        self.m1_filas = ttk.Entry(entrada_frame, width=5)
        self.m1_filas.grid(row=0, column=2, padx=5)
        
        ttk.Label(entrada_frame, text="Columnas:").grid(row=0, column=3, sticky=tk.W, padx=5)
        self.m1_columnas = ttk.Entry(entrada_frame, width=5)
        self.m1_columnas.grid(row=0, column=4, padx=5)
        
        ttk.Label(entrada_frame, text="Matriz 2:").grid(row=1, column=0, sticky=tk.W, padx=5)
        ttk.Label(entrada_frame, text="Filas:").grid(row=1, column=1, sticky=tk.W, padx=5)
        self.m2_filas = ttk.Entry(entrada_frame, width=5)
        self.m2_filas.grid(row=1, column=2, padx=5)
        
        ttk.Label(entrada_frame, text="Columnas:").grid(row=1, column=3, sticky=tk.W, padx=5)
        self.m2_columnas = ttk.Entry(entrada_frame, width=5)
        self.m2_columnas.grid(row=1, column=4, padx=5)
        
        btn_generar = ttk.Button(entrada_frame, text="Generar Campos", 
                                command=self.generar_campos_matrices)
        btn_generar.grid(row=2, column=0, columnspan=5, pady=10)
        
        # Frame para tablas de entrada
        self.tablas_frame = ttk.Frame(main_frame)
        self.tablas_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Frame para operaciones
        ops_frame = ttk.LabelFrame(main_frame, text="Operaciones", padding=10)
        ops_frame.pack(fill=tk.X, pady=5)
        
        btn_suma = ttk.Button(ops_frame, text="Sumar Matrices", 
                             command=self.sumar_matrices)
        btn_suma.pack(side=tk.LEFT, padx=5)
        
        btn_mult = ttk.Button(ops_frame, text="Multiplicar Matrices", 
                             command=self.multiplicar_matrices)
        btn_mult.pack(side=tk.LEFT, padx=5)
        
        btn_ejemplo = ttk.Button(ops_frame, text="Cargar Ejemplo", 
                                command=self.ejemplo_matrices)
        btn_ejemplo.pack(side=tk.LEFT, padx=5)
        
        # Frame para resultados
        self.resultado_matrices_frame = ttk.LabelFrame(main_frame, text="Resultado", padding=10)
        self.resultado_matrices_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.resultado_matrices_text = tk.Text(self.resultado_matrices_frame, height=10, width=80, 
                                              state=tk.DISABLED, wrap=tk.WORD)
        self.resultado_matrices_text.pack(fill=tk.BOTH, expand=True)
    
    def generar_campos_matrices(self):
        """Genera campos para ingreso de elementos de matrices"""
        try:
            # Validar que sean enteros
            filas1 = self.m1_filas.get()
            cols1 = self.m1_columnas.get()
            filas2 = self.m2_filas.get()
            cols2 = self.m2_columnas.get()
            
            # Validar que sean números enteros
            try:
                filas1 = int(filas1)
                cols1 = int(cols1)
                filas2 = int(filas2)
                cols2 = int(cols2)
            except ValueError:
                messagebox.showerror("Error", "el tamaño de las matrices debe ser un número entero")
                return
            
            # Limpiar frame anterior
            for widget in self.tablas_frame.winfo_children():
                widget.destroy()
            
            # Crear variables para almacenar datos
            self.entries_m1 = []
            self.entries_m2 = []
            
            # Matriz 1
            frame_m1 = ttk.LabelFrame(self.tablas_frame, text=f"Matriz 1 ({filas1}x{cols1})", padding=5)
            frame_m1.pack(fill=tk.BOTH, padx=5, pady=5)
            
            for i in range(filas1):
                row_entries = []
                for j in range(cols1):
                    entry = ttk.Entry(frame_m1, width=8)
                    entry.grid(row=i, column=j, padx=2, pady=2)
                    row_entries.append(entry)
                self.entries_m1.append(row_entries)
            
            # Matriz 2
            frame_m2 = ttk.LabelFrame(self.tablas_frame, text=f"Matriz 2 ({filas2}x{cols2})", padding=5)
            frame_m2.pack(fill=tk.BOTH, padx=5, pady=5)
            
            for i in range(filas2):
                row_entries = []
                for j in range(cols2):
                    entry = ttk.Entry(frame_m2, width=8)
                    entry.grid(row=i, column=j, padx=2, pady=2)
                    row_entries.append(entry)
                self.entries_m2.append(row_entries)
            
            # Guardar dimensiones
            self.dim_m1 = (filas1, cols1)
            self.dim_m2 = (filas2, cols2)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar campos: {str(e)}")
    
    def obtener_matrices_desde_entries(self):
        """Obtiene las matrices desde los entries"""
        try:
            matriz1 = []
            for row in self.entries_m1:
                fila = []
                for entry in row:
                    valor = entry.get()
                    if valor:
                        fila.append(float(valor))
                    else:
                        raise ValueError("Todos los campos deben estar llenos")
                matriz1.append(fila)
            
            matriz2 = []
            for row in self.entries_m2:
                fila = []
                for entry in row:
                    valor = entry.get()
                    if valor:
                        fila.append(float(valor))
                    else:
                        raise ValueError("Todos los campos deben estar llenos")
                matriz2.append(fila)
            
            self.matriz1 = np.array(matriz1)
            self.matriz2 = np.array(matriz2)
            return True
        
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return False
    
    def sumar_matrices(self):
        """Suma dos matrices"""
        if not hasattr(self, 'entries_m1') or not hasattr(self, 'entries_m2'):
            messagebox.showerror("Error", "Primero debe generar los campos")
            return
        
        if not self.obtener_matrices_desde_entries():
            return
        
        # Verificar que tengan mismo tamaño
        if self.matriz1.shape != self.matriz2.shape:
            resultado = "las matrices no se pueden sumar"
        else:
            resultado_matriz = self.matriz1 + self.matriz2
            resultado = self.formatear_matriz(resultado_matriz, "Suma de Matrices")
        
        self.mostrar_resultado_matrices(resultado)
    
    def multiplicar_matrices(self):
        """Multiplica dos matrices"""
        if not hasattr(self, 'entries_m1') or not hasattr(self, 'entries_m2'):
            messagebox.showerror("Error", "Primero debe generar los campos")
            return
        
        if not self.obtener_matrices_desde_entries():
            return
        
        # Verificar coherencia dimensional
        if self.matriz1.shape[1] != self.matriz2.shape[0]:
            resultado = "las matrices no se pueden multiplicar"
        else:
            resultado_matriz = np.dot(self.matriz1, self.matriz2)
            resultado = self.formatear_matriz(resultado_matriz, "Multiplicación de Matrices")
        
        self.mostrar_resultado_matrices(resultado)
    
    def formatear_matriz(self, matriz, titulo="Matriz"):
        """Formatea una matriz para mostrar"""
        texto = f"\n{titulo}:\n"
        texto += "=" * 50 + "\n"
        for fila in matriz:
            texto += "  [ " + "  ".join([f"{valor:10.4f}" for valor in fila]) + " ]\n"
        return texto
    
    def mostrar_resultado_matrices(self, texto):
        """Muestra el resultado en el area de texto"""
        self.resultado_matrices_text.config(state=tk.NORMAL)
        self.resultado_matrices_text.delete(1.0, tk.END)
        self.resultado_matrices_text.insert(tk.END, texto)
        self.resultado_matrices_text.config(state=tk.DISABLED)
    
    def ejemplo_matrices(self):
        """Carga un ejemplo de matrices"""
        # Matriz de ejemplo
        self.m1_filas.delete(0, tk.END)
        self.m1_filas.insert(0, "3")
        self.m1_columnas.delete(0, tk.END)
        self.m1_columnas.insert(0, "2")
        self.m2_filas.delete(0, tk.END)
        self.m2_filas.insert(0, "3")
        self.m2_columnas.delete(0, tk.END)
        self.m2_columnas.insert(0, "2")
        
        self.generar_campos_matrices()
        
        # Llenar con valores de ejemplo
        valores_m1 = [[100, 150], [200, 120], [80, 90]]
        valores_m2 = [[120, 160], [180, 140], [100, 110]]
        
        for i, fila in enumerate(valores_m1):
            for j, valor in enumerate(fila):
                self.entries_m1[i][j].delete(0, tk.END)
                self.entries_m1[i][j].insert(0, str(valor))
        
        for i, fila in enumerate(valores_m2):
            for j, valor in enumerate(fila):
                self.entries_m2[i][j].delete(0, tk.END)
                self.entries_m2[i][j].insert(0, str(valor))
        
        # Mostrar descripción
        texto = "\n"
        texto += "PROBLEMA DE EJEMPLO - MATRICES DE VENTAS\n"
        texto += "=" * 50 + "\n\n"
        texto += "Una empresa tiene dos centros de distribución.\n"
        texto += "Matriz A: Ventas en Enero\n"
        texto += "Matriz B: Ventas en Febrero\n\n"
        texto += "Matriz A (Enero):\n"
        texto += "  [     100.0000     150.0000 ]\n"
        texto += "  [     200.0000     120.0000 ]\n"
        texto += "  [      80.0000      90.0000 ]\n\n"
        texto += "Matriz B (Febrero):\n"
        texto += "  [     120.0000     160.0000 ]\n"
        texto += "  [     180.0000     140.0000 ]\n"
        texto += "  [     100.0000     110.0000 ]\n\n"
        texto += "Presione 'Sumar Matrices' para ver las ventas totales\n"
        
        self.mostrar_resultado_matrices(texto)
    
    # ========================================================================
    # SECCIÓN 2: SISTEMAS LINEALES
    # ========================================================================
    
    def crear_interfaz_sistemas(self):
        """Crea la interfaz para sistemas de ecuaciones lineales"""
        
        main_frame = ttk.Frame(self.frame_sistemas)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sección de entrada
        entrada_frame = ttk.LabelFrame(main_frame, text="Entrada del Sistema", padding=10)
        entrada_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(entrada_frame, text="Dimensión del sistema (N×N):").pack(side=tk.LEFT, padx=5)
        self.dim_sistema = ttk.Entry(entrada_frame, width=5)
        self.dim_sistema.pack(side=tk.LEFT, padx=5)
        
        btn_generar_sist = ttk.Button(entrada_frame, text="Generar Campos", 
                                     command=self.generar_campos_sistema)
        btn_generar_sist.pack(side=tk.LEFT, padx=5)
        
        btn_ejemplo_sist = ttk.Button(entrada_frame, text="Cargar Ejemplo", 
                                     command=self.ejemplo_sistema)
        btn_ejemplo_sist.pack(side=tk.LEFT, padx=5)
        
        # Frame para tablas
        self.tablas_sist_frame = ttk.Frame(main_frame)
        self.tablas_sist_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Frame para operaciones
        ops_frame = ttk.LabelFrame(main_frame, text="Métodos de Solución", padding=10)
        ops_frame.pack(fill=tk.X, pady=5)
        
        btn_cramer = ttk.Button(ops_frame, text="Resolver con Cramer", 
                               command=self.resolver_cramer)
        btn_cramer.pack(side=tk.LEFT, padx=5)
        
        btn_inversa = ttk.Button(ops_frame, text="Resolver con Matriz Inversa", 
                                command=self.resolver_inversa)
        btn_inversa.pack(side=tk.LEFT, padx=5)
        
        # Frame para resultados
        self.resultado_sist_frame = ttk.LabelFrame(main_frame, text="Resultado", padding=10)
        self.resultado_sist_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(self.resultado_sist_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.resultado_sist_text = tk.Text(self.resultado_sist_frame, height=12, width=80, 
                                          state=tk.DISABLED, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.resultado_sist_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.resultado_sist_text.yview)
    
    def generar_campos_sistema(self):
        """Genera campos para el sistema de ecuaciones"""
        try:
            dim = int(self.dim_sistema.get())
            
            # Limpiar frame anterior
            for widget in self.tablas_sist_frame.winfo_children():
                widget.destroy()
            
            # Crear variables para almacenar datos
            self.entries_A = []
            self.entries_b = []
            
            # Matriz A
            frame_A = ttk.LabelFrame(self.tablas_sist_frame, text=f"Matriz de Coeficientes A ({dim}x{dim})", padding=5)
            frame_A.pack(fill=tk.BOTH, padx=5, pady=5)
            
            for i in range(dim):
                row_entries = []
                for j in range(dim):
                    entry = ttk.Entry(frame_A, width=8)
                    entry.grid(row=i, column=j, padx=2, pady=2)
                    row_entries.append(entry)
                self.entries_A.append(row_entries)
            
            # Vector b
            frame_b = ttk.LabelFrame(self.tablas_sist_frame, text=f"Vector de Términos Independientes b ({dim}x1)", padding=5)
            frame_b.pack(fill=tk.X, padx=5, pady=5)
            
            for i in range(dim):
                entry = ttk.Entry(frame_b, width=8)
                entry.pack(side=tk.LEFT, padx=2, pady=2)
                self.entries_b.append(entry)
            
            self.dim_sist = dim
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero válido")
    
    def obtener_sistema_desde_entries(self):
        """Obtiene el sistema desde los entries"""
        try:
            A = []
            for row in self.entries_A:
                fila = []
                for entry in row:
                    valor = entry.get()
                    if valor:
                        fila.append(float(valor))
                    else:
                        raise ValueError("Todos los campos deben estar llenos")
                A.append(fila)
            
            b = []
            for entry in self.entries_b:
                valor = entry.get()
                if valor:
                    b.append(float(valor))
                else:
                    raise ValueError("Todos los campos deben estar llenos")
            
            self.sistema_A = np.array(A)
            self.sistema_b = np.array(b)
            return True
        
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return False
    
    def calcular_determinante(self, matriz):
        """Calcula el determinante de una matriz"""
        return np.linalg.det(matriz)
    
    def resolver_cramer(self):
        """Resuelve usando el método de Cramer"""
        if not hasattr(self, 'entries_A') or not hasattr(self, 'entries_b'):
            messagebox.showerror("Error", "Primero debe generar los campos")
            return
        
        if not self.obtener_sistema_desde_entries():
            return
        
        det_A = self.calcular_determinante(self.sistema_A)
        
        if abs(det_A) < 1e-10:
            resultado = "El sistema de ecuaciones no tiene solución |A| = 0"
            self.mostrar_resultado_sistema(resultado)
            return
        
        resultado = "\n"
        resultado += "MÉTODO DE CRAMER\n"
        resultado += "=" * 70 + "\n\n"
        resultado += self.formatear_matriz(self.sistema_A, "Matriz A")
        resultado += f"\n|A| = {det_A:.6f}\n\n"
        
        n = len(self.sistema_b)
        solucion = []
        
        for i in range(n):
            A_i = self.sistema_A.copy()
            A_i[:, i] = self.sistema_b
            det_A_i = self.calcular_determinante(A_i)
            
            var_name = chr(120 + i)  # x, y, z, ...
            resultado += self.formatear_matriz(A_i, f"Matriz A{var_name}")
            resultado += f"|A{var_name}| = {det_A_i:.6f}\n"
            resultado += f"{var_name} = |A{var_name}| / |A| = {det_A_i:.6f} / {det_A:.6f} = {det_A_i/det_A:.6f}\n\n"
            
            solucion.append(det_A_i / det_A)
        
        resultado += "\n" + "=" * 70 + "\n"
        resultado += "SOLUCIÓN DEL SISTEMA:\n"
        for i, valor in enumerate(solucion):
            var_name = chr(120 + i)
            resultado += f"{var_name} = {valor:.6f}\n"
        
        self.mostrar_resultado_sistema(resultado)
    
    def resolver_inversa(self):
        """Resuelve usando el método de matriz inversa"""
        if not hasattr(self, 'entries_A') or not hasattr(self, 'entries_b'):
            messagebox.showerror("Error", "Primero debe generar los campos")
            return
        
        if not self.obtener_sistema_desde_entries():
            return
        
        det_A = self.calcular_determinante(self.sistema_A)
        
        if abs(det_A) < 1e-10:
            resultado = "El sistema de ecuaciones no tiene solución |A| = 0 y la matriz A no tiene inversa"
            self.mostrar_resultado_sistema(resultado)
            return
        
        A_inversa = np.linalg.inv(self.sistema_A)
        solucion = np.dot(A_inversa, self.sistema_b)
        
        resultado = "\n"
        resultado += "MÉTODO DE MATRIZ INVERSA\n"
        resultado += "=" * 70 + "\n\n"
        resultado += self.formatear_matriz(self.sistema_A, "Matriz A")
        resultado += f"\n|A| = {det_A:.6f}\n\n"
        resultado += self.formatear_matriz(A_inversa, "Matriz Inversa A^(-1)")
        resultado += "\nSolución: X = A^(-1) * b\n\n"
        resultado += "=" * 70 + "\n"
        resultado += "SOLUCIÓN DEL SISTEMA:\n"
        for i, valor in enumerate(solucion):
            var_name = chr(120 + i)
            resultado += f"{var_name} = {valor:.6f}\n"
        
        self.mostrar_resultado_sistema(resultado)
    
    def mostrar_resultado_sistema(self, texto):
        """Muestra el resultado en el área de texto"""
        self.resultado_sist_text.config(state=tk.NORMAL)
        self.resultado_sist_text.delete(1.0, tk.END)
        self.resultado_sist_text.insert(tk.END, texto)
        self.resultado_sist_text.config(state=tk.DISABLED)
    
    def ejemplo_sistema(self):
        """Carga un ejemplo de sistema"""
        self.dim_sistema.delete(0, tk.END)
        self.dim_sistema.insert(0, "3")
        self.generar_campos_sistema()
        
        # Llenar con valores de ejemplo
        # 2x + y - z = 8
        # -3x - y + 2z = -11
        # -2x + y + 2z = -3
        
        valores_A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
        valores_b = [8, -11, -3]
        
        for i, fila in enumerate(valores_A):
            for j, valor in enumerate(fila):
                self.entries_A[i][j].delete(0, tk.END)
                self.entries_A[i][j].insert(0, str(valor))
        
        for i, valor in enumerate(valores_b):
            self.entries_b[i].delete(0, tk.END)
            self.entries_b[i].insert(0, str(valor))
        
        # Mostrar descripción
        texto = "\n"
        texto += "PROBLEMA DE EJEMPLO - SISTEMA 3x3\n"
        texto += "=" * 70 + "\n\n"
        texto += "Resolver el siguiente sistema de ecuaciones lineales:\n\n"
        texto += "  2x + y - z = 8\n"
        texto += "  -3x - y + 2z = -11\n"
        texto += "  -2x + y + 2z = -3\n\n"
        texto += "Presione 'Resolver con Cramer' o 'Resolver con Matriz Inversa'\n"
        texto += "para ver la solución usando ambos métodos.\n"
        
        self.mostrar_resultado_sistema(texto)
    
    # ========================================================================
    # SECCIÓN 3: VECTORES
    # ========================================================================
    
    def crear_interfaz_vectores(self):
        """Crea la interfaz para operaciones con vectores"""
        
        main_frame = ttk.Frame(self.frame_vectores)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sección de entrada
        entrada_frame = ttk.LabelFrame(main_frame, text="Entrada de Vectores", padding=10)
        entrada_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(entrada_frame, text="Vector 1 - Magnitud:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.v1_mag = ttk.Entry(entrada_frame, width=10)
        self.v1_mag.grid(row=0, column=1, padx=5)
        
        ttk.Label(entrada_frame, text="Ángulo (grados):").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.v1_ang = ttk.Entry(entrada_frame, width=10)
        self.v1_ang.grid(row=0, column=3, padx=5)
        
        ttk.Label(entrada_frame, text="Vector 2 - Magnitud:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.v2_mag = ttk.Entry(entrada_frame, width=10)
        self.v2_mag.grid(row=1, column=1, padx=5)
        
        ttk.Label(entrada_frame, text="Ángulo (grados):").grid(row=1, column=2, sticky=tk.W, padx=5)
        self.v2_ang = ttk.Entry(entrada_frame, width=10)
        self.v2_ang.grid(row=1, column=3, padx=5)
        
        btn_procesar = ttk.Button(entrada_frame, text="Procesar Vectores", 
                                 command=self.procesar_vectores)
        btn_procesar.grid(row=2, column=0, columnspan=4, pady=10)
        
        # Frame para operaciones
        ops_frame = ttk.LabelFrame(main_frame, text="Operaciones Vectoriales", padding=10)
        ops_frame.pack(fill=tk.X, pady=5)
        
        btn_componentes = ttk.Button(ops_frame, text="Componentes Rectangulares", 
                                    command=self.mostrar_componentes)
        btn_componentes.pack(side=tk.LEFT, padx=5)
        
        btn_suma = ttk.Button(ops_frame, text="Suma de Vectores", 
                             command=self.suma_vectores)
        btn_suma.pack(side=tk.LEFT, padx=5)
        
        btn_punto = ttk.Button(ops_frame, text="Producto Punto", 
                              command=self.producto_punto)
        btn_punto.pack(side=tk.LEFT, padx=5)
        
        btn_angulo = ttk.Button(ops_frame, text="Ángulo entre Vectores", 
                               command=self.angulo_vectores)
        btn_angulo.pack(side=tk.LEFT, padx=5)
        
        btn_cruz = ttk.Button(ops_frame, text="Producto Cruz", 
                             command=self.producto_cruz)
        btn_cruz.pack(side=tk.LEFT, padx=5)
        
        btn_ejemplo_vec = ttk.Button(ops_frame, text="Ejemplo", 
                                    command=self.ejemplo_vectores)
        btn_ejemplo_vec.pack(side=tk.LEFT, padx=5)
        
        btn_graficar = ttk.Button(ops_frame, text="Graficar Vectores", 
                                 command=self.graficar_vectores)
        btn_graficar.pack(side=tk.LEFT, padx=5)
        
        # Frame para resultados
        self.resultado_vec_frame = ttk.LabelFrame(main_frame, text="Resultado", padding=10)
        self.resultado_vec_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(self.resultado_vec_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.resultado_vec_text = tk.Text(self.resultado_vec_frame, height=12, width=80, 
                                         state=tk.DISABLED, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.resultado_vec_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.resultado_vec_text.yview)
    
    def procesar_vectores(self):
        """Procesa los vectores ingresados"""
        try:
            v1_mag = float(self.v1_mag.get())
            v1_ang_deg = float(self.v1_ang.get())
            v2_mag = float(self.v2_mag.get())
            v2_ang_deg = float(self.v2_ang.get())
            
            # Convertir a radianes
            v1_ang_rad = math.radians(v1_ang_deg)
            v2_ang_rad = math.radians(v2_ang_deg)
            
            # Calcular componentes
            self.v1_x = v1_mag * math.cos(v1_ang_rad)
            self.v1_y = v1_mag * math.sin(v1_ang_rad)
            self.v2_x = v2_mag * math.cos(v2_ang_rad)
            self.v2_y = v2_mag * math.sin(v2_ang_rad)
            
            self.v1_mag_orig = v1_mag
            self.v2_mag_orig = v2_mag
            self.v1_ang_orig = v1_ang_deg
            self.v2_ang_orig = v2_ang_deg
            
            self.mostrar_componentes()
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos")
    
    def mostrar_componentes(self):
        """Muestra las componentes rectangulares"""
        if not hasattr(self, 'v1_x'):
            messagebox.showerror("Error", "Primero debe procesar los vectores")
            return
        
        resultado = "\n"
        resultado += "COMPONENTES RECTANGULARES\n"
        resultado += "=" * 70 + "\n\n"
        
        resultado += f"Vector 1:\n"
        resultado += f"  Magnitud: {self.v1_mag_orig:.4f}\n"
        resultado += f"  Ángulo: {self.v1_ang_orig:.4f}°\n"
        resultado += f"  V1 = ({self.v1_x:.6f}, {self.v1_y:.6f})\n\n"
        
        resultado += f"Vector 2:\n"
        resultado += f"  Magnitud: {self.v2_mag_orig:.4f}\n"
        resultado += f"  Ángulo: {self.v2_ang_orig:.4f}°\n"
        resultado += f"  V2 = ({self.v2_x:.6f}, {self.v2_y:.6f})\n"
        
        self.mostrar_resultado_vectores(resultado)
    
    def suma_vectores(self):
        """Suma los vectores"""
        if not hasattr(self, 'v1_x'):
            messagebox.showerror("Error", "Primero debe procesar los vectores")
            return
        
        # Sumar componentes
        suma_x = self.v1_x + self.v2_x
        suma_y = self.v1_y + self.v2_y
        
        # Calcular magnitud
        magnitud_suma = math.sqrt(suma_x**2 + suma_y**2)
        
        # Calcular dirección
        angulo_suma_rad = math.atan2(suma_y, suma_x)
        angulo_suma_deg = math.degrees(angulo_suma_rad)
        
        resultado = "\n"
        resultado += "SUMA DE VECTORES\n"
        resultado += "=" * 70 + "\n\n"
        resultado += f"V1 = ({self.v1_x:.6f}, {self.v1_y:.6f})\n"
        resultado += f"V2 = ({self.v2_x:.6f}, {self.v2_y:.6f})\n\n"
        resultado += f"V_suma = V1 + V2\n"
        resultado += f"V_suma = ({suma_x:.6f}, {suma_y:.6f})\n\n"
        resultado += f"Magnitud: |V_suma| = √({suma_x:.6f}² + {suma_y:.6f}²)\n"
        resultado += f"         |V_suma| = {magnitud_suma:.6f}\n\n"
        resultado += f"Dirección: θ = arctan({suma_y:.6f} / {suma_x:.6f})\n"
        resultado += f"          θ = {angulo_suma_deg:.4f}°\n"
        
        self.mostrar_resultado_vectores(resultado)
    
    def producto_punto(self):
        """Calcula el producto punto"""
        if not hasattr(self, 'v1_x'):
            messagebox.showerror("Error", "Primero debe procesar los vectores")
            return
        
        # Producto punto
        prod_punto = self.v1_x * self.v2_x + self.v1_y * self.v2_y
        
        resultado = "\n"
        resultado += "PRODUCTO PUNTO (ESCALAR)\n"
        resultado += "=" * 70 + "\n\n"
        resultado += f"V1 = ({self.v1_x:.6f}, {self.v1_y:.6f})\n"
        resultado += f"V2 = ({self.v2_x:.6f}, {self.v2_y:.6f})\n\n"
        resultado += f"V1 · V2 = (V1x × V2x) + (V1y × V2y)\n"
        resultado += f"V1 · V2 = ({self.v1_x:.6f} × {self.v2_x:.6f}) + ({self.v1_y:.6f} × {self.v2_y:.6f})\n"
        resultado += f"V1 · V2 = {prod_punto:.6f}\n"
        
        self.mostrar_resultado_vectores(resultado)
    
    def angulo_vectores(self):
        """Calcula el ángulo entre vectores"""
        if not hasattr(self, 'v1_x'):
            messagebox.showerror("Error", "Primero debe procesar los vectores")
            return
        
        # Producto punto
        prod_punto = self.v1_x * self.v2_x + self.v1_y * self.v2_y
        
        # Magnitudes
        mag1 = math.sqrt(self.v1_x**2 + self.v1_y**2)
        mag2 = math.sqrt(self.v2_x**2 + self.v2_y**2)
        
        # Ángulo
        cos_ang = prod_punto / (mag1 * mag2)
        # Limitar a [-1, 1] por errores numéricos
        cos_ang = max(-1, min(1, cos_ang))
        angulo_rad = math.acos(cos_ang)
        angulo_deg = math.degrees(angulo_rad)
        
        resultado = "\n"
        resultado += "ÁNGULO ENTRE VECTORES\n"
        resultado += "=" * 70 + "\n\n"
        resultado += f"V1 = ({self.v1_x:.6f}, {self.v1_y:.6f})\n"
        resultado += f"V2 = ({self.v2_x:.6f}, {self.v2_y:.6f})\n\n"
        resultado += f"|V1| = {mag1:.6f}\n"
        resultado += f"|V2| = {mag2:.6f}\n"
        resultado += f"V1 · V2 = {prod_punto:.6f}\n\n"
        resultado += f"cos(θ) = (V1 · V2) / (|V1| × |V2|)\n"
        resultado += f"cos(θ) = {prod_punto:.6f} / ({mag1:.6f} × {mag2:.6f})\n"
        resultado += f"cos(θ) = {cos_ang:.6f}\n\n"
        resultado += f"θ = arccos({cos_ang:.6f})\n"
        resultado += f"θ = {angulo_rad:.6f} radianes\n"
        resultado += f"θ = {angulo_deg:.4f}°\n"
        
        self.mostrar_resultado_vectores(resultado)
    
    def producto_cruz(self):
        """Calcula el producto cruz (en 3D con z=0)"""
        if not hasattr(self, 'v1_x'):
            messagebox.showerror("Error", "Primero debe procesar los vectores")
            return
        
        # Extender a 3D con z=0
        v1_3d = np.array([self.v1_x, self.v1_y, 0])
        v2_3d = np.array([self.v2_x, self.v2_y, 0])
        
        # Producto cruz
        prod_cruz = np.cross(v1_3d, v2_3d)
        
        resultado = "\n"
        resultado += "PRODUCTO CRUZ\n"
        resultado += "=" * 70 + "\n\n"
        resultado += f"V1 = ({self.v1_x:.6f}, {self.v1_y:.6f}, 0)\n"
        resultado += f"V2 = ({self.v2_x:.6f}, {self.v2_y:.6f}, 0)\n\n"
        resultado += f"V1 × V2 = (V1y×V2z - V1z×V2y, V1z×V2x - V1x×V2z, V1x×V2y - V1y×V2x)\n"
        resultado += f"V1 × V2 = ({self.v1_y:.6f}×0 - 0×{self.v2_y:.6f}, 0×{self.v2_x:.6f} - {self.v1_x:.6f}×0, {self.v1_x:.6f}×{self.v2_y:.6f} - {self.v1_y:.6f}×{self.v2_x:.6f})\n"
        resultado += f"V1 × V2 = ({prod_cruz[0]:.6f}, {prod_cruz[1]:.6f}, {prod_cruz[2]:.6f})\n\n"
        resultado += f"Magnitud del producto cruz: |V1 × V2| = {np.linalg.norm(prod_cruz):.6f}\n"
        
        self.mostrar_resultado_vectores(resultado)
    
    def graficar_vectores(self):
        """Grafica los vectores en una nueva ventana"""
        if not hasattr(self, 'v1_x'):
            messagebox.showerror("Error", "Primero debe procesar los vectores")
            return
        
        # Crear ventana gráfica
        ventana_grafica = tk.Toplevel(self.root)
        ventana_grafica.title("Gráfica de Vectores")
        ventana_grafica.geometry("600x600")
        
        # Crear figura
        fig = Figure(figsize=(6, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        # Configurar el gráfico
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Gráfica de Vectores')
        
        # Graficar Vector 1
        ax.arrow(0, 0, self.v1_x, self.v1_y, head_width=0.5, head_length=0.5, 
                fc='blue', ec='blue', linewidth=2, label=f'V1 ({self.v1_mag_orig:.2f}, {self.v1_ang_orig:.2f}°)')
        
        # Graficar Vector 2
        ax.arrow(0, 0, self.v2_x, self.v2_y, head_width=0.5, head_length=0.5, 
                fc='red', ec='red', linewidth=2, label=f'V2 ({self.v2_mag_orig:.2f}, {self.v2_ang_orig:.2f}°)')
        
        # Graficar suma de vectores
        suma_x = self.v1_x + self.v2_x
        suma_y = self.v1_y + self.v2_y
        ax.arrow(0, 0, suma_x, suma_y, head_width=0.5, head_length=0.5, 
                fc='green', ec='green', linewidth=2, linestyle='--', label='V1 + V2')
        
        # Agradecer etiquetas
        ax.plot([self.v1_x], [self.v1_y], 'bo', markersize=6)
        ax.plot([self.v2_x], [self.v2_y], 'ro', markersize=6)
        ax.plot([suma_x], [suma_y], 'go', markersize=6)
        
        # Añadir leyenda
        ax.legend(loc='upper right')
        
        # Insertar gráfico en la ventana
        canvas = FigureCanvasTkAgg(fig, master=ventana_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def mostrar_resultado_vectores(self, texto):
        """Muestra el resultado en el área de texto"""
        self.resultado_vec_text.config(state=tk.NORMAL)
        self.resultado_vec_text.delete(1.0, tk.END)
        self.resultado_vec_text.insert(tk.END, texto)
        self.resultado_vec_text.config(state=tk.DISABLED)
    
    def ejemplo_vectores(self):
        """Carga un ejemplo de vectores"""
        self.v1_mag.delete(0, tk.END)
        self.v1_mag.insert(0, "10")
        self.v1_ang.delete(0, tk.END)
        self.v1_ang.insert(0, "30")
        
        self.v2_mag.delete(0, tk.END)
        self.v2_mag.insert(0, "15")
        self.v2_ang.delete(0, tk.END)
        self.v2_ang.insert(0, "120")
        
        # Procesar
        self.procesar_vectores()
        
        # Mostrar descripción
        resultado = "\n"
        resultado += "PROBLEMA DE EJEMPLO - VECTORES EN FÍSICA\n"
        resultado += "=" * 70 + "\n\n"
        resultado += "Dos fuerzas actúan sobre un objeto.\n"
        resultado += "Fuerza 1: Magnitud 10 N, Ángulo 30°\n"
        resultado += "Fuerza 2: Magnitud 15 N, Ángulo 120°\n\n"
        resultado += "Los vectores han sido cargados.\n"
        resultado += "Presione los botones para realizar operaciones.\n"
        resultado += "Presione 'Graficar Vectores' para visualizar.\n"
        
        self.mostrar_resultado_vectores(resultado)


def main():
    """Función principal"""
    root = tk.Tk()
    app = CalculadoraMatricesVectores(root)
    root.mainloop()


if __name__ == "__main__":
    main()
