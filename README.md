# Daraz-sku-Analyzer
Streamlit app for Daraz sellers to quickly count how many times each product SKU was sold from an uploaded Excel (.xlsx) file — works locally and on Streamlit Cloud.
# 🛍️ Daraz Sold Items Counter — Streamlit App

A simple yet powerful **Streamlit web application** that helps Daraz sellers quickly analyze their **monthly sales report** just by **dragging and dropping their Excel (.xlsx) file** — no coding required!

---

## 🎯 Purpose

This app is designed for **Daraz sellers** who want to easily track how many times each product (SKU) was sold during a specific period.  
It reads your Daraz Excel report, identifies the **“Product SKU”** column, and automatically calculates the **total repeat count** of each SKU.

---

## ⚙️ Features

- 🖱️ **Drag & Drop Upload** — Just drop your Daraz `.xlsx` file into the Streamlit browser window  
- 📈 **Instant Analysis** — Instantly see how many times each SKU was sold  
- ☁️ **Cloud Ready** — Can be deployed on **Streamlit Cloud** for anytime, anywhere access  
- ⚡ **Fast & Simple** — No API keys or manual data cleaning required  
- 💾 **Local & Online Support** — Works seamlessly both on localhost and Streamlit Cloud  

---

## 🚀 How It Works

1. **Open the app** in your browser  
   - Local: `localhost`  
   - Cloud: Streamlit Cloud deployed link  
2. **Drag & drop** your Daraz Excel (.xlsx) sales report file  
3. The app will automatically:  
   - Read the file  
   - Find the **“Product SKU”** column  
   - Count how many times each SKU appears  
4. **View the result** in an interactive, tabular format

---

## 🧰 Requirements  

Before running the app, make sure you have Python and the following libraries installed:


pip install streamlit pandas openpyxl


## ▶️ Run Locally

Run the app on your computer with this command:

streamlit run app.py


Once it starts, open the provided localhost link in your browser to use the interface.

## 📊 Example Output
Product SKU	Sold Count
ABC123	15
XYZ456	8
LMN789	3
💡 Tips

Deploy this app on Streamlit Cloud to access it online without running Python locally.

Share your public Streamlit app link with your team for easy collaboration.

Works great with monthly or weekly Daraz reports.

## 🧑‍💻 Developer Notes

Built with ❤️ using Python, Streamlit, pandas, and openpyxl.
This project aims to simplify Daraz sales tracking for small business owners and sellers.

## 📬 Contact

For feedback or improvements, feel free to open an issue or submit a pull request on GitHub.

⭐ Star this repo if you found it helpful!

---

Would you like me to also generate a **short one-line project summary** (for GitHub’s “About” section under the repo title)? It helps your repository look more polished in search results.

```bash
pip install streamlit pandas openpyxl
