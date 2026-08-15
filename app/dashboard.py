from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
import yaml

from app.data_validation import normalize_columns, validate_dataframe

st.set_page_config(page_title="Financial Dashboard", layout="wide")


@st.cache_data
def load_templates() -> dict:
    with open("config/source_templates.yml", "r", encoding="utf-8") as template_file:
        return yaml.safe_load(template_file)


def read_excel(uploaded_file) -> pd.DataFrame:
    df = pd.read_excel(uploaded_file)
    df.columns = normalize_columns(df.columns)
    return df


def render_upload_page() -> None:
    st.header("Source Data Upload")
    templates = load_templates()
    source_type = st.selectbox("Source type", list(templates.keys()))
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

    if uploaded_file is None:
        st.info("Upload Sales, Production, Trial Balance, Debtors, Creditors, Coal, or Chemical Consumption Excel files.")
        return

    df = read_excel(uploaded_file)
    result = validate_dataframe(df, templates[source_type]["required_columns"])

    if result.is_valid:
        st.success(f"File passed validation with {len(df):,} rows.")
    else:
        for error in result.errors:
            st.error(error)
    for warning in result.warnings:
        st.warning(warning)
    st.dataframe(df.head(100), use_container_width=True)


def render_executive_dashboard() -> None:
    st.header("Executive Dashboard")
    st.caption("Prototype view. Connect PostgreSQL facts to replace the sample trend data.")
    sample = pd.DataFrame(
        {
            "month": ["Apr", "May", "Jun", "Jul", "Aug", "Sep"],
            "sales": [1250000, 1420000, 1375000, 1510000, 1660000, 1725000],
            "production": [920, 980, 950, 1025, 1090, 1130],
            "profit": [155000, 184000, 171000, 199000, 225000, 241000],
        }
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("YTD Sales", f"₹{sample['sales'].sum():,.0f}")
    kpi2.metric("YTD Production", f"{sample['production'].sum():,.0f}")
    kpi3.metric("YTD Profit", f"₹{sample['profit'].sum():,.0f}")
    kpi4.metric("Net Margin", f"{sample['profit'].sum() / sample['sales'].sum():.1%}")

    left, right = st.columns(2)
    left.plotly_chart(px.line(sample, x="month", y="sales", markers=True, title="Monthly Sales Trend"), use_container_width=True)
    right.plotly_chart(px.bar(sample, x="month", y="production", title="Monthly Production"), use_container_width=True)


def render_mapping_page() -> None:
    st.header("Mapping & Configuration")
    st.write("Maintain ledger-to-report mapping for P&L, Balance Sheet, Cash Flow, and ratios.")
    st.data_editor(
        pd.DataFrame(
            [
                {
                    "ledger_name": "Sales Domestic",
                    "primary_group": "Revenue",
                    "report_section": "P&L",
                    "report_line": "Sales",
                    "cash_flow_type": "Operating",
                    "normal_sign": "credit",
                }
            ]
        ),
        num_rows="dynamic",
        use_container_width=True,
    )


def main() -> None:
    st.sidebar.title("Finance MIS")
    page = st.sidebar.radio(
        "Navigation",
        [
            "Executive Dashboard",
            "Source Data",
            "Mapping & Configuration",
            "Sales MIS",
            "Production MIS",
            "P&L",
            "Balance Sheet",
            "Cash Flow",
            "Ratios & KPIs",
            "Customer Analysis",
            "Supplier Analysis",
            "Drill-down Transactions",
        ],
    )

    if page == "Executive Dashboard":
        render_executive_dashboard()
    elif page == "Source Data":
        render_upload_page()
    elif page == "Mapping & Configuration":
        render_mapping_page()
    else:
        st.header(page)
        st.info("This module is scaffolded and ready for PostgreSQL-backed implementation.")


if __name__ == "__main__":
    main()
