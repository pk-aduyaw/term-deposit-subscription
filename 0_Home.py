import streamlit as st


st.set_page_config(
    page_title="Term Deposit Predictor",
    layout='wide'
)


    # --------- Add custom CSS to adjust the width of the sidebar
st.markdown( """ <style> 
        section[data-testid="stSidebar"]
        { width: 200px !important;
        }
        </style> """,
        unsafe_allow_html=True,
)


def main():

    st.header('Term Deposit Subscriber Prediction App.')

    cols = st.columns(2)
    # Term Deposit Prediction Status
    with cols[0]:
        st.subheader('Term Deposit Subscriber Prediction Status')
        st.write("This application provides a platform for predicting the term deposit subscriber status of clients by leveraging historical data.")

    # Application Features
    with cols[0]:
        st.subheader('Application Features')
        st.markdown("""
        * Predict - Allows user to predict subscription status using one available model.
        * History - Displays all previous predictions made using the app.
        """)

    # Key Advantages
    with cols[0]:
        st.subheader('Key Advantages')
        st.markdown("""
                    Discover the advantages of using this Subscription Prediction App, such as;
                    * User-friendly interface
                    """)

    # How to run the app
    with cols[1]:
        st.subheader('How to Run the App')
        st.write("Follow the steps to run the Customer Churn Prediction App and make accurate predictions for customer churn.")
        st.code("""
                # Activate virtual environment
                venv/Scripts/activate

                # Run the application
                streamlit run 0_Home.py
                """, language="python")

    
    # Need Assistance
    with cols[1]:
        st.subheader('Need Assistance?')
        st.write("If you need any assistance or have questions, feel free to reach out. Email: princeekow4@gmail.com")
        cols = st.columns(4)
        with cols[0]:
            st.link_button(":red[GitHub]", "https://github.com/pk-aduyaw/ML-Embedding-in-GUI",)
        with cols[1]:
            st.link_button(":red[Medium]", "https://medium.com/@pkaduyaw/enhancing-customer-retention-a-machine-learning-solution-f58abb4b77c5")
        with cols[2]:
            st.link_button(":red[LinkedIn]", "https://www.linkedin.com/in/prince-kwabena-aduyaw")
        with cols[3]:
            st.link_button(":red[X]", "https://twitter.com/pk_aduyaw")





if __name__=='__main__':
    main()