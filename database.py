import streamlit as st
from supabase import create_client

@st.cache_resource
def db():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_ANON_KEY"])

def client_slug():
    return st.secrets.get("CLIENT_SLUG","demo-pharma")

def get_projects():
    return db().table("client_projects").select("*").eq("client_slug",client_slug()).order("created_at",desc=True).execute().data or []

def get_products():
    return db().table("client_products").select("*").eq("client_slug",client_slug()).execute().data or []

def create_request(kind, product, detail):
    return db().table("client_requests").insert({"client_slug":client_slug(),"kind":kind,"product":product or None,"detail":detail,"status":"Nueva"}).execute()

def create_safety_event(product, detail):
    return db().table("client_safety_intake").insert({"client_slug":client_slug(),"product":product,"detail":detail,"status":"Recibido"}).execute()

def get_documents():
    return db().table("client_documents").select("*").eq("client_slug",client_slug()).execute().data or []
