# Disease Spread App and Visualisations

### Description
Vietnam has a long coastal line, over two thousand rivers of different sizes and lengths, eight basins with a catchment area larger than 10,000 km2, and abundant surface water resources, hence exposes at a high level to climate-related hazards and extreme weather condition, e.g. monsoon, severe floods, droughts, etc. These geographic and meteorological characteristics cause a lot of challenges for not only economy, sustainable development, but also health sector. According to the results of the study “Health Vulnerability and Adaptation Assessment Under the Impacts of Climate Change in Vietnam” implemented by Hanoi University of Public Health (HUPH, 2018), in the period of 1997-2016 on climate-sensitive diseases has shown that on a yearly average basis there were 2,487,939 cases of influenza and 154,168 cases of dengue fever. In particular, diarrheal still ranked at the sixth leading cause of disability-adjusted life years (DALYs) and the fifth leading cause of premature death in 2016, accounting for 140,425 DALYs and 1,958 deaths. According to the Global Burden of Diseases Report, the projected burden on economy and society of climate-sensitive diseases in the coming decades is increasing and suffering strongly, which is due to lack of trained staffs, inadequate regulations, and poor facilities. This project aims to analyses the relationship among different environmental factors on the disease outbreaks in Vietnam, e.g., an early warning system for prioritized climate-sensitive diseases (dengue fever, influenza, diarrhea), a real-time monitoring and tracking of the spread of diseases for a faster and more efficient response to the outbreak, and a real-time recommendation system that can recommend the best controlling measures.
### Usage
The completed project will allow users to select a province of Vietnam from an interactive map, they will then select various parameters to display a relevent graph. They should also be able to select a machine learning model to visualise an outbreak prediction for the timeframe selected.
### File Structure

--->WebApp (Final Application)
    |
    --->FullData (contains datasets for indidual provinces)
    --->Saved_Models (contains models trained and saved by refine_dataset.ipynb)
    --->Templates (contains all web pages for web application)
        |
        --->Home.html
        --->Info.html
        --->Predict.html
        --->Stats.html
    --->app.py (backend/flask application)
    --->Final_full_cleaned_dataset.xlsx (combined dataset of all provinces)
    --->refine_dataset.ipynb (processes datasets, trains models and saves models)
    --->requirements.txt (requirements for all python files)
    --->test_app.py (unit tests for app.py)
    --->TestFile.csv (test csv for unit test)
    --->TestFile.xlsx (test excel for unit test)

### How to Deploy
Starting Program:
• Download Github repository
• Run pip install -r requirements.txt in command prompt
• Open command prompt at \WebApp
• Run python app.py
• Open browser and go to localhost:5000

### Reference:
[1] Climate Variability and Dengue Hemorrhagic Fever in Hanoi, Viet Nam, During 2008 to 2015,
2018.
