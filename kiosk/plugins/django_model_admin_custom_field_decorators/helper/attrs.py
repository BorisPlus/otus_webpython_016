def fill_clever_attributes_dict(self, obj, **kwargs):
    attributes = dict()
    for k in kwargs:
        if kwargs.get(k).startswith('use_orm__'):
            object_orm_field_attempt = kwargs.get(k)[len('use_orm__'):]
            if hasattr(self, object_orm_field_attempt):
                object_admin_orm_field = getattr(self, object_orm_field_attempt)
                if callable(object_admin_orm_field):
                    v = object_admin_orm_field(obj)
                else:
                    v = object_admin_orm_field
            elif hasattr(obj, object_orm_field_attempt):
                object_orm_field = getattr(obj, object_orm_field_attempt)
                if callable(object_orm_field):
                    v = object_orm_field()
                else:
                    v = object_orm_field
            else:
                v = kwargs.get(k)
        else:
            v = kwargs.get(k)
        attributes[k] = v
    return attributes
