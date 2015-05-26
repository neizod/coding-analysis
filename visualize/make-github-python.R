#!/usr/bin/env Rscript

library(ggplot2)
source('base.R')

python.data = parse.read.table('github', 'compatibility-python.txt')

compat.ok = c('django', 'httpie', 'ipython', 'powerline', 'requests',
              'shadowsocks', 'YouCompleteMe', 'youtube-dl', 'thefuck',
              'legit', 'python-patterns')

compat.swing = c('compose', 'pyspider', 'salt')

compat.almost = c('flask', 'tornado', 'scrapy', 'sentry', 'scikit-learn',
                  'fabric', 'beets', 'ajenti', 'Flashlight', 'celery',
                  'pandas', 'boto')

compat.noway = c('ansible', 'bup', 'Dshell', 'reddit', 'huxley', 'sshuttle')

compat.all = c(compat.ok, compat.swing, compat.almost, compat.noway)

python.data = python.data[python.data$repo %in% compat.all,]

png('gh-py-all.png', width=600, height=450)
ggplot(python.data, aes(x=date, y=py3/files, group=repo)) +
    geom_line() +
    theme_bw()
dev.off()
