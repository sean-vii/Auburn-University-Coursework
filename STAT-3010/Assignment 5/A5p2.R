setwd("C:/Users/Sean/Documents/GitHub/STAT-3010/Assignment 5") # Laptop config 

## ---- (a) Read the CSV file ---------------------------------------------
humidity <- read.csv("hw5q2.csv", stringsAsFactors = TRUE)

# Side-by-side box-plot of humidity by season
boxplot(Humidity ~ Season, data = humidity,
        main = "Relative Humidity by Season",
        ylab = "Relative humidity (%)",
        xlab = "Season")

## ---- (b) Normal Q-Q plots ----------------------------------------------
# Put two plots in one row for easy comparison
par(mfrow = c(1, 2))

# Summer
qqnorm(subset(humidity, Season == "Summer")$Humidity,
       main = "Q-Q Plot – Summer")
qqline(subset(humidity, Season == "Summer")$Humidity)

# Winter
qqnorm(subset(humidity, Season == "Winter")$Humidity,
       main = "Q-Q Plot – Winter")
qqline(subset(humidity, Season == "Winter")$Humidity)

# return to default one-plot layout
par(mfrow = c(1, 1))

## ---- (c) Variances and IQRs --------------------------------------------
var_by_season <- tapply(humidity$Humidity, humidity$Season, var)
iqr_by_season <- tapply(humidity$Humidity, humidity$Season, IQR)

cat("\nVariance by season (%²):\n")
print(var_by_season)

cat("\nInter-quartile range by season (%):\n")
print(iqr_by_season)
