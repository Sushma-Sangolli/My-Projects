import streamlit as st
import mysql.connector

# Custom CSS for Styling
st.markdown(
    """
    <style>
        /* Set the full background color to sky blue */
        .stApp {
            background-color: skyblue;
        }
        
        /* Set label background to white and text to black */
        div[data-testid="stForm"] label,
        div[data-testid="stWidgetLabel"] {
            background-color: white !important;
            color: black !important;
            padding: 5px;
            border-radius: 5px;
        }

        /* Change input text to black */
        input, textarea {
            color: black !important;
            background-color: white !important;
            border: 1px solid black !important;
        }

        /* Change number input box text to black */
        .stNumberInput input {
            color: black !important;
            background-color: white !important;
        }
        
        /* Change buttons to black background with white text */
        .stButton>button {
            color: white !important;
            background-color: black !important;
            border: 2px solid white !important;
            padding: 5px 10px;
            font-weight: bold;
        }

        /* Change sidebar text to white */
        .css-1d391kg p, .css-1d391kg span {
            color: white !important;
        }

        /* Change success and error message backgrounds */
        .stAlert {
            background-color: white !important;
            color: black !important;
            border-left: 5px solid black !important;
        }
        /* Change input labels and success messages to black */
        div[data-testid="stWidgetLabel"] label, .stAlert {
            color: black !important;
        }
            /* Make success message text black */
        .stAlert {
            color: black !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# MySQL Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  
        port=3306,
        user="root",  
        password="root",  
        database="employee_db"
    )

# Insert Employee Function
def insert_employee(emp_id, name, department, salary):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO employees (id, name, department, salary) VALUES (%s, %s, %s, %s)", 
                       (emp_id, name, department, salary))
        conn.commit()
        st.success("✅ Employee added successfully!")
    except mysql.connector.Error as err:
        st.error(f"❌ Database Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Fetch Employee Function
def fetch_employee(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, department, salary FROM employees WHERE id = %s", (emp_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# Streamlit UI
st.title("🏢 Employee Management System")

menu = st.sidebar.selectbox("📌 Menu", ["Add Employee", "Fetch Employee"])

# Add Employee Form
if menu == "Add Employee":
    st.header("🆕 Add Employee")

    emp_id = st.number_input("Employee ID", min_value=1, step=1)
    name = st.text_input("Employee Name")
    department = st.text_input("Department")
    salary = st.number_input("Salary", min_value=0.0, step=0.01)

    if st.button("Submit"):
        if emp_id and name and department and salary:
            insert_employee(emp_id, name, department, salary)
        else:
            st.error("⚠️ All fields are required!")

# Fetch Employee Details
elif menu == "Fetch Employee":
    st.header("🔍 Fetch Employee Details")
    emp_id = st.number_input("Enter Employee ID", min_value=1, step=1)

    if st.button("Fetch"):
        result = fetch_employee(emp_id)
        if result:
            st.write(f"** Name:** {result[0]}")
            st.write(f"** Department:** {result[1]}")
            st.write(f"** Salary:** ₹{result[2]}")
        else:
            st.error("❌ Employee not found!")
