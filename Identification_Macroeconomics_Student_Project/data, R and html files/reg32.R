#necessary packages
require(plm)
require(foreign)
require(stargazer)
require(lmtest)
#data
Rdata = read.dta("data, R and html files/2section2.dta")
#OLS regression
regols = plm(Drcapout~Drcapspend+factor(state)+factor(year), data = Rdata, model = "within")
#Dependent variable - output
regout = plm(Drcapout~Drcapspend+factor(state)+factor(year) | . - Drcapspend + factor(state)*Drcapspend_nat, data = Rdata, model = "within")
#Dependent variable - employment
regemp = plm(Demp~Drcapspend+factor(state)+factor(year) | . - Drcapspend + factor(state)*Drcapspend_nat, data = Rdata, model = "within")
#Dependent variable - CPI
regcpi = plm(Dcpi_ACCRA~Drcapspend+factor(state)+factor(year) | . - Drcapspend + factor(state)*Drcapspend_nat, data = Rdata, model = "within")
#Dependent variable - population
regpop = plm(Dpop~Drcapspend+factor(state)+factor(year) | . - Drcapspend + factor(state)*Drcapspend_nat, data = Rdata, model = "within")
#regressions with clustered standard errors
regout_cl = coeftest(regout, vcov=vcovHC(regout, type="sss", cluster="group"))
regemp_cl = coeftest(regemp, vcov=vcovHC(regemp, type="sss", cluster="group"))
regcpi_cl = coeftest(regcpi, vcov=vcovHC(regcpi, type="sss", cluster="group"))
regpop_cl = coeftest(regpop, vcov=vcovHC(regpop, type="sss", cluster="group"))
#producing nice table
stargazer(regout_cl, regemp_cl, regcpi_cl, regpop_cl, type='text', out='reg32.html', keep='Drcapspend', digits="2", covariate.labels='Prime military contracts', keep.stat='n', add.lines=list(c('Year and state fixed effects', 'Yes', 'Yes', 'Yes', 'Yes'), c('Clustered standard errors', 'Yes', 'Yes', 'Yes', 'Yes')))
