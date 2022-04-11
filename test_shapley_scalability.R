# Test shapley package
source("C:/Users/fyang28/Desktop/Pouliot/shapley/R/shapley.R")

# Define a simple aggregation function
reg <- function(regressors) {
  if (length(regressors) == 0) return(0)
  formula <- paste0("mpg ~ ", paste(regressors, collapse = "+"))
  m <- summary(lm(formula, data = mtcars))
  m[["r.squared"]]
}

# Define another simple aggreation function
agg_test <- function(el){
  sum(el)
}

tic=proc.time()[3]
#res1 <- shapley_sampled(reg,
#                c("cyl", "disp", "hp", "drat", "wt", "qsec", "vs", "am", "gear", "carb"),
#                last_n = 10,
#                precision = .01,
#                silent = TRUE)
#res1 <- shapley(reg,
#                c("cyl", "disp", "hp", "drat", "wt", "qsec", "vs", "am", "gear", "carb"),
#                )
res1 <- shapley(agg_test,
                c(1,55,3,4,7,8,9,12,4,44,66,77,88,99,100,16,17),
                )

toc=proc.time()[3] - tic
print(res1)
print(toc)