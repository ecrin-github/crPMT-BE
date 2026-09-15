from getpass import getpass
import numpy as np
import pandas as pd
import sqlalchemy as db


"""
From the CTUs Service Providers list
"""



def main():
    # Change these values accordingly
    ctuFp = "/home/ubuntu/data/ctus/CTUs Service Providers.csv"
    db_hostname = "localhost"
    db_port = "5441"
    db_name = "crpmt"
    
    df = pd.read_csv(ctuFp, sep=',', dtype=str, na_filter=False)

    # Selecting and renaming columns to match DB column names
    df_ctu = df[["CTU Short Name", "CTU Name", "Address Info", "Country"]]
    df_ctu = df_ctu.rename(columns={'CTU Short Name': 'short_name', 'CTU Name': 'name', 'Address Info': 'address_info', 'Country': 'country_id'})
    df_ctu["manual_add"] = False

    # Engine for connection
    user = input("Enter DB user: ")
    password = getpass("Enter DB password: ")
    engine = db.create_engine(f'postgresql+psycopg2://{user}:{password}@{db_hostname}:{db_port}/{db_name}')

    # Tables to use
    metadata = db.MetaData()
    countries = db.Table('countries', metadata, autoload_with=engine)
    ctus = db.Table('ctus', metadata, autoload_with=engine)

    with engine.connect() as conn:
        for index, row in df_ctu.iterrows():
            # Getting country and contact FKs
            stmt_countries = db.select(countries.c.iso2).where(countries.c.iso3 == row["country_id"])

            # All converts a CursorResult object into a Python Sequence (tuples)
            res_countries = conn.execute(stmt_countries).all()

            if (len(res_countries) == 0) :
                print(f"Couldn't find country from 3-letter code {row['country_id']}")
            
            if (len(res_countries) > 1) :
                print(f"Found too many countries from 3-letter code {row['country_id']}")

            # Tuples with a single value
            if len(res_countries) > 0:
                row["country_id"] = res_countries[0][0]
            else:
                row["country_id"] = None

            # print(row)

            # Inserting CTU
            conn.execute(ctus.insert(), row.to_dict())
        conn.commit()

    print("Done!")



if __name__ == "__main__":
    main()