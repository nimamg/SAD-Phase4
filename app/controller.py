from app.insurance_checker import Insurance
from app.models import (TestDescription, Laboratory, Address, TimeSlot, Patient,
                        Appointment, Payment, TestRequest, Test)
from app.payment_handler import PaymentHandler
from app.dao import DAO


class TestRequestHandler:
    @staticmethod
    def get_test_descriptions():
        result = []
        for test in DAO.get_list_of_all_test_descriptions():
            result.append({'id': test.id, 'name': test.name})
        return result

    @staticmethod
    def get_labs_and_prices(test_ids, patient_id):
        patient = Patient.objects.get(id=patient_id)
        proper_labs = [lab for lab in Laboratory.objects.all() if lab.has_every_test(test_ids)]

        data = list()
        for lab in proper_labs:

            data_instance = dict()
            data_instance['id'] = lab.id
            data_instance['name'] = lab.name

            lab_total_cost = 0
            for test_id in test_ids:
                lab_total_cost += Insurance.get_price(lab.tests.get(test_description_id=test_id), patient)

            data_instance['price'] = lab_total_cost
            data.append(data_instance)
        return data

    @staticmethod
    def get_list_of_addresses(patient_id):
        patient = Patient.objects.get(id=patient_id)
        address_list = patient.get_list_of_addresses()
        result = []
        for address in address_list:
            result.append({'address': address.address, 'id': address.id})
        return result

    @staticmethod
    def create_new_address(data):
        address = Address.objects.create(
            **data
        )
        return address.id

    @staticmethod
    def get_time_slots(lab_id):
        lab = Laboratory.objects.get(id=lab_id)
        time_slots_list = lab.get_list_of_time_slots()
        result = []
        for time_slot in time_slots_list:
            result.append({
                'id': time_slot.id,
                'date': (
                        str(time_slot.start_date.date()) + ' '
                        + time_slot.start_date.strftime('%H:%M') + '-'
                        + time_slot.end_date.strftime('%H:%M')
                )
            })
        return result

    @staticmethod
    def create_test_request(data):
        patient = Patient.objects.get(id=data.get('patient'))

        laboratory = Laboratory.objects.get(id=data.get('laboratory'))

        lab_time_slot = TimeSlot.objects.get(
            id=data.get('time_slot'),
            expert__laboratory=laboratory,
            is_taken=False
        )

        address = Address.objects.get(
            id=data.get('address'),
            patient=patient
        )

        test_ids = data.get('tests')

        cost = 0
        for test_id in test_ids:
            cost += Insurance.get_price(laboratory.tests.get(test_description_id=test_id), patient)

        appointment = Appointment.objects.create(
            time_slot=lab_time_slot,
            address=address,
            patient=patient,
        )

        payment = Payment.objects.create(
            amount=cost,
            is_successful=False
        )

        test_request = TestRequest.objects.create(
            payment_request=payment,
            appointment=appointment
        )

        for test_id in test_ids:
            Test.objects.create(
                lab_test=laboratory.tests.get(test_description_id=test_id),
                test_request=test_request,
            )

        payment_url = PaymentHandler.get_payment_url(payment)

        return {
            'payment_url': payment_url,
            'cost': cost,
        }

    @staticmethod
    def update_payment_status(payment_id, success):
        payment = Payment.objects.get(id=payment_id)
        payment.update_state(success)