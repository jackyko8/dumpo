import re

def dumpo(obj, **kwargs):
    _level = 0
    as_is = []
    as_is_tag = "<as_is>"
    compressed = True
    debug = False
    deep_types = []
    excluded = []
    excluded_tag = "<excluded>"
    expand_keys = False
    include_all_keys = False
    include_functions = False
    indent = "| "
    item_quotes = None
    json_like = False
    maxdepth = 5
    quotes = ""
    show_all_types = False
    show_types = True
    too_deep_tag = "<too_deep>"

    # Allow overriding; otherwise, put this block after all kwargs init
    json_like = kwargs.get('json_like', json_like)
    if json_like:
        indent = '  '
        item_quotes = '"'
        show_types = False
        show_all_types = False

    _level = kwargs.get('_level', _level)
    as_is = kwargs.get('as_is', as_is)
    as_is_tag = kwargs.get('as_is_tag', as_is_tag)
    compressed = kwargs.get('compressed', compressed)
    debug = kwargs.get('debug', debug)
    deep_types = kwargs.get('deep_types', deep_types)
    excluded = kwargs.get('excluded', excluded)
    excluded_tag = kwargs.get('excluded_tag', excluded_tag)
    expand_keys = kwargs.get('expand_keys', expand_keys)
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
        if show_all_types or (show_types and not my_type_name in ('str', 'int', 'float', 'bool', 'dict', 'list', 'tuple', 'NoneType')):
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
                        dummy = obj[x]
                    except:
                        type_iter = 'i'  # Item: item for item in obj
                        bracket_begin, bracket_end = '[', ']'
                    else:
                        type_iter = 's'  # Subscript: obj[item] for item in obj
                    # Just one loop
                    break
            except:
                # Cannot even loop; stay as object
                pass

        return type_name, type_iter, keyed, bracket_begin, bracket_end


    def typeDesc(type_name, type_iter, keyed, bracket_begin, bracket_end):
        return f'<{type_name}>' + bracket_begin + (type_iter.upper() if keyed else type_iter) + bracket_end


    def keyIgnored(k):
        return isinstance(k, str) and k.startswith('__') and k.endswith('__')


    def attrGenItem(obj):
        n = 0
        for item in obj:
            yield {n: item}
            n += 1


    def attrGenSubscript(obj):
        for item in obj:
            # item may have a structure
            if f'{item}' in excluded:
                if excluded_tag == '':
                    continue
                yield {item: excluded_tag}
            else:
                yield {item: obj[item]}


    def attrGenAttribute(obj):
        item_list = obj.__dict__
        if include_all_keys:
            item_list = dir(obj)
        for item in item_list:
            # item may have a structure
            if not keyIgnored(item):
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
                    if include_functions and isFunc:
                        yield {f'{item}()': {}}
                    elif not isFunc:
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
                if obj == excluded_tag:
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
            if keyed and keyIgnored(itemKey):
                continue
            n += 1
            ret += postStr + preStr
            objStr = typeToShow(itemObj)
            if type(itemObj) == type(obj):
                # Same as parent. To avoid recursion, display as is (quietly)
                objStr += jsonTreat(f'{itemObj}')
            else:
                objStr += dumpo(itemObj, **kwargs)
            if keyed:
                # Do not use f'...' as the quote strings may form an unwanted bracket
                ret += item_quoteB
                if expand_keys:
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
