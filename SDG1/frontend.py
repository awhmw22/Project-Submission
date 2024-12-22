import streamlit as st
import pandas as pd
import pickle
import altair as alt

# Load the trained model using Streamlit's cache mechanism
@st.cache_data
def load_model():
    with open('best_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

def user_input_features():
    with st.sidebar:
        st.header('User Inputs for Prediction')
        sex = st.radio('Select Sex:', ['Male', 'Female'])
        age_group = st.radio('Select Age Group:', ['Youth', 'Adult', 'Senior'])
        year = st.slider('Select Year:', 2000, 2025, 2023)
        unemployment_rate = st.number_input('Enter Unemployment Rate (%):', min_value=0.0, max_value=100.0, step=0.1)

    data = {
        'Sex': {'Male': 0, 'Female': 1}[sex],
        'Age': {'Youth': 0, 'Adult': 1, 'Senior': 2}[age_group],
        'Year': year,
        'Value_unemployed': unemployment_rate
    }
    return pd.DataFrame(data, index=[0])

def suggest_interventions(prediction):
    if prediction > 5:
        return "High Poverty Risk - Recommend enhancing social support programs."
    return "Low Poverty Risk - Continue monitoring and supportive economic measures."

def main():
    st.title('Poverty Prediction Dashboard')
    st.write("This dashboard provides an interface to predict poverty rates based on demographic and economic factors.")
    
    model = load_model()
    input_df = user_input_features()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Input Parameters')
        st.write(input_df)

    prediction = model.predict(input_df[['Sex', 'Age', 'Year', 'Value_unemployed']])[0]
    interventions = suggest_interventions(prediction)

    with col2:
        st.subheader('Prediction and Interventions')
        st.write(f'Predicted Poverty Rate: {prediction:.2f}%')
        st.write(interventions)

    # Optional: Display data visualization if needed
    if st.checkbox('Show Impact Analysis'):
        # Simulate different unemployment rates and their impact
        unemployment_rates = pd.Series(range(int(input_df['Value_unemployed'][0]-5), int(input_df['Value_unemployed'][0]+6)))
        poverty_predictions = [
            model.predict(pd.DataFrame({
                'Sex': [input_df.at[0, 'Sex']],
                'Age': [input_df.at[0, 'Age']],
                'Year': [input_df.at[0, 'Year']],
                'Value_unemployed': [rate]
            }))[0] for rate in unemployment_rates
        ]
        
        impact_analysis = pd.DataFrame({
            'Unemployment Rate': unemployment_rates,
            'Predicted Poverty Rate': poverty_predictions
        })
        
        chart = alt.Chart(impact_analysis).mark_line().encode(
            x='Unemployment Rate:Q',
            y='Predicted Poverty Rate:Q',
            tooltip=['Unemployment Rate', 'Predicted Poverty Rate']
        ).properties(title="Impact of Unemployment Rate on Poverty Rate")
        st.altair_chart(chart, use_container_width=True)

if __name__ == "__main__":
    main()
