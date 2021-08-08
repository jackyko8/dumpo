import re


def dumpo(obj, **kwargs):
    _known_type = (
        'str',
        'int',
        'float',
        'bool',
        'dict',
        'list',
        'tuple',
        'NoneType'
    )

    _valid_kwargs = (
        '_level',
        'as_is',
        'as_is_tag',
        'code_tag',
        'compressed',
        'debug',
        'deep_types',
        'excluded',
        'excluded_tag',
        'expand_keys',
        'include_all_keys',
        'include_everything',
        'include_internals',
        'include_functions',
        'indent',
        'item_quotes',
        'json_like',
        'maxdepth',
        'quotes',
        'show_all_types',
        'show_types',
        'too_deep_tag',
    )

    _level = 0
    as_is = []
    as_is_tag = "<as_is>"
    code_tag = "<code>"
    compressed = True
    debug = False
    deep_types = []
    excluded = []
    excluded_tag = "<excluded>"
    expand_keys = False
    include_all_keys = False
    include_everything = False
    include_internals = False
    include_functions = False
    indent = "| "
    item_quotes = None
    json_like = False
    maxdepth = 5
    quotes = ""
    show_all_types = False
    show_types = True
    too_deep_tag = "<too_deep>"

    json_like = kwargs.get('json_like', json_like)
    if json_like:
        indent = '  '
        item_quotes = '"'
        show_types = False
        show_all_types = False

    _level = kwargs.get('_level', _level)
    as_is = kwargs.get('as_is', as_is)
    as_is_tag = kwargs.get('as_is_tag', as_is_tag)
    code_tag = kwargs.get('code_tag', code_tag)
    compressed = kwargs.get('compressed', compressed)
    debug = kwargs.get('debug', debug)
    deep_types = kwargs.get('deep_types', deep_types)
    excluded = kwargs.get('excluded', excluded)
    excluded_tag = kwargs.get('excluded_tag', excluded_tag)
    expand_keys = kwargs.get('expand_keys', expand_keys)
    include_internals = kwargs.get('include_internals', include_internals)
    include_functions = kwargs.get('include_functions', include_functions)
    indent = kwargs.get('indent', indent)
    item_quotes = kwargs.get('item_quotes', item_quotes)
    maxdepth = kwargs.get('maxdepth', maxdepth)
    quotes = kwargs.get('quotes', quotes)
    include_all_keys = kwargs.get('include_all_keys', include_all_keys)
    show_all_types = kwargs.get('show_all_types', show_all_types)
    show_types = kwargs.get('show_types', show_types)
    too_deep_tag = kwargs.get('too_deep_tag', too_deep_tag)

    if isinstance(as_is, str):
        as_is = [as_is]

    if isinstance(deep_types, str):
        deep_types = [deep_types]

    if isinstance(excluded, str):
        excluded = [excluded]

    # Override other includes
    include_everything = kwargs.get('include_everything', include_everything)
    if include_everything:
        expand_keys = True
        include_all_keys = True
        include_functions = True
    elif not '__dict__' in excluded:
        # Hard exclude
        excluded.append('__dict__')


    # Check for unknown kwargs
    class UnknownKwargs(Exception):
        pass

    _unknown_kwargs = []
    for kwa in kwargs:
        if not kwa in _valid_kwargs:
            _unknown_kwargs.append(kwa)
    try:
        if len(_unknown_kwargs):
            raise UnknownKwargs
    except UnknownKwargs:
        if _level == 0:
            print(f'Unknown key word arguments ignored: {", ".join(_unknown_kwargs)}')
        pass

    def getQuotes(quotesSpec, defaultB, defaultE):
        b = defaultB
        e = defaultE
        if quotesSpec != None:
            b = ''
            e = ''
            if len(quotesSpec) > 0:
                b = quotesSpec[0]
                e = b
            if len(quotesSpec) > 1:
                e = quotesSpec[1]
        return b, e


    def escapeQuotes(s, b, e):
        ret = s
        # Only if the begin and end quotes are the same
        if b and b == e:
            ret = ret.replace(b, '\\' + b)
        return ret


    def jsonTreat(obj):
        ret = f'{obj}'
        if json_like and (isinstance(obj, str) or not re.search(r"^([-+])?[0-9]+(\.[0-9]+)?$", ret)):
            ret = ret.replace('\n', '\\n')
            ret = '"' + escapeQuotes(ret, '"', '"') + '"'
        return ret


    def typeToShow(obj):
        ret = ''
        my_type_name = type(obj).__name__
        if show_all_types or (show_types and not my_type_name in _known_type):
            ret = f'<{my_type_name}>'
        return ret


    def typeAnalyser(obj):
        type_iter = 'o'  # Object (scalar)
        type_name = type(obj).__name__
        keyed = False  # Not keyed
        bracket_begin, bracket_end = '{', '}'

        if isinstance(obj, dict):
            keyed = True
            type_iter = 's'  # Subscript: obj[item] for item in obj
        elif isinstance(obj, list):
            type_iter = 'i'  # Item: item for item in obj
            bracket_begin, bracket_end = '[', ']'
        elif isinstance(obj, tuple):
            type_iter = 'i'  # Item: item for item in obj
            bracket_begin, bracket_end = '(', ')'
        elif isinstance(obj, set):
            type_iter = 'i'  # Item: item for item in obj
            bracket_begin, bracket_end = '{', '}'
        elif hasattr(obj, '__dict__'):
            keyed = True
            type_iter = 'a'  # Attribute: getattr(obj, item) for item in obj.__dict__
        elif not isinstance(obj, str):
            # Failing all that, try actual looping
            try:
                for x in obj:
                    try:
                        _ = obj[x]
                    except:
                        type_iter = 'i'  # Item: item for item in obj
                    else:
                        type_iter = 's'  # Subscript: obj[item] for item in obj
                        if f'{x}' == f'{obj[0]}':
                            type_iter = 'i'
                            # It is actually an item, just that the object
                            # is acceptable to subscribe (like ndarray)
                    # Just one loop
                    break
                if type_iter == 'i':
                    bracket_begin, bracket_end = '[', ']'
            except:
                # Cannot even loop; stay as object
                pass

        return type_name, type_iter, keyed, bracket_begin, bracket_end


    def typeDesc(type_name, type_iter, keyed, bracket_begin, bracket_end):
        return f'<{type_name}>' + bracket_begin + (type_iter.upper() if keyed else type_iter) + bracket_end


    def keyIgnored(obj, item):
        ignored = False

        # Not ignoring non-string items
        if isinstance(item, str):
            isFunc = False
            isBuiltIn = False
            isInternal = False

            try:
                isFunc = callable(getattr(obj, item))
            except:
                pass
            if item.startswith('__'):
                isBuiltIn = True
            elif item.startswith('_'):
                isInternal = True

            if include_all_keys:
                # Only exclude __dict__
                if item == '__dict__':
                    ignored = True
            else:
                if isBuiltIn:
                    ignored = True
                elif not include_internals and isInternal:
                    ignored = True
                elif not include_functions and isFunc:
                    ignored = True

        return ignored


    def attrGenItem(obj):
        n = 0
        for item in obj:
            if keyIgnored(obj, item):
                continue
            yield {n: item}
            n += 1


    def attrGenSubscript(obj):
        for item in obj:
            # item may have a structure
            if keyIgnored(obj, item):
                continue
            if f'{item}' in excluded:
                if excluded_tag == '':
                    continue
                yield {item: excluded_tag}
            else:
                yield {item: obj[item]}


    def attrGenAttribute(obj):
        # item_list = obj.__dict__
        # if include_all_keys or include_functions:
        #     item_list = dir(obj)
        item_list = dir(obj)
        for item in item_list:
            # item may have a structure
            if keyIgnored(obj, item):
                continue
            if not hasattr(obj, item):
                continue
            attr = getattr(obj, item)
            isFunc = callable(attr)
            if f'{item}' in excluded:
                if excluded_tag == '':
                    continue
                if isFunc:
                    yield {f'{item}()': excluded_tag}
                else:
                    yield {item: excluded_tag}
            else:
                if isFunc:
                    yield {f'{item}()': code_tag}
                else:
                    yield {item: attr}


    type_name, type_iter, keyed, bracket_begin, bracket_end = typeAnalyser(obj)

    if _level > maxdepth and not type_name in deep_types:
        ret = jsonTreat(too_deep_tag)
        if debug:
            ret += typeDesc(type_name, type_iter, keyed, bracket_begin, bracket_end)
        return ret

    kwargs['_level'] = _level + 1

    lineBreak = '\n' if indent else ' '  # No line break if indent is blank

    ind = indent * _level  # The indentation of the object
    preStr = indent * (_level + 1)  # The indentation of the elements of the object
    postStr = lineBreak  # End of the previous line

    attrGen = {'i': attrGenItem, 's': attrGenSubscript, 'a': attrGenAttribute, 'o': None}[type_iter]

    quoteB, quoteE = getQuotes(quotes, '', '')
    item_quoteB, item_quoteE = getQuotes(item_quotes, quoteB, quoteE)

    ret = ''

    if attrGen == None or type_name in as_is:
        # A scalar object
        if type_name == 'str':
            if json_like:
                # No freedom to use own quotes
                ret += jsonTreat(obj)
            else:
                # The 'excluded' tag appears as a string.
                # It is not blank as the generator should have filtered excluded_tag == ''
                if obj == excluded_tag or obj == code_tag:
                    ret += obj
                else:
                    if quoteB == '' and quoteE == '':
                        # Force quotes for str
                        ret += '"' + escapeQuotes(obj, '"', '"') + '"'
                    else:
                        ret += quoteB + escapeQuotes(obj, quoteB, quoteE) + quoteE
        elif json_like:
            ret += jsonTreat(obj)
        else:
            ret += f'{obj}{as_is_tag if type_name in as_is else ""}'
        if debug:
            ret += typeDesc(type_name, type_iter, keyed, bracket_begin, bracket_end)
    else:
        # An iterable with generator attrGen
        # Only list, tuple and list are compressable
        if compressed and type_name in ('list', 'tuple', 'set'):
            lineBreak = ''
            ind = ' '
            postStr = ''
            preStr = ' '

        n = 0
        objStr = ''
        ret += bracket_begin
        attrs = attrGen(obj)
        for item in attrs:
            # itm is a single element dict
            for x in item:
                # Only one loop
                itemKey = x
                itemObj = item[x]
            if keyed and keyIgnored(itemObj, itemKey):
                continue
            n += 1
            ret += postStr + preStr
            objStr = typeToShow(itemObj)
            if type(itemObj).__name__ not in _known_type and type(itemObj) == type(obj):
                # Same as parent. To avoid recursion, display as is (quietly)
                objStr += jsonTreat(f'{itemObj}')
            else:
                objStr += dumpo(itemObj, **kwargs)
            if keyed:
                # Do not use f'...' as the quote strings may form an unwanted bracket
                ret += item_quoteB
                if expand_keys and not isinstance(itemKey, str):
                    itemKey = dumpo(itemKey, **kwargs)
                ret += escapeQuotes(f'{itemKey}', item_quoteB, item_quoteE)
                ret += item_quoteE + ': '
            # Do not quote here as objStr may be a structure
            ret += f'{objStr}'
            postStr = ',' + lineBreak

        if n == 0:
            # Show as is (overwriting opening, no +=)
            ret = jsonTreat(f'{obj}{as_is_tag if objStr else ""}')
            if debug:
                ret += typeDesc(type_name, type_iter, keyed, bracket_begin, bracket_end)
        else:
            ret += lineBreak + ind + bracket_end

        if json_like and isinstance(obj, tuple):
            ret = jsonTreat(ret)

    if _level == 0:
        ret = typeToShow(obj) + ret

    return ret
