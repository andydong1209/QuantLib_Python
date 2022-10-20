import QuantLib as ql

# 1.Enviroment
settings = ql.Settings.instance()
evDate = ql.Date(8, 6, 2021)
settings.setEvaluationDate(evDate)

Cal = ql.NullCalendar()
DC365 = ql.Actual365Fixed()
settlementDays = 0
refDate = Cal.advance(evDate, settlementDays, ql.Days, ql.Following, False)
maturity = Cal.advance(evDate, 1, ql.Years, ql.Following, False)

# 2.Market Data
S0 = 100
Q_S = ql.SimpleQuote(S0)
hQ_S = ql.QuoteHandle(Q_S)

r = 0.06
rTS = ql.FlatForward(settlementDays, Cal, r, DC365, ql.Compounded, ql.Annual)
h_rTS = ql.YieldTermStructureHandle(rTS)

q = 0.03
qTS = ql.FlatForward(settlementDays, Cal, q, DC365, ql.Compounded, ql.Annual)
h_qTS = ql.YieldTermStructureHandle(qTS)

vol = 0.3
volTS = ql.BlackConstantVol(evDate, Cal, vol, DC365)
h_volTS = ql.BlackVolTermStructureHandle(volTS)

GBSProcess = ql.GeneralizedBlackScholesProcess(hQ_S, h_qTS, h_rTS, h_volTS)

# 3.Instrument
europeanExer = ql.EuropeanExercise(maturity)

strike = 100.0
optType = ql.Option.Call
vanillaPayoff = ql.PlainVanillaPayoff(optType, strike)
anEuroOption = ql.EuropeanOption(vanillaPayoff, europeanExer)

# 4.Engine
AEE = ql.AnalyticEuropeanEngine(GBSProcess)
anEuroOption.setPricingEngine(AEE)

# 5.MTM
Value = anEuroOption.NPV()
print("MTM: ", Value)

# 6.Greeks
Delta = anEuroOption.delta()
print("Delta: ", Delta)
Gamma = anEuroOption.gamma()
print("Gamma: ", Gamma)
Vega = anEuroOption.vega() 
print("Vega: ", Vega)

Theta = anEuroOption.theta()
print("Theta: ", Theta)
Rho = anEuroOption.rho()
print("Rho: ", Rho)
DividendRho = anEuroOption.dividendRho()
print("Dividend Rho: ", DividendRho)

# 7.Implied Volatility
Price1 = 15.0
vol1 = anEuroOption.impliedVolatility(15.0, GBSProcess)
print("Implied Vol at Price ", Price1,": ", vol1)
Price2 = 10.0
vol2 = anEuroOption.impliedVolatility(10.0, GBSProcess)
print("Implied Vol at Price ", Price2, ": "vol2)