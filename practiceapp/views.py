from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .database import get_session
from .models import PracticeappPerson

class PersonAPI(APIView):
    def get(self, request):
        session = get_session()
        try:
            people = session.query(PracticeappPerson).all()
            people_data = [{'id': person.id, 'first_name': person.first_name, 'last_name': person.last_name, 'phone_number': person.phone_number} for person in people]
            return Response(people_data, status=status.HTTP_200_OK)
        finally:
            session.close()

    def post(self, request):
        session = get_session()
        try:
            new_person = PracticeappPerson(
                first_name=request.data.get('first_name'),
                last_name=request.data.get('last_name'),
                phone_number=request.data.get('phone_number')
            )
            session.add(new_person)
            session.commit()
            return Response({'status': 'Person added'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            session.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()

    def put(self, request, person_id):
        session = get_session()
        try:
            person = session.query(PracticeappPerson).filter_by(id=person_id).first()
            if person:
                person.first_name = request.data.get('first_name', person.first_name)
                person.last_name = request.data.get('last_name', person.last_name)
                person.phone_number = request.data.get('phone_number', person.phone_number)
                session.commit()
                return Response({'status': 'Person updated'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            session.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()

    def delete(self, request, person_id):
        session = get_session()
        try:
            person = session.query(PracticeappPerson).filter_by(id=person_id).first()
            if person:
                session.delete(person)
                session.commit()
                return Response({'status': 'Person deleted'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)
        finally:
            session.close()