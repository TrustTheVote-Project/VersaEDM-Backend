from pydantic import constr, BaseModel, Field


def fieldname_alias(python_fieldname: str) -> str:
    if python_fieldname.startswith('obj_'):
        return '@' + python_fieldname[4:]
    else:
        return ''.join(word.capitalize() for word in python_fieldname.split('_'))


class ObjectId(BaseModel):
    __root__: constr(regex=r'[A-Za-z_][A-Za-z0-9._-]*', min_length=1) = Field(
        ..., description='An xsi:idref datatype'
    )

    def __str__(self):
        return str(self.__root__)

    def __repr__(self):
        return repr(self.__root__)

    def __eq__(self, other):
        return self.__root__ == other

    def __hash__(self):
        return hash(self.__root__)


class ObjectIdRef(BaseModel):
    __root__: constr(regex=r'[A-Za-z_][A-Za-z0-9._-]*', min_length=1) = Field(
        ..., description='An xsi:idref datatype'
    )

    def __str__(self):
        return str(self.__root__)

    def __repr__(self):
        return repr(self.__root__)

    def __eq__(self, other):
        return self.__root__ == other

    def __hash__(self):
        return hash(self.__root__)
