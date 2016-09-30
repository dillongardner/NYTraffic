library(feather)
library(dplyr)
library(tidyr)
library(ggplot2)
library(stlplus)
library(dygraph)
library(lubridate)

##########################################################################
# Read and format
##########################################################################

myData <- read_feather("NYTrafficData.feather")
myData <- myData[!duplicated(myData),]

# Convert Date column from character to date object
myData$Date <-  lubridate::mdy(myData$Date)

# Some dates have multiple entries for each id.
# Looks like this happens with one having cash reported as 0
# We'll just take the highest value for each date
myData <- myData %>% 
  mutate(total_count=`cash-count` + `etc-count`) %>%
  group_by(Date, id) %>%
  arrange(desc(total_count)) %>%
  slice(1L) %>% 
  ungroup()

wideData <- myData %>%
  select(Date, id, total_count) %>%
  spread(id, total_count)

fullDateRange <- data_frame(Date=seq(wideData$Date[1], 
                                     tail(wideData$Date, 1),
                                     by="1 day"))

fullDataWide <- left_join(fullDateRange, wideData, by="Date")
fullDataLong <- gather(fullDataWide, "id", "total_count", -Date)

##########################################################################
# Plot Data
##########################################################################

p <- ggplot(fullDataLong %>% filter(id==1)) + 
  geom_point(aes(x=Date, y=total_count, color=id))
plotly::ggplotly(p)
fullDataLong %>% filter(id=1)

monthlyWide <- fullDataWide
day(monthlyWide$Date) <- 1
monthlyWide <- monthlyWide %>%
  group_by(Date) %>%
  summarise_each(funs(mean(., na.rm=T)))

stlDaily <- stlplus(fullDataWide$`9`,t=fullDataWide$Date,
                    n.p=7, s.window="periodic",
                    sub.labels=c("Sun", "Mon", "Tues",
                                 "Wed", "Thur", "Fri", "Sat"))
stlMonthly <- stlplus(monthlyWide$`9`, t=monthlyWide$Date,
                      n.p=12, s.window="periodic",
                      sub.start=3, sub.labels = month.name)

plot(stlMonthly)
plot_cycle(stlMonthly)
plot(stlDaily)
plot_cycle(stlDaily)
plot_seasonal(stlDaily)
