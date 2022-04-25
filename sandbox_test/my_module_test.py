#from prediction service, call the functions
import prediction_service.prediction as pred



def test_square(input_value):

    #when
    domain = pred.predict_domain(input_value)

    #Then 
    assert domain =="Weather"




