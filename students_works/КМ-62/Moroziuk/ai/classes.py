def calculate_y_i(vector, input, sigma):
    res = 0.0
    for i in vector:
        res = res + ((i - input)**2)/(2 * sigma**2)
    return res


def classificate_vacancy_by_salary(vacancies):
    vacanciesWithSalary = []

    class1 = [3000, 2870, 3125]
    class2 = [5200, 49999, 5600]
    class3 = [7100, 6500, 8000]
    class4 = [10000, 12000, 11000]
    class5 = [22000, 25000, 24800]
    class6 = [55000, 65000, 67000]
    class7 = [130000, 125000, 120000]

    sigma = 0.3
    for i in vacancies:
        input = i.salary
        y1 = calculate_y_i(class1, input, sigma) / len(class1)
        y2 = calculate_y_i(class2, input, sigma) / len(class2)
        y3 = calculate_y_i(class3, input, sigma) / len(class3)
        y4 = calculate_y_i(class4, input, sigma) / len(class4)
        y5 = calculate_y_i(class5, input, sigma) / len(class5)
        y6 = calculate_y_i(class6, input, sigma) / len(class6)
        y7 = calculate_y_i(class7, input, sigma) / len(class7)

        y = [y1, y2, y3, y4, y5, y6, y7]

        if y1 == min(y):
            vacanciesWithSalary.append(VacancyBySalary(category = "first category", name = i.name))
        elif y2 == min(y):
            vacanciesWithSalary.append(VacancyBySalary(category="second category", name=i.name))
        elif y3 == min(y):
            vacanciesWithSalary.append(VacancyBySalary(category="thirtd category", name=i.name))
        elif y4 == min(y):
            vacanciesWithSalary.append(VacancyBySalary(category="forth category", name=i.name))
        elif y5 == min(y):
            vacanciesWithSalary.append(VacancyBySalary(category="fifth category", name=i.name))
        elif y6 == min(y):
            vacanciesWithSalary.append(VacancyBySalary(category="sixth category", name=i.name))
        elif y7 == min(y):
            vacanciesWithSalary.append(VacancyBySalary(category="seventh category", name=i.name))

    return vacanciesWithSalary


class VacancyBySalary():
    category = ""
    name = ""

    def __init__(self, category, name):
        self.category = category
        self.name = name
