import requests
import re
from pprint import pprint
import types


class Petstore:
    def __init__(self, url):
        self.resp = requests.get(url=url)
        self.j_response = self.resp.json()

    def get_args(self):
        defin_keys = list()
        for key in self.j_response:
            if key == 'definitions':
                for defin_key in self.j_response[key]:
                    # In Definitions: ApiResponse, Category...
                    defin_keys.append(defin_key)

        properties = list()
        for key in self.j_response:
            if key == 'definitions':
                for defin_key in self.j_response[key]:
                    # definitions/apiresponse/properties/code-type-message
                    properties.append(self.j_response[key][defin_key]['properties'])

        objects = dict()
        for n in range(len(defin_keys)):
            objects[defin_keys[n]] = properties[n]
        # properties for each definition in definitions
        return objects  # возвращает параметры объектов, которые отдают функции из paths

    def get_params(self):
        paths_keys = list()
        for key in self.j_response:
            if key == 'paths':
                for paths_key in self.j_response[key]:
                    # path in pathes
                    paths_keys.append(paths_key)

        params = dict()
        for paths_key in paths_keys:  # pet/petid

            params[paths_key] = {
                'post': None,
                'get': None,
                'put': None,
                'delete': None,
            }

            for tag in self.j_response['paths'][paths_key]:  # get, post
                temp_params = list()
                n = 0
                for dict_param in self.j_response['paths'][paths_key][tag][
                    'parameters']:  # if there are multiple params
                    # print(paths_key, tag)
                    # print(dict_param)
                    temp2_params = list()
                    for param in dict_param:  # in, name
                        if param == 'name':
                            temp2_params.append(self.j_response['paths'][paths_key][tag]['parameters'][n][param])
                        if param == 'type':
                            temp2_params.append(self.j_response['paths'][paths_key][tag]['parameters'][n][param])
                    if len(temp2_params) > 1:
                        joined_temp_params = '-'.join(temp2_params)
                        temp_params.append(joined_temp_params)
                    else:
                        temp_params.append(temp2_params[0])
                    n += 1
                # бывает пустой список вместо параметров
                if len(temp_params) > 0:
                    params[paths_key][tag] = temp_params
                else:
                    params[paths_key][tag] = None

        #pprint(params)
        return params

    @staticmethod
    def func_creater(params):
        all_funcs = list()
        for fnc in params:  # /pet
            f_name = True
            f_args = list()
            f_body = True

            f_name = fnc.replace('/', '_')
            for args in params[fnc].values():  # delete, get, post
                if isinstance(args, list):
                    for arg in args:
                        if '-' in arg:
                            _args = arg.split('-')
                            f_args.append((_args[0], _args[1]))
                        else:
                            f_args.append((arg, 'object'))
            f_args = list(dict.fromkeys(f_args)) # проверка на дубликаты переменных

            if len(f_args) == 3:
                f_body = f'def {f_name}({f_args[0][0]}, {f_args[1][0]}, {f_args[2][0]}):\n    raise NotImplementedError\n    return object    ()'
            elif len(f_args) == 2:
                f_body = f'def {f_name}({f_args[0][0]}, {f_args[1][0]}):\n    raise NotImplementedError\n    return object    ()'
            elif len(f_args) == 1:
                f_body = f'def {f_name}({f_args[0][0]}):\n    raise NotImplementedError\n    return object    ()'
            elif len(f_args) == 0:
                f_body = f'def {f_name}():\n    raise NotImplementedError\n    return object    ()'

            all_funcs.append(f_body)

        return all_funcs
#: {f_args[0][1]}, {f_args[1][1]}
# f_name = 'getId'
# f_args = [('arg1', 'int'), ('arg2', 'str')]
# f_output = 'dict' #object?
# f_body = f'def {f_name}({f_args[0][0]}, {f_args[1][0]}):\n    raise NotImplementedError\n    return dict    ()'

# myfunc = exec(f_body)

# myfunc(2, '3')
api = Petstore('https://petstore.swagger.io/v2/swagger.json/')
parsed = api.get_params()
funcs = api.func_creater(parsed)
# print(funcs[1])
# myfunc = exec(funcs[1])
# print(myfunc)

