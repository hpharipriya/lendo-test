from celery import shared_task
# from .models import AdditionResult, CustomerApplication

result = 1

@shared_task
def add_numbers():
    global result
    print("Running add numbers periodic task")
    result = result
    print("Hello Sony result is :", result)
    print("jj")

    # AdditionResult.objects.create(answer=result)


## Todo ## get applications in pending status from database and send request to corresponding bank APIs.
#
# @shared_task
# def check_application_status():
#   # DB model call to fetch all pending applications.
    # Identify corresponding banks from related model.
    # Make Bank API calls
    # based on the status, update application status in db
    # else put in the queue again.

    # get_all_pending_apps_details()

#     new_status = " " # status from Bank API
#     print("Check the application status")
#     result += result
#     print("Hello Sony!!")
#     print("jhhhj")
#     c = CustomerApplication.objects.get(pk=id)
#     c.status = new_status
#     c.save()
