from .models import Patient

def getPatientIDByUserID(user_id):
    try:
        patient=Patient.objects.get(user_id=user_id)
        return patient.id
    except Patient.DoesNotExist:
        return None
