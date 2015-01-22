from .abstract import WordProcessor, Identifier


c = WordProcessor(
    quoting = r'"(?:[^"\\]|\\.)*"' + '|' + r"'([^'\\]|\\.)'",
    line_comment = r'//.*',
    block_comment = r'/\*.*\*/',
    keywords = ['auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 'inline', 'int', 'long', 'register', 'restrict', 'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while', '_Alignas', '_Alignof', '_Atomic', '_Bool', '_Complex', '_Generic', '_Imaginary', '_Noreturn', '_Static_assert', '_Thread_local', '#if', '#elif', '#else', '#endif', '#defined', '#ifdef', '#ifndef', '#define', '#undef', '#include', '#line', '#error', '#pragma'],
)



c_plus_plus = WordProcessor(
    quoting = r'"(?:[^"\\]|\\.)*"' + '|' + r"'([^'\\]|\\.)'",
    line_comment = r'//.*',
    block_comment = r'/\*.*\*/',
    keywords = ['alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand', 'bitor', 'bool', 'break', 'case', 'catch', 'char', 'char16_t', 'char32_t', 'class', 'compl', 'const', 'constexpr', 'const_cast', 'continue', 'decltype', 'default', 'delete', 'do', 'double', 'dynamic_cast', 'else', 'enum', 'explicit', 'export', 'extern', 'false', 'float', 'for', 'friend', 'goto', 'if', 'inline', 'int', 'long', 'mutable', 'namespace', 'new', 'noexcept', 'not', 'not_eq', 'nullptr', 'operator', 'or', 'or_eq', 'private', 'protected', 'public', 'register', 'reinterpret_cast', 'return', 'short', 'signed', 'sizeof', 'static', 'static_assert', 'static_cast', 'struct', 'switch', 'template', 'this', 'thread_local', 'throw', 'true', 'try', 'typedef', 'typeid', 'typename', 'union', 'unsigned', 'using', 'virtual', 'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq', 'override', 'final', '#if', '#elif', '#else', '#endif', '#defined', '#ifdef', '#ifndef', '#define', '#undef', '#include', '#line', '#error', '#pragma'],
)



c_sharp = WordProcessor(
    quoting = r'"(?:[^"\\]|\\.)*"' + '|' + r"'([^'\\]|\\.)'",
    line_comment = r'//.*',
    block_comment = r'/\*.*\*/',
    keywords = ['abstract', 'as', 'base', 'bool', 'break', 'byte', 'case', 'catch', 'char', 'checked', 'class', 'const', 'continue', 'decimal', 'default', 'delegate', 'do', 'double', 'else', 'enum', 'event', 'explicit', 'extern', 'false', 'finally', 'fixed', 'float', 'for', 'foreach', 'goto', 'if', 'implicit', 'in', 'int', 'interface', 'internal', 'is', 'lock', 'long', 'namespace', 'new', 'null', 'object', 'operator', 'out', 'override', 'params', 'private', 'protected', 'public', 'readonly', 'ref', 'return', 'sbyte', 'sealed', 'short', 'sizeof', 'stackalloc', 'static', 'string', 'struct', 'switch', 'this', 'throw', 'true', 'try', 'typeof', 'uint', 'ulong', 'unchecked', 'unsafe', 'ushort', 'using', 'virtual', 'void', 'volatile', 'while', 'add', 'alias', 'ascending', 'async', 'await', 'descending', 'dynamic', 'from', 'get', 'global', 'group', 'into', 'join', 'let', 'orderby', 'partial', 'remove', 'select', 'set', 'value', 'var', 'where', 'yield'],
)



java = WordProcessor(
    quoting = r'"(?:[^"\\]|\\.)*"' + '|' + r"'([^'\\]|\\.)'",
    line_comment = r'//.*',
    block_comment = r'/\*.*\*/',
    keywords = ['abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private', 'protected', 'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while'],
)



python = WordProcessor(
    quoting = r"r?(\"{1,3}|\'{1,3})([^\1\\]*?(\\.[^\1\\]*?)*?)\1",
    line_comment = r"#.*",
    keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'],
)



ruby = WordProcessor(
    quoting = r"(\"|\')([^\1\\]*?(\\.[^\1\\]*?)*?)\1",
    line_comment = r"#.*",
    keywords = ['__ENCODING__', '__LINE__', '__FILE__', 'BEGIN', 'END', 'alias', 'and', 'begin', 'break', 'case', 'class', 'def', 'defined?', 'do', 'else', 'elsif', 'end', 'ensure', 'false', 'for', 'if', 'in', 'module', 'next', 'nil', 'not', 'or', 'redo', 'rescue', 'retry', 'return', 'self', 'super', 'then', 'true', 'undef', 'unless', 'until', 'when', 'while', 'yield'],
)



haskell = WordProcessor(
    quoting = r'"(?:[^"\\]|\\.)*"' + '|' + r"'([^'\\]|\\.)'",
    line_comment = r"--.*",
    keywords = ['as', 'case', 'of', 'class', 'data', 'data family', 'data instance', 'default', 'deriving', 'deriving instance', 'do', 'forall', 'foreign', 'hiding', 'if', 'then', 'else', 'import', 'infix', 'infixl', 'infixr', 'instance', 'let', 'in', 'mdo', 'module', 'newtype', 'proc', 'qualified', 'rec', 'type', 'type family', 'type instance', 'where'],
)



php = WordProcessor(
    quoting = r"(\"|\')([^\1\\]*?(\\.[^\1\\]*?)*?)\1",
    line_comment = r"#.*" + '|' + r'//.*',
    block_comment = r'/\*.*\*/',
    keywords = ['__halt_compiler', 'abstract', 'and', 'array', 'as', 'break', 'callable', 'case', 'catch', 'class', 'clone', 'const', 'continue', 'declare', 'default', 'die', 'do', 'echo', 'else', 'elseif', 'empty', 'enddeclare', 'endfor', 'endforeach', 'endif', 'endswitch', 'endwhile', 'eval', 'exit', 'extends', 'final', 'finally', 'for', 'foreach', 'function', 'global', 'goto', 'if', 'implements', 'include', 'include_once', 'instanceof', 'insteadof', 'interface', 'isset', 'list', 'namespace', 'new', 'or', 'print', 'private', 'protected', 'public', 'require', 'require_once', 'return', 'static', 'switch', 'throw', 'trait', 'try', 'unset', 'use', 'var', 'while', 'xor', 'yield', '__CLASS__', '__DIR__', '__FILE__', '__FUNCTION__', '__LINE__', '__METHOD__', '__NAMESPACE__', '__TRAIT__'],
)



scala = WordProcessor(
    quoting = r'"(?:[^"\\]|\\.)*"' + '|' + r"'([^'\\]|\\.)'",
    line_comment = r'//.*',
    block_comment = r'/\*.*\*/',
    keywords = ['abstract', 'case', 'catch', 'class', 'def', 'do', 'else', 'extends', 'false', 'final', 'finally', 'for', 'forSome', 'if', 'implicit', 'import', 'lazy', 'match', 'new', 'null', 'object', 'override', 'package', 'private', 'protected', 'return', 'sealed', 'super', 'this', 'throw', 'trait', 'try', 'true', 'type', 'val', 'var', 'while', 'with', 'yield']
)



go = WordProcessor(
    quoting = r"(\"|\`)([^\1\\]*?(\\.[^\1\\]*?)*?)\1",
    line_comment = r'//.*',
    block_comment = r'/\*.*\*/',
    keywords = ['break', 'case', 'chan', 'const', 'continue', 'default', 'defer', 'else', 'fallthrough', 'for', 'func', 'go', 'goto', 'if', 'import', 'interface', 'map', 'package', 'range', 'return', 'select', 'struct', 'switch', 'type', 'var'],
)




javascript = WordProcessor(
    quoting = r"(\"|\')([^\1\\]*?(\\.[^\1\\]*?)*?)\1",
    line_comment = r'//.*',
    block_comment = r'/\*.*\*/',
    keywords = ['abstract', 'arguments', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue', 'debugger', 'default', 'delete', 'do', 'double', 'else', 'enum', 'eval', 'export', 'extends', 'false', 'final', 'finally', 'float', 'for', 'function', 'goto', 'if', 'implements', 'import', 'in', 'instanceof', 'int', 'interface', 'let', 'long', 'native', 'new', 'null', 'package', 'private', 'protected', 'public', 'return', 'short', 'static', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'true', 'try', 'typeof', 'var', 'void', 'volatile', 'while', 'with', 'yield'],
)



perl = WordProcessor(
    quoting = r"(\"|\')([^\1\\]*?(\\.[^\1\\]*?)*?)\1",
    line_comment = r"#.*",
    keywords = ['__DATA__', '__END__', '__FILE__', '__LINE__', '__PACKAGE__', 'and', 'cmp', 'continue', 'CORE', 'do', 'else', 'elsif', 'eq', 'exp', 'for', 'foreach', 'ge', 'gt', 'if', 'le', 'lock', 'lt', 'm', 'ne', 'no', 'or', 'package', 'q', 'qq', 'qr', 'qw', 'qx', 's', 'sub', 'tr', 'unless', 'until', 'while', 'xor', 'y'],
)



def select(ext):
    return { '.c': c,
             '.cc': c_plus_plus,
             '.cpp': c_plus_plus,
             '.cxx': c_plus_plus,
             '.cs': c_sharp,
             '.go': go,
             '.hs': haskell,
             '.java': java,
             '.js': javascript,
             '.php': php,
             '.pl': perl,
             '.py': python,
             '.rb': ruby,
             '.scala': scala }[ext.lower()]
