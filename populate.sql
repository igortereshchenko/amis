INSERT INTO Users (pasword, user_name, age)
VALUES ('1111', 'Bob', '2000-01-18');

INSERT INTO Users (pasword, user_name, age)
VALUES ('Admin', 'Admin', '2003-11-18');

INSERT INTO Users (pasword, user_name, age)
VALUES ('test', 'test', '2000-05-19');

INSERT INTO Complex (complex_name, complex_level)
VALUES ('start', 'no');

INSERT INTO Complex (complex_name, complex_level)
VALUES ('hard sestem', 'litl');

INSERT INTO Complex (complex_name, complex_level)
VALUES ('for you', 'hard');

INSERT INTO Exercise (exercise_name, information)
VALUES ('push ups', 'http://sportizdorovie.ru/wp-content/uploads/2018/01/%D0%9E%D1%82%D0%B6%D0%B8%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F-%D1%81-%D1%80%D0%B0%D0%B7%D0%BD%D0%BE%D0%B9-%D0%BF%D0%BE%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%BE%D0%B9-%D1%80%D1%83%D0%BA.jpg');

INSERT INTO Exercise (exercise_name, information)
VALUES ('squats', 'https://media.self.com/photos/57da2eaa46d0cb351c8c7ebc/master/w_1600%2Cc_limit/correct-squat_feat.jpg');

INSERT INTO Exercise (exercise_name, information)
VALUES ('Superman', 'https://image.shutterstock.com/image-photo/superman-260nw-311954117.jpg');

INSERT INTO Complex_has_exercise (complex_name, exercise_name, repeater)
VALUES ('for you', 'Superman', 20);

INSERT INTO Complex_has_exercise (complex_name, exercise_name, repeater)
VALUES ('for you', 'squats', 15);

INSERT INTO Complex_has_exercise (complex_name, exercise_name, repeater)
VALUES ('hard sestem', 'push ups', 100);

INSERT INTO Activate ( user_name, complex_name, time_start, status, weight, hight)
VALUES ('test', 'for you', '2019-10-25 23:59:59', 'rejected', 80, 176);

INSERT INTO Activate( user_name, complex_name, time_start, status, weight, hight)
VALUES ('test', 'for you', '2019-10-24 23:59:59', 'rejected', 81, 176);

INSERT INTO Activate ( user_name, complex_name, time_start, status, weight, hight)
VALUES ('test', 'for you', '2019-10-25 13:00:00', 'done', 81, 176);

INSERT INTO Messenger (messenger_name)
VALUES ('telegram');

INSERT INTO Messenger (messenger_name)
VALUES ('ukr.net');

INSERT INTO Messenger (messenger_name)
VALUES ('viber');

INSERT INTO User_has_messenger (messenger_name, user_name, address)
VALUES ('ukr.net', 'test', 'bobsuper@ukr.net');

INSERT INTO User_has_messenger (messenger_name, user_name, address)
VALUES ('telegram', 'bob', '@misterbobi');

INSERT INTO User_has_messenger (messenger_name, user_name, address)
VALUES ('telegram', 'bob', '@bobbbentop');
