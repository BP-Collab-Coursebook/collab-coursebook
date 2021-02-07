"""Purpose of this file

This file describes the frontend views related to course.
"""

from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _

from base.models import Course, CourseStructureEntry, Topic
from base.utils import check_owner_permission

from frontend.forms import AddAndEditCourseForm, FilterAndSortForm
from frontend.forms.course import TopicChooseForm, AddTopicForm

import json
from .json_handler import JsonHandler
from django.shortcuts import render


class DuplicateCourseView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Duplicate course view

     Duplicates a course.

    :attr DuplicateCourseView.model: The model of the view
    :type DuplicateCourseView.model: Model
    :attr DuplicateCourseView.template_name: The path to the html template
    :type DuplicateCourseView.template_name: str
    :attr DuplicateCourseView.form_class: The form class of the view
    :type DuplicateCourseView.form_class: Form
    :attr DuplicateCourseView.success_url: Redirection of a successful url
    :type DuplicateCourseView.success_url: __proxy__
    """
    model = Course
    template_name = 'frontend/course/duplicate.html'
    form_class = AddAndEditCourseForm
    success_url = reverse_lazy('frontend:dashboard')

    def get_success_message(self, cleaned_data):
        """Success message

        Returns the success message after the duplicating of a new course was successful.

        :param cleaned_data: The cleaned data
        :type cleaned_data: dict

        :return: the success message
        :rtype: __proxy__
        """
        original_course = Course.objects.get(pk=self.get_object().id)
        return _(
            f"Course '{cleaned_data['title']}' successfully created. "
            f"All settings and contents of the course "
            f"'{original_course.title}' were copied.")

    def get_initial(self):
        """Initial

        Returns the current user to the initial of the owner field.

        :return: the initial data
        :rtype: dict
        """
        course_to_duplicate = Course.objects.get(pk=self.get_object().id)
        data = course_to_duplicate.__dict__
        # set data not included in the dict
        data['owners'] = get_user(self.request)
        data['image'] = course_to_duplicate.image
        # this data has the wrong key
        data['category'] = course_to_duplicate.category
        data['period'] = course_to_duplicate.period
        return data

    def form_valid(self, form):
        """Form validation

        Saves the filters and sorting from the form.

        :param form: The form that contains the filter and the sorting
        :type form: FilterAndSortForm

        :return: Itself rendered to a response
        :rtype: HttpResponse
        """
        duplicated_course = form.save()
        original_course = Course.objects.get(pk=self.get_object().id)
        course_structure_entries = CourseStructureEntry.objects.filter(course=original_course)
        # duplicate course structure entries
        for entry in course_structure_entries:
            entry.pk = None
            entry.course = duplicated_course
            entry.save()
        return super().form_valid(form)


# pylint: disable=too-many-ancestors
class AddCourseView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Add course view

    Adds a new course to the database

    :attr AddCourseView.model: The model of the view
    :type AddCourseView.model: Model
    :attr AddCourseView.template_name: The path to the html template
    :type AddCourseView.template_name: str
    :attr AddCourseView.form_class: The form class of the view
    :type AddCourseView.form_class: Form
    :attr AddCourseView.success_url: Redirection of a successful url
    :type AddCourseView.success_url: __proxy__
    """
    model = Course
    template_name = 'frontend/course/create.html'
    form_class = AddAndEditCourseForm
    success_url = reverse_lazy('frontend:dashboard')

    def get_success_message(self, cleaned_data):
        """Success message

        Returns the success message after the addition of a new course was successful.

        :param cleaned_data: The cleaned data
        :type cleaned_data: dict

        :return: the success message
        :rtype: __proxy__
        """
        return _(f"Course '{cleaned_data['title']}' successfully created")

    def get_initial(self):
        """Initial

        Returns the current user to the initial of the owner field.

        :return: the initial data
        :rtype: dict
        """
        initial = super().get_initial()
        initial['owners'] = get_user(self.request).profile
        return initial


class EditCourseView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Edit course view

    Displays the edit course page

    :attr EditCourseView.model: The model of the view
    :type EditCourseView.model: Model
    :attr EditCourseView.template_name: The path to the html template
    :type EditCourseView.template_name: str
    :attr EditCourseView.form_class: The form class of the view
    :type EditCourseView.form_class: Form
    """
    model = Course
    template_name = 'frontend/course/edit.html'
    form_class = AddAndEditCourseForm

    def get_success_url(self):
        """Success URL

        Returns the url for successful editing.

        :return: The url of the content to which the edited argument
        belonged
        :rtype: str
        """
        course_id = self.get_object().id
        return reverse('frontend:course', args=(course_id,))

    def get_success_message(self, cleaned_data):
        """Success message

        Returns the success message after the editing was successful.

        :param cleaned_data: The cleaned data
        :type cleaned_data: dict

        return: the success message
        rtype: __proxy__
        """
        return _(f"Course '{cleaned_data['title']}' successfully edited")



#TODO <Iteration 4>
def edit_course_structure(request, pk):
    """
    For editing the Course structure. It is displayed in a drag and droppable view.
    :param HttpRequest request: The given request
    :param int pk: the id of the course whose structure should be edited
    :return: It renders the response if there is no post, if there was it redirects
    to the course view
    :rtype: HttpResponse
    """
    course = Course.objects.get(pk=pk)

    # Topics
    # create_structure_from_form(request, add_topic_formset, created_course)
    pkList = []
    for owner in course.owners.all():
        pkList.append(owner.pk)

    if get_user(request).pk not in pkList:
        messages.error(request, "You don't have permission to do this.",
                       extra_tags="alert-danger")
        return HttpResponseRedirect(reverse('frontend:course', args=(pk,)))

    if request.method == 'POST':
        print(request.POST)
        json_topic_list = request.POST.get('topic_list')

        data = json.loads(json_topic_list)
        CourseStructureEntry.objects.filter(course=course).delete()
        JsonHandler.create_structures_from_json_data(course, data)

        return HttpResponseRedirect(reverse('frontend:course', args=(course.id,)))

    if request.GET.get('duplicate'):
        duplicate_course = Course.objects.get(pk=request.GET.get('duplicate'))
        json_response = JsonHandler.create_json_topics_structure(duplicate_course)
    else:
        json_response = JsonHandler.create_json_topics_structure(course)

    course = Course.objects.get(pk=pk)
    return render(request, 'frontend/course/edit_course_structure.html',
                  {'course': course, 'form': TopicChooseForm,
                   'existing_structure': json.dumps(json_response)})


#TODO <Iteration 4>
class AddTopicView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    #TODO
    """
    model = Topic
    template_name = 'frontend/course/add_topic.html'
    form_class = AddTopicForm

    def get_success_message(self, cleaned_data):
        """Success message

        Returns the success message after the addition of a new topic was successful.

        :param cleaned_data: The cleaned data
        :type cleaned_data: dict

        :return: the success message
        :rtype: __proxy__
        """
        return _(f"Topic '{cleaned_data['title']}' successfully created")


    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            topic = form.save(commit=False)
            topic.save()
            course_id = self.kwargs['pk']
            return HttpResponse('<script type="text/javascript">window.close(); window.opener.parent.location.reload(true);</script>')

        else:
            return self.form_invalid(form)




# pylint: disable=too-many-ancestors
class CourseView(DetailView, FormMixin):
    """Course list view

    Displays the course detail page

    :attr CourseView.model: The model of the view
    :type CourseView.model: Model
    :attr CourseView.template_name: The path to the html template
    :type CourseView.template_name:str
    :attr CourseView.form_class: The form class of the view
    :type CourseView.form_class: Form
    :attr CourseView.context_object_name: The context object name
    :type CourseView.context_object_name: str
    """
    template_name = 'frontend/course/view.html'
    model = Course
    form_class = FilterAndSortForm
    context_object_name = "course"

    def __init__(self):
        self.sorted_by = 'None'
        self.filtered_by = 'None'
        super().__init__()

    # pylint: disable=unused-argument
    def post(self, request, *args, **kwargs):
        """Post

        Defines what happens after form is posted. Sets object and the checks if form is valid

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict

        :return: The result from form_valid / form_invalid depending on the result from is_valid
        :rtype: TemplateResponse
        """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        """Form validation

        Saves the filters and sorting from the form.

        :param form: The form that contains the filter and the sorting
        :type form: FilterAndSortForm

        :return: Itself rendered to a response
        :rtype: HttpResponse
        """
        self.sorted_by = form.cleaned_data['sort']
        self.filtered_by = form.cleaned_data['filter']
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        """Context data

        Gets the  context data for the page.

        :param kwargs: The keyword arguments
        :type kwargs: dict

        :return: The context
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        structure_entries = CourseStructureEntry. \
            objects.filter(course=context["course"]).order_by('index')

        topics_recursive = []
        current_topic = None
        for entry in structure_entries:
            index_split = entry.index.split('/')
            # Topic
            if len(index_split) == 1:
                current_topic = {'topic': entry.topic, 'subtopics': [],
                                 'topic_contents': entry.topic.get_contents(self.sorted_by,
                                                                            self.filtered_by)}
                topics_recursive.append(current_topic)
            # Subtopic
            # Only handle up to one subtopic level
            else:
                current_topic["subtopics"].append({'topic': entry.topic,
                                                   'topic_contents':
                                                       entry.topic.
                                                  get_contents(self.sorted_by, self.filtered_by)})

        context["structure"] = topics_recursive
        context['isCurrentUserOwner'] = self.request.user.profile in context['course'].owners.all()

        if self.sorted_by is not None:
            context['sorting'] = self.sorted_by
        if self.filtered_by is not None:
            context['filtering'] = self.filtered_by

        """# create a list of topics ordered by (sub-)topic and index
        flat_topic_list = create_topic_and_subtopic_list(topics, super().get_object())
        print(flat_topic_list)
        context['topics'] = flat_topic_list
        # create a list of files for each (sub-)topic
        files = []
        for _, topic, _ in flat_topic_list:
            files.append(topic.get_contents(self.sorted_by, self.filtered_by))

        context['files'] = files
        # context['Content'] = Content
        if self.sorted_by is not None:
            context['sorting'] = self.sorted_by
        if self.filtered_by is not None:
            context['filtering'] = self.filtered_by
        
        if self.request.user.is_authenticated:
            context['coursebook_length'] = models.get_coursebook_length(user=get_user(self.request), course=self.object)
            context['coursebook'] = models.get_coursebook(get_user(self.request), self.object)
            missing_topics = [x.title for x in self.object.topic_list.order_by('child_topic__index')
                              if Favourite.objects.filter(user=get_user(self.request),
                                                          course=self.object, topic=x).count() == 0
                              or Favourite.objects.get(user=get_user(self.request),
                                                       course=self.object,
                                                       topic=x).content_list.all().count() == 0]
            context['missing_topics'] = ", ".join(missing_topics)
        """

        return context


# pylint: disable=too-many-ancestors
class CourseDeleteView(LoginRequiredMixin, DeleteView):
    """Course delete view

    Deletes the user and redirects to course list

    :attr CourseDeleteView.model: The model of the view
    :type CourseDeleteView.model: Model
    :attr CourseDeleteView.template_name: The path to the html template
    :type CourseDeleteView.template_name: str
    """
    model = Course
    template_name = 'frontend/course/delete_course_confirm.html'

    def get_success_url(self):
        """Success url

        Returns the url to return to after successful delete

        :return: the success url
        :rtype: str
        """
        return reverse_lazy('frontend:dashboard')

    # Check if the user is allowed to view the delete page
    def dispatch(self, request, *args, **kwargs):
        """Dispatch

        Overwrites dispatch: Check if a user is allowed to visit the page.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict

        :return: the response to redirect to overview of the course if the user is not owner
        :rtype: HttpResponse
        """
        if check_owner_permission(request, self.get_object(), messages):
            return HttpResponseRedirect(reverse_lazy('frontend:course',
                                                     args=(self.get_object().id,)))
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete

        Deletes the course when the user clicks the delete button

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict

        :return: the redirect to success url (course list)
        :rtype: HttpResponse
        """

        messages.success(request, "Course '" + self.get_object().title +
                         "' successfully deleted", extra_tags="alert-success")
        return super().delete(self, request, *args, **kwargs)
