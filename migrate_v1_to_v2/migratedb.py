import subprocess

def migrate_account_balances():

    queries = """

.bail on
PRAGMA busy_timeout = 5000;

ATTACH DATABASE '/var/lib/quantrocket/quantrocket.account.balance.sqlite' AS v1;

.print 'Copying LatestBalance'

INSERT OR IGNORE INTO LatestBalance (
    Account,
    AccountType,
    AccruedCash,
    AvailableFunds,
    Broker,
    BuyingPower,
    Currency,
    Cushion,
    DayTradesRemaining,
    EquityWithLoanValue,
    ExcessLiquidity,
    FullAvailableFunds,
    FullExcessLiquidity,
    FullInitMarginReq,
    FullMaintMarginReq,
    GrossPositionValue,
    HighestSeverity,
    InitMarginReq,
    LastUpdated,
    Leverage,
    LookAheadAvailableFunds,
    LookAheadExcessLiquidity,
    LookAheadInitMarginReq,
    LookAheadMaintMarginReq,
    LookAheadNextChange,
    MaintMarginReq,
    NetLiquidation,
    Paper,
    PreviousEquityWithLoanValue,
    RegTEquity,
    RegTMargin,
    SMA,
    SettledCash,
    TotalCashValue
)
SELECT 
    Account,
    AccountType,
    AccruedCash,
    AvailableFunds,
    'ibkr' AS Broker,
    BuyingPower,
    Currency,
    Cushion,
    DayTradesRemaining,
    EquityWithLoanValue,
    ExcessLiquidity,
    FullAvailableFunds,
    FullExcessLiquidity,
    FullInitMarginReq,
    FullMaintMarginReq,
    GrossPositionValue,
    HighestSeverity,
    InitMarginReq,
    DatetimeCreated AS LastUpdated,
    Leverage,
    LookAheadAvailableFunds,
    LookAheadExcessLiquidity,
    LookAheadInitMarginReq,
    LookAheadMaintMarginReq,
    LookAheadNextChange,
    MaintMarginReq,
    NetLiquidation,
    SUBSTR(Account,1,1) = 'D' AS Paper,
    PreviousEquityWithLoanValue,
    RegTEquity,
    RegTMargin,
    SMA,
    SettledCash,
    TotalCashValue
FROM v1.LatestBalance;

.print 'Copying Balance'

INSERT OR IGNORE INTO Balance (
    Account,
    AccountType,
    AccruedCash,
    AvailableFunds,
    Broker,
    BuyingPower,
    Currency,
    Cushion,
    Date,
    DayTradesRemaining,
    EquityWithLoanValue,
    ExcessLiquidity,
    FullAvailableFunds,
    FullExcessLiquidity,
    FullInitMarginReq,
    FullMaintMarginReq,
    GrossPositionValue,
    HighestSeverity,
    InitMarginReq,
    LastUpdated,
    Leverage,
    LookAheadAvailableFunds,
    LookAheadExcessLiquidity,
    LookAheadInitMarginReq,
    LookAheadMaintMarginReq,
    LookAheadNextChange,
    MaintMarginReq,
    NetLiquidation,
    Paper,
    PreviousEquityWithLoanValue,
    RegTEquity,
    RegTMargin,
    SMA,
    SettledCash,
    TotalCashValue
)
SELECT 
    Account,
    AccountType,
    AccruedCash,
    AvailableFunds,
    'ibkr' AS Broker,
    BuyingPower,
    Currency,
    Cushion,
    Date,
    DayTradesRemaining,
    EquityWithLoanValue,
    ExcessLiquidity,
    FullAvailableFunds,
    FullExcessLiquidity,
    FullInitMarginReq,
    FullMaintMarginReq,
    GrossPositionValue,
    HighestSeverity,
    InitMarginReq,
    DatetimeCreated AS LastUpdated,
    Leverage,
    LookAheadAvailableFunds,
    LookAheadExcessLiquidity,
    LookAheadInitMarginReq,
    LookAheadMaintMarginReq,
    LookAheadNextChange,
    MaintMarginReq,
    NetLiquidation,
    SUBSTR(Account,1,1) = 'D' AS Paper,
    PreviousEquityWithLoanValue,
    RegTEquity,
    RegTMargin,
    SMA,
    SettledCash,
    TotalCashValue
FROM v1.Balance;
"""

    subprocess.check_output(
        ["sqlite3", "/var/lib/quantrocket/quantrocket.v2.account.balance.sqlite"],
        input=bytes(queries.encode("utf-8")))
    
    print("copied v1 account balances to v2")

def migrate_master():

    queries = """

.bail on
PRAGMA busy_timeout = 5000;

ATTACH DATABASE '/var/lib/quantrocket/quantrocket.master.main.sqlite' AS v1;

.print 'Copying into _SecurityIBKR'

INSERT OR IGNORE INTO _SecurityIBKR (
    AggGroup,
    BondType,
    Callable,
    Category,
    ComboLegs,
    ConId,
    ContractMonth,
    Convertible,
    Coupon,
    CouponType,
    Currency,
    DescAppend,
    EvMultiplier,
    EvRule,
    Industry,
    Isin,
    IssueDate,
    LastTradeDate,
    LocalSymbol,
    LongName,
    MarketName,
    MarketRuleIds,
    Maturity,
    MdSizeMultiplier,
    MinTick,
    Multiplier,
    PriceMagnifier,
    PrimaryExchange,
    Putable,
    Ratings,
    RealExpirationDate,
    Right,
    SecType,
    Sector,
    Strike,
    Symbol,
    TimeZoneId,
    Timezone,
    TradingClass,
    UnderConId,
    UnderSecType,
    UnderSymbol,
    ValidExchanges
)
SELECT 
    AggGroup,
    BondType,
    Callable,
    Category,
    ComboLegs,
    ConId,
    ContractMonth,
    Convertible,
    Coupon,
    CouponType,
    Currency,
    DescAppend,
    EvMultiplier,
    EvRule,
    Industry,
    SUBSTR(Cusip,6) AS ISIN,
    IssueDate,
    LastTradeDate,
    LocalSymbol,
    LongName,
    MarketName,
    MarketRuleIds,
    Maturity,
    MdSizeMultiplier,
    MinTick,
    Multiplier,
    PriceMagnifier,
    PrimaryExchange,
    Putable,
    Ratings,
    RealExpirationDate,
    Right,
    SecType,
    Sector,
    Strike,
    Symbol,
    TimeZoneId,
    Timezone,
    TradingClass,
    UnderConId,
    UnderSecType,
    UnderSymbol,
    ValidExchanges
FROM v1.Security
ORDER BY DatetimeCreated ASC;

.print 'Copying into IBKRTradingHours'

INSERT OR IGNORE INTO IBKRTradingHours (
    Datetime,
    Exchange,
    Open,
    Rth,
    SecType
)
SELECT 
    Datetime,
    Exchange,
    Open,
    Rth,
    SecType
FROM v1.TradingHours;

.print 'Copying into IBKRPriceIncrementRule'

INSERT OR IGNORE INTO IBKRPriceIncrementRule (
    MarketRuleId,
    MarketRulesJson
)
SELECT 
    MarketRuleId,
    MarketRulesJson
FROM v1.PriceIncrementRule;

.print 'Copying into _IBKRSecurityPriceIncrementRule'

INSERT OR IGNORE INTO _IBKRSecurityPriceIncrementRule (
    ConId,
    Exchange,
    MarketRuleId
)
SELECT 
    ConId,
    Exchange,
    MarketRuleId
FROM v1.SecurityPriceIncrementRule;

.print 'Copying into _IBKRDelisted'

INSERT OR IGNORE INTO _IBKRDelisted (
    ConId,
    DateDelisted,
    DatetimeCreated
)
SELECT 
    ConId,
    DateDelisted,
    DatetimeCreated
FROM v1.Delisted;

.print 'Copying into _IBKREtf'

INSERT OR IGNORE INTO _IBKREtf (
    ConId,
    DatetimeCreated
)
SELECT 
    ConId,
    DatetimeCreated
FROM v1.Etf;

.print 'Copying into SecurityIBKR'

INSERT OR IGNORE INTO SecurityIBKR (
    Sid,
    ConId,
    Symbol,
    SecType,
    Etf,
    PrimaryExchange,
    Currency,
    Mic,
    LocalSymbol,
    TradingClass,
    MarketName,
    LongName,
    TimeZoneId,
    Timezone,
    ValidExchanges,
    AggGroup,
    Sector,
    Industry,
    Category,
    MinTick,
    PriceMagnifier,
    MdSizeMultiplier,
    LastTradeDate,
    ContractMonth,
    RealExpirationDate,
    Multiplier,
    UnderConId,
    UnderSymbol,
    UnderSecType,
    MarketRuleIds,
    Strike,
    Right,
    Isin,
    Cusip,
    Ratings,
    DescAppend,
    BondType,
    CouponType,
    Callable,
    Putable,
    Coupon,
    Convertible,
    Maturity,
    IssueDate,
    EvRule,
    EvMultiplier,
    Delisted,
    DateDelisted
)
SELECT
    CASE SecType
        WHEN 'BAG' THEN 'IC' || SUBSTR(CAST(s.ConId AS CHAR),4) 
        ELSE COALESCE(i.Sid, 'IB' || CAST(s.ConId AS CHAR))
    END AS Sid,
    s.ConId,
    Symbol,
    SecType,
    e.ConId IS NOT NULL AS Etf,
    s.PrimaryExchange,
    Currency,
    m.Mic,
    NULLIF(LocalSymbol, ''),
    NULLIF(TradingClass, ''),
    NULLIF(MarketName, ''),
    NULLIF(LongName, ''),
    NULLIF(TimeZoneId, ''),
    NULLIF(Timezone, ''),
    NULLIF(ValidExchanges, ''),
    NULLIF(AggGroup, ''),
    NULLIF(Sector, ''),
    NULLIF(Industry, ''),
    NULLIF(Category, ''),
    NULLIF(MinTick, ''),
    NULLIF(PriceMagnifier, ''),
    NULLIF(MdSizeMultiplier, ''),
    NULLIF(LastTradeDate, ''),
    NULLIF(ContractMonth, ''),
    NULLIF(RealExpirationDate, ''),
    NULLIF(Multiplier, ''),
    NULLIF(UnderConId, ''),
    NULLIF(UnderSymbol, ''),
    NULLIF(UnderSecType, ''),
    NULLIF(MarketRuleIds, ''),
    NULLIF(Strike, ''),
    NULLIF(Right, ''),
    NULLIF(Isin, ''),
    NULLIF(Cusip, ''),
    NULLIF(Ratings, ''),
    NULLIF(DescAppend, ''),
    NULLIF(BondType, ''),
    NULLIF(CouponType, ''),
    NULLIF(Callable, ''),
    NULLIF(Putable, ''),
    NULLIF(Coupon, ''),
    NULLIF(Convertible, ''),
    NULLIF(Maturity, ''),
    NULLIF(IssueDate, ''),
    NULLIF(EvRule, ''),
    NULLIF(EvMultiplier, ''),
    d.DateDelisted IS NOT NULL AS Delisted,
    d.DateDelisted AS DateDelisted
FROM _SecurityIBKR s
LEFT JOIN _IBKRSid i
    ON i.ConId = s.ConId
LEFT JOIN _IBKREtf e
    ON e.ConId = s.ConId
LEFT JOIN _IBKRDelisted d
    ON d.ConId = i.ConId
LEFT JOIN _IBKRMic m
    ON m.PrimaryExchange = s.PrimaryExchange
ORDER BY s.ROWID DESC;

.print 'Copying into SecuritySid'

INSERT OR IGNORE INTO SecuritySid (
    Sid
)
SELECT
    CASE SecType
        WHEN 'BAG' THEN 'IC' || SUBSTR(CAST(s.ConId AS CHAR),4) 
        ELSE COALESCE(i.Sid, 'IB' || CAST(s.ConId AS CHAR))
    END AS Sid
FROM _SecurityIBKR s
LEFT JOIN _IBKRSid i
    ON i.ConId = s.ConId;
  
.print 'Copying into Universe'

INSERT OR IGNORE INTO Universe (
    Code,
    Sid,
    DatetimeCreated
)
SELECT 
    u.Code,
    COALESCE(s.Sid, i.Sid),
    u.DatetimeCreated
FROM v1.Universe u
LEFT JOIN Security s
    ON s.ibkr_ConId = u.ConId
LEFT JOIN _IBKRSid i
    ON i.ConId = u.ConId
WHERE COALESCE(s.ibkr_ConId, i.ConId) IS NOT NULL;

"""

    subprocess.check_output(
        ["sqlite3", "/var/lib/quantrocket/quantrocket.v2.master.main.sqlite"],
        input=bytes(queries.encode("utf-8")))
    
    print("copied v1 master to v2")

def migrate_orders():

    queries = """

.bail on
PRAGMA busy_timeout = 5000;

ATTACH DATABASE '/var/lib/quantrocket/quantrocket.blotter.orders.sqlite' AS v1;
ATTACH DATABASE '/var/lib/quantrocket/quantrocket.v2.master.main.sqlite' AS master;

.print 'Copying into Orders'

INSERT OR IGNORE INTO Orders (
    Account,
    Action,
    AdjustableTrailingUnit,
    AdjustedStopLimitPrice,
    AdjustedStopPrice,
    AdjustedTrailingAmount,
    AlgoId,
    AlgoStrategy,
    AllOrNone,
    AuxPrice,
    BlockOrder,
    Broker,
    ClientId,
    ConId,
    DiscretionaryAmt,
    DisplaySize,
    Exchange,
    FaGroup,
    FaMethod,
    FaPercentage,
    FaProfile,
    GoodAfterTime,
    GoodTillDate,
    Hidden,
    LmtPrice,
    LmtPriceOffset,
    MinQty,
    NotHeld,
    OcaGroup,
    OcaType,
    OpenClose,
    OrderDetailsJson,
    OrderId,
    OrderNum,
    OrderRef,
    OrderType,
    Origin,
    OutsideRth,
    ParentId,
    PercentOffset,
    PermId,
    Sid,
    Submitted,
    SweepToFill,
    Tif,
    TotalQuantity,
    TrailStopPrice,
    TrailingPercent,
    Transmit,
    TriggerMethod,
    TriggerPrice,
    WhatIf
)
SELECT 
    t.Account,
    t.Action,
    t.AdjustableTrailingUnit,
    t.AdjustedStopLimitPrice,
    t.AdjustedStopPrice,
    t.AdjustedTrailingAmount,
    t.AlgoId,
    t.AlgoStrategy,
    t.AllOrNone,
    t.AuxPrice,
    t.BlockOrder,
    'ibkr' AS Broker,
    t.ClientId,
    t.ConId,
    t.DiscretionaryAmt,
    t.DisplaySize,
    t.Exchange,
    t.FaGroup,
    t.FaMethod,
    t.FaPercentage,
    t.FaProfile,
    t.GoodAfterTime,
    t.GoodTillDate,
    t.Hidden,
    t.LmtPrice,
    t.LmtPriceOffset,
    t.MinQty,
    t.NotHeld,
    t.OcaGroup,
    t.OcaType,
    t.OpenClose,
    t.OrderDetailsJson,
    t.Id AS OrderId,
    t.OrderNum,
    t.OrderRef,
    t.OrderType,
    t.Origin,
    t.OutsideRth,
    t.ParentId,
    t.PercentOffset,
    t.PermId,
    COALESCE(s.Sid, i.Sid),
    t.DatetimeCreated AS Submitted,
    t.SweepToFill,
    t.Tif,
    t.TotalQuantity,
    t.TrailStopPrice,
    t.TrailingPercent,
    t.Transmit,
    t.TriggerMethod,
    t.TriggerPrice,
    t.WhatIf
FROM v1.Orders t
LEFT JOIN master.Security s
    ON s.ibkr_ConId = t.ConId
LEFT JOIN master._IBKRSid i
    ON i.ConId = t.ConId
WHERE COALESCE(s.ibkr_ConId, i.ConId) IS NOT NULL;
"""

    subprocess.check_output(
        ["sqlite3", "/var/lib/quantrocket/quantrocket.v2.blotter.orders.sqlite"],
        input=bytes(queries.encode("utf-8")))
    
    print("copied v1 orders to v2")

def migrate_order_errors():

    queries = """

.bail on
PRAGMA busy_timeout = 5000;

ATTACH DATABASE '/var/lib/quantrocket/quantrocket.blotter.errors.sqlite' AS v1;

.print 'Copying into OrderError'

INSERT OR IGNORE INTO OrderError (
    DatetimeCreated,
    ErrorCode,
    ErrorMsg,
    OrderId
)
SELECT 
    DatetimeCreated,
    ErrorCode,
    ErrorMsg,
    OrderId
FROM v1.OrderError;
"""

    subprocess.check_output(
        ["sqlite3", "/var/lib/quantrocket/quantrocket.v2.blotter.errors.sqlite"],
        input=bytes(queries.encode("utf-8")))
    
    print("copied v1 order errors to v2")
    

def migrate_executions():

    queries = """

.bail on
PRAGMA busy_timeout = 5000;

ATTACH DATABASE '/var/lib/quantrocket/quantrocket.blotter.executions.sqlite' AS v1;
ATTACH DATABASE '/var/lib/quantrocket/quantrocket.v2.master.main.sqlite' AS master;

.print 'Copying into Execution'

INSERT OR IGNORE INTO Execution (
    Account,
    AvgPrice,
    ClientId,
    ComboType,
    Commission,
    ConId,
    CumQty,
    Currency,
    DatetimeCreated,
    EvMultiplier,
    EvRule,
    Exchange,
    ExecId,
    LastLiquidity,
    Liquidation,
    ModelCode,
    OrderId,
    OrderNum,
    OrderRef,
    PermId,
    Price,
    Quantity,
    RealizedPnl,
    Sid,
    Side,
    Time,
    Yield,
    YieldRedemptionDate
)
SELECT 
    t.Account,
    t.AvgPrice,
    t.ClientId,
    t.ComboType,
    t.Commission,
    t.ConId,
    t.CumQty,
    t.Currency,
    t.DatetimeCreated,
    t.EvMultiplier,
    t.EvRule,
    t.Exchange,
    t.ExecId,
    t.LastLiquidity,
    t.Liquidation,
    t.ModelCode,
    t.OrderId,
    t.OrderNum,
    t.OrderRef,
    t.PermId,
    t.Price,
    t.Quantity,
    t.RealizedPnl,
    COALESCE(s.Sid, i.Sid),
    t.Side,
    t.Time,
    t.Yield,
    t.YieldRedemptionDate
FROM v1.Execution t
LEFT JOIN master.Security s
    ON s.ibkr_ConId = t.ConId
LEFT JOIN master._IBKRSid i
    ON i.ConId = t.ConId
WHERE COALESCE(s.ibkr_ConId, i.ConId) IS NOT NULL;

.print 'Copying into BrokerLatestPosition'

INSERT OR IGNORE INTO BrokerLatestPosition (
    Account,
    AvgCost,
    DatetimeCreated,
    Quantity,
    Sid
)
SELECT 
    t.Account,
    t.AvgCost,
    t.DatetimeCreated,
    t.Quantity,
    COALESCE(s.Sid, i.Sid)
FROM v1.BrokerLatestPosition t
LEFT JOIN master.Security s
    ON s.ibkr_ConId = t.ConId
LEFT JOIN master._IBKRSid i
    ON i.ConId = t.ConId
WHERE COALESCE(s.ibkr_ConId, i.ConId) IS NOT NULL;

.print 'Copying into LatestPosition'

INSERT OR IGNORE INTO LatestPosition (
    Account,
    DatetimeCreated,
    Id,
    OrderRef,
    Quantity,
    Sid
)
SELECT 
    t.Account,
    t.DatetimeCreated,
    REPLACE(t.Id, t.ConId, COALESCE(s.Sid, i.Sid)),
    t.OrderRef,
    t.Quantity,
    COALESCE(s.Sid, i.Sid)
FROM v1.LatestPosition t
LEFT JOIN master.Security s
    ON s.ibkr_ConId = t.ConId
LEFT JOIN master._IBKRSid i
    ON i.ConId = t.ConId
WHERE COALESCE(s.ibkr_ConId, i.ConId) IS NOT NULL;
"""

    subprocess.check_output(
        ["sqlite3", "/var/lib/quantrocket/quantrocket.v2.blotter.executions.sqlite"],
        input=bytes(queries.encode("utf-8")))
        
    print("copied v1 executions and positions to v2")

def migrate_order_statuses():

    queries = """

.bail on
PRAGMA busy_timeout = 5000;

ATTACH DATABASE '/var/lib/quantrocket/quantrocket.blotter.statuses.sqlite' AS v1;

.print 'Copying into OrderStatus'

INSERT OR IGNORE INTO OrderStatus (
    AvgFillPrice,
    Broker,
    ClientId,
    DatetimeCreated,
    Filled,
    LastFillPrice,
    MktCapPrice,
    OrderId,
    OrderNum,
    ParentId,
    PermId,
    Remaining,
    Status,
    WhyHeld
)
SELECT 
    AvgFillPrice,
    'ibkr' AS Broker,
    ClientId,
    DatetimeCreated,
    Filled,
    LastFillPrice,
    MktCapPrice,
    OrderId,
    OrderNum,
    ParentId,
    PermId,
    Remaining,
    Status,
    WhyHeld
FROM v1.OrderStatus;
"""

    subprocess.check_output(
        ["sqlite3", "/var/lib/quantrocket/quantrocket.v2.blotter.statuses.sqlite"],
        input=bytes(queries.encode("utf-8")))
    
    print("copied v1 order statuses to v2")
    
def migrate_blotter():
    
    migrate_orders()
    migrate_order_errors()
    migrate_order_statuses()
    migrate_executions()

def migrate_reuters_estimates():

    queries = """

.bail on
PRAGMA busy_timeout = 5000;

ATTACH DATABASE '/var/lib/quantrocket/quantrocket.fundamental.reuters.estimates.sqlite' AS v1;
ATTACH DATABASE '/var/lib/quantrocket/quantrocket.v2.master.main.sqlite' AS master;

.print 'Copying into Estimate'

INSERT OR IGNORE INTO Estimate (
    Actual,
    AnnounceDate,
    DatetimeCreated,
    FiscalPeriodEndDate,
    FiscalPeriodNumber,
    FiscalPeriodType,
    FiscalYear,
    High,
    Indicator,
    Low,
    Mean,
    Median,
    NumOfEst,
    Sid,
    StdDev,
    Unit,
    UpdatedDate
)
SELECT 
    t.Actual,
    t.AnnounceDate,
    t.DatetimeCreated,
    t.FiscalPeriodEndDate,
    t.FiscalPeriodNumber,
    t.FiscalPeriodType,
    t.FiscalYear,
    t.High,
    t.Indicator,
    t.Low,
    t.Mean,
    t.Median,
    t.NumOfEst,
    COALESCE(s.Sid, i.Sid),
    t.StdDev,
    t.Unit,
    t.UpdatedDate
FROM v1.Estimate t
LEFT JOIN master.Security s
    ON s.ibkr_ConId = t.ConId
LEFT JOIN master._IBKRSid i
    ON i.ConId = t.ConId
WHERE COALESCE(s.ibkr_ConId, i.ConId) IS NOT NULL;

.print 'Copying into Indicator'

INSERT OR IGNORE INTO Indicator (
    Code,
    DatetimeCreated,
    Description
)
SELECT 
    Code,
    DatetimeCreated,
    Description
FROM v1.Indicator;
"""

    subprocess.check_output(
        ["sqlite3", "/var/lib/quantrocket/quantrocket.v2.fundamental.reuters.estimates.sqlite"],
        input=bytes(queries.encode("utf-8")))
        
    print("copied v1 Reuters estimates to v2")
    
def migrate_wsh_calendar():

    queries = """

.bail on
PRAGMA busy_timeout = 5000;

ATTACH DATABASE '/var/lib/quantrocket/quantrocket.fundamental.wsh.calendar.sqlite' AS v1;
ATTACH DATABASE '/var/lib/quantrocket/quantrocket.v2.master.main.sqlite' AS master;

.print 'Copying into Calendar'

INSERT OR IGNORE INTO Calendar (
    Date,
    DatetimeCreated,
    LastUpdated,
    Period,
    Sid,
    Status,
    Time,
    Timezone
)
SELECT 
    t.Date,
    t.DatetimeCreated,
    t.LastUpdated,
    t.Period,
    COALESCE(s.Sid, i.Sid),
    t.Status,
    t.Time,
    t.Timezone
FROM v1.Calendar t
LEFT JOIN master.Security s
    ON s.ibkr_ConId = t.ConId
LEFT JOIN master._IBKRSid i
    ON i.ConId = t.ConId
WHERE COALESCE(s.ibkr_ConId, i.ConId) IS NOT NULL;
"""

    subprocess.check_output(
        ["sqlite3", "/var/lib/quantrocket/quantrocket.v2.fundamental.wsh.calendar.sqlite"],
        input=bytes(queries.encode("utf-8")))
    
    print("copied v1 WSH calendar to v2")
    