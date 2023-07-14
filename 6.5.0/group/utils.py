from django.contrib.auth.models import Permission


def get_action_name(name):
    """
    汉化
    :param name:
    :return:
    """
    name = name.replace('Can add ', '增加').replace('Can change ', '编辑').replace('Can delete ', '删除').replace('Can view ',
                                                                                                            '查看')
    return name


def get_permissions():
    """
    获取所有的权限
    :return:
    """
    all = Permission.objects.all()

    
    data = {}
    
    for item in all:
        label = item.content_type.app_label
        if label not in data:
            data[label] = {
                'label': label,
                'children': [item]
            }
        else:
            d = data.get(label)
            children = d.get('children')
            children.append(item)
        
    

    
    for key in data:
        item = data.get(key)
        children = item.get('children')
        

        obj = {}
        for i in children:
            
            label = i.content_type.name
            if label not in obj:
                obj[label] = {
                    'label': label,
                    'children': [{
                        'id': i.id,
                        'label': get_action_name(i.name)
                    }]
                }
            else:
                obj[label].get('children').append({
                    'id': i.id,
                    'label': get_action_name(i.name)
                })
        array = []
        for i in obj:
            array.append(obj.get(i))
        item['children'] = array

    jsonData = []
    for i in data:
        jsonData.append(data.get(i))

    return jsonData
