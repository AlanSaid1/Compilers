from delta import Compiler, Phase

source = '10 || 20 || 30'


c = Compiler('program')
c.realize(source, Phase.EVALUATION)
print()
print(c.wat_code)
print()
print(c.result)