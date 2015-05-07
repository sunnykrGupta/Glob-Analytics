#install dplyr from cran .. if problem persists update r-base-core to >= v3.1.0
#install ggplot2 from cran package, reshape2 will be installed with ggplot2.
library(dplyr)
library(reshape2)
library(ggplot2)

#Politic Top 15 Countries
# Statistics
pol.df <- read.csv(file="Visualization/csv/top15_politic.csv",head=TRUE,sep=",")
# Melting the data [Wide to long]
pol.df.1 <- melt(pol.df, id.vars = c("country", "score"))

# Visualization of top 15 countries with proportion of pos, neg & ntrl tweets
politic = ggplot(data = pol.df.1, aes(Country - Political , Positivity_Score)) +
  geom_bar(aes(x =  reorder(country, -value), y = value, fill = factor(variable)), stat = "identity") +
  xlab("Country - Political") + 
  ylab("Positivty_Score")


  print(politic)

# Tourism Top 15 Countries 
# Statistics
tour.df <- read.csv(file="Visualization/csv/top15_tourism.csv",head=TRUE,sep=",")
# Melting the data [Wide to long]
tour.df.1 <- melt(tour.df, id.vars = c("country", "score"))

# Visualization of top 15 countries with proportion of pos, neg & ntrl tweets
tourism = ggplot(data = tour.df.1, aes(Country, Positivity_Score)) +
  geom_bar(aes(x =  reorder(country, -value), y = value, fill = factor(variable)), stat = "identity")+
  xlab("Country - Tourism") + 
  ylab("Positivty_Score")
print(tourism)

# Economy Top 15 Countries
# Statistics
eco.df <- read.csv(file="Visualization/csv/top15_economy.csv",head=TRUE,sep=",")
# Melting the data [Wide to long]
eco.df.1 <- melt(eco.df, id.vars = c("country", "score"))
# Visualization of top 15 countries with proportion of pos, neg & ntrl tweets
economy = ggplot(data = eco.df.1, aes(Country, Positivity_Score)) +
  geom_bar(aes(x =  reorder(country, -value), y = value, fill = factor(variable)), stat = "identity")+
  xlab("Country - Economical") + 
  ylab("Positivty_Score")
  print(economy)

# Religion Top 15 Countries
# Statistics
rel.df <- read.csv(file="Visualization/csv/top15_religion.csv",head=TRUE,sep=",")
# Melting the data [Wide to long]
rel.df.1 <- melt(rel.df, id.vars = c("country", "score"))
# Visualization of top 15 countries with proportion of pos, neg & ntrl tweets
religion = ggplot(data = rel.df.1, aes(Country, Positivity_Score)) +
  geom_bar(aes(x =  reorder(country, -value), y = value, fill = factor(variable)), stat = "identity")+
  xlab("Country - Religion") + 
  ylab("Positivty_Score")

  print(religion)