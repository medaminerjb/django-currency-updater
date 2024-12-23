from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from .models import SchedulerSettings
from .updater import update_currency_rate

scheduler = None

def start_scheduler():
    """
    Start the background scheduler.

    This function will start the background scheduler and schedule the job if not already running.
    If the scheduler is already running, it will print a message indicating so and do nothing.
    If there are no scheduler settings, it will print a message indicating that automation is disabled and do nothing.

    :return: None
    """
    global scheduler
    if scheduler is not None:
        print("Scheduler is already running.")
        return

    scheduler_settings = SchedulerSettings.objects.first()
    if not scheduler_settings:
        print("No scheduler settings found. Automation is disabled.")
        return

    scheduler = BackgroundScheduler()
    schedule_params = scheduler_settings.get_schedule_params()

    scheduler.add_job(
        update_currency_rate,
        **schedule_params,
    )
    scheduler.start()
    print(f"Scheduler started with {schedule_params}.")

def stop_scheduler():
    global scheduler
    if scheduler:
        scheduler.shutdown()
        scheduler = None
        print("Scheduler stopped.")
