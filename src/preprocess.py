import pandas as pd
import numpy as np

def preprocess_input(user_input):
    """
    Takes raw user input dictionary
    Applies same tranformation as training data
    Retruns processed dataset ready for model
    """
   
    # Step 1 -  Convert Dict to DataFrame
    df = pd.DataFrame([user_input])

    # Step 2 - Cap RevolvingUtilizationOfUnsecuredLines at 1
    df["RevolvingUtilizationOfUnsecuredLines"] = df["RevolvingUtilizationOfUnsecuredLines"].clip(upper = 1)


    # Step 3 Cap DebtRatio at 10
    df["DebtRatio"] = df["DebtRatio"].clip(upper = 10)


    # Retrun the dataframe
    return df
