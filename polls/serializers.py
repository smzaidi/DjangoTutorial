from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Question, Choice
from rest_framework.response import Response
from django.http import HttpResponseBadRequest

class ChoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    choice_text = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Choice.objects.create(**validated_data)


class ChoiceSerializerWithVotes(ChoiceSerializer):
    votes = serializers.IntegerField(read_only=True)

# class MultipleChoiceSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     choice_texts = serializers.Charfield(max_length=200)
#     split_texts = [x.strip() for x in choice_texts.split(",")]
#
#     def create_multiple(self, validated_data):
#         for t in split_texts:
#             return Choice.objects.create(**validated_data)

class QuestionListPageSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    question_text = serializers.CharField(max_length=200, required=True)
    pub_date = serializers.DateTimeField()
    # was_published_recently = serializers.BooleanField(read_only=True) # Serializer is smart enough to understand that was_published_recently is a method on Question
    #Remember that was was_published_recently was disabled for the test run
    choices = ChoiceSerializer(many=True, write_only=True, required=False)

    if len(str(question_text)) == 0:
        raise ValidationError({'questionError': 'Question must be inputted when making a POST request.'})
    elif not question_text: #If question does not exist
        raise ValidationError({'questionError': 'Question must be inputted when making a POST request.'})

    def create(self, validated_data):
        choices = validated_data.pop('choices', [])

        if len(choices) <= 1:
            # return HttpResponseBadRequest()
            raise ValidationError({
            'choiceError': 'Two or more choices are required per question added.'
            })
        else:
            question = Question.objects.create(**validated_data)
            for choice_dict in choices:
                choice_dict['question'] = question
                Choice.objects.create(**choice_dict)
            return question

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionDetailPageSerializer(QuestionListPageSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)


class QuestionResultPageSerializer(QuestionListPageSerializer):
    choices = ChoiceSerializerWithVotes(many=True, read_only=True)
    max_voted_choice = ChoiceSerializerWithVotes(read_only=True)


class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField(required=False)
