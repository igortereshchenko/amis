
from math import exp

class Input_L:
    def activation(self, x):
        self.y = x * 1
        return self.y


class Image_L:
    def __init__(self, w):
        self.w = w

    def activation(self, x):
        sum = 0
        for i in range(len(self.w)):
            sum += exp(-(self.w[i] - x[i])**2/0.3**2)
        return sum


class Add_L:
    def activation(self, x):
        sum = 0
        for i in x:
            sum += i
        res = sum / len(x)
        return res

class Output_L:
    def activation(self, x):
        clas = "light"
        val = x[clas]
        for i in x.items():
            if i[1] > val:
                clas = i[0]
        return clas

def NN(params, input_data, level):

    if len(params) <= 1:
        return 'error'

    input_list = []
    for i in range(len(input_data)):
        input_list.append(Input_L)

    image_list = []
    for i in range(len(params)):
        image_list.append(Image_L(params[i][:-1]))

    res = Output_L()
    y_input = []
    y_image = []
    y_add = {}
    class_A = Add_L()
    class_B = Add_L()
    class_c = Add_L()

    for i in range(len(input_data)):
        y_input.append(input_list[i].activation(input_list[i], input_data[i]))

    y_image.append([])
    y_image.append([])
    for i in range(len(params)):
        if level[i] == "light":
            y_image[0].append(image_list[i].activation(y_input))
        else:
            y_image[2].append(image_list[i].activation(y_input))

    y_add.update({"light": class_A.activation(y_image[0])})
    y_add.update({type : class_B.activation(y_image[1])})

    res = res.activation(y_add)
    return res