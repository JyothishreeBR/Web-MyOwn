import pandas as pd
import numpy as np

np.random.seed(42)  # For reproducibility

num_samples = 5000
# Features 
cgpa = np.round(np.random.uniform(5.0, 10.0, num_samples), 2)  # CGPA 5 to 10
backlogs = np.random.randint(0, 5, num_samples)               # 0 to 4 backlogs
certifications = np.random.randint(0, 10, num_samples)        # 0 to 9 certs
aptitude = np.random.randint(40, 100, num_samples)            # 40 to 100
coding = np.random.randint(40, 100, num_samples)              # 40 to 100
communication = np.random.randint(40, 100, num_samples)       # 40 to 100
projects = np.random.randint(0, 8, num_samples)               # 0 to 7 projects
hackathon = np.random.randint(0, 2, num_samples)              # 0 or 1
resume = np.random.randint(1, 11, num_samples)                # 1 to 10
branch = np.random.randint(0, 6, num_samples)                 # 0 to 5 for branches

# Generate target variables based on a simple rule
# Ready if CGPA > 7 and (aptitude + coding) > 120, else Not Ready
placement_readiness = ((cgpa > 7) & ((aptitude + coding + communication ) > 60)).astype(int)

# Company fit tiers based on CGPA and readiness (simple rule)
company_fit = []
for i in range(num_samples):
    if placement_readiness[i] == 1:
        if cgpa[i] >= 8 and aptitude[i] + coding[i] + communication[i] > 80:
            company_fit.append('Tier 1')
        elif  cgpa[i] > 6 and cgpa [i] < 8 and aptitude[i] +  coding[i] + communication[i] > 60:
            company_fit.append('Tier 2')
    else:
        company_fit.append('Not Eligible')

data = {
    'cgpa': cgpa,
    'backlogs': backlogs,
    'certifications': certifications,
    'aptitude': aptitude,
    'coding': coding,
    'communication': communication,
    'projects': projects,
    'hackathon': hackathon,
    'resume': resume,
    'branch': branch,
    'placement_readiness': placement_readiness,
    'company_fit': company_fit
}

df = pd.DataFrame(data)
df.to_csv('placement_data.csv', index=False)
print("Generated data saved to 'placement_data.csv'")