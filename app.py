import streamlit as st
from graphviz import Digraph

# Configuración inicial
st.set_page_config(page_title="Simulador WWII: Árbol de Decisiones", layout="wide")
st.title("🇩🇪 Simulador de Decisiones: Alemania en la WWII")
st.markdown("---")

# Datos del árbol
data = {
    'decisiones': [
        'Invasión_Polonia', 'Batalla_Inglaterra', 'Operación_Barbarroja',
        'Declarar_Guerra_EEUU', 'Stalingrado', 'Normandía', 'Ardenas'
    ],
    'opciones': [
        ['Sí', 'No'],
        ['Fracaso', 'Éxito'],
        ['Sí', 'No'],
        ['Sí', 'No'],
        ['Derrota', 'Victoria'],
        ['Sí', 'No'],
        ['Fracaso', 'Éxito']
    ],
    'consecuencias': {
        ('Invasión_Polonia', 'Sí'): 'Frente Occidental abierto',
        ('Invasión_Polonia', 'No'): 'Neutralidad temporal',
        ('Batalla_Inglaterra', 'Fracaso'): 'UK resiste',
        ('Batalla_Inglaterra', 'Éxito'): 'Posible invasión a UK',
        ('Operación_Barbarroja', 'Sí'): 'Desgaste en el Este',
        ('Operación_Barbarroja', 'No'): 'Sin Frente Oriental',
        ('Declarar_Guerra_EEUU', 'Sí'): 'EEUU entra en guerra',
        ('Declarar_Guerra_EEUU', 'No'): 'EEUU solo en Pacífico',
        ('Stalingrado', 'Derrota'): 'Pérdida de 300k soldados',
        ('Stalingrado', 'Victoria'): 'Control del Volga',
        ('Normandía', 'Sí'): 'Aliados avanzan',
        ('Normandía', 'No'): 'Muro Atlántico resiste',
        ('Ardenas', 'Fracaso'): 'Últimos recursos perdidos',
        ('Ardenas', 'Éxito'): 'Aliados retroceden'
    },
    'resultados': {
        ('Sí', 'Fracaso', 'Sí', 'Sí', 'Derrota', 'Sí', 'Fracaso'): '💥 DERROTA Total (Escenario histórico)',
        ('No', 'Éxito', 'No', 'No', 'Victoria', 'No', 'Éxito'): '🎖️ VICTORIA Hipótetica',
        ('Sí', 'Fracaso', 'No', 'No', 'Victoria', 'No', 'Éxito'): '⚖️ Resultado Incierto'
    }
}

# Sidebar con controles
with st.sidebar:
    st.header("🔘 Opciones")
    decisiones_usuario = {}
    for i, dec in enumerate(data['decisiones']):
        decisiones_usuario[dec] = st.radio(
            f"{dec}:",
            options=data['opciones'][i],
            key=dec
        )
    
    if st.button("Calcular Ruta"):
        st.session_state['decisiones'] = decisiones_usuario

# Mostrar resultados y árbol
if 'decisiones' in st.session_state:
    decisiones = st.session_state['decisiones']
    
    # Mostrar consecuencias
    st.subheader("📜 Consecuencias de tus Decisiones")
    for dec, opcion in decisiones.items():
        st.write(f"- **{dec}**: {opcion} → {data['consecuencias'][(dec, opcion)]}")
    
    # Calcular resultado final
    resultado_key = tuple(decisiones.values())
    resultado = data['resultados'].get(resultado_key, '🔍 Resultado No Definido')
    st.markdown(f"### 🏁 **Resultado Final:** {resultado}")
    
    # Generar árbol gráfico
    st.subheader("🌳 Árbol de Decisiones")
    dot = Digraph(comment='Árbol de Decisiones WWII')
    dot.attr('node', shape='box', style='filled', fillcolor='lightgrey')
    dot.attr('edge', color='black')
    
    # Nodo raíz
    dot.node('Raíz', 'Alemania WWII')
    
    # Añadir nodos según decisiones
    prev_node = 'Raíz'
    for dec, opcion in decisiones.items():
        node_id = f"{dec}_{opcion}"
        dot.node(node_id, f"{dec}\nOpción: {opcion}\nConsecuencia: {data['consecuencias'][(dec, opcion)]}")
        dot.edge(prev_node, node_id)
        prev_node = node_id
    
    # Resultado final
    dot.node('Resultado', f"FIN: {resultado}", fillcolor='lightblue' if 'VICTORIA' in resultado else 'salmon')
    dot.edge(prev_node, 'Resultado')
    
    # Mostrar el árbol
    st.graphviz_chart(dot)
else:
    st.info("⏳ Selecciona tus decisiones y haz clic en **Calcular Ruta**.")

# Instrucciones
st.markdown("---")
st.markdown("""
### 📌 Instrucciones:
1. Usa el **panel izquierdo** para seleccionar opciones.
2. Haz clic en **Calcular Ruta** para ver el árbol.
3. Explora cómo cambia el resultado final.
""")