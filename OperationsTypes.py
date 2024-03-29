from collections import defaultdict

from SymbolTable import Matrix

result_types = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

for op in ['.+', '.-', '.*', './']:
    result_types[op][Matrix.__name__][Matrix.__name__] = Matrix.__name__

for op in ['+', '-', '*', '/',  '+=', '-=', '*=', '/=', '<', '>', '<=', '>=', '==', '!=']:
    result_types[op]['int']['int'] = 'int'

for op in ['*=', '*']:
    result_types[op]['int'][Matrix.__name__] = Matrix.__name__
    result_types[op]['float'][Matrix.__name__] = Matrix.__name__
    result_types[op][Matrix.__name__]['int'] = Matrix.__name__
    result_types[op][Matrix.__name__]['float'] = Matrix.__name__

for op in ['/=', '/']:
    result_types[op][Matrix.__name__]['int'] = Matrix.__name__
    result_types[op][Matrix.__name__]['float'] = Matrix.__name__

for op in ['+', '-', '*', '/', '+=', '-=', '*=', '/=']:
    result_types[op]['int']['float'] = 'float'
    result_types[op]['float']['int'] = 'float'
    result_types[op]['float']['float'] = 'float'
    result_types[op][Matrix.__name__][Matrix.__name__] = Matrix.__name__

for op in ['<', '>', '<=', '>=', '==', '!=']:
    result_types[op]['int']['float'] = 'int'
    result_types[op]['float']['int'] = 'int'
    result_types[op]['float']['float'] = 'int'

result_types['+']['string']['string'] = 'string'
result_types['*']['string']['int'] = 'string'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    result_types[op]['string']['string'] = 'int'
    result_types[op][Matrix.__name__][Matrix.__name__] = 'int'

result_types['\''][Matrix.__name__] = Matrix.__name__
result_types['-'][Matrix.__name__] = Matrix.__name__
result_types['-']['int'] = 'int'
result_types['-']['float'] = 'float'