import streamlit as st
import pandas as pd
import io
import warnings

# suppress harmless openpyxl user warning about default style
warnings.filterwarnings("ignore", category=UserWarning, module='openpyxl')

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="Prime Labs – SKU Analyzer",
    layout="wide",
    page_icon="📊"
)

# ---------------------- CUSTOM STYLES ----------------------
st.markdown(
    """
    <style>
        /* Background gradient */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #ffffff 0%, #f5f6f7 100%);
        }

        /* Top-left brand badge */
        .brand-badge {
            font-size:14px; color:#6b7280; margin-bottom: 8px;
        }

        /* Card styling */
        .card {
            background: linear-gradient(180deg, #ffffff 0%, #fbfbfb 100%);
            padding: 22px;
            border-radius: 15px;
            box-shadow: -4px 4px 12px rgba(0, 0, 0, 0.08);
            margin-bottom: 20px;
        }

        /* Section title */
        .section-title { font-size:18px; font-weight:600; margin-bottom:8px; }

        /* Footer */
        footer { visibility: hidden; }
        .footer-custom { text-align:center; color:#9ca3af; font-size:13px; padding:18px 0 6px 0; }

        /* Make dataframes fit better */
        .stDataFrame { overflow: auto; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------- HEADER / BRAND ----------------------
st.markdown('<div class="brand-badge">🧪 Prime Labs – SKU Analyzer</div>', unsafe_allow_html=True)
st.title("Daraz Seller SKU Sold Count Analyzer")
st.write("Upload your Daraz report (CSV or XLSX). The app will detect the SKU column and show SKU-wise sold counts.")

# ---------------------- FILE UPLOADER ----------------------
uploaded_file = st.file_uploader("📤 Upload your Daraz file", type=["xlsx", "xls", "csv"])


def detect_sku_column(columns):
    """Try to find the SKU column name from common variants."""
    lower_map = {c.lower().strip(): c for c in columns}

    candidates = [
        'sellersku', 'seller_sku', 'seller sku', 'sku', 'item_sku', 'item sku', 'seller sku'
    ]
    for cand in candidates:
        if cand in lower_map:
            return lower_map[cand]
    # fallback: look for any column that contains 'sku' substring
    for lc, orig in lower_map.items():
        if 'sku' in lc:
            return orig
    return None


if uploaded_file is not None:
    # read file robustly
    try:
        if uploaded_file.name.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Failed to read the uploaded file: {e}")
        st.stop()

    # quick preview of columns for debugging if needed
    cols = list(df.columns)

    # detect sku column
    sku_col = detect_sku_column(cols)

    if sku_col is None:
        st.error("Could not find an SKU column. The app looked for column names like 'sellerSku', 'SKU', 'seller_sku'.")
        ("Columns found: " + ", ".join(cols[:50]))
    else:
        # Ensure SKU column is string
        df[sku_col] = df[sku_col].astype(str)

        # Raw Data Preview
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📄 Raw Data Preview</div>', unsafe_allow_html=True)
            st.dataframe(df.head(10))
            st.markdown('</div>', unsafe_allow_html=True)

        # Compute sales summary: count occurrences of exact SKU string
        sku_count = df[sku_col].value_counts(dropna=True).reset_index()
        sku_count.columns = ['sellerSku', 'total_sold_count']

        # Sales Summary
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📊 Sales Summary</div>', unsafe_allow_html=True)
            st.dataframe(sku_count)
            st.markdown('</div>', unsafe_allow_html=True)

        # Top N selector
        max_items = min(200, len(sku_count))
        default_n = 15 if max_items >= 15 else max_items
        top_n = st.slider("Select Top N Items to Display", min_value=5 if max_items>=5 else 1, max_value=max_items, value=default_n)

        top_items = sku_count.head(top_n)

        # Chart (Horizontal Bar)
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<div class="section-title">🏆 Top {top_n} Best-Selling Items</div>', unsafe_allow_html=True)

        import matplotlib.pyplot as plt

            # Convert sellerSku column to string (safety)
        top_items['sellerSku'] = top_items['sellerSku'].astype(str)

            # Horizontal Bar Chart using Matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(top_items['sellerSku'], top_items['total_sold_count'], color="#2E86C1")
        ax.set_xlabel("Units Sold", fontsize=12)
        ax.set_ylabel("Item (Seller SKU)", fontsize=12)
        ax.set_title(f"Top {top_n} Best-Selling Items", fontsize=14, fontweight='bold')
        ax.invert_yaxis()  # Highest selling item appears on top
        ax.grid(axis='x', linestyle='--', alpha=0.4)

        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)



        # Download buttons (CSV + Excel)
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">⬇️ Download Sales Summary</div>', unsafe_allow_html=True)

            csv_data = sku_count.to_csv(index=False).encode('utf-8')

            # Excel export
            towrite = io.BytesIO()
            with pd.ExcelWriter(towrite, engine='openpyxl') as writer:
                sku_count.to_excel(writer, index=False, sheet_name='SalesSummary')
            towrite.seek(0)
            excel_data = towrite.read()

            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button(label="Download as CSV", data=csv_data, file_name="SellerSKU_Sold_Count.csv", mime='text/csv')
            with col2:
                st.download_button(label="Download as Excel", data=excel_data, file_name="SellerSKU_Sold_Count.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            st.markdown('</div>', unsafe_allow_html=True)


# Footer
st.markdown('<div class="footer-custom">© Prime Labs – SKU Analyzer</div>', unsafe_allow_html=True)
