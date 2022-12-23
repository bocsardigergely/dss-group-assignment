library(tidyverse)
library(ggpubr)
library(rstatix)
library(lme4)
library(stargazer)
library(lmerTest)
library(modelsummary)

setwd('/Users/gbocsardi/Documents/JADS_semester_3/DSS/Assignment Group')
data <- read.csv('participant data/form_data.csv')

# T test
##### 
diverse_sat <- data %>% 
  filter(is_diverse == "True") %>% 
  pull(satisfaction)

non_sat <- data %>%  
  filter(is_diverse == "False") %>% 
  pull(satisfaction)

stat_test <- data %>% 
  t_test(satisfaction ~ is_diverse, var.equal = TRUE) %>% 
  add_significance()
print(stat_test)


# Create a box-plot
bxp <- ggboxplot(
  data, x = "is_diverse", y = "satisfaction", 
  ylab = "satisfaction", xlab = "diversity", add = "jitter"
)

# Add p-value and significance levels
stat_test <- stat_test %>% add_xy_position(x = "is_diverse")
bxp + 
  stat_pvalue_manual(stat_test, tip.length = 0) +
  labs(subtitle = get_test_label(stat_test, detailed = TRUE))

#####

# Multi regression
#####

data$is_diverse <- as.factor(data$is_diverse)
data$user_id <- as.factor(data$user_id)

model_1 <- lmer(satisfaction ~ diversity + active_eng + emotions + matched_taste + novelty + is_diverse + active_eng*is_diverse + emotions*is_diverse  + (1|user_id), data = data)
summary(model_1)


mean <- ls_means(model_1, level = 0.9)
plot(mean)

res <- as.data.frame(coef(summary(model_1)))



stargazer(select(res, -"t value") , summary = FALSE)

gof <- get_gof(model_1)
stargazer(gof, summary=FALSE)

# correlation map
#####

cormat <- round(cor(data[c('diversity', 'active_eng', 'emotions', 'matched_taste', 'novelty', 'satisfaction')]),2)
library(reshape2)
melted_cormat <- melt(cormat)
library(ggplot2)
ggplot(data = melted_cormat, aes(x=Var1, y=Var2, fill=value)) + 
  geom_tile()

library("PerformanceAnalytics")
my_data <- data[c('diversity', 'active_eng', 'emotions', 'matched_taste', 'novelty', 'satisfaction')]
chart.Correlation(my_data, histogram=TRUE, pch=19)


