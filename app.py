import streamlit as st
from datetime import datetime

st.set_page_config(page_title="SITIO PV Portal", page_icon="🛡️", layout="wide")

st.markdown("""<style>
.block-container{max-width:1050px;padding-top:2rem}
div[data-testid="stMetric"]{background:#f7f8fa;border:1px solid #e7e9ee;padding:14px;border-radius:12px}
.status{padding:20px;border-radius:14px;background:#edf9f1;border:1px solid #b9e3c6;margin-bottom:18px}
.card{padding:18px;border:1px solid #e5e7eb;border-radius:14px;margin:10px 0;background:white}
.small{color:#667085;font-size:.9rem}
</style>""", unsafe_allow_html=True)

if "requests" not in st.session_state: st.session_state.requests=[]
if "events" not in st.session_state: st.session_state.events=[]

st.title("SITIO PV Portal")
st.caption("Demo Pharma Paraguay S.A. · Farmacovigilancia gestionada por SITIO")

page=st.sidebar.radio("Portal",["Inicio","Proyectos","＋ Nuevo proyecto","Medicamentos","Documentos","⚠ Reportar evento"])
st.sidebar.caption("Portal exclusivo del cliente · DEMO")

projects=[
 {"id":"PV-2026-018","name":"Implementación BPFV","progress":82,"status":"SITIO trabajando","next":"Preparación de presentación ante DINAVISA","need":None},
 {"id":"PV-2026-021","name":"PGR · GLUCOX 5 mg","progress":54,"status":"Acción requerida","next":"Completar documentación del producto","need":"Subir información de seguridad vigente"},
]

def project_card(p):
    st.markdown(f'<div class="card"><b>{p["name"]}</b><br><span class="small">{p["id"]}</span></div>',unsafe_allow_html=True)
    st.progress(p["progress"]/100,text=f'{p["progress"]}% completado')
    st.write("**Estado:**",p["status"])
    st.write("**Siguiente paso:**",p["next"])
    if p["need"]: st.warning("Necesitamos de usted: "+p["need"])

if page=="Inicio":
    st.markdown('<div class="status"><h3>🟢 Farmacovigilancia bajo gestión</h3>SITIO está gestionando sus actividades. Solo le avisaremos cuando necesitemos algo de usted.</div>',unsafe_allow_html=True)
    a,b,c=st.columns(3); a.metric("Proyectos activos",len(projects)); b.metric("Medicamentos",3); c.metric("Acciones suyas",1)
    st.subheader("Sus proyectos")
    for p in projects: project_card(p)
    st.subheader("Necesitamos de usted")
    st.warning("PV-2026-021 · Subir información de seguridad vigente de GLUCOX 5 mg.")
elif page=="Proyectos":
    st.header("Proyectos")
    for p in projects: project_card(p)
    for r in st.session_state.requests:
        st.info(f'🆕 {r["type"]} · Solicitud recibida por SITIO · {r["created"]}')
elif page=="＋ Nuevo proyecto":
    st.header("Solicitar un nuevo proyecto")
    st.write("No necesita conocer el nombre regulatorio exacto. Díganos qué necesita y SITIO organiza el trabajo.")
    typ=st.selectbox("¿Qué necesita?",["Poner/mantener BPFV en regla","Incorporar un medicamento","PSUR / PGR / documento de seguridad","Estudio post-autorización","Capacitación","No sé qué necesito"])
    product=st.text_input("Medicamento (si aplica)")
    detail=st.text_area("Cuéntenos brevemente qué necesita")
    up=st.file_uploader("Adjuntar documento (opcional)")
    if st.button("Enviar a SITIO",type="primary"):
        st.session_state.requests.append({"type":typ,"product":product,"detail":detail,"created":datetime.now().strftime("%d/%m/%Y %H:%M")})
        st.success("Solicitud recibida. SITIO la revisará y el avance aparecerá en este portal.")
elif page=="Medicamentos":
    st.header("Medicamentos bajo gestión")
    st.dataframe([{"Medicamento":"CARDIOMAX 10 mg","Registro":"DINAVISA DEMO-001","Estado PV":"🟢 Al día","Próximo hito":"Revisión anual"},{"Medicamento":"GLUCOX 5 mg","Registro":"DINAVISA DEMO-002","Estado PV":"🟠 Acción requerida","Próximo hito":"PGR"},{"Medicamento":"MED-X 100 mg","Registro":"DINAVISA DEMO-003","Estado PV":"🟢 Al día","Próximo hito":"Seguimiento"}],use_container_width=True,hide_index=True)
elif page=="Documentos":
    st.header("Sus documentos")
    st.dataframe([{"Documento":"Expediente BPFV","Proyecto":"PV-2026-018","Estado":"En preparación"},{"Documento":"PGR GLUCOX 5 mg","Proyecto":"PV-2026-021","Estado":"En preparación"},{"Documento":"Reporte mensual PV","Proyecto":"Mantenimiento","Estado":"Disponible"}],use_container_width=True,hide_index=True)
    st.caption("Aquí solo se muestran documentos destinados al cliente.")
else:
    st.header("Reportar un posible evento")
    st.write("No necesita decidir si es una reacción adversa. Envíenos lo que recibió y SITIO lo evaluará.")
    prod=st.selectbox("Medicamento",["CARDIOMAX 10 mg","GLUCOX 5 mg","MED-X 100 mg","Otro"])
    txt=st.text_area("Pegue aquí el WhatsApp, email o describa lo ocurrido")
    st.file_uploader("Adjuntar captura, PDF o documento")
    if st.button("Enviar a SITIO",type="primary"):
        st.session_state.events.append({"product":prod,"text":txt})
        st.success("Recibido. SITIO evaluará la información y le contactará solo si hace falta algo más.")
