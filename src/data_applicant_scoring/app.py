
import logging
import pandas as pd
import json
import pickle
import sklearn


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
    pid = feat_dict["applicant_id"]
    feat_dict.pop("applicant_id", None)
    feat_dict["credit_score"] = feat_dict["credit_score"] / 1000
    feat_dict["age"] = feat_dict["age"] / 85
    mod = pd.DataFrame([feat_dict])
    model = pickle.load(open("src/data_applicant_scoring/tenant_score_ml_model", 'rb'))
    ans = model.predict(mod)[0]
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
        'body': json.dumps(dict({'applicant_id': str(pid), 'level': level, 'score': fans}))}


# score({"applicant_id": "BC5T2A09-ELE2-4HG0-AE74-4E2DF78A3E1D",
#         "credit_score": 678,
#         "eviction": 2,
#         "criminal": 1,
#         "age": 28})