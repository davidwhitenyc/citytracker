import marimo

__generated_with = "0.19.9"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # citytracker.nyc
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > Developed by: David White david.white@changemakerdata.nyc<br>
    > Full Details on GitHub: https://github.com/davidwhitenyc/citytracker
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
        mo.image(
            src="https://raw.githubusercontent.com/davidwhitenyc/citytracker/main/docs/images/Flag_of_New_York_City.svg",
            width=400,
            height=300,
            rounded=True,
            alt="NYC Flag",
        ),
        mo.md("*Flag of the City of New York*"),
    ], align="start")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## About this project
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    >**[NYC Open Data](https://opendata.cityofnewyork.us/)** is a free public website where New York City government agencies share information with residents in a format anyone can access and use. The site contains thousands of datasets on topics like business, education, environment, and city services that people can search, download, and analyze. Whether you're a complete beginner curious about how your city works or an experienced researcher looking for specific statistics, the platform offers training classes, how-to guides, and tools to help you find and understand the data you need. It's designed to make government information transparent and useful for everyday New Yorkers, journalists, researchers, and anyone interested in exploring data about the city.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setting up our workspace using Marimo Notebooks
    """)
    return


@app.cell
def _():
    # 0.1 Import libraries for API access, data wrangling, and data visualization
    import marimo as mo
    import os
    from dotenv import load_dotenv
    from sodapy import Socrata
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt 
    import seaborn as sns
    import plotly.express as px
    import plotly.graph_objects as go
    from great_tables import GT, loc, style, md

    return Socrata, load_dotenv, mo, os, pd, sns


@app.cell
def _(mo):
    # 0.2 Set notebook-wide themes for text display (via CSS injection)
    mo.Html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

        /* Override Marimo's font variables */
        .marimo, :root {
            --marimo-heading-font: 'Space Grotesk', 'SF Pro Display', 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
            --marimo-text-font: 'Space Grotesk', 'SF Pro Display', 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
        }

        /* Typography */
        .prose {
            font-size: 1.125rem;
            line-height: 1.7;
            color: #2c3e50;
        }

        /* Headings with dark background */
        .prose h1, .prose h2 {
            background-color: #034C8C;
            color: #f2f2f2;
            padding: 0.6em 0.8em;
            border-radius: 4px;
            margin-top: 1.5em;
        }

        /* Headings without background */
        .prose h3, .prose h4 {
            color: #1a1a2e;
            margin-top: 1.5em;
        }

        .prose h1 { font-size: 7.5rem; font-weight: 700; }
        .prose h2 { font-size: 1.875rem; font-weight: 600; }
        .prose h3 { font-size: 1.375rem; font-weight: 500; }
        .prose h4 { font-size: 1.125rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }

    </style>
    """)
    return


@app.cell
def _(sns):
    # TODO
    # 0.3 Set notebook-wide themes for data graphics display

    nyc_palette = ["#E8692B", "#2A5A8C", "#5A89B3", "#B0B0B0", "#3A3A3A"]
    sns.set_theme(style="whitegrid")
    sns.set_palette(nyc_palette)
    return


@app.cell
def _():
    # TODO 
    # 0.4 Set custom defaults for the display of Great Tables tables
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Project styles reference
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Typography
    # Heading 1
    ## Heading 2
    ### Heading 3
    #### Heading 4
    *Body Text (italicized)*<br><br>
    **Body Text (with emphasis)**<br><br>
    ***Body Text (emphasis and italics)***<br><br>
    Body Text (regular)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Colors
    """)
    return


@app.cell
def _(mo):
    mo.image(
            src="https://raw.githubusercontent.com/davidwhitenyc/citytracker/main/docs/AdobeColor-color theme_Flag_of_New_York_City.jpeg",
            height=900,
            rounded=True,
            alt="NYC Flag-Inspired Color Theme",
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Loading data into our project
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Dataset 01: Affordable Housing Production by Building
    > The Department of Housing Preservation and Development (HPD) reports on projects, buildings, and units that began after January 1, 2014, and are counted towards either the Housing New York plan (1/1/2014 – 12/31/2021) or the Housing Our Neighbors: A Blueprint for Housing & Homelessness plan (1/1/2022 – present).<br>
    > [Data Source](https://data.cityofnewyork.us/Housing-Development/Affordable-Housing-Production-by-Building/hg8x-zxpr/about_data)<br>
    > [Data Dictionary](https://data.cityofnewyork.us/api/views/hg8x-zxpr/files/b960c601-e951-4103-9414-223adef41fce?download=true&filename=Affordable%20Housing%20Production%20by%20Building%20Data%20Dictionary.xlsx)
    """)
    return


@app.cell
def _(Socrata, load_dotenv, os, pd):
    ## 1. Load data from NYC Open Data via the Socrata API

    # 1.1 Load the Socrata App Token
    load_dotenv()

    token = os.getenv("SOCRATA_APP_TOKEN")

    client = Socrata("data.cityofnewyork.us", token)


    # 1.2 # Set the endpoint for the data pull
    socrata_url = 'data.cityofnewyork.us'

    endpoint = 'hg8x-zxpr' # This number is unique to each NYC dataset, see README for more information


    # 1.3 Select the data to pull using SQL-style language and create an object to contain the data
    query = """
        SELECT *
        LIMIT 100000
    """

    client = Socrata(
        socrata_url,
        app_token=None,
        timeout=1000
    )

    results = client.get(endpoint, query=query)

    # 1.4 Put the results into a DataFrame
    housing = pd.DataFrame.from_records(results)

    # # 1.5 Display DataFrame info
    # print(housing.info(verbose=True))

    # # 1.6 Glimpse
    # housing.sample(5)
    return (housing,)


@app.cell
def _(housing, pd):
    # 2. Set the appropriate data types for numeric and date columns

    housing['extemely_low_income_units'] = housing['extremely_low_income_units'].astype('float')
    housing['very_low_income_units'] = housing['very_low_income_units'].astype('float')
    housing['low_income_units'] = housing['low_income_units'].astype('float')
    housing['moderate_income_units'] = housing['moderate_income_units'].astype('float')
    housing['middle_income_units'] = housing['middle_income_units'].astype('float')
    housing['other_income_units'] = housing['other_income_units'].astype('float')

    housing['project_start_date'] = pd.to_datetime(housing['project_start_date'])
    housing['project_completion_date'] = pd.to_datetime(housing['project_completion_date'])

    # Create year columns for easier grouping
    housing['start_year'] = housing['project_start_date'].dt.year
    housing['completion_year'] = housing['project_completion_date'].dt.year
    return


@app.cell
def _(housing):

    # 3. Create a DataFrame grouped by year
    units_by_year = (
        housing.groupby(['start_year', 'borough'])[ ['extemely_low_income_units', 
                                                     'very_low_income_units', 
                                                     'low_income_units', 
                                                     'moderate_income_units', 
                                                     'middle_income_units', 
                                                     'other_income_units'] ].sum().reset_index()        
    )
    return (units_by_year,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Dataset 02: TKTK
    > TKTK.<br>
    > [Data Source]()<br>
    > [Data Dictionary]()
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Dataset 03: TKTK
    > TKTK.<br>
    > [Data Source]()<br>
    > [Data Dictionary]()
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Issue #1: Housing Affordability
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.image(
            src="https://raw.githubusercontent.com/davidwhitenyc/citytracker/main/docs/images/Zohran-Website-Quote-Housing.png",
            width="100%",
            rounded=True,
            alt="Quote from https://www.zohranfornyc.com/platform",
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Let's use the <code style="color:#E8692B">Affordable Housing Production by Building</code> NYC Open Data dataset to illustrate the current challenges regarding affordable housing, and track progress, if any, over time.
    """)
    return


@app.cell
def _():
    return


@app.cell
def _(sns, units_by_year):
    # TODO: Change 'year' and 'unit_type' to widgets

    # Filter for a specific year, then plot

    year_data = units_by_year[units_by_year['start_year'] == 2024]
    unit_type = 'extemely_low_income_units'
    sns.barplot(year_data, x='borough', y=unit_type, estimator='sum', errorbar=None)
    return


@app.cell
def _():
    # TODO
    # Add explanatory text to accompany this graphic
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Issue #2: TKTK
    """)
    return


@app.cell
def _():
    # TODO 

    # Add pull quote for issue #2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Issue #3: TKTK
    """)
    return


@app.cell
def _():
    # TODO 

    # Add pull quote for issue #3
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    """)
    return


if __name__ == "__main__":
    app.run()
