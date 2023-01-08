
import logging
import pandas as pd
import json
import pickle


LOGGER = logging.getLogger(__name__)


def execute(data: dict):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.info('event parameter: {}'.format(data))
    # print("Received event: " + json.dumps(event, indent=2))
    body = data
    print("Received body:  " + str(body))
    try:
        return score(body)
    except Exception as e:
        logger.error(e)
        print(json.dumps({'error': str(e)}))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def score(data):
    LOGGER.info("Hello World")
    feat_dict = data
    feat_dict["credit_score"] = feat_dict["credit_score"] / 1000
    feat_dict["age"] = feat_dict["age"] / 85
    mod = pd.DataFrame([feat_dict])
    model = pickle.load(open("tenant_score_ml_model", 'rb'))
    ans = model.predict(mod)
    print("tenant scoring: ")
    if ans > 1:
        fans = 100
    elif ans < 0:
        fans = 20
    elif 0.85 > ans:
        fans = ans * 100 + 7
    else:
        fans = ans * 100
    if fans < 25:
        level = 1
    elif fans < 45:
        level = 2
    elif fans < 60:
        level = 3
    elif fans < 80:
        level = 4
    else:
        level = 5
    return {
        'statusCode': 200,
        'body': json.dumps({'applicant_id': feat_dict["applicant_id"], 'level': level, 'score': fans})}


