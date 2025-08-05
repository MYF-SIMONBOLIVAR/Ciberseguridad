import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pytz
import time  
import base64
from dotenv import load_dotenv
import os

# Carga las variables del archivo .env
load_dotenv() 

#configuracion del remitente, las variables de entorno estan definidas en el archivo .env
sender_email = os.getenv('SENDER_EMAIL')
password = os.getenv('EMAIL_PASSWORD')
receiver_email = os.getenv('RECEIVER_EMAIL')

#envia correo de notificación
def enviar_notificacion_html(correo_persona, fecha_hora):
    subject ="Nuevo clic registrado"

#Cuerpo del mensaje 
    body = f"""
    <html>
    <body>
        <h3>Nuevo clic detectado</h3>
        <p><strong>Correo:</strong> {correo_persona}</p>
        <p><strong>Fecha:</strong> {fecha_hora}</p>
    </body>
    </html>
    """
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        
    except Exception as e:
        st.error(f"Error al enviar correo: {e}")

# Captura el parámetro 'correo' de la URL
query_params = st.query_params
correo = query_params.get("correo", "")

# Configuración de la zona horaria
zona_colombia = pytz.timezone('America/Bogota')
fecha_hora = datetime.now(zona_colombia).strftime("%Y-%m-%d %H:%M:%S")

# Guarda los clics en memoria
if "clics" not in st.session_state:
    st.session_state.clics = []

# Configuración de la página
st.markdown(
    "<h1 style='text-align:center; color:#19277f;'>¡Atención!</h1>"
    "<h2 style='text-align:center; color:#d9534f;'>¡No abras enlaces sospechosos!</h2>",
    
    unsafe_allow_html=True
)

# Función para cargar y mostrar imagen como HTML
def mostrar_imagen(path, caption=""):
    with open(path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
        html = f"""
        <div style="text-align: center;">
            <img src="data:image/jpeg;base64,{encoded}" style="width:70%; height:auto; border-radius:10px;" />
            <p style="font-weight:bold;">{caption}</p>
        </div>
        """
        return html

imagen_placeholder = st.empty()
html_img = mostrar_imagen("Campaña.png")
imagen_placeholder.markdown(html_img, unsafe_allow_html=True)

# Espera para simular carga de imagen
time.sleep(7)

imagen_placeholder.empty()

# Muestra el mensaje de alerta
if correo:
# Guarda el clic
    st.session_state.clics.append(f"{fecha_hora} - {correo}")
# Enviar notificación
    enviar_notificacion_html(correo, fecha_hora)
  
# Mensaje de campaña 
st.write(f"Acabas de hacer clic en un enlace que formaba parte de una prueba de concientización sobre seguridad digital,Este ejercicio fue diseñado por el Departamento de Tecnología para identificar posibles riesgos de seguridad y fortalecer nuestra cultura de ciberseguridad.")
st.write("Recuerda: nunca hagas clic en enlaces sospechosos o no verificados, ya que esto puede comprometer tu información personal y la seguridad de toda la empresa. Si tienes dudas sobre la legitimidad de un correo, comunícate de inmediato con el Departamento de TI.")
st.write("Lee la siguiente información para más detalles y realiza el cuestionario. Recuerda que la seguridad de la empresa depende de todos nosotros.")

# Muestra enlace al PDF
st.write("### Información de Ciberseguridad")

# Cargar y mostrar el PDF 
# Muestra botón para descargar el PDF en vez de abrir en otra pestaña
with open("Correo_Sospechoso_Empresa_Segura.pdf", "rb") as f:
    st.download_button(
        label="Descargar PDF de Ciberseguridad",
        data=f,
        file_name="Correo_Sospechoso_Empresa_Segura.pdf",
        mime="application/pdf")
        


# Línea final decorativa
st.markdown("<hr style='border: none; height: 4px; background-color: #fab70e;'>", unsafe_allow_html=True)

# Logo y pie de página
col1, col2, col3 = st.columns([3, 1, 3])  
with col2:
    st.image("logo.png", width=200)

st.markdown("""
    <div style="text-align: center; margin-top: 20px; color: #19277f;">
        <p>© 2025 Muelles y Frenos Simón Bolívar. Todos los derechos reservados.</p>
    </div>

""", unsafe_allow_html=True)


