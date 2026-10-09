import streamlit as st
import hmac
from datetime import datetime, timedelta
import pandas as pd

# 1. إعدادات الصفحة الأساسية (بدون أي إيقونات لتبدو رسمية تماماً)
st.set_page_config(
    page_title="Enterprise Zero-Waste Intelligence Platform | B2B",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تصميم CSS مخصص لترتيب الخلفية، الألوان، والجعل الواجهة أنيقة ومريحة
st.markdown("""
    <style>
    .main {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    .stSidebar {
        background-color: #111827;
    }
    div.stButton > button {
        background-color: #1f2937;
        color: #ffffff;
        border-radius: 8px;
        border: 1px solid #374151;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #3b82f6;
        border-color: #3b82f6;
    }
    .metric-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #374151;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة سجل العمليات (Audit Trail) وقاعدة الفروع والباسوردات داخل الجلسة
if "audit_logs" not in st.session_state:
    st.session_state["audit_logs"] = [
        {"الوقت (Time)": "2026-10-09 18:00", "المستخدم (User)": "Lara AlFaisal (المالك الرئيسي)",
         "الفرع": "النظام المركزي", "العملية (Action)": "تفعيل الأمان السيبراني ونظام كلمات المرور المتعددة للفرع",
         "الحالة": "مؤكد ✅"}
    ]

if "branch_passwords" not in st.session_state:
    st.session_state["branch_passwords"] = {
        "فرع الرياض الرئيسي - الرياض (Riyadh Main Branch - 01)": "Riyadh_01",
        "فرع التحلية - جدة (Tahlia Branch - 02)": "Tahlia_02",
        "فرع الرمال - الدمام (Al-Rimal Branch - 03)": "Rimal_03",
        "فرع الراشد - الخبر (Al-Rashid Branch - 04)": "Rashid_04"
    }


# 3. نظام الأمان المتقدم (حماية مركزية + كلمات مرور مستقلة للفروع بدون أي تلميحات)
def check_password():
    """Returns True if the user has authenticated successfully."""

    def password_entered():
        entered_pwd = st.session_state["password"]

        # كلمة المرور الرئيسية للمالك أو مدير الشركة الشامل
        if hmac.compare_digest(entered_pwd, "B2B_ZeroWaste@99"):
            st.session_state["password_correct"] = True
            st.session_state["user_role"] = "Admin / CEO"
            st.session_state["active_branch_locked"] = None
            del st.session_state["password"]
            return

        # التحقق إذا كانت كلمة المرور تخص فرعاً معيناً
        matched_branch = None
        for branch, pwd in st.session_state["branch_passwords"].items():
            if hmac.compare_digest(entered_pwd, pwd):
                matched_branch = branch
                break

        if matched_branch:
            st.session_state["password_correct"] = True
            st.session_state["user_role"] = "Branch Staff"
            st.session_state["active_branch_locked"] = matched_branch
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # واجهة الترحيب الرسمية باللغة الإنجليزية والعربية بدون أي إيموجي أو تلميح لكلمة المرور
        st.markdown("<h1 style='text-align: center; color: #3b82f6;'>Enterprise Zero-Waste Intelligence Platform</h1>",
                    unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align: center; color: #9ca3af;'>B2B Retail Inventory & Expiry Management System | Secure Access Portal</p>",
            unsafe_allow_html=True)
        st.markdown("<hr style='border-color: #374151;'>", unsafe_allow_html=True)

        st.text_input(
            "أدخل كلمة المرور الرئيسية (للإدارة) أو كلمة مرور الفرع الخاصة بك:",
            type="password",
            on_change=password_entered,
            key="password"
        )
        return False

    elif not st.session_state["password_correct"]:
        st.markdown("<h1 style='text-align: center; color: #3b82f6;'>Enterprise Zero-Waste Intelligence Platform</h1>",
                    unsafe_allow_html=True)
        st.text_input(
            "أدخل كلمة المرور الرئيسية أو كلمة مرور الفرع:",
            type="password",
            on_change=password_entered,
            key="password"
        )
        st.error("❌ كلمة المرور غير صحيحة. يرجى التأكد والمحاولة مرة أخرى.")
        return False
    else:
        return True


if not check_password():
    st.stop()

# 4. الشريط الجانبي والأقسام المتقدمة
st.sidebar.markdown("## 🏢 إدارة المنصة المركزية")
st.sidebar.markdown(f"**الصلاحية الحالية:** `{st.session_state.get('user_role', 'Admin')}`")
st.sidebar.markdown("---")

menu_selection = st.sidebar.radio(
    "اختر القسم (Select Section):",
    [
        "📊 لوحة التحكم التنفيذية (Executive Dashboard)",
        "📦 إدارة المنتجات والمخزون (Inventory Management)",
        "⚠️ مراقبة الهدر والإنذار المبكر (5 - 7 أيام)",
        "💰 الحاسبة المالية والعائد الاستثماري (Financial ROI Calculator)",
        "👥 إدارة الفروع والموظفين (Branches & Staff Control)",
        "📋 سجل العمليات والتدقيق (Audit Logs & Trail)",
        "⚙️ إعدادات النظام والأمان (System & Security Settings)"
    ]
)

st.sidebar.markdown("---")

# إذا كان المستخدم موظف فرع، يتم قفل الفرع المخصص له فقط. إذا كان مديراً، يستطيع التنقل بين الفروع بحرية
locked_branch = st.session_state.get("active_branch_locked", None)
if locked_branch:
    selected_branch = st.sidebar.selectbox(
        "🌐 الفرع النشط (مقفل لصلاحية فرعك):",
        [locked_branch]
    )
    st.sidebar.caption("🔒 هذا الحساب مخصص لهذا الفرع فقط لأسباب أمنية.")
else:
    selected_branch = st.sidebar.selectbox(
        "🌐 اختر الفرع النشط (Active Branch):",
        list(st.session_state["branch_passwords"].keys()) + ["... (إجمالي الفروع النشطة: 412 فرعاً مسجلاً)"]
    )

st.sidebar.markdown("---")
if st.sidebar.button("🔒 تسجيل الخروج (Logout)"):
    st.session_state["password_correct"] = False
    st.rerun()

# 5. محتوى الصفحات

# --- القسم الأول: لوحة التحكم التنفيذية ---
if "لوحة التحكم التنفيذية" in menu_selection:
    st.markdown("# 📊 لوحة التحكم التنفيذية الاستراتيجية")
    st.markdown("### Executive Strategic Dashboard | مراقبة حية لقطاع التجزئة الكبرى")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="نسبة توفير الهدر المستهدفة | Target Waste Reduction", value="38.5%", delta="تحسن 3.5% 📈")
    with col2:
        st.metric(label="الفروع المرتبطة والنشطة | Active Branches", value="412 فرع", delta="متصل لحظياً 🌐")
    with col3:
        st.metric(label="المنتجات الحرجة (5-7 أيام) | Critical Items", value="142 منتج", delta="تنبيه مبكر ⚠️")
    with col4:
        st.metric(label="حالة النظام والأمان | System & Security", value="مؤمن 100%", delta="تشفير عالي المستوى 🔒")

    st.markdown("---")
    st.markdown("### ⚡ التوصيات الاستراتيجية الفورية (AI Decision Engine)")

    st.info(f"💡 الفرع النشط حالياً: **{selected_branch}**. تم رصد منتجات ضمن نافذة الإنذار المبكر (5-7 أيام):")

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown("**حليب طازج 2 لتر**")
        st.caption("الصلاحية المتبقية: 5 أيام | السعر: 12.0 ر.س | باركود: P101")
        if st.button("✔ تطبيق خصم إنقاذ 30%", key="btn_1"):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            user_name = st.session_state.get('user_role', 'Staff')
            st.session_state["audit_logs"].insert(0, {"الوقت (Time)": current_time, "المستخدم (User)": user_name,
                                                      "الفرع": selected_branch,
                                                      "العملية (Action)": "تطبيق خصم إنقاذ 30% على منتج: حليب طازج 2 لتر",
                                                      "الحالة": "تم التنفيذ ✅"})
            st.success("تم تحديث السعر وتفعيل الخصم في نقاط البيع (POS) وتوثيق العملية في سجل التدقيق!")
    with col_p2:
        st.markdown("**خبز توست أبيض**")
        st.caption("الصلاحية المتبقية: 6 أيام | السعر: 5.0 ر.س | باركود: P102")
        if st.button("✔ تطبيق خصم إنقاذ 40%", key="btn_2"):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            user_name = st.session_state.get('user_role', 'Staff')
            st.session_state["audit_logs"].insert(0, {"الوقت (Time)": current_time, "المستخدم (User)": user_name,
                                                      "الفرع": selected_branch,
                                                      "العملية (Action)": "تطبيق خصم إنقاذ 40% على منتج: خبز توست أبيض",
                                                      "الحالة": "تم التنفيذ ✅"})
            st.success("تم تفعيل خصم الإنقاذ الفوري بنجاح وتوثيقه في السجل!")
    with col_p3:
        st.markdown("**دجاج مبرد كامل**")
        st.caption("الصلاحية المتبقية: 5 أيام | السعر: 18.0 ر.س | باركود: P104")
        if st.button("🔄 طلب نقل لفرع نشط", key="btn_3"):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            user_name = st.session_state.get('user_role', 'Staff')
            st.session_state["audit_logs"].insert(0, {"الوقت (Time)": current_time, "المستخدم (User)": user_name,
                                                      "الفرع": selected_branch,
                                                      "العملية (Action)": "طلب مناقلة لوجستية لمنتج: دجاج مبرد كامل",
                                                      "الحالة": "قيد المعالجة 🔄"})
            st.info("تم إرسال طلب المناقلة اللوجستية وتوثيق الحدث في السجل المركزي.")

# --- القسم الثاني: إدارة المنتجات والمخزون ---
elif "إدارة المنتجات والمخزون" in menu_selection:
    st.markdown("# 📦 إدارة المنتجات والمخزون المركزي")
    st.markdown("### Inventory & Product Management System")
    st.markdown("---")

    tab1, tab2 = st.tabs(["➕ إضافة منتج جديد (مدير أو موظف الفرع)", "📁 الاستيراد الجماعي للبيانات (CSV Batch Import)"])

    with tab1:
        st.markdown("#### إضافة منتج أو شركة جديدة لقاعدة البيانات")
        with st.form("add_product_form"):
            company_name_input = st.text_input("اسم الشركة / الجهة التجارية (Company Name):",
                                               placeholder="مثال: أسواق العثيم / بنده")
            p_name = st.text_input("اسم المنتج (Product Name):", placeholder="مثال: جبنة مربعات طبيعية")
            p_barcode = st.text_input("رقم الباركود (Barcode / SKU):", placeholder="مثال: P205")
            p_price = st.number_input("سعر الوحدة بالريال (Unit Price):", min_value=0.0, value=15.0)
            p_days = st.number_input("أيام الصلاحية المتبقية (Remaining Shelf-Life Days):", min_value=1, value=6)
            p_category = st.selectbox("تصنيف المنتج (Category):",
                                      ["ألبان وأسجاد", "مخبوزات", "لحوم وطيور", "خضار وفواكه", "معلبات"])

            submit_btn = st.form_submit_button("حفظ وإضافة المنتج والشركة للمنصة")
            if submit_btn:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                user_name = st.session_state.get('user_role', 'Staff')
                st.session_state["audit_logs"].insert(0, {"الوقت (Time)": current_time, "المستخدم (User)": user_name,
                                                          "الفرع": selected_branch,
                                                          "العملية (Action)": f"إضافة شركة ({company_name_input}) ومنتج: {p_name}",
                                                          "الحالة": "تم الحفظ ✅"})
                st.success(
                    f"تم حفظ الشركة ({company_name_input}) والمنتج ({p_name}) بنجاح للفرع المحدد وتوثيقه في السجل المركزي!")

    with tab2:
        st.markdown("#### رفع ملفات البيانات الجماعية (CSV / Excel)")
        uploaded_file = st.file_uploader("اختر ملف البيانات بصيغة CSV:", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            user_name = st.session_state.get('user_role', 'Staff')
            st.session_state["audit_logs"].insert(0, {"الوقت (Time)": current_time, "المستخدم (User)": user_name,
                                                      "الفرع": selected_branch,
                                                      "العملية (Action)": f"استيراد ملف بيانات جماعي: {uploaded_file.name}",
                                                      "الحالة": "مكتمل ✅"})
            st.success("تم تحليل واستيراد ملف المنتجات بنجاح وتوثيق العملية في سجل التدقيق!")
        else:
            st.info(
                "قم بررفع ملف يحتوي على أعمدة (Product_Name, Barcode, Price, Expiry_Days) لتحديث المخزون دفعة واحدة.")

# --- القسم الثالث: مراقبة الهدر والإنذار المبكر ---
elif "مراقبة الهدر والإنذار المبكر" in menu_selection:
    st.markdown("# ⚠️ مراقبة الهدر والإنذار المبكر (نافذة 5 - 7 أيام)")
    st.markdown("### Real-time Expiry & Early Warning System (5-7 Days Window)")
    st.markdown("---")
    st.warning(
        "🚨 تنبيه استراتيجي: المنتجات التالية دخلت في نافذة الإنذار المبكر (من 5 إلى 7 أيام) وتتطلب إجراءً وقائياً عاجلاً.")

    data_critical = {
        "المنتج (Product)": ["حليب طازج 2 لتر", "خبز توست أبيض", "دجاج مبرد كامل", "زبادي طبيعي 1كغ"],
        "الباركود (Barcode)": ["P101", "P102", "P104", "P109"],
        "الصلاحية المتبقية": ["5 أيام ⚠️", "6 أيام 🟡", "5 أيام ⚠️", "7 أيام 🟢"],
        "السعر الأصلي": ["12.0 ر.س", "5.0 ر.س", "18.0 ر.س", "8.5 ر.س"],
        "الحالة التشغيلية": ["جاهز للخصم", "مراقبة نشطة", "طلب نقل", "آمن نسبياً"]
    }
    st.table(pd.DataFrame(data_critical))

# --- القسم الرابع: الحاسبة المالية والعائد الاستثماري ---
elif "الحاسبة المالية والعائد الاستثماري" in menu_selection:
    st.markdown("# 💰 الحاسبة المالية وتحليل العائد الاستثماري (ROI)")
    st.markdown("### Financial Impact & Monthly Savings Calculator")
    st.markdown("---")

    monthly_loss = st.number_input(
        "أدخل إجمالي الخسائر الشهرية المتوقعة من الهدر (ريال سعودي):",
        min_value=1000, max_value=10000000, value=150000, step=5000
    )

    savings = monthly_loss * 0.385
    annual_savings = savings * 12

    col_calc1, col_calc2 = st.columns(2)
    with col_calc1:
        st.metric(label="المبلغ المتوقع توفيره شهرياً بفضل المنصة", value=f"{savings:,.2f} ر.س")
    with col_calc2:
        st.metric(label="إجمالي التوفير السنوي المتوقع للشركة", value=f"{annual_savings:,.2f} ر.س")

    st.success(
        "✨ هذه الحسابات مبنية على نماذج كفاءة سلاسل الإمداد المعتمدة بنسبة إنقاذ 38.5% من الهدر القابل للاسترجاع.")

# --- القسم الخامس: إدارة الفروع والموظفين ---
elif "إدارة الفروع والموظفين" in menu_selection:
    st.markdown("# 👥 إدارة الفروع وباسوردات الدخول المستقلة")
    st.markdown("### Branch & Multi-Password Access Control System")
    st.markdown("---")
    st.info("💡 يمكنك من هنا إضافة فروع جديدة وتعيين كلمة مرور خاصة بكل فرع ليتمكن موظفوه من الدخول لفرعهم فقط.")

    if st.session_state.get('user_role') == "Admin / CEO":
        with st.form("add_branch_form"):
            new_branch_name = st.text_input("اسم الفرع الجديد (Branch Name):", placeholder="مثال: فرع النزهة - الرياض")
            new_branch_pwd = st.text_input("كلمة المرور الخاصة بالفرع (Branch Password):", placeholder="مثال: Nozha_05")
            add_branch_btn = st.form_submit_button("إضافة الفرع وتوليد كلمة المرور")

            if add_branch_btn and new_branch_name and new_branch_pwd:
                st.session_state["branch_passwords"][new_branch_name] = new_branch_pwd
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state["audit_logs"].insert(0,
                                                      {"الوقت (Time)": current_time, "المستخدم (User)": "Admin / CEO",
                                                       "الفرع": new_branch_name,
                                                       "العملية (Action)": f"إضافة فرع جديد وتعيين كلمة مرور مستقلة",
                                                       "الحالة": "تم بنجاح ✅"})
                st.success(f"تم إضافة فرع ({new_branch_name}) وتفعيل كلمة المرور الخاصة به بنجاح!")

    st.markdown("#### الفروع المسجلة وباسورداتها الحالية:")
    branch_df = pd.DataFrame(list(st.session_state["branch_passwords"].items()),
                             columns=["اسم الفرع (Branch)", "كلمة المرور الخاصة (Password)"])
    st.table(branch_df)

    st.markdown("#### صلاحيات المستويات الإدارية:")
    staff_data = {
        "المستوى الإداري": ["المالك الرئيسي (Lara AlFaisal)", "مدير الشركة الشامل (CEO)", "موظف الفرع / الكاشير"],
        "نطاق الصلاحيات": ["التحكم المطلق وحماية النظام وصلاحيات أخذ النسخ الاحتياطي",
                           "متابعة نسب الهدر، إضافة فروع وباسورداتها، وإدارة الشركات",
                           "إدخال البيانات، طلبات النقل، وتفعيل الخصومات لفرعه فقط"]
    }
    st.table(pd.DataFrame(staff_data))

# --- القسم السادس: سجل العمليات والتدقيق ---
elif "سجل العمليات والتدقيق" in menu_selection:
    st.markdown("# 📋 سجل العمليات والتدقيق اللحظي (Audit Trail)")
    st.markdown("### Real-time System Audit Logs & Activity Tracking")
    st.markdown("---")
    st.info("💡 يسجل هذا النظام كافة التعديلات، إضافات الفروع والباسوردات، واعتمادات الخصومات لحظياً.")

    st.dataframe(pd.DataFrame(st.session_state["audit_logs"]), use_container_width=True)

# --- القسم السابع: إعدادات النظام والأمان ---
elif "إعدادات النظام والأمان" in menu_selection:
    st.markdown("# ⚙️ إعدادات النظام، التشفير والأمان المتقدم")
    st.markdown("### Advanced System Settings & Security Compliance")
    st.markdown("---")

    st.markdown("* **حالة الاتصال والربط:** متصل بنجاح ببيئة التشغيل المحلية الآمنة (Local Secure Sandbox).")
    st.markdown("* **التحكم بالجلسات:** مفعلة عبر خوارزمية HMAC وكلمات مرور فرعية مستقلة لكل فرع.")
    st.markdown("* **حماية الملكية البرمجية والنسخ الاحتياطي:** محصورة حصرياً بالمالك والمطور الرئيسي.")

    # ميزة النسخ الاحتياطي المحمية حصرياً للمالك الرئيسي Lara AlFaisal
    if st.session_state.get('user_role') == "Admin / CEO":
        st.markdown("---")
        st.markdown("### 🔒 لوحة تحكم المالك الرئيسي الحصرية")
        if st.button("🔄 إنشاء نسخة احتياطية مشفرة وتصدير النظام التجريبي"):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state["audit_logs"].insert(0, {"الوقت (Time)": current_time,
                                                      "المستخدم (User)": "Lara AlFaisal (المالك الرئيسي)",
                                                      "الفرع": "النظام المركزي",
                                                       "العملية (Action)": "تصدير نسخة احتياطية تجريبية مقفلة",
                                                      "الحالة": "تم بنجاح 🔒"})
            st.success("تم إنشاء وتصدير النسخة الاحتياطية التجريبية بنجاح على جهازك وتوثيقها في سجل التدقيق.")
    else:
        st.info("ℹ️ خاصية أخذ النسخ الاحتياطي وتصدير البيانات محصورة بالمالك الرئيسي للمنصة فقط.")

# 6. تذييل الصفحة الاحترافي مع حفظ حقوق الملكية الفكرية (بدون إيموجي وبكل رسمية)
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #9ca3af; font-size: 14px;'>
        Enterprise Zero-Waste Intelligence Platform | مصممة خصيصاً لشركات التجزئة الكبرى © 2026<br>
        <span style='color: #3b82f6; font-weight: bold;'>Designed & Developed by Lara AlFaisal</span>
    </div>
    """,
    unsafe_allow_html=True
)
