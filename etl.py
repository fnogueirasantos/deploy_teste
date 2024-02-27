import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

class Etl:

    def __init__(self, ID_COLUMN = 'id',NPS_COLUMN = 'Nps', dataset = pd.read_csv('Dataset_lite.csv'), ml = pd.read_csv('Features.csv')):
        self.ID_COLUMN = ID_COLUMN
        self.NPS_COLUMN = NPS_COLUMN
        self.dataset = dataset
        self.dataset_ml = ml
    
    def etl_barchart(self, select_column):
        df = self.dataset
        
        # Grouping by 'select_column' and 'NPSGroup', then counting the occurrences of self.ID_COLUMN
        df_barchart = (
            df.groupby([f'{select_column}', 'NPSGroup'])[self.ID_COLUMN]
            .count()
            .reset_index()
        )
        
        # Calculating the percentage based on the count of occurrences in each group
        df_barchart['Percentage'] = (
            round(df_barchart.groupby(f'{select_column}')[self.ID_COLUMN]
                .transform(lambda x: (x / x.sum()) * 100), 2)
        )
        
        # Creating a 'Text' column with the percentage values as strings
        df_barchart['Text'] = df_barchart['Percentage'].astype(str) + '%'
        
        # Returning the resulting DataFrame
        return df_barchart
    
    def etl_histogram(self, select_column):
        df = self.dataset
        df_hist = df[[f'{select_column}', 'Nps','NPSGroup']]
        # Return the resulting histogram if needed
        return df_hist
    
    def etl_machine_learning(self):
        feature_importance = self.dataset_ml.head(10)
        return feature_importance
    
    def etl_barcahart_services(self, df_filtered):
        df = df_filtered
        df_features = self.dataset_ml
        numeric_df = df.select_dtypes(include='number')
        numeric_df.drop(columns=['Departure Delay in Minutes','Arrival Delay in Minutes',
                                'Flight Distance','id','Age','TotalScore','Nps'], inplace=True)
        df_service = pd.DataFrame(round(numeric_df.describe(),2).T)[['mean']].reset_index()
        df_service['mean'] = (df_service['mean'] / 5) * 10
        df_service.rename(columns={'index':'Feature','mean':'Mean'}, inplace=True)
        bins = [0, 4, 10, float('inf')]
        labels = ['Low', 'Neutral', 'High']
        # Create a new column 'AgeGroup' based on the specified bins and labels
        df_features['ModelGroup'] = pd.cut(df_features['Importance'], bins=bins, labels=labels, right=False)
        df_features = df_features[['Feature','ModelGroup']]
        df_service = pd.merge(df_service, df_features, on='Feature', how='inner')
        df_service = df_service.sort_values(by='Mean', ascending=False)
        return df_service

if __name__ == "__main__":
    pass
