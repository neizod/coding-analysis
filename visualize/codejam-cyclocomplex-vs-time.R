#!/usr/bin/env Rscript

library(ggplot2)
source('base.R')

## prepare data ##############################################################

cyclo.data = Reduce(merge, list(
    parse.read.table('codejam', 'cyclomatic-complexity.2014.txt'),
    parse.read.table('codejam', 'contest-problem-name.2014.txt'),
    parse.read.table('codejam', 'submission-time.2014.txt'),
    parse.read.table('codejam', 'language.2014.txt')))

cyclo.lotto = cyclo.data[cyclo.data$pname == 'B. New Lottery Game',]

## plotting ##################################################################

plot = ggplot(cyclo.lotto, aes(x=submission.time/60,
                               y=mean.cyclomatic.complexity)) +
    geom_smooth(method=lm, col='black', se=FALSE, aes(linetype=language)) +
    scale_linetype_manual(values=c('dotdash', 'dotted', 'solid')) +
    xlab('submission time (minutes)') +
    ylab('average cyclomatic complexity') +
    theme_bw() +
    theme(legend.justification=c(0,1), legend.position=c(0,1))
ggsave(plot, file='cj-cc-time.png', width=5, height=3)
