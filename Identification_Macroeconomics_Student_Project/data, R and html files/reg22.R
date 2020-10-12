#necessary packages
require(plm)
require(foreign)
require(stargazer)
require(lmtest)
#data
Rdata = read.dta("data, R and html files/1section1.dta") 
#running the regression with interaction term 
regi1 <- lm(lrgdpp1~pk_norm+pk_fin+pk_norm*excredit+pk_fin*excredit+factor(country), data = Rdata)
regi11 = coeftest(regi1, vcov = vcovHC(regi1, type = "HC0"))
regi2 <- lm(lrgdpp2~pk_norm+pk_fin+pk_norm*excredit+pk_fin*excredit+factor(country), data = Rdata)
regi22 = coeftest(regi2, vcov = vcovHC(regi2, type = "HC0"))
regi3 <- lm(lrgdpp3~pk_norm+pk_fin+pk_norm*excredit+pk_fin*excredit+factor(country), data = Rdata)
regi33 = coeftest(regi3, vcov = vcovHC(regi3, type = "HC0"))
regi4 <- lm(lrgdpp4~pk_norm+pk_fin+pk_norm*excredit+pk_fin*excredit+factor(country), data = Rdata)
regi44 = coeftest(regi4, vcov = vcovHC(regi4, type = "HC0"))
regi5 <- lm(lrgdpp5~pk_norm+pk_fin+pk_norm*excredit+pk_fin*excredit+factor(country), data = Rdata)
regi55 = coeftest(regi5, vcov = vcovHC(regi5, type = "HC0"))
stargazer(regi11, regi22, regi33, regi44, regi55,  type='text', out='reg22.html', keep=c('pk_norm', 'pk_fin', 'pk_norm:excredit', 'pk_fin:excredit'), digits=1, dep.var.labels=c('Log real GDP per capita in the years 1 to 5 relative to the year 0'), covariate.labels=c('Normal recession', 'Financial recession', 'Normal recession * excess credit', 'Financial recession * excess credit'), keep.stat=c('n','adj.rsq'), add.lines=list(c('Country fixed effects', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'), c('Macrocontrols included', 'No', 'No', 'No', 'No', 'No')), notes=c('Robust standard errors are shown in brackets', 'Number of observations 1831'))
