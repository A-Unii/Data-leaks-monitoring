import streamlit as st

from api import get_alerts, get_companies, create_company


st.set_page_config(
    page_title="Data Leaks Monitoring",
    page_icon="🛡️",
    layout="wide"
)



# Header


st.title("Data Leaks Monitoring")
st.caption(
    "Monitorización en la nube de filtración de datos en la Deep Web"
)

st.divider()



# Nav Bar


if "page" not in st.session_state:
    st.session_state.page = "alerts"

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 ALERTAS", use_container_width=True):
        st.session_state.page = "alerts"

with col2:
    if st.button("🏢 EMPRESAS", use_container_width=True):
        st.session_state.page = "companies"

st.divider()



# Alertas (Alerts)


if st.session_state.page == "alerts":

    st.header("Alertas")

    try:
        alerts = get_alerts()
        companies = get_companies()

        # Filters
        col1, col2 = st.columns(2)

        with col1:
            company_filter = st.selectbox(
                "Empresa",
                ["Todas"] + [
                    company["company_id"]
                    for company in companies
                ]
            )

        with col2:
            severities = sorted({
                str(alert.get("severity", "")).upper()
                for alert in alerts
                if alert.get("severity")
            })

            severity_filter = st.selectbox(
                "Severidad",
                ["Todas"] + severities
            )

        # Apply filters
        filtered_alerts = alerts

        if company_filter != "Todas":
            filtered_alerts = [
                alert
                for alert in filtered_alerts
                if alert.get("company_id") == company_filter
            ]

        if severity_filter != "Todas":
            filtered_alerts = [
                alert
                for alert in filtered_alerts
                if str(alert.get("severity", "")).upper()
                == severity_filter
            ]

        st.write(f"**{len(filtered_alerts)} alertas**")

        # Alert list
        if not filtered_alerts:
            st.info("No hay alertas que coincidan con los filtros.")

        for alert in filtered_alerts:

            severity = str(
                alert.get("severity", "UNKNOWN")
            ).upper()

            company_id = alert.get(
                "company_id",
                "Empresa desconocida"
            )

            title = alert.get(
                "title",
                "Alerta detectada"
            )

            description = alert.get(
                "description",
                alert.get("text", "")
            )

            with st.container(border=True):

                st.subheader(
                    f"{severity} — {company_id}"
                )

                if title != "Alerta detectada":
                    st.write(f"**{title}**")

                st.write(description)

                if alert.get("alert_id"):
                    st.caption(
                        f"Alert ID: {alert['alert_id']}"
                    )

    except Exception as error:
        st.error(
            f"No se pudieron cargar las alertas: {error}"
        )



# Empresas (Companies)

else:

    st.header("Empresas")

    try:
        companies = get_companies()

        if not companies:
            st.info("No hay empresas registradas.")

        for company in companies:

            with st.container(border=True):

                st.subheader(
                    company.get(
                        "name",
                        company["company_id"]
                    )
                )

                st.write(
                    f"**Company ID:** "
                    f"{company['company_id']}"
                )

                st.write(
                    f"**Domains:** "
                    f"{', '.join(company.get('domains', []))}"
                )

        st.divider()

        st.subheader("➕ Dar de alta una empresa")

        with st.form("company_form"):

            company_id = st.text_input(
                "Company ID *"
            )

            domains = st.text_input(
                "Domains *",
                placeholder="ejemplo.es, ejemplo.com"
            )

            name = st.text_input("Nombre")

            emails = st.text_input(
                "Emails",
                placeholder="admin@ejemplo.es, user@ejemplo.es"
            )

            keywords = st.text_input(
                "Keywords",
                placeholder="keyword1, keyword2"
            )

            notification_email = st.text_input(
                "Email de notificaciones"
            )

            users = st.text_input(
                "Usuarios",
                placeholder="usuario1, usuario2"
            )

            submitted = st.form_submit_button(
                "Crear empresa"
            )

            if submitted:

                if not company_id or not domains:
                    st.error(
                        "Company ID y Domains son obligatorios."
                    )

                else:

                    company = {
                        "company_id": company_id,
                        "domains": [
                            item.strip()
                            for item in domains.split(",")
                            if item.strip()
                        ]
                    }

                    optional_fields = {
                        "name": name,
                        "emails": emails,
                        "keywords": keywords,
                        "notification_email": notification_email,
                        "users": users
                    }

                    for field, value in optional_fields.items():

                        if field == "notification_email":

                            if value.strip():
                                company[field] = value.strip()

                        elif value.strip():

                            company[field] = [
                                item.strip()
                                for item in value.split(",")
                                if item.strip()
                            ]

                    try:

                        create_company(company)

                        st.success(
                            "Empresa creada correctamente."
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"No se pudo crear la empresa: {error}"
                        )

    except Exception as error:

        st.error(
            f"No se pudieron cargar las empresas: {error}"
        )
