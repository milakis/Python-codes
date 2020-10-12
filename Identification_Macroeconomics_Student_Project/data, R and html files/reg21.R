#necessary packages
require(plm)
require(foreign)
require(stargazer)
require(lmtest)
#data
Rdata = read.dta("data, R and html files/1section1.dta")
#running the regression and then regression with robust standard errors
regr1 <- lm(lrgdpp1~pk_norm+pk_fin+factor(country), data = Rdata)
regr11 = coeftest(regr1, vcov = vcovHC(regr1, type = "HC0"))
regr2 <- lm(lrgdpp2~pk_norm+pk_fin+factor(country), data = Rdata)
regr22 = coeftest(regr2, vcov = vcovHC(regr2, type = "HC0"))
regr3 <- lm(lrgdpp3~pk_norm+pk_fin+factor(country), data = Rdata)
regr33 = coeftest(regr3, vcov = vcovHC(regr3, type = "HC0"))
regr4 <- lm(lrgdpp4~pk_norm+pk_fin+factor(country), data = Rdata)
regr44 = coeftest(regr4, vcov = vcovHC(regr4, type = "HC0"))
regr5 <- lm(lrgdpp5~pk_norm+pk_fin+factor(country), data = Rdata)
regr55 = coeftest(regr5, vcov = vcovHC(regr5, type = "HC0"))
#producing nice table
stargazer(regr11, regr22, regr33, regr44, regr55,  type='text', out='reg21.html', keep=c('pk_norm', 'pk_fin'), digits=1, dep.var.labels=c('Log real GDP per capita in the years 1 to 5 relative to the year 0'), covariate.labels=c('Normal recession', 'Financial recession'), keep.stat=c('n','adj.rsq'), add.lines=list(c('Country fixed effects', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'),c('Macrocontrols included', 'No', 'No', 'No', 'No', 'No')), notes=c('Robust standard errors are shown in brackets', 'Number of observations 1831'))
