library(ggplot2)
library(dplyr)
library(reshape2)

# change these to run on other files
csv_1 <- 'measurement_final.csv'

raw_data1 <- read.csv(csv_1)

combined_data <- rbind(raw_data1)

# add site field by finding text between www. and .com
combined_data$site <- substr(combined_data$link, regexpr('www.', combined_data$link) + 4, regexpr('.com', combined_data$link) - 1)

# melt data
melted_data <- melt(combined_data)

# plot total load times by site (AMP vs not)
load_time_data <- filter(melted_data, variable %in% c('amp_total', 'non_amp_total'))
ggplot(load_time_data, aes(value)) + 
  stat_ecdf(aes(group = variable, color = variable), geom = "line") + 
  facet_wrap(~site) +
  scale_x_continuous(limits = c(0, 45000)) +
  labs(x = 'Load Time (ms)', y = 'Percent')

ggsave("load_time.png", height = 15, width = 20)

# plot time to first byte by site (AMP vs not)
