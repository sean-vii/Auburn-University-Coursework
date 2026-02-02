setwd("C:/Users/Sean/Documents/GitHub/STAT-3010/Assignment 1") # Laptop config 

# Load dataset
transducers <- read.csv("Transducers.csv", header = TRUE)

# Identify variables
defective_counts <- transducers$X2  
batches <- nrow(transducers)

# Compute frequencies
freq_table <- table(defective_counts)
relative_freq <- freq_table / sum(freq_table)

# Compute density
class_width <- 1  # B/c defects are counted as whole numbers, class width is just 1
density_values <- relative_freq / class_width

# Compute proportion of batches with 5 or less defects
batches_5 <- sum(defective_counts <= 5)
batch_proportion <- batches_5 / batches

# Print the batch proportion
print(paste("Proportion of batches with ≤ 5 defective transducers:", round(batch_proportion, 2)))

# Histogram 
hist(defective_counts, 
     breaks = seq(min(defective_counts), max(defective_counts), by = class_width), 
     freq = FALSE,
     col = "lightblue", 
     border = "black", 
     xlab = "Defective Transducers", 
     ylab = "Density")

# Include density in the histogram
lines(density(defective_counts, adjust = 1), col = "red", lwd = 2)
