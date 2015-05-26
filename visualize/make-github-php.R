#!/usr/bin/env Rscript

library(ggplot2)
source('base.R')

php.data = parse.read.table('github', 'compatibility-php.txt')

compat.abandon = c('CodeIgniter', 'composer', 'laravel', 'framework',
                   'sage', 'symfony', 'yii2', 'cakephp', 'Faker', 'zf2',
                   'guzzle', 'openbay', 'PHPExcel', 'core', 'ThinkUp',
                   'october', 'Silex', 'DesignPatternsPHP')

compat.keep = c('Carbon', 'PHPMailer', 'piwik', 'Slim', 'yii', 'WordPress',
                'phabricator', 'Mobile-Detect', '_s', 'sovereign', 'daux.io',
                'phpunit', 'monolog', 'react', 'assetic', 'twitteroauth')

compat.all = c(compat.abandon, compat.keep)

php.data = php.data[php.data$repo %in% compat.all,]

png('gh-php-all.png', width=600, height=450)
ggplot(php.data, aes(x=date, y=php53/files, group=repo)) +
    geom_line() +
    theme_bw()
dev.off()
