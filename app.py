import streamlit as st 
from prediction_service import prediction as pred 
import streamlit.components.v1 as components

def welcome():
    return "Welcome All"

def predict_doamin(Input_text):
    return pred.predict_domain(Input_text)

def predict_entity(Input_text):
    return pred.predict_entity(Input_text)



def main():
    #st.title("Domain Processing")

    page_bg_img = '''
    <style>
    body {
    background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
    background-size: cover;
    }
    </style>
    '''
    html_temp = """
    
    
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Domain Processing App </h2>
    </div>
    
    
    """
    HTML_WRAPPER = """<div style="overflow-x: auto;  border-radius: 0.25rem; padding: 1rem">{}"""

    st.markdown(html_temp,unsafe_allow_html=True)
    st.markdown(
    """
    <style>
    .reportview-container {
        background: url("http://getwallpapers.com/wallpaper/full/8/7/4/641945.jpg")
    }
   .sidebar .sidebar-content {
        background: url("http://getwallpapers.com/wallpaper/full/8/7/4/641945.jpg")
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    #st.subheader('Input command to device')
    Input_text=st.text_input("Input Command","Type Here")

    if 'result' not in st.session_state:
        st.session_state.result=""
    if 'entity' not in st.session_state:
        st.session_state.entity=""
    try:
        if st.button("Predict"):
            st.session_state.result=predict_doamin(Input_text)
            st.session_state.entity=predict_entity(Input_text)
        st.success('The domain is:  {}'.format(st.session_state.result))
        #st.markdown(entity,unsafe_allow_html=True)
        #components.html(str(entity))    
        st.session_state.entity = st.session_state.entity.replace("\n\n","\n")
        st.write(HTML_WRAPPER.format(st.session_state.entity),unsafe_allow_html=True)
    except ValueError:
        st.success('The domain is not found.')
        st.write(HTML_WRAPPER.format(st.session_state.entity),unsafe_allow_html=True)

################ For Device Response ###############################
    html_response = """
    
    
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Named Entity Recognition Extraction</h2>
    </div>
    
    
    """
    st.markdown('##')
    st.write('\n\n\n')
    st.markdown(html_response,unsafe_allow_html=True)
    response_text=st.text_input("Response Command","Type Here")
    if 'result_res' not in st.session_state:
        st.session_state.result_res=""
    if 'entity_res' not in st.session_state:
        st.session_state.entity_res=""
    try:
        if st.button("Predict NER"):
            st.session_state.result_res=predict_doamin(response_text)
            st.session_state.entity_res=predict_entity(response_text)
        #st.success('The domain is:  {}'.format(st.session_state.result_res))
        #st.markdown(entity,unsafe_allow_html=True)
        #components.html(str(entity))    
        #st.session_state.entity_res = st.session_state.entity_res.replace("\n\n","\n")
            st.markdown(HTML_WRAPPER.format(st.session_state.entity_res),unsafe_allow_html=True)
    except ValueError:
        st.success('The domain is not found.')

    # if st.button("About"):
    #     st.text("Lets LEarn")
    #     st.text("Built with Streamlit")

if __name__=='__main__':
    main()