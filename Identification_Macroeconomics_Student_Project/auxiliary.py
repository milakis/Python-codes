import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from IPython.core.display import HTML


def data():
    df = pd.read_stata('data, R and html files/1section.dta')
    df['loansgdp'] = df.tloans/df.gdp
    return df.head()

def fig21():
    # dynamics of loans to gdp ratio over time for USA, Germany, Australia, France
    df = pd.read_stata('data, R and html files/1section.dta')
    usa = df[df.country == 'USA']
    ger = df[df.country == 'Germany']
    aus = df[df.country == 'Australia']
    fr = df[df.country == 'France']
    uk = df[df.country == 'UK']
    sp = df[df.country == 'Spain']
    
    fig = plt.figure(figsize=(10,5))
    plt.suptitle('Figure 2.1 Ratio of private loans to GDP in selected developed economies')
    
    plt.subplot(2, 3, 1)
    plt.plot(usa.year, usa.loansgdp, color='c')
    plt.title('USA')
    
    plt.subplot(2, 3, 2)
    plt.plot(ger.year, ger.loansgdp, color='c')
    plt.title('Germany')
    
    plt.subplot(2, 3, 3)
    plt.plot(aus.year, aus.loansgdp, color='c')
    plt.title('Australia')
    
    plt.subplot(2, 3, 4)
    plt.plot(fr.year, fr.loansgdp, color='c')
    plt.title('France', y=-0.35)
    
    plt.subplot(2, 3, 5)
    plt.plot(uk.year, uk.loansgdp, color='c')
    plt.title('UK', y=-0.35)
    
    plt.subplot(2, 3, 6)
    plt.plot(sp.year, sp.loansgdp, color='c')
    plt.title('Spain', y=-0.35)
    
    fig.text(0.05,-0.08,'Source: Jorda et al.(2013) set');
    plt.show()
    
def prep1():
    #preparation of excess credit dummy
    df = pd.read_stata('data, R and html files/1section.dta')
    df['loansgdp'] = df.tloans/df.gdp
    df['diff_loansgdp'] = 100*df['loansgdp'].diff()
    loans_table = df.pivot_table(values = 'diff_loansgdp', index = 'country', columns = 'year')
    pd.options.display.float_format = '{:,.3f}'.format
    mean_year = loans_table.mean() 
    mean_all = mean_year.mean()
    df['excredit'] = (df['diff_loansgdp'] > mean_all).astype(int)
    #data preparation
    df['year'] = df['year'].astype('int')
    df['pk_fin'] = df['pk_fin'].astype('int')
    df['pk_norm'] = df['pk_norm'].astype('int')
    df['lrgdp'] = np.log(df.rgdp)
    #copy to the file for R
    df.to_stata('data, R and html files/1section1.dta')
    df = df.loc[(df['pk_fin'] == 1) & (df['excredit'] == 1)]
    df = df[['year','country', 'pk_norm', 'pk_fin', 'excredit', 'pop', 'gdp', 'rgdp', 'lrgdp', 'tloans', 'loansgdp', 'diff_loansgdp', 'dlcpi', 'dlriy', 'stir', 'ltrate', 'ldlrgdp', 'ldlcpi', 'ldlriy', 'lstir', 'lltrate']]
    return df.head()

def data2():
    #obtaining the data
    df = pd.read_stata('data, R and html files/2section.dta')
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    df['year'] = df['year'].astype('int')
    df = df[['year', 'state', 'stateid', 'Total_GSP', 'cpi', 'population', 'spend', 'employ_CES', 'Dcpi_ACCRA']]
    #state output
    #output in millions
    df['out'] = df.Total_GSP*1000000
    #real output
    df['rout'] = df.out/df.cpi
    #real output per capita
    df['rcapout'] = df.rout/df.population
    #percent change of real output per capita
    df['Drcapout'] = df.sort_values(['year']).groupby('state')['rcapout'].pct_change()
    #state spending
    #real spending
    df['rspend'] = df.spend/df.cpi
    #real spending per capita
    df['rcapspend'] = df.rspend/df.population
    #real p.c.spending change as % of real p.c. output
    df['rcapspend_lag'] = df.sort_values('year').groupby(['state'])['rcapspend'].shift(1)
    df['rcapout_lag'] = df.sort_values('year').groupby(['state'])['rcapout'].shift(1)
    df['Drcapspend'] = (df.rcapspend - df.rcapspend_lag)/df.rcapout_lag
    #state employment
    #employment in thousands
    df['emp'] = df.employ_CES*1000
    #% change in employment rate
    df['emp_lag'] = df.sort_values('year').groupby(['state'])['emp'].shift(1)
    df['population_lag'] = df.sort_values('year').groupby(['state'])['population'].shift(1)
    df['Demp'] = (df.emp/df.population - df.emp_lag/df.population_lag)/(df.emp_lag/df.population_lag)
    #state population
    #% change of population
    df['Dpop'] = (df.population-df.population_lag)/df.population_lag
    #aggregate population
    df1 = df.groupby('year')['population'].sum()
    df1 = df1.to_frame().reset_index()
    df1 = pd.concat([df1]*51)
    df1 = df1.drop(columns="year")
    df1 = df1.to_numpy()
    df['population_nat'] = df1
    #aggregate output
    #aggregation of real output
    df1 = df.groupby('year')['rout'].sum()
    df1 = df1.to_frame().reset_index()
    df1 = pd.concat([df1]*51)
    df1 = df1.drop(columns="year")
    df1 = df1.to_numpy()
    df['rout_nat'] = df1
    #agg real output per capita
    df['rcapout_nat'] = df.rout_nat/df.population_nat
    #percent change of real output per capita
    df['Drcapout_nat'] = df.sort_values(['year']).groupby('state')['rcapout_nat'].pct_change()
    #aggregate spending
    #aggregation of real spending
    summ_spend = df.groupby('year')['rspend'].sum()
    summ_spend = summ_spend.to_frame().reset_index()
    df1 = pd.concat([summ_spend]*51)
    df1 = df1.drop(columns="year")
    df1 = df1.to_numpy()
    df['rspend_nat'] = df1
    #total national real spending per capita
    df['rcapspend_nat'] = df.rspend_nat/df.population_nat
    #change of national real (work) p.c. spending as % of real national output p.c.
    df['rcapspend_nat_lag'] = df.sort_values('year').groupby(['state'])['rcapspend_nat'].shift(1)
    df['rcapout_nat_lag'] = df.sort_values('year').groupby(['state'])['rcapout_nat'].shift(1)
    df['Drcapspend_nat'] = (df.rcapspend_nat - df.rcapspend_nat_lag)/df.rcapout_nat_lag
    df2 = df[['year', 'state', 'Drcapout', 'Drcapspend', 'Drcapspend_nat', 'Demp', 'Dpop']]
    df2.to_stata('data, R and html files/2section2.dta')
    return df2.head()

def fig31():
    #obtaining the data
    df = pd.read_stata('data, R and html files/2section.dta')
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    df['year'] = df['year'].astype('int')
    df = df[['year', 'state', 'stateid', 'Total_GSP', 'cpi', 'population', 'spend', 'employ_CES', 'Dcpi_ACCRA']]
    #state output
    #output in millions
    df['out'] = df.Total_GSP*1000000
    #real output
    df['rout'] = df.out/df.cpi
    #state spending
    #real spending
    df['rspend'] = df.spend/df.cpi
    #real spending per capita
    #data for states
    states = df[['year', 'state', 'rspend', 'rout']]
    IL = states[states.state == 'IL']
    CA = states[states.state == 'CA']
    #aggregate data
    summsp = df.groupby('year')['rspend'].sum()
    summsp = summsp.to_frame().reset_index()
    summout = df.groupby('year')['rout'].sum()
    summout = summout.to_frame().reset_index()
    summout = summout.drop(columns="year")
    summout = summout.to_numpy()
    summsp['rout'] = summout
    summsp['state'] = "All"
    #merge 3 datasets
    st = pd.concat([IL, CA])
    fin = pd.concat([st, summsp], sort=True)
    #spendings over output
    fin['spout'] = fin.rspend/fin.rout
    #create pivot table
    gr1 = pd.pivot_table(fin, index=['year'], columns=['state'], values=['spout'])
    #create graph
    plt.plot(gr1)
    plt.title("Figure 3.1 State Prime Military Contract Spending as a Fraction of State GDP")
    plt.xlabel("Year")
    plt.ylabel("Fraction")
    plt.legend(['California', 'National', 'Illinois']);
    plt.show()   

#running R files to obtain HTML tables files
import subprocess
def reg21():
    process = subprocess.Popen(['Rscript', 'reg21.R'], shell=False)
    return process.wait()

def reg22():
    process = subprocess.Popen(['Rscript', 'reg22.R'], shell=False)
    return process.wait()

def reg23():
    process = subprocess.Popen(['Rscript', 'reg23.R'], shell=False)
    return process.wait()

def reg31():
    process = subprocess.Popen(['Rscript', 'reg31.R'], shell=False)
    return process.wait()

def reg32():
    process = subprocess.Popen(['Rscript', 'reg32.R'], shell=False)
    return process.wait()

def fig41():
    #graph of ESPs by month 
    time = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    ESP = [3.2, 47.5, 27.9, 13.7, 1.0, 0.7, 0.9, 1.1, 0.2]
    fig, ax = plt.subplots()
    plt.bar(time, ESP, color='c')
    plt.ylabel('ESPs by billions $')
    plt.xticks(time, rotation=30)
    plt.title('Figure 4.1 Economic Stimulus Payments in 2008')
    fig.text(0.05,-0.08,'Source: the Internal Revenue Service');
    plt.show()
    
def table41():
    #table of short summary statistics
    df = pd.read_stata('data, R and html files/3section1.dta')
    stat = pd.DataFrame(columns = ['Variable', 'Value'])
    stat['Variable'] = ['Number of observations', 'Number of unique households', 'Number of households received ESPs', 'Average ESP in $']
    stat['Value'] = [df['newid'].count(), df.newid.nunique(), df[df['esp'] != 0].count()['newid'], df[df['esp'] != 0].mean()['esp']]
    pd.set_option('display.float_format', lambda x: '%.0f' % x)
    display(stat)
    
def fig42():
    df = pd.read_stata('data, R and html files/3section1.dta')
    #graph for the timing of ESPs reported by households
    short = df[df['esp'] != 0]
    short = short.yymm.value_counts()
    short = short.to_frame().reset_index()
    short.sort_values(by=['index'], inplace=True)
    yymm = list(short['yymm'])
    time1 = ['Jun 08', 'Jul 08', 'Aug 08', 'Sep 08', 'Oct 08', 'Nov 08', 'Dec 08', 'Jan 09', 'Feb 09', 'Mar 09']
    time1 = list(time1)
    fig, ax = plt.subplots()
    plt.bar(time1, yymm, color='c')
    plt.ylabel('Number of households received ESPs')
    plt.xticks(time1, rotation=30)
    plt.title('Figure 4.2 Timing of ESPs reported by households')
    fig.text(0.05,-0.08,'Source: EC Survey');
    plt.show()
    
def table42():
    #households characteristics
    df = pd.read_stata('data, R and html files/3section1.dta')
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    sm = df[['age', 'numkids', 'income', 'liqassii']].describe()
    display(sm)
    
def fig43():
    df = pd.read_stata('data, R and html files/3section1.dta')
    #obtaining the means for expenditures groups
    status = ['HH did not receive ESP', 'HH received ESP']
    food = [df.mean()['cfood'], df[df['esp'] != 0].mean()['cfood']]
    sne = [df.mean()['csnd'], df[df['esp'] != 0].mean()['csnd']]
    ne = [df.mean()['cndur'], df[df['esp'] != 0].mean()['cndur']]
    tot = [df.mean()['ctotsmed'], df[df['esp'] != 0].mean()['ctotsmed']]
    #creating the graph
    fig = plt.figure(figsize=(10, 5))
    plt.suptitle('Figure 4.3 Expenditures of households received and not received ESPs (in $)')
    plt.subplot(2, 2, 1)
    plt.bar(status, food, color='c')
    plt.title('Food expenditures')
    plt.ylim(1950, 2050)
    plt.subplot(2, 2, 2)
    plt.bar(status, sne, color='c')
    plt.title('Strictly nondurable expenditures')
    plt.ylim(4350, 4700)
    plt.subplot(2, 2, 3)
    plt.bar(status, ne, color='c')
    plt.title('Nondurable expenditures', y=-0.35)
    plt.ylim(5400, 5900)
    plt.subplot(2, 2, 4)
    plt.bar(status, tot, color='c')
    plt.title('Total expenditures', y=-0.35)
    plt.ylim(10700, 11050)
    plt.show()
    
def av_treat_effect():
    df = pd.read_stata('data, R and html files/3section1.dta')
    print('Average treatment effect of ESPs on food expenditures is ${:,.0f}.'.format(df[df['esp'] != 0].mean()['cfood'] - df.mean()['cfood']))
    print('Average treatment effect of ESPs on strictly nondurable expenditures is ${:,.0f}.'.format(df[df['esp'] != 0].mean()['csnd'] - df.mean()['csnd']))
    print('Average treatment effect of ESPs on nondurable  expenditures is ${:,.0f}.'.format(df[df['esp'] != 0].mean()['cndur'] - df.mean()['cndur']))
    print('Average treatment effect of ESPs on total expenditures is ${:,.0f}.'.format(df[df['esp'] != 0].mean()['ctotsmed'] - df.mean()['ctotsmed']))


def fig23():
    df = pd.read_stata('data, R and html files/1section.dta')
    df = df[['year', 'country', 'logdp', 'loloans', 'pkth']]
    #dataframe for the period 1870-1913
    dff = df.loc[df['year'] < 1914]
    #countries with patterns 2-1
    arrayf21 = ['Australia', 'Canada', 'Japan', 'Norway', 'Spain', 'Sweden', 'UK', 'USA']
    dff21 = dff.loc[dff['country'].isin(arrayf21)]
    #index for 2 and 1
    ipkf21 = dff21.index[dff21['pkth'] == 1].tolist()
    ithf21 = dff21.index[dff21['pkth'] == 2].tolist()
    #2 datasets with 2 and 1
    pkf21 = dff21.loc[ipkf21]
    thf21 = dff21.loc[ithf21]
    #add 2 datasets into 1
    f21 = pd.concat([thf21.reset_index(drop=True),pkf21.reset_index(drop=True)], axis=1)
    #countries with patterns 2-2
    arrayf22 = ['France', 'Switzerland']
    dff22 = dff.loc[dff['country'].isin(arrayf22)]
    #index for 2 and 1
    ipkf22 = dff22.index[dff22['pkth'] == 1].tolist()
    ithf22 = dff22.index[dff22['pkth'] == 2].tolist()
    #2 datasets with 2 and 1
    pkf22 = dff22.loc[ipkf22]
    thf22 = dff22.loc[ithf22]
    thf22 = thf22[thf22.year != 1913]
    f22 = pd.concat([thf22.reset_index(drop=True),pkf22.reset_index(drop=True)], axis=1)
    #countries with patterns 1-1
    arrayf11 = ['Denmark', 'Germany', 'Italy', 'Netherlands']
    dff11 = dff.loc[dff['country'].isin(arrayf11)]
    #index for 2 and 1
    ipkf11 = dff11.index[dff11['pkth'] == 1].tolist()
    ithf11 = dff11.index[dff11['pkth'] == 2].tolist()
    #2 datasets with 2 and 1
    pkf11 = dff11.loc[ipkf11]
    pkf11 = pkf11[pkf11.year != 1870]
    thf11 = dff11.loc[ithf11]
    f11 = pd.concat([thf11.reset_index(drop=True),pkf11.reset_index(drop=True)], axis=1)
    #merge 3 sets with all patterns
    f = f21.append([f22, f11], ignore_index = True)
    #rname columns
    f.columns = ['year2', 'country2', 'logdp2', 'loloans2', 'pkth2', 'year1', 'country1', 'logdp1', 'loloans1', 'pkth1']
    #gdp
    #difference in expansion 
    f['expgdp'] = f.logdp1 - f.logdp2
    #average change in expansion
    gdpfexp = f.expgdp.mean()
    #difference in recession
    f['logdp1_lag'] = f.logdp1.shift(1)
    f['recgdp'] = f.logdp2 - f.logdp1_lag 
    #average change in recession
    gdpfrec = f.recgdp.mean()
    #loans
    #difference in expansion 
    f['exploans'] = f.loloans1 - f.loloans2
    #average change in expansion
    loansfexp = f.exploans.mean()
    #difference in recession
    f['loloans1_lag'] = f.loloans1.shift(1)
    f['recloans'] = f.loloans2 - f.loloans1_lag 
    #average change in recession
    loansfrec = f.recloans.mean()
    #years
    #difference in expansion 
    f['expyear'] = f.year1 - f.year2
    #average change in expansion
    yearfexp = f.expyear.mean()
    #difference in recession
    f['year1_lag'] = f.year1.shift(1)
    f['recyear'] = f.year1_lag - f.year2 
    #average change in recession
    yearfrec = f.recyear.mean()
    #rate for gdp 
    gdpratefexp = gdpfexp/yearfexp
    gdpratefrec = gdpfrec/yearfrec
    #rate for loans
    loansratefexp = loansfexp/yearfexp
    loansratefrec = loansfrec/yearfrec
    #dataframe for the period 1920-1938
    dff = df.loc[(df['year'] > 1913) & (df['year'] < 1948)]
    #countries with patterns 2-1
    arrayf21 = ['Australia', 'Germany', 'Japan']
    dff21 = dff.loc[dff['country'].isin(arrayf21)]
    #index for 2 and 1
    ipkf21 = dff21.index[dff21['pkth'] == 1].tolist()
    ithf21 = dff21.index[dff21['pkth'] == 2].tolist()
    #2 datasets with 2 and 1
    pkf21 = dff21.loc[ipkf21]
    thf21 = dff21.loc[ithf21]
    #add 2 datasets into 1
    f21 = pd.concat([thf21.reset_index(drop=True),pkf21.reset_index(drop=True)], axis=1)
    #countries with patterns 2-2
    arrayf22 = ['Spain', 'Netherlands']
    dff22 = dff.loc[dff['country'].isin(arrayf22)]
    #index for 2 and 1
    ipkf22 = dff22.index[dff22['pkth'] == 1].tolist()
    ithf22 = dff22.index[dff22['pkth'] == 2].tolist()
    #2 datasets with 2 and 1
    pkf22 = dff22.loc[ipkf22]
    thf22 = dff22.loc[ithf22]
    thf22 = thf22[thf22.year != 1938]
    f22 = pd.concat([thf22.reset_index(drop=True),pkf22.reset_index(drop=True)], axis=1)
    #countries with patterns 1-1
    arrayf11 = ['Canada', 'Denmark', 'Italy', 'Norway', 'Sweden', 'UK']
    dff11 = dff.loc[dff['country'].isin(arrayf11)]
    #index for 2 and 1
    ipkf11 = dff11.index[dff11['pkth'] == 1].tolist()
    ithf11 = dff11.index[dff11['pkth'] == 2].tolist()
    #2 datasets with 2 and 1
    pkf11 = dff11.loc[ipkf11]
    pkf11 = pkf11[pkf11.year != 1920]
    thf11 = dff11.loc[ithf11]
    f11 = pd.concat([thf11.reset_index(drop=True),pkf11.reset_index(drop=True)], axis=1)           
    #countries with patterns 1-2
    arrayf12 = ['France', 'Switzerland', 'USA']
    dff12 = dff.loc[dff['country'].isin(arrayf12)]
    #index for 2 and 1
    ipkf12 = dff12.index[dff12['pkth'] == 1].tolist()
    ithf12 = dff12.index[dff12['pkth'] == 2].tolist()
    #2 datasets with 2 and 1
    pkf12 = dff12.loc[ipkf12]
    pkf12 = pkf12[pkf12.year != 1920]
    thf12 = dff12.loc[ithf12]
    thf12 = thf12[thf12.year != 1938]
    f12 = pd.concat([thf12.reset_index(drop=True),pkf12.reset_index(drop=True)], axis=1)
    #merge 3 sets with all patterns
    f = f21.append([f22, f11, f12], ignore_index = True)
    #rname columns
    f.columns = ['year2', 'country2', 'logdp2', 'loloans2', 'pkth2', 'year1', 'country1', 'logdp1', 'loloans1', 'pkth1']
    #gdp
    #difference in expansion 
    f['expgdp'] = f.logdp1 - f.logdp2
    #average change in expansion
    gdpsexp = f.expgdp.mean()
    #difference in recession
    f['logdp1_lag'] = f.logdp1.shift(1)
    f['recgdp'] = f.logdp2 - f.logdp1_lag 
    #average change in recession
    gdpsrec = f.recgdp.mean()
    #loans
    #difference in expansion 
    f['exploans'] = f.loloans1 - f.loloans2
    #average change in expansion
    loanssexp = f.exploans.mean()
    #difference in recession
    f['loloans1_lag'] = f.loloans1.shift(1)
    f['recloans'] = f.loloans1_lag - f.loloans2
    #average change in recession
    loanssrec = f.recloans.mean()
    #years
    #difference in expansion 
    f['expyear'] = f.year1 - f.year2
    #average change in expansion
    yearsexp = f.expyear.mean()
    #difference in recession
    f['year1_lag'] = f.year1.shift(1)
    f['recyear'] = f.year1_lag - f.year2 
    #average change in recession
    yearsrec = f.recyear.mean()
    #rate for gdp 
    gdpratesexp = gdpsexp/yearsexp
    gdpratesrec = gdpsrec/yearsrec
    #rate for loans
    loansratesexp = loanssexp/yearsexp
    loansratesrec = loanssrec/yearsrec
    #dataframe for the period 1948-1971
    dff = df.loc[(df['year'] > 1938) & (df['year'] < 1972)]
    #countries with patterns 2-1
    arrayf21 = ['Australia', 'Denmark', 'Japan', 'France', 'Germany', 'Italy', 'Netherlands', 'Norway', 'Sweden', 'UK']
    dff21 = dff.loc[dff['country'].isin(arrayf21)]
    #index for 2 and 1
    ipkf21 = dff21.index[dff21['pkth'] == 1].tolist()
    ithf21 = dff21.index[dff21['pkth'] == 2].tolist()
    #2 datasets with 2 and 1
    pkf21 = dff21.loc[ipkf21]
    thf21 = dff21.loc[ithf21]
    #add 2 datasets into 1
    f21 = pd.concat([thf21.reset_index(drop=True),pkf21.reset_index(drop=True)], axis=1)
    #countries with patterns 1-1
    arrayf11 = ['Canada', 'Spain', 'Switzerland', 'USA']
    dff11 = dff.loc[dff['country'].isin(arrayf11)]
    #index for 2 and 1
    ipkf11 = dff11.index[dff11['pkth'] == 1].tolist()
    ithf11 = dff11.index[dff11['pkth'] == 2].tolist()
    #2 datasets with 2 and 1
    pkf11 = dff11.loc[ipkf11]
    pkf11 = pkf11[pkf11.year != 1948]
    thf11 = dff11.loc[ithf11]
    f11 = pd.concat([thf11.reset_index(drop=True),pkf11.reset_index(drop=True)], axis=1)
    #merge 3 sets with all patterns
    f = f21.append(f11, ignore_index = True)
    #rname columns
    f.columns = ['year2', 'country2', 'logdp2', 'loloans2', 'pkth2', 'year1', 'country1', 'logdp1', 'loloans1', 'pkth1']
    #gdp
    #difference in expansion 
    f['expgdp'] = f.logdp1 - f.logdp2
    #average change in expansion
    gdptexp = f.expgdp.mean()
    #difference in recession
    f['logdp1_lag'] = f.logdp1.shift(1)
    f['recgdp'] = f.logdp2 - f.logdp1_lag 
    #average change in recession
    gdptrec = f.recgdp.mean()
    #loans
    #difference in expansion 
    f['exploans'] = f.loloans1 - f.loloans2
    #average change in expansion
    loanstexp = f.exploans.mean()
    #difference in recession
    f['loloans1_lag'] = f.loloans1.shift(1)
    f['recloans'] = f.loloans1_lag - f.loloans2
    #average change in recession
    loanstrec = f.recloans.mean()
    #years
    #difference in expansion 
    f['expyear'] = f.year1 - f.year2
    #average change in expansion
    yeartexp = f.expyear.mean()
    #difference in recession
    f['year1_lag'] = f.year1.shift(1)
    f['recyear'] = f.year1_lag - f.year2 
    #average change in recession
    yeartrec = f.recyear.mean()
    #rate for gdp 
    gdpratetexp = gdptexp/yeartexp
    gdpratetrec = gdpsrec/yeartrec
    #rate for loans
    loansratetexp = loanstexp/yeartexp
    loansratetrec = loanstrec/yeartrec
    #dataframe for the period 1972-2016
    dff = df.loc[(df['year'] > 1971) & (df['year'] <= 2016)]
    #countries with patterns 2-1
    arrayf21 = ['Australia', 'Denmark', 'Japan', 'France', 'Germany', 'Italy', 'Netherlands', 'Norway', 'Sweden', 'UK', 'Canada', 'Spain', 'Switzerland', 'USA']
    dff21 = dff.loc[dff['country'].isin(arrayf21)]
    #index for 2 and 1
    ipkf21 = dff21.index[dff21['pkth'] == 1].tolist()
    ithf21 = dff21.index[dff21['pkth'] == 2].tolist()
    #2 datasets with 2 and 1
    pkf21 = dff21.loc[ipkf21]
    thf21 = dff21.loc[ithf21]
    #add 2 datasets into 1
    f = pd.concat([thf21.reset_index(drop=True),pkf21.reset_index(drop=True)], axis=1)
    #rname columns
    f.columns = ['year2', 'country2', 'logdp2', 'loloans2', 'pkth2', 'year1', 'country1', 'logdp1', 'loloans1', 'pkth1']
    #gdp
    #difference in expansion 
    f['expgdp'] = f.logdp1 - f.logdp2
    #average change in expansion
    gdplexp = f.expgdp.mean()
    #difference in recession
    f['logdp1_lag'] = f.logdp1.shift(1)
    f['recgdp'] = f.logdp2 - f.logdp1_lag 
    #average change in recession
    gdplrec = f.recgdp.mean()
    #loans
    #difference in expansion 
    f['exploans'] = f.loloans1 - f.loloans2
    #average change in expansion
    loanslexp = f.exploans.mean()
    #difference in recession
    f['loloans1_lag'] = f.loloans1.shift(1)
    f['recloans'] = f.loloans1_lag - f.loloans2
    #average change in recession
    loanslrec = f.recloans.mean()
    #years
    #difference in expansion 
    f['expyear'] = f.year1 - f.year2
    #average change in expansion
    yearlexp = f.expyear.mean()
    #difference in recession
    f['year1_lag'] = f.year1.shift(1)
    f['recyear'] = f.year1_lag - f.year2 
    #average change in recession
    yearlrec = f.recyear.mean()
    #rate for gdp 
    gdpratelexp = gdplexp/yearlexp
    gdpratelrec = gdplrec/yearlrec
    #rate for loans
    loansratelexp = loanslexp/yearlexp
    loansratelrec = loanslrec/yearlrec
    #nice table with the results
    stat = pd.DataFrame(columns = ['Variable, period 1', 'Value, period 1', 'Variable, period 2', 'Value, period 2',  'Variable, period 3', 'Value, period 3', 'Variable, period 4', 'Value, period 4'])
    stat['Variable, period 1'] = ['gdpfexp', 'gdpfrec', 'loansfexp', 'loansfrec', 'gdpratefexp', 'gdpratefrec', 'loansratefexp', 'loansratefrec', 'yearfexp', 'yearfrec']
    stat['Value, period 1'] = [gdpfexp*100, gdpfrec*100, loansfexp*100, loansfrec*100, gdpratefexp*100, gdpratefrec*100, loansratefexp*100, loansratefrec*100, yearfexp, yearfrec]
    stat['Variable, period 2'] = ['gdpsexp', 'gdpsrec', 'loanssexp', 'loanssrec', 'gdpratesexp', 'gdpratesrec', 'loansratesexp', 'loansratesrec', 'yearsexp', 'yearsrec']
    stat['Value, period 2'] = [gdpsexp*100, gdpsrec*100, loanssexp*100, loanssrec*100, gdpratesexp*100, gdpratesrec*100, loansratesexp*100, loansratesrec*100, yearsexp, yearsrec]
    stat['Variable, period 3'] = ['gdptexp', 'gdptrec', 'loanstexp', 'loanstrec', 'gdpratetexp', 'gdpratetrec', 'loansratetexp', 'loansratetrec', 'yeartexp', 'yeartrec']
    stat['Value, period 3'] = [gdptexp*100, gdptrec*100, loanstexp*100, loanstrec*100, gdpratetexp*100, gdpratetrec*100, loansratetexp*100, loansratetrec*100, yeartexp, yeartrec]
    stat['Variable, period 4'] = ['gdplexp', 'gdplrec', 'loanslexp', 'loanslrec', 'gdpratelexp', 'gdpratelrec', 'loansratelexp', 'loansratelrec', 'yearlexp', 'yearlrec']
    stat['Value, period 4'] = [gdplexp*100, gdplrec*100, loanslexp*100, loanslrec*100, gdpratelexp*100, gdpratelrec*100, loansratelexp*100, loansratelrec*100, yearlexp, yearlrec]
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    #figure
    fig = plt.figure(figsize=(19, 16))
    plt.suptitle('Figure 2.3 Cyclical properties of output and credit in 4 periods')
    periods = ['Pre-WWI', 'WWI', 'BW', 'Post-BW']
    plt.subplot(3, 4, 1)
    gdpamplexp = [gdpfexp*100, gdpsexp*100, gdptexp*100, gdplexp*100]
    gdpamplexp = list(np.around(np.array(gdpamplexp),1))
    plt.bar(periods, gdpamplexp, color=['mediumorchid', 'limegreen', 'indianred', 'dodgerblue'])
    plt.ylabel('Percent')
    plt.ylim(-10, 40)
    plt.xlabel('Expansion')
    plt.title('Average amplitude, GDP growth')
    for a,b in zip(periods, gdpamplexp):
        plt.text(a, b, str(b)) 
    plt.subplot(3, 4, 2)
    gdpamplrec = [gdpfrec*100, gdpsrec*100, gdptrec*100, gdplrec*100]
    gdpamplrec = list(np.around(np.array(gdpamplrec),1))
    plt.bar(periods, gdpamplrec, color=['mediumorchid', 'limegreen', 'indianred', 'dodgerblue'])
    plt.ylabel('Percent')
    plt.ylim(-10, 40)
    plt.xlabel('Recession')
    plt.title('Average  amplitude, GDP growth')
    for a,b in zip(periods, gdpamplrec):
        plt.text(a, b, str(b))   
    plt.subplot(3, 4, 3)
    loansamplexp = [loansfexp*100, loanssexp*100, loanstexp*100, loanslexp*100]
    loansamplexp = list(np.around(np.array(loansamplexp),1))
    plt.bar(periods, loansamplexp, color=['mediumorchid', 'limegreen', 'indianred', 'dodgerblue'])
    plt.ylabel('Percent')
    plt.ylim(-10, 40)
    plt.xlabel('Expansion')
    plt.title('Average amplitude, loans growth')
    for a,b in zip(periods, loansamplexp):
        plt.text(a, b, str(b))  
    plt.subplot(3, 4, 4)
    loansamplrec = [loansfrec*100, loanssrec*100, loanstrec*100, loanslrec*100]
    loansamplrec = list(np.around(np.array(loansamplrec),1))
    plt.bar(periods, loansamplrec, color=['mediumorchid', 'limegreen', 'indianred', 'dodgerblue'])
    plt.ylabel('Percent')
    plt.ylim(-10, 40)
    plt.xlabel('Recession')
    plt.title('Average amplitude, loans growth')
    for a,b in zip(periods,loansamplrec):
        plt.text(a, b, str(b))
    plt.subplot(3, 4, 5)
    gdprateexp = [gdpratefexp*100, gdpratesexp*100, gdpratetexp*100, gdpratelexp*100]
    gdprateexp = list(np.around(np.array(gdprateexp),1))
    plt.bar(periods, gdprateexp, color=['mediumorchid', 'limegreen', 'indianred', 'dodgerblue'])
    plt.ylabel('Percent')
    plt.ylim(-7, 7)
    plt.xlabel('Expansion')
    plt.title('Average rate, GDP growth')
    for a,b in zip(periods, gdprateexp):
        plt.text(a, b, str(b))
    plt.subplot(3, 4, 6)
    gdpraterec = [gdpratefrec*100, gdpratesrec*100, gdpratetrec*100, gdpratelrec*100]
    gdpraterec = list(np.around(np.array(gdpraterec),1))
    plt.bar(periods, gdpraterec, color=['mediumorchid', 'limegreen', 'indianred', 'dodgerblue'])
    plt.ylabel('Percent')
    plt.ylim(-7, 7)
    plt.xlabel('Recession')
    plt.title('Average rate, GDP growth')
    for a,b in zip(periods, gdpraterec):
        plt.text(a, b, str(b))
    plt.subplot(3, 4, 7)
    loansrateexp = [loansratefexp*100, loansratesexp*100, loansratetexp*100, loansratelexp*100]
    loansrateexp = list(np.around(np.array(loansrateexp),1))
    plt.bar(periods, loansrateexp, color=['mediumorchid', 'limegreen', 'indianred', 'dodgerblue'])
    plt.ylabel('Percent')
    plt.ylim(-7, 7)
    plt.xlabel('Expansion')
    plt.title('Average rate, loans growth')
    for a,b in zip(periods, loansrateexp):
        plt.text(a, b, str(b))
    plt.subplot(3, 4, 8)
    loansraterec = [loansratefrec*100, loansratesrec*100, loansratetrec*100, loansratelrec*100]
    loansraterec = list(np.around(np.array(loansraterec),1))
    plt.bar(periods, loansraterec, color=['mediumorchid', 'limegreen', 'indianred', 'dodgerblue'])
    plt.ylabel('Percent')
    plt.ylim(-7, 7)
    plt.xlabel('Recession')
    plt.title('Average rate, loans growth')
    for a,b in zip(periods, loansraterec):
        plt.text(a, b, str(b))
    plt.subplot(3, 4, 9)
    yearexp = [yearfexp, yearsexp, yeartexp, yearlexp]
    yearexp = list(np.around(np.array(yearexp),1))
    plt.bar(periods, yearexp, color=['mediumorchid', 'limegreen', 'indianred', 'dodgerblue'])
    plt.ylabel('Years')
    plt.ylim(0, 10)
    plt.xlabel('Expansion')
    plt.title('Average duration')
    for a,b in zip(periods, yearexp):
        plt.text(a, b, str(b))
    plt.subplot(3, 4, 10)
    yearrec = [yearfrec, yearsrec, yeartrec, yearlrec]
    yearrec = list(np.around(np.array(yearrec),1))
    plt.bar(periods, yearrec, color=['mediumorchid', 'limegreen', 'indianred', 'dodgerblue'])
    plt.ylabel('Years')
    plt.ylim(0, 10)
    plt.xlabel('Recession')
    plt.title('Average duration')
    for a,b in zip(periods, yearrec):
        plt.text(a, b, str(b))
    plt.show()
