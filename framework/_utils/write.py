import sys


def json(data, file=sys.stdout, depth=3):
    ''' write json with compact but readable form: indent size = 2 spaces,
        and no more indent if exceed depth. '''
    from re import sub
    from json import dumps
    pattern = r'\n {{{},}}(  |(?=\]|\}}))'.format(2*max(0, depth-1))
    file.write(sub(pattern, ' ', dumps(data, indent=2, sort_keys=True)))


def table(data, file=sys.stdout):
    ''' write table-like for futher using in R. '''
    from csv import writer, QUOTE_NONE
    writer_obj = writer(file, quoting=QUOTE_NONE, lineterminator='\n',
                        delimiter='\t', escapechar='\\', doublequote=False)
    repr_or_na = lambda cell: repr(cell) if cell is not None else 'NA'
    for row in data:
        writer_obj.writerow([repr_or_na(col) for col in row])
