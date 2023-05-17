import streamlit as st
import requests

# Function to send file
def send_file(file):
    url = "http://127.0.0.1:5000/upload"
    files = {'file': open(file, 'rb')}
    response = requests.post(url, files=files)
    return response

# Main app
def main():
    st.title("Audio Upload App")

    uploaded_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3'])

    if uploaded_file is not None:
        file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
        st.write(file_details)

        # Saving file and sending it to the server
        with open(uploaded_file.name, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        res = send_file(uploaded_file.name)
        st.write("Response: ", res)

if __name__ == "__main__":
    main()
