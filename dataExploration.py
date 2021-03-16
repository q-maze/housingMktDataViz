import pandas as pd

input_df = pd.read_csv("Location_Affordability_Index_v_1.0.csv")
by_state = input_df.groupby('SF1_BlockGroups_STATE_NAME').mean()

# df = by_state['residential_density'].mean().to_frame(name='mean_res_dens').reset_index()

print(by_state.columns.tolist())
