# The Impact of Income Inequality on Political Polarization

## Context and Methodology
In this project, I regress Political Polarization on Income Inequality to identify the correlation between these variables. I use state-level data from 2008 onwards to do pooled cross-section data. This is because there is not enought high-quality publicly available data that can be used to make panels and control for individual and time-fixed effects.

In the baseline model, I regress the absolute value of %entage of democratic voters in the state minus 50% on the Gini Coefficient (Measure of Income Inequality). After this baseline model, I control for education, unemployment and race in successive steps. 

## Data Sources
- I get the Presidential Election data from the MIT Election Lab
- Income Inequality data from statehealthcompare.shadac.org
- Education Data from the FRED
- Unemployment Data from the FRED
- Race Demographics Data from IPUMS NHGIS

## Results 

In the baseline model, the icient of Income Inequality is -0.5437 (significant at 5%). This means that for every 1 unit of increase in the Gini Index, the political polarization falls by 0.56%. This regression suggests that people with the same income have more political polarization among them, and the difference between incomes increases, political polarization decreases. 

In the full specification model, I control for unemployment rate, rates of bachelors degrees among adults and percentage white people in the state. This regression gives me -0.56 as the coefficient of income inequality. So, for every one unit increase in Gini Index, political polarization falls by 0.54%. 

<img width="1473" height="511" alt="image" src="https://github.com/user-attachments/assets/40285ebd-dcb5-43fa-a65f-17677811600c" />

<img width="1118" height="612" alt="image" src="https://github.com/user-attachments/assets/9a3b8134-356f-4599-bb43-660a6281a679" />

## Biases 

There are many omitted variables in this study because as we add more controls, the results become less significant. Because of the small sample size of this study to begin with, if I add too many controls, all results will become insignificant. Furthermore, I also cannot control for time and individual fixed effects because of lack of proper panel data. 

