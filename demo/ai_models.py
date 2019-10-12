from demo.dbio import DemoMySQLIO

# Define your DataBase IO Module
db = DemoMySQLIO(debug=True)


def demo_ai_model(dbio, value):  # Do your Magic here ~~
    usr_df = dbio.user_info(value)
    email_type = usr_df['email'].str.rsplit("@", n=1, expand=True)
    email_type = email_type[1].str.rsplit(".com", n=1, expand=True)[0]
    usr_df['email_type'] = email_type
    return usr_df
