import numpy as np
import pandas as pd
import sqlalchemy as db


def main():
    ctuFp = "/home/ubuntu/data/crpmt/sas_tracker_public.csv"
    df = pd.read_csv(ctuFp, sep=',', dtype=str, na_filter=False)

    # print(df)

    # Selecting and renaming columns to match DB column names
    df_person = df[["Contact", "Contact Title", "Contact email"]]
    df_person = df.rename(columns={"Contact": 'full_name', "Contact Title": 'position', "Contact email": 'email'})

    df_ctu = df[["Title", "CTU Short Name", "Address Info", "Status", "Country", "Contact"]]
    df_ctu = df_ctu.rename(columns={'Title': 'name', 'CTU Short Name': 'short_name', 'Address Info': 'address_info', 'Status': 'sas_verification', 'Country': 'country_id', 'Contact': 'contact_id'})

    # SAS verification true if approved, otherwise false
    df_ctu['sas_verification'] = np.where(df_ctu['sas_verification'] == "Approved", True, False)

    # Engine for connection
    user = input("Enter DB user: ")
    password = input("Enter DB password: ")
    engine = db.create_engine(f'postgresql+psycopg2://{user}:{password}@localhost:5441/crpmt')

    # Tables to use
    metadata = db.MetaData()
    countries = db.Table('countries', metadata, autoload_with=engine)
    persons = db.Table('persons', metadata, autoload_with=engine)
    ctus = db.Table('ctus', metadata, autoload_with=engine)

    with engine.connect() as conn:
        # Inserting CTU contacts
        conn.execute(persons.insert(), df_person.to_dict(orient='records'))
        conn.commit()

        for index, row in df_ctu.iterrows():
            # Getting country and contact FKs
            stmt_countries = db.select(countries.c.id).where(countries.c.iso3 == row["country_id"])
            stmt_persons = db.select(persons.c.id).where(persons.c.full_name == row["contact_id"])

            # All converts a CursorResult object into a Python Sequence (tuples)
            res_countries = conn.execute(stmt_countries).all()
            res_persons = conn.execute(stmt_persons).all()

            if (len(res_countries) == 0) :
                print(f"Couldn't find country from 3-letter code {row['country_id']}")
            if (len(res_persons) == 0) :
                print(f"Couldn't find person {row['contact_id']} (shouldn't happen)")
            
            if (len(res_countries) > 1) :
                print(f"Found too many countries from 3-letter code {row['country_id']}")
            if (len(res_persons) > 1) :
                print(f"Found too many {row['contact_id']} persons (shouldn't happen)")

            # Tuples with a single value
            row["country_id"] = res_countries[0][0]
            row["contact_id"] = res_persons[0][0]

            # print(row)

            # Inserting CTU
            conn.execute(ctus.insert(), row.to_dict())
            conn.commit()

    print("Done!")



if __name__ == "__main__":
    main()