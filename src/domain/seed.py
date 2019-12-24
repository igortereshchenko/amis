from .models import db, Schemas, Entities, Attributes, Users


def seed():
    db.session.query(Attributes).delete()
    db.session.query(Entities).delete()
    db.session.query(Schemas).delete()
    db.session.query(Users).delete()

    db.session.add(
        Users(Username="artemkovtun",
              Password="5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5",
              Schemas=[
                  Schemas(
                      Name="Shop",
                      Entities=[
                          Entities(
                              Name="Product",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("product_id", "int", False, True),
                                  Attributes("product_type_id", "int", False, False),
                                  Attributes("oem_id", "int", False, False),
                                  Attributes("product_name", "varchar(100)", True, False),
                                  Attributes("product_model", "varchar(50)", True, False),
                                  Attributes("product_specs", "varchar(100)", True, False)
                              ]
                          ),
                          Entities(
                              Name="Manufacturer",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("oem_id", "int", False, True),
                                  Attributes("oem_name", "varchar(50)", True, False)
                              ]
                          ),
                          Entities(
                              Name="ProductType",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("product_type_id", "int", False, True),
                                  Attributes("product_type_name", "varchar(50)", True, False)
                              ]
                          ),
                          Entities(
                              Name="Part",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("part_id", "int", False, True),
                                  Attributes("product_type_id", "int", False, False),
                                  Attributes("oem_id", "int", False, False),
                                  Attributes("part_name", "varchar(75)", True, False)
                              ]
                          ),
                          Entities(
                              Name="JobPart",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("job_id", "int", False, True),
                                  Attributes("part_id", "int", False, True),
                                  Attributes("job_part_quantity", "int", True, False),
                                  Attributes("job_part_price", "decimal", True, False)
                              ]
                          ),
                          Entities(
                              Name="Job",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("job_id", "int", False, True),
                                  Attributes("client_id", "int", False, False),
                                  Attributes("device_id", "int", False, False),
                                  Attributes("job_start_date", "date", True, False),
                                  Attributes("job_end_date", "date", True, False),
                                  Attributes("job_labour_hours", "int", True, False),
                                  Attributes("job_labour_charge", "decimal", True, False),
                                  Attributes("job_parts_charge", "decimal", True, False),
                                  Attributes("job_total_charge", "decimal", True, False),
                                  Attributes("job_paid", "tinyint", True, False)
                              ]
                          ),
                          Entities(
                              Name="Device",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("device_id", "int", False, True),
                                  Attributes("product_id", "int", False, False),
                                  Attributes("device_serial", "varchar(50)", True, False),
                                  Attributes("device_notes", "varchar(500)", True, False)
                              ]
                          ),
                          Entities(
                              Name="Client",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("client_id", "int", False, True),
                                  Attributes("client_firstname", "nvarchar(75)", True, False),
                                  Attributes("client_lastname", "nvarchar(75)", True, False),
                                  Attributes("client_sex", "nvarchar(20)", True, False),
                                  Attributes("client_address", "nvarchar(250)", True, False),
                                  Attributes("client_landline", "nvarchar(25)", True, False),
                                  Attributes("client_mobile", "nvarchar(25)", True, False),
                                  Attributes("client_email", "nvarchar(100)", True, False),
                                  Attributes("client_website", "nvarchar(150)", True, False)
                              ]
                          ),
                          Entities(
                              Name="JobNotes",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("job_notes_id", "int", False, True),
                                  Attributes("job_notes_text", "varchar(500)", True, False)
                              ]
                          ),
                          Entities(
                              Name="JobService",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("job_id", "int", False, True),
                                  Attributes("service_id", "int", False, True)
                              ]
                          ),
                          Entities(
                              Name="Service",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("service_id", "int", False, True),
                                  Attributes("service_name", "varchar(75)", True, False)
                              ]
                          )
                      ]
                  ),
                  Schemas(
                      Name="MovieTheater",
                      Entities=[
                          Entities(
                              Name="Movie",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("id", "int", False, True),
                                  Attributes("imdb_id", "varchar(45)", True, False),
                                  Attributes("title", "varchar(45)", True, False),
                                  Attributes("summary", "blob", True, False),
                                  Attributes("release_date", "date", True, False),
                                  Attributes("runtime", "varchar(45)", True, False),
                                  Attributes("poster", "varchar(45)", True, False),
                                  Attributes("rating", "varchar(45)", True, False)
                              ]
                          ),
                          Entities(
                              Name="MovieGenre",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("movie_id", "int", False, True),
                                  Attributes("genre_id", 'int', False, True),
                                  Attributes("series_id", "int", False, True)
                              ]
                          ),
                          Entities(
                              Name="Genre",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("genre_id", "int", False, True),
                                  Attributes("genre_name", "varchar(45)", True, False)
                              ]
                          ),
                          Entities(
                              Name="MoviePerson",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("movie_id", "int", False, True),
                                  Attributes("person_id", "int", False, True),
                                  Attributes("character_name", "varchar(45)", True, False),
                                  Attributes("season_id", "int", False, True),
                                  Attributes("episode_id", "int", False, True)
                              ]
                          ),
                          Entities(
                              Name="Person",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("person_id", "int", False, True),
                                  Attributes("person_name", "varchar(45)", True, False)
                              ]
                          ),
                          Entities(
                              Name="PersonRole",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("person_id", "int", False, True),
                                  Attributes("role_id", "int", False, True)
                              ]
                          ),
                          Entities(
                              Name="Role",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("role_id", "int", False, True),
                                  Attributes("role_type", "varchar(10)", False, False)
                              ]
                          ),
                          Entities(
                              Name="TVSeries",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("series_id", "int", False, True),
                                  Attributes("imdb_id", "varchar(45)", True, False),
                                  Attributes("title", "varchar(45)", True, False),
                                  Attributes("genre", "varchar(45)", True, False),
                                  Attributes("start_year", "varchar(45)", True, False),
                                  Attributes("ent_year", "varchar(45)", True, False),
                              ]
                          ),
                          Entities(
                              Name="SeriesSeason",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("season_id", "int", False, True),
                                  Attributes("imdb_id", "varchar(45)", False, True),
                                  Attributes("summary", "varchar(45)", False, True),
                                  Attributes("season_number", "varchar(45)", False, True),
                                  Attributes("series_id", "int", False, False)
                              ]
                          ),
                          Entities(
                              Name="SeasonEpisode",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("episode_id", "int", False, True),
                                  Attributes("imdb_id", "varchar(45)", True, False),
                                  Attributes("title", "varchar(45)", True, False),
                                  Attributes("summary", "varchar(45)", True, False),
                                  Attributes("airdate", "varchar(45)", True, False),
                                  Attributes("season_id", "int", False, False)
                              ]
                          )
                      ]
                  ),
                  Schemas(
                      Name="Company",
                      Entities=[
                          Entities(
                              Name="Department",
                              IsOverrideExisted=False,
                              Attributes=[
                                  Attributes("id", "uuid", False, True),
                                  Attributes("name", "nvarchar(100)", False, False)
                              ]
                          ),
                          Entities(
                              Name="Employee",
                              IsOverrideExisted=False,
                              Attributes=[
                                  Attributes("id", "uuid", False, True),
                                  Attributes("department_id", "uuid", False, False),
                                  Attributes("fullname", "nvarchar2(100)", False, False)
                              ]
                          ),
                          Entities(
                              Name="Client",
                              IsOverrideExisted=False,
                              Attributes=[
                                  Attributes("name", "nvarchar(100)", False, True),
                                  Attributes("address", "nvarchar(100)", False, True)
                              ]
                          ),
                          Entities(
                              Name="Contract",
                              IsOverrideExisted=False,
                              Attributes=[
                                  Attributes("number", "nvarchar(128)", False, True),
                                  Attributes("client_name", "nvarchar(100)", False, False),
                                  Attributes("date", "timestamp", True, False),
                                  Attributes("value", "decimal", False, False)
                              ]
                          ),
                          Entities(
                              Name="Performers",
                              IsOverrideExisted=False,
                              Attributes=[
                                  Attributes("employee_id", "uuid", False, True),
                                  Attributes("contract_number", "nvarchar(128)", False, True)
                              ]
                          )
                      ]
                  ),
                  Schemas(
                      Name="Person",
                      Entities=[
                          Entities(
                              Name="Person",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("id", "uuid", False, True),
                                  Attributes("firstname", "nvarchar2(100)", False, False),
                                  Attributes("lastname", "nvarchar2(100)", False, False),
                                  Attributes("middlename", "nvarchar2(100)", False, False),
                                  Attributes("sex", "nvarchar(10)", True, False),
                                  Attributes("birthdate", "date", True, False),
                                  Attributes("dear", "nvarchar(300)", True, False),
                                  Attributes("ssn", "nvarchar2(200)", False, False),
                                  Attributes("isResident", "boolean", True, False),
                                  Attributes("education", "nvarchar2(100)", True, False)
                              ]
                          )
                      ]
                  ),
                  Schemas(
                      Name="Market",
                      Entities=[
                          Entities(
                              Name="Custromers",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("id", "uuid", False, True),
                                  Attributes("name", "nvarchar2(100)", False, False),
                                  Attributes("contract_sign_date", "datetime", False, False),
                                  Attributes("category_id", "uuid", False, False),
                                  Attributes("valid_from", "timestamp", True, False),
                                  Attributes("valid_to", "timestamp", True, False),
                                  Attributes("current_record", "nvarchar(300)", True, False)
                              ]
                          ),
                          Entities(
                              Name="Store",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("id", "uuid", False, True),
                                  Attributes("name", "nvarchar2(100)", False, False),
                                  Attributes("address1", "nvarchar2(100)", False, False),
                                  Attributes("address2", "nvarchar2(100)", True, False),
                                  Attributes("region", "nvarchar2(100)", False, False),
                                  Attributes("category_id", "uuid", False, False),
                                  Attributes("valid_from", "timestamp", True, False),
                                  Attributes("valid_to", "timestamp", True, False),
                                  Attributes("current_record", "nvarchar2(300)", True, False)
                              ]
                          ),
                          Entities(
                              Name="Time",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("date_id", "uuid", False, True),
                                  Attributes("day", "uuid", False, False),
                                  Attributes("month", "uuid", False, False),
                                  Attributes("quarter", "uuid", False, False),
                                  Attributes("year", "uuid", False, False),
                                  Attributes("isHoliday", "boolean", False, False)
                              ]
                          ),
                          Entities(
                              Name="Product",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("id", "uuid", False, True),
                                  Attributes("name", "nvarchar2(100)", False, False),
                                  Attributes("description", "nvarchar2(100)", False, False),
                                  Attributes("brand", "nvarchar2(100)", True, False),
                                  Attributes("category_id", "uuid", False, False),
                                  Attributes("valid_from", "timestamp", True, False),
                                  Attributes("valid_to", "timestamp", True, False),
                                  Attributes("current_record", "nvarchar2(300)", True, False)
                              ]
                          ),
                          Entities(
                              Name="Sales",
                              IsOverrideExisted=True,
                              Attributes=[
                                  Attributes("customer_id", "uuid", False, True),
                                  Attributes("date_id", "uuid", False, True),
                                  Attributes("store_id", "uuid", False, True),
                                  Attributes("product_di", "uuid", False, True),
                                  Attributes("units", "integer", False, False),
                                  Attributes("price", "decimal", False, False)
                              ]
                          ),
                      ]
                  )
              ]))

    db.session.add(
        Users(Username="admin",
              Password="5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5",
              IsAdmin=True,
              Schemas=[])
    )

    db.session.add(
        Users(Username="james.parker",
              Password="5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5",
              IsAdmin=True,
              Schemas=[
                  Schemas(
                      Name="Library",
                      Entities=[
                          Entities(
                              Name="Books",
                              Attributes=[
                                  Attributes("id", "uuid", False, True),
                                  Attributes("name", "nvarchar2(100)", False, False),
                                  Attributes("description", "nvarchar2(100)", False, False),
                                  Attributes("publisher_id", "uuid", False, False),
                                  Attributes("published_on", "timestamp", True, False),
                                  Attributes("price", "decimal", True, False)
                              ]
                          ),
                          Entities(
                              Name="Author",
                              Attributes=[
                                  Attributes("id", "uuid", False, True),
                                  Attributes("firstname", "nvarchar2(100)", False, False),
                                  Attributes("lastname", "nvarchar2(100)", False, False),
                                  Attributes("birthdate", "timestamp", True, False)
                              ]
                          ),
                          Entities(
                              Name="BookAuthor",
                              Attributes=[
                                  Attributes("book_id", "uuid", False, True),
                                  Attributes("author_id", "uuid", False, True)
                              ]
                          ),
                          Entities(
                              Name="Publisher",
                              Attributes=[
                                  Attributes("id", "uuid", False, True),
                                  Attributes("firstname", "nvarchar2(100)", False, False),
                                  Attributes("lastname", "nvarchar2(100)", False, False),
                                  Attributes("birthdate", "timestamp", True, False)
                              ]
                          )
                      ]
                  )
              ])
    )


    db.session.commit()
