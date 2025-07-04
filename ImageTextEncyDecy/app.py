# File: app.py

import streamlit as st
import os
from crypto_utils import *
from access_control import *
from PIL import Image
import numpy as np
import io

ensure_files()
st.set_page_config(layout="wide", page_title="ImageTextEncyDecy")

st.title("🔐 Secure Image & Text Encryption (Local Simulation)")

role = st.sidebar.selectbox("Choose Role", ["Owner", "User", "Cloud Provider"])

if role == "Owner":
    st.header("👑 Owner Panel")
    option = st.selectbox("Select Action", ["Encrypt Text", "Encrypt Image", "Grant Access", "View Requests"])

    if option == "Encrypt Text":
        text = st.text_area("Enter text to encrypt:")
        filename = st.text_input("Save as filename (e.g., note1.txt)")
        if st.button("Encrypt and Save"):
            if text and filename:
                key = generate_key()
                encrypted = encrypt_text(text, key)
                with open(f"data/encrypted/{filename}", "w") as f:
                    f.write(encrypted)
                grant_access(filename, "owner", save_key_hex(key))
                log_access("owner", filename, "owner")
                st.success(f"Saved as {filename} and access granted to owner.")

    elif option == "Encrypt Image":
        image_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
        filename = st.text_input("Save as name (without extension)")
        if st.button("Encrypt Image") and image_file and filename:
            key = generate_key()
            img = Image.open(image_file)
            enc_data, shape = encrypt_image(image_file, key)
            enc_path = f"data/encrypted/{filename}.bin"
            with open(enc_path, "wb") as f:
                f.write(enc_data)
            with open(enc_path + ".shape", "w") as f:
                f.write(",".join(map(str, shape)))
            grant_access(filename, "owner", save_key_hex(key))
            log_access("owner", filename, "owner")
            st.success(f"Encrypted image saved as {filename}.bin")

    elif option == "Grant Access":
        filename = st.text_input("File to share (e.g., note1.txt or image1)")
        user = st.text_input("Grant access to username:")
        if st.button("Grant Access"):
            key_hex = get_key_if_allowed(filename, "owner")
            if key_hex:
                grant_access(filename, user, key_hex)
                log_access("owner", filename, user)
                clear_request(filename, user)
                st.success(f"Access granted to {user} for {filename}")
            else:
                st.error("You don't have access to that file.")

    elif option == "View Requests":
        requests = get_requests()
        if not requests:
            st.info("No pending access requests.")
        else:
            for filename, users in requests.items():
                for user in users:
                    col1, col2 = st.columns([3, 1])
                    col1.markdown(f"📄 **{user}** requested access to **{filename}**")
                    if col2.button("Approve", key=f"{filename}-{user}"):
                        key_hex = get_key_if_allowed(filename, "owner")
                        if key_hex:
                            grant_access(filename, user, key_hex)
                            log_access("owner", filename, user)
                            clear_request(filename, user)
                            st.success(f"Access granted to {user} for {filename}")

elif role == "User":
    st.header("🙋‍♂️ User Panel")
    username = st.text_input("Enter your username", value="user")
    action = st.selectbox("Action", ["Decrypt Text", "Decrypt Image", "Request Access"])

    if action == "Decrypt Text":
        filename = st.text_input("Enter filename (e.g., note1.txt)")
        path = f"data/encrypted/{filename}"

        if st.button("See Encrypted Data (Text)"):
            if os.path.exists(path):
                with open(path, "r") as f:
                    encrypted = f.read()
                with st.expander("Encrypted Text Preview"):
                    st.code(encrypted, language="text")
            else:
                st.warning("Encrypted file not found.")

        if st.button("Decrypt Text"):
            if os.path.exists(path):
                key_hex = get_key_if_allowed(filename, username)
                if key_hex:
                    with open(path, "r") as f:
                        enc = f.read()
                    try:
                        text = decrypt_text(enc, load_key_hex(key_hex))
                        st.text_area("Decrypted Text", text, height=200)
                    except Exception:
                        st.error("Decryption failed")
                else:
                    st.warning("You don't have access to this file.")
            else:
                st.error("File not found")

    elif action == "Decrypt Image":
        filename = st.text_input("Enter image filename (without .bin)")
        enc_path = f"data/encrypted/{filename}.bin"
        shape_path = enc_path + ".shape"

        if st.button("See Encrypted Data (Image)"):
            if os.path.exists(enc_path) and os.path.exists(shape_path):
                with open(enc_path, "rb") as f:
                    enc_data = f.read()
                with open(shape_path, "r") as f:
                    shape = tuple(map(int, f.read().split(",")))
                try:
                    arr = np.frombuffer(enc_data, dtype=np.uint8)
                    reshaped = arr[:np.prod(shape)].reshape(shape)
                    enc_img = Image.fromarray(reshaped.astype(np.uint8), 'RGB')
                    st.image(enc_img, caption="Encrypted Image Preview", use_column_width=True)
                except Exception as e:
                    st.error(f"Unable to render image: {str(e)}")
            else:
                st.warning("Encrypted image or shape file not found.")

        if st.button("Decrypt Image"):
            if os.path.exists(enc_path) and os.path.exists(shape_path):
                key_hex = get_key_if_allowed(filename, username)
                if key_hex:
                    with open(enc_path, "rb") as f:
                        enc_data = f.read()
                    with open(shape_path, "r") as f:
                        shape = tuple(map(int, f.read().split(",")))
                    img = decrypt_image(enc_data, shape, load_key_hex(key_hex))
                    if img:
                        st.image(img, caption="Decrypted Image", use_column_width=True)
                    else:
                        st.error("Decryption failed")
                else:
                    st.warning("You don't have access to this image.")
            else:
                st.error("Image or shape file not found.")

    elif action == "Request Access":
        filename = st.text_input("Enter filename you want access to (e.g., note1.txt or image1)")
        if st.button("Request Access"):
            request_access(filename, username)
            st.success(f"Access request sent for {filename}")

elif role == "Cloud Provider":
    st.header("☁️ Cloud Provider View")
    logs = view_log()
    for log in logs:
        st.write(f"📁 [{log['timestamp']}] {log['owner']} ➜ {log['shared_with']} → `{log['filename']}`")
