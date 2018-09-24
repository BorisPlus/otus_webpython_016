from django.utils.html import mark_safe, format_html_join, escape


def a(title=None, text=None, href=None, css_class=None):
    def decorator(decorate_me):
        def wrapper(self, obj):
            return mark_safe(
                '<a href="{href}" title="{title}" class="{css_class}">{text}</a>'.format(
                    href=href or decorate_me(self, obj),
                    title=title or decorate_me(self, obj),
                    text=text or decorate_me(self, obj),
                    css_class=css_class or "undef_css_class",
                )
            )

        return wrapper

    return decorator


def img(src=None, alt=None, width=None, css_class=None):
    def decorator(decorate_me):
        def wrapper(self, obj):
            return mark_safe(
                '<img alt="{alt}" src="{src}" width="{width}" class="{css_class}">'.format(
                    src=src or decorate_me(self, obj),
                    alt=alt or decorate_me(self, obj),
                    width=width or "150",
                    css_class=css_class or "undef_css_class",
                )
            )

        return wrapper

    return decorator


def html_list(row_format, seporator='<br>'):
    def decorator(decorate_me):
        def wrapper(self, obj):
            rows = []
            for item in decorate_me(self, obj):
                row = []
                for cell in item:
                    row.append(escape(cell))
                rows.append(tuple(row))
            return format_html_join(
                mark_safe(seporator),
                row_format,
                tuple(rows),
            )

        return wrapper

    return decorator
