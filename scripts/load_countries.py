import pandas as pd
import sqlalchemy as db


def main():
    countriesFp = "/home/ubuntu/data/countries/countryInfoCleaned.tsv"
    df = pd.read_csv(countriesFp, sep='\t', dtype=str, na_filter = False)

    # Engine for connection
    user = input("Enter DB user: ")
    password = input("Enter DB password: ")
    engine = db.create_engine(f'postgresql+psycopg2://{user}:{password}@localhost:5441/crpmt')

    # Selecting and renaming columns to match DB column names
    values_list = df[["#ISO", "ISO3", "Country", "Continent"]]
    values_list = values_list.rename(columns={'#ISO': 'iso2', 'ISO3': 'iso3', 'Country': 'name', 'Continent': 'continent'})

    # Table to use
    metadata = db.MetaData()
    countries = db.Table('countries', metadata, autoload_with=engine)

    # Inserting countries
    with engine.connect() as conn:
        conn.execute(countries.insert(), values_list.to_dict(orient='records'))
        conn.commit()
    
    print("Done!")



if __name__ == "__main__":
    main()