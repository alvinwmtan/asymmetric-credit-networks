library(tidyverse)
library(here)
library(Metrics)

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

final_distribs <- read_csv(here("final_distribs.csv"))

# rmse <- final_distribs |> 
#   group_by(sim) |> 
#   summarise(rmse = rmse(value, estimated))

ggplot(rmse, aes(x = rmse)) +
  geom_histogram()

# entropy <- function(distrib) {
#   -1 * sum(distrib * log2(distrib))
# }
# 
# entropies <- final_distribs |> 
#   group_by(sim) |> 
#   summarise(obs_ent = entropy(value),
#             est_ent = entropy(estimated))

ggplot(entropies, aes(x = obs_ent, y = est_ent)) +
  geom_point() +
  geom_smooth(method = "lm") +
  geom_abline(slope = 1, intercept = 0,
              col = "grey", lty = "dashed") +
  theme_classic()

sim_metrics <- read_csv(here("sim_metrics.csv"))

ggplot(sim_metrics, aes(x = value, y = symmetry)) +
  geom_point() +
  geom_smooth(method = "lm", formula = "y ~ exp(x)")
