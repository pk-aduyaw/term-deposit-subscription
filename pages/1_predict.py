import streamlit as st
import pandas as pd
import joblib
import os

# Configure the page
st.set_page_config(
    page_title='Predictions',
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

# ------ Set header for page
st.title('Subscriber Prediction Page')

column1, column2 = st.columns([.6, .4])
with column1:
    model_option = st.selectbox('Choose which model to use for prediction', options=['RandomForest Model'])


# Define the local file paths
model_path = './model/RandomForest_model.joblib'
local_encoder_path = './model/label_encoder.joblib'

# -------- Function to load the model from local files
@st.cache_resource(show_spinner="Loading model")
def rf_pipeline():
    # Load the RandomForest model from the local path
    with open(model_path, 'rb') as f:
        pipeline = joblib.load(f)
    return pipeline


# --------- Function to load encoder from local files
def load_encoder():
    # Load label encoder
    with open(local_encoder_path, 'rb') as b:
        label_encoder = joblib.load(b)
    return label_encoder


# --------- Create a function for model selection
def select_model():
    # ------- Option for first model
    if model_option == 'RandomForest Model':
        model = rf_pipeline()
    encoder = load_encoder()
    return model, encoder



# ---- Initialize prediction in session state
if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None
if 'prediction_proba' not in st.session_state:
    st.session_state['prediction_proba'] = None

# ------- Create a function to make prediction
def make_prediction(model, encoder):

    age = st.session_state['age']
    job = st.session_state['job']
    marital = st.session_state['marital']
    education = st.session_state['education']
    default = st.session_state['default']
    balance = st.session_state['balance']
    housing = st.session_state['housing']
    loan = st.session_state['loan']
    contact = st.session_state['contact']
    day = st.session_state['day']
    month = st.session_state['month']
    duration = st.session_state['duration']
    campaign = st.session_state['campaign']
    pdays = st.session_state['pdays']
    previous = st.session_state['previous']
    poutcome = st.session_state['poutcome']
    
        
    columns = ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing',
       'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays',
       'previous', 'poutcome']
        
    values = [[age, job, marital, education, default, balance, housing,
            loan, contact, day, month, duration,
            campaign, pdays, previous, poutcome]]
        
    data = pd.DataFrame(values, columns=columns)

    # -------- Get the value for prediction
    prediction = model.predict(data)
    prediction = encoder.inverse_transform(prediction)
    st.session_state['prediction'] = prediction

    # -------- Get the value for prediction probability
    prediction_proba = model.predict_proba(data)
    st.session_state['prediction_proba'] = prediction_proba

    data['y'] = prediction

    data.to_csv('./data/history.csv', mode='a', header=not os.path.exists('./data/history.csv'), index=False)

    return prediction, prediction_proba


# ------- Prediction page creation
def input_features():

    with st.form('features'):
        model_pipeline, encoder = select_model()
        col1, col2 = st.columns(2)

        # ------ Collect customer information
        with col1:
            st.subheader('Bank Client Data')
            st.number_input('age', min_value=18, key='age')
            st.selectbox('job', options=['management', 'technician', 'entrepreneur', 'blue-collar',
            'unknown', 'retired', 'admin.', 'services', 'self-employed',
            'unemployed', 'housemaid', 'student'], key='job')
            st.selectbox('marital', options=['married', 'divorced','single'], key='marital')
            st.selectbox('education', options=['tertiary', 'secondary', 'unknown', 'primary'], key='education')
            st.radio('default', options=['yes', 'no'],horizontal=True, key='default')
            st.number_input("balance", placeholder="amount in euros", key='balance')
            st.radio('housing', options=['yes', 'no'],horizontal=True, key='housing')
            st.radio('loan', options=['yes', 'no'],horizontal=True, key='loan')
            
        # ------ Collect Last Contact for Current Campaign
        with col2:
            st.subheader('Last Current Campaign Contact')
            st.selectbox('contact', options=['unknown', 'cellular', 'telephone'], key='contact')
            st.select_slider('day', options=(1, 31), key='day')
            st.selectbox('month', options=['may', 'jun', 'jul', 'aug', 'oct', 'nov', 'dec', 'jan', 'feb',
       'mar', 'apr', 'sep'], key='month')
            st.number_input("duration", placeholder="time in seconds", key='duration')
            
        # ------ Collect Other Relevant Details
        with col2:
            st.subheader('Other Details')
            st.number_input('campaign', min_value=1, key='campaign')
            st.number_input('pdays', min_value=-1, key='pdays')
            st.number_input('previous', min_value=0, key='previous')
            st.selectbox('poutcome', options=['unknown', 'failure', 'other', 'success'], key='poutcome')
            
        st.form_submit_button('Predict', on_click=make_prediction, kwargs=dict(model=model_pipeline, encoder=encoder))

    return True
        

if __name__=='__main__':
    input_features()
    prediction = st.session_state['prediction']
    probability = st.session_state['prediction_proba']    

    if st.session_state['prediction'] == None:
        cols = st.columns([3, 4, 3])
        with cols[1]:
            st.markdown('#### Predictions will show here ⤵️')
        cols = st.columns([.25,.5,.25])
        with cols[1]:
            st.markdown('##### No predictions made yet. Make prediction')
    else:
        if prediction == "Yes":
            cols = st.columns([.1,.8,.1])
            with cols[1]:
                st.markdown(f'### The customer will subscribe to a term deposit with a {round(probability[0][1],2)}% probability.')
            cols = st.columns([.3,.4,.3])
            with cols[1]:
                st.success('Subscription status predicted successfullly🎉')
        else:
            cols = st.columns([.1,.8,.1])
            with cols[1]:
                st.markdown(f'### The customer will not subscribe to a term deposit with a {round(probability[0][0],2)}% probability.')
            cols = st.columns([.3,.4,.3])
            with cols[1]:
                st.success('Subscription status predicted successfullly🎉')