class FilterQueryBuilder:
    def __init__(self, query=None):
        self.__repr__ = self.__str__

        self.query = query

    def _operations(self, property_name, keyword, operator, conditional):
        conditional = getattr(self, conditional)
        return conditional(
            "{} {} '{}'".format(property_name, operator, keyword)
        )

    def _functions(self, property_name, keyword, function_name, conditional):
        conditional = getattr(self, conditional)
        conditional(
            "{}({},'{}')".format(function_name, property_name, keyword)
        )

    def _conditionals(self, query, conditional):
        return " {} {} {}".format(self.query.strip(), conditional, query)

    # Conditional operators
    def and_(self, query):
        self.query = self._conditionals(query, "and")

    def or_(self, query):
        self.query = self._conditionals(query, "or")

    # Equality operators
    def eq_(self, property_name, keyword, conditional="and"):
        return self._operations(
            property_name=property_name,
            keyword=keyword,
            operator="eq",
            conditional=conditional
        )

    def ne_(self, property_name, keyword, conditional="and"):
        return self._operations(
            property_name=property_name,
            keyword=keyword,
            operator="ne",
            conditional=conditional
        )

    def not_(self, property_name, keyword, conditional="and"):
        return self._operations(
            property_name=property_name,
            keyword=keyword,
            operator="not",
            conditional=conditional
        )

    def in_(self, property_name, keyword, conditional="and"):
        return self._operations(
            property_name=property_name,
            keyword=keyword,
            operator="in",
            conditional=conditional
        )

    # Relational operators
    def lt_(self, property_name, keyword, conditional="and"):
        return self._operations(
            property_name=property_name,
            keyword=keyword,
            operator="lt",
            conditional=conditional
        )

    def le_(self, property_name, keyword, conditional="and"):
        return self._operations(
            property_name=property_name,
            keyword=keyword,
            operator="le",
            conditional=conditional
        )

    def gt_(self, property_name, keyword, conditional="and"):
        return self._operations(
            property_name=property_name,
            keyword=keyword,
            operator="gt",
            conditional=conditional
        )

    def ge_(self, property_name, keyword, conditional="and"):
        return self._operations(
            property_name=property_name,
            keyword=keyword,
            operator="ge",
            conditional=conditional
        )

    # Lambda operators
    def any_(self):
        pass

    def all_(self):
        pass

    # Functions
    def starts_with(self, property_name, keyword, conditional="and"):
        return self._functions(
            property_name=property_name,
            keyword=keyword,
            function_name="startsWith",
            conditional=conditional
        )

    def ends_with(self, property_name, keyword, conditional="and"):
        return self._functions(
            property_name=property_name,
            keyword=keyword,
            function_name="endsWith",
            conditional=conditional
        )

    def contains(self, property_name, keyword, conditional="and"):
        return self._functions(
            property_name=property_name,
            keyword=keyword,
            function_name="contains",
            conditional=conditional
        )

    def __str__(self):
        return str(self.query.strip())

    def __call__(self):
        return self.__repr__()

    def __bool__(self):
        return self.query is not None
