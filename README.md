# SITIO PV Client Portal

Portal Streamlit exclusivo para clientes de SITIO BioMedical Solutions.

## Demo
```bash
pip install -r requirements.txt
streamlit run app.py
```

Esta versión usa exclusivamente datos ficticios y estado de sesión. No introducir datos reales de pacientes.

## Diseño de seguridad
Este repositorio contiene únicamente la interfaz cliente. No contiene pantallas, notas, costes ni lógica interna de SITIO. La versión conectada usará credenciales limitadas y aislamiento por tenant en el backend.

## Siguiente fase
Conectar a un backend compartido (PostgreSQL/Supabase), autenticación real, storage privado y políticas RLS por cliente.
