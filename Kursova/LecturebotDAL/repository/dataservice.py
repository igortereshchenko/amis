from sqlalchemy import func

from LecturebotDAL.dbcontext import DBEngine, ModelBase, Session
from sqlalchemy.orm.attributes import InstrumentedAttribute

ModelBase.metadata.create_all(DBEngine)

session = Session()


def get_data(class_name):
    return session.query(class_name).all()


def get_data_by_id(class_name, gradebook_number):
    return session.query(class_name).filter_by(gradebook_number = int(gradebook_number)).first()
	
	
def get_data_by(class_name, gradebook_number):
    return session.query(class_name).filter_by(gradebook_number = int(gradebook_number))


def insert_data(data):
    session.add(data)


def delete_data(class_name,id):
    user = session.query(class_name).filter_by(gradebook_number = id).first()
    session.delete(user)


def update_data(obj, class_name):
    mapped_values = {}
    for item in class_name.__dict__.items():
        field_name = item[0]
        field_type = item[1]
        is_column = isinstance(field_type, InstrumentedAttribute)
        if is_column:
            mapped_values[field_name] = getattr(obj, field_name)

    session.query(class_name).filter_by(gradebook_number = obj.gradebook_number).update(mapped_values)


def req1(cl1, cl2, cl3):
    res = session.query(cl1.first_name, func.count(cl3.name))\
        .select_from(cl1)\
        .join(cl2)\
        .join(cl3)\
        .group_by(cl1.first_name).all()
    return res


def req2(cl1, cl2, cl3):
    res = session.query(cl2.id, cl1.first_name, cl1.second_name, cl3.name) \
        .select_from(cl1) \
        .join(cl2) \
        .join(cl3) \
        .all()
    return res


def req3(cl1, cl2, cl3):
    res = session.query(cl3.name, func.count(cl3.name)) \
        .select_from(cl1) \
        .join(cl2) \
        .join(cl3) \
        .group_by(cl3.name).all()
    return res


def save():
    session.commit()


def get_data_by_init(class_name, id):
    return session.query(class_name).filter_by(initalization_num = int(id)).first()



def delete_data_init(class_name,initalization_num):
    user = session.query(class_name).filter_by(initalization_num = initalization_num).first()
    session.delete(user)
	
def get_data_by_pass(class_name, pass_number):
    return session.query(class_name).filter_by(pass_number = int(pass_number)).first()



def delete_data_pass(class_name,pass_number):
    user = session.query(class_name).filter_by(pass_number = pass_number).first()
    session.delete(user)
	
	
def get_data_by_passn(class_name, pass_num):
    return session.query(class_name).filter_by(pass_num = int(pass_num)).first()



def delete_data_passn(class_name,pass_num):
    user = session.query(class_name).filter_by(pass_num = pass_num).first()
    session.delete(user)
	
	
def update_data_cw(obj, class_name):
    mapped_values = {}
    for item in class_name.__dict__.items():
        field_name = item[0]
        field_type = item[1]
        is_column = isinstance(field_type, InstrumentedAttribute)
        if is_column:
            mapped_values[field_name] = getattr(obj, field_name)

    session.query(class_name).filter_by(initalization_num = obj.initalization_num).update(mapped_values)
	
	
def update_data_t(obj, class_name):
    mapped_values = {}
    for item in class_name.__dict__.items():
        field_name = item[0]
        field_type = item[1]
        is_column = isinstance(field_type, InstrumentedAttribute)
        if is_column:
            mapped_values[field_name] = getattr(obj, field_name)

    session.query(class_name).filter_by(pass_number = obj.pass_number).update(mapped_values)
	
	
def update_data_s(obj, class_name):
    mapped_values = {}
    for item in class_name.__dict__.items():
        field_name = item[0]
        field_type = item[1]
        is_column = isinstance(field_type, InstrumentedAttribute)
        if is_column:
            mapped_values[field_name] = getattr(obj, field_name)

    session.query(class_name).filter_by(pass_num = obj.pass_num).update(mapped_values)
	
def get_data_by_build_num(class_name, build_num):
    return session.query(class_name).filter_by(build_num = int(build_num)).first()



def delete_data_build_num(class_name,build_num):
    user = session.query(class_name).filter_by(build_num = build_num).first()
    session.delete(user)
	
	
def update_data_b(obj, class_name):
    mapped_values = {}
    for item in class_name.__dict__.items():
        field_name = item[0]
        field_type = item[1]
        is_column = isinstance(field_type, InstrumentedAttribute)
        if is_column:
            mapped_values[field_name] = getattr(obj, field_name)

    session.query(class_name).filter_by(build_num = obj.build_num).update(mapped_values)
	
	
def classificate(a,b,c):

    x_A = [[1, 1, 1],
           [2, 2, 2],
           [3, 3, 3]]
    x_B = [[4, 5, 5]]
    classes = ['A', 'B']

    sigma = 0.3
    input_data = [a, b, c]

    y3 = 0
    y4 = 0
    y3t = 0
    y4t = 0


    y1t = math.exp(-(((x_A[0][0] - input_data[0])**2 + (x_A[0][1] - input_data[1])**2 + (x_A[0][2] - input_data[2])**2)/(2 * (sigma**2)))) + math.exp(-(((x_A[1][0] - input_data[0])**2 + (x_A[1][1] - input_data[1])**2 + (x_A[1][2] - input_data[2])**2)/(2 * (sigma**2)))) + math.exp(-(((x_A[2][0] - input_data[0])**2 + (x_A[2][1] - input_data[1])**2 + (x_A[2][2] - input_data[2])**2)/(2 * (sigma**2))))
    y1 = y1t / len(x_A)
    y2t = math.exp(-(((x_B[0][0] - input_data[0])**2 + (x_B[0][1] - input_data[1])**2 + (x_B[0][2] - input_data[2])**2)/(2 * (sigma**2))))
    y2 = y2t / len(x_B)
    return(y1,y2)

def get_data_class(class_name, gradebook_number):
    return session.query(class_name).filter_by(gradebook_number = int(gradebook_number)).slice( 2 )
