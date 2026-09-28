import streamlit as st
from database import get_projects,get_products,get_documents,create_request,create_safety_event
st.set_page_config(page_title="SITIO PV Portal",page_icon="🛡️",layout="wide")
st.title("SITIO PV Portal"); st.caption("Demo Pharma Paraguay S.A. · Portal exclusivo del cliente")
page=st.sidebar.radio("Portal",["Inicio","Proyectos","＋ Nuevo proyecto","Medicamentos","Documentos","⚠ Reportar evento"])
try: projects=get_projects(); products=get_products()
except Exception as e:
 st.error("Backend no configurado todavía. Añada los Secrets de Supabase en Streamlit."); st.stop()
def card(p):
 st.subheader(p["title"]+(f' · {p["product"]}' if p.get("product") else ""))
 st.caption(p["code"]); st.progress((p.get("client_progress") or 0)/100,text=f'{p.get("client_progress") or 0}%')
 st.write("**Estado:**",p.get("client_status") or "En proceso"); st.write("**Siguiente paso:**",p.get("client_next_step") or "SITIO trabajando")
 if p.get("client_need"): st.warning("Necesitamos de usted: "+p["client_need"])
if page=="Inicio":
 st.success("🟢 Farmacovigilancia bajo gestión por SITIO")
 a,b,c=st.columns(3); a.metric("Proyectos",len(projects)); b.metric("Medicamentos",len(products)); c.metric("Acciones suyas",sum(bool(x.get("client_need")) for x in projects))
 for p in projects: card(p)
elif page=="Proyectos":
 for p in projects: card(p)
elif page=="＋ Nuevo proyecto":
 st.header("Solicitar nuevo proyecto"); typ=st.selectbox("¿Qué necesita?",["Poner/mantener BPFV en regla","Incorporar un medicamento","PSUR / PGR / documento de seguridad","Estudio post-autorización","Capacitación","No sé qué necesito"])
 prod=st.text_input("Medicamento (si aplica)"); detail=st.text_area("Cuéntenos brevemente qué necesita")
 if st.button("Enviar a SITIO",type="primary"):
  create_request(typ,prod,detail); st.success("Solicitud enviada a SITIO."); st.rerun()
elif page=="Medicamentos":
 st.dataframe([{"Medicamento":x["name"],"Registro":x.get("registration"),"Estado PV":x.get("pv_status"),"Próximo hito":x.get("next_milestone")} for x in products],use_container_width=True,hide_index=True)
elif page=="Documentos":
 docs=get_documents(); st.dataframe([{"Documento":x["name"],"Proyecto":x.get("project_code"),"Estado":x.get("status")} for x in docs],use_container_width=True,hide_index=True); st.caption("Solo documentos marcados CLIENT son visibles aquí.")
else:
 st.header("Reportar un posible evento"); st.write("No necesita decidir si es una reacción adversa. Envíenos lo recibido y SITIO lo evalúa.")
 prod=st.selectbox("Medicamento",[x["name"] for x in products]+["Otro"]); detail=st.text_area("Pegue el mensaje o describa lo ocurrido")
 if st.button("Enviar a SITIO",type="primary"):
  if not detail.strip(): st.warning("Incluya alguna información.")
  else: create_safety_event(prod,detail); st.success("Recibido por SITIO.")
