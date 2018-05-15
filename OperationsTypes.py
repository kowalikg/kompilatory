from collections import defaultdict

result_types = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

class Matrix(object):
    def __init__(self, dim):
        self.dimensions = dim

for op in ['+', '-', '*', '/', '<', '>', '<=', '>=', '==', '!=']:
    result_types[op]['int']['int'] = 'int'

for op in ['+', '-', '*', '/']:
    result_types[op]['int']['float'] = 'float'
    result_types[op]['float']['int'] = 'float'
    result_types[op]['float']['float'] = 'float'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    result_types[op]['int']['float'] = 'int'
    result_types[op]['float']['int'] = 'int'
    result_types[op]['float']['float'] = 'int'

result_types['+']['string']['string'] = 'string'
result_types['*']['string']['int'] = 'string'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    result_types[op]['string']['string'] = 'int'