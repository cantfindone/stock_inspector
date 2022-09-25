from finance import finance_indicator

sheet = finance_indicator.get('603501')
print(sheet.head(2).T)