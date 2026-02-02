setwd("C:/Users/Sean/Documents/GitHub/STAT-3010/Assignment 5") # Laptop config 

## ---- (A) Create the data frame ------------------------------------------
Location <- c("A", "A", "A", "B", "B", "B", "C")
Height   <- c(100, 200, 300, 450, 600, 800, 1000)
Distance <- c(253, 337, 395, 451, 495, 534, 573)

Galileo <- data.frame(Location, Height, Distance)

print(Galileo)

## ---- (B) Summary statistics for Distance --------------------------------
cat("\nSummary statistics for Distance:\n")
cat("  Mean      :", mean(Galileo$Distance), "\n")
cat("  Median    :", median(Galileo$Distance), "\n")
cat("  Variance  :", var(Galileo$Distance), "\n")
cat("  IQR       :", IQR(Galileo$Distance), "\n")

## ---- (C) Add fitted values and logical indicator ------------------------
Galileo$D.Hat <- 200 + 0.708*Galileo$Height - 0.000344*Galileo$Height^2
Galileo$LO <- Galileo$D.Hat < Galileo$Distance

Galileo_sub <- subset(Galileo, !LO) # keep only rows where estimate is NOT lower than measurement
cat("\nRows where estimate ≥ measurement:\n")
print(Galileo_sub)

## ---- (D) Scatter-plot with theoretical curve (base graphics) ------------
plot(Height, Distance,
     pch = 19, cex = 1.2,
     xlab = "Height (cm)",
     ylab = "Measured distance (cm)",
     main = "Galileo experiment: Distance vs. Height")

curve(200 + 0.708*x - 0.000344*x^2,
      from = min(Height), to = max(Height),
      add  = TRUE, lty = 2, lwd = 2)
