library(GEOquery)
library(limma)
library(ggplot2)
library(plotly)
library(FamilyRank)

options("scipen" = 10)

# Reading Data from GEO using GEOquery
# Obtain using accession code, a real dataset of methylation data from healthy (control) and tb (case) patients
gset <- getGEO("GSE145714", GSEMatrix = TRUE, getGPL=FALSE)
gset <- gset$GSE145714_series_matrix.txt.gz
ex <- exprs(gset)

# Access metadata of the expression set to identify real groupings for patients, using characteristics from this can be a basis for better realism in simulations
meta_data <- pData(gset)
meta_data <- meta_data[,c(2,41:44)] # filter based on discrete categorical information
colnames(meta_data)[c(2:5)] <- c("hiv_status", "gender", "tb_status", "timepoint")
meta_data <- meta_data[order(meta_data$tb_status),c("hiv_status", "gender", "tb_status", "timepoint")] # order by binary status of tb status
print(meta_data)
# There exists an overrepresentation of patients with TB (10 to 22)

# Identifying the statistical properties of a simulated methylation dataset in comparison to a real dataset can help make the synthetic data more realistic
# Plot the distribution of average beta values across all samples
mean_cpg_across_samples = rowMeans(ex, na.rm=TRUE)
hist(mean_cpg_across_samples, main = "Distribution of CpG's for every Sample", xlab="Beta values",col="Green")

# This figure shows a bimodal distribution with two peaks, the simulation sampling was done using a uniform distribution where all beta-values had equal chances.
# Use FamilyRank's rbinorm function to generate 100 samples from a two component Guassian curve
bimodal_samples <- rbinorm(n=100, mean1=0.2, mean2=0.8, sd1=0.05, sd2=0.11, prop=.5)
plot(density(bimodal_samples), main = "Bimodal distribution")
# Draws from this distribution have a small chance of being outside the scope of realistic values (0,1) which means values which are outliers should be normalised and controlled for to be more realistic

# --- Python GEO read ---
#import GEOparse
#gse = GEOparse.get_GEO(geo="GSE145714", destdir="./", include_data=True)
#for gsm_name, gsm in gse.gsms.items():
#    print("Name: ", gsm_name)
#    print("Metadata: ",)
#    for key, value in gsm.metadata.items():
#        print(" - %s : %s" % (key, ", ".join(value)))
#    print("Table data: ",)
#    print(gsm.table)

# --- Python activities
#import random
#import numpy as np
#import pandas as pd
#import seaborn as sns
#from scipy.stats import uniform, ttest_ind
#import matplotlib.pyplot as plt
#from statsmodels.stats import multitest

def assign_donor_groups(donors):
    donors_with_groups = []
    for index in range(0,len(donors)):
        grouping_assigned = random.randint(0,1)
        if grouping_assigned == 1:
            label = 1
            new_groups = donors[index]
        elif grouping_assigned == 0:
            label = 0
            new_groups = donors[index]
        donor = np.concatenate([np.array([label]), new_groups])
        donors_with_groups.append(donor)
    return donors_with_groups

def assign_donor_groups_by_signal(donors):
    donors_with_groups_by_signal = []

    for index in range(0,len(donors)):
        if donors[index][0] == 1:
            label = 1
            new_groups = donors[index]
        elif donors[index][0] == 0:
            label = 0
            new_groups = donors[index]
        donor = np.concatenate([np.array([label]), new_groups])
        donors_with_groups_by_signal.append(donor)
    return donors_with_groups_by_signal

# Randomly assigning donors to groups
donors_with_groups = assign_donor_groups(donors)
donors_with_groups_df = pd.DataFrame(donors_with_groups)
#donors_with_groups = assign_donor_groups_by_signal(donors)
#donors_with_groups_df = pd.DataFrame(donors_with_groups)

# splitting donors into groups
group1 = donors_with_groups_df.loc[donors_with_groups_df[1]==1.0]
group2 = donors_with_groups_df.loc[donors_with_groups_df[1]==0.0]

def test_donor_group_difference(group1, group2):
    t_test_statistic, t_test_pvalue = ttest_ind(group1,group2, equal_var=True)
    return t_test_pvalue

t_test = test_donor_group_difference(group1,group2)

def p_adjust_fdr(t_test_output):
    rejected_bool, pvalue_corrected = multitest.fdrcorrection(pvals=t_test_output)
    return pd.DataFrame(pvalue_corrected)

#def repeat_generation_analysis(n_reps):
#    signal_strengths = [0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
#    p_value_sig_count = 0
#    for i in range(0, n_reps):
#        simulated_donors = simulate_donors(donor_count=60, size=size)
#        donors = make_donors_with_signal(simulated_donors, signal, signal_strengths[i])
#        donors_with_groups = assign_donor_groups_by_signal(donors)
#        donors_with_groups_df = pd.DataFrame(donors_with_groups)
#        group1 = donors_with_groups_df.loc[donors_with_groups_df[1] == 1.0]
#        group2 = donors_with_groups_df.loc[donors_with_groups_df[1] == 0.0]
#        t_test = test_donor_group_difference(group1, group2)
#        adjusted_t_tests = p_adjust_fdr(t_test)
#        for val in adjusted_t_tests.values:
#            if(val < 0.05):
#                p_value_sig_count += 1
#        data = sns.distplot(adjusted_t_tests)
#        plt.title('Histogram of p-values')
#        plt.xlabel('P-values')
#        plt.ylabel('Frequency')
#        plt.show()
#        print("Times sign p found: ",p_value_sig_count)

#repeat_generation_analysis(10)
