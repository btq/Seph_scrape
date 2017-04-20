import glob
import pandas as pd

filelist=glob.glob("files/sephora_hair_search_201*.xlsx")

all_df = pd.read_excel(filelist[0])

for f in filelist[1:]:
    this_df=pd.read_excel(f)
    all_df=all_df.append(this_df,ignore_index=True)
print all_df.shape

all_df.to_excel('files/sephora_hair_concat.xlsx',index=False)
