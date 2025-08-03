# import streamlit as st
# from backend.chat_handler import (
#     add_user, get_all_users, save_message,
#     get_chat_history, save_meeting_to_db,
#     clear_chat_history, get_user_name_by_email,
#     delete_user
# )
# from backend.meeting_logic import try_schedule_meeting
# from backend.emailer import send_confirmation_email

# st.set_page_config(page_title="🤖 AI Meeting Scheduler", layout="centered")
# st.title("🧠  ZenithMeet : AI-Powered Smart Meeting Scheduler")
# st.subheader("Chat-based group meeting scheduler")

# st.sidebar.title("👤 Register")
# name_input = st.sidebar.text_input("Your Name")
# email_input = st.sidebar.text_input("Your Email")

# if st.sidebar.button("➕ Register"):
#     if name_input and email_input:
#         add_user(name_input, email_input)
#         st.success("✅ Registered Successfully!")
#         st.rerun()
#     else:
#         st.sidebar.warning("Please enter both name and email.")

# st.sidebar.markdown("---")

# user_list = get_all_users()
# user_options = [f"{u['name']} ({u['email']})" for u in user_list]
# selected_user = st.sidebar.selectbox("🧑 Select user to login & chat", options=["-- Select --"] + user_options)

# if selected_user != "-- Select --":
#     selected_email = selected_user.split("(")[-1].strip(")")
#     selected_name = selected_user.split("(")[0].strip()
#     st.session_state["logged_in"] = True
#     st.session_state["name"] = selected_name
#     st.session_state["email"] = selected_email

#     st.sidebar.markdown("---")
#     st.sidebar.markdown("### ⚠️ Danger Zone")
#     confirmed = st.sidebar.checkbox("✔️ Confirm Delete")
#     if st.sidebar.button("🗑️ Delete This User"):
#         if confirmed:
#             deleted = delete_user(selected_email)
#             if deleted:
#                 st.sidebar.success(f"🗑️ User '{selected_name}' deleted successfully!")
#                 st.session_state.clear()
#                 st.rerun()
#             else:
#                 st.sidebar.error("❌ Could not delete the user.")
#         else:
#             st.sidebar.warning("☝️ Please confirm before deleting.")

# if st.session_state.get("logged_in", False):
#     user_name = st.session_state["name"]
#     user_email = st.session_state["email"]
#     st.success(f"Welcome, {user_name}!")

#     st.markdown("### 🗨️ Group Chat History")
#     history = get_chat_history()
#     for row in history:
#         with st.chat_message("user"):
#             st.markdown(f"**{row['name']}**: {row['message']}\n\n🕒 *{row['timestamp']}*")

#     message = st.chat_input("Type your message here...")
#     if message:
#         save_message(add_user(user_name, user_email), message)
#         st.rerun()

#     st.markdown("---")
#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("📅 Schedule Meeting"):
#             with st.spinner("🔍 Analyzing with Gemini..."):
#                 success, msg, data = try_schedule_meeting()

#             if not success:
#                 st.error(msg)
#             else:
#                 save_meeting_to_db(data["participants"], data["time"], data["place"], user_email)
#                 email_status = send_confirmation_email(data["participants"], data["time"], data["place"])
#                 names = [get_user_name_by_email(p) or p.split("@")[0] for p in data["participants"]]
#                 st.success("✅ Meeting Scheduled!")
#                 st.markdown(f"""
# **📅 Date & Time:** {data["time"]} IST  
# **📍 Venue:** {data["place"]}  
# **👥 Participants:** {', '.join(names)}
# """)
#                 st.success("📧 Email confirmation sent." if email_status else "❌ Failed to send email.")

#     with col2:
#         if st.button("🗑️ Clear Chat History"):
#             clear_chat_history()
#             st.success("🧹 Chat history cleared.")
#             st.rerun()
# else:
#     st.warning("Please register and select your user to start chatting and scheduling.")

import streamlit as st
from datetime import datetime
from pytz import timezone

from backend.chat_handler import (
    add_user, get_all_users, save_message,
    get_chat_history, save_meeting_to_db,
    clear_chat_history, get_user_name_by_email,
    delete_user
)
from backend.meeting_logic import try_schedule_meeting
from backend.emailer import send_confirmation_email

IST = timezone("Asia/Kolkata")

st.set_page_config(page_title="AI Meeting Scheduler", layout="centered")
st.title("🕑ZenithMeet : AI-Powered Smart Meeting Scheduler")
st.subheader("Chat-based group meeting scheduler")

# ---------------- Sidebar -----------------
st.sidebar.title("👤 Register")
name_input = st.sidebar.text_input("Your Name")
email_input = st.sidebar.text_input("Your Email")

if st.sidebar.button("➕ Register"):
    if name_input and email_input:
        add_user(name_input, email_input)
        st.success("✅ Registered Successfully!")
        st.rerun()
    else:
        st.sidebar.warning("Please enter both name and email.")

st.sidebar.markdown("---")

user_list = get_all_users()
user_options = [f"{u['name']} ({u['email']})" for u in user_list]
selected_user = st.sidebar.selectbox("🧑 Select user to login & chat", options=["-- Select --"] + user_options)

if selected_user != "-- Select --":
    selected_email = selected_user.split("(")[-1].strip(")")
    selected_name = selected_user.split("(")[0].strip()
    st.session_state["logged_in"] = True
    st.session_state["name"] = selected_name
    st.session_state["email"] = selected_email

    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚠️ Danger Zone")
    confirmed = st.sidebar.checkbox("✔️ Confirm Delete")
    if st.sidebar.button("🗑️ Delete This User"):
        if confirmed:
            deleted = delete_user(selected_email)
            if deleted:
                st.sidebar.success(f"🗑️ User '{selected_name}' deleted successfully!")
                st.session_state.clear()
                st.rerun()
            else:
                st.sidebar.error("❌ Could not delete the user.")
        else:
            st.sidebar.warning("☝️ Please confirm before deleting.")

# ---------------- Main Chat Interface -----------------
if st.session_state.get("logged_in", False):
    user_name = st.session_state["name"]
    user_email = st.session_state["email"]
    st.success(f"Welcome, {user_name}!")

    st.markdown("### 🗨️ Group Chat History")
    history = get_chat_history()
    for row in history:
        try:
            dt = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S")
            dt_ist = dt.strftime("%Y-%m-%d %I:%M %p") + " IST"  # 👈 No timezone shift here
        except:
            dt_ist = row['timestamp']  # fallback if parsing fails
    
        with st.chat_message("user"):
            st.markdown(f"**{row['name']}**: {row['message']}\n\n🕒 *{dt_ist}*")


    message = st.chat_input("Type your message here...")
    if message:
        save_message(add_user(user_name, user_email), message)
        st.rerun()

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📅 Schedule Meeting"):
            with st.spinner("🔍 Analyzing with Gemini..."):
                success, msg, data = try_schedule_meeting()

            if not success:
                st.error(msg)
            else:
                save_meeting_to_db(data["participants"], data["time"], data["place"], user_email)
                email_status = send_confirmation_email(data["participants"], data["time"], data["place"])
                names = [get_user_name_by_email(p) or p.split("@")[0] for p in data["participants"]]
                st.success("✅ Meeting Scheduled!")
                st.markdown(f"""
**📅 Date & Time:** {data["time"]} IST  
**📍 Venue:** {data["place"]}  
**👥 Participants:** {', '.join(names)}
""")
                st.success("📧 Email confirmation sent." if email_status else "❌ Failed to send email.")

    with col2:
        if st.button("🗑️ Clear Chat History"):
            clear_chat_history()
            st.success("🧹 Chat history cleared.")
            st.rerun()
else:
    st.warning("Please register and select your user to start chatting and scheduling.")
