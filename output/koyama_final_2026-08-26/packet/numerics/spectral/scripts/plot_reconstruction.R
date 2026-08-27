args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
  stop("usage: Rscript plot_reconstruction.R reconstruction.tsv output.pdf output.png")
}

data <- read.delim(args[1], check.names = FALSE)
moduli <- c(7, 8, 11, 19, 23)
colors <- c("#111111", "#3B82F6", "#10B981", "#F59E0B", "#DC2626")
labels <- c("observed", "1 zero/character", "3 zeros/character", "10 zeros/character", "25 zeros/character")

draw_figure <- function() {
  layout(matrix(seq_along(moduli), ncol = 1))
  par(mar = c(2.4, 4.2, 1.3, 1.0), oma = c(2.0, 0.5, 1.0, 0.5),
      mgp = c(2.2, 0.7, 0), tcl = -0.25)
  for (q in moduli) {
    panel <- data[data$q == q & data$a == q - 1, ]
    xx <- log10(panel$x)
    yy <- as.matrix(panel[, c("E_observed", "E_K1", "E_K3", "E_K10", "E_K25")])
    ylim <- range(yy, finite = TRUE)
    plot(xx, yy[, 1], type = "l", lwd = 1.4, col = colors[1],
         xlab = "", ylab = bquote(E[.(q)](x, -1, 1)), ylim = ylim,
         axes = FALSE)
    axis(1, at = seq(6, 14, by = 2), labels = if (q == 23) seq(6, 14, by = 2) else FALSE)
    axis(2, las = 1)
    box()
    for (j in 2:5) lines(xx, yy[, j], col = colors[j], lwd = 0.9)
    abline(h = 0, col = "grey75", lty = 3)
    mtext(paste0("N = ", q), side = 3, adj = 0.01, line = 0.1, font = 2, cex = 0.85)
    if (q == 7) {
      legend("topright", legend = labels, col = colors, lty = 1,
             lwd = c(1.4, rep(0.9, 4)), bty = "n", ncol = 3, cex = 0.72)
    }
  }
  mtext(expression(log[10](x)), side = 1, outer = TRUE, line = 0.7)
  mtext("Observed ordinary-count race and low-zero explicit-formula truncations",
        side = 3, outer = TRUE, line = -0.1, font = 2, cex = 0.95)
}

pdf(args[2], width = 8.0, height = 11.0, useDingbats = FALSE)
draw_figure()
dev.off()

png(args[3], width = 1800, height = 2475, res = 220)
draw_figure()
dev.off()
