from datetime import date
import streamlit as st

l1 = ['Abhishek kumar', 'Altaf Hussain', 'Anoop Kumar verma', 'Gaurav Kashya', 'Jay Vardha',
    'Kashish Pandey', 'Neha Gautam', 'Pratyaksh Yadav', 'Prem Mohan', 'Priya Singh',
    'Ranjeet Kumar', 'Sandeep Balmiki', 'Saumya', 'Shreya Singh', 'Sonam Pal']

l2 = list(reversed(l1))

record_file = 'records.txt'

try:
    with open(record_file, 'r') as f:
        pass
except FileNotFoundError:
    with open(record_file, 'w') as f:
        f.write("date,Name1,status1,Name2,status2\n")

if 'index1' not in st.session_state:
    st.session_state.index1 = 0
if 'index2' not in st.session_state:
    st.session_state.index2 = 0
if 'name1' not in st.session_state:
    st.session_state.name1 = None
if 'name2' not in st.session_state:
    st.session_state.name2 = None
if 'role1' not in st.session_state:
    st.session_state.role1 = None
if 'role2' not in st.session_state:
    st.session_state.role2 = None

def is_done(name):
    with open(record_file, 'r') as file:
        for line in file.readlines()[1:]:
            parts = line.strip().split(',')
            if len(parts) == 5:
                _, n1, s1, n2, s2 = parts
                if (n1 == name and s1 == 'done') or (n2 == name and s2 == 'done'):
                    return True
    return False

def get_one_name(l, index_key, name_key, role_key, list_id):
    idx = st.session_state[index_key]

    while idx < len(l):
        current_name = l[idx]
        if is_done(current_name):
            idx += 1
            continue

        st.write(f"Is **{current_name}** available?")
        response = st.text_input(f"Answer for {current_name} (Yes/No)", key=f"input_{list_id}")
        if response.lower().strip() == 'yes':
            if not st.session_state[role_key]:  # Only ask for the role if it's not already set
                role = st.text_input(f"Is {current_name} Tech or Non-Tech?", key=f"role_{list_id}")
                if st.button("Submit", key=f"btn_{list_id}"):
                    if role.lower().strip() == 'tech':
                        st.session_state[role_key] = 'Tech'
                        st.session_state.role2 = 'Non-Tech'
                    elif role.lower().strip() == 'non-tech':
                        st.session_state[role_key] = 'Non-Tech'
                        st.session_state.role2 = 'Tech'
                    st.session_state[name_key] = current_name
                    st.session_state[index_key] = idx + 1
                    st.rerun()
            else:
                st.session_state[name_key] = current_name
                st.session_state[index_key] = idx + 1
                st.rerun()
        elif response.lower().strip() == 'no':
            st.session_state[index_key] = idx + 1
            st.rerun()

        break

# Sidebar for options
st.sidebar.title("Options")
option = st.sidebar.radio("Choose an action:", ["Make Pair", "Manually Add Pair", "Clear All Pairs"])

if option == "Make Pair":
    st.title("Available Users Pairing")
    st.write(f"Date: {date.today()}")

    if not st.session_state.name1:
        get_one_name(l1, 'index1', 'name1', 'role1', 'list1')

    if not st.session_state.name2:
        get_one_name(l2, 'index2', 'name2', 'role2', 'list2')

    if st.session_state.name1 and st.session_state.name2:
        with open(record_file, 'a') as file:
            file.write(f"{date.today()},{st.session_state.name1},done,{st.session_state.name2},done\n")
        st.success(f"✅  {st.session_state.name1} ({st.session_state.role1}) and {st.session_state.name2} ({st.session_state.role2})")
        
        st.session_state.name1 = None
        st.session_state.name2 = None
        st.session_state.role1 = None
        st.session_state.role2 = None
        st.session_state.index1 += 1
        st.session_state.index2 += 1

elif option == "Manually Add Pair":
    st.title("Manually Add Pair")
    name1 = st.text_input("Enter Name 1:")
    role1 = st.selectbox("Role for Name 1:", ["Tech", "Non-Tech"])
    name2 = st.text_input("Enter Name 2:")
    role2 = st.selectbox("Role for Name 2:", ["Tech", "Non-Tech"])
    if st.button("Add Pair"):
        with open(record_file, 'a') as file:
            file.write(f"{date.today()},{name1},done,{name2},done\n")
        st.success(f"✅ Pair added: {name1} ({role1}) and {name2} ({role2})")

elif option == "Clear All Pairs":
    st.title("Clear All Pairs")
    if st.button("Clear"):
        with open(record_file, 'w') as file:
            file.write("date,Name1,status1,Name2,status2\n")
        st.success("✅ All pairs cleared.")
