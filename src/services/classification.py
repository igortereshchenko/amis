from domain.models import db, Schemas, Entities, Attributes
import math
import operator


class EntityNameClassification:
    sigma = 0.1

    @staticmethod
    def map_attributes(template, current):
        return [1 if attribute in current else 0 for attribute in template]

    def pdf(self, weights, to_classify):
        return math.e ** ((sum([weight * x for weight, x in zip(weights, to_classify)]) - 1) / self.sigma ** 2)

    @staticmethod
    def normalize(array):
        length = math.sqrt(sum([value ** 2 for value in array]))
        return [value / length for value in array] if length != 0 else [0 for _ in range(len(array))]

    def classify(self, samples, point):
        normalized_samples = [(self.normalize(sample[0]), sample[1]) for sample in samples]
        normalized_point = self.normalize(point)

        summation = {}
        for normalized_data_sample in normalized_samples:
            sample_pdf_value = self.pdf(normalized_data_sample[0], normalized_point)
            summation[normalized_data_sample[1]] = summation.get(normalized_data_sample[1], 0) + sample_pdf_value

        return summation

    def execute(self, to_classify):
        attributes = [value[0] for value in db.session.query(Attributes.Name).distinct(Attributes.Name).all()]
        entities = db.session.query(Entities.Id, Entities.Name, Attributes.Name)\
            .join(Attributes, Entities.Id == Attributes.EntityIdFk).all()

        tables = dict()
        for row in entities:
            tables[(row[0], row[1])] = tables.get((row[0], row[1]), []) + [row[2]]

        samples = list()
        for key, value in tables.items():
            samples.append((self.map_attributes(attributes, value), key[1]))

        result = self.classify(samples, self.map_attributes(attributes, to_classify))
        return tuple([{"name": name, "value": value} for name, value in
                      sorted(result.items(), key=operator.itemgetter(1), reverse=True) if value > 1e-40])
