import numpy as np
import json

from neural_network_model.classify.training import TrainingModel, think

FILE_WITH_WEIGHTS = 'neural_network_model/classify/synapses_temp.json'

# ERROR_THRESHOLD = 0.03
# load our calculated synapse values


def get_weights(filename='neural_network_model/classify/synapses_temp.json'):
    with open(filename) as data_file:
        synapse = json.load(data_file)
        synapse_0 = np.asarray(synapse['synapse0'])
        synapse_1 = np.asarray(synapse['synapse1'])
        words = np.asarray(synapse['words'])
        classes = np.asarray(synapse['classes'])
    return synapse_0, synapse_1, synapse, words, classes


def classify(sentence, show_details, error_threshold):
    synapse_0, synapse_1, _, words, classes = get_weights(filename=FILE_WITH_WEIGHTS)
    results = think(sentence, synapse_0, synapse_1, words, show_details)
    results = [[i, r] for i, r in enumerate(results) if r > error_threshold]
    results.sort(key=lambda x: x[1], reverse=True)
    return_results = [[classes[r[0]], r[1]] for r in results]
    return return_results


def correlation_coef(class_1, class_2):
    synapse_0, _, synapse, words, classes = get_weights(filename=FILE_WITH_WEIGHTS)
    first_index = synapse['classes'].index(class_1)
    second_index = synapse['classes'].index(class_2)
    array_1 = [item[first_index] for item in synapse_0]
    array_2 = [item[second_index] for item in synapse_0]
    corrcoef = np.corrcoef(array_1, array_2)
    return corrcoef[0][1]


def get_best_discipline(question):
    result = classify(question, show_details=False, error_threshold=0)
    if len(result) > 0:
        return result[0][0]