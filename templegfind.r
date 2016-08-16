#data import
dataImport = read.csv("/BSEProject/yearly/2010.csv",sep = ",")
dataImport$TIMESTAMP = as.Date(dataImport$TIMESTAMP,"%d-%b-%Y")
companyList = dataImport[order(dataImport$TIMESTAMP),]
companyList_LT = companyList[companyList$SYMBOL=="LT",]
companyList_LT$SYMBOL = as.character(companyList_LT$SYMBOL)
companyList_LT$TIMESTAMP = as.character(companyList_LT$TIMESTAMP)

legDetails = data.frame("stock_id" = 0,"leg_no"=0,"start candle serial number"=0,"start date of leg"=0, 
                        "start price"=0,"end candle serial number"=0,"end date of leg"=0,"end price"=0,
                        "leg height"=0,"leg direction"=0 )
d = data.frame()
legStart=0
legPrice = 0
flag = FALSE
flag2 = "SMALL"
j =1
legNumber = 0
legStartDate = 0
startPrice = 0
endPrice = 0
candleNumber = 0
candlStartNumber = 0
candleEndNumber = 0
legEndDate = 0
legHeight = 0
legDirection = 0
for( i in 1:dim(companyList_LT)[1])
{
  legPrice = companyList_LT$LOW[i]
  candleNumber= candleNumber + 1
  j=j+1
  if(j < dim(companyList_LT)[1]+1 && companyList_LT$LOW[j] > legPrice)
  {
    if(flag == FALSE){
      if(i == 0){
        startPrice = companyList_LT$LOW[i]
      }
      if(flag2=="SMALL" && i != 0){
        legNumber = legNumber+1
        endPrice = companyList_LT$LOW[i]
        candleEndNumber = candleNumber
        legEndDate = companyList_LT$TIMESTAMP[i]
        d = rbind(d,data.frame(as.character(companyList_LT$SYMBOL[i]),as.numeric(legNumber),
                               as.numeric(candleStartNumber),as.character(legStartDate),
                               startPrice,as.numeric(candleEndNumber),as.character(legEndDate),endPrice,0,0))
      }
      legStartDate = companyList_LT$TIMESTAMP[i]
      print(legStartDate)
      startPrice = companyList_LT$LOW[i]
      candleStartNumber = candleNumber
      flag = TRUE
    }  
  }
  else
  {
    if(flag == TRUE)
    {
      legNumber = legNumber + 1
      endPrice = companyList_LT$LOW[i]
      candleEndNumber = candleNumber
      legEndDate = companyList_LT$TIMESTAMP[i]
      d = rbind(d,data.frame(as.character(companyList_LT$SYMBOL[i]),as.numeric(legNumber),
                             as.numeric(candleStartNumber),as.character(legStartDate),
                             startPrice,as.numeric(candleEndNumber),as.character(legEndDate),endPrice,0,0))
      startPrice = endPrice
      legStartDate = legEndDate
      candleStartNumber = candleEndNumber
      flag = FALSE
      flag2 = "SMALL"
    } 
  }
}
colnames(d) = colnames(legDetails)
print(d)