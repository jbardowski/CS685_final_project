import pandas, csv
scope3_categories = ["Purchased goods and services",
    "Capital goods",
    "Fuel and energy-related activities",
    "Upstream transportation and distribution",
    "Waste generated in operations",
    "Business travel",
    "Employee commuting",
    "Upstream leased assets",
    "Downstream transportation and distribution",
    "Processing of sold products",
    "Use of sold products",
    "End-of-life treatment of sold products",
    "Downstream leased assets",
    "Franchises",
    "Investments",
]

# ================= TUNING SECTION =====================
LINE_COUNT_WEIGHT = 0.7

GENERIC = 0.3
SPECIFIC = 0.6
VAGUE = 0.3
SPECIFICITY_WEIGHT = 0.1

CATEGORY_WEIGHT = 0.3

SCOPE_3_WEIGHT = 1.1
RAW_SCOPE_3 = 0.8

SAT_WEIGHT = 15

if __name__ == "__main__":
    FILENAME = 'report_prediction.csv'
    df = pandas.read_csv(FILENAME)
    
    file_count = df['file'].unique().size
    score_map = pandas.DataFrame({"score": [0]*file_count, 
                                  "total_scope3":[0]*file_count, 
                                  "total_esg": [0]*file_count,
                                  "saturation": [0]*file_count}, 
                                 index=[k for k in df['file'].unique()])
    print(score_map.head())
    label_map = {"vague": VAGUE, "generic": GENERIC, "specific": SPECIFIC}
    for fn in df['file'].unique():
        fn_df = df.loc[df['file'] == fn]
        total_scope3 = fn_df.loc[fn_df['predicted_scope3'] == "yes"].size
        score_map["total_scope3"][fn] = total_scope3
        total_esg = fn_df.loc[fn_df['predicted_vague'] != "notESG"].size
        score_map["total_esg"][fn] = total_esg
        
        # add points for specificity + scope 3
        total_specific_scope3 = fn_df.loc[(fn_df["predicted_vague"] == "specific") & (fn_df["predicted_scope3"] == "yes")].size
        for v, n in label_map.items():
            specificity_bonus = fn_df.loc[(fn_df["predicted_vague"] == v) & (fn_df["predicted_scope3"] == "yes")].size * n
            score_map["score"][fn] += specificity_bonus * SCOPE_3_WEIGHT
        
        # add minor points for specificity and no scope 3
        for v, n in label_map.items():
            esg_bonus = fn_df.loc[(fn_df["predicted_vague"] == v) & (fn_df["predicted_scope3"] == "no")].size * n
            score_map["score"][fn] += esg_bonus * SPECIFICITY_WEIGHT
           
        
        # raw specific scope 3 scaling:
        
        score_map["score"][fn] +=  total_specific_scope3 * RAW_SCOPE_3 
        
        # saturation bonus
        saturation = 0.1 # pity default
        if total_scope3:
            saturation = (total_specific_scope3 / total_scope3)    
        
        score_map["saturation"][fn] = saturation
        # score_map["score"][fn] += saturation * SAT_WEIGHT
        
    # normailze data:
    a, b = 0, 100
    x, y = score_map.score.min(), score_map.score.max()
    score_map['norm_score'] = (score_map.score - x) / (y - x) * (b - a) + a
    print(score_map.head())
    score_map.sort_values(by="norm_score", inplace=True)
    score_map.to_csv("final_scores.csv")
        
    
    