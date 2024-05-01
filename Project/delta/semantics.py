from arpeggio import PTNodeVisitor


class SemanticMistake(Exception):

    def __init__(self, message):
        super().__init__(f'Semantic error: {message}')


class SemanticVisitor(PTNodeVisitor):

    RESERVED_WORDS = ['true', 'false', 'var',
                      'if', 'else', 'while']

    def __init__(self, parser, **kwargs):
        super().__init__(**kwargs)
        self.__parser = parser
        self.__symbol_table = []

    def position(self, node):
        return self.__parser.pos_to_linecol(node.position)

    @property
    def symbol_table(self):
        return self.__symbol_table

    def visit_decl_variable(self, node, children):
        name = node.value
        if name in SemanticVisitor.RESERVED_WORDS:
            raise SemanticMistake(
                'Reserved word not allowed as variable name at position '
                f'{self.position(node)} => {name}'
            )
        if name in self.__symbol_table:
            raise SemanticMistake(
                'Duplicate variable declaration at position '
                f'{self.position(node)} => {name}'
            )
        self.__symbol_table.append(name)

    def visit_lhs_variable(self, node, children):
        name = node.value
        if name not in self.__symbol_table:
            raise SemanticMistake(
                'Assignment to undeclared variable at position '
                f'{self.position(node)} => {name}'
            )

    def visit_rhs_variable(self, node, children):
        name = node.value
        if name not in self.__symbol_table:
            raise SemanticMistake(
                'Undeclared variable reference at position '
                f'{self.position(node)} => {name}'
            )
        
    '''
    Hace que al momento de encontrarse con alguno de estos nodos, se haga la correcta conversión de los valores
    '''
    def visit_integer(self, node, children):
        #binary
        if node.value.startswith('#b'):
            value = int(node.value[2:], 2)
        # octal
        elif node.value.startswith('#o'):
            value = int(node.value[2:], 8)
        # exadecimal
        elif node.value.startswith('#x'):
            value = int(node.value[2:], 16)
        # Al igual que si solo se encuentra sin estos prefijos
        else:
            value = int(node.value)
        if value < 0:
            raise SemanticMistake(
                'Negative integer at position '
                f'{self.position(node)} => {value}'
            )
        if value > 0xFFFFFFFF:
            raise SemanticMistake(
                'Integer out of range at position '
                f'{self.position(node)} => {value}'
            )

