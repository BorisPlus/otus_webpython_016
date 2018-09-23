from django.contrib.admin.widgets import AdminURLFieldWidget


class ImageWidget(AdminURLFieldWidget):
    template_name = 'admin/widgets/img.html'
