import streamlit as st
import cv2
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime, time, timezone
import base64
import io
import json
from PIL import Image

# ==============================================================================
# PAGE CONFIGURATION & METADATA (Must be the first Streamlit command)
# ==============================================================================
st.set_page_config(
    page_title="Face Recognition Attendance System",
    page_icon="👤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# CUSTOM GEMINI-INSPIRED CSS DESIGN SYSTEM
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Main Background & Typography */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F0EDE4 !important;
        font-family: 'Outfit', sans-serif !important;
        color: #1C2E2C !important;
    }
    
    /* Clean rounded card containers */
    .gemini-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        border: 1px solid #D6D2C4;
        padding: 28px;
        box-shadow: 0 4px 20px rgba(0, 71, 65, 0.03);
        margin-bottom: 24px;
        transition: all 0.3s ease;
    }
    .gemini-card:hover {
        box-shadow: 0 6px 24px rgba(0, 71, 65, 0.06);
    }
    
    /* Modern Gemini gradient headers */
    .gemini-gradient-text {
        background: linear-gradient(135deg, #004741 0%, #146C64 50%, #2A6F68 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 32px;
        margin-bottom: 12px;
        letter-spacing: -0.5px;
        text-align: center;
    }
    
    .gemini-sparkle-logo {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #ADFAFF 0%, #004741 55%, #0C3833 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px auto;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.2);
        animation: pulse 3s infinite alternate;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        100% { transform: scale(1.06); }
    }
    
    /* Custom Status Banner */
    .status-banner {
        padding: 8px 16px;
        border-radius: 24px;
        font-size: 13px;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 20px;
    }
    .status-banner.success {
        background-color: #E6F4EA;
        color: #137333;
        border: 1px solid #CEEAD6;
    }
    .status-banner.warning {
        background-color: #FEF7E0;
        color: #B06000;
        border: 1px solid #FEEFC3;
    }
    .status-banner.error {
        background-color: #FCE8E6;
        color: #C5221F;
        border: 1px solid #FAD2CF;
    }
    
    /* Layout styling for screens */
    .header-bar {
        background-color: #FFFFFF;
        border-radius: 16px;
        border: 1px solid #D6D2C4;
        padding: 16px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.01);
    }
    
    .header-title-text {
        font-size: 20px;
        font-weight: 600;
        color: #1C2E2C;
        background: linear-gradient(120deg, #004741, #0C3833);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Premium Stats Cards */
    .stat-card {
        background: #FFFFFF;
        border: 1px solid #D6D2C4;
        border-radius: 16px;
        padding: 18px 12px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.01);
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        border-color: #004741;
        box-shadow: 0 4px 12px rgba(0, 71, 65, 0.06);
    }
    .stat-value {
        font-size: 26px;
        font-weight: 700;
        color: #004741;
        margin-bottom: 2px;
    }
    .stat-label {
        font-size: 12px;
        color: #5F6368;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Profile Image Style */
    .profile-img-preview {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #004741;
        box-shadow: 0 4px 12px rgba(0, 71, 65, 0.15);
        margin: 10px auto;
        display: block;
    }
    
    /* Dialog/Card Results styling */
    .result-card {
        border-radius: 16px;
        padding: 20px;
        margin-top: 15px;
        border: 1.5px solid;
    }
    .result-card.success {
        background-color: #F6FCF8;
        border-color: #34A853;
    }
    .result-card.warning {
        background-color: #FFFDF6;
        border-color: #FBBC05;
    }
    .result-card.error {
        background-color: #FDF7F7;
        border-color: #EA4335;
    }
    
    /* Pill button overrides for Streamlit baseButton elements */
    button[data-testid="baseButton-primary"] {
        border-radius: 24px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
        padding: 8px 24px !important;
        background: linear-gradient(135deg, #004741 0%, #125E56 100%) !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(0, 71, 65, 0.15) !important;
        transition: all 0.3s ease !important;
    }
    button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #003732 0%, #004741 100%) !important;
        box-shadow: 0 6px 15px rgba(0, 71, 65, 0.25) !important;
    }
    button[data-testid="baseButton-secondary"] {
        border-radius: 24px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
        padding: 8px 24px !important;
        color: #004741 !important;
        border: 1.5px solid #004741 !important;
        background-color: transparent !important;
        transition: all 0.3s ease !important;
    }
    button[data-testid="baseButton-secondary"]:hover {
        background-color: rgba(0, 71, 65, 0.05) !important;
        color: #003732 !important;
        border-color: #003732 !important;
    }
    
    /* Styled camera input border */
    .stCameraInput {
        border: 2px solid #D6D2C4 !important;
        border-radius: 20px !important;
        overflow: hidden !important;
    }
    
    /* Global hides for streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
if 'screen' not in st.session_state:
    st.session_state.screen = 0
if 'show_admin_drawer' not in st.session_state:
    st.session_state.show_admin_drawer = False
if 'employees_cache' not in st.session_state:
    st.session_state.employees_cache = None
if 'recognition_result' not in st.session_state:
    st.session_state.recognition_result = None
if 'registration_stage' not in st.session_state:
    st.session_state.registration_stage = "form"
if 'registration_success_data' not in st.session_state:
    st.session_state.registration_success_data = None

# ==============================================================================
# FIREBASE BACKEND CONTROLLER & CREDENTIAL LOAD
# ==============================================================================
@st.cache_resource(show_spinner=False)
def initialize_firebase():
    """Initializes Firebase Admin SDK using Streamlit Secrets securely."""
    if "firebase" not in st.secrets:
        return False, "Streamlit secrets does not contain a ['firebase'] entry.", None, None, False
        
    try:
        # Load from secrets
        cred_info = dict(st.secrets["firebase"])
        
        # Format the private key (replacing literal \n backslash sequence with actual newlines)
        if "private_key" in cred_info:
            cred_info["private_key"] = cred_info["private_key"].replace("\\n", "\n")
            
        cred = credentials.Certificate(cred_info)
        
        project_id = cred_info.get("project_id", "faceattendancesystem-75057")
        bucket_name = f"{project_id}.appspot.com"
        
        # Avoid duplicate initialization
        if not firebase_admin._apps:
            app = firebase_admin.initialize_app(cred, {
                'storageBucket': bucket_name
            })
        else:
            app = firebase_admin.get_app()
            
        # Connect Firestore
        db = firestore.client()
        
        # Test GCS Storage Bucket accessibility
        bucket = storage.bucket()
        storage_active = False
        try:
            # Safely test connection
            list(bucket.list_blobs(max_results=1))
            storage_active = True
        except Exception:
            # Falling back to local/Firestore storage if GCS bucket does not exist or isn't enabled
            storage_active = False
            
        return True, "🟢 Connected to Firebase", db, bucket, storage_active
        
    except Exception as e:
        return False, f"🔴 Firebase Connection Error: {str(e)}", None, None, False

# Establish connection
fb_success, fb_status_msg, db, bucket, storage_active = initialize_firebase()

# ==============================================================================
# REUSABLE COMPONENT: CONNECTION STATUS BANNER
# ==============================================================================
def render_connection_banner():
    if fb_success:
        if storage_active:
            status_html = """
            <div class="status-banner success">
                <span style="color: #34A853;">●</span> Connected to Firebase Cloud (Firestore & Storage Active)
            </div>
            """
        else:
            status_html = """
            <div class="status-banner warning">
                <span style="color: #FBBC05;">●</span> Connected to Firebase (Firestore Active | Storage Inactive — Base64 Fallback Mode)
            </div>
            """
    else:
        status_html = f"""
        <div class="status-banner error">
            <span style="color: #EA4335;">●</span> {fb_status_msg}
        </div>
        """
    st.markdown(status_html, unsafe_allow_html=True)

# ==============================================================================
# HELPER DATA ACTIONS
# ==============================================================================
def fetch_and_cache_employees(force=False):
    """Loads all registered employees from Firestore and caches in st.session_state."""
    if not fb_success or db is None:
        return []
    if st.session_state.employees_cache is not None and not force:
        return st.session_state.employees_cache
        
    try:
        docs = db.collection("employees").stream()
        employees = []
        for doc in docs:
            data = doc.to_dict()
            employees.append(data)
        st.session_state.employees_cache = employees
        return employees
    except Exception as e:
        st.error(f"Error loading employee profiles: {e}")
        return []

# Prefetch employees cache if connected
if fb_success:
    fetch_and_cache_employees()

# ==============================================================================
# SCREEN 0: WELCOME INTRO LANDING PAGE
# ==============================================================================
if st.session_state.screen == 0:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Outer layout container
    welcome_container_start = """
    <div class="welcome-container" style="display: flex; flex-direction: column; align-items: center; text-align: center; padding: 40px 20px; background: #FFFFFF; border-radius: 24px; border: 1px solid #D6D2C4; box-shadow: 0 8px 30px rgba(0, 71, 65, 0.04); max-width: 600px; margin: 40px auto;">
        <div class="gemini-sparkle-logo">
            <span class="gemini-sparkle" style="color: white; font-size: 32px; font-weight: bold;">✦</span>
        </div>
        <div class="gemini-gradient-text">Face Recognition Attendance</div>
        <p class="welcome-desc" style="color: #5F6368; font-size: 16px; line-height: 1.6; margin-bottom: 30px; max-width: 500px;">
            A production-ready automated attendance management solution. 
            Instantly identify registered profiles, check in employees, and view logs 
            via a lightweight local face recognition process connected directly to your cloud Firebase backend.
        </p>
    """
    st.markdown(welcome_container_start, unsafe_allow_html=True)
    
    # Render connection status directly inside the card
    render_connection_banner()
    
    # Let the user know if secrets need configuration
    if not fb_success:
        st.info("💡 Make sure to configure your Firebase Admin credentials inside `.streamlit/secrets.toml` to connect to your project.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Center button container using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Application", type="primary", use_container_width=True, disabled=not fb_success):
            st.session_state.screen = 1
            st.rerun()

# ==============================================================================
# SCREEN 1: MAIN ATTENDANCE & CAMERA DASHBOARD
# ==============================================================================
elif st.session_state.screen == 1:
    # Header bar
    st.markdown(f"""
    <div class="header-bar">
        <div class="header-title-text">👤 Face Attendance System</div>
        <div>
            <span class="gemini-badge">Dashboard</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display Status Banner
    render_connection_banner()
    
    # Check if Firebase works
    if not fb_success:
        st.error("Application requires a successful Firebase connection to proceed.")
        if st.button("Back to Welcome Screen", type="secondary"):
            st.session_state.screen = 0
            st.rerun()
        st.stop()
        
    # Top Action buttons for menu
    header_col1, header_col2 = st.columns([4, 1])
    with header_col2:
        admin_lbl = "Close Drawer ⋮" if st.session_state.show_admin_drawer else "Admin Menu ⋮"
        if st.button(admin_lbl, type="secondary", use_container_width=True):
            st.session_state.show_admin_drawer = not st.session_state.show_admin_drawer
            st.rerun()
            
    # ==========================================
    # ADMIN CONTROL DRAWER PANEL
    # ==========================================
    if st.session_state.show_admin_drawer:
        st.markdown('<div class="gemini-card" style="border-left: 4px solid #004741;">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin-top: 0; margin-bottom: 20px;">📊 Administration Console</h4>', unsafe_allow_html=True)
        
        # Load fresh caches
        employees = fetch_and_cache_employees()
        
        # Calculate Check-ins Today
        today_start = datetime.combine(datetime.now().date(), time.min)
        today_logs = []
        try:
            today_docs = db.collection("attendance").where("timestamp", ">=", today_start).stream()
            today_logs = [doc.to_dict() for doc in today_docs]
        except Exception:
            # Fallback in case of index errors or network errors
            pass
            
        unique_checkins_today = len(set(log["employee_id"] for log in today_logs))
        total_registered = len(employees)
        attendance_rate = (unique_checkins_today / total_registered * 100) if total_registered > 0 else 0.0
        
        # Render Stat Cards
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{total_registered}</div><div class="stat-label">Registered Profiles</div></div>', unsafe_allow_html=True)
        with s_col2:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{unique_checkins_today}</div><div class="stat-label">Checked In Today</div></div>', unsafe_allow_html=True)
        with s_col3:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{attendance_rate:.1f}%</div><div class="stat-label">Attendance Rate</div></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Admin tabs
        tab1, tab2 = st.tabs(["👥 Registered Employees", "📅 Attendance Logs"])
        
        with tab1:
            # Filters
            f_col1, f_col2 = st.columns([2, 1])
            with f_col1:
                search_q = st.text_input("🔍 Search employees by name or ID", placeholder="Search...")
            with f_col2:
                # Unique departments
                depts = ["All Departments"] + sorted(list(set(emp.get("department", "Default") for emp in employees)))
                dept_sel = st.selectbox("Department Filter", depts)
                
            # Filter Cache
            filtered_employees = employees
            if search_q:
                filtered_employees = [
                    emp for emp in filtered_employees
                    if search_q.lower() in emp.get("name", "").lower() or search_q.lower() in emp.get("employee_id", "").lower()
                ]
            if dept_sel != "All Departments":
                filtered_employees = [
                    emp for emp in filtered_employees
                    if emp.get("department", "") == dept_sel
                ]
                
            # Prepare employee grid data
            grid_data = []
            for emp in filtered_employees:
                reg_time_str = ""
                reg_dt = emp.get("registered_at")
                if reg_dt:
                    reg_time_str = reg_dt.strftime("%Y-%m-%d %H:%M:%S")
                grid_data.append({
                    "Employee ID": emp.get("employee_id", ""),
                    "Name": emp.get("name", ""),
                    "Department": emp.get("department", ""),
                    "Registered At": reg_time_str
                })
                
            if grid_data:
                st.dataframe(grid_data, use_container_width=True, hide_index=True)
            else:
                st.info("No matching registered employees found.")
                
            if employees:
                st.markdown("<hr style='border-top: 1px dashed #D6D2C4; margin: 20px 0;'>", unsafe_allow_html=True)
                st.markdown("<h5 style='margin-top: 0; margin-bottom: 12px; font-weight: 600; color: #1C2E2C;'>🗑️ Remove Employee Profile</h5>", unsafe_allow_html=True)
                
                # Selectbox containing all employee listings
                delete_options = {f"{emp['name']} ({emp['employee_id']})": emp for emp in employees}
                selected_del_label = st.selectbox("Select Profile to Remove", list(delete_options.keys()), key="select_delete_emp")
                
                # Confirmation input column
                del_col1, del_col2 = st.columns([1, 2])
                with del_col1:
                    confirm_delete = st.button("🗑️ Delete Profile", type="primary", use_container_width=True, key="btn_confirm_delete")
                
                if confirm_delete:
                    selected_emp = delete_options[selected_del_label]
                    emp_id = selected_emp["employee_id"]
                    emp_name = selected_emp["name"]
                    
                    with st.spinner(f"Removing {emp_name}'s profile..."):
                        try:
                            # 1. Try to delete the photo from Firebase Storage if storage is active
                            photo_url = selected_emp.get("photo_url", "")
                            if storage_active and photo_url and not photo_url.startswith("data:image/"):
                                try:
                                    blob_path = f"photos/{emp_id}.jpg"
                                    blob = bucket.blob(blob_path)
                                    if blob.exists():
                                        blob.delete()
                                except Exception:
                                    pass
                            
                            # 2. Delete the document from Firestore
                            db.collection("employees").document(emp_id).delete()
                            
                            # 3. Reload cache and rerun
                            fetch_and_cache_employees(force=True)
                            st.success(f"Profile of {emp_name} ({emp_id}) successfully removed.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error removing profile: {e}")
                
        with tab2:
            # Query logs (limit 150 to keep it lightweight, sorted in memory to avoid Firebase index error)
            logs_grid = []
            try:
                logs_docs = db.collection("attendance").limit(150).stream()
                all_logs = [doc.to_dict() for doc in logs_docs]
                # Sort in memory by timestamp descending
                all_logs.sort(key=lambda x: x.get("timestamp") if x.get("timestamp") else datetime.min, reverse=True)
                
                for log in all_logs:
                    ts = log.get("timestamp")
                    ts_str = ts.strftime("%Y-%m-%d %I:%M:%S %p") if ts else ""
                    logs_grid.append({
                        "Employee ID": log.get("employee_id", ""),
                        "Name": log.get("name", ""),
                        "Department": log.get("department", ""),
                        "Timestamp": ts_str,
                        "Status": log.get("status", "Checked In")
                    })
            except Exception as e:
                st.error(f"Error loading logs: {e}")
                
            if logs_grid:
                st.dataframe(logs_grid, use_container_width=True, hide_index=True)
            else:
                st.info("No attendance logs recorded yet.")
                
        st.markdown("</div>", unsafe_allow_html=True)
        
    # ==========================================
    # CAMERA PREVIEW & ACTIONS
    # ==========================================
    cam_col1, cam_col2, cam_col3 = st.columns([1, 4, 1])
    img_file = None
    with cam_col2:
        img_file = st.camera_input("Position your face in the frame", label_visibility="collapsed")
        st.markdown('<p style="text-align: center; color: #5F6368; font-size: 14px; margin-top: -8px; font-weight: 500;">Position your face in the frame</p>', unsafe_allow_html=True)
        
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        mark_attendance = st.button("✅ Mark Attendance", type="primary", use_container_width=True)
    with btn_col2:
        register_new = st.button("➕ New Registration", type="secondary", use_container_width=True)
        
    if register_new:
        # Reset result states before navigation
        st.session_state.recognition_result = None
        st.session_state.registration_stage = "form"
        st.session_state.screen = 2
        st.rerun()
        
    # ==========================================
    # ATTENDANCE LOGIC EXECUTION
    # ==========================================
    if mark_attendance:
        if img_file is None:
            st.session_state.recognition_result = {
                "status": "error",
                "message": "⚠️ Camera input is empty! Please verify your webcam is active and allow camera permissions."
            }
        else:
            with st.spinner("Analyzing biometric face features..."):
                try:
                    # Convert image bytes to numpy array
                    image = Image.open(io.BytesIO(img_file.getvalue()))
                    image_np = np.array(image.convert("RGB"))
                    
                    # Detect face encodings
                    face_locations = face_recognition.face_locations(image_np)
                    face_encodings = face_recognition.face_encodings(image_np, face_locations)
                    
                    if not face_encodings:
                        st.session_state.recognition_result = {
                            "status": "error",
                            "message": "❌ Face not detected. Please ensure your face is fully visible in the frame with good lighting."
                        }
                    else:
                        target_encoding = face_encodings[0]
                        employees = fetch_and_cache_employees()
                        
                        if not employees:
                            st.session_state.recognition_result = {
                                "status": "mismatch",
                                "message": "⚠️ There are no registered employees in the database yet."
                            }
                        else:
                            # Extract encodings from database cache
                            known_encodings = [np.array(emp["face_encoding"]) for emp in employees]
                            
                            # Run matching algorithms
                            # Tolerance 0.5 balances precision and recall
                            matches = face_recognition.compare_faces(known_encodings, target_encoding, tolerance=0.5)
                            face_distances = face_recognition.face_distance(known_encodings, target_encoding)
                            
                            best_match_idx = np.argmin(face_distances) if len(face_distances) > 0 else -1
                            
                            if best_match_idx != -1 and matches[best_match_idx]:
                                # Match found! Get employee data
                                emp_data = employees[best_match_idx]
                                distance = face_distances[best_match_idx]
                                confidence = max(0.0, min(100.0, (1.0 - distance) * 100.0))
                                
                                # Log attendance to Firestore
                                checkin_time = datetime.now()
                                doc_id = f"{emp_data['employee_id']}_{checkin_time.strftime('%Y%m%d_%H%M%S')}"
                                
                                log_record = {
                                    "employee_id": emp_data["employee_id"],
                                    "name": emp_data["name"],
                                    "department": emp_data["department"],
                                    "timestamp": checkin_time,
                                    "status": "Checked In",
                                    "confidence": float(confidence)
                                }
                                
                                db.collection("attendance").document(doc_id).set(log_record)
                                
                                st.session_state.recognition_result = {
                                    "status": "success",
                                    "employee": emp_data,
                                    "confidence": confidence,
                                    "timestamp": checkin_time
                                }
                            else:
                                # No match in database
                                st.session_state.recognition_result = {
                                    "status": "mismatch",
                                    "message": "⚠️ You're not registered yet"
                                }
                except Exception as e:
                    st.session_state.recognition_result = {
                        "status": "error",
                        "message": f"❌ Recognition failure: {str(e)}"
                    }
            st.rerun()
            
    # ==========================================
    # DISPLAY RECOGNITION RESULTS
    # ==========================================
    if st.session_state.recognition_result is not None:
        result = st.session_state.recognition_result
        
        if result["status"] == "success":
            emp = result["employee"]
            formatted_time = result["timestamp"].strftime("%Y-%m-%d %I:%M:%S %p")
            
            # Celebrate
            st.balloons()
            
            st.markdown(f"""
            <div class="result-card success">
                <h4 style="color: #34A853; margin-top: 0; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                    ✅ Attendance Marked Successfully!
                </h4>
                <div style="display: flex; gap: 20px; align-items: center; flex-wrap: wrap;">
                    <img src="{emp.get('photo_url', '')}" class="profile-img-preview" style="margin: 0;" />
                    <div style="flex: 1; min-width: 200px;">
                        <table style="border-collapse: collapse; width: 100%; border: none;">
                            <tr style="border: none;"><td style="font-weight: 600; padding: 4px 0; color: #5F6368; border: none;">Name:</td><td style="font-weight: 500; padding: 4px 0; border: none;">{emp.get('name', '')}</td></tr>
                            <tr style="border: none;"><td style="font-weight: 600; padding: 4px 0; color: #5F6368; border: none;">Employee ID:</td><td style="font-weight: 500; padding: 4px 0; border: none;">{emp.get('employee_id', '')}</td></tr>
                            <tr style="border: none;"><td style="font-weight: 600; padding: 4px 0; color: #5F6368; border: none;">Department:</td><td style="font-weight: 500; padding: 4px 0; border: none;">{emp.get('department', '')}</td></tr>
                            <tr style="border: none;"><td style="font-weight: 600; padding: 4px 0; color: #5F6368; border: none;">Logged At:</td><td style="font-weight: 500; padding: 4px 0; border: none;">{formatted_time}</td></tr>
                            <tr style="border: none;"><td style="font-weight: 600; padding: 4px 0; color: #5F6368; border: none;">Match Confidence:</td><td style="font-weight: 500; padding: 4px 0; border: none;">{result.get('confidence', 0.0):.1f}%</td></tr>
                        </table>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        elif result["status"] == "mismatch":
            st.markdown(f"""
            <div class="result-card warning">
                <h4 style="color: #FBBC05; margin-top: 0; margin-bottom: 8px;">{result['message']}</h4>
                <p style="margin: 0; font-size: 14px; color: #5F6368; margin-bottom: 12px;">
                    We couldn't find a matching face profile in the system database. Would you like to create a new registration record?
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action button inside Streamlit layout to go to Screen 2
            if st.button("Register New Profile Now 👤", type="primary", use_container_width=True):
                st.session_state.recognition_result = None
                st.session_state.registration_stage = "form"
                st.session_state.screen = 2
                st.rerun()
                
        elif result["status"] == "error":
            st.markdown(f"""
            <div class="result-card error">
                <h4 style="color: #EA4335; margin-top: 0; margin-bottom: 8px;">Operation Failed</h4>
                <p style="margin: 0; font-size: 14px;">{result['message']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        # Clean button to dismiss results
        if st.button("Dismiss / Clear", type="secondary"):
            st.session_state.recognition_result = None
            st.rerun()

# ==============================================================================
# SCREEN 2: EMPLOYEE REGISTRATION SCREEN
# ==============================================================================
elif st.session_state.screen == 2:
    # Header bar
    st.markdown(f"""
    <div class="header-bar">
        <div class="header-title-text">👤 Face Recognition – Employee Registration</div>
        <div>
            <span class="gemini-badge">Enrollment</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display Status Banner
    render_connection_banner()
    
    # Return button
    if st.button("← Back to Dashboard", type="secondary"):
        st.session_state.screen = 1
        st.session_state.registration_stage = "form"
        st.session_state.registration_success_data = None
        st.rerun()
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render stage: form entry vs success confirmation
    if st.session_state.registration_stage == "form":
        st.markdown('<div class="gemini-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top: 0; margin-bottom: 20px;">Enroll New Profile</h3>', unsafe_allow_html=True)
        
        # Form inputs
        reg_id = st.text_input("Employee ID (e.g. EMP1001)", placeholder="EMP1001").strip()
        reg_name = st.text_input("Full Name", placeholder="John Doe").strip()
        reg_dept = st.selectbox(
            "Department", 
            ["Engineering", "Human Resources", "Marketing", "Sales", "Operations", "Finance", "Legal"]
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Camera input for registration
        st.markdown('<h5>Capture Face Photo</h5>', unsafe_allow_html=True)
        reg_img = st.camera_input("Register Photo", label_visibility="collapsed")
        st.markdown('<p style="color: #5F6368; font-size: 13px; margin-top: -6px; text-align: center;">Position the face clearly in the camera center and look directly at the lens.</p>', unsafe_allow_html=True)
        
        submit_reg = st.button("📸 Capture & Complete Registration", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Action handler
        if submit_reg:
            # 1. Validation
            if not reg_id:
                st.error("Employee ID is required.")
            elif not reg_name:
                st.error("Full Name is required.")
            elif reg_img is None:
                st.error("Please capture a face photo using the camera input.")
            else:
                with st.spinner("Processing registration and saving details..."):
                    try:
                        # Convert image to numpy array
                        img = Image.open(io.BytesIO(reg_img.getvalue()))
                        img_np = np.array(img.convert("RGB"))
                        
                        # Extract Face Encodings
                        face_locs = face_recognition.face_locations(img_np)
                        face_encs = face_recognition.face_encodings(img_np, face_locs)
                        
                        if not face_encs:
                            st.error("❌ No face detected. Please ensure your face is fully visible with adequate lighting.")
                        elif len(face_encs) > 1:
                            st.error("❌ Multiple faces detected in frame. Only one person should be in the camera preview.")
                        else:
                            # 2. Check for duplicate employee ID in Firestore
                            dup_check = db.collection("employees").document(reg_id).get()
                            if dup_check.exists:
                                st.error(f"❌ Employee ID '{reg_id}' is already registered in the system.")
                            else:
                                # 3. Save photo & obtain URL
                                img_bytes = reg_img.getvalue()
                                photo_url = ""
                                
                                if storage_active:
                                    # Upload to Firebase Storage
                                    blob_path = f"photos/{reg_id}.jpg"
                                    blob = bucket.blob(blob_path)
                                    blob.upload_from_string(img_bytes, content_type="image/jpeg")
                                    blob.make_public()
                                    photo_url = blob.public_url
                                else:
                                    # Storage inactive fallback: Base64 encoding saved in Firestore
                                    b64_str = base64.b64encode(img_bytes).decode("utf-8")
                                    photo_url = f"data:image/jpeg;base64,{b64_str}"
                                    
                                # 4. Store metadata in Firestore
                                employee_record = {
                                    "employee_id": reg_id,
                                    "name": reg_name,
                                    "department": reg_dept,
                                    "face_encoding": face_encs[0].tolist(),  # Store list of floats
                                    "photo_url": photo_url,
                                    "registered_at": datetime.now(timezone.utc)
                                }
                                
                                db.collection("employees").document(reg_id).set(employee_record)
                                
                                # Clear local cache to force reload
                                fetch_and_cache_employees(force=True)
                                
                                # Move to success screen
                                st.session_state.registration_success_data = employee_record
                                st.session_state.registration_stage = "success"
                                st.rerun()
                                
                    except Exception as e:
                        st.error(f"Registration Failed: {e}")
                        
    elif st.session_state.registration_stage == "success":
        st.balloons()
        emp_data = st.session_state.registration_success_data
        
        st.markdown('<div class="gemini-card" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: #34A853; margin-top: 0;">🎉 Registration Completed!</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #5F6368; font-size: 15px; margin-bottom: 20px;">Profile registered successfully under Employee ID: <b>{emp_data.get("employee_id")}</b></p>', unsafe_allow_html=True)
        
        # Profile image preview
        st.markdown(f'<img src="{emp_data.get("photo_url")}" class="profile-img-preview" />', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="max-width: 300px; margin: 0 auto 24px auto; text-align: left;">
            <p style="margin: 6px 0;"><b>Name:</b> {emp_data.get("name")}</p>
            <p style="margin: 6px 0;"><b>Department:</b> {emp_data.get("department")}</p>
            <p style="margin: 6px 0;"><b>Status:</b> Biometrics Encoded</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Return to Dashboard", type="primary", use_container_width=True):
            st.session_state.screen = 1
            st.session_state.registration_stage = "form"
            st.session_state.registration_success_data = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
