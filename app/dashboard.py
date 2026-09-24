
from pathlib import Path
import json
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
PREDICTIONS = ROOT / "data" / "churniq_predictions.csv"
METRICS = ROOT / "reports" / "metrics.json"

st.set_page_config(
    page_title="ChurnIQ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
[data-testid="stMetricValue"] {font-size: 2rem;}
div[data-testid="stMetric"] {
    border: 1px solid rgba(128,128,128,.18);
    padding: 14px;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

st.title("ChurnIQ")
st.caption("AI-Powered Customer Churn Prediction & Retention Analytics")

if not PREDICTIONS.exists():
    st.error(
        "Missing data/churniq_predictions.csv. "
        "Export it from the ChurnIQ Colab notebook first."
    )
    st.stop()

df = pd.read_csv(PREDICTIONS)

required = {
    "ChurnProbability", "RiskLevel", "MonthlyCharges", "MonthlyRevenueAtRisk",
    "AnnualRevenueAtRisk", "Contract", "InternetService", "PaymentMethod",
    "tenure", "ActualChurn"
}
missing = required - set(df.columns)
if missing:
    st.error(f"Missing columns in predictions CSV: {sorted(missing)}")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
risk_options = ["Low", "Medium", "High"]
selected_risk = st.sidebar.multiselect(
    "Risk level", risk_options, default=risk_options
)
contract_options = sorted(df["Contract"].dropna().unique().tolist())
selected_contract = st.sidebar.multiselect(
    "Contract", contract_options, default=contract_options
)
internet_options = sorted(df["InternetService"].dropna().unique().tolist())
selected_internet = st.sidebar.multiselect(
    "Internet service", internet_options, default=internet_options
)

filtered = df[
    df["RiskLevel"].isin(selected_risk)
    & df["Contract"].isin(selected_contract)
    & df["InternetService"].isin(selected_internet)
].copy()

overview, risk_tab, drivers_tab, customers_tab = st.tabs(
    ["Overview", "Risk Analytics", "Model & Drivers", "Customer Priorities"]
)

with overview:
    total = len(filtered)
    avg_prob = filtered["ChurnProbability"].mean() if total else 0
    high = int((filtered["RiskLevel"] == "High").sum())
    monthly = filtered["MonthlyRevenueAtRisk"].sum()
    annual = filtered["AnnualRevenueAtRisk"].sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Customers", f"{total:,}")
    c2.metric("Avg churn probability", f"{avg_prob:.1%}")
    c3.metric("High-risk customers", f"{high:,}")
    c4.metric("Monthly revenue at risk", f"${monthly:,.0f}")
    c5.metric("Annual revenue at risk", f"${annual:,.0f}")

    st.info(
        "Revenue-at-risk is an analytical estimate based on "
        "MonthlyCharges × predicted churn probability. It is not realized loss."
    )

    left, right = st.columns(2)
    with left:
        risk_counts = (
            filtered["RiskLevel"]
            .value_counts()
            .reindex(["Low", "Medium", "High"])
            .fillna(0)
            .reset_index()
        )
        risk_counts.columns = ["RiskLevel", "Customers"]
        fig = px.bar(
            risk_counts,
            x="RiskLevel",
            y="Customers",
            title="Customer Risk Distribution",
            text_auto=True,
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        contract = (
            filtered.groupby("Contract", as_index=False)["ChurnProbability"]
            .mean()
            .sort_values("ChurnProbability", ascending=False)
        )
        fig = px.bar(
            contract,
            x="Contract",
            y="ChurnProbability",
            title="Average Churn Risk by Contract",
            text_auto=".1%",
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        internet = (
            filtered.groupby("InternetService", as_index=False)["ChurnProbability"]
            .mean()
            .sort_values("ChurnProbability", ascending=False)
        )
        fig = px.bar(
            internet,
            x="InternetService",
            y="ChurnProbability",
            title="Average Churn Risk by Internet Service",
            text_auto=".1%",
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        payment = (
            filtered.groupby("PaymentMethod", as_index=False)["ChurnProbability"]
            .mean()
            .sort_values("ChurnProbability", ascending=False)
        )
        fig = px.bar(
            payment,
            x="PaymentMethod",
            y="ChurnProbability",
            title="Average Churn Risk by Payment Method",
            text_auto=".1%",
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

with risk_tab:
    st.subheader("Risk & Revenue Exposure")

    fig = px.scatter(
        filtered,
        x="MonthlyCharges",
        y="ChurnProbability",
        size="MonthlyRevenueAtRisk",
        color="RiskLevel",
        hover_data=["tenure", "Contract", "InternetService", "PaymentMethod"],
        title="Monthly Charges vs Churn Probability",
    )
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

    exposure = (
        filtered.groupby("RiskLevel", as_index=False)
        .agg(
            Customers=("RiskLevel", "size"),
            MonthlyRevenueAtRisk=("MonthlyRevenueAtRisk", "sum"),
            AnnualRevenueAtRisk=("AnnualRevenueAtRisk", "sum"),
            AvgChurnProbability=("ChurnProbability", "mean"),
        )
    )
    st.dataframe(
        exposure.style.format({
            "MonthlyRevenueAtRisk": "${:,.2f}",
            "AnnualRevenueAtRisk": "${:,.2f}",
            "AvgChurnProbability": "{:.1%}",
        }),
        use_container_width=True,
        hide_index=True,
    )

with drivers_tab:
    st.subheader("Model Performance")

    if METRICS.exists():
        info = json.loads(METRICS.read_text(encoding="utf-8"))
        best = info.get("best_model", "Unknown")
        st.success(f"Best model: {best}")

        model_rows = []
        for name, values in info.get("models", {}).items():
            row = {"Model": name}
            for k, v in values.items():
                if k != "confusion_matrix":
                    row[k] = v
            model_rows.append(row)

        if model_rows:
            metrics_df = pd.DataFrame(model_rows)
            st.dataframe(metrics_df, use_container_width=True, hide_index=True)
    else:
        st.warning(
            "metrics.json is not present yet. Export it from Colab to show "
            "the verified model-comparison metrics."
        )

    st.subheader("Observed High-Risk Pattern")
    st.write(
        "Within the current test-set predictions, the highest-risk customers "
        "are concentrated around short tenure, month-to-month contracts, "
        "fiber-optic internet, and frequently electronic-check payment."
    )
    st.caption(
        "This is descriptive model output from the IBM sample data; "
        "it should not be interpreted as a causal claim."
    )

with customers_tab:
    st.subheader("Retention Priority Queue")

    limit = st.slider("Customers to display", 10, 100, 25, 5)

    top = filtered.sort_values(
        ["ChurnProbability", "MonthlyRevenueAtRisk"],
        ascending=False
    ).head(limit)

    show_cols = [
        c for c in [
            "customerID", "tenure", "Contract", "InternetService",
            "PaymentMethod", "MonthlyCharges", "ChurnProbability",
            "RiskLevel", "MonthlyRevenueAtRisk", "ActualChurn"
        ] if c in top.columns
    ]

    styled = top[show_cols].copy()
    st.dataframe(
        styled.style.format({
            "MonthlyCharges": "${:,.2f}",
            "ChurnProbability": "{:.1%}",
            "MonthlyRevenueAtRisk": "${:,.2f}",
        }),
        use_container_width=True,
        hide_index=True,
    )

    csv = top.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered priority list",
        data=csv,
        file_name="churniq_retention_priorities.csv",
        mime="text/csv",
    )

st.divider()
st.caption(
    "ChurnIQ is a portfolio/educational ML project using the IBM Telco "
    "Customer Churn sample dataset. Predictions are not production decisions."
)
