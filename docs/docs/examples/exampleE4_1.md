# Input data for creating a synthetic population

You can create a more specific synthetic population by providing more precise data about the population distribution for regions. This section describes all the input data that can be used for creating a synthetic population. You can create a synthetic population with only a few necessary input data and values. However, if you want to create a more specific synthetic population, you can provide more specific inputs described in this section. 

You can specify these specific data globally as described in [Synthpops configuration file](../Synthetic_pop_settings.md#input-data-global-dict) as a `csv`/`xlsx` file containing of paths to the files. Also you can specify them as 'default','all', or for each region or like 'CZ01' for each parent region name, like 'Czechia'.

**NOTE: All keys (column names) must be used in the default format. DO NOT RENAME THEM!**

## Types of input data
> **necessary input data:**

- Age distribution

> **Optional input data:**

- Region mobility data
- Employment rate
- Enrollment rate
- Household head age brackets
- Household head age distribution by family size
- School size brackets
- School size distribution
- School size distribution by type
- School types by age
- Workplace size counts by the number of people

### Age distribution data
The age distribution contains information about each region and its age distribution. You can use 16, 18 or 20 brackets for the age distribution settings. Also this is the place for providing information about the region code, its name and sum of the population. The distribution of all brackets must sum up to 1.0.

- For 16 brackets: 00_04,...,70_74,75_100
- For 18 brackets: 00_04,...,80_84,85_100
- For 20 brackets: 00_04,...,90_94,95_100

*An example* can be downloaded [here.](../synthpops_data/population_age_distribution.xlsx)

| location_code | name               | population | 00_04             | 05_09             | ... | 95_99             |
|---------------|--------------------|------------|-------------------|-------------------|-----|-------------------|
| CZ01          | Hlavní město Praha | 1241664    | 0.057312606308953 | 0.041531364362662 | ... | 0.0007804043606   |
| CZ02          | Středočeský kraj   | 1279345    | 0.063014276836975 | 0.051952366249917 | ... | 0.000469771640957 |

### region mobility data
Region mobility data can be used for adding people from different regions to a selected region. Basically, it simulates the number of people traveling across regions. These traveling agents are picked randomly from agents traveling from each region. The diagonal is empty, because it is not possible to travel from region to itself.

If the distribution information across regions is not known, you can specify a wider area, for example, a country. So you can use `Czechia` instead of `CZ01`, ..., `CZXX`. However, if you want to specify each region, you can do that as well, or you can also specify only some regions and the rest will be filled with the country level data. **NOTE: for a wider area you have to specify the country name not only in input data, but also in [Synthpops region configuration creater](../Synthetic_pop_settings.md#settings-for-region-configuration)**

*An example* can be downloaded [here.](../synthpops_data/NUTS2_mobility_data.csv)

| location_code | name               | CZ01   | CZ02  | ... | CZ08 |
|---------------|--------------------|--------|-------|-----|------|
| CZ01          | Hlavní město Praha |        | 15847 | ... | 169  |
| CZ02          | Středočeský kraj   | 100045 |       | ... | 121  |

### Employment rate distribution by age 
Employment distribution data stands for defining the probability of being employed at certain age defined from start year to the end year, commonly in the interval from 16 to 100 years of age. It can also hold region codes for another regions, but it will run only selected based on [main synthetic population settings](./exampleE4.md). It can use keys for region codes or region names, optionally. **NOTE: It depends on `region_data_name` defined in region settings, in supplied data must least one region name which correspond with region location code or a wider area name must be supplied**.

*An example* can be downloaded [here.](../synthpops_data/employment_rates_by_age.csv)

| Age | CZ01  | CZ02  | ... | CZ08  | Czechia |
|-----|-------|-------|-----|-------|---------|
| 16  | 0.332 | 0.319 | ... | 0.241 | 0       |
| 17  | 0.332 | 0.237 | ... | 0.310 | 0       |
| ... | ...   | ...   | ... | ...   | 0       |
| 100 | 0.064 | 0.039 | ..  | 0.015 | 0       |

### School enrollment rate distribution by age
School enrollment distribution data stands for defining the probability of being enrolled in school at certain age defined from start year to the end year, again from 16 to 100 years of age. The same instructions apply for region coding as in the employment rate distribution information above.

*An example* can be downloaded [here.](../synthpops_data/enrollment_rates_by_age.csv)

| Age | CZ01  | CZ02  | ... | CZ08  | Czechia |
|-----|-------|-------|-----|-------|---------|
| 0   | 0     | 0     | ... | 0     | 0       |
| ... | ...   | ...   | ... | ...   | ...     |
| 17  | 0.974 | 0.974 | ... | 0.974 | 0.974   |
| 18  | 0.707 | 0.707 | ... | 0.707 | 0.707   |
| ... | ...   | ...   | ... | ...   | ...     |
| 100 | 0     | 0     | ... | 0     | 0       |


### Household head age brackets
Household head age brackets are used for defining the age brackets for household head. It is used for creating household head age distribution. Every bracket is defined from minimum age to the maximum age, commonly between 15 and 100 years by step of 5. **NOTE: all household related input data must be based on this brackets**

*An Example* can be downloaded [here.](../synthpops_data/household_head_age_brackets.csv)

| min_age | max_age |
|---------|---------|
| 15      | 19      |
| 20      | 24      |
| ...     | ...     |
| 75      | 79      |
| 80      | 100     |

### Household head age distribution by family size
Household head age distribution by family size is used for defining the number of household heads at certain household head age brackets. Each row in this table specifies the distribution for a given family size. The family size is the first entry in the row. The remaining entries are, for each household head age bracket, the number or percentage of households with a household head in that age bracket. In the `*.csv` file the certain household head age brackets are defined by number from 0 to N (based on total number of brackets).

*An example* can be downloaded [here.](../synthpops_data/household_head_age_distribution_by_family_size.csv)

| number | 0     | 1    | 2      | ... | 13    |
|-----|-------|------|--------|-----|-------|
| 1   | 1.0   | 1.0  | 1.0    | ... | 1.0   |
| 2   | 163.0 | 999. | 2316.0 | ... | 2230  |
| ... | ...   | ...  | ...    | ... | ...   |
| 7   | 24.0  | 33.0 | 63.0   | ... | 144.0 |
| 8   | 0.0   | 0.0  | 0.0    | ... | 0.0   |

### Household size distribution
Household size distribution is used for defining the distribution of households at certain household size. Each row in this table specifies the distribution for a given household size. It depends on the household head age brackets. Every row is defined as the percentage distribution across given every row of household head age bracket. **NOTE: this household input data depends on household head age brackets. Also the sum of all distributions must be equal to 1**.

*An example* can be downloaded [here.](../synthpops_data/household_size_distribution.csv)

| number | distribution |
|-----|--------------|
| 1   | 0.064        |
| 2   | 0.108        |
| ... | ...          |
| 7   | 0.128        |
| 8   | 0.0          |

### School size brackets
School size brackets are used for defining the size of school. It is used for creating school size distribution. Every bracket is defined from the minimum to the maximum size. **NOTE: all school related input data must be based on these brackets**

*An example* can be downloaded [here.](../synthpops_data/school_size_brackets.csv)

| min  | max  |
|------|------|
| 20   | 50   |
| 51   | 100  |
| 101  | 300  |
| ...  | ...  |
| 2301 | 2700 |

### School size distribution
School size distribution is used for defining the number of schools at certain school size brackets. Each row in this table specifies the distribution for a given school size. It depends on the school size brackets. Every row is defined as the percentage distribution across given every row of the school size bracket.

*An example* can be downloaded [here.](../synthpops_data/school_size_distribution.csv)

| distribution         |
|----------------------|
| 0.06024096385542162  |
| 0.07831325301204821  |
| ...                  |
| 0.006024096385542101 |
| 0.0                  |

### School size distribution by type
School size distribution by type is used for defining the distribution of school size by school type. Each row in this table specifies the distribution for a given school type. It depends on the school size brackets. Every row is defined as the percentage distribution across given every row of school size bracket. You can specify types of school by yourself and set them age distribution in [school types by age](#school-types-by-age) section. **NOTE: this school input data depends on school size brackets and on [school types by age](#school-types-by-age). Also every row distribution sum must be equal to 1**.

`pk` = preschool, `es` = elementary school, `ms` = middle school, `hs` = high school, `uv` = university

*An example* can be downloaded [here.](../synthpops_data/school_size_distribution_by_type.csv)

| school_type | distribution                                                                                    |
|-------------|-------------------------------------------------------------------------------------------------|
| pk          | "0.012658227848101266, 0.0, ..., 0.43037974683544306, 0.0, 0.0, 0.0, 0.0, 0.0,"                 |
| es          | "0.012658227848101266, 0.0, ..., 0.43037974683544306, 0.0, 0.0, 0.0, 0.0, 0.0,"                 |
| hs          | "0.07407407407407407, 0.1111111111111111, ... , 0.18518518518518517, 0.0, 0.0 , 0.0"            |
| uv          | "0.027522935779816515, 0.009174311926605505, ... , 0.2018348623853211, 0.3944954128440367, 0.0" |

**NOTE: distribution must be in double quotes to be validly parsed**

### School types by age
School types by age is used for defining the age distribution for each school type. It is used for creating school age distribution. Every row in this table specifies the distribution for a given school type. You can define here those school types.

`pk` = preschool, `es` = elementary school, `ms` = middle school, `hs` = high school, `uv` = university

*An example* can be downloaded [here.](../synthpops_data/school_types_by_age.csv)

| school_type | min_age | max_age |
|-------------|---------|---------|
| pk          | 3       | 5       |
| es          | 6       | 10      |
| hs          | 15      | 18      |
| uv          | 19      | 100     |

### Workplace size counts by number of people
Workplace size counts is defined by number of people in a specific workplace and the total count of those workplaces. There are defined "brackets" for minimum to maximum agents per workplace and the total count of those workplaces.

*An example* can be downloaded [here.](../synthpops_data/workplace_size_counts_by_num_personnel.csv)

| min_people | max_people | count    |
|------------|------------|----------|
| 1          | 4          | 107682.0 |
| 5          | 9          | 35584.0  |
| ...        | ...        | ...      |
| 500        | 999        | 245.0    |
| 1000       | 1999       | 150.0    |
