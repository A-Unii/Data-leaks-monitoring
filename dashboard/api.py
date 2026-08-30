import requests
import streamlit as st


API_URL = st.secrets["API_URL"].rstrip("/")


def get_alerts():
    response = requests.get(f"{API_URL}/alerts", timeout=10)
    response.raise_for_status()
    return response.json()


def get_companies():
    response = requests.get(f"{API_URL}/companies", timeout=10)
    response.raise_for_status()
    return response.json()


def create_company(company):
    response = requests.post(
        f"{API_URL}/companies",
        json=company,
        timeout=10
    )
    response.raise_for_status()
    return response.json()