import pandas as pd
import statsmodels.api as sm

income_df = pd.read_csv(r"https://raw.githubusercontent.com/vikram1221/poli_sci_project/refs/heads/main/Income%20inequality%20(Gini%20Coefficient).csv")

income_df.rename(columns = {"Data" : "Gini_Index", "TimeFrame" : "year", "Location" : "state"}, inplace = True)
# print(income_df.head(20))

president_df = pd.read_csv(r"https://raw.githubusercontent.com/vikram1221/poli_sci_project/refs/heads/main/1976-2024-president.csv")
president_df.drop(columns = ["state_fips", "state_ic", "office", "candidate", "writein", "version", "state_cen"], inplace = True)

# Create a seperate dataframe that has the %entage votes of the democratic party over the years
democrat_df = president_df[president_df["party_simplified"] == "DEMOCRAT"]
democrat_df.drop(columns = ["party_detailed"], inplace = True)

democrat_df["percentage_votes"] = democrat_df["candidatevotes"] / democrat_df["totalvotes"]

democrat_df["political_polarization"] = abs(democrat_df["percentage_votes"] - 0.50)
# print(democrat_df.head())


# Standardizing the dataframes for states to have data for only 2008, 2012, 2016, 2020, 2024

income_df["year"] = income_df["year"].astype(int)

years_considered = [2008, 2012, 2016, 2020, 2024]
income_df = income_df[income_df["year"].isin(years_considered)]
income_df["state"] = income_df["state"].str.upper()
# print(income_df.head(20))

democrat_df = democrat_df[democrat_df["year"].isin(years_considered)]
# print(democrat_df.head(20))

# Merging 
merged_df = pd.merge(income_df, democrat_df, on = ["state", "year"])
print(merged_df.head())

# Regressing political polarization on the genie index

y = merged_df["political_polarization"]
X = merged_df["Gini_Index"]

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

print(model.summary())


# Adding Education 
ed_df1 = pd.read_csv(r"https://raw.githubusercontent.com/vikram1221/poli_sci_project/refs/heads/main/fredgraph%20(1).csv")
ed_df2 = pd.read_csv(r"https://raw.githubusercontent.com/vikram1221/poli_sci_project/refs/heads/main/fredgraph%20(2).csv")
ed_df3 = pd.read_csv(r"https://raw.githubusercontent.com/vikram1221/poli_sci_project/refs/heads/main/fredgraph%20(3).csv")
ed_df4 = pd.read_csv(r"https://raw.githubusercontent.com/vikram1221/poli_sci_project/refs/heads/main/fredgraph%20(4).csv")
ed_df5 = pd.read_csv(r"https://raw.githubusercontent.com/vikram1221/poli_sci_project/refs/heads/main/fredgraph%20(5).csv")

ed_df1["observation_date"] = pd.to_datetime(ed_df1["observation_date"]).dt.year
ed_df2["observation_date"] = pd.to_datetime(ed_df2["observation_date"]).dt.year
ed_df3["observation_date"] = pd.to_datetime(ed_df3["observation_date"]).dt.year
ed_df4["observation_date"] = pd.to_datetime(ed_df4["observation_date"]).dt.year
ed_df5["observation_date"] = pd.to_datetime(ed_df5["observation_date"]).dt.year

ed_df1.rename(columns = {"observation_date": "year"}, inplace = True)
ed_df2.rename(columns = {"observation_date": "year"}, inplace = True)
ed_df3.rename(columns = {"observation_date": "year"}, inplace = True)
ed_df4.rename(columns = {"observation_date": "year"}, inplace = True)
ed_df5.rename(columns = {"observation_date": "year"}, inplace = True)


state_code_map = {
    "GCT1502AL": "Alabama",
    "GCT1502AK": "Alaska",
    "GCT1502AZ": "Arizona",
    "GCT1502AR": "Arkansas",
    "GCT1502CA": "California",
    "GCT1502CO": "Colorado",
    "GCT1502CT": "Connecticut",
    "GCT1502DE": "Delaware",
    "GCT1502DC": "District of Columbia",
    "GCT1502FL": "Florida",
    "GCT1502GA": "Georgia",
    "GCT1502HI": "Hawaii",
    "GCT1502ID": "Idaho",
    "GCT1502IL": "Illinois",
    "GCT1502IN": "Indiana",
    "GCT1502IA": "Iowa",
    "GCT1502KS": "Kansas",
    "GCT1502KY": "Kentucky",
    "GCT1502LA": "Louisiana",
    "GCT1502ME": "Maine",
    "GCT1502MD": "Maryland",
    "GCT1502MA": "Massachusetts",
    "GCT1502MI": "Michigan",
    "GCT1502MN": "Minnesota",
    "GCT1502MS": "Mississippi",
    "GCT1502MO": "Missouri",
    "GCT1502MT": "Montana",
    "GCT1502NE": "Nebraska",
    "GCT1502NV": "Nevada",
    "GCT1502NH": "New Hampshire",
    "GCT1502NJ": "New Jersey",
    "GCT1502NM": "New Mexico",
    "GCT1502NY": "New York",
    "GCT1502NC": "North Carolina",
    "GCT1502ND": "North Dakota",
    "GCT1502OH": "Ohio",
    "GCT1502OK": "Oklahoma",
    "GCT1502OR": "Oregon",
    "GCT1502PA": "Pennsylvania",
    "GCT1502RI": "Rhode Island",
    "GCT1502SC": "South Carolina",
    "GCT1502SD": "South Dakota",
    "GCT1502TN": "Tennessee",
    "GCT1502TX": "Texas",
    "GCT1502UT": "Utah",
    "GCT1502VT": "Vermont",
    "GCT1502VA": "Virginia",
    "GCT1502WA": "Washington",
    "GCT1502WV": "West Virginia",
    "GCT1502WI": "Wisconsin",
    "GCT1502WY": "Wyoming"
}

ed_df1 = ed_df1.rename(columns=state_code_map)
ed_df2 = ed_df2.rename(columns=state_code_map)
ed_df3 = ed_df3.rename(columns=state_code_map)
ed_df4 = ed_df4.rename(columns=state_code_map)
ed_df5 = ed_df5.rename(columns=state_code_map)

dfs = [ed_df1, ed_df2, ed_df3, ed_df4, ed_df5]

ed_long_dfs = []

for df in dfs:
    df_long = df.melt(id_vars="year", var_name="State", value_name="bachelors_or_higher_pct")

    ed_long_dfs.append(df_long)

education_long = pd.concat(ed_long_dfs, ignore_index=True)

education_long = education_long[education_long["year"].isin(years_considered)] 

education_long["State"] = education_long["State"].str.upper()

education_long.rename(columns = {"State" : "state"}, inplace = True)

# print(education_long.head(50))
# print(education_long.shape)

# Merging education with our previous dataset

ed_merged_df = pd.merge(merged_df, education_long, on = ["state", "year"])
print(ed_merged_df)

#  Regression model with education control
y = ed_merged_df["political_polarization"]
X = ed_merged_df[["Gini_Index", "bachelors_or_higher_pct"]]

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

print(model.summary())


# Adding unemployment
un_df1 = pd.read_csv(r"https://raw.githubusercontent.com/vikram1221/poli_sci_project/refs/heads/main/fredgraph%20(6).csv")
un_df2 = pd.read_csv(r"https://raw.githubusercontent.com/vikram1221/poli_sci_project/refs/heads/main/fredgraph%20(7).csv")
un_df3 = pd.read_csv(r"https://raw.githubusercontent.com/vikram1221/poli_sci_project/refs/heads/main/fredgraph%20(8).csv")
un_df4 = pd.read_csv(r"https://raw.githubusercontent.com/vikram1221/poli_sci_project/refs/heads/main/fredgraph%20(9).csv")
un_df5 = pd.read_csv(r"https://raw.githubusercontent.com/vikram1221/poli_sci_project/refs/heads/main/fredgraph%20(10).csv")

un_df1["observation_date"] = pd.to_datetime(un_df1["observation_date"]).dt.year
un_df2["observation_date"] = pd.to_datetime(un_df2["observation_date"]).dt.year
un_df3["observation_date"] = pd.to_datetime(un_df3["observation_date"]).dt.year
un_df4["observation_date"] = pd.to_datetime(un_df4["observation_date"]).dt.year
un_df5["observation_date"] = pd.to_datetime(un_df5["observation_date"]).dt.year

un_df1.rename(columns = {"observation_date": "year"}, inplace = True)
un_df2.rename(columns = {"observation_date": "year"}, inplace = True)
un_df3.rename(columns = {"observation_date": "year"}, inplace = True)
un_df4.rename(columns = {"observation_date": "year"}, inplace = True)
un_df5.rename(columns = {"observation_date": "year"}, inplace = True)

unemployment_code_map = {
    "LAUST010000000000003A": "Alabama",
    "LAUST020000000000003A": "Alaska",
    "LAUST040000000000003A": "Arizona",
    "LAUST050000000000003A": "Arkansas",
    "LAUST060000000000003A": "California",
    "LAUST080000000000003A": "Colorado",
    "LAUST090000000000003A": "Connecticut",
    "LAUST100000000000003A": "Delaware",
    "LAUST110000000000003A": "District of Columbia",
    "LAUST120000000000003A": "Florida",
    "LAUST130000000000003A": "Georgia",
    "LAUST150000000000003A": "Hawaii",
    "LAUST160000000000003A": "Idaho",
    "LAUST170000000000003A": "Illinois",
    "LAUST180000000000003A": "Indiana",
    "LAUST190000000000003A": "Iowa",
    "LAUST200000000000003A": "Kansas",
    "LAUST210000000000003A": "Kentucky",
    "LAUST220000000000003A": "Louisiana",
    "LAUST230000000000003A": "Maine",
    "LAUST240000000000003A": "Maryland",
    "LAUST250000000000003A": "Massachusetts",
    "LAUST260000000000003A": "Michigan",
    "LAUST270000000000003A": "Minnesota",
    "LAUST280000000000003A": "Mississippi",
    "LAUST290000000000003A": "Missouri",
    "LAUST300000000000003A": "Montana",
    "LAUST310000000000003A": "Nebraska",
    "LAUST320000000000003A": "Nevada",
    "LAUST330000000000003A": "New Hampshire",
    "LAUST340000000000003A": "New Jersey",
    "LAUST350000000000003A": "New Mexico",
    "LAUST360000000000003A": "New York",
    "LAUST370000000000003A": "North Carolina",
    "LAUST380000000000003A": "North Dakota",
    "LAUST390000000000003A": "Ohio",
    "LAUST400000000000003A": "Oklahoma",
    "LAUST410000000000003A": "Oregon",
    "LAUST420000000000003A": "Pennsylvania",
    "LAUST440000000000003A": "Rhode Island",
    "LAUST450000000000003A": "South Carolina",
    "LAUST460000000000003A": "South Dakota",
    "LAUST470000000000003A": "Tennessee",
    "LAUST480000000000003A": "Texas",
    "LAUST490000000000003A": "Utah",
    "LAUST500000000000003A": "Vermont",
    "LAUST510000000000003A": "Virginia",
    "LAUST530000000000003A": "Washington",
    "LAUST540000000000003A": "West Virginia",
    "LAUST550000000000003A": "Wisconsin",
    "LAUST560000000000003A": "Wyoming"
}


un_dfs = [un_df1, un_df2, un_df3, un_df4, un_df5]

un_dfs = [df.rename(columns=unemployment_code_map) for df in un_dfs]

un_long_dfs = []

for df in un_dfs:
    df_long = df.melt(id_vars="year", var_name="State", value_name="unemployment_rate")
    
    un_long_dfs.append(df_long)

unemployment_long = pd.concat(un_long_dfs, ignore_index=True)

unemployment_long = unemployment_long[unemployment_long["year"].isin(years_considered)]


unemployment_long["State"] = unemployment_long["State"].str.upper()

unemployment_long = unemployment_long.rename(columns={"State": "state"})

# print(unemployment_long.head(50))
# print(unemployment_long.shape)

un_merged_df = pd.merge(ed_merged_df, unemployment_long, on = ["state", "year"])
# print(un_merged_df.head(50))


# Regression model with education control
y = un_merged_df["political_polarization"]
X = un_merged_df[["Gini_Index", "bachelors_or_higher_pct", "unemployment_rate"]]

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

print(model.summary())

# Adding demographic controls to the dataset

demo_df = pd.read_csv(r"https://raw.githubusercontent.com/vikram1221/poli_sci_project/refs/heads/main/nhgis0001_ts_nominal_state.csv")
# print(demo_df.head(10))

# Rename the actual estimate columns, ignoring MOE columns
rename_map = {
    # White
    "B18AA115": "white_2011",
    "B18AA125": "white_2012",
    "B18AA135": "white_2013",
    "B18AA145": "white_2014",
    "B18AA155": "white_2015",
    "B18AA165": "white_2016",
    "B18AA175": "white_2017",
    "B18AA185": "white_2018",
    "B18AA195": "white_2019",
    "B18AA205": "white_2020",
    "B18AA215": "white_2021",
    "B18AA225": "white_2022",
    "B18AA235": "white_2023",
    "B18AA245": "white_2024",

    # Black
    "B18AB115": "black_2011",
    "B18AB125": "black_2012",
    "B18AB135": "black_2013",
    "B18AB145": "black_2014",
    "B18AB155": "black_2015",
    "B18AB165": "black_2016",
    "B18AB175": "black_2017",
    "B18AB185": "black_2018",
    "B18AB195": "black_2019",
    "B18AB205": "black_2020",
    "B18AB215": "black_2021",
    "B18AB225": "black_2022",
    "B18AB235": "black_2023",
    "B18AB245": "black_2024",

    # American Indian / Alaska Native
    "B18AC115": "native_2011",
    "B18AC125": "native_2012",
    "B18AC135": "native_2013",
    "B18AC145": "native_2014",
    "B18AC155": "native_2015",
    "B18AC165": "native_2016",
    "B18AC175": "native_2017",
    "B18AC185": "native_2018",
    "B18AC195": "native_2019",
    "B18AC205": "native_2020",
    "B18AC215": "native_2021",
    "B18AC225": "native_2022",
    "B18AC235": "native_2023",
    "B18AC245": "native_2024",

    # Asian / Pacific Islander / Other demo
    "B18AD115": "asian_pacific_other_2011",
    "B18AD125": "asian_pacific_other_2012",
    "B18AD135": "asian_pacific_other_2013",
    "B18AD145": "asian_pacific_other_2014",
    "B18AD155": "asian_pacific_other_2015",
    "B18AD165": "asian_pacific_other_2016",
    "B18AD175": "asian_pacific_other_2017",
    "B18AD185": "asian_pacific_other_2018",
    "B18AD195": "asian_pacific_other_2019",
    "B18AD205": "asian_pacific_other_2020",
    "B18AD215": "asian_pacific_other_2021",
    "B18AD225": "asian_pacific_other_2022",
    "B18AD235": "asian_pacific_other_2023",
    "B18AD245": "asian_pacific_other_2024",

    # Two or more racess
    "B18AE115": "two_or_more_2011",
    "B18AE125": "two_or_more_2012",
    "B18AE135": "two_or_more_2013",
    "B18AE145": "two_or_more_2014",
    "B18AE155": "two_or_more_2015",
    "B18AE165": "two_or_more_2016",
    "B18AE175": "two_or_more_2017",
    "B18AE185": "two_or_more_2018",
    "B18AE195": "two_or_more_2019",
    "B18AE205": "two_or_more_2020",
    "B18AE215": "two_or_more_2021",
    "B18AE225": "two_or_more_2022",
    "B18AE235": "two_or_more_2023",
    "B18AE245": "two_or_more_2024",
}

demo_df = demo_df.rename(columns = rename_map)

demo_df = demo_df[[col for col in demo_df.columns if not col.endswith("M")]]

# print(demo_df.head(10))

# Columns after renaming
demo_cols = [col for col in demo_df.columns if "_" in col and col.split("_")[-1].isdigit()]

demo_long_list = []

for col in demo_cols:
    parts = col.split("_")
    year = int(parts[-1])
    demo_var = "_".join(parts[:-1])

    temp = demo_df[["STATE", "STATEFP", col]].copy()
    temp = temp.rename(columns={
        "STATE": "state",
        col: demo_var
    })
    temp["year"] = year

    demo_long_list.append(temp)

demo_long = pd.concat(demo_long_list, ignore_index=True)

# Reshape so each state-year has all demo variables in one row
demo_long = demo_long.pivot_table(
    index=["state", "STATEFP", "year"],
    values=["white", "black", "native", "asian_pacific_other", "two_or_more"],
    aggfunc="first"
).reset_index()

# Standardize state names for merging
demo_long["state"] = demo_long["state"].str.upper()

demo_long["total"] = demo_long["asian_pacific_other"] + demo_long["black"] + demo_long["native"] + demo_long["white"]
demo_long["percentage_white"] = demo_long["white"] / demo_long["total"]


# print(demo_long.head(18))
# print(demo_long["year"].unique())
# print(demo_long.shape)

demo_long = demo_long[demo_long["year"].isin(years_considered)]

# print(demo_long.head(18))

demo_merged_df = pd.merge(un_merged_df, demo_long, on = ["state", "year"])
# print(demo_merged_df.head(15))

# Regressing with all previous controls and percentage_white population

y = demo_merged_df["political_polarization"]
X = demo_merged_df[["Gini_Index", "bachelors_or_higher_pct", "unemployment_rate", "percentage_white"]]

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

print(model.summary())


import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

# Get coefficients, drop intercept
coefs = model.params.drop("const")

# Optional: rename labels
coefs = coefs.rename({
    "Gini_Index": "Gini Index",
    "bachelors_or_higher_pct": "Bachelor's or Higher",
    "unemployment_rate": "Unemployment Rate",
    "percentage_white": "Percent White"
})

# Bar chart
plt.figure(figsize=(9, 5))
plt.bar(coefs.index, coefs.values, color = "firebrick")

plt.axhline(0, color="black", linewidth=1)
plt.title("Correlation between Key Socioeconomic Factors on Political Polarization over Last 4 Elections")
plt.ylabel("Impact Coefficient")
plt.xlabel("Socioeconomic Factors")
plt.xticks(rotation=0, ha="center")
plt.color("red")

plt.tight_layout()
plt.show()

print(demo_df.describe())