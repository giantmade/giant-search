def is_page_title(obj):
    """
    Determine if the given object is a Django CMS Page Title model instance.
    """

    from cms.models import Title
    return isinstance(obj, Title)


def is_cms_plugin(obj):
    """
    Determine if the given object is a Django CMS Plugin model instance.
    """

    from cms.models import CMSPlugin
    return isinstance(obj, CMSPlugin)
