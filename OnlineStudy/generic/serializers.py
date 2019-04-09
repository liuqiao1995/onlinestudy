from rest_framework import serializers
from generic import models


class CategorySerializer(serializers.ModelSerializer):
    """课程分类"""

    class Meta:
        model = models.Category
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """课程"""
    status = serializers.CharField(source='get_status_display')
    lesson = serializers.CharField(source='coursedetail.lesson')
    price = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()
    free_course = serializers.SerializerMethodField()

    def get_price(self, obj):
        """返回最低价"""
        return obj.price_policy.all().order_by('price').first().price

    def get_teacher(self, obj):
        """获取讲师"""
        res = obj.coursedetail.teacher.all()
        return [{"username": teacher.username, "title": teacher.title} for teacher in res]

    def get_free_course(self, obj):
        res = obj.course_chapters.all().first().course_lesson.all()
        return [{"title": lesson.title} for lesson in res if lesson.free_trail]

    class Meta:
        model = models.Course
        fields = ['id', 'title', 'course_img', 'status', 'study_number', 'price',
                  'lesson', 'teacher', 'free_course']


class CourseDetailSerializer(serializers.ModelSerializer):
    """课程详情"""
    title = serializers.CharField(source='course.title')
    course_img = serializers.CharField(source='course.course_img')
    study_number = serializers.CharField(source='course.study_number')
    difficult = serializers.CharField(source='course.difficult')
    price = serializers.SerializerMethodField()
    course_outline = serializers.SerializerMethodField()

    def get_price(self, obj):
        """价格"""
        return obj.course.price_policy.all().order_by('price').first().price

    def get_course_outline(self, obj):
        """大纲"""
        res = obj.course_outline.all()
        return [{"content": courseOutline.content} for courseOutline in res]

    class Meta:
        model = models.CourseDetail
        fields = ['title', 'course_img', 'study_number', 'difficult', 'price',
                  'lesson', 'teacher', 'brief', 'why_study','slogan',
                  'point', 'course_outline', 'harvest', 'object_person',
                  'prerequisite']


class ChapterSerializer(serializers.ModelSerializer):
    """课程章节、全部课时"""
    chapter_lesson = serializers.SerializerMethodField()

    def get_chapter_lesson(self, obj):
        res = obj.course_lesson.all().order_by('order')
        return [{"id": cou_les.id, "title": cou_les.title, 'free_trail': cou_les.free_trail} for cou_les in res]

    class Meta:
        model = models.CourseChapter
        fields = ['id', 'title', 'chapter_lesson']


class CommentSerializer(serializers.ModelSerializer):
    """用户评论"""
    account = serializers.CharField(source='account.username')

    class Meta:
        model = models.Comment
        fields = ['id', 'account', 'comment_date', 'content']


class CommonQuestionSerializer(serializers.ModelSerializer):
    """常见问题"""

    class Meta:
        model = models.CommonQuestion
        fields = ['id', 'question', 'answer']