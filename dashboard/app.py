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

# Kav Bar

if "page" not in st.session_state:
    st.session_state.page = "alerts"

col1, col2 = st.columns(2)

with col1:
    if st.button(
        "📊 ALERTAS",
        use_container_width=True
    ):
        st.session_state.page = "alerts"

with col2:
    if st.button(
        "🏢 EMPRESAS",
        use_container_width=True
    ):
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

            company_options = ["Todas"]

            company_options += [
                company["company_id"]
                for company in companies
            ]

            company_filter = st.selectbox(
                "Empresa",
                company_options
            )

        with col2:

            severity_options = ["Todas"]

            severity_options += sorted({
                str(
                    alert.get(
                        "severity",
                        ""
                    )
                ).upper()
                for alert in alerts
                if alert.get("severity")
            })

            severity_filter = st.selectbox(
                "Severidad",
                severity_options
            )

        # Apply filters

        filtered_alerts = alerts

        if company_filter != "Todas":

            filtered_alerts = [
                alert
                for alert in filtered_alerts
                if alert.get("company_id")
                == company_filter
            ]

        if severity_filter != "Todas":

            filtered_alerts = [
                alert
                for alert in filtered_alerts
                if str(
                    alert.get(
                        "severity",
                        ""
                    )
                ).upper()
                == severity_filter
            ]

        st.write(
            f"**{len(filtered_alerts)} alertas**"
        )

        # Alert cards

        if not filtered_alerts:

            st.info(
                "No hay alertas que coincidan "
                "con los filtros seleccionados."
            )

        for alert in filtered_alerts:

            severity = str(
                alert.get(
                    "severity",
                    "UNKNOWN"
                )
            ).upper()

            company_name = alert.get(
                "company_name",
                alert.get(
                    "company_id",
                    "Empresa desconocida"
                )
            )

            company_id = alert.get(
                "company_id",
                "—"
            )

            matches = alert.get(
                "matches",
                []
            )

            source = alert.get(
                "source",
                "—"
            )

            document_id = alert.get(
                "document_id",
                "—"
            )

            date = alert.get(
                "date",
                "—"
            )

            detected_at = alert.get(
                "detected_at",
                "—"
            )

            alert_id = alert.get(
                "alert_id",
                "—"
            )

            with st.container(
                border=True
            ):

                # Header

                st.subheader(
                    f"{severity} — {company_name}"
                )

                st.caption(
                    f"Company ID: {company_id}"
                )

                # Matches

                st.markdown(
                    "**Coincidencias detectadas**"
                )

                if matches:

                    for match in matches:

                        match_type = match.get(
                            "type",
                            "unknown"
                        )

                        match_value = match.get(
                            "value",
                            ""
                        )

                        icons = {
                            "user": "👤",
                            "domain": "🌐",
                            "email": "✉️",
                            "keyword": "🔑"
                        }

                        icon = icons.get(
                            match_type,
                            "🔎"
                        )

                        st.write(
                            f"{icon} **{match_type}** — "
                            f"`{match_value}`"
                        )

                else:

                    st.write(
                        "Sin coincidencias registradas."
                    )

                # Source information

                st.markdown(
                    "**Información del origen**"
                )

                st.write(
                    f"**Fuente:** {source}"
                )

                st.write(
                    f"**Documento:** `{document_id}`"
                )

                st.write(
                    f"**Fecha del documento:** {date}"
                )

                st.write(
                    f"**Detectado:** {detected_at}"
                )

                st.caption(
                    f"Alert ID: {alert_id}"
                )

    except Exception as error:

        st.error(
            f"No se pudieron cargar las alertas: {error}"
        )

# Empresas (COMPANIES)

else:

    st.header("Empresas")

    try:

        companies = get_companies()

        # Company list

        if not companies:

            st.info(
                "No hay empresas registradas."
            )

        for company in companies:

            company_id = company.get(
                "company_id",
                "—"
            )

            name = company.get(
                "name",
                company_id
            )

            domains = company.get(
                "domains",
                []
            )

            emails = company.get(
                "emails",
                []
            )

            keywords = company.get(
                "keywords",
                []
            )

            users = company.get(
                "users",
                []
            )

            notification_email = company.get(
                "notification_email",
                "—"
            )

            with st.container(
                border=True
            ):

                st.subheader(name)

                st.write(
                    f"**Company ID:** `{company_id}`"
                )

                st.write(
                    f"**Domains:** "
                    f"{', '.join(domains) if domains else '—'}"
                )

                st.write(
                    f"**Emails:** "
                    f"{', '.join(emails) if emails else '—'}"
                )

                st.write(
                    f"**Keywords:** "
                    f"{', '.join(keywords) if keywords else '—'}"
                )

                st.write(
                    f"**Users:** "
                    f"{', '.join(users) if users else '—'}"
                )

                st.write(
                    f"**Email de notificaciones:** "
                    f"{notification_email}"
                )

        # Create company

        st.divider()

        st.subheader(
            "➕ Dar de alta empresa"
        )

        with st.form(
            "company_form"
        ):

            company_id = st.text_input(
                "Company ID *"
            )

            domains = st.text_input(
                "Domains *",
                placeholder="ejemplo.es, ejemplo.com"
            )

            name = st.text_input(
                "Nombre"
            )

            emails = st.text_input(
                "Emails",
                placeholder=(
                    "admin@ejemplo.es, "
                    "user@ejemplo.es"
                )
            )

            keywords = st.text_input(
                "Keywords",
                placeholder=(
                    "keyword1, keyword2"
                )
            )

            notification_email = st.text_input(
                "Email de notificaciones"
            )

            users = st.text_input(
                "Usuarios",
                placeholder=(
                    "usuario1, usuario2"
                )
            )

            submitted = st.form_submit_button(
                "Crear empresa"
            )

            if submitted:

                # Required fields

                if not company_id.strip():

                    st.error(
                        "Company ID es obligatorio."
                    )

                elif not domains.strip():

                    st.error(
                        "Domains es obligatorio."
                    )

                else:

                    company = {
                        "company_id": company_id.strip(),
                        "domains": [
                            item.strip()
                            for item in domains.split(",")
                            if item.strip()
                        ]
                    }

                    # Optional fields

                    if name.strip():

                        company["name"] = name.strip()

                    if emails.strip():

                        company["emails"] = [
                            item.strip()
                            for item in emails.split(",")
                            if item.strip()
                        ]

                    if keywords.strip():

                        company["keywords"] = [
                            item.strip()
                            for item in keywords.split(",")
                            if item.strip()
                        ]

                    if notification_email.strip():

                        company[
                            "notification_email"
                        ] = notification_email.strip()

                    if users.strip():

                        company["users"] = [
                            item.strip()
                            for item in users.split(",")
                            if item.strip()
                        ]

                    # Send to API

                    try:

                        create_company(
                            company
                        )

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