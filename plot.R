library(tidyverse)
library(here)

all_longs <- read_csv(here("all_longs.csv"))

p <- ggplot(all_longs, aes(x = iter, y = value, col = variable)) +
  geom_point(alpha = .005, size = .1) +
  geom_smooth() +
  theme_classic() +
  labs(x = "Iteration",
       y = "Cumulative proportion",
       col = "Equivalence class") +
  coord_cartesian(ylim = c(0, 0.25))

ggsave("cum_plot.png", p, device = "png", 
       width = 12, height = 8, units = "cm")