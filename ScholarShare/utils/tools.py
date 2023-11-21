from django.forms import model_to_dict


def list_model_to_dict(models, fields=None):
    dict_list = []
    for each in models:
        dict_list.append(model_to_dict(each, exclude=fields))
    return dict_list
