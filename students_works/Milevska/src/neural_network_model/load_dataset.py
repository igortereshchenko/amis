import json


def parse_data_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        result = []
        for question in data:
            result.append({
                'discipline': question.get('main_category'),
                'question': question.get('question'),
                'answers': question.get('answers')
            })
    return result


def training_data():
    return parse_data_from_file('neural_network_model/data/dataset.json')


def test_data():
    return parse_data_from_file('neural_network_model/data/test_data.json')
