"""Purpose of this file

This file contains forms associated with the content types.
"""

from django import forms
from django.forms import modelformset_factory

from content.models import YTVideoContent, ImageContent, PDFContent, ImageAttachment, TextField, Latex, SingleImage


class AddContentFormYoutubeVideo(forms.ModelForm):
    """Add YouTube video

    This model represents the add form for YouTube videos.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
        """
        model = YTVideoContent
        exclude = ['content']


class AddContentFormImage(forms.ModelForm):
    """Add image content

    This model represents the add form for image contents.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
            Meta.widgets (Dict[str, Textarea]): Customization of the model form
        """
        model = ImageContent
        exclude = ['content']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px'}),
        }


class AddContentFormAttachedImage(forms.ModelForm):
    """Add attached image

    This model represents the add form for image attachments
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
        """
        model = ImageAttachment
        exclude = ['images', 'content']


class AddContentFormPdf(forms.ModelForm):
    """Add PDF content

    This model represents the add form for PDF contents.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
            Meta.widgets (Dict[str, Textarea]): Customization of the model form
        """
        model = PDFContent
        exclude = ['license', 'content']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px'}),
            'pdf': forms.FileInput(attrs={'accept': 'application/pdf'}),
        }


class AddTextField(forms.ModelForm):
    """Add text field

    This model represents the add form for text fields.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
            Meta.widgets (Dict[str, Textarea]): Customization of the model form
        """
        model = TextField
        exclude = ['content']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px', 'placeholder': 'https://www.uni-bielefeld.de'
                                                                                     '/lili/forschung/projekte/archiv'
                                                                                     '/L2-pro/text.html'}),
            'textfield': forms.Textarea(attrs={'placeholder': 'Den Körper trainieren viele Menschen. Aber wer '
                                                              'trainiert auch sein Gehirn? „Das Gehirn muss genauso '
                                                              'trainiert werden wie der Körper“, sagt Professor '
                                                              'Siegfried Lehrl von der Universität '
                                                              'Erlangen-Nürnberg. Denn wissenschaftliche '
                                                              'Untersuchungen haben gezeigt, dass wir die '
                                                              'Leistungsfähigkeit unseres Gehirns um 10 bis 15% '
                                                              'steigern können, wenn wir einige Wochen lang täglich '
                                                              'zehn Minuten unser Gehirn trainieren.'})
        }


class AddLatex(forms.ModelForm):
    """Add LaTeX

    This model represents the add form for LaTeX code.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
            Meta.widgets (Dict[str, Textarea]): Customization of the model form
        """
        model = Latex
        exclude = ['content', 'pdf']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px', 'placeholder': 'https://ctan.org/pkg/lipsum'}),
            'textfield': forms.Textarea(
                attrs={
                    'placeholder': 'This is a matrix \\\\ \n '
                                   '$ M = \\begin{pmatrix} 1 & 2 & 3\\\\ a & b & c \\end{ pmatrix}$ \\\\ \n'
                                   'This is a table \\\\ \n '
                                   '\\begin{center} \n \\begin{tabular} {||c c c c||} \n \\hline'
                                   'Col1 & Col2 & Col2 & Col3 \\\\ [0.5ex] \n \\hline \n \\hline \n '
                                   '1 & 6 & 87837 & 787 \\\\ \n \\hline \n'
                                   '\\end{tabular} \n \\end{center}'})
        }


class AddSingleImage(forms.ModelForm):
    """Add single image

    This model represents the add form for single images that is used for image attachments.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
            Meta.widgets (Dict[str, Textarea]): Customization of the model form
        """
        model = SingleImage
        exclude = []
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px'}),
        }


# SingleImageFormSet: Image attachment form set
SingleImageFormSet = modelformset_factory(
    SingleImage,
    fields=("source", "license", "image"),
    extra=0,
    widgets={
        'source': forms.Textarea(attrs={'style': 'height: 25px', 'required': 'true'}),
        'image': forms.FileInput(attrs={'required': 'true'})
    }
)

# Dict[str, ModelForm]: Contains all available content types form.
CONTENT_TYPE_FORMS = {
    YTVideoContent.TYPE: AddContentFormYoutubeVideo,
    ImageContent.TYPE: AddContentFormImage,
    PDFContent.TYPE: AddContentFormPdf,
    ImageAttachment.TYPE: AddContentFormAttachedImage,
    TextField.TYPE: AddTextField,
    Latex.TYPE: AddLatex,
    SingleImage.TYPE: AddSingleImage
}
