from django.shortcuts import get_object_or_404
import subprocess, datetime
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Question, Choice
from .serializers import QuestionListPageSerializer, QuestionDetailPageSerializer, ChoiceSerializer, VoteSerializer, QuestionResultPageSerializer


@api_view(['GET', 'POST'])
def questions_view(request): #Handle cases where no q_text inputted; Redirect to 400: Bad Request
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionListPageSerializer(questions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionListPageSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionListPageSerializer(question).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def multiple_questions_view(request):
    serializer = QuestionListPageSerializer(many=True, data=request.data)
    if serializer.is_valid():
        questions = serializer.save()
        return Response(QuestionDetailPageSerializer(questions, many=True).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def question_detail_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'GET':
        serializer = QuestionDetailPageSerializer(question)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = QuestionDetailPageSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionDetailPageSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response("Question deleted", status=status.HTTP_204_NO_CONTENT)

# class multiple_choices_View(viewsets.ModelViewSet):
#
#     queryset = Choice.objects.all()
#     serializer_class = ChoiceSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['POST'])
def choices_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if len(request.data) >= 2:
        serializer = ChoiceSerializer(data=request.data)
        split_texts = [x.strip() for x in data.split(",")]

        def create_multiple(self, validated_data):
            x = 0
            for t in split_texts:
                return Choice.objects.create(**validated_data)

                if serializer.is_valid():
                    choice = serializer.save(question=question+x)
                    x+=1
                    return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)
    else:
        serializer = ChoiceSerializer(data=request.data)

        if serializer.is_valid():
            choice = serializer.save(question=question)
            return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
def vote_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():

        try:
            choice = get_object_or_404(Choice, pk=serializer.validated_data['choice_id'], question=question)
            choice.votes += 1
            choice.save()
            return Response(choice.votes)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            # raise ValidationError({'voteError': 'No choices exist for this particular question.'
            #     })
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            raise ValidationError({'voteError': 'No choices exist for this particular question.'
                })
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def question_result_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = QuestionResultPageSerializer(question)
    return Response(serializer.data)

@api_view(['GET'])
def uptime_view(request):
    output = subprocess.check_output(['sh', '/app/polls/time.sh'])
    return Response(output)
    output = output.split()
    dates = output[0].decode().split('-')
    times = output[1].decode().split(':')
    print(dates, times)
    year = int(dates[0])
    month = int(dates[1])
    day = int(dates[2])
    hour = int(times[0])
    mins = int(times[1])
    sec = int(times[2])
    d = datetime.datetime(year, month, day, hour, mins, sec)
    isoformat = d.now(timezone.utc).astimezone().isoformat()
    return Response("{"+ "'dateTime'" + ": " "'" + str(isoformat) + "'"+ "}")
