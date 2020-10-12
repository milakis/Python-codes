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
#producing nice table
stargazer(regout, regemp, regcpi, regpop, regols, type='text', out='reg31.html', keep='Drcapspend', digits="2", dep.var.labels=c('Output', 'Employment', 'CPI', 'Population', 'OLS Output'), covariate.labels='Prime military contracts', keep.stat=c('n','adj.rsq'), add.lines=list(c('Year and state fixed effects', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes')))
