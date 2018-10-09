from django.contrib import admin
from django.contrib.admin.widgets import AdminURLFieldWidget


class ImageWidget(AdminURLFieldWidget):
    template_name = 'admin/widgets/img.html'


class ImagedModelAdmin(admin.ModelAdmin):
    image_fields = []

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.image_fields:
            request = kwargs.pop("request", None)
            kwargs['widget'] = ImageWidget
            return db_field.formfield(**kwargs)
        return super(ImagedModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)