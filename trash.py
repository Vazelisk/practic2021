import types


def create_function(name, args):
    def y(): pass

    y_code = types.CodeType(args,
                            y.__code__.co_nlocals,
                            y.__code__.co_stacksize,
                            y.__code__.co_flags,
                            y.__code__.co_code,
                            y.__code__.co_consts,
                            y.__code__.co_names,
                            y.__code__.co_varnames,
                            y.__code__.co_filename,
                            name,
                            y.__code__.co_firstlineno,
                            y.__code__.co_lnotab)

    return types.FunctionType(y_code, y.func_globals, name)


myfunc = create_function('myfunc', 3)

print(repr(myfunc))
print(myfunc.func_name)
print(myfunc.func_code.co_argcount)

myfunc(1, 2, 3, 4)
