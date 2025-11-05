import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Álgebra Lineal",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Título principal
st.title("🧮 Calculadora de Matrices, Sistemas Lineales y Vectores")
st.markdown("---")

# Crear tabs
tab1, tab2, tab3 = st.tabs(["📊 Matrices", "🔢 Sistemas Lineales", "➡️ Vectores"])

# ============================================================================
# SECCIÓN 1: MATRICES
# ============================================================================

with tab1:
    st.header("Operaciones con Matrices")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dimensiones Matriz 1")
        m1_filas = st.number_input("Filas Matriz 1:", min_value=1, max_value=10, value=2, key="m1_filas")
        m1_columnas = st.number_input("Columnas Matriz 1:", min_value=1, max_value=10, value=2, key="m1_columnas")
    
    with col2:
        st.subheader("Dimensiones Matriz 2")
        m2_filas = st.number_input("Filas Matriz 2:", min_value=1, max_value=10, value=2, key="m2_filas")
        m2_columnas = st.number_input("Columnas Matriz 2:", min_value=1, max_value=10, value=2, key="m2_columnas")
    
    st.markdown("---")
    
    # Input de matrices
    st.subheader("Ingrese los elementos de las matrices")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Matriz 1 ({int(m1_filas)}x{int(m1_columnas)})**")
        matriz1_data = []
        for i in range(int(m1_filas)):
            fila = st.columns(int(m1_columnas))
            fila_data = []
            for j in range(int(m1_columnas)):
                val = fila[j].number_input(f"M1[{i+1},{j+1}]", value=1.0, key=f"m1_{i}_{j}")
                fila_data.append(val)
            matriz1_data.append(fila_data)
        matriz1 = np.array(matriz1_data)
    
    with col2:
        st.write(f"**Matriz 2 ({int(m2_filas)}x{int(m2_columnas)})**")
        matriz2_data = []
        for i in range(int(m2_filas)):
            fila = st.columns(int(m2_columnas))
            fila_data = []
            for j in range(int(m2_columnas)):
                val = fila[j].number_input(f"M2[{i+1},{j+1}]", value=1.0, key=f"m2_{i}_{j}")
                fila_data.append(val)
            matriz2_data.append(fila_data)
        matriz2 = np.array(matriz2_data)
    
    st.markdown("---")
    
    # Operaciones
    st.subheader("Operaciones")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Sumar Matrices", key="btn_suma_mat"):
            if matriz1.shape == matriz2.shape:
                resultado = matriz1 + matriz2
                st.success("✅ Suma de Matrices")
                st.write("**Resultado:**")
                st.dataframe(pd.DataFrame(resultado, columns=[f"Col {i+1}" for i in range(resultado.shape[1])]))
            else:
                st.error("❌ las matrices no se pueden sumar (dimensiones diferentes)")
    
    with col2:
        if st.button("✖️ Multiplicar Matrices", key="btn_mult_mat"):
            if matriz1.shape[1] == matriz2.shape[0]:
                resultado = np.dot(matriz1, matriz2)
                st.success("✅ Multiplicación de Matrices")
                st.write("**Resultado:**")
                st.dataframe(pd.DataFrame(resultado, columns=[f"Col {i+1}" for i in range(resultado.shape[1])]))
            else:
                st.error("❌ las matrices no se pueden multiplicar (columnas M1 ≠ filas M2)")
    
    with col3:
        if st.button("📋 Cargar Ejemplo", key="btn_ej_mat"):
            st.session_state['ej_mat'] = True
    
    if 'ej_mat' in st.session_state and st.session_state['ej_mat']:
        st.info("""
        **EJEMPLO - Matrices de Ventas**
        
        Una empresa tiene dos centros de distribución.
        - Matriz A: Ventas en Enero
        - Matriz B: Ventas en Febrero
        """)
        
        ej_m1 = np.array([[100, 150], [200, 120], [80, 90]])
        ej_m2 = np.array([[120, 160], [180, 140], [100, 110]])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**Enero**")
            st.dataframe(ej_m1)
        with col2:
            st.write("**Febrero**")
            st.dataframe(ej_m2)
        with col3:
            st.write("**Total**")
            st.dataframe(ej_m1 + ej_m2)

# ============================================================================
# SECCIÓN 2: SISTEMAS LINEALES
# ============================================================================

with tab2:
    st.header("Solución de Sistemas de Ecuaciones Lineales")
    
    dim = st.slider("Dimensión del sistema (N×N):", min_value=2, max_value=5, value=3)
    
    st.markdown("---")
    
    # Matriz A
    st.subheader(f"Matriz de Coeficientes A ({dim}x{dim})")
    matriz_a = []
    for i in range(dim):
        fila = st.columns(dim)
        fila_data = []
        for j in range(dim):
            val = fila[j].number_input(f"A[{i+1},{j+1}]", value=1.0, key=f"a_{i}_{j}")
            fila_data.append(val)
        matriz_a.append(fila_data)
    matriz_a = np.array(matriz_a)
    
    st.markdown("---")
    
    # Vector b
    st.subheader(f"Vector de Términos Independientes b")
    vector_b = []
    cols = st.columns(dim)
    for i in range(dim):
        val = cols[i].number_input(f"b[{i+1}]", value=1.0, key=f"b_{i}")
        vector_b.append(val)
    vector_b = np.array(vector_b)
    
    st.markdown("---")
    
    # Resolver
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Resolver con Cramer", key="btn_cramer"):
            det_a = np.linalg.det(matriz_a)
            
            if abs(det_a) < 1e-10:
                st.error("❌ El sistema de ecuaciones no tiene solución |A| = 0")
            else:
                st.success("✅ Solución por Método de Cramer")
                
                with st.expander("Mostrar pasos detallados"):
                    st.write(f"**Determinante de A:** |A| = {det_a:.6f}")
                    
                    solucion = []
                    for i in range(dim):
                        a_i = matriz_a.copy()
                        a_i[:, i] = vector_b
                        det_a_i = np.linalg.det(a_i)
                        
                        var_name = chr(120 + i)
                        x_val = det_a_i / det_a
                        solucion.append(x_val)
                        
                        st.write(f"**{var_name} = |A{var_name}| / |A| = {det_a_i:.6f} / {det_a:.6f} = {x_val:.6f}**")
                
                st.write("**SOLUCIÓN:**")
                sol_dict = {}
                for i, val in enumerate(solucion):
                    var_name = chr(120 + i)
                    sol_dict[var_name] = val
                st.json(sol_dict)
    
    with col2:
        if st.button("🔄 Resolver con Matriz Inversa", key="btn_inversa"):
            det_a = np.linalg.det(matriz_a)
            
            if abs(det_a) < 1e-10:
                st.error("❌ El sistema de ecuaciones no tiene solución |A| = 0 y la matriz A no tiene inversa")
            else:
                st.success("✅ Solución por Método de Matriz Inversa")
                
                a_inv = np.linalg.inv(matriz_a)
                solucion = np.dot(a_inv, vector_b)
                
                with st.expander("Mostrar pasos detallados"):
                    st.write("**Matriz Inversa A^(-1):**")
                    st.dataframe(pd.DataFrame(a_inv))
                
                st.write("**SOLUCIÓN:**")
                sol_dict = {}
                for i, val in enumerate(solucion):
                    var_name = chr(120 + i)
                    sol_dict[var_name] = val
                st.json(sol_dict)
    
    with col3:
        if st.button("📋 Cargar Ejemplo", key="btn_ej_sist"):
            st.session_state['ej_sist'] = True
    
    if 'ej_sist' in st.session_state and st.session_state['ej_sist']:
        st.info("""
        **EJEMPLO - Sistema 3×3**
        
        2x + y - z = 8
        -3x - y + 2z = -11
        -2x + y + 2z = -3
        
        **Solución:** x = 2, y = 3, z = -1
        """)

# ============================================================================
# SECCIÓN 3: VECTORES
# ============================================================================

with tab3:
    st.header("Operaciones con Vectores")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Vector 1")
        v1_mag = st.number_input("Magnitud V1:", min_value=0.1, value=10.0, key="v1_mag")
        v1_ang = st.number_input("Ángulo V1 (grados):", min_value=0.0, max_value=360.0, value=30.0, key="v1_ang")
    
    with col2:
        st.subheader("Vector 2")
        v2_mag = st.number_input("Magnitud V2:", min_value=0.1, value=15.0, key="v2_mag")
        v2_ang = st.number_input("Ángulo V2 (grados):", min_value=0.0, max_value=360.0, value=120.0, key="v2_ang")
    
    st.markdown("---")
    
    # Convertir a componentes
    v1_ang_rad = math.radians(v1_ang)
    v2_ang_rad = math.radians(v2_ang)
    
    v1_x = v1_mag * math.cos(v1_ang_rad)
    v1_y = v1_mag * math.sin(v1_ang_rad)
    v2_x = v2_mag * math.cos(v2_ang_rad)
    v2_y = v2_mag * math.sin(v2_ang_rad)
    
    # Operaciones
    st.subheader("Operaciones Vectoriales")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("📐 Componentes", key="btn_comp"):
            st.session_state['op_comp'] = True
    
    with col2:
        if st.button("➕ Suma", key="btn_suma_vec"):
            st.session_state['op_suma'] = True
    
    with col3:
        if st.button("🔵 Prod. Punto", key="btn_punto"):
            st.session_state['op_punto'] = True
    
    with col4:
        if st.button("📏 Ángulo", key="btn_angulo"):
            st.session_state['op_angulo'] = True
    
    with col5:
        if st.button("✖️ Prod. Cruz", key="btn_cruz"):
            st.session_state['op_cruz'] = True
    
    with col6:
        if st.button("📈 Graficar", key="btn_graficar"):
            st.session_state['op_graficar'] = True
    
    st.markdown("---")
    
    # Mostrar resultados
    if 'op_comp' in st.session_state and st.session_state['op_comp']:
        st.success("📐 Componentes Rectangulares")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Vector 1:** V1 = ({v1_x:.6f}, {v1_y:.6f})")
        with col2:
            st.write(f"**Vector 2:** V2 = ({v2_x:.6f}, {v2_y:.6f})")
    
    if 'op_suma' in st.session_state and st.session_state['op_suma']:
        suma_x = v1_x + v2_x
        suma_y = v1_y + v2_y
        magnitud_suma = math.sqrt(suma_x**2 + suma_y**2)
        angulo_suma = math.degrees(math.atan2(suma_y, suma_x))
        
        st.success("➕ Suma de Vectores")
        st.write(f"**V_suma = ({suma_x:.6f}, {suma_y:.6f})**")
        st.write(f"**Magnitud:** |V_suma| = {magnitud_suma:.6f}")
        st.write(f"**Ángulo:** θ = {angulo_suma:.4f}°")
    
    if 'op_punto' in st.session_state and st.session_state['op_punto']:
        prod_punto = v1_x * v2_x + v1_y * v2_y
        st.success("🔵 Producto Punto")
        st.write(f"**V1 · V2 = {prod_punto:.6f}**")
    
    if 'op_angulo' in st.session_state and st.session_state['op_angulo']:
        prod_punto = v1_x * v2_x + v1_y * v2_y
        mag1 = math.sqrt(v1_x**2 + v1_y**2)
        mag2 = math.sqrt(v2_x**2 + v2_y**2)
        cos_ang = prod_punto / (mag1 * mag2)
        cos_ang = max(-1, min(1, cos_ang))
        angulo_rad = math.acos(cos_ang)
        angulo_deg = math.degrees(angulo_rad)
        
        st.success("📏 Ángulo entre Vectores")
        st.write(f"**θ = {angulo_deg:.4f}°**")
        st.write(f"**θ = {angulo_rad:.6f} radianes**")
    
    if 'op_cruz' in st.session_state and st.session_state['op_cruz']:
        v1_3d = np.array([v1_x, v1_y, 0])
        v2_3d = np.array([v2_x, v2_y, 0])
        prod_cruz = np.cross(v1_3d, v2_3d)
        
        st.success("✖️ Producto Cruz")
        st.write(f"**V1 × V2 = ({prod_cruz[0]:.6f}, {prod_cruz[1]:.6f}, {prod_cruz[2]:.6f})**")
        st.write(f"**Magnitud:** |V1 × V2| = {np.linalg.norm(prod_cruz):.6f}")
    
    if 'op_graficar' in st.session_state and st.session_state['op_graficar']:
        st.success("📈 Gráfica de Vectores")
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Límites
        max_val = max(abs(v1_x), abs(v1_y), abs(v2_x), abs(v2_y), abs(v1_x + v2_x), abs(v1_y + v2_y)) + 2
        ax.set_xlim(-max_val, max_val)
        ax.set_ylim(-max_val, max_val)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)
        
        # Vectores
        ax.arrow(0, 0, v1_x, v1_y, head_width=0.5, head_length=0.5, fc='blue', ec='blue', linewidth=2, label=f'V1')
        ax.arrow(0, 0, v2_x, v2_y, head_width=0.5, head_length=0.5, fc='red', ec='red', linewidth=2, label=f'V2')
        
        suma_x = v1_x + v2_x
        suma_y = v1_y + v2_y
        ax.arrow(0, 0, suma_x, suma_y, head_width=0.5, head_length=0.5, fc='green', ec='green', linewidth=2, linestyle='--', label='V1 + V2')
        
        # Puntos
        ax.plot([v1_x], [v1_y], 'bo', markersize=8)
        ax.plot([v2_x], [v2_y], 'ro', markersize=8)
        ax.plot([suma_x], [suma_y], 'go', markersize=8)
        
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_title('Gráfica de Vectores', fontsize=14)
        ax.legend(loc='upper right', fontsize=10)
        
        st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center">
    <p>🧮 Calculadora de Álgebra Lineal | Proyecto: Ecuaciones Diferenciales</p>
    <p><a href="https://github.com/JhonRamirez22/CALCULADORA-ALGEBRALINEAL" target="_blank">GitHub Repository</a></p>
    </div>
    """, unsafe_allow_html=True)

import pandas as pd
