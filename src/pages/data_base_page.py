import streamlit as st
from services.data_base_service import BackupService
from datetime import datetime
import os

backup_service = BackupService()

def admin_page():
    st.title("Администрирование базы данных")

    backup_dir = "/home/arnemkova/Flight_Booking_Service/src/backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)

    if st.button("Создать резервную копию"):
        backup_path = os.path.join(backup_dir, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.backup")
        try:
            message = backup_service.create_backup(backup_path)
            st.success(message)
        except RuntimeError as e:
            st.error(e)

    uploaded_file = st.file_uploader("Выберите файл резервной копии для восстановления", type=["backup"])
    if uploaded_file:
        backup_path = os.path.join(backup_dir, uploaded_file.name)
        with open(backup_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("Восстановить данные"):
            try:
                message = backup_service.restore_backup(backup_path)
                st.success(message)
            except RuntimeError as e:
                st.error(e)
