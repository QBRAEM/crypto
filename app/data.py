import pandas as pd
import numpy as np
import pickle as pk
import datetime

def generate():
    types = {
        "row_id": 'int32',
        "Asset_ID": 'int8',
        "Count": 'int32',
        "Open": 'float64',
        "High": 'float64',
        "Low": 'float64',
        "Close": 'float64',
        "Volume": 'float64',
        "VWAP": 'float64',
    }

    assets = pd.read_csv("g-research-crypto-forecasting/asset_details.csv")
    df = pd.read_csv("g-research-crypto-forecasting/train.csv", dtype=types)
    df = df.replace([np.inf, -np.inf], np.nan).ffill().bfill()
        
    asset_list = []
    for i, asset in assets.iterrows():
        asset_id = asset["Asset_ID"]
        asset_name = asset["Asset_Name"]
        asset_weight = asset["Weight"]
        df_asset = df[df["Asset_ID"] == asset_id].set_index("timestamp")
        df_asset = df_asset.reindex(np.array(range(df_asset.index[0], df_asset.index[-1] + 60, 60))).ffill()
        df_asset.reset_index(inplace=True)
        
        # Asset list
        asset_list.append({
            "Asset_ID": asset_id,
            "Asset_Name": asset_name,
            "Asset_Weight": asset_weight,
        })
        
        # Data for forecasting
        # TODO: Add shadows and stuff
        # with open("./df_asset_forecast_%d.data" % asset_id, 'wb') as f:
        #     pickler = pk.Pickler(f)
        #     pickler.dump({
        #         "Asset_ID": asset_id,
        #         "Asset_Name": asset_name,
        #         "Asset_Weight": asset_weight,
        #         "Asset_Data": df_asset,
        #     })
        
        # Data for visualization
        df_asset_viz = df_asset.copy()
        df_asset_viz["timestamp_hour"] = df_asset_viz["timestamp"] // 3600
        df_asset_viz = df_asset_viz.groupby("timestamp_hour").mean().set_index("timestamp")
        df_asset_viz.reset_index(inplace=True)
        df_asset_viz["Open_0_1"] = (df_asset_viz["Open"] - df_asset_viz["Open"].min()) / (df_asset_viz["Open"].max() - df_asset_viz["Open"].min())
        df_asset_viz["High_0_1"] = (df_asset_viz["High"] - df_asset_viz["High"].min()) / (df_asset_viz["High"].max() - df_asset_viz["High"].min())
        df_asset_viz["Low_0_1"] = (df_asset_viz["Low"] - df_asset_viz["Low"].min()) / (df_asset_viz["Low"].max() - df_asset_viz["Low"].min())
        df_asset_viz["Close_0_1"] = (df_asset_viz["Close"] - df_asset_viz["Close"].min()) / (df_asset_viz["Close"].max() - df_asset_viz["Close"].min())
        df_asset_viz["VWAP_0_1"] = (df_asset_viz["VWAP"] - df_asset_viz["VWAP"].min()) / (df_asset_viz["VWAP"].max() - df_asset_viz["VWAP"].min())
        df_asset_viz["Target_0_1"] = (df_asset_viz["Target"] - df_asset_viz["Target"].min()) / (df_asset_viz["Target"].max() - df_asset_viz["Target"].min())
        df_asset_viz["datetime"] = df_asset_viz.apply(lambda row: datetime.datetime.fromtimestamp(row["timestamp"]), axis=1)
        with open("./df_asset_viz_%d.data" % asset_id, 'wb') as f:
            pickler = pk.Pickler(f)
            pickler.dump({
                "Asset_ID": asset_id,
                "Asset_Name": asset_name,
                "Asset_Weight": asset_weight,
                "Asset_Data": df_asset_viz,
            })
        

    with open("./asset_list.data", 'wb') as f:
        pickler = pk.Pickler(f)
        pickler.dump(asset_list)
        
            
    
    
def load_asset_list():
    with open("./asset_list.data", 'rb') as f:
        unpickler = pk.Unpickler(f)
        asset_list = unpickler.load()
    return asset_list
    

