insert into users (username, password) values ('artemkovtun',  '5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5');
insert into users (username, password) values ('supermario',  '5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5');
insert into users (username, password) values ('jamesmartins',  '5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5');


insert into files (id, createdbyfk, name, createdon) values ('E001222E-8AD9-49F2-BB1A-C0B6A54A6A77','artemkovtun', 'data.xlsx', current_timestamp);
insert into files (id, createdbyfk, name, createdon) values ('9353E549-21D6-40CC-A61E-CEADA0187C69','supermario', 'awesome table.xlsx', current_timestamp);
insert into files (id, createdbyfk, name, createdon) values ('382EF0BB-22E9-4BF8-836B-2C24D4E2CD1D','jamesmartins', 'customers.xlsx', current_timestamp);


insert into filepages (id, fileidfk, name, createdon) values ('35C70D70-7CA4-4AEA-8961-380BE3FE58FF',
                                                              'E001222E-8AD9-49F2-BB1A-C0B6A54A6A77',
                                                              'main',
                                                              current_timestamp);

insert into filepages (id, fileidfk, name, createdon) values ('B253EC5E-D6A9-4324-A4D7-F7A8F5614DC8',
                                                              '9353E549-21D6-40CC-A61E-CEADA0187C69',
                                                              'users',
                                                              current_timestamp);

insert into filepages (id, fileidfk, name, createdon) values ('1D332B1E-0F18-42E7-8456-510F8692A0F1',
                                                              '9353E549-21D6-40CC-A61E-CEADA0187C69',
                                                              'companies',
                                                              current_timestamp);

insert into filepages (id, fileidfk, name, createdon) values ('47EA4E57-BF51-4171-895F-5DD68C6DB29C',
                                                              '382EF0BB-22E9-4BF8-836B-2C24D4E2CD1D',
                                                              'main',
                                                              current_timestamp);

insert into filecolumns (id, filepageidfk, name, type, createdon) values ('C78A6200-6EDF-4686-8249-94C9DAAFFE27',
                                                                          '35C70D70-7CA4-4AEA-8961-380BE3FE58FF',
                                                                          'id',
                                                                          'integer',
                                                                          current_timestamp);

insert into filecolumns (id, filepageidfk, name, type, createdon) values ('FB792506-EAAE-4476-882A-CBB234296F8B',
                                                                          '35C70D70-7CA4-4AEA-8961-380BE3FE58FF',
                                                                          'birthdate',
                                                                          'datetime',
                                                                          current_timestamp);

insert into filecolumns (id, filepageidfk, name, type, createdon) values ('1CC8E0C6-FF5A-44AE-94E4-5FEE5D13E9D8',
                                                                          'B253EC5E-D6A9-4324-A4D7-F7A8F5614DC8',
                                                                          'firstname',
                                                                          'nvarchar2',
                                                                          current_timestamp);

insert into filecolumns (id, filepageidfk, name, type, createdon) values ('965C4040-D94C-4844-B6A6-662EE0B5FBC1',
                                                                          'B253EC5E-D6A9-4324-A4D7-F7A8F5614DC8',
                                                                          'lastname',
                                                                          'nvarchar2',
                                                                          current_timestamp);

insert into filecolumns (id, filepageidfk, name, type, createdon) values ('110C6933-9DB1-462A-B178-E4D5070A687C',
                                                                          'B253EC5E-D6A9-4324-A4D7-F7A8F5614DC8',
                                                                          'middlename',
                                                                          'nvarchar',
                                                                          current_timestamp);

insert into filecolumns (id, filepageidfk, name, type, createdon) values ('9139A33C-1AEE-4DF2-BC41-4777F13C912E',
                                                                          '1D332B1E-0F18-42E7-8456-510F8692A0F1',
                                                                          'name',
                                                                          'nvarchar2',
                                                                          current_timestamp);

insert into filecolumns (id, filepageidfk, name, type, createdon) values ('61CECDB0-7B70-4D70-BBE1-76E06C98EAAA',
                                                                          '1D332B1E-0F18-42E7-8456-510F8692A0F1',
                                                                          'id',
                                                                          'guid',
                                                                          current_timestamp);

insert into filecolumns (id, filepageidfk, name, type, createdon) values ('11774B81-A9B5-449B-95B6-383E2DC5147F',
                                                                          '47EA4E57-BF51-4171-895F-5DD68C6DB29C',
                                                                          'id',
                                                                          'guid',
                                                                          current_timestamp);

insert into filecolumns (id, filepageidfk, name, type, createdon) values ('DF17710D-DBEE-41D6-B209-AA9A688B42CB',
                                                                          '47EA4E57-BF51-4171-895F-5DD68C6DB29C',
                                                                          'fullname',
                                                                          'nvarchar2',
                                                                          current_timestamp);

insert into filecolumns (id, filepageidfk, name, type, createdon) values ('8B94DF37-53F8-4B38-9653-ACD70C355399',
                                                                          '47EA4E57-BF51-4171-895F-5DD68C6DB29C',
                                                                          'email',
                                                                          'text',
                                                                          current_timestamp);

insert into schemas (id, createdbyfk, name, createdon) values ('06E696FF-245D-4A3F-B97A-234C367FAF82',
                                                               'artemkovtun',
                                                               'university',
                                                               current_timestamp);

insert into schemas (id, createdbyfk, name, createdon) values ('F9B1DB6A-3B20-4E6E-AEDE-3D882F771E54',
                                                               'supermario',
                                                               'library',
                                                               current_timestamp);

insert into schemas (id, createdbyfk, name, createdon) values ('20BE2054-01DD-4835-B46D-B1186401B653',
                                                               'jamesmartins',
                                                               'messenger',
                                                               current_timestamp);

insert into entities (id, schemaidfk, name, createdon) values ('5799BB8D-1187-4B66-B2B3-981D886C6C03',
                                                               '06E696FF-245D-4A3F-B97A-234C367FAF82',
                                                               'users',
                                                               current_timestamp);

insert into entities (id, schemaidfk, name, createdon) values ('C334A046-DF09-4697-837C-AF7DC7EC5DCE',
                                                               '06E696FF-245D-4A3F-B97A-234C367FAF82',
                                                               'groups',
                                                               current_timestamp);

insert into entities (id, schemaidfk, name, createdon) values ('4ACD209D-9775-4651-9B74-D782FAD3191D',
                                                               'F9B1DB6A-3B20-4E6E-AEDE-3D882F771E54',
                                                               'books',
                                                               current_timestamp);

insert into entities (id, schemaidfk, name, createdon) values ('E7A202E9-6ADD-451C-BD98-62457306B22F',
                                                               'F9B1DB6A-3B20-4E6E-AEDE-3D882F771E54',
                                                               'authors',
                                                               current_timestamp);

insert into entities (id, schemaidfk, name, createdon) values ('C748E669-8E62-4ADF-B3A9-19E39B762E1F',
                                                               'F9B1DB6A-3B20-4E6E-AEDE-3D882F771E54',
                                                               'bookauthor',
                                                               current_timestamp);

insert into entities (id, schemaidfk, name, createdon) values ('8D610123-D275-47FA-827D-45504BC27072',
                                                               '20BE2054-01DD-4835-B46D-B1186401B653',
                                                               'messages',
                                                               current_timestamp);


insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('8626A6C9-AACC-439B-82E1-FE11CBC521BD',
                                                                                         '5799BB8D-1187-4B66-B2B3-981D886C6C03',
                                                                                         'username',
                                                                                         'nvarchar2(100)',
                                                                                         False,
                                                                                         True,
                                                                                         current_timestamp);
insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('BC812DDB-D21B-4F3A-9A36-E4B02815EAEA',
                                                                                         '5799BB8D-1187-4B66-B2B3-981D886C6C03',
                                                                                         'email',
                                                                                         'nvarchar2(100)',
                                                                                         False,
                                                                                         False,
                                                                                         current_timestamp);
insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('3D970268-34CD-475C-8DC3-06A9176D6B3E',
                                                                                         '5799BB8D-1187-4B66-B2B3-981D886C6C03',
                                                                                         'password',
                                                                                         'nvarchar2(100)',
                                                                                         True,
                                                                                         False,
                                                                                         current_timestamp);
insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('4CC05865-EB56-4BCE-BF52-531F69562003',
                                                                                         'C334A046-DF09-4697-837C-AF7DC7EC5DCE',
                                                                                         'id',
                                                                                          'uuid',
                                                                                         False,
                                                                                         True,
                                                                                         current_timestamp);
insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('AA3AC7EC-74DA-4FEB-9E93-B79060E0348A',
                                                                                         'C334A046-DF09-4697-837C-AF7DC7EC5DCE',
                                                                                         'title',
                                                                                          'nvarchar2(100)',
                                                                                         False,
                                                                                         False,
                                                                                         current_timestamp);

insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('4BB5AE1B-D0DB-4429-9F7A-2D5E21391EA6',
                                                                                         '4ACD209D-9775-4651-9B74-D782FAD3191D',
                                                                                         'id',
                                                                                          'uuid',
                                                                                         False,
                                                                                         True,
                                                                                         current_timestamp);

insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('06CA2A89-028F-4E8F-9351-28E5BFD637A7',
                                                                                         '4ACD209D-9775-4651-9B74-D782FAD3191D',
                                                                                         'title',
                                                                                          'nvarchar2(100)',
                                                                                         False,
                                                                                         False,
                                                                                         current_timestamp);


insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('32C0BC55-EF41-4410-8171-BB2857E285FE',
                                                                                         'E7A202E9-6ADD-451C-BD98-62457306B22F',
                                                                                         'id',
                                                                                         'uuid',
                                                                                         False,
                                                                                         True,
                                                                                         current_timestamp);

insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('83DDE839-8DC0-4CC0-B591-DDD13E75552D',
                                                                                         'E7A202E9-6ADD-451C-BD98-62457306B22F',
                                                                                         'firstname',
                                                                                         'nvarchar2(100)',
                                                                                         True,
                                                                                         False,
                                                                                         current_timestamp);

insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('30B9D90F-93FF-4190-B716-E652994636BF',
                                                                                         'E7A202E9-6ADD-451C-BD98-62457306B22F',
                                                                                         'lastname',
                                                                                         'nvarchar2(100)',
                                                                                         False,
                                                                                         False,
                                                                                         current_timestamp);

insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('D2F5B2B8-11B2-471D-B217-D268ACFB6E8F',
                                                                                         'C748E669-8E62-4ADF-B3A9-19E39B762E1F',
                                                                                         'bookId',
                                                                                         'uuid',
                                                                                         False,
                                                                                         True,
                                                                                         current_timestamp);

insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('719EE495-607B-4A52-8F53-72650C22BB7F',
                                                                                         'C748E669-8E62-4ADF-B3A9-19E39B762E1F',
                                                                                         'authorId',
                                                                                         'uuid',
                                                                                         False,
                                                                                         True,
                                                                                         current_timestamp);

insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('27B96329-5D60-4B8E-B178-6FFD8929472A',
                                                                                         '8D610123-D275-47FA-827D-45504BC27072',
                                                                                         'id',
                                                                                         'uuid',
                                                                                         False,
                                                                                         True,
                                                                                         current_timestamp);

insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('A30543C3-3AD4-4DA7-B59B-D64B299DB108',
                                                                                         '8D610123-D275-47FA-827D-45504BC27072',
                                                                                         'text',
                                                                                         'nvarchar2(100)',
                                                                                         False,
                                                                                         False,
                                                                                         current_timestamp);

insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('FD60B3D1-0697-44CE-972B-DF9FF9101A3E',
                                                                                         '8D610123-D275-47FA-827D-45504BC27072',
                                                                                         'sender',
                                                                                         'uuid',
                                                                                         False,
                                                                                         False,
                                                                                         current_timestamp);

insert into attributes (id, entityidfk, name, type, "isNull", isprimarykey, createdon) values ('35ADED2C-04B6-4E1E-B566-5186BD81780B',
                                                                                         '8D610123-D275-47FA-827D-45504BC27072',
                                                                                         'receiver',
                                                                                         'uuid',
                                                                                         False,
                                                                                         False,
                                                                                         current_timestamp);


