library(tidyverse)
library(here)
library(Metrics)

theme_set(theme_classic())

###### Simulation 1 ######

all_longs <- read_csv(here("all_longs.csv"))

cum_plot <- ggplot(all_longs, aes(x = iter, y = value, col = variable)) +
  geom_point(alpha = .005, size = .1) +
  geom_smooth() +
  labs(x = "Iteration",
       y = "Cumulative proportion",
       col = "Equivalence class") +
  coord_cartesian(ylim = c(0, 0.25))

ggsave(here("plots", "cum_plot.png"), cum_plot, device = "png", 
       width = 12, height = 8, units = "cm")

###### Simulation 2 ######

sim_metrics_3 <- read_csv(here("sim_metrics_3.csv"))

rmse_hist <- ggplot(sim_metrics_3, aes(x = rmse)) +
  geom_histogram() +
  labs(x = "RMSE",
       y = "Number of simulations")

ggsave(here("plots", "rmse_hist.png"), rmse_hist, device = "png", 
       width = 12, height = 8, units = "cm")

entropy <- ggplot(sim_metrics_3, aes(x = value, y = estimated)) +
  geom_point() +
  geom_smooth(method = "lm") +
  geom_abline(slope = 1, intercept = 0,
              col = "grey", lty = "dashed") +
  theme_classic() +
  labs(x = "Observed entropy",
       y = "Predicted entropy")

ggsave(here("plots", "entropy.png"), entropy, device = "png", 
       width = 12, height = 8, units = "cm")

sym_3 <- ggplot(sim_metrics_3, aes(x = value, y = symmetry)) +
  geom_point() +
  geom_smooth(method = "lm", formula = "y ~ exp(x)") +
  labs(x = "Observed entropy",
       y = "Transition matrix symmetry")

ggsave(here("plots", "sym_3.png"), sym_3, device = "png", 
       width = 12, height = 8, units = "cm")

###### Simulation 3 ######

sim_metrics_5 <- read_csv(here("sim_metrics_5.csv"))

sym_5 <- ggplot(sim_metrics_5, aes(x = value, y = symmetry)) +
  geom_point() +
  geom_smooth(method = "lm", formula = "y ~ exp(x)") +
  labs(x = "Observed entropy",
       y = "Transition matrix symmetry")

ggsave(here("plots", "sym_5.png"), sym_5, device = "png", 
       width = 12, height = 8, units = "cm")
