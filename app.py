import streamlit as st
import pandas as pd
import random

# تحميل أسماء من ملف Excel
def upload_file():
    uploaded_file = st.file_uploader("اختر ملف Excel", type=["xlsx", "xls"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        return df.iloc[:, 0].dropna().tolist()
    return []

# عرض الأسماء
def show_names(names):
    st.write("الأسماء المدخلة:", len(names))
    st.write(names)

# إجراء القرعة
def draw_lottery(names, num_winners):
    if names:
        if 1 <= num_winners <= len(names):
            winners = random.sample(names, num_winners)
            st.write("اسماء الفائزين:", len(winners))
            st.write(winners)
            return winners
        else:
            st.warning("يرجى إدخال عدد صحيح من 1 إلى عدد الأسماء.")
    else:
        st.warning("يرجى تحميل الأسماء أولاً.")

from io import BytesIO
import pandas as pd

# حفظ الفائزين بصيغة Excel باستخدام openpyxl
def download_winners(winners):
    if winners:
        df = pd.DataFrame(winners, columns=["أسماء الفائزين"])
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:  # استخدام openpyxl كبديل
            df.to_excel(writer, index=False, sheet_name="الفائزين")
        st.download_button(
            label="تحميل الفائزين",
            data=output.getvalue(),
            file_name="winners.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("لم يتم إجراء القرعة بعد.")



# إعداد واجهة التطبيق
st.title("قرعة المهندسين Newgen ")
names = upload_file()

if names:
    if st.button("إظهار الأسماء"):
        show_names(names)

    num_winners = st.number_input("أدخل عدد الفائزين المطلوب", min_value=1, max_value=len(names), step=1)
    if st.button("إجراء القرعة"):
        winners = draw_lottery(names, num_winners)
        download_winners(winners)
