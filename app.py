import streamlit as st
import openai
import datetime

# Configurar la API de OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Configurar la página de Streamlit
st.set_page_config(page_title="Health AI", page_icon="💡", layout="centered")

# Estilos CSS para mejorar la apariencia
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        .title {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            color: #ffcc00;
        }
        .subtitle {
            font-size: 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        .footer {
            font-size: 12px;
            text-align: center;
            margin-top: 50px;
            color: #aaaaaa;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown('<div class="title">Health AI - Asistente Inteligente</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Tu asistente para recordatorios de salud y generación de imágenes con IA</div>', unsafe_allow_html=True)

# Sección "Cómo funciona"
st.subheader("¿Cómo funciona?")
st.write("""
1. Ingrese una tarea de salud en el cuadro de texto.
2. Presione el botón 'Generar Recordatorio'.
3. La IA generará un recordatorio personalizado para su tarea.
4. Puede generar una imagen basada en texto con la IA.
5. Revise la lista de recordatorios generados para ver su historial.
""")

# Función para generar recordatorios con ChatGPT
def generar_recordatorio(tarea):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un asistente que genera recordatorios de salud amigables y útiles."},
                {"role": "user", "content": f"Genera un recordatorio amigable para la siguiente tarea de salud: {tarea}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al generar el recordatorio: {str(e)}"

# Entrada del usuario para recordatorios
tarea = st.text_input("Escriba una tarea de salud (Ej: Tomar medicación a las 9 AM)")
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if st.button("Generar Recordatorio"):
    if tarea:
        recordatorio = generar_recordatorio(tarea)
        st.session_state.tasks.append({
            "tarea": tarea,
            "recordatorio": recordatorio,
            "hora": datetime.datetime.now().strftime("%H:%M")
        })
        st.success("Recordatorio generado con éxito!")
    else:
        st.warning("Por favor, ingrese una tarea válida.")

# Mostrar lista de recordatorios generados
st.subheader("Recordatorios Generados")
for task in st.session_state.tasks:
    st.markdown(f"**{task['tarea']}** - {task['recordatorio']} ({task['hora']})")

# Función para generar una imagen con DALL·E
def generar_imagen(descripcion):
    try:
        response = openai.images.generate(
            model="dall-e-3",  # Usa DALL-E 3 en lugar de DALL-E 2
            prompt=descripcion,
            n=1,  # Generar una única imagen
            size="1024x1024"
        )

        # Debugging: Mostrar la respuesta de OpenAI en la app
        st.write("Respuesta de OpenAI:", response)

        # Verificar si se generó correctamente la imagen
        if response.data and len(response.data) > 0:
            return response.data[0].url
        else:
            return None
    except Exception as e:
        st.error(f"Error al generar la imagen: {e}")
        return None

# Interfaz de usuario en Streamlit
st.subheader("Generador de Imágenes con IA (DALL·E)")

descripcion = st.text_input("Describe la imagen que quieres generar (Ej: Un médico robot con un estetoscopio)")

if st.button("Generar Imagen"):
    if descripcion:
        try:
            # Llamar a la API de OpenAI para generar la imagen
            response = generar_imagen(descripcion)  

            if response and "data" in response:
                # Extraer la URL de la imagen generada
                imagen_url = response["data"][0]["url"]
                
                # Mostrar la imagen en Streamlit
                st.image(imagen_url, caption="Imagen generada por DALL·E", use_container_width=True)
            else:
                st.error("No se pudo generar la imagen. Intenta con otra descripción.")

        except Exception as e:
            st.error(f"Error al generar la imagen: {e}")
    else:
        st.warning("Por favor, ingresa una descripción antes de generar la imagen.")
# Footer
st.markdown('<div class="footer">Desarrollado con ❤️ por IA - 2024</div>', unsafe_allow_html=True)
