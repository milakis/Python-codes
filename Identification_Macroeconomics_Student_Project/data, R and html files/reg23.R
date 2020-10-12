#necessary packages
require(plm)
require(foreign)
require(stargazer)
require(lmtest)
#data
Rdata = read.dta("data, R and html files/1section1.dta")
#running the regression with interaction term and macrocntrols 
regc1 <- lm(lrgdpp1~pk_norm+pk_fin+pk_norm*excredit+pk_fin*excredit+dlrgdp+dlcpi+dlriy+stir+ltrate+ldlrgdp+ldlcpi+ldlriy+lstir+lltrate+factor(country), data = Rdata)
regc11 = coeftest(regc1, vcov = vcovHC(regc1, type = "HC0"))
regc2 <- lm(lrgdpp2~pk_norm+pk_fin+pk_norm*excredit+pk_fin*excredit+dlrgdp+dlcpi+dlriy+stir+ltrate+ldlrgdp+ldlcpi+ldlriy+lstir+lltrate+factor(country), data = Rdata)
regc22 = coeftest(regc2, vcov = vcovHC(regc2, type = "HC0"))
regc3 <- lm(lrgdpp3~pk_norm+pk_fin+pk_norm*excredit+pk_fin*excredit+dlrgdp+dlcpi+dlriy+stir+ltrate+ldlrgdp+ldlcpi+ldlriy+lstir+lltrate+factor(country), data = Rdata)
regc33 = coeftest(regc3, vcov = vcovHC(regc3, type = "HC0"))
regc4 <- lm(lrgdpp4~pk_norm+pk_fin+pk_norm*excredit+pk_fin*excredit+dlrgdp+dlcpi+dlriy+stir+ltrate+ldlrgdp+ldlcpi+ldlriy+lstir+lltrate+factor(country), data = Rdata)
regc44 = coeftest(regc4, vcov = vcovHC(regc4, type = "HC0"))
regc5 <- lm(lrgdpp5~pk_norm+pk_fin+pk_norm*excredit+pk_fin*excredit+dlrgdp+dlcpi+dlriy+stir+ltrate+ldlrgdp+ldlcpi+ldlriy+lstir+lltrate+factor(country), data = Rdata)
regc55 = coeftest(regc5, vcov = vcovHC(regc5, type = "HC0"))
#producing the nice table
stargazer(regc11, regc22, regc33, regc44, regc55,  type='text', out='reg23.html', keep=c('pk_norm', 'pk_fin', 'pk_norm:excredit', 'pk_fin:excredit'), digits=1, dep.var.labels=c('Log real GDP per capita in the years 1 to 5 relative to the year 0'), covariate.labels=c('Normal recession', 'Financial recession', 'Normal recession * excess credit', 'Financial recession * excess credit'), keep.stat=c('n','adj.rsq'), add.lines=list(c('Country fixed effects', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'), c('Macrocontrols', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes')), notes=c('Robust standard errors are shown in brackets', 'Number of observations 1831'))
