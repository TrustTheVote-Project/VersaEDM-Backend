from pydantic import constr, BaseModel, Field


def fieldname_alias(python_fieldname: str) -> str:
    if python_fieldname.startswith('_'):
        return '@' + python_fieldname[1:]
    else:
        return ''.join(word.capitalize() for word in python_fieldname.split('_'))


class ObjectId(BaseModel):
    __root__: constr(regex=r'[A-Za-z_][A-Za-z0-9._-]*', min_length=1) = Field(
        ..., description='An xsi:idref datatype'
    )


class ObjectIdRef(BaseModel):
    __root__: constr(regex=r'[A-Za-z_][A-Za-z0-9._-]*', min_length=1) = Field(
        ..., description='An xsi:idref datatype'
    )