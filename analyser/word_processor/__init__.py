from .abstract import WordProcessor, Identifier


cpp = WordProcessor(
    quoting = r'"(?:[^"\\]|\\.)*"' + '|' + r"'([^'\\]|\\.)'",
    comment = [r'/\*.*\*/', r'//.*'],
    keywords = ['alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand', 'bitor', 'bool', 'break', 'case', 'catch', 'char', 'char16_t', 'char32_t', 'class', 'compl', 'const', 'constexpr', 'const_cast', 'continue', 'decltype', 'default', 'delete', 'do', 'double', 'dynamic_cast', 'else', 'enum', 'explicit', 'export', 'extern', 'false', 'float', 'for', 'friend', 'goto', 'if', 'inline', 'int', 'long', 'mutable', 'namespace', 'new', 'noexcept', 'not', 'not_eq', 'nullptr', 'operator', 'or', 'or_eq', 'private', 'protected', 'public', 'register', 'reinterpret_cast', 'return', 'short', 'signed', 'sizeof', 'static', 'static_assert', 'static_cast', 'struct', 'switch', 'template', 'this', 'thread_local', 'throw', 'true', 'try', 'typedef', 'typeid', 'typename', 'union', 'unsigned', 'using', 'virtual', 'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq', 'override', 'final', '#if', '#elif', '#else', '#endif', '#defined', '#ifdef', '#ifndef', '#define', '#undef', '#include', '#line', '#error', '#pragma'],
    noise = r'[^a-zA-Z_0-9]'
)



java = WordProcessor(
    quoting = r'"(?:[^"\\]|\\.)*"' + '|' + r"'([^'\\]|\\.)'",
    comment = [r'/\*.*\*/', r'//.*'],
    keywords = ['abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private', 'protected', 'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while'],
    noise = r'[^a-zA-Z_0-9]'
)



python = WordProcessor(
    quoting = r"r?(\"{1,3}|\'{1,3})([^\1\\]*?(\\.[^\1\\]*?)*?)\1",
    comment = [None, r"#.*"],
    keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'],
    noise = r'[^a-zA-Z_0-9]'
)



def select(ext):
    return { '.cpp': cpp,
             '.java': java,
             '.py': python }[ext.lower()]
