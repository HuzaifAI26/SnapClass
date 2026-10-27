import streamlit as st
import base64
from pathlib import Path

LOGO_PATH = Path(__file__).resolve().parents[2] / "assets" / "ai_master.png"


def get_logo_html():
    if not LOGO_PATH.exists():
        return "<span style='font-weight:bold;'>AI Master</span>"

    with open(LOGO_PATH, "rb") as logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode("utf-8")

    return (
        f"<img src='data:image/png;base64,{logo_base64}' "
        "style='height:60px; width:auto; object-fit:contain;' "
        "alt='AI Master logo' />"
    )


def footer_home():
    logo_html = get_logo_html()

    st.markdown(
        f"""
        <div style="
            margin-top:2rem;
            display:flex;
            gap:8px;
            justify-content:center;
            align-items:center;
        ">
            <p style="font-weight:bold; color:white; margin:0;">
                Created with ❤️ by
            </p>
            {logo_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def footer_dashboard():
    logo_html = get_logo_html()

    st.markdown(
        f"""
        <div style="
            margin-top:2rem;
            display:flex;
            gap:8px;
            justify-content:center;
            align-items:center;
        ">
            <p style="font-weight:bold; color:black; margin:0;">
                Created with ❤️ by
            </p>
            {logo_html}
        </div>
        """,
        unsafe_allow_html=True
    )
