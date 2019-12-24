from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, FormView, TemplateView

from vcs.forms import StudentLoginForm, LectureCommentForm, PredictScoreForm
from vcs.models import LectureActivity, Lecture, LectureComment, LecturePack, TotalLectureActivities

import numpy as np
from sklearn.svm import SVC
from random import randint, random


def get_dataset():
    views_list = []
    comments_list = []
    likes_list = []

    scores_list = []

    for _ in range(1000):
        views = randint(0, 50)
        comments = randint(0, 50)
        likes = randint(0, 50)

        if any(criterion > 10 for criterion in [views, comments, likes]):
            score_range = np.random.choice(4, 1, p=[0.05, 0.2, 0.4, 0.35])[0]
        elif comments > 15:
            score_range = np.random.choice(4, 1, p=[0.05, 0.15, 0.5, 0.3])[0]
        elif views > 40:
            score_range = np.random.choice(4, 1, p=[0.05, 0.15, 0.4, 0.4])[0]
        elif likes > 25:
            score_range = np.random.choice(4, 1, p=[0.05, 0.15, 0.6, 0.2])[0]
        elif views + comments + likes > 10:
            score_range = np.random.choice(4, 1, p=[0, 0.3, 0.4, 0.3])[0]
        else:
            score_range = np.random.choice(4, 1, p=[0, 0.5, 0.35, 0.15])[0]

        if score_range == 0:
            score = randint(0, 25)
        elif score_range == 1:
            score = randint(26, 50)
        elif score_range == 2:
            score = randint(51, 75)
        elif score_range == 3:
            score = randint(76, 100)

        views_list.append(views)
        comments_list.append(comments)
        likes_list.append(likes)

        scores_list.append(score)

    for v, c, l, s in zip(
        views_list, comments_list, likes_list, scores_list
    ):
        TotalLectureActivities.objects.create(
            views=v,
            comments=c,
            likes=l,
            score=s
        )


get_dataset()


class StudentLoginView(FormView):
    form_class = StudentLoginForm
    template_name = 'student_login.html'
    success_url = reverse_lazy('lecture_list')

    def form_valid(self, form):
        validated_data = form.cleaned_data

        user = authenticate(email=validated_data["email"], password=validated_data["password"])
        login(self.request, user)

        return super().form_valid(form)


class LectureList(ListView):
    template_name = 'lecture_list.html'

    def get_queryset(self):
        group = self.request.user.university_group
        if group:
            return group.lectures.all()
        return self.request.user.teacher_lectures.filter(version=1)


class LectureDetail(DetailView, CreateView):
    template_name = 'lecture_detail.html'
    model = Lecture
    form_class = LectureCommentForm

    def get_form(self, form_class=None):
        return form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        likes = LectureActivity.objects.filter(lecture=self.object, like=True).count()
        context["likes"] = likes
        context["other_versions"] = Lecture.objects\
            .filter(Q(original_lecture=self.object))\
            .exclude(id=self.object.id)
        context["form"] = self.form_class

        activity, _ = LectureActivity.objects.get_or_create(student=self.request.user, lecture=self.object)
        activity.view_count += 1
        if 'like' in self.request.GET.keys():
            if activity.like:
                activity.like = False
            else:
                activity.like = True

        activity.save()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form):
        LectureComment.objects.create(text=form.cleaned_data["text"], user=self.request.user, lecture=self.get_object())

        return HttpResponseRedirect(self.request.path)


class LecturePackList(ListView):
    model = LecturePack
    template_name = 'lecture_pack_list.html'

    def get_queryset(self):
        return LecturePack.objects.all()


class LecturePackDetail(DetailView):
    model = LecturePack
    template_name = 'lecture_pack_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lectures'] = self.object.lecture_set.all()
        return context


class PredictScore(FormView):
    template_name = 'predict_score.html'
    form_class = PredictScoreForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_act = TotalLectureActivities.objects.all().iterator()

        X, y = [], []
        for a in all_act:
            X.append([a.views, a.comments, a.likes])
            y.append([a.score])

        clf = SVC(gamma='auto')
        clf.fit(
            X,
            y,
        )
        SVC(gamma='auto')

        # print(clf.predict([[50, 50, 50]]))

        initial = self.get_initial()
        context['prediction'] = clf.predict([[
            initial['views'],
            initial['comments'],
            initial['likes']
        ]])

        return context

    def get_initial(self):
        initial = self.initial.copy()

        if not initial:
            views = 0
            comments = LectureComment.objects.filter(user=self.request.user, lecture_id=self.kwargs['lecture_id']).count()
            likes = 0
            for a in LectureActivity.objects.filter(student=self.request.user, lecture_id=self.kwargs['lecture_id']):
                views += a.view_count
                likes += int(a.like)

            return {'views': views, 'comments': comments, 'likes': likes}
        return initial
